import random
from player import Player
from enemies import Enemy

class Battle:
    def __init__(self, player, items):
        self.player = player
        self.items = items

    def calculate_damage(self, base_attack):
        #Calculates player and enemy damage within a range of 50% less to 50% more
        damage = random.randint(max(1, base_attack // 2), base_attack * 1.5)
        if random.random() < 0.1:  # Critical hit chance 10%
            damage *= 2
            print("Critical hit!")
        return damage

    def player_attack(self, enemy):
        #Handles the player attacking, if enemy dies, player gains exp and gold with a chance for loot, else the enemy attacks back
        player_damage = max(0, self.calculate_damage(self.player.attack) - enemy.defence)
        enemy.take_damage(player_damage)
        print(f"You dealt {player_damage} damage to {enemy.name}.")
        
        if not enemy.is_alive():
            print(f"You defeated the {enemy.name}!")
            self.player.gain_exp(enemy.exp, enemy.level)
            self.player.gold += enemy.gold
            print(f"You gained {enemy.gold} gold.")
            return True
        
        enemy_damage = max(0, self.calculate_damage(enemy.attack) - self.player.defence)
        self.player.take_damage(enemy_damage)
        print(f"{enemy.name} dealt {enemy_damage} damage to you.")
        
        if not self.player.is_alive():
            print("You have been defeated. Game over.")
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

    def battle(self, enemy):
        #Battle logic, displays player and enemy stats, updates the cooldowns of any items
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
            self.player.update_cooldowns()
            print(f"\n{self.player.name} HP: {self.player.hp}\nAttack: {self.player.attack}\nDefence: {self.player.defence}\n\n{enemy.name} HP: {enemy.hp}\nAttack: {enemy.attack}\nDefence: {enemy.defence}\n")
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
                        self.player.gain_exp(enemy.exp)
                        self.player.gold += enemy.gold
                        print(f"You gained {enemy.exp} EXP and {enemy.gold} gold.")
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
                print("You have been defeated. Game over.")
                return
            
        if self.player.is_alive() and not enemy.is_alive():
            #Removes all buffs from the player at the end of a battle
            self.player.remove_all_buffs()

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
                elif selected_item.effect_type in ["healing", "damage", "buff"]:
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
        return item