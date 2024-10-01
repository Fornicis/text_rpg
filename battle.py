import random
from player import Player
from enemies import Enemy, ENEMY_ATTACK_TYPES
import time
class Battle:
    def __init__(self, player, items, game):
        self.player = player
        self.items = items
        self.game = game
        self.attack_types = {
            "normal": {"name": "Normal Attack", "stamina_modifier": 0, "damage_modifier": 1},
            "power": {"name": "Power Attack", "stamina_modifier": 3, "damage_modifier": 1.5},
            "quick": {"name": "Quick Attack", "stamina_modifier": 1, "damage_modifier": 0.8, "extra_attacks": 1},
            "defensive": {"name": "Defensive Stance", "stamina_modifier": 2, "damage_modifier": 0, "defence_boost_percentage": 25, "duration": 5}
        }
        self.defensive_stance = {"boost": 0, "duration": 0}
        self.player_stunned = False

    def calculate_damage(self, base_attack, attacker, attack_type = "normal"):
        #Calculates player and enemy damage within a range of 80% to 120% of base attack
        #attack_info = self.attack_types[attack_type]
        if isinstance(attacker, Enemy):
            attack_info = ENEMY_ATTACK_TYPES[attack_type]
        else:
            attack_info = self.attack_types[attack_type]
            
        modified_attack = base_attack * attack_info["damage_modifier"]
        damage = random.randint(int(modified_attack * 0.8), int(modified_attack * 1.2))
        is_critical = random.random() < 0.1  # Critical hit chance 10%
        if is_critical:
            damage = int(damage * 1.5)
            print(f"Critical hit by {attacker.name if isinstance(attacker, Enemy) else attacker}!")
        return damage, is_critical

    def player_attack(self, enemy):
        #Handles the player attacking, if enemy dies, player gains exp and gold with a chance for loot, else the enemy attacks back
        if self.player_stunned:
            print("You're stunned and lose your turn.")
            self.player_stunned = False
            return False
        
        print("\nChoose your attack type:")
        for key, value in self.attack_types.items():
            weapon_type = self.player.equipped.get("weapon", {"weapon_type": "light"}).weapon_type
            base_stamina_cost = self.player.get_weapon_stamina_cost(weapon_type)
            total_stamina_cost = base_stamina_cost + value['stamina_modifier']
            print(f"[{key[0]}] {value['name']} (Stamina cost: {total_stamina_cost})")
        
        while True:
            choice = input("\nEnter your choice: \n").lower()
            if choice in [k[0] for k in self.attack_types.keys()]:
                attack_type = [k for k in self.attack_types.keys() if k.startswith(choice)][0]
                break
            else:
                print("Invalid choice. Please try again.")

        attack_info = self.attack_types[attack_type]
        weapon_type = self.player.equipped.get("weapon", {"weapon_type": "light"}).weapon_type
        base_stamina_cost = self.player.get_weapon_stamina_cost(weapon_type)
        total_stamina_cost = base_stamina_cost + attack_info['stamina_modifier']

        if self.player.stamina < total_stamina_cost:
            print(f"Not enough stamina for {attack_info['name']}!")
            return False

        self.player.use_stamina(total_stamina_cost)
        
        total_damage = 0
        attacks = 1 + attack_info.get("extra_attacks", 0)
        
        for _ in range(attacks):
            player_damage, player_crit = self.calculate_damage(self.player.attack, self.player.name, attack_type)
            player_damage = max(0, player_damage - enemy.defence)
            enemy.take_damage(player_damage)
            total_damage += player_damage
        
        print(f"You used {attack_info['name']} and dealt a total of {total_damage} damage to {enemy.name}.")
        
        if attack_type == "defensive":
            defence_boost = int(self.player.defence * attack_info["defence_boost_percentage"] / 100)
            self.defensive_stance = {
                "boost": defence_boost,
                "duration": attack_info["duration"]
            }
            self.player.defence += self.defensive_stance["boost"]
            print(f"Your defence increased by {self.defensive_stance['boost']} ({attack_info['defence_boost_percentage']}%) for the next {self.defensive_stance['duration']} turns.")
        
        if not enemy.is_alive():
            print(f"You defeated the {enemy.name}!")
            self.player.record_kill(enemy.name)
            self.player.gain_exp(enemy.exp, enemy.level)
            self.player.gold += enemy.gold
            print(f"You gained {enemy.gold} gold.")
            self.loot_drop(enemy.tier)
            self.player.remove_combat_buffs()
            return True
        
        # Enemy attack remains the same
        """enemy_damage, enemy_crit = self.calculate_damage(enemy.attack, enemy.name)
        enemy_damage = max(0, enemy_damage - self.player.defence)
        self.player.take_damage(enemy_damage)
        print(f"{enemy.name} dealt {enemy_damage} damage to you.")"""
        
        self.enemy_attack(enemy)
        
        if not self.player.is_alive():
            self.handle_player_defeat()
            return True
        
        return False
    
    def enemy_attack(self, enemy):
        attack_type = enemy.choose_attack()
        enemy_damage, enemy_crit = self.calculate_damage(enemy.attack, enemy, attack_type)
        enemy_damage = max(0, enemy_damage - self.player.defence)
        
        attack_name = ENEMY_ATTACK_TYPES[attack_type]["name"]
        
        self.display_attack_animation(enemy.name, attack_name)
        self.player.take_damage(enemy_damage)
        
        print(f"{enemy.name} used {attack_name} and dealt {enemy_damage} damage to you.")
        
        effect = ENEMY_ATTACK_TYPES[attack_type].get("effect")
        if effect:
            self.apply_enemy_effect(effect, enemy, enemy_damage)

        if attack_type == "quick":
            print(f"{enemy.name} attacks again with Quick Attack!")
            second_damage, _= self.calculate_damage(enemy.attack, enemy, "quick")
            second_damage = max(0, second_damage - self.player.defence)
            self.player.take_damage(second_damage)
            print(f"{enemy.name} dealt an additional {second_damage} damage to you.")
    
    def display_attack_animation(self, attacker_name, attack_name):
        #Shows the enemy attacking in a dramatic way!
        print(f"\n{attacker_name} is preparing to attack...")
        time.sleep(1)  # Pause for dramatic effect
        print(f">>> {attack_name.upper()} <<<")
        time.sleep(0.5)
    
    def apply_enemy_effect(self, effect, enemy, damage):
        if effect == "lifesteal":
            heal_amount = int(damage * 0.5)
            enemy.heal(heal_amount)
            print(f"{enemy.name} healed for {heal_amount} HP!")
        elif effect == "self_damage":
            self_damage = int(damage * 0.2)
            enemy.take_damage(self_damage)
            print(f"{enemy.name} took {self_damage} self-damage from its reckless attack!")
        elif effect == "stamina_drain":
            stamina_loss = min(20, self.player.stamina)
            self.player.use_stamina(stamina_loss)
            print(f"You lost {stamina_loss} stamina from the draining attack!")
        elif effect == "stun":
            if random.random() < 0.3:  # 30% chance to stun
                self.player_stunned = True
                print("You've been stunned and will lose your next turn!")
    
    def update_defensive_stance(self):
        #Update the defensive stance effect.
        if self.defensive_stance["duration"] > 0:
            self.defensive_stance["duration"] -= 1
            if self.defensive_stance["duration"] == 0:
                self.player.defence -= self.defensive_stance["boost"]
                print(f"Your defence boost from Defensive Stance has worn off.")
                self.defensive_stance = {"boost": 0, "duration": 0}
            else:
                print(f"\nDefensive Stance remains active for {self.defensive_stance['duration']} more turns.\n")

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

    def display_battle_status(self, enemy):
        #Shows the defined info below whenever player attacks, helps to keep track of info
        print(f"\n{self.player.name} HP: {self.player.hp}")
        print(f"Attack: {self.player.attack}")
        print(f"Defence: {self.player.defence}")
        print(f"Stamina: {self.player.stamina}/{self.player.max_stamina}")
        print(f"Level: {self.player.level}")
        print(f"Exp: {self.player.exp}/{self.player.level * 100}")
        
        if self.defensive_stance["duration"] > 0:
            print(f"Defensive Stance: +{self.defensive_stance['boost']} defence for {self.defensive_stance['duration']} more turns.")
        
        if self.player_stunned:
            print("You are stunned and will lose your next turn.")
        
        if self.player.active_hots:
            print("\nActive HoT Effects:")
            for hot_name, hot_info in self.player.active_hots.items():
                print(f"- {hot_name}: {hot_info['tick_effect']} HP/turn for {hot_info['duration']} more turns")
                
        if self.player.active_buffs:
            print("\nActive Buffs:")
            for buff_name, buff_info in self.player.active_buffs.items():
                if isinstance(buff_info, dict):
                    print(f"- {buff_name.capitalize()}: +{buff_info['value']} for {buff_info['duration']} more turns")
                else:
                    print(f"- {buff_name.capitalize()}: +{buff_info}")
        
        print(f"\n{enemy.name} HP: {enemy.hp}")
        print(f"Attack: {enemy.attack}")
        print(f"Defence: {enemy.defence}")
        print(f"Level: {enemy.level}")

    def battle(self, enemy):
        #Battle logic, displays player and enemy stats, updates the cooldowns of any items and buffs
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
            self.display_battle_status(enemy)
            self.player.update_cooldowns()
            self.player.update_hots()
            self.player.update_buffs()
            self.update_defensive_stance()
            
            action = input("Do you want to:\n[a]ttack\n[u]se item\n[r]un?\n>").lower()
            
            if action == "a":
                #Runs the player_attack method when selected
                battle_over = self.player_attack(enemy)
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
                    print("No item used. You lose your turn.")
            elif action == "r":
                #Handles the player trying to run away
                if self.run_away(enemy):
                    return
            else:
                print("Invalid action. You lose your turn.")
                
            if not self.player.is_alive():
                self.handle_player_defeat()
                return True
    
    def handle_player_defeat(self):
        if self.player.respawn_counter >= 1:
            print("You have been defeated...")
            print("As your conciousness fades away, you feel a divine presence gazing upon you...")
            print("A benevolent deity takes pity on you and grants you another chance at life.")
            self.player.lose_level()
            self.player.lose_gold()
            self.player.respawn()
            self.game.current_location = "Village"
        else:
            self.player.game_over()
    
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