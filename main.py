import random
import os
import platform
from player import Player
from enemies import Enemy, initialise_enemies
from items import Item, initialise_items
from shop import Shop
from world_map import WorldMap

def clear_screen():
    operating_system = platform.system()
    #Windows
    if operating_system != 'Win64' and operating_system != 'Windows':
        os.system('clear')
    #Mac and Linux
    else:
        os.system('cls')

def pause():
    input("\nPress Enter to continue...")

def display_message(message):
    clear_screen()
    print(message)
    pause()

class Game:
    def __init__(self):
        self.player = None
        self.current_location = "Village"
        self.world_map = WorldMap()
        self.items = initialise_items()
        self.enemies = initialise_enemies()
        self.shop = Shop(self.items)
        self.shop.stock_shop()

    def create_character(self):
        name = input("Enter your character's name: ")
        self.player = Player(name)
        # Give the player a Peasants Outfit to start with
        starting_items = [self.items["Wooden Sword"], self.items["Peasants Top"], self.items["Peasants Bottoms"]]
        self.player.inventory.append(self.items["Basic Health Potion"])
        for item in starting_items:
            self.player.equip_item(item)
        print(f"Welcome, {self.player.name}! Your adventure begins in the Village.")
        print("You start with a Peasants Outfit equipped and a Basic Health Potion in your inventory.")

    def show_status(self):
        clear_screen()
        print(f"\n{self.player.name} (Level {self.player.level}):")
        print(f"HP: {self.player.hp}/{self.player.max_hp}")
        print(f"EXP: {self.player.exp}")
        print(f"Gold: {self.player.gold}")
        print(f"Attack: {self.player.attack}")
        print(f"Defence: {self.player.defence}")
        print(f"Current location: {self.current_location}")
        print("\nEquipped Items:")
        for slot, item in self.player.equipped.items():
            if item:
                print(f"{slot.capitalize()}: {item.name}")

    def move(self):
        clear_screen()
        print("\nConnected locations:")
        connected_locations = self.world_map.get_connected_locations(self.current_location)
        for location in connected_locations:
            print(f"- {location}")
        destination = input("Where do you want to go? ").strip().title()
        if destination in connected_locations:
            self.current_location = destination
            print(f"You have arrived at {self.current_location}.")
            self.location_actions()
        else:
            print("You can't go there from here.")

    def location_actions(self):
        while True:
            action = input("\nWhat would you like to do? [e]xplore, [u]se item, [m]ove, [l]eave: ")
            if action.lower() == 'e':
                self.encounter()
            elif action.lower() == 'u':
                self.use_item_menu()
            elif action.lower() == 'm':
                self.move()
            elif action.lower() == 'l':
                break
            else:
                print("Invalid action. Try again.")

    def encounter(self):
        possible_enemies = self.world_map.get_enemies(self.current_location)
        if possible_enemies and random.random() < 0.7:
            enemy_type = random.choice(possible_enemies)
            enemy_template = self.enemies[enemy_type]
            # Create a new instance of the enemy
            enemy = Enemy(
                enemy_template.name,
                enemy_template.hp,
                enemy_template.attack,
                enemy_template.defence,
                enemy_template.exp,
                enemy_template.gold,
                enemy_template.tier
            )
            print(f"You encountered a {enemy.name}!")
            self.battle(enemy)
        else:
            print("You explored the area but found nothing of interest.")

    def rest(self):
        heal_amount = self.player.max_hp // 4  # Heal 25% of max HP
        self.player.heal(heal_amount)
        print(f"You rest and recover {heal_amount} HP.")

    def calculate_damage(self, base_attack):
        min_damage = max(1, base_attack - 5)
        max_damage = base_attack + 5
        damage = random.randint(min_damage, max_damage)
        #Critical hit chance 10%
        if random.random() < 0.1:
            damage *= 2
            print("You dealt a critical hit!")
            if damage == 0:
                print("Too bad 0 * 2 is still 0!")
        return damage
    
    def battle(self, enemy):
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
            self.player.update_cooldowns()
            print(f"\n{self.player.name} HP: {self.player.hp}")
            print(f"{enemy.name} HP: {enemy.hp}")
            action = input("Do you want to [a]ttack, [u]se item, or [r]un? ")
            
            if action.lower() == "a":
                player_base_damage = self.calculate_damage(self.player.attack)
                enemy_base_damage = self.calculate_damage(enemy.attack)
                
                player_damage = max(0, player_base_damage - enemy.defence)
                enemy_damage = max(0, enemy_base_damage - self.player.defence)
                
                enemy.take_damage(player_damage)
                print(f"You dealt {player_damage} damage to {enemy.name}.")
                
                if not enemy.is_alive():
                    print(f"You defeated the {enemy.name}!")
                    self.player.gain_exp(enemy.exp)
                    self.player.gold += enemy.gold
                    print(f"You gained {enemy.exp} EXP and {enemy.gold} gold.")
                    self.loot_drop(enemy.tier)
                    break
                
                self.player.take_damage(enemy_damage)
                print(f"{enemy.name} dealt {enemy_damage} damage to you.")
                
                if not self.player.is_alive():
                    print("You have been defeated. Game over.")
                    return
            
            elif action.lower() == "u":
                self.player.show_consumables()
                item_name = input("Enter the name of the item you want to use (or 'cancel'): ")
                if item_name.lower() == 'cancel':
                    continue
                
                item = next((item for item in self.player.inventory if item.name.lower() == item_name.lower()), None)
                if item:
                    target = self.player if item.effect_type in ["healing", "buff"] else enemy
                    self.use_battle_item(item, target)
                else:
                    print("You don't have that item.")
                pause()
            
            elif action.lower() == "r":
                if random.random() < 0.5:
                    print("You successfully ran away!")
                    return
                else:
                    print("You failed to run away.")
                    self.player.take_damage(max(0, enemy.attack - self.player.defence))
                    print(f"{enemy.name} dealt {max(0, enemy.attack - self.player.defence)} damage to you.")
            
            else:
                print("Invalid action. You lose your turn.")
    
    def use_battle_item(self, item, target):
        if item.type == "consumable":
            if item.effect_type == "healing":
                heal_amount = item.effect
                target.heal(heal_amount)
                print(f"{target.name} used {item.name} and restored {heal_amount} HP.")
            elif item.effect_type == "damage":
                damage = item.effect
                target.take_damage(damage)
                print(f"{target.name} used {item.name} and dealt {damage} damage.")
            elif item.effect_type == "buff":
                buff_amount = item.effect
                target.attack += buff_amount
                print(f"{target.name} used {item.name} and increased attack by {buff_amount}.")
            self.player.inventory.remove(item)
        else:
            print(f"{item.name} cannot be used in battle.")

    

    def loot_drop(self, enemy_tier):
        if random.random() < 0.3:  # 30% chance of loot drop
            if enemy_tier == "low":
                loot_pool = [item for item in self.items.values() if item.tier == "common"]
            elif enemy_tier in ["medium", "medium-hard"]:
                loot_pool = [item for item in self.items.values() if item.tier == "medium"]
            elif enemy_tier in ["medium-hard", "hard"]:  # high tier
                loot_pool = [item for item in self.items.values() if item.tier == "rare"]
            elif enemy_tier == "very-hard":
                loot_pool = [item for item in self.items.values() if item.tier == "epic"]
            elif enemy_tier == "extreme":
                loot_pool = [item for item in self.items.values() if item.tier == "legendary"]
            else:
                loot_pool = [item for item in self.items.values() if item.tier == "mythical"]
                
            
            item = random.choice(loot_pool)
            self.player.inventory.append(item)
            print(f"You found a {item.name}!")
            
    def shop_menu(self):
        while True:
            clear_screen()
            self.shop.rotate_stock()  # Check if it's time to rotate stock
            print("\n--- Shop Menu ---")
            print("1. Buy items")
            print("2. Sell items")
            print("3. Exit shop")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.buy_item()
            elif choice == '2':
                self.sell_item()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def buy_item(self):
        self.shop.display_inventory()
        item_name = input("Enter the name of the item you want to buy (or 'cancel'): ")
        if item_name.lower() == 'cancel':
            return

        # Create a case-insensitive dictionary of inventory items
        inventory_lower = {name.lower(): info for name, info in self.shop.inventory.items()}

        if item_name.lower() in inventory_lower:
            item_info = inventory_lower[item_name.lower()]
            if self.player.gold >= item_info['item'].value:
                self.player.gold -= item_info['item'].value
                self.player.inventory.append(item_info['item'])
                self.shop.remove_item(item_info['item'].name, 1)
                print(f"You bought {item_info['item'].name} for {item_info['item'].value} gold.")
            else:
                print("You don't have enough gold to buy this item.")
        else:
            print("This item is not available in the shop.")


    def sell_item(self):
        self.player.show_inventory()
        item_name = input("Enter the name of the item you want to sell (or 'cancel'): ")
        if item_name.lower() == 'cancel':
            return

        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                sell_price = item.value // 2  # Sell for half the buy price
                self.player.gold += sell_price
                self.player.inventory.remove(item)
                self.shop.add_item(item, 1)
                print(f"You sold {item.name} for {sell_price} gold.")
                return
        print("You don't have that item.")

    def equip_menu(self):
        self.player.show_inventory()
        item_name = input("Enter the name of the item you want to equip (or 'cancel'): ")
        if item_name.lower() == "cancel":
            return
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                self.player.equip_item(item)
                return
        print("You don't have that item.")

    def use_item(self, item):
            if item.effect_type == "healing":
                heal_amount = min(item.effect, self.player.max_hp - self.player.hp)
                self.player.heal(heal_amount)
                print(f"You used {item.name} and restored {heal_amount} HP.")
            elif item.effect_type == "buff":
                self.player.attack += item.effect
                print(f"You used {item.name} and increased your attack by {item.effect}.")
            else:
                print(f"You can't use {item.name} outside of battle.")
                return
            self.player.inventory.remove(item)

    def use_item_menu(self):
        self.player.show_inventory()
        item_name = input("Enter the name of the item you want to use (or 'cancel'): ")
        if item_name.lower() == "cancel":
            return
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                if self.player.use_item(item):
                    print(f"You used {item.name}.")
                return
        print("You don't have that item.")
        pause()

    def game_loop(self):
        self.create_character()
        
        while True:
            self.player.update_cooldowns()
            self.show_status()
            action = input("\nWhat do you want to do? [m]ove, [i]nventory, [c]onsumbales, [e]quip, [l]ocation actions, [u]se item, [s]hop (Village only), [r]est (Restore 25% health, easy mode), [q]uit: ")
            
            if action.lower() == "m":
                self.move()
            elif action.lower() == "i":
                clear_screen()
                self.player.show_inventory()
                pause()
            elif action.lower() == "c":
                clear_screen()
                self.player.show_consumables()
                self.player.show_cooldowns()
                pause()
            elif action.lower() == "e":
                clear_screen()
                self.equip_menu()
            elif action.lower() == "l":
                clear_screen()
                self.location_actions()
            elif action.lower() == "u":
                clear_screen()
                self.use_item_menu()
            elif action.lower() == "s":
                if self.current_location == "Village":
                    self.shop_menu()
                else:
                    print("You can only access the shop in the Village.")
            elif action.lower() == "r":
                self.rest()
            elif action.lower() == "q":
                print("Thanks for playing!")
                break
            else:
                print("Invalid action. Try again.")
                
            self.shop.rotate_stock()  # Check if it's time to rotate stock after each action

if __name__ == "__main__":
    game = Game()
    game.game_loop()