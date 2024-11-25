import random
from display import pause
from player import Player
from enemies import Enemy, ENEMY_ATTACK_TYPES, MONSTER_VARIANTS
from status_effects import *


class Battle:
    def __init__(self, player, items, game):
        self.player = player
        self.items = items
        self.game = game
        self.turn_counter = 0
        self.battle_ended = False
        self.enemy = None
        
    def player_attack(self, enemy):
        # First check for status effects that prevent attacking
        if self.handle_pre_attack_effects(enemy):
            return False, None

        # Get and validate attack choice
        attack_type, attack_info = self.get_player_attack_choice()
        if not attack_type:
            return False, None

        # Handle stamina cost
        if not self.handle_stamina_cost(attack_type, attack_info):
            return False, None

        # Apply any pre-attack buffs
        self.apply_attack_buffs(attack_info)

        # Perform the attack and get results
        message, total_damage, self_damage_info, attack_hit = self.player.perform_attack(enemy, attack_type)

        # Handle post-attack effects and cleanup
        self.handle_post_attack_effects(enemy, attack_hit, total_damage, attack_type, attack_info)

        # Remove temporary attack buffs
        self.remove_attack_buffs(attack_info)

        # Check battle ending conditions
        if self.check_battle_end(enemy):
            return True, None

        return False, self_damage_info

    def handle_pre_attack_effects(self, enemy):
        # Handle stun
        if self.player.stunned:
            print("You're stunned and lose your turn.")
            self.player.stunned = False
            self.player.remove_status_effect("Stun")
            if self.player.status_effects:
                self.player.update_status_effects(self.player)
            return True

        # Handle confusion
        confusion_effect = next((effect for effect in self.player.status_effects if effect.name == "Confusion"), None)
        if confusion_effect:
            if random.random() < 0.5:
                print("You're confused and attack yourself!")
                damage, hit_type, _, _ = self.player.calculate_damage(self.player, self.player, "normal")
                self.player.take_damage(damage)
                print(f"You dealt {damage} damage to yourself!")
                print("Your attack on yourself snaps you out of your confusion!")
                pause()
                self.player.remove_status_effect("Confusion")
                return True
            else:
                print(f"{self.player.name} snaps out of their confusion!")
                self.player.remove_status_effect("Confusion")

        # Handle freeze
        frozen_effect = next((effect for effect in self.player.status_effects if effect.name == "Freeze"), None)
        if frozen_effect:
            if random.random() < 0.5:
                print("You're frozen and cannot attack!")
                self.enemy_attack(enemy)
                pause()
                return True
            else:
                print(f"{self.player.name} thaws out from the ice and attacks!")
                self.player.remove_status_effect("Freeze")

        return False

    def get_player_attack_choice(self):
        """Get player's attack choice and return attack type and info"""
        self.player.display_attack_options()
        available_attacks = self.player.get_available_attack_types()
        
        while True:
            choice = input(f"\nEnter your choice (1-{len(available_attacks)}): ")
            if choice.isdigit() and 1 <= int(choice) <= len(available_attacks):
                attack_type = list(available_attacks.keys())[int(choice) - 1]
                return attack_type, available_attacks[attack_type]
            print("Invalid choice. Please try again.")

    def handle_stamina_cost(self, attack_type, attack_info):
        """Calculate and apply stamina cost for attack"""
        weapon_type = self.player.equipped.get("weapon", {"weapon_type": "light"}).weapon_type
        base_stamina_cost = self.player.get_weapon_stamina_cost(weapon_type)
        total_stamina_cost = base_stamina_cost + attack_info['stamina_modifier']

        if self.player.stamina < total_stamina_cost:
            print(f"Not enough stamina for {attack_info['name']}!")
            return False

        self.player.use_stamina(total_stamina_cost)
        return True

    def apply_attack_buffs(self, stat_buffs):
        """Apply temporary stat buffs for attack duration"""
        for stat, value in stat_buffs.items():
            if hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) + value)

    def remove_attack_buffs(self, stat_buffs):
        """Remove temporary stat buffs after attack"""
        for stat, value in stat_buffs.items():
            if hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) - value)
                
    def handle_post_attack_effects(self, enemy, attack_hit, total_damage, attack_type, attack_info):
        # Handle damage reflection
        if attack_hit: # Only reflect damage if the attack hits
            reflected_damage = 0
            for effect in enemy.status_effects:
                if effect.name == "Damage Reflect":
                    reflected_damage = effect.apply_func(enemy, effect.strength, total_damage) # Pass total damage to function
                    if isinstance(reflected_damage, tuple):
                        reflected_damage, _ = reflected_damage
                        if reflected_damage > 0:
                            self.player.take_damage(reflected_damage)
                            print(f"{self.player.name} takes {reflected_damage} reflected damage!")

        # Handle attack effects
        if 'effect' in attack_info and attack_hit:
            self.apply_attack_effect(attack_info['effect'], enemy, self.player, total_damage)
        
        # Handle stance changes
        if attack_type == "defensive":
            self.player.apply_defensive_stance(attack_info["duration"], attack_info["defence_boost_percentage"])
        elif attack_type == "power_stance":
            self.player.apply_power_stance(attack_info["duration"], attack_info["attack_boost_percentage"])
        elif attack_type == "berserker_stance":
            self.player.apply_berserker_stance(attack_info["duration"], attack_info["attack_boost_percentage"])
        elif attack_type == "accuracy_stance":
            self.player.apply_accuracy_stance(attack_info["duration"], attack_info["accuracy_boost_percentage"])
        elif attack_type == "evasion_stance":
            self.player.apply_evasion_stance(attack_info["duration"], attack_info["evasion_boost_percentage"])


        # Handle weapon coating
        if attack_hit and self.player.weapon_coating:
            print(f"{enemy.name} is poisoned by your coated weapon!")
            poison_effect = POISON(
                duration=self.player.weapon_coating['duration'],
                strength=self.player.weapon_coating['stacks']
            )
            enemy.apply_status_effect(poison_effect)
            self.player.update_weapon_coating()

    def check_battle_end(self, enemy):
        if not enemy.is_alive():
            self.end_battle("enemy_defeat", enemy)
            return True
        
        if enemy.stunned:
            print(f"{enemy.name} is stunned and loses their turn!")
            enemy.stunned = False
        else:
            self.enemy_attack(enemy)
        
        if not self.player.is_alive():
            self.end_battle("player_defeat")
            return True
        
        return False

    def enemy_attack(self, enemy):
        attack_type = enemy.choose_attack()
        attack_info = ENEMY_ATTACK_TYPES[attack_type]
        
        message, total_damage, self_damage_info, attack_hit = enemy.perform_attack(self.player, attack_type)
        
        if attack_hit:
            # Handle main effect
            if 'effect' in attack_info:
                self.apply_attack_effect(attack_info['effect'], self.player, enemy, total_damage)
                
            # Handle any extra effects
            if 'extra_effects' in attack_info:
                for extra_effect in attack_info['extra_effects']:
                    self.apply_attack_effect(extra_effect, self.player, enemy, total_damage)
            
        reflected_damage = 0
        for effect in self.player.status_effects:
            if effect.name == "Damage Reflect":
                reflected_damage += effect.apply(self.player, total_damage)
        
        if reflected_damage > 0:
            enemy.take_damage(reflected_damage)
            print(f"{enemy.name} takes {reflected_damage} reflected damage!")

        if not self.player.is_alive():
            self.end_battle("player_defeat")
        
        return False, self_damage_info
    
    def apply_attack_effect(self, effect_type, target, attacker, damage):
        #print(f"Applying {effect_type} effect from {attacker.name} to {target.name}")  # Debug output
        effect_strength = max(1, attacker.level // 5)
        if effect_type == "poison":
            effect_strength = max(1, attacker.level // 3)
            poison_effect = POISON(4, effect_strength)
            target.apply_status_effect(poison_effect)
        elif effect_type == "burn":
            burn_effect = BURN(4, effect_strength)
            target.apply_status_effect(burn_effect)
        elif effect_type == "freeze":
            freeze_effect = FREEZE(2, effect_strength)
            target.apply_status_effect(freeze_effect)
        elif effect_type == "stun":
            stun_effect = STUN(2, effect_strength)
            target.apply_status_effect(stun_effect)
        elif effect_type == "confusion":
            confusion_effect = CONFUSION(3, effect_strength)
            target.apply_status_effect(confusion_effect)
        elif effect_type == "stamina_drain":
            stamina_drain_effect = STAMINA_DRAIN(damage)
            target.apply_status_effect(stamina_drain_effect)
        elif effect_type == "damage_reflect":
            damage_reflect_effect = DAMAGE_REFLECT(4, effect_strength)
            attacker.apply_status_effect(damage_reflect_effect)
        elif effect_type == "lifesteal":
            heal_effect = VAMPIRIC(damage)
            attacker.apply_status_effect(heal_effect)
        elif effect_type == "defence_break":
            effect_strength = 0.5
            defence_break_effect = DEFENCE_BREAK(4, effect_strength, damage)
            target.apply_status_effect(defence_break_effect)
        elif effect_type == "attack_weaken":
            attack_weaken_effect = ATTACK_WEAKEN(4, effect_strength, damage)
            target.apply_status_effect(attack_weaken_effect)
        # Add other effects as needed
    
    def chance_to_hit(self, attacker, target):
        print(f"Chance to hit %: {attacker.accuracy - target.evasion}")
    
    def battle(self, enemy):
        #Battle logic, displays player and enemy stats, updates the cooldowns of any items and buffs
        self.enemy = enemy
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while not self.battle_ended:
            self.turn_counter += 1
            self.player.update_cooldowns()
            self.player.update_hots()
            self.player.update_buffs()
            #self.player.update_status_effects(self.player)
            enemy.update_status_effects(enemy)
            self.display_battle_status(enemy)
            
            if not self.player.is_alive():
                self.end_battle("player_defeat")
                return
            
            if not enemy.is_alive():
                self.end_battle("enemy_defeat", enemy)
                return
            
            if self.player.stunned:
                print("You're stunned and lose your turn.")
                self.player.update_status_effects(self.player)
                self.player.remove_status_effect("Stun")
                self.player.stunned = False
                self.enemy_attack(enemy)
                continue
            
            action = input("\nDo you want to:\n[a]ttack\n[u]se item\n[r]un?\n>").lower()
            
            self_damage_info = None
            
            if action == "a":
                #Runs the player_attack method when selected
                battle_over, self_damage_info = self.player_attack(enemy)
                self.player.update_status_effects(self.player)
                if battle_over:
                    return
            elif action == "u":
                #Handles item usage and ensures player gains exp and gold if enemy dies
                used_item = self.use_item_menu(enemy)
                if used_item:
                    if used_item.effect_type == "damage" and not enemy.is_alive():
                        print(f"{enemy.name} has been defeated!")
                        self.player.gain_exp(enemy.exp, enemy.level)
                        self.player.gold += enemy.gold
                        print(f"You gained {enemy.gold} gold.")
                        return
                    else:
                        self.player.update_status_effects(self.player)
                        self.enemy_attack(enemy)
                else:
                    print("No item used. You lose your turn.")
                    self.player.update_status_effects(self.player)
                    self.enemy_attack(enemy)
            elif action == "r":
                #Handles the player trying to run away
                if self.run_away(enemy):
                    self.player.update_status_effects(self.player)
                    return
            else:
                print("Invalid action. You lose your turn.")
                self.player.update_status_effects(self.player)
            
    def end_battle(self, reason, enemy=None):
        self.battle_ended = True
        
        if reason == "player_defeat":
            self.handle_player_defeat()
        elif reason == "enemy_defeat":
            print(f"You defeated the {enemy.name}!")
            self.player.record_kill(enemy.name)
            self.player.gain_exp(enemy.exp, enemy.level)
            self.player.gold += enemy.gold
            print(f"You gained {enemy.gold} gold.")
            self.loot_drop(enemy.tier)
            self.battle_ended = False
        elif reason == "run_away":
            print("You successfully ran away from the battle.")
        
        self.player.cleanup_after_battle()
        self.enemy = None
        
    
    def loot_drop(self, enemy_tier):
        """Enhanced loot drop system with stack handling and enemy variants"""
        # Get variant info from the enemy if it exists
        variant_data = getattr(self.enemy, 'variant', None)
        drops = []
        
        # Handle variant-specific drops first, if applicable
        if variant_data and 'loot_modifiers' in variant_data:
            # Handle guaranteed drops from variants
            guaranteed_drops = variant_data['loot_modifiers'].get('guaranteed_drops', [])
            for guaranteed_type in guaranteed_drops:
                if guaranteed_type in ["common", "uncommon", "rare", "epic", "masterwork", "legendary", "mythical"]:
                    # Get items of the guaranteed tier
                    tier_items = [item for item in self.items.values() if item.tier == guaranteed_type]
                    if tier_items:
                        drops.append(self.create_item_drop(random.choice(tier_items)))
                else:
                    # Get items of the guaranteed type (like "consumable")
                    type_items = [item for item in self.items.values() if item.type == guaranteed_type and self._is_tier_appropriate(item.tier, self.player.level)]
                    if type_items:
                        drops.append(self.create_item_drop(random.choice(type_items)))
                        
            # Get base drops with variant modifiers (this handles quantity bonus)
            base_drops = self.generate_loot(enemy_tier, variant_data['loot_modifiers'])
            drops.extend(base_drops)
        else:
            # Regular random loot check (30% chance)
            if random.random() < 0.3:
                base_drops = self.generate_loot(enemy_tier, None)
                drops.extend(base_drops)
        
        # Display and add drops if any were generated
        if drops:
            self.display_loot(drops)
            self.add_loot_to_player(drops)
                
    def generate_loot(self, enemy_tier, variant_modifiers=None):
        """Generate loot based on enemy tier with enemy variants"""
        drops = []
        base_loot_tiers = self.get_loot_tiers(enemy_tier)
        loot_tiers = base_loot_tiers.copy()
        
        # Get valid items for the loot pool
        loot_pool = [item for item in self.items.values() if item.tier in loot_tiers]
        
        if not loot_pool:
            return drops
        
        # Determine number of items to drop
        num_drops = 1
        
        # Add variant quantity bonus if applicable
        if variant_modifiers and "quantity_bonus" in variant_modifiers:
            num_drops += variant_modifiers["quantity_bonus"]
        
        # 10% chance for additional drop
        while random.random() < 0.1 and num_drops < 3:
            num_drops += 1
            
        for _ in range(num_drops):
            item = random.choice(loot_pool)
            drops.append(self.create_item_drop(item))
        
        # Apply variant quality boost if applicable
        if variant_modifiers and "quality_boost" in variant_modifiers:
            tier_order = ["common", "uncommon", "rare", "epic", "masterwork", "legendary", "mythical"]
            for item in drops:
                if random.random() < variant_modifiers["quality_boost"]:
                    current_tier_idx = tier_order.index(item.tier)
                    if current_tier_idx < len(tier_order) - 1:
                        # Get an item of the next tier
                        next_tier = tier_order[current_tier_idx + 1]
                        next_tier_items = [i for i in self.items.values() if i.tier == next_tier]
                        if next_tier_items:
                            upgraded_item = self.create_item_drop(random.choice(next_tier_items))
                            drops[drops.index(item)] = upgraded_item
        
        return drops
    
    def create_item_drop(self, item):
        """Helper method to create a new item instance with appropriate stack size"""
        if item.is_stackable():
            # Calculate stack size based on tier
            base_stack = {
                "common": (1, 3),
                "uncommon": (1, 2),
                "rare": (1, 2),
                "epic": 1,
                "masterwork": 1,
                "legendary": 1,
                "mythical": 1
            }
            
            # Get stack range for item tier
            stack_range = base_stack.get(item.tier, (1, 1))
            
            # Calculate stack size
            if isinstance(stack_range, tuple):
                stack_size = random.randint(*stack_range)
            else:
                stack_size = stack_range
            
            # Create new item with stack size
            new_item = type(item)(
                item.name, item.type, item.value, item.tier,
                effect_type=item.effect_type, effect=item.effect,
                cooldown=item.cooldown, duration=item.duration,
                tick_effect=item.tick_effect,
                weapon_type=item.weapon_type,
                stamina_restore=item.stamina_restore
            )
            new_item.stack_size = stack_size
            return new_item
        else:
            return item
    
    def _is_tier_appropriate(self, tier, player_level):
        """Check if an item is appropriate for the player level"""
        tier_requirements = {
            "common": 1,
            "uncommon": 3,
            "rare": 6,
            "epic": 10,
            "masterwork": 15,
            "legendary": 20,
            "mythical": 25
        }
        return player_level >= tier_requirements.get(tier, 1)
    
    def display_loot(self, drops):
        """Display dropped loot with stack information"""
        print("\nLoot dropped:")
        
        # Group items by name for cleaner display
        grouped_drops = {}
        for item in drops:
            if item.name in grouped_drops:
                if item.is_stackable():
                    grouped_drops[item.name]['quantity'] += item.stack_size
                else:
                    grouped_drops[item.name]['quantity'] += 1
            else:
                grouped_drops[item.name] = {
                    'item': item,
                    'quantity': item.stack_size if item.is_stackable() else 1
                }
        
        # Display grouped items
        for name, info, in grouped_drops.items():
            item = info['item']
            quantity = info['quantity']
            
            # Format the display string
            quantity_str = f" x{quantity}" if quantity > 1 else ""
            tier_str = f"[{item.tier.capitalize()}]"
            value_str = f"({item.value} gold each)" if quantity > 1 else f"({item.value} gold)"
            
            print(f"- {name}{quantity_str} {tier_str} {value_str}")
            
            # Show additional info for equipment
            if item.type in ["weapon", "shield", "helm", "chest", "boots", "gloves", "back", "legs", "belt", "ring"]:
                stats = []
                if item.attack > 0:
                    stats.append(f"Attack: {item.attack}")
                if hasattr(item, 'armour_penetration') and item.armour_penetration > 0:
                    stats.append(f"AP: {item.armour_penetration}")
                if hasattr(item, 'accuracy') and item.accuracy > 0:
                    stats.append(f"Accuracy: {item.accuracy}")
                if item.defence > 0:
                    stats.append(f"Defence: {item.defence}")
                if hasattr(item, 'block_chance') and item.block_chance > 0:
                    stats.append(f"BC: {item.block_chance}")
                if hasattr(item, 'damage_reduction') and item.damage_reduction > 0:
                    stats.append(f"DR: {item.damage_reduction}")
                if hasattr(item, 'evasion') and item.evasion > 0:
                    stats.append(f"Evasion: {item.evasion}")
                if hasattr(item, 'crit_chance') and item.crit_chance > 0:
                    stats.append(f"Crit: {item.crit_chance}%")
                if hasattr(item, 'crit_damage') and item.crit_damage > 0:
                    stats.append(f"Crit Damage: {item.crit_damage}")
                if stats:
                    print(f"  {', '.join(stats)}")
                    
            # Show effect for consumables
            elif item.type in ["consumable", "food", "drink", "weapon coating"]:
                effect_desc = self.player.get_effect_description(item)
                if effect_desc:
                    print(f"  Effect: {effect_desc}")

    def add_loot_to_player(self, drops):
        """Add dropped items to player inventory with stack handling"""
        for item in drops:
            self.player.add_item(item)
    
    def get_loot_tiers(self, enemy_tier):
        """Determine eligible loot tiers based on enemy tier"""
        basic_tiers = {
            "low": ["common"],
            "medium": ["uncommon"],
            "medium-hard": ["uncommon", "rare"],
            "hard": ["rare", "epic"],
            "very-hard": ["epic", "masterwork"],
            "extreme": ["masterwork", "legendary"],
            "boss": ["legendary", "mythical"]
        }
        
        # Define the maximum possible tier upgrade based on base tier
        max_tier_upgrade = {
            "low": "rare",
            "medium": "epic",
            "medium-hard": "epic",
            "hard": "legendary",
            "very-hard": "legendary",
            "extreme": "mythical",
            "boss": "mythical"
        }
        
        # Get base tiers for the enemy's tier
        tiers = basic_tiers.get(enemy_tier, ["common"])
        max_allowed_tier = max_tier_upgrade.get(enemy_tier, "rare")
        
        # tier_order defines the progression of tiers
        tier_order = ["common", "uncommon", "rare", "epic", "masterwork", "legendary", "mythical"]
        
        # Check for variant in enemy name and apply tier boost if applicable
        enemy_name = self.enemy.name if hasattr(self, 'enemy') else ""
        for variant in MONSTER_VARIANTS:
            if variant in enemy_name:
                variant_data = MONSTER_VARIANTS[variant]["loot_modifiers"]
                if random.random() < variant_data.get("quality_boost", 0):
                    # Get current highest tier
                    current_highest = tiers[-1]
                    current_idx = tier_order.index(current_highest)
                    max_allowed_idx = tier_order.index(max_allowed_tier)
                    
                    # Only upgrade if we haven't reached the maximum allowed tier
                    if current_idx < max_allowed_idx:
                        next_tier = tier_order[current_idx + 1]
                        tiers.append(next_tier)
                    break
                    
        return tiers
    
    def run_away(self, enemy):
        #Gives the player a 50% chance to run away from the enemy, if they fail, the enemy attacks, damage is set based on difference between enemy attack and player defence * 2
        if random.random() < 0.5:
            print("You successfully ran away!")
            return True
        else:
            damage_taken = max(0, (enemy.attack - self.player.defence) * 2)
            self.player.take_damage(damage_taken)
            print(f"You failed to run away and took {damage_taken} damage.")
            return False
    
    def handle_player_defeat(self):
        if self.player.respawn_counter >= 1:
            print("You have been defeated...")
            print("As your conciousness fades away, you feel a divine presence gazing upon you...")
            print("A benevolent deity takes pity on you and grants you another chance at life.")
            self.player.lose_level()
            self.player.lose_gold()
            self.player.respawn()
            self.game.current_location = "Village"
            self.game.initialise_battle()
        else:
            self.player.game_over()

    def display_battle_status(self, enemy):
        #Shows the defined info below whenever player attacks, helps to keep track of info
        self.player.show_stats()
        
        # Calculate and display hit chances
        player_hit_chance = max(5, min(95, self.player.accuracy - enemy.evasion))
        enemy_hit_chance = max(5, min(95, enemy.accuracy - self.player.evasion))
        print(f"\nYour chance to hit: {player_hit_chance}%")
        print(f"{enemy.name}'s chance to hit you: {enemy_hit_chance}%")
            
        if self.player.status_effects:
            print("\nPlayer Status Effects:")
            effect_messages = []
            for effect in self.player.status_effects:
                effect_str = str(effect)
                if effect_str:
                    effect_messages.append(f"- {effect_str}")
            if effect_messages:
                print("\n".join(effect_messages))
        
        if self.player.weapon_coating:
            print(f"\nYour weapon is coated with {self.player.weapon_coating['name']} ({self.player.weapon_coating['remaining_duration']} attacks remaining)")
        
        print(f"\nLevel {enemy.level} {enemy.name} ({enemy.monster_type.title()}), HP: {enemy.hp}")
        print(f"Atk: {enemy.attack}, Acc: {enemy.accuracy}, Crit: {enemy.crit_chance}%, Crit Dmg: {enemy.crit_damage}%, AP: {enemy.armour_penetration}")
        print(f"Def: {enemy.defence}, Eva: {enemy.evasion}, DR: {enemy.damage_reduction}, BC: {enemy.block_chance}%")
        
        if enemy.status_effects:
            print(f"\n{enemy.name} Status Effects:")
            effect_messages = []
            for effect in enemy.status_effects:
                effect_str = str(effect)
                if effect_str:
                    effect_messages.append(f"- {effect_str}")
            if effect_messages:
                print("\n".join(effect_messages))

    def use_item_menu(self, enemy):
        #Handles item usage inside battle, checks if player has the item, if so and not on cooldown, uses item by calling use_combat_item method
        usable_items = self.player.show_usable_items()
        if not usable_items:
            return None

        while True:
            choice = input("\nEnter the number or name of the item you want to use (or 'c' to cancel): ").strip().lower()
            
            if choice == 'c':
                return None
            
            selected_item = None
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(usable_items):
                    selected_item = usable_items[index]
            else:
                matching_items = [item for item in usable_items if item.name.lower().startswith(choice)]
                if len(matching_items) == 1:
                    selected_item = matching_items[0]
                elif len(matching_items) > 1:
                    print("Multiple matching items found. Please be more specific:")
                    for item in matching_items:
                        print(f"- {item.name}")
                else:
                    print("No matching item found.")
            
            if selected_item:
                if selected_item.name in self.player.cooldowns and self.player.cooldowns[selected_item.name] > 0:
                    print(f"You can't use {selected_item.name} yet. Cooldown: {self.player.cooldowns[selected_item.name]} turns.")
                elif selected_item.effect_type in ["healing", "damage", "buff", "hot"]:
                    return self.use_combat_item(selected_item, enemy)
                else:
                    print(f"You can't use {selected_item.name} in combat.")
            else:
                print("Invalid choice. Please try again.")
                
    def use_combat_item(self, item, enemy):
        #Handles the use of items in combat, ensures items are correctly applied
        if item.effect_type == "healing":
            success, message = self.player.use_item(item)
            print(message)
        elif item.effect_type == "damage":
            damage = item.effect
            enemy.take_damage(damage)
            self.player.inventory.remove(item)
            print(f"You used {item.name} and dealt {damage} damage to {enemy.name}.")
        elif item.effect_type == "buff":
            success, message = self.player.use_item(item)
            print(message)
        elif item.effect_type == "hot":
            success, message = self.player.use_item(item)
            print(message)
        return item