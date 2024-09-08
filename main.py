import os
import platform
import random
from player import Player
from enemies import initialise_enemies, Enemy
from items import initialise_items
from shop import Shop
from world_map import WorldMap
from save_system import save_game, load_game, get_save_files

def clear_screen():
    #Clears the console screen based on the operating system.
    os.system('cls' if platform.system() in ['Win64', 'Windows'] else 'clear')

def pause():
    #Pauses the game until the user presses Enter.
    input("\nPress Enter to continue...")
    
def display_title():
    clear_screen()
    print("""
    ╔═══════════════════════════════════════════╗
    ║             TEXT RPG ADVENTURE            ║
    ║                                           ║
    ║              © Fornicis, 2024             ║
    ╚═══════════════════════════════════════════╝
    """)

def display_help():
    clear_screen()
    print("""
    === HELP ===
    
    Welcome to Text RPG Adventure!
    
    BASIC GAMEPLAY:
    - You start in the Village, which serves as your home base.
    - Explore different areas, battle monsters, and collect loot to level up.
    - Your goal is to become strong enough to face the ultimate challenges.

    NAVIGATION:
    - Use the [m]ove command to travel between connected areas.
    - Some areas have level requirements to enter.
    - Use numbers, name, or first few characters of area to move to it.
    - Use the [v]iew map command to see the world layout.

    COMBAT:
    - Battles are turn-based. You can:
      [a]ttack: Deal damage to the enemy
      [u]se item: Use a consumable from your inventory
      [r]un: Attempt to flee (not always successful)
    - Defeating enemies grants EXP and sometimes loot.

    INVENTORY AND EQUIPMENT:
    - Access your [i]nventory to see your items.
    - Use the [e]quip command to manage your gear.
    - [c]onsumables can be viewed separately for quick access.

    SHOP:
    - Visit the shop in the Village to buy and sell items.
    - To sell items just enter the number associated with the item.
    - Multiple items can be bought/sold at once, simple enter the numbers seperated by a space.
    - The shop's inventory changes periodically.

    SAVING AND LOADING:
    - Use the [sa]ve game command to save your progress.
    - You can load your game from the main menu.

    OTHER COMMANDS:
    - [r]est: Restore some HP (only in the Village)
    - [u]se item: Use a consumable item
    - [l]ocation actions: Perform actions specific to your current location

    TIPS:
    - Pay attention to your HP, EXP, and gold.
    - Upgrade your equipment regularly.
    - Save your game often to avoid losing progress.
    - Explore new areas as you level up, but be cautious of tough enemies.

    Remember, most actions can be performed by typing the letter in brackets, 
    e.g., 'm' for move, 'i' for inventory, etc.

    Good luck on your adventure!
    """)
    input("Press Enter to return to the main menu...")
    
