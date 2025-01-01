import random
import pygame
from display import *
from player import Player
from enemies import create_enemy, Enemy
from items import initialise_items
from shop import Blacksmith, Alchemist, Inn
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
        self.blacksmith = Blacksmith(self.items)
        self.alchemist = Alchemist(self.items)
        self.inn = Inn(self.items)
        self.battle = None
        self.random_events = RandomEventSystem()
        self.display = Display()
        self.display.set_game(self)
        self.battle_display = BattleDisplay(self.display)
        self.config = DisplayConfig()
        
        #Stocks the shops initially
        self.blacksmith.stock_shop()
        self.alchemist.stock_shop()
        self.inn.stock_shop()
        
        from autosave import AutosaveManager
        self.autosave_manager = AutosaveManager(self)

    def create_character(self):
        """Create a new player character with a visual interface"""
        visual_input = VisualInput(self.display)
        
        while True:
            self.display.screen.fill('black')
            
            # Draw title
            self.display.draw_text("=== CHARACTER CREATION ===", 
                                (self.config.SCREEN_WIDTH // 2, 50), 
                                'title', center=True)
            
            # Draw name input prompt
            self.display.draw_text("Enter your name:", 
                                (self.config.SCREEN_WIDTH // 2, 150), 
                                'huge', center=True)
            
            # Draw input box
            input_x = (self.config.SCREEN_WIDTH - visual_input.width) // 2
            input_y = 200
            visual_input.draw(input_x, input_y)
            
            # Draw instructions
            self.display.draw_text("Press ENTER when finished", 
                                (self.config.SCREEN_WIDTH // 2, 300), 
                                'medium', center=True)
            
            pygame.display.flip()
            self.display.clock.tick(self.display.config.FPS)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                    
                if visual_input.handle_event(event):
                    self.player = Player(visual_input.text)
                    self.player.give_starter_items()
                    self.initialise_battle()
                    
                    # Show welcome message
                    self.display.screen.fill('black')
                    self.display.draw_text(f"Welcome, {self.player.name}!", 
                                        (self.config.SCREEN_WIDTH // 2, 150), 
                                        'huge', center=True)
                    self.display.draw_text("Your adventure begins in the Village.", 
                                        (self.config.SCREEN_WIDTH // 2, 250), 
                                        'large', center=True)
                    self.display.draw_text("Autosave is enabled and will save your game every 10 turns.", 
                                        (self.config.SCREEN_WIDTH // 2, 350), 
                                        'medium', center=True)
                    self.display.draw_text("Press ENTER to continue...", 
                                        (self.config.SCREEN_WIDTH // 2, 450), 
                                        'medium', center=True)
                    pygame.display.flip()
                    
                    # Wait for enter press
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                waiting = False
                            elif event.type == pygame.QUIT:
                                return None
                                
                        self.display.clock.tick(self.display.config.FPS)
                    
                    return self.player
        
    def initialise_battle(self):
        #Ensures that battles are enabled even on reload
        if self.player is not None:
            self.battle = Battle(self.player, self.items, self)
        
    def show_stats(self):
        self.display.clear_screen()
        self.player.show_stats()
        print(f"Current location: {self.current_location}\nDay: {self.player.days}")
        
    def location_actions(self):
        menu = LocationActionsMenu(self.display, self.player)
        while True:
            result = menu.show_actions_menu(self)
            if result == "quit":
                return "quit"
            elif not result:
                break

    def encounter(self):
        # Check to see if random event triggers
        self.display.text_buffer.clear()
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
                    self.battle_display.draw_battle_message("You find yourself back in the Village after your defeat.")
                    return
            else:
                print("You explored the area but found nothing of interest.")
        else:
            print("You explored the area but found nothing of interest.")

    def rest(self):
        #self.display.draw_game_screen(self.player, self.current_location)
        #Restores a portion of the player's health and stamina
        heal_amount = self.player.max_hp // 4  # Heal 25% of max HP
        stamina_restore = self.player.max_stamina // 4 # Restores 25% of max stamina
        self.player.heal(heal_amount)
        self.player.restore_stamina(stamina_restore)
        self.player.days += 1
        layout = self.display.calculate_layout()
        self.display.draw_panel(*layout['battle_log_panel'])
        self.display.draw_text(f"You rest and recover {heal_amount} HP and {stamina_restore} stamina.",
                               (self.display.config.SCREEN_WIDTH // 2, self.display.config.SCREEN_HEIGHT - 250),
                               'large', center=True)
        self.display.draw_text(f"It is now day {self.player.days}",
                               (self.display.config.SCREEN_WIDTH // 2, self.display.config.SCREEN_HEIGHT - 200),
                               'large', center=True)

    def equip_menu(self):
        equipment_menu = EquipmentMenu(self.display, self.player)
        equipment_menu.show_equipment_menu()
        self.player.recalculate_stats
        self.display.draw_game_screen(self.player, self.current_location)
    
    def use_item_menu(self, in_combat=False, enemy=None):
        """Visual menu for using items"""
        if in_combat:
            self.battle_display.draw_battle_screen(self.player, game.current_location, enemy)
        else:
            self.display.draw_game_screen(self.player, self.current_location)
        
        layout = self.display.calculate_layout()
        battle_log = layout['battle_log_panel']
        x = battle_log[2]
        y = battle_log[3]
        width = battle_log[0]
        height = battle_log[1]
        
        usable_items = [item for item in self.player.inventory 
                        if item.type in ["consumable", "food", "drink", "weapon coating", "soul_crystal"]]
        if not usable_items:
            if in_combat:
                self.display.draw_text("You have no usable items.",
                                    (x + width//2, y + 30), 'large', center=True)
            else:
                self.display.draw_text("You have no usable items.",
                                       (self.display.config.SCREEN_WIDTH // 2,
                                        self.display.config.SCREEN_HEIGHT - 250),
                                       'large', center=True)
            return None
        
        # Draw items in battle log area
        self.display.draw_panel(width, height, x, y)
        
        self.display.draw_text("Usable Items:", 
                            (x + width//2, y + 20), 'large', center=True)
        
        # Show items with scrolling if needed
        items_per_page = 6
        scroll_offset = 0
        
        while True:
            # Clear item display area
            self.display.draw_panel(width, height, x, y)
            
            # Group identical items
            item_groups = {}
            for item in usable_items:
                key = (item.name, item.type)
                if key in item_groups:
                    item_groups[key]['count'] += item.stack_size if hasattr(item, 'stack_size') else 1
                else:
                    item_groups[key] = {
                        'item': item,
                        'count': item.stack_size if hasattr(item, 'stack_size') else 1
                    }
            
            # Display visible items
            visible_groups = list(item_groups.values())[scroll_offset:scroll_offset + items_per_page]
            for i, group in enumerate(visible_groups):
                item = group['item']
                count = group['count']
                item_y = y + 60 + (i * 30)
                
                # Show cooldown if applicable
                if item.name in self.player.cooldowns and self.player.cooldowns[item.name] > 0:
                    cooldown_text = f"{item.name} x{count} (Cooldown: {self.player.cooldowns[item.name]})"
                    self.display.draw_text(f"{i+1}. {cooldown_text}",
                                        (x + 20, item_y), 'medium', colour='gray')
                else: 
                    if isinstance(item, SoulCrystal):
                        if item.used:
                            effect_desc = "Depleted"
                        else:
                            effect_desc = "Soul Crystal - see inventory for details"
                        self.display.draw_text(f"{i+1}. {item.name} ({effect_desc})",
                                            (x + 20, item_y), 'medium')
                    else:
                        # Show item with effect description
                        effect_desc = self.player.get_effect_description(item)
                        self.display.draw_text(f"{i+1}. {item.name} x{count}: {effect_desc}",
                                            (x + 20, item_y), 'medium')
            
            # Show navigation instructions
            instruction_y = y + 20
            if len(usable_items) > items_per_page:
                self.display.draw_text("UP/DOWN: Scroll | Select with 1-6 | ESC: Cancel",
                                    (x + width//2, instruction_y), 'medium', center=True)
            else:
                self.display.draw_text("Select with 1-6 | ESC: Cancel",
                                    (x + width//2, instruction_y), 'medium', center=True)
            
            pygame.display.flip()
            
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                        
                    elif event.key == pygame.K_UP and scroll_offset > 0:
                        scroll_offset -= 1
                        
                    elif event.key == pygame.K_DOWN:
                        if scroll_offset < len(usable_items) - items_per_page:
                            scroll_offset += 1
                            
                    elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                        index = event.key - pygame.K_1
                        if index < len(visible_groups):
                            selected_item = visible_groups[index]['item']
                            
                            if selected_item.name in self.player.cooldowns and self.player.cooldowns[selected_item.name] > 0:
                                continue
                                
                            if in_combat:
                                if selected_item.effect_type in ["healing", "damage", "buff", "stamina"]:
                                    return self.battle.use_combat_item(selected_item, enemy)
                                else:
                                    continue
                            else:
                                success, message = self.player.use_item(selected_item)
                                if success and selected_item.effect_type == "teleport":
                                    destination = self.player.use_teleport_scroll(game)
                                    if destination:
                                        self.current_location = destination
                                        return selected_item
                                elif success:
                                    return selected_item
                            self.display.pause()    
                            # Refresh the display after use
                            pygame.draw.rect(self.display.screen, 'gray20', 
                                        (x, y, width, height))
            
            self.display.clock.tick(self.display.config.FPS)
        
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
                
    def handle_save(self):
        """Handle visual save menu"""
        from display import SaveMenuDisplay
        save_menu = SaveMenuDisplay(self.display, self.player)
        save_file = save_menu.show_save_menu()
        
        if save_file:
            save_game(self.player, self.current_location, save_file)
            return True
        return False
    
    def handle_quit(self):
        """Handle game quit sequence"""
        save_menu = SaveMenuDisplay(self.display, self.player)
        
        self.display.screen.fill('black')
        self.display.draw_text("Save before quitting?",
                            (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT // 2 - 50), 
                            'large', center=True)
        self.display.draw_text("ENTER: Yes | ESC: No",
                            (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT // 2 + 50), 
                            'medium', center=True)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        save_menu.show_save_menu()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
            self.display.clock.tick(self.display.config.FPS)
        
        self.display.cleanup()
        return "quit"
    
    def handle_game_events(self):
        """Handle game events and player actions"""
        self.display.draw_game_screen(self.player, self.current_location)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.handle_quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return self.handle_quit()
                
                # Process the input and update state
                action_type = self.process_input(event.key)
                if action_type == "quit":
                    return self.handle_quit()
                elif action_type in ["move", "rest", "explore"]:
                    # Update state only when input was processed
                    self.player.update_cooldowns()
                    self.player.update_buffs()
                    self.blacksmith.rotate_stock(self.player.level)
                    self.alchemist.rotate_stock(self.player.level)
                    self.inn.rotate_stock(self.player.level)
                    self.autosave_manager.increment_turn()
                    
        return None
    
    def process_input(self, key):
        """Process keyboard input and return True is state should update"""
        # General commands available everywhere
        if key == pygame.K_ESCAPE or key == pygame.K_q:
            return "quit"
        elif key == pygame.K_m:
            if self.display.handle_movement(self):
                return "move"
        elif key == pygame.K_i:
            self.display.clear_screen()
            self.player.show_inventory()
            self.display.pause()
            return True
        elif key == pygame.K_e:
            self.display.clear_screen()
            self.equip_menu()
            return True
        elif key == pygame.K_u:
            used_item = self.use_item_menu()
            if used_item:
                self.player.show_cooldowns()
            self.display.pause()
            return True
        elif key == pygame.K_v:
            self.world_map.display_map(self.current_location, self.player.level, self.player)
            return True
        elif key == pygame.K_k:
            self.player.display_kill_stats()
            self.display.pause()
            return True
        elif key == pygame.K_s:
            self.handle_save()
            return True
        elif key == pygame.K_t:
            self.autosave_manager.toggle_autosave()
            return True
        elif key == pygame.K_r:
            self.rest()
            self.display.pause()
            return "rest"

        # Village-specific commands
        if self.current_location == "Village":
            if key == pygame.K_a:
                self.alchemist.visual_shop_menu(self.player)
                return True
            elif key == pygame.K_b:
                self.blacksmith.visual_shop_menu(self.player)
                return True
            elif key == pygame.K_n:
                self.inn.inn_menu(self.player)
                return True
            
        # Non-Village specific commands
        if self.current_location != "Village":
            if key == pygame.K_l:
                self.location_actions()
                return True

        return None
    
        
    def game_loop(self):
        #Main game loop that handles player actions.
        while True:
            action = self.display.display_title()
            if action == "quit":
                self.display.cleanup()
                return
            #Creates a new character if new game is selected
            elif action == "new_game":
                self.create_character()
                break
            elif action == "load_game":
                #If load game is selected, asks the player to select which save they want to use, if not returns the player to main menu
                save_file = self.display.display_load_game()
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
                        self.display.draw_text("Failed to load game. Starting new character creation.", (self.config.TEXT_AREA_X + self.config.PADDING, self.config.TEXT_AREA_Y + 25))
                        self.create_character()
                        break
                else:
                    self.display.clear_screen()
                    self.display.draw_text("No save file selected. Returning to main menu.", ((self.config.SCREEN_WIDTH // 2), (self.config.SCREEN_HEIGHT // 2) - 50), size='large', center=True)
                    self.display.pause()
            elif action == "help":
                self.display.display_help()
        
        # Main game loop
        while True:
            self.display.draw_game_screen(self.player, self.current_location)
            result = self.handle_game_events()
            if result == "quit":
                return
            
            self.display.clock.tick(self.display.config.FPS)

if __name__ == "__main__":
    game = Game()
    game.game_loop()