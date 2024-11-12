import random
from display import *
from player import Player
from enemies import create_enemy, Enemy
from items import initialise_items
from shop import Armourer, Alchemist, Inn
from battle import Battle
from world_map import WorldMap
from save_system import save_game, load_game, get_save_files
from random_events import *

class Game:
    def __init__(self):
        #Initializes the game with default settings and items.
        self.player = None
        self.current_location = "Village"
        self.world_map = WorldMap()
        self.items = initialise_items()
        self.armourer = Armourer(self.items)
        self.alchemist = Alchemist(self.items)
        self.inn = Inn(self.items)
        self.battle = None
        self.random_events = RandomEventSystem()
        
        #Stocks the shops initially
        self.armourer.stock_shop()
        self.alchemist.stock_shop()
        self.inn.stock_shop()
        
        from autosave import AutosaveManager
        self.autosave_manager = AutosaveManager(self)

    def create_character(self):
        #Creates a new player character.
        name = input("Enter your character's name: ")
        self.player = Player(name)
        self.initialise_battle()
        print(f"\nWelcome, {self.player.name}! Your adventure begins in the Village.")
        print("\nAutosave is enabled and will save your game every 10 turns.")
        print("You can toggle autosave on/off using the [au] command.")
        print("The system keeps your 3 most recent autosaves.")
        pause()
        
    def initialise_battle(self):
        #Ensures that battles are enabled even on reload
        if self.player is not None:
            self.battle = Battle(self.player, self.items, self)
        
    def show_stats(self):
        clear_screen()
        self.player.show_stats()
        print(f"Current location: {self.current_location}\nDay: {self.player.days}")
                
    def move(self):
        #Handles player movement between locations
        clear_screen()
        print("\nConnected locations:")
        #Shows locations connected to current location using helper function
        connected_locations = self.world_map.get_connected_locations(self.current_location) 
        #Creates list of available locations if player meets level requirements
        available_locations = [] 
        
        for i, location in enumerate(connected_locations, 1):
            min_level = self.world_map.get_min_level(location)
            if self.player.level >= min_level:
                print(f"{i}. {location} (Required Level: {min_level})")
                available_locations.append(location)
            else:
                print(f"X. {location} (Required Level: {min_level}) [LOCKED]")
        
        while True:
            #Allows player to enter either location number, name or letters
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
        if self.player.stamina < 5:
            print("You do not have enough energy to move, please rest up!")
            pause()
        elif self.player.level >= min_level:
            self.current_location = destination
            self.player.add_visited_location(destination)
            print(f"You have arrived at {self.current_location}.")
            self.player.use_stamina(5)
            if self.current_location == "Village":
                print("Welcome to the Village! You can rest, shop, or prepare for your next adventure here.")
                return False  # Indicate that we should not run location actions
            else:
                return True  # Indicate that we should run location actions
        else:
            #If player isn't correct level, rejects move request
            print(f"You need to be at least level {min_level} to enter {destination}.")
            return False
        
    def location_actions(self):
        #Handles actions available at the current location.
        while True:
            self.player.show_stats()
            action = input("\nWhat would you like to do?\n[e]xplore\n[u]se item\n[r]est\n[l]eave\n>").lower()
            if action == 'e':
                clear_screen()
                self.encounter()
                input("\nPress enter to continue...")
            elif action == 'u':
                clear_screen()
                self.use_item_menu()
                pause()
            elif action == 'r':
                clear_screen()
                self.rest()
            elif action == 'l':
                break
            else:
                print("Invalid action. Try again.")

    def encounter(self):
    # Check to see if random event triggers
        if self.random_events.trigger_random_event(self.player, self):
            return

        # Handles enemy encounters during exploration.
        possible_enemies = self.world_map.get_enemies(self.current_location)
        if possible_enemies and random.random() < 0.7:
            enemy_type = random.choice(possible_enemies)
            enemy = create_enemy(enemy_type, self.player)
            
            if enemy:
                print(f"You encountered a {enemy.name}!")
                if hasattr(enemy, 'variant') and enemy.variant and 'lore' in enemy.variant:
                    print(enemy.variant['lore'])
                self.battle.battle(enemy)

                if self.current_location == "Village":
                    print("You find yourself back in the Village after your defeat.")
                    return
            else:
                print("You explored the area but found nothing of interest.")
        else:
            print("You explored the area but found nothing of interest.")

    def rest(self):
        clear_screen()
        #Restores a portion of the player's health and stamina
        heal_amount = self.player.max_hp // 4  # Heal 25% of max HP
        stamina_restore = self.player.max_stamina // 4 # Restores 25% of max stamina
        self.player.heal(heal_amount)
        self.player.restore_stamina(stamina_restore)
        self.player.days += 1
        print(f"You rest and recover {heal_amount} HP and {stamina_restore} stamina.")
        print(f"It is now day {self.player.days}")

    def equip_menu(self):
        while True:
            clear_screen()
            print("\n=== Equipment Menu ===")
            print("\nCurrently Equipped:")
            for slot, item in self.player.equipped.items():
                if item:
                    print(f"{slot.capitalize()}: {item.name}")
                    stats = [
                        f"Attack: +{item.attack}" if item.attack > 0 else None,
                        f"Defence: +{item.defence}" if item.defence > 0 else None,
                        f"Accuracy: +{item.accuracy}" if item.accuracy > 0 else None,
                        f"Damage Reduction: +{item.damage_reduction}" if hasattr(item, 'damage_reduction') and item.damage_reduction > 0 else None,
                        f"Evasion: +{item.evasion}" if hasattr(item, 'evasion') and item.evasion > 0 else None,
                        f"Crit Chance: +{item.crit_chance}%" if hasattr(item, 'crit_chance') and item.crit_chance > 0 else None,
                        f"Crit Damage: +{item.crit_damage}%" if hasattr(item, 'crit_damage') and item.crit_damage > 0 else None,
                        f"Block Chance: +{item.block_chance}%" if hasattr(item, 'block_chance') and item.block_chance > 0 else None,
                    ]
                    if slot == "weapon":
                        stamina_cost = self.player.get_weapon_stamina_cost(item.weapon_type)
                        stats.append(f"Stamina use: {stamina_cost}")
                        stats.append(f"Weapon type: {item.weapon_type.title()}")
                    print("  " + ", ".join(filter(None, stats)))
                else:
                    print(f"{slot.capitalize()}: None")

            print("\nInventory:")
            equippable_items = [item for item in self.player.inventory if item.type in self.player.equipped]
            for i, item in enumerate(equippable_items, 1):
                stats = [
                    f"Attack: +{item.attack}" if item.attack > 0 else None,
                    f"Accuracy: +{item.accuracy}" if item.accuracy > 0 else None,
                    f"Armour Penetration: +{item.armour_penetration}" if item.armour_penetration > 0 else None,
                    f"Defence: +{item.defence}" if item.defence > 0 else None,
                    f"Damage Reduction: +{item.damage_reduction}" if hasattr(item, 'damage_reduction') and item.damage_reduction > 0 else None,
                    f"Evasion: +{item.evasion}" if hasattr(item, 'evasion') and item.evasion > 0 else None,
                    f"Crit Chance: +{item.crit_chance}%" if hasattr(item, 'crit_chance') and item.crit_chance > 0 else None,
                    f"Crit Damage: +{item.crit_damage}%" if hasattr(item, 'crit_damage') and item.crit_damage > 0 else None,
                    f"Block Chance: +{item.block_chance}%" if hasattr(item, 'block_chance') and item.block_chance > 0 else None,
                ]
                if item.type == "weapon":
                    stamina_cost = self.player.get_weapon_stamina_cost(item.weapon_type)
                    stats.append(f"Stamina Cost: {stamina_cost}")
                    stats.append(f"Weapon type: {item.weapon_type.title()}")
                print(f"{i}. {item.name} (Type: {item.type.capitalize()}) - " + ", ".join(filter(None, stats)))

            choice = input("\nEnter the number of the item you want to equip (or 'q' to quit): ")
            if choice.lower() == 'q':
                break

            try:
                item_index = int(choice) - 1
                if 0 <= item_index < len(equippable_items):
                    selected_item = equippable_items[item_index]
                    current_item = self.player.equipped[selected_item.type]
                    print(f"\nComparing {selected_item.name} with current {selected_item.type}:")
                    self.compare_items(current_item, selected_item)
                    confirm = input("\nDo you want to equip this item? (y/n): ")
                    if confirm.lower() == 'y':
                        self.player.equip_item(selected_item)
                        print(f"\n{selected_item.name} equipped!")
                else:
                    print("Invalid item number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")

            self.player.recalculate_stats()
            input("\nPress Enter to continue...")

    def compare_items(self, current_item, new_item):
        def print_stat_change(stat_name, current_val, new_val):
            if current_val != new_val:
                change = new_val - current_val
                print(f"  {stat_name}: {current_val} -> {new_val} ({change:+d})")

        stats = [
            ("Attack", "attack"),
            ("Accuracy", "accuracy"),
            ("Armour Penetration", "armour_penetration"),
            ("Defence", "defence"),
            ("Damage Reduction", "damage_reduction"),
            ("Evasion", "evasion"),
            ("Crit Chance", "crit_chance"),
            ("Crit Damage", "crit_damage"),
            ("Block Chance", "block_chance"),
        ]

        for stat_name, stat_attr in stats:
            current_val = getattr(current_item, stat_attr, 0) if current_item else 0
            new_val = getattr(new_item, stat_attr, 0)
            print_stat_change(stat_name, current_val, new_val)

        if new_item.type == "weapon":
            current_stamina_cost = self.player.get_weapon_stamina_cost(current_item.weapon_type) if current_item else 0
            new_stamina_cost = self.player.get_weapon_stamina_cost(new_item.weapon_type)
            print_stat_change("Stamina Cost", current_stamina_cost, new_stamina_cost)
            print(f"  Weapon Type: {current_item.weapon_type.title() if current_item else 'None'} -> {new_item.weapon_type.title()}")
    
    def use_item_menu(self, in_combat=False, enemy=None):
        #Enables player to use items and makes sure that only usable items are shown
        usable_items = self.player.show_usable_items()
        if not usable_items:
            return None

        while True:
            #Allows player to use the item number or name to use item
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
                #Checks to see if selected item is on cooldown, if it is refuses the use
                if selected_item.name in self.player.cooldowns and self.player.cooldowns[selected_item.name] > 0:
                    print(f"You can't use {selected_item.name} yet. Cooldown: {self.player.cooldowns[selected_item.name]} turns.")
                elif in_combat:
                    if selected_item.effect_type in ["healing", "damage", "buff", "stamina"]:
                        return self.use_combat_item(selected_item, enemy)
                    else:
                        print(f"You can't use {selected_item.name} in combat.")
                else:
                    success, message = self.player.use_item(selected_item, self)
                    print(message)
                    if success:
                        pause()
                    return selected_item if success else None
            else:
                print("Invalid choice. Please try again.")
        
    def choose_save_file(self, for_loading=False):
        #Allows the player to choose which save file they wish to overwrite if available, if not allows the player to make one
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
            #Creates a new character if new game is selected
            if action == "new_game":
                self.create_character()
                break
            elif action == "load_game":
                #If load game is selected, asks the player to select which save they want to use, if not returns the player to main menu
                save_file = self.choose_save_file(for_loading=True)
                if save_file:
                    #If save file is selected sets the current player and location to the data saved, if it fails automatically starts new character creation
                    loaded_player, loaded_location= load_game(save_file)
                    if loaded_player and loaded_location:
                        self.player = loaded_player
                        self.current_location = loaded_location
                        self.player.recalculate_stats()
                        self.initialise_battle()
                        break
                    else:
                        print("Failed to load the game. Starting a new game.")
                        self.create_character()
                        break
                else:
                    print("No save file selected. Returning to main menu.")
                    input("Press Enter to continue...")
        
        while True:
            self.player.update_cooldowns() #Reduces the cooldown on items by 1 on every action (Might change to only occur during battles)
            self.player.update_buffs() #Reduces the duration of buffs by 1
            self.show_stats() #Ensures the player can see their status easily
            if self.current_location == "Village":
                #Provides a set of options players can do if in the village, such as using shops and resting, otherwise prevents these actions
                action = input("\nWhat do you want to do?\n[m]ove\n[i]nventory\n[c]onsumables\n[e]quip"
                            "\n[u]se item\n[a]lchemist\n[ar]mourer\n[in]n\n[r]est\n[v]iew map\n[k]ill log\n[sa]ve game\n[au]tosave toggle\n[q]uit\n>").lower()
            else:
                action = input("\nWhat do you want to do?\n[m]ove\n[i]nventory\n[c]onsumables\n[e]quip"
                            "\n[l]ocation actions\n[u]se item\n[v]iew map\n[k]ill log\n[sa]ve game\n[au]tosave toggle\n[q]uit\n>").lower()
            #Handling of choices by player depending on what is chosen
            if action == "m":
                #Moves the palyer to different location if level requirements met
                clear_screen()
                self.world_map.display_map(self.current_location, self.player.level, self.player)
                self.move()
                if self.current_location != "Village":
                    self.location_actions()
            elif action == "i":
                #Open the player inventory
                clear_screen()
                self.player.show_inventory()
                pause()
            elif action == "c":
                #Shows the players consumables and cooldowns active
                clear_screen()
                self.player.show_consumables()
                self.player.show_cooldowns()
                pause()
            elif action == "e":
                #Opens the equip menu
                clear_screen()
                self.equip_menu()
            elif action == "u":
                #Opens the item usage menu
                clear_screen()
                used_item = self.use_item_menu()
                if used_item:
                    self.player.show_cooldowns()
                pause()
            elif action == "r":
                #Rests the player restoring 25% health
                self.rest()
                pause()
            elif action == "in":
                #Accesses the inn
                self.inn.inn_menu(self.player)
            elif action == "v":
                #Opens the world map for the player
                self.world_map.display_map(self.current_location, self.player.level, self.player)
            elif action == "k":
                self.player.display_kill_stats()
                pause()
            elif action == "q":
                #Prompts the player if they want to save the game before quitting
                save_option = input("Do you want to save before quitting? (y/n): ").lower()
                if save_option == "y":
                    save_file = self.choose_save_file()
                    save_game(self.player, self.current_location, self.player.days, save_file)
                print("Thanks for playing!")
                return
            elif action == "l" and self.current_location != "Village":
                #Opens the location actions if the player is not in the village
                clear_screen()
                self.location_actions()
            elif action == "ar" and self.current_location == "Village":
                #Accesses the weapon and armour store as long as the player is in the village location
                self.armourer.shop_menu(self.player)
            elif action == "a" and self.current_location == "Village":
                #Accesses the alchemist (consumables) shop as long as the player is in the village location
                self.alchemist.shop_menu(self.player)
            elif action == "sa":
                #Allows the player to save at any point in case of unexpected crashes, will look into making an autosave feature
                save_file = self.choose_save_file()
                save_game(self.player, self.current_location, save_file)
            elif action == "au":
                self.autosave_manager.toggle_autosave()
            elif action == "d":
                self.player.print_debug_modifiers()
                pause()
            else:
                print("Invalid action. Try again.")
              
            self.armourer.rotate_stock(self.player.level)  # Check if it's time to rotate stock after each action
            self.alchemist.rotate_stock(self.player.level) #^
            self.inn.rotate_stock(self.player.level)#^^
            self.autosave_manager.increment_turn() # Increments turn for autosave manager function

if __name__ == "__main__":
    game = Game()
    game.game_loop()