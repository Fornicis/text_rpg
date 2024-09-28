import random
from player import Player
from enemies import Enemy

class Battle:
    def __init__(self, player, items, game):
        self.player = player
        self.items = items
        self.game = game

    def calculate_damage(self, base_attack, attacker_name):
        #Calculates player and enemy damage within a range of 80% to 120% of base attack
        damage = random.randint(int(base_attack * 0.8), int(base_attack * 1.2))
        is_critical = random.random() < 0.1  # Critical hit chance 10%
        if is_critical:
            damage = int(damage * 1.5)
            print(f"Critical hit by {attacker_name}!")
        return damage, is_critical

    def player_attack(self, enemy):
        #Handles the player attacking, if enemy dies, player gains exp and gold with a chance for loot, else the enemy attacks back
        equipped_weapon = self.player.equipped.get("weapon")
        weapon_type = equipped_weapon.weapon_type if equipped_weapon else "light"
        stamina_cost = self.player.get_weapon_stamina_cost(weapon_type)
        if not self.player.can_attack():
            print("Not enough stamina to attack!")
            return False

        self.player.use_stamina(stamina_cost)
        player_damage, player_crit = self.calculate_damage(self.player.attack, self.player.name)
        player_damage = max(0, player_damage - enemy.defence)
        enemy.take_damage(player_damage)
        print(f"You dealt {player_damage} damage to {enemy.name}.")
        
        if not enemy.is_alive():
            print(f"You defeated the {enemy.name}!")
            self.player.gain_exp(enemy.exp, enemy.level)
            self.player.gold += enemy.gold
            print(f"You gained {enemy.gold} gold.")
            self.loot_drop(enemy.tier)
            self.player.remove_combat_buffs()
            return True
        
        enemy_damage, enemy_crit = self.calculate_damage(enemy.attack, enemy.name)
        enemy_damage = max(0, enemy_damage - self.player.defence)
        self.player.take_damage(enemy_damage)
        print(f"{enemy.name} dealt {enemy_damage} damage to you.")
        
        if not self.player.is_alive():
            self.handle_player_defeat()
            return True
        
        return False

    def run_away(self, enemy):
        #Gives the player a 50% chance to run away from the enemy, if they fail, the enemy attacks, damage is set based on difference between enemy attack and player defence * 2
        if random.random() < 0.5:
            print("You successfully ran away!")
            return True
        else:
            damage_taken = max(0, (enemy.attack * 2) - self.player.defence)
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
        #Battle logic, displays player and enemy stats, updates the cooldowns of any items
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
            self.display_battle_status(enemy)
            self.player.update_cooldowns()
            self.player.update_hots()
            self.player.update_buffs()
            
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