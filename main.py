import random
import os
import platform

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

class Item:
    def __init__(self, name, item_type, value, tier, attack=0, defence=0, effect_type=None, effect=0, cooldown=0):
        self.name = name
        self.type = item_type
        self.value = value
        self.tier = tier
        self.attack = attack
        self.defence = defence
        self.effect_type = effect_type
        self.effect = effect
        self.cooldown = cooldown

class Character:
    def __init__(self, name, hp, attack, defence):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=10, defence=5)
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.inventory = []
        self.equipped = {
            "weapon": None,
            "helm": None,
            "chest": None,
            "legs": None,
            "boots": None,
            "gloves": None,
            "shield": None
        }

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defence += 3
        print(f"Congratulations! You reached level {self.level}!")
        print("Your stats have increased.")

    def equip_item(self, item):
        if item.type in self.equipped:
            if self.equipped[item.type]:
                self.unequip_item(item.type)
            self.equipped[item.type] = item
            if item.type == "weapon":
                self.attack += item.attack
            else:
                self.defence += item.defence
            if item in self.inventory:
                self.inventory.remove(item)
            print(f"You equipped {item.name}.")
        else:
            print("You can't equip that item.")

    def unequip_item(self, slot):
        item = self.equipped[slot]
        if item:
            if slot == "weapon":
                self.attack -= item.attack
            else:
                self.defence -= item.defence
            self.inventory.append(item)
            self.equipped[slot] = None
            print(f"You unequipped {item.name}.")

    def use_item(self, item):
        if item.type == "consumable":
            self.heal(item.effect)
            self.inventory.remove(item)
            print(f"You used {item.name} and restored {item.effect} HP.")
        else:
            print("You can't use that item.")

    def show_inventory(self):
        print("\nInventory:")
        for item in self.inventory:
            print(f"- {item.name} (Value: {item.value} gold)")
        print("\nEquipped:")
        for slot, item in self.equipped.items():
            print(f"{slot.capitalize()}: {item.name if item else 'None'}")
            
    def show_consumables(self):
        consumables = [item for item in self.inventory if item.type == "consumable"]
        if consumables:
            print("\nConsumable Items:")
            for item in consumables:
                effect_description = self.get_effect_description(item)
                print(f"- {item.name}: {effect_description}")
        else:
            print("\nYou have no consumable items.")

    def get_effect_description(self, item):
        if item.effect_type == "healing":
            return f"Restores {item.effect} HP"
        elif item.effect_type == "damage":
            return f"Deals {item.effect} damage"
        elif item.effect_type == "buff":
            return f"Increases attack by {item.effect}"
        else:
            return "Unknown effect"

class Enemy(Character):
    def __init__(self, name, hp, attack, defence, exp, gold, tier):
        super().__init__(name, hp, attack, defence)
        self.exp = exp
        self.gold = gold
        self.tier = tier

class Shop:
    def __init__(self, all_items):
        self.inventory = {}
        self.all_items = all_items
        self.restock_counter = 0
        self.restock_frequency = 10  # Restock every 10 game actions

    def add_item(self, item, quantity):
        if item.name in self.inventory:
            self.inventory[item.name]['quantity'] += quantity
        else:
            self.inventory[item.name] = {'item': item, 'quantity': quantity}

    def remove_item(self, item_name, quantity):
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] -= quantity
            if self.inventory[item_name]['quantity'] <= 0:
                del self.inventory[item_name]

    def display_inventory(self):
        print("\nShop Inventory:")
        # Sort the inventory items by value
        sorted_inventory = sorted(
            self.inventory.items(),
            key=lambda x: x[1]['item'].value,
            reverse=False  # For descending order (highest value first)
        )
        for item_name, info in sorted_inventory:
            print(f"- {item_name}: {info['quantity']} available (Price: {info['item'].value} gold)")

    def rotate_stock(self):
        self.restock_counter += 1
        if self.restock_counter >= self.restock_frequency:
            print("\nThe shop has restocked with new items!")
            self.restock_counter = 0
            self.inventory.clear()
            self.stock_shop()

    def stock_shop(self):
        num_items = random.randint(5, 10)  # Stock 5-10 random items
        available_items = list(self.all_items.values())
        for _ in range(num_items):
            item = random.choice(available_items)
            quantity = random.randint(1, 5)
            self.add_item(item, quantity)