def title_screen():
    while True:
        display_title()
        print("\n    1. Play")
        print("    2. Load Game")
        print("    3. Help")
        print("    4. Quit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            return "new_game"
        elif choice == '2':
            return "load_game"
        elif choice == '3':
            display_help()
        elif choice == '4':
            print("Thanks for playing! Goodbye.")
            exit()
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

class Game:
    def __init__(self):
        #Initializes the game with default settings and items.
        self.player = None
        self.current_location = "Village"
        self.world_map = WorldMap()
        self.items = initialise_items()
        self.enemies = initialise_enemies()
        self.shop = Shop(self.items)
        self.shop.stock_shop()

    def create_character(self):
        #Creates a new player character.
        name = input("Enter your character's name: ")
        self.player = Player(name)
        print(f"Welcome, {self.player.name}! Your adventure begins in the Village.")

    def show_status(self):
        #Displays the player's current status.
        clear_screen()
        print(f"\n{self.player.name} (Level {self.player.level}):")
        print(f"HP: {self.player.hp}/{self.player.max_hp}, EXP: {self.player.exp}, Gold: {self.player.gold}, "
            f"Attack: {self.player.attack}, Defence: {self.player.defence}, Current location: {self.current_location}")
        print("\nEquipped Items:")
        for slot, item in self.player.equipped.items():
            if item:
                print(f"{slot.capitalize()}: {item.name} (Tier: {item.tier.capitalize()})")
                if item.attack > 0:
                    print(f"  Attack: +{item.attack}")
                if item.defence > 0:
                    print(f"  Defence: +{item.defence}")
                if item.effect_type:
                    print(f"  Effect: {item.effect_type.capitalize()} - ", end="")
                    if isinstance(item.effect, tuple):
                        print(f"{item.effect[0].capitalize()} +{item.effect[1]}")
                    else:
                        print(f"{item.effect}")
                    if item.cooldown > 0:
                        print(f"  Cooldown: {item.cooldown} turns")
            else:
                print(f"{slot.capitalize()}: None")
                
    def move(self):
        #Handles player movement
        clear_screen()
        print("\nConnected locations:")
        connected_locations = self.world_map.get_connected_locations(self.current_location)
        available_locations = []
        
        for i, location in enumerate(connected_locations, 1):
            min_level = self.world_map.get_min_level(location)
            if self.player.level >= min_level:
                print(f"{i}. {location} (Required Level: {min_level})")
                available_locations.append(location)
            else:
                print(f"X. {location} (Required Level: {min_level}) [LOCKED]")
        
        while True:
            choice = input("\nWhere do you want to go? (Enter number, name, or first few letters): ").strip()
            
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(available_locations):
                    destination = available_locations[index]
                    break
            else:
                matching_locations = [loc for loc in available_locations if loc.lower().startswith(choice.lower())]
                if len(matching_locations) == 1:
                    destination = matching_locations[0]
                    break
                elif len(matching_locations) > 1:
                    print("Multiple matching locations found. Please be more specific:")
                    for loc in matching_locations:
                        print(f"- {loc}")
                else:
                    print("No matching location found.")
            
            print("Invalid choice. Please try again.")
        
        min_level = self.world_map.get_min_level(destination)
        if self.player.level >= min_level:
            self.current_location = destination
            print(f"You have arrived at {self.current_location}.")
            if self.current_location == "Village":
                print("Welcome to the Village! You can rest, shop, or prepare for your next adventure here.")
                return False  # Indicate that we should not run location actions
            else:
                return True  # Indicate that we should run location actions
        else:
            print(f"You need to be at least level {min_level} to enter {destination}.")
            return False
        
    def location_actions(self):
        #Handles actions available at the current location.
        while True:
            action = input("\nWhat would you like to do?\n[e]xplore\n[u]se item\n[l]eave\n>").lower()
            if action == 'e':
                clear_screen()
                self.encounter()
            elif action == 'u':
                clear_screen()
                self.use_item_menu()
            elif action == 'l':
                break
            else:
                print("Invalid action. Try again.")

    def encounter(self):
        #Handles enemy encounters during exploration.
        possible_enemies = self.world_map.get_enemies(self.current_location)
        if possible_enemies and random.random() < 0.7:
            enemy_type = random.choice(possible_enemies)
            enemy_template = self.enemies[enemy_type]
            
            # Create an enemy instance with only the required attributes
            enemy = Enemy(
                name=enemy_template.name,
                hp=enemy_template.hp,
                attack=enemy_template.attack,
                defence=enemy_template.defence,
                exp=enemy_template.exp,
                gold=enemy_template.gold,
                tier=enemy_template.tier
            )
            
            print(f"You encountered a {enemy.name}!")
            self.battle(enemy)
        else:
            print("You explored the area but found nothing of interest.")

    def rest(self):
        clear_screen()
        #Restores a portion of the player's health, only in the Village.
        if self.current_location != "Village":
            print("You can only rest in the Village.")
            return

        heal_amount = self.player.max_hp // 4  # Heal 25% of max HP
        self.player.heal(heal_amount)
        print(f"You rest and recover {heal_amount} HP.")

    def calculate_damage(self, base_attack):
        #Calculates damage dealt based on the player's attack.
        damage = random.randint(max(1, base_attack - 5), base_attack + 5)
        if random.random() < 0.1:  # Critical hit chance 10%
            damage *= 2
            print("You dealt a critical hit!")
        return damage
    
    def battle(self, enemy):
        #Battle logic
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
            self.player.update_cooldowns()
            print(f"\n{self.player.name} HP: {self.player.hp}\nAttack: {self.player.attack}\nDefence: {self.player.defence}\n\n{enemy.name} HP: {enemy.hp}\nAttack: {enemy.attack}\nDefence: {enemy.defence}\n")
            action = input("Do you want to:\n[a]ttack\n[u]se item\n[r]un?\n>").lower()
            
            if action == "a":
                self.player_attack(enemy)
            elif action == "u":
                clear_screen()
                used_item = self.use_item_menu(in_combat=True, enemy=enemy)
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
                if self.run_away(enemy):
                    return
            else:
                print("Invalid action. You lose your turn.")
            
            if not self.player.is_alive():
                print("You have been defeated. Game over.")
                
            if self.player.is_alive() and not enemy.is_alive():
                self.player.remove_all_buffs()

    def player_attack(self, enemy):
        #Handles the player's attack on the enemy.
        player_damage = max(0, self.calculate_damage(self.player.attack) - enemy.defence)
        enemy.take_damage(player_damage)
        print(f"You dealt {player_damage} damage to {enemy.name}.")
        
        if not enemy.is_alive():
            print(f"You defeated the {enemy.name}!")
            self.player.gain_exp(enemy.exp)
            self.player.gold += enemy.gold
            print(f"You gained {enemy.exp} EXP and {enemy.gold} gold.")
            self.loot_drop(enemy.tier)
            return
        
        enemy_damage = max(0, self.calculate_damage(enemy.attack) - self.player.defence)
        self.player.take_damage(enemy_damage)
        print(f"{enemy.name} dealt {enemy_damage} damage to you.")
        
        if not self.player.is_alive():
            print("You have been defeated. Game over.")

    def run_away(self, enemy):
        #Handles the player's attempt to run away from battle.
        if random.random() < 0.5:
            print("You successfully ran away!")
            pause()
            clear_screen()
            return True
        else:
            damage_taken = max(0, enemy.attack - self.player.defence)
            self.player.take_damage(damage_taken)
            print(f"You failed to run away and took {damage_taken} damage.")
            return False

    def use_combat_item(self, item, enemy):
        #Uses items in combat, prints different messages based on item used
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
            "hard": ["rare"],
            "very-hard": ["epic"],
            "extreme": ["legendary"],
        }
        return tiers.get(enemy_tier, ["mythical"])

    def shop_menu(self):
        #Displays the shop menu for buying and selling items.
        while True:
            clear_screen()
            self.shop.rotate_stock(self.player.level)  # Check if it's time to rotate stock
            print("\n--- Shop Menu ---")
            print("1. Buy items")
            print("2. Sell items")
            print("3. Exit shop")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.buy_items()
            elif choice == '2':
                self.sell_items()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def buy_items(self):
        #Handles the buying of items from the shop.
        while True:
            clear_screen()
            self.shop.display_inventory(self.player.level)
            print(f"\nYour gold: {self.player.gold}")
            print("\nEnter the numbers of the items you want to buy, separated by spaces.")
            print("For example, to buy items 1, 3, and 5, type: 1 3 5")
            print("Type 'q' when you're finished buying items.")

            choice = input("\nYour choice: ").lower()
            
            if choice == 'q':
                break
            
            try:
                item_indices = [int(i) - 1 for i in choice.split()]
                sorted_inventory = sorted(self.shop.inventory.items(), key=lambda x: x[1]['item'].value, reverse=False)
                items_to_buy = [sorted_inventory[i][1]['item'] for i in item_indices if 0 <= i < len(sorted_inventory)]
                
                if not items_to_buy:
                    print("No valid items selected.")
                    continue
                
                total_cost = sum(item.value for item in items_to_buy)
                
                print("\nYou're about to buy:")
                for item in items_to_buy:
                    print(f"- {item.name} for {item.value} gold")
                print(f"\nTotal cost: {total_cost} gold")
                
                if self.player.gold < total_cost:
                    print("You don't have enough gold to buy these items.")
                    input("\nPress Enter to continue...")
                    continue
                
                confirm = input("Do you want to proceed? (y/n): ").lower()
                if confirm == 'y':
                    for item in items_to_buy:
                        self.player.gold -= item.value
                        self.player.inventory.append(item)
                        self.shop.remove_item(item.name, 1)
                    print(f"You bought {len(items_to_buy)} items for a total of {total_cost} gold.")
                else:
                    print("Purchase cancelled.")
            
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid item numbers separated by spaces.")
            
            input("\nPress Enter to continue...")


    def sell_items(self):
        #Handles selling of multiple items at once to shop
        while True:
            self.player.show_inventory()
            print("\nEnter the numbers of the items you want to sell, separated by spaces.")
            print("For example, to sell items 1, 3, and 5, type: 1 3 5")
            print("Type 'q' when you're finished selling items.")

            choice = input("\nYour choice: ").lower()
            
            if choice == 'q':
                break
            
            try:
                item_indices = [int(i) - 1 for i in choice.split()]
                items_to_sell = [self.player.inventory[i] for i in item_indices if 0 <= i < len(self.player.inventory)]
                
                if not items_to_sell:
                    print("No valid items selected.")
                    continue
                
                total_value = sum(item.value // 2 for item in items_to_sell)
                
                print("\nYou're about to sell:")
                for item in items_to_sell:
                    print(f"- {item.name} for {item.value // 2} gold")
                print(f"\nTotal value: {total_value} gold")
                
                confirm = input("Do you want to proceed? (y/n): ").lower()
                if confirm == 'y':
                    for item in items_to_sell:
                        sell_price = item.value // 2
                        self.player.gold += sell_price
                        self.player.inventory.remove(item)
                        self.shop.add_item(item, 1)
                    print(f"You sold {len(items_to_sell)} items for a total of {total_value} gold.")
                else:
                    print("Sale cancelled.")
            
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
            
            input("\nPress Enter to continue...")

    def equip_menu(self):
        while True:
            clear_screen()
            print("\n=== Equipment Menu ===")
            print("\nCurrently Equipped:")
            for slot, item in self.player.equipped.items():
                if item:
                    print(f"{slot.capitalize()}: {item.name}")
                    if item.attack > 0:
                        print(f"  Attack: +{item.attack}")
                    if item.defence > 0:
                        print(f"  Defence: +{item.defence}")
                else:
                    print(f"{slot.capitalize()}: None")

            print("\nInventory:")
            equippable_items = [item for item in self.player.inventory if item.type in self.player.equipped]
            for i, item in enumerate(equippable_items, 1):
                print(f"{i}. {item.name} (Type: {item.type.capitalize()})")

            choice = input("\nEnter the number of the item you want to equip (or 'q' to quit): ")
            if choice.lower() == 'q':
                break

            try:
                item_index = int(choice) - 1
                if 0 <= item_index < len(equippable_items):
                    selected_item = equippable_items[item_index]
                    current_item = self.player.equipped[selected_item.type]

                    print(f"\nComparing {selected_item.name} with current {selected_item.type}:")
                    print(f"Current {selected_item.type.capitalize()}: ", end="")
                    if current_item:
                        print(f"{current_item.name}")
                        print(f"  Attack: +{current_item.attack}")
                        print(f"  Defence: +{current_item.defence}")
                    else:
                        print("None")

                    print(f"New {selected_item.type.capitalize()}: {selected_item.name}")
                    print(f"  Attack: +{selected_item.attack}")
                    print(f"  Defence: +{selected_item.defence}")

                    if current_item:
                        attack_change = selected_item.attack - current_item.attack
                        defence_change = selected_item.defence - current_item.defence
                    else:
                        attack_change = selected_item.attack
                        defence_change = selected_item.defence

                    print(f"\nChanges if equipped:")
                    print(f"  Attack: {attack_change:+d}")
                    print(f"  Defence: {defence_change:+d}")

                    confirm = input("\nDo you want to equip this item? (y/n): ")
                    if confirm.lower() == 'y':
                        self.player.equip_item(selected_item)
                        print(f"\n{selected_item.name} equipped!")
                else:
                    print("Invalid item number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")

            input("\nPress Enter to continue...")

    def use_item_menu(self, in_combat=False, enemy=None):
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
                elif in_combat:
                    if selected_item.effect_type in ["healing", "damage", "buff"]:
                        return self.use_combat_item(selected_item, enemy)
                    else:
                        print(f"You can't use {selected_item.name} in combat.")
                else:
                    success, message = self.player.use_item(selected_item)
                    print(message)
                    return selected_item if success else None
            else:
                print("Invalid choice. Please try again.")
        
    def choose_save_file(self, for_loading=False):
        save_files = get_save_files()
        if not save_files:
            if for_loading:
                print("No save files found.")
                return None
            else:
                return input("Enter a name for your new save file: ") + ".json"
        
        print("Available save files:")
        for i, file in enumerate(save_files, 1):
            print(f"{i}. {file}")
        
        if not for_loading:
            print(f"{len(save_files) + 1}. Create a new save file")
        
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(save_files):
                    return save_files[choice - 1]
                elif not for_loading and choice == len(save_files) + 1:
                    return input("Enter a name for your new save file: ") + ".json"
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
    def game_loop(self):
        #Main game loop that handles player actions.
        while True:
            action = title_screen()
            
            if action == "new_game":
                self.create_character()
                break
            elif action == "load_game":
                save_file = self.choose_save_file(for_loading=True)
                if save_file:
                    loaded_player, loaded_location = load_game(save_file)
                    if loaded_player and loaded_location:
                        self.player = loaded_player
                        self.current_location = loaded_location
                        break
                    else:
                        print("Failed to load the game. Starting a new game.")
                        self.create_character()
                        break
                else:
                    print("No save file selected. Returning to main menu.")
                    input("Press Enter to continue...")
        
        while True:
            self.player.update_cooldowns()
            self.show_status()
            if self.current_location == "Village":
                action = input("\nWhat do you want to do?\n[m]ove\n[i]nventory\n[c]onsumables\n[e]quip"
                            "\n[u]se item\n[s]hop\n[r]est\n[v]iew map\n[sa]ve game\n[q]uit\n>").lower()
            else:
                action = input("\nWhat do you want to do?\n[m]ove\n[i]nventory\n[c]onsumables\n[e]quip"
                            "\n[l]ocation actions\n[u]se item\n[v]iew map\n[sa]ve game\n[q]uit\n>").lower()
            if action == "m":
                clear_screen()
                self.world_map.display_map(self.current_location, self.player.level)
                run_location_actions = self.move()
                if run_location_actions:
                    self.location_actions()
            elif action == "i":
                clear_screen()
                self.player.show_inventory()
                pause()
            elif action == "c":
                clear_screen()
                self.player.show_consumables()
                self.player.show_cooldowns()
                pause()
            elif action == "e":
                clear_screen()
                self.equip_menu()
            elif action == "u":
                clear_screen()
                self.use_item_menu()
            elif action == "r":
                self.rest()
                pause()
            elif action == "v":
                self.world_map.display_map(self.current_location, self.player.level)
            elif action == "q":
                save_option = input("Do you want to save before quitting? (y/n): ").lower()
                if save_option == "y":
                    save_file = self.choose_save_file()
                    save_game(self.player, self.current_location, save_file)
                print("Thanks for playing!")
                title_screen()
            elif action == "l" and self.current_location != "Village":
                clear_screen()
                self.location_actions()
            elif action == "s" and self.current_location == "Village":
                self.shop_menu()
            elif action == "sa":
                save_file = self.choose_save_file()
                save_game(self.player, self.current_location, save_file)
            else:
                print("Invalid action. Try again.")
            
            self.show_status()    
            self.shop.rotate_stock(self.player.level)  # Check if it's time to rotate stock after each action

if __name__ == "__main__":
    game = Game()
    game.game_loop()