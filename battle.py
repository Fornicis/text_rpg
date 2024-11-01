import random
from player import Player
from enemies import Enemy, ENEMY_ATTACK_TYPES
from status_effects import *


class Battle:
    def __init__(self, player, items, game):
        self.player = player
        self.items = items
        self.game = game
        self.turn_counter = 0
        self.battle_ended = False
        
    def player_attack(self, enemy):
        # First check for status effects that prevent attacking
        if self.handle_pre_attack_effects(enemy):
            return False, None

        # Get and validate attack choice
        attack_type, available_attacks = self.get_player_attack_choice()
        if not attack_type:
            return False, None

        # Handle stamina cost
        if not self.handle_stamina_cost(attack_type, available_attacks):
            return False, None

        # Perform the attack and get results
        message, total_damage, self_damage_info, attack_hit = self.player.perform_attack(enemy, attack_type)

        # Handle post-attack effects
        self.handle_post_attack_effects(enemy, attack_hit, total_damage, attack_type)

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
                damage, hit_type, _ = self.player.calculate_damage(self.player, self.player, "normal")
                self.player.take_damage(damage)
                print(f"You dealt {damage} damage to yourself!")
                print("Your attack on yourself snaps you out of your confusion!")
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
                return True
            else:
                print(f"{self.player.name} thaws out from the ice and attacks!")
                self.player.remove_status_effect("Freeze")

        return False

    def get_player_attack_choice(self):
        self.player.display_attack_options()
        available_attacks = self.player.get_available_attack_types()
        
        while True:
            choice = input(f"\nEnter your choice (1-{len(available_attacks)}): ")
            if choice.isdigit() and 1 <= int(choice) <= len(available_attacks):
                attack_type = list(available_attacks.keys())[int(choice) - 1]
                return attack_type, available_attacks
            else:
                print("Invalid choice. Please try again.")

    def handle_stamina_cost(self, attack_type, available_attacks):
        attack_info = available_attacks[attack_type]
        weapon_type = self.player.equipped.get("weapon", {"weapon_type": "light"}).weapon_type
        base_stamina_cost = self.player.get_weapon_stamina_cost(weapon_type)
        total_stamina_cost = base_stamina_cost + attack_info['stamina_modifier']

        if self.player.stamina < total_stamina_cost:
            print(f"Not enough stamina for {attack_info['name']}!")
            return False

        self.player.use_stamina(total_stamina_cost)
        return True

    def handle_post_attack_effects(self, enemy, attack_hit, total_damage, attack_type):
        # Handle damage reflection
        reflected_damage = 0
        for effect in enemy.status_effects:
            if effect.name == "Damage Reflect":
                reflected_damage += effect.apply(enemy, total_damage)
        
        if reflected_damage > 0:
            self.player.take_damage(reflected_damage)
            print(f"{self.player.name} takes {reflected_damage} reflected damage!\n")

        # Handle stance effects
        if attack_type == "defensive":
            stance_message = self.player.apply_defensive_stance()
            if stance_message:
                print(stance_message)
        elif attack_type == "power_stance":
            stance_message = self.player.apply_power_stance()
            if stance_message:
                print(stance_message)
        elif attack_type == "berserker_stance":
            stance_message = self.player.apply_berserker_stance()
            if stance_message:
                print(stance_message)
        elif attack_type == "accuracy_stance":
            stance_message = self.player.apply_accuracy_stance()
            if stance_message:
                print(stance_message)
        elif attack_type == "evasion_stance":
            stance_message = self.player.apply_evasion_stance()
            if stance_message:
                print(stance_message)

        # Handle weapon coating
        if attack_hit and self.player.weapon_coating:
            print(f"{enemy.name} is poisoned by your coated weapon!\n")
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
        effect_type = attack_info.get("effect")
        message, total_damage, self_damage_info, attack_hit = enemy.perform_attack(self.player, attack_type)
        
        reflected_damage = 0
        for effect in self.player.status_effects:
            if effect.name == "Damage Reflect":
                reflected_damage += effect.apply(self.player, total_damage)
        
        if reflected_damage > 0:
            enemy.take_damage(reflected_damage)
            print(f"{enemy.name} takes {reflected_damage} reflected damage!")
        
        if attack_hit == True and effect_type:
            self.apply_attack_effect(effect_type, self.player, enemy, total_damage)

        if not self.player.is_alive():
            self.end_battle("player_defeat")
        
        return False, self_damage_info
    
    def apply_attack_effect(self, effect_type, target, attacker, damage):
        #print(f"Applying {effect_type} effect from {attacker.name} to {target.name}")  # Debug output
        effect_strength = max(1, attacker.level // 5)
        if effect_type == "poison":
            effect_strength = max(1, attacker.level // 2)
            poison_effect = POISON(3, effect_strength)
            target.apply_status_effect(poison_effect)
        elif effect_type == "burn":
            burn_effect = BURN(3, effect_strength)
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
            damage_reflect_effect = DAMAGE_REFLECT(3, effect_strength)
            attacker.apply_status_effect(damage_reflect_effect)
        elif effect_type == "lifesteal":
            heal_effect = VAMPIRIC(damage)
            attacker.apply_status_effect(heal_effect)
        elif effect_type == "defence_break":
            defence_break_effect = DEFENCE_BREAK(3, effect_strength)
            target.apply_status_effect(defence_break_effect)
        elif effect_type == "attack_weaken":
            attack_weaken_effect = ATTACK_WEAKEN(3, effect_strength)
            target.apply_status_effect(attack_weaken_effect)
        # Add other effects as needed
    
    def chance_to_hit(self, attacker, target):
        print(f"Chance to hit %: {attacker.accuracy - target.evasion}")
    
    def battle(self, enemy):
        #Battle logic, displays player and enemy stats, updates the cooldowns of any items and buffs
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
        
    
    def loot_drop(self, enemy_tier):
        #Handles loot drops after defeating an enemy.
        if random.random() < 0.3:  # 30% chance of loot drop
            loot_pool = [item for item in self.items.values() if item.tier in self.get_loot_tiers(enemy_tier)]
            item = random.choice(loot_pool)
            self.player.inventory.append(item)
            print(f"You found a {item.name}!")

    def get_loot_tiers(self, enemy_tier):
        #Returns the appropriate loot tiers based on the enemy tier.
        tiers = {
            "low": ["common"],
            "medium": ["uncommon"],
            "medium-hard": ["uncommon", "rare"],
            "hard": ["rare, epic"],
            "very-hard": ["epic, masterwork"],
            "extreme": ["masterwork, legendary"],
        }
        return tiers.get(enemy_tier, ["mythical"])
    
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
        
        print(f"\n{enemy.name} HP: {enemy.hp}")
        print(f"Atk: {enemy.attack}")
        print(f"Def: {enemy.defence}")
        print(f"Lvl: {enemy.level}")
        
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