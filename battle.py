import random
import pygame
from display import Display, BattleDisplay
from player import Player
from enemies import Enemy, ENEMY_ATTACK_TYPES, MONSTER_VARIANTS
from status_effects import *


class Battle:
    def __init__(self, player, items, game):
        self.player = player
        self.items = items
        self.game = game
        self.current_location = game.current_location
        self.turn_counter = 0
        self.battle_ended = False
        self.enemy = None
        self.display = Display()
        self.battle_display = BattleDisplay(game.display)
        self.player.battle_display = self.battle_display
        self._battle_display = self.battle_display
        
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
        self.battle_display.draw_battle_message(message)
        
        if attack_hit:
            reflected_damage = self.handle_damage_reflection(self.player, enemy, total_damage)
            if reflected_damage > 0:
                self.battle_display.draw_battle_message(f"\n{self.player.name} takes {reflected_damage} reflected damage!")
            # Provide visual feedback for hit
            self.battle_display.draw_battle_screen(self.player, self.current_location, enemy)
            pygame.display.flip()
        
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
            self.battle_display.draw_battle_message("\nYou're stunned and lose your turn.")
            self.player.stunned = False
            self.player.remove_status_effect("Stun")
            if self.player.status_effects:
                self.player.update_status_effects(self.player)
            return True

        # Handle confusion
        confusion_effect = next((effect for effect in self.player.status_effects if effect.name == "Confusion"), None)
        if confusion_effect:
            if random.random() < 0.5:
                self.battle_display.draw_battle_message("\nYou're confused and attack yourself!")
                damage, hit_type, _, _ = self.player.calculate_damage(self.player, self.player, "normal")
                self.player.take_damage(damage)
                self.battle_display.draw_battle_message(f"\nYou dealt {damage} damage to yourself!")
                self.battle_display.draw_battle_message("\nYour attack on yourself snaps you out of your confusion!")
                pygame.time.wait(1500)
                #self.display.pause()
                self.player.remove_status_effect("Confusion")
                return True
            else:
                self.battle_display.draw_battle_message(f"\n{self.player.name} snaps out of their confusion!")
                pygame.time.wait(1500)
                self.player.remove_status_effect("Confusion")

        # Handle freeze
        frozen_effect = next((effect for effect in self.player.status_effects if effect.name == "Freeze"), None)
        if frozen_effect:
            if random.random() < 0.5:
                self.battle_display.draw_battle_message("\nYou're frozen and cannot attack!")
                self.enemy_attack(enemy)
                self.player.update_status_effects(self.player)
                #self.display.pause()
                return True
            else:
                self.battle_display.draw_battle_message(f"\n{self.player.name} thaws out from the ice and attacks!")
                pygame.display.flip()
                pygame.time.wait(1000)
                self.player.remove_status_effect("Freeze")

        return False

    def get_player_attack_choice(self):
        """Visual attack selection menu"""
        available_attacks = self.player.get_available_attack_types()
        
        self.battle_display.draw_battle_screen(self.player, self.current_location, self.enemy)
        self.player.display_attack_options()
        self.battle_display.draw_enemy_panel(self.enemy, *self.battle_display.layout['enemy_panel'])
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        choice = event.key - pygame.K_1 + 1
                        if 1 <= choice <= len(available_attacks):
                            attack_type = list(available_attacks.keys())[choice - 1]
                            return attack_type, available_attacks[attack_type]
                    elif event.key == pygame.K_ESCAPE:
                        return None, None
            pygame.time.wait(10)

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
            self.player.update_buffs()
            self.player.update_hots()
            self.player.update_cooldowns()

        # Handle attack effects
        if 'effect' in attack_info and attack_hit:
            self.apply_attack_effect(attack_info['effect'], enemy, self.player, total_damage)
        
        # Handle stance changes
        if attack_type.endswith("_stance"):
            if attack_type == "defensive_stance":
                stance = DEFENSIVE_STANCE(attack_info["duration"], attack_info["defence_boost_percentage"])
            elif attack_type == "power_stance":
                stance = POWER_STANCE(attack_info["duration"], attack_info["attack_boost_percentage"])
            elif attack_type == "berserker_stance":
                stance = BERSERKER_STANCE(attack_info["duration"], attack_info["attack_boost_percentage"])
            elif attack_type == "accuracy_stance":
                stance = ACCURACY_STANCE(attack_info["duration"], attack_info["accuracy_boost_percentage"])
            elif attack_type == "evasion_stance":
                stance = EVASION_STANCE(attack_info["duration"], attack_info["evasion_boost_percentage"])
            
            stance.set_battle_display(self.battle_display)
            self.player.apply_status_effect(stance)

    def check_battle_end(self, enemy):
        self.battle_display.wait_for_animation()
        
        if not enemy.is_alive() and not self.player.is_alive():
            self.end_battle("enemy_defeat", enemy)
            print(f"\nWith your final mighty strike, you fell the {enemy.name}, but the blow reduces your health to 0!\n")
            self.display.pause()
            self.end_battle("player_defeat")
            return True
        
        if not enemy.is_alive():
            self.end_battle("enemy_defeat", enemy)
            return True
        
        enemy.update_status_effects(enemy)
        
        if not enemy.is_alive():
            self.end_battle("enemy_defeat", enemy)
            return True
        
        if enemy.stunned:
            print(f"\n{enemy.name} is stunned and loses their turn!")
            enemy.stunned = False
        else:
            self.enemy_attack(enemy)
            
        self.player.update_status_effects(self.player)
        
        if not self.player.is_alive():
            self.end_battle("player_defeat")
            return True
        
        return False

    def enemy_attack(self, enemy):
        attack_type = enemy.choose_attack()
        attack_info = ENEMY_ATTACK_TYPES[attack_type]
        
        message, total_damage, self_damage_info, attack_hit = enemy.perform_attack(self.player, attack_type)
        self.battle_display.draw_battle_message(message)
        
        if attack_hit:
            # Provide visual feedback for hit
            self.battle_display.draw_battle_screen(self.player, self.current_location, enemy)
            pygame.display.flip()
            
            # Handle main effect
            if 'effect' in attack_info:
                self.apply_attack_effect(attack_info['effect'], self.player, enemy, total_damage)
                
            # Handle any extra effects
            if 'extra_effects' in attack_info:
                for extra_effect in attack_info['extra_effects']:
                    self.apply_attack_effect(extra_effect, self.player, enemy, total_damage)
            
        """reflected_damage = self.handle_damage_reflection(enemy, self.player, total_damage)
        if reflected_damage > 0:
            self.battle_display.draw_battle_message(f"{enemy.name} takes {reflected_damage} reflected damage!")"""

        if not self.player.is_alive():
            self.end_battle("player_defeat")
        
        return False, self_damage_info
    
    def handle_damage_reflection(self, attacker, defender, damage):
        reflected_damage = 0
        for effect in defender.status_effects:
            if effect.name == "Damage Reflect":
                reflected_damage += effect.apply_func(attacker, effect.strength, damage)[0]
        if reflected_damage > 0:
            attacker.take_damage(reflected_damage)
        return reflected_damage
    
    def apply_attack_effect(self, effect_type, target, attacker, damage):
        #print(f"Applying {effect_type} effect from {attacker.name} to {target.name}")  # Debug output
        effect_strength = max(1, attacker.level // 5)
        effect = None
        if effect_type == "poison":
            effect_strength = max(1, attacker.level // 3)
            effect = POISON(4, effect_strength)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == "burn":
            effect = BURN(4, effect_strength)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == "freeze":
            effect = FREEZE(2, 0)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == "stun":
            effect = STUN(2, 0)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == "confusion":
            effect = CONFUSION(3, 0)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == "stamina_drain":
            effect = STAMINA_DRAIN(damage)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == "damage_reflect":
            effect = DAMAGE_REFLECT(4, 0)
            if effect:
                effect.set_battle_display(self.battle_display)
                attacker.apply_status_effect(effect)
        elif effect_type == "lifesteal":
            effect = VAMPIRIC(damage)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == "defence_break":
            effect_strength = 1
            effect = DEFENCE_BREAK(3, effect_strength, damage)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == "attack_weaken":
            effect_strength = 1
            effect = ATTACK_WEAKEN(3, effect_strength, damage)
            if effect:
                effect.set_battle_display(self.battle_display)
                target.apply_status_effect(effect)
        elif effect_type == 'self_damage':
            effect = SelfDamage(damage)
            if effect:
                effect.set_battle_display(self.battle_display)
                attacker.apply_status_effect(effect)
        """if effect:
            effect.set_battle_display(self.battle_display)
            target.apply_status_effect(effect)"""
        # Add other effects as needed
    
    def chance_to_hit(self, attacker, target):
        print(f"Chance to hit %: {attacker.accuracy - target.evasion}")
    
    def battle(self, enemy):
        #Battle logic, displays player and enemy stats, updates the cooldowns of any items and buffs
        self.enemy = enemy
        enemy.battle_display = self._battle_display
        enemy._prev_hp = enemy.hp
        self.player._prev_hp = self.player.hp
        scroll_offset = 0
        self.battle_display.draw_battle_message(f"Battle start! {self.player.name} vs {enemy.name}")
        
        while not self.battle_ended:
            self.battle_display.draw_battle_screen(self.player, self.current_location, enemy, scroll_offset=scroll_offset)
            self.turn_counter += 1
            
            if not self.player.is_alive():
                self.end_battle("player_defeat")
                return
            
            if not enemy.is_alive():
                self.end_battle("enemy_defeat", enemy)
                return
            
            if self.player.stunned:
                self.battle_display.draw_battle_message("\nYou're stunned and lose your turn!")
                self.player.update_status_effects(self.player)
                self.player.remove_status_effect("Stun")
                self.player.stunned = False
                self.enemy_attack(enemy)
                continue
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.KEYDOWN:
                    # Get reference to display's text buffer
                    text_buffer = self.battle_display.display.text_buffer
                    max_display_lines = 10
                    max_scroll = max(0, len(text_buffer) - max_display_lines)
                    
                    if event.key == pygame.K_DOWN and scroll_offset > 0:
                        scroll_offset = max(0, scroll_offset - 1)
                    elif event.key == pygame.K_UP and scroll_offset < max_scroll:
                        scroll_offset += 1
                    
                    # Battle action handling
                    if event.key == pygame.K_a:
                        battle_over, self_damage_info = self.player_attack(enemy)
                        if battle_over:
                            return
                    elif event.key == pygame.K_u:
                        used_item = self.use_item_menu(enemy)
                        if used_item:
                            if used_item.effect_type == "damage" and not enemy.is_alive():
                                self.end_battle("enemy_defeat", enemy)
                                return
                            else:
                                self.player.update_status_effects(self.player)
                                self.enemy_attack(enemy)
                        else:
                            self.player.update_status_effects(self.player)
                            self.enemy_attack(enemy)
                    elif event.key == pygame.K_r:
                        if self.run_away(enemy):
                            self.battle_display.display.text_buffer.clear()
                            return
                self.display.draw_battle_log_panel(
                    *self.display.calculate_layout()['battle_log_panel'],
                    scroll_offset = scroll_offset
                )
        self.battle_display.display.text_buffer.clear()
                
        pygame.display.flip()
        self.display.clock.tick(self.display.config.FPS)
            
    def end_battle(self, reason, enemy=None):
        self.battle_ended = True
        self.battle_display.display.text_buffer.clear()
        self.player.cleanup_after_battle()
        if reason == "player_defeat":
            self.handle_player_defeat()
            #self.display.pause()
        elif reason == "enemy_defeat":
            #self.display.pause()
            self.battle_display.draw_battle_message(f"You defeated the {enemy.name}!")
            self.display.pause()
            self.player.record_kill(enemy.name)
            self.player.gain_exp(enemy.exp, enemy.level)
            self.player.gold += enemy.gold
            self.battle_display.draw_battle_message(f"You gained {enemy.gold} gold!")
            self.loot_drop(enemy.tier)
            self.display.pause()
            self.battle_ended = False
        elif reason == "run_away":
            return
        
        #self.battle_display.display.text_buffer.clear()
        
        self.enemy = None
        pygame.display.flip()
        
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
        self.battle_display.draw_battle_message("\nLoot dropped:")
        
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
            slot_str = f"({item.type.capitalize()})"
            
            self.battle_display.draw_battle_message(f"- {name}{quantity_str} {slot_str} {tier_str} {value_str}")
            
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
                    self.battle_display.draw_battle_message(f"  {', '.join(stats)}")
                    
            # Show effect for consumables
            elif item.type in ["consumable", "food", "drink", "weapon coating"]:
                effect_desc = self.player.get_effect_description(item)
                if effect_desc:
                    self.battle_display.draw_battle_message(f"  Effect: {effect_desc}")

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
            self.battle_display.display.text_buffer.clear()
            self.player.debuff_modifiers.clear()
            self.battle_display.draw_battle_message("You successfully ran away from the battle! Brave Sir Robin!")
            self.display.pause()
            return True
        else:
            damage_taken = max(0, (enemy.attack - self.player.defence) * 2)
            self.player.take_damage(damage_taken)
            self.battle_display.draw_battle_message(f"You failed to run away and took {damage_taken} damage.")
            return False
    
    def handle_player_defeat(self):
        if self.player.respawn_counter >= 1:
            #print("DEBUG: Starting defeat sequence")
            self.battle_display.draw_battle_message("You have been defeated...")
            self.battle_display.draw_battle_message("As your consciousness fades away, you feel a divine presence gazing upon you...")
            self.battle_display.draw_battle_message("A benevolent deity takes pity on you and grants you another chance at life.")
            #print("DEBUG: Before first pause")
            self.display.pause()
            #print("DEBUG: Before lose_level")
            self.player.lose_level()
            self.display.pause()
            #print("DEBUG: Before lose_gold")
            self.player.lose_gold()
            #print("DEBUG: Before respawn")
            self.player.respawn()
            self.display.pause()
            #print("DEBUG: Before location change")
            self.game.current_location = "Village"
            #print("DEBUG: Before initialise_battle")
            self.game.initialise_battle()
            #print("DEBUG: End sequence")
            self.display.draw_game_screen(self.player, self.game.current_location)
        else:
            self.player.game_over()

    def use_item_menu(self, enemy):
        """Handle visual item menu in battle"""
        used_item = self.game.use_item_menu(in_combat=True, enemy=enemy)
        
        if used_item and used_item.effect_type in ["healing", "damage", "buff", "hot"]:
            self.battle_display.draw_battle_screen(self.player, self.current_location, enemy)
            return used_item
        
        return None
                
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