class Game:
    def __init__(self):
        self.player = None
        self.current_location = "Village"
        self.initialise_items()
        self.initialise_enemies()
        self.initialise_map()
        self.shop = Shop(self.items)
        self.shop.stock_shop()

    def initialise_items(self):
        self.items = {
            #Starter items
            "Peasants Top": Item("Peasants Top", "chest", 0, "starter", defence=1),
            "Peasants Bottoms": Item("Peasants Bottoms", "legs", 0, "starter", defence=1),
            "Wooden Sword": Item("Wooden Sword", "weapon", 0, "starter", attack=2),
            #Low tier weapons
            "Rusty Sword": Item("Rusty Sword", "weapon", 20, "low", attack=5),
            #Low tier armour
            "Wooden Shield": Item("Wooden Shield", "shield", 15, "low", defence=3),
            "Leather Helm": Item("Leather Helm", "helm", 10, "low", defence=2),
            #Low tier consumables
            "Health Potion": Item("Health Potion", "consumable", 15, "low", effect_type= "healing", effect=20, cooldown=3),
            #Medium tier items
            "Steel Sword": Item("Steel Sword", "weapon", 100, "medium", attack=15),
            "Kite Shield": Item("Kite Shield", "shield", 80, "medium", defence=8),
            #High tier
            "Enchanted Blade": Item("Enchanted Blade", "weapon", 300, "high", attack=25),
            "Dragon Shield": Item("Dragon Shield", "shield", 250, "high", defence=15),
            "Elixir of Life": Item("Elixir of Life", "consumable", 120, "high", effect_type="healing", effect=100, cooldown=3),
        }

    def initialise_enemies(self):
        self.enemies = {
            #Easy Enemies
            "Rat": Enemy("Rat", 20, 5, 1, 10, random.randrange(3, 10), "low"),
            "Goblin": Enemy("Goblin", 30, 8, 3, 15, 10, "low"),
            #Medium Enemies
            "Wolf": Enemy("Wolf", 60, 15, 8, 30, 25, "medium"),
            "Orc": Enemy("Orc", 80, 18, 12, 40, 35, "medium"),
            #Hard Enemies
            "Dragon": Enemy("Dragon", 200, 30, 25, 100, 200, "high"),
        }

    def initialise_map(self):
        self.game_map = {
            "Village": {"enemies": [], "connected_to": ["Forest", "Plains"]},
            "Forest": {"enemies": ["Rat", "Goblin", "Wolf"], "connected_to": ["Village", "Mountain"]},
            "Plains": {"enemies": ["Goblin", "Wolf"], "connected_to": ["Village", "Desert"]},
            "Mountain": {"enemies": ["Wolf", "Orc"], "connected_to": ["Forest", "Dragon's Lair"]},
            "Desert": {"enemies": ["Orc"], "connected_to": ["Plains", "Ancient Ruins"]},
            "Dragon's Lair": {"enemies": ["Dragon"], "connected_to": ["Mountain"]},
            "Ancient Ruins": {"enemies": ["Orc", "Dragon"], "connected_to": ["Desert"]}
        }

    def create_character(self):
        name = input("Enter your character's name: ")
        self.player = Player(name)
        # Give the player a Peasants Outfit to start with
        starting_items = [self.items["Wooden Sword"], self.items["Peasants Top"], self.items["Peasants Bottoms"]]
        self.player.inventory.append(self.items["Health Potion"])
        for item in starting_items:
            self.player.equip_item(item)
        print(f"Welcome, {self.player.name}! Your adventure begins in the Village.")
        print("You start with a Peasants Outfit equipped.")

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
        for location in self.game_map[self.current_location]["connected_to"]:
            print(f"- {location}")
        destination = input("Where do you want to go? ").strip().title()
        if destination in self.game_map[self.current_location]["connected_to"]:
            self.current_location = destination
            print(f"You have arrived at {self.current_location}.")
            self.location_actions()
        else:
            print("You can't go there from here.")

    def location_actions(self):
        while True:
            action = input("\nWhat would you like to do? [e]xplore, [r]est, [l]eave: ")
            if action.lower() == 'e':
                self.encounter()
            elif action.lower() == 'r':
                self.rest()
            elif action.lower() == 'l':
                break
            else:
                print("Invalid action. Try again.")

    def encounter(self):
        if self.game_map[self.current_location]["enemies"] and random.random() < 0.7:
            enemy_type = random.choice(self.game_map[self.current_location]["enemies"])
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

    def battle(self, enemy):
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
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

    def loot_drop(self, enemy_tier):
        if random.random() < 0.3:  # 30% chance of loot drop
            if enemy_tier == "low":
                loot_pool = [item for item in self.items.values() if item.tier == "low"]
            elif enemy_tier == "medium":
                loot_pool = [item for item in self.items.values() if item.tier == "medium"]
            else:  # high tier
                loot_pool = [item for item in self.items.values() if item.tier == "high"]
            
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

    def game_loop(self):
        self.create_character()
        
        while True:
            self.show_status()
            action = input("\nWhat do you want to do? [m]ove, [i]nventory, [c]onsumbales, [e]quip, [u]se item, [s]hop (Village only), [q]uit: ")
            
            if action.lower() == "m":
                self.move()
            elif action.lower() == "i":
                clear_screen()
                self.player.show_inventory()
                pause()
            elif action.lower() == "c":
                clear_screen()
                self.player.show_consumables()
                pause()
            elif action.lower() == "e":
                clear_screen()
                self.equip_menu()
            elif action.lower() == "u":
                clear_screen()
                self.use_item_menu()
            elif action.lower() == "s":
                if self.current_location == "Village":
                    self.shop_menu()
                else:
                    print("You can only access the shop in the Village.")
            elif action.lower() == "q":
                print("Thanks for playing!")
                break
            else:
                print("Invalid action. Try again.")
                
            self.shop.rotate_stock()  # Check if it's time to rotate stock after each action

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

    def use_item_menu(self):
        self.player.show_consumables()
        item_name = input("Enter the name of the item you want to use (or 'cancel'): ")
        if item_name.lower() == "cancel":
            return
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower() and item.type == "consumable":
                self.use_item(item)
                return
        print("You don't have that consumable item.")
        pause()

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

if __name__ == "__main__":
    game = Game()
    game.game_loop()