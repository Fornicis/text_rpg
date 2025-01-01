import pygame
import sys
from dataclasses import dataclass
from items import SoulCrystal

@dataclass
class DisplayConfig:
    SCREEN_WIDTH: int = 1680
    SCREEN_HEIGHT: int = 1050
    FPS: int = 60
    PADDING: int = 10
    MENU_SPACING: int = 20
    TEXT_AREA_WIDTH: int = 900
    TEXT_AREA_HEIGHT: int = 150
    TEXT_AREA_X: int = 390
    TEXT_AREA_Y: int = 750
    MAX_TEXT_LINES: int = 30

class FontManager:
    SIZES = {
        'tiny': 12,
        'small': 16,
        'medium': 20,
        'large': 24,
        'huge': 32,
        'title': 40
    }
    
    @staticmethod
    def get_font(size='medium'):
        return pygame.font.SysFont("Comic Sans MS", FontManager.SIZES[size])

class Display:
    def __init__(self):
        pygame.init()
        self.config = DisplayConfig()
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.text_buffer = []
        self.scroll_offset = 0
        self.max_scroll_lines = 30
        self.game = None
        pygame.display.set_caption("TEXT RPG ADVENTURE")

    def set_game(self, game):
        self.game = game
    
    def clear_screen(self):
        self.screen.fill('black')
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return False
        return True

    def wait_for_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "new_game"
                    elif event.key == pygame.K_2:
                        return "load_game"
                    elif event.key == pygame.K_3:
                        return "help"
                    elif event.key == pygame.K_4:
                        return "quit"
                
            self.clock.tick(self.config.FPS)

    def draw_text(self, text, pos, size='medium', colour='white', center=False):
        font = FontManager.get_font(size)
        text_surface = font.render(text, True, colour)
        if center:
            rect = text_surface.get_rect(center=pos)
            self.screen.blit(text_surface, rect)
        else:
            self.screen.blit(text_surface, pos)

    def display_title(self):
        self.clear_screen()
        
        start_screen_image = pygame.image.load("assets/start_screen_images/start_screen.jpg")
        start_screen_image = pygame.transform.scale(start_screen_image, (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        start_screen_image.set_alpha(128)
        self.screen.blit(start_screen_image, (0, 0))
        
        title_pos = (self.config.SCREEN_WIDTH // 2, 100)
        self.draw_text("=== TEXT RPG ADVENTURE ===", title_pos, 'title', center=True)
        
        options = ["1. Play", "2. Load Game", "3. Help", "4. Quit"]
        for i, option in enumerate(options, 1):
            pos = (self.config.SCREEN_WIDTH // 2, 
                  200 + i * (self.config.MENU_SPACING * 2))
            self.draw_text(option, pos, 'large', center=True)
        
        pygame.display.flip()
        return self.wait_for_input()
    
    def display_load_game(self):
        from save_system import get_save_files
        """Display visual load game menu screen with scrolling"""
        save_files = get_save_files()
        if not save_files:
            return self.display_no_saves()
        
        scroll_offset = 0
        saves_per_page = 20
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and scroll_offset > 0:
                        scroll_offset -= 1
                    elif event.key == pygame.K_DOWN and scroll_offset < max(0, len(save_files) - saves_per_page):
                        scroll_offset += 1
                    elif event.key == pygame.K_RETURN:
                        selected = self.handle_save_selection(save_files, scroll_offset)
                        if selected is not None:
                            return selected
            
            self.screen.fill('black')
            
            # Draw title
            self.draw_text("=== LOAD GAME ===", 
                        (self.config.SCREEN_WIDTH // 2, 100), 
                        'title', center=True)
            self.draw_text("=== Press ENTER to enter save file selection ===",
                           (self.config.SCREEN_WIDTH // 2, 150),
                           'huge', center=True)
            # Draw save files
            start_idx = max(0, scroll_offset)
            end_idx = min(start_idx + saves_per_page, len(save_files))
            
            for i in range(start_idx, end_idx):
                pos = (self.config.SCREEN_WIDTH // 2, 
                    200 + (i - start_idx) * (self.config.MENU_SPACING * 2))
                self.draw_text(f"{i+1}. {save_files[i]}", pos, 'large', center=True)
            
            # Draw navigation instructions
            if len(save_files) > saves_per_page:
                self.draw_text("UP/DOWN: Scroll  Enter: Select  ESC: Back", 
                            (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 50), 
                            'medium', center=True)
            
            pygame.display.flip()
            self.clock.tick(self.config.FPS)

    def handle_save_selection(self, save_files, scroll_offset):
        """Handle numeric input for save file selection"""
        visual_input = VisualInput(self)
        
        while True:
            self.screen.fill('black')
            
            self.draw_text("Enter save number (ESC to cancel):", 
                        (self.config.SCREEN_WIDTH // 2, (self.config.SCREEN_HEIGHT // 2) - 100), 
                        'huge', center=True)
            
            input_x = (self.config.SCREEN_WIDTH - visual_input.width) // 2
            input_y = self.config.SCREEN_HEIGHT // 2 - 50
            visual_input.draw(input_x, input_y)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    return None
                    
                if visual_input.handle_event(event):
                    try:
                        index = int(visual_input.text) - 1
                        if 0 <= index < len(save_files):
                            return save_files[index]
                    except ValueError:
                        pass
                    visual_input.text = ""
            
            self.clock.tick(self.config.FPS)

    def display_no_saves(self):
        """Display message when no saves exist"""
        self.clear_screen()
        self.draw_text("=== LOAD GAME ===", 
                    (self.config.SCREEN_WIDTH // 2, 100), 
                    'title', center=True)
        self.draw_text("No save files found.", 
                    (self.config.SCREEN_WIDTH // 2, 200), 
                    'medium', center=True)
        self.draw_text("Press ESC to return", 
                    (self.config.SCREEN_WIDTH // 2, 300), 
                    'medium', center=True)
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    return None
                
    
    def display_help(self):
        help_text = [
            "=== TEXT RPG ADVENTURE HELP ===",
            "",
            "Welcome, brave adventurer! This guide will help you navigate your journey.",
            "",
            "GAME BASICS:",
            "- Your adventure begins in the Village, your home base.",
            "- Explore various locations, battle monsters, and collect loot to level up.",
            "- Your goal is to become strong enough to face the ultimate challenges in the Heavens.",
            "- You have 5 respawns granted by the deities in the Heavens, after your fifth one, it's game over.",
            "",
            "NAVIGATION:",
            "- Use the [m]ove command to travel between connected areas.",
            "- Some areas have level requirements to enter.",
            "- Use the [v]iew map command to see the world layout and available paths.",
            "",
            "COMBAT:",
            "- Battles are turn-based. Your options are:",
            "[a]ttack: Deal damage to the enemy (costs stamina based on weapon type)",
            "[u]se item: Use a consumable from your inventory",
            "[r]un: Attempt to flee (not always successful)",
            "- Defeating enemies grants EXP, gold, and sometimes loot.",
            "- Your stamina replenishes on level up and resting, it is used for attacks.",
            "",
            "INVENTORY AND EQUIPMENT:",
            "- Access your [i]nventory to see all your items.",
            "- Use the [e]quip command to manage your gear.",
            "- [c]onsumables can be viewed separately for quick access.",
            "- Equip better gear to increase your attack and defense stats.",
            "",
            "SHOPS:",
            "- Visit shops in the Village to buy and sell items:",
            "- [b]lacksmith: Buy and sell weapons and armour",
            "- [a]lchemist: Buy and sell potions and consumables",
            "- [in]n: Rest to restore HP and stamina, buy food and drinks",
            "- Shop inventories change periodically, so check back often.",
            "",
            "CHARACTER PROGRESSION:",
            "- Gain EXP by defeating enemies. Level up to increase your stats.",
            "- Higher levels unlock access to new areas with stronger enemies and better loot.",
            "",
            "CONSUMABLES AND BUFFS:",
            "- Use healing potions to restore HP during and outside of combat.",
            "- Buff items can temporarily increase your stats. Items which increase all stats increase Attack, Defence, Accuracy and Evasion.",
            "- Food and drinks can restore stamina and provide various effects.",
            "",
            "RANDOM EVENTS:",
            "- Random events can occur while exploring, which can aid or hinder your progress.",
            "- Some events may grant rewards, while others may impose penalties.",
            "",
            "SAVING AND LOADING:",
            "- Use the [sa]ve game command to save your progress.",
            "- Load your game from the main menu when starting the game.",
            "",
            "TIPS:",
            "- Rest at the Inn or use the [r]est command anywhere (reduced effectiveness) to restore HP and stamina.",
            "- Upgrade your equipment regularly to stay competitive.",
            "- Use the right weapon type for your playstyle (light, medium, or heavy).",
            "- Always carry healing items for tough battles.",
            "- Explore new areas as you level up, but be cautious of tough enemies.",
            "",
            "Remember, most actions can be performed by typing the letter in brackets,", 
            "e.g., 'm' for move, 'i' for inventory, etc.",
            "",
            "Good luck on your adventure!"
        ]

        scroll_offset = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_UP:
                        scroll_offset = max(0, scroll_offset - 20)
                    if event.key == pygame.K_DOWN:
                        scroll_offset += 20

            self.screen.fill('black')
            y_pos = 50 - scroll_offset
            
            for line in help_text:
                if 0 <= y_pos <= self.config.SCREEN_HEIGHT:
                    self.draw_text(line, (self.config.SCREEN_WIDTH // 2, y_pos), 'large', center=True)
                y_pos += self.config.MENU_SPACING

            self.draw_text("Use UP/DOWN arrows to scroll, ESC to return", 
                          (20, self.config.SCREEN_HEIGHT - 40))
            pygame.display.flip()
            self.clock.tick(self.config.FPS)

    def pause(self, show_prompt=True):
        if show_prompt:
            """self.draw_text("This is a test print to check if this is the issue",
                        (self.config.SCREEN_WIDTH //2, self.config.SCREEN_HEIGHT // 2 - self.config.PADDING *2),
                        'large', center=True)"""
            self.draw_text("Press ENTER to continue...", 
                        (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - self.config.PADDING * 4),
                        center=True)
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

    def update_game_screen(self, player):
        self.screen.fill('black')
        self.draw_game_screen(player, player.current_location)
        pygame.display.flip()
        self.clock.tick(self.config.FPS)

    def add_message(self, text):
        for line in text.split('\n'):
            if line.strip():
                self.text_buffer.append(line.strip())
                
        while len(self.text_buffer) > self.max_scroll_lines:
            self.text_buffer.pop(0)

    def calculate_layout(self):
        """Calculates the layout of the game screen based on the current window size."""
        width = self.config.SCREEN_WIDTH
        height = self.config.SCREEN_HEIGHT
        padding = self.config.PADDING
        
        # Player panel goes under location panel
        player_panel = {
            'width': width * 0.12,
            'height': height * 0.3,
            'x': padding,
            'y': padding
        }
        
        enemy_panel = {
            'width': width * 0.12,
            'height': height * 0.3,
            'x': width - (width * 0.12 + padding),
            'y': padding
        }
        
        # Command menu to the right of main area
        command_panel = {
            'width': width * 0.08,
            'height': height * 0.28,
            'x': width - (width * 0.08 + padding),
            'y': padding
        }
        
        # Main area to the right of player/location panels
        main_panel = {
            'width': width - ((player_panel['width'] + padding * 2) + (command_panel['width'] + padding * 2)),
            'height': height * 0.7,
            'x': player_panel['width'] + padding * 2,
            'y': padding
        }
        
        battle_panel = {
            'width': width - ((player_panel['width'] + padding * 2) + (enemy_panel['width'] + padding * 2)),
            'height': height * 0.7,
            'x': player_panel['width'] + padding * 2,
            'y': padding
        }
        
        # Bottom panels height
        bottom_height = height - (main_panel['height'] + (padding * 3))
        
        # Modified widths: status panels 0.75x, battle log 1.5x
        total_width = width - (padding * 2)
        unit_width = total_width / 3
        
        # Player status effects panel
        player_status_panel = {
            'width': unit_width * 0.75,
            'height': bottom_height,
            'x': padding,
            'y': main_panel['height'] + (padding * 2)
        }
        
        # Battle log
        battle_log_panel = {
            'width': unit_width * 1.5,
            'height': bottom_height,
            'x': player_status_panel['x'] + player_status_panel['width'] + padding,
            'y': main_panel['height'] + (padding * 2)
        }
        
        # Player status bars
        player_status_bars_panel = {
            'width': unit_width * 0.7,
            'height': padding,
            'x': player_panel['width'] + (padding * 2),
            'y': padding
        }
        
        # Attack animation panel
        attack_animation_panel = {
            'width': unit_width * 0.8,
            'height': padding * 4,
            'x': player_status_bars_panel['x'] + player_status_bars_panel['width'],
            'y': padding * 4
        }
        
        # Enemy status effects panel
        enemy_status_panel = {
            'width': unit_width * 0.75,
            'height': bottom_height,
            'x': battle_log_panel['x'] + battle_log_panel['width'] + padding,
            'y': main_panel['height'] + (padding * 2)
        }
        
        # Enemy status bars
        enemy_status_bars_panel = {
            'width': unit_width * 0.7,
            'height': padding,
            'x': battle_panel['width'] - enemy_panel['width'] + (padding * 3),
            'y': padding
        }
        
        # Player weapon buffs panel
        player_weapon_buffs_panel = {
            'width': player_panel['width'],
            'height': height - player_panel['height'] - bottom_height - padding * 4,
            'x': player_panel['x'],
            'y': player_panel['y'] + player_panel['height'] + padding
        }
        
        # Equipped equipment panel
        equipped_equipment_panel = {
            'width': width // 3,
            'height': height // 1.5,
            'x': padding * 2,
            'y': padding * 10
        }
        
        # Equipment comparison panel
        equipment_comparison_panel = {
            'width': width // 4,
            'height': height // 3,
            'x': equipped_equipment_panel['x'] + equipped_equipment_panel['width'] + padding * 5,
            'y': padding * 10
        }
        
        # Equipment inventory panel
        equipment_inventory_panel = {
            'width': equipped_equipment_panel['width'],
            'height': height // 1.5,
            'x': width - equipped_equipment_panel['width'] - padding * 2,
            'y': padding * 10
        }
        
        return {
            'player_panel': (player_panel['width'], player_panel['height'], 
                            player_panel['x'], player_panel['y']),
            'enemy_panel': (enemy_panel['width'], enemy_panel['height'], 
                            enemy_panel['x'], enemy_panel['y']),
            'main_panel': (main_panel['width'], main_panel['height'], 
                        main_panel['x'], main_panel['y']),
            'battle_panel': (battle_panel['width'], battle_panel['height'], 
                            battle_panel['x'], battle_panel['y']),
            'command_panel': (command_panel['width'], command_panel['height'], 
                            command_panel['x'], command_panel['y']),
            'player_status_panel': (player_status_panel['width'], player_status_panel['height'], 
                                player_status_panel['x'], player_status_panel['y']),
            'player_status_bars_panel': (player_status_bars_panel['width'], player_status_bars_panel['height'], 
                                player_status_bars_panel['x'], player_status_bars_panel['y']),
            'battle_log_panel': (battle_log_panel['width'], battle_log_panel['height'], 
                            battle_log_panel['x'], battle_log_panel['y']),
            'attack_animation_panel': (attack_animation_panel['width'], attack_animation_panel['height'], 
                            attack_animation_panel['x'], attack_animation_panel['y']),
            'enemy_status_panel': (enemy_status_panel['width'], enemy_status_panel['height'], 
                            enemy_status_panel['x'], enemy_status_panel['y']),
            'enemy_status_bars_panel': (enemy_status_bars_panel['width'], enemy_status_bars_panel['height'],    
                            enemy_status_bars_panel['x'], enemy_status_bars_panel['y']),
            'player_weapon_buffs_panel': (player_weapon_buffs_panel['width'], player_weapon_buffs_panel['height'], 
                                        player_weapon_buffs_panel['x'], player_weapon_buffs_panel['y']),
            'equipped_equipment_panel': (equipped_equipment_panel['width'], equipped_equipment_panel['height'], 
                                        equipped_equipment_panel['x'], equipped_equipment_panel['y']),
            'equipment_comparison_panel': (equipment_comparison_panel['width'], equipment_comparison_panel['height'], 
                                        equipment_comparison_panel['x'], equipment_comparison_panel['y']),
            'equipment_inventory_panel': (equipment_inventory_panel['width'], equipment_inventory_panel['height'], 
                                        equipment_inventory_panel['x'], equipment_inventory_panel['y'])
        }
    
    def calculate_text_dimensions(self, text, font_size='medium'):
        font = FontManager.get_font(font_size)
        text_surface = font.render(text, True, 'white')
        return text_surface.get_width(), text_surface.get_height()
    
    def draw_panel(self, width, height, x, y, content_list=None, font_size='medium', font_colour='white'):
        pygame.draw.rect(self.screen, 'gray20', (x, y, width, height))
        pygame.draw.rect(self.screen, 'gray', (x, y, width, height), 2)
        
        current_y = y + self.config.PADDING
        if content_list:
            for content in content_list:
                if current_y + self.calculate_text_dimensions(content, font_size)[1] > y + height - self.config.PADDING:
                    break
                self.draw_text(content, (x + self.config.PADDING, current_y), font_size, font_colour)
                current_y += self.calculate_text_dimensions(content, font_size)[1] + 5
    
    def draw_game_screen(self, player, current_location, enemy=None):
        self.screen.fill('black')
        layout = self.calculate_layout()
        # Draw player info panel (left side)
        self.draw_player_panel(player, *layout['player_panel'], current_location)
        # Draw main game area (centre)
        self.draw_main_area(*layout['main_panel'], current_location)
        # Draw battle log (bottom)
        self.draw_panels(player, enemy)
        # Draw command menu (right side)
        self.draw_command_menu(*layout['command_panel'], current_location)
        
        pygame.display.update()
        self.clock.tick(self.config.FPS)
        
    def draw_player_panel(self, player, width, height, x, y, location):    
        # Player stats
        stats = [
            f"Name: {player.name}",
            f"Location: {location}",
            f"Level: {player.level}",
            f"HP: {player.hp}/{player.max_hp}",
            f"Stamina: {player.stamina}/{player.max_stamina}",
            f"Gold: {player.gold}",
            "",
            f"Attack: {player.attack}",
            f"Accuracy: {player.accuracy}",
            f"Armour Penetration: {player.armour_penetration}",
            f"Crit Chance: {player.crit_chance}",
            f"Crit Damage: {player.crit_damage}",
            f"Defence: {player.defence}",
            f"Evasion: {player.evasion}",
            f"Block Chance: {player.block_chance}",
            f"Damage Reduction: {player.damage_reduction}"
        ]
        
        self.draw_panel(width, height, x, y, stats, font_colour='yellow')
            
    def draw_location_panel(self, location, width, height, x, y):
        content = [f"Location: {location}"]
        self.draw_panel(width, height, x, y, content, 'large')
        
    def draw_main_area(self, width, height, x, y, current_location):
        # Background
        self.draw_panel(width, height, x, y)
        
        # Map location to image path
        location_images = {
            "Village": "assets/area_images/village.jpg",
            "Forest": "assets/area_images/forest.jpg",
            "Plains": "assets/area_images/plains.jpg",
            "Deepwoods": "assets/area_images/deepwoods.jpg",
            "Cave": "assets/area_images/cave.jpg",
            "Swamp": "assets/area_images/swamp.jpg",
            "Temple": "assets/area_images/temple.jpg",
            "Mountain": "assets/area_images/mountain.jpg",
            "Desert": "assets/area_images/desert.jpg",
            "Valley": "assets/area_images/valley.jpg",
            "Toxic Swamp": "assets/area_images/toxic_swamp.jpg",
            "Ruins": "assets/area_images/ruins.jpg",
            "Mountain Peaks": "assets/area_images/mountain_peaks.jpg",
            "Scorching Plains": "assets/area_images/scorching_plains.jpg",
            "Shadowed Valley": "assets/area_images/shadowed_valley.jpg",
            "Death Caves": "assets/area_images/death_caves.jpg",
            "Ancient Ruins": "assets/area_images/ancient_ruins.jpg",
            "Death Valley": "assets/area_images/death_valley.jpg",
            "Dragons Lair": "assets/area_images/dragon_lair.jpg",
            "Volcanic Valley": "assets/area_images/volcanic_valley.jpg",
            "Heavens": "assets/area_images/heavens.jpg"
        }
        
        if current_location in location_images:
            try:
                # Load and scale image to fit the main area
                image = pygame.image.load(location_images[current_location])
                scaled_image = pygame.transform.scale(image, (width - 4, height - 4))
                self.screen.blit(scaled_image, (x + 2, y + 2))
            except pygame.error:
                # Fallback text if image loading fails
                font = FontManager.get_font('large')
                text = font.render(f"Current Location: {current_location}", True, 'white')
                text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
                self.screen.blit(text, text_rect)
    
    def draw_player_status_panel(self, width, height, x, y, player):
        self.draw_panel(width, height, x, y)
        
        self.draw_text("Player Status Effects:", (x + self.config.PADDING, y + self.config.PADDING))
        current_y_1 = y + 25 
        current_y_2 = y + self.config.PADDING
        
        if player and hasattr(player, 'status_effects'):
            for effect in player.status_effects:
                if effect.is_active:
                    effect_text = f"{effect.name} ({effect.remaining_duration} turns)"
                    if hasattr(effect, 'strength') and effect.strength > 1:
                        effect_text += f" ({effect.strength} stacks)"
                    self.draw_text(effect_text, (x + self.config.PADDING, current_y_1))
                    current_y_1 += 20
                    
        if hasattr(player, 'active_buffs') and player.active_buffs:
            current_y_1 += 10
            self.draw_text("Active Buffs:", (x + self.config.PADDING, current_y_1))
            current_y_1 += 20
            for stat, buff_info in player.active_buffs.items():
                if isinstance(buff_info, dict):
                    stat_name = stat.replace('_', ' ').title()
                    if 'duration' in buff_info:
                        buff_text = f"{stat_name} +{buff_info['value']} ({buff_info['duration']} turns)"
                    else:
                        buff_text = f"{stat_name} +{buff_info['value']}"
                    self.draw_text(buff_text, (x + self.config.PADDING, current_y_1))
                    current_y_1 += 20
        
        combat_buffs = []
        if hasattr(player, 'combat_buff_modifiers'):
            for stat, modifier in player.combat_buff_modifiers.items():
                if modifier > 0:
                    stat_name = stat.replace('_', ' ').title()
                    combat_buffs.append(f"{stat_name} +{modifier}")
            if combat_buffs:
                self.draw_text("Combat Buff Modifiers:", (x + width // 2, current_y_2))
                current_y_2 += 20
                for buff in combat_buffs:
                    self.draw_text(buff, (x + width // 2, current_y_2))
                    current_y_2 += 20
                    
        if hasattr(player, 'active_hots') and player.active_hots:
            self.draw_text("Active HoTs:", (x + width // 2, current_y_2))
            current_y_2 += 20
            for hot in player.active_hots:
                self.draw_text(f"{hot}:", (x + width // 2, current_y_2))
                current_y_2 += 20
                for value, duration in player.active_hots.items():
                    self.draw_text(f"+{duration['tick_effect']} HP per turn ({duration['duration']} turns)", (x + width // 2, current_y_2))
                    current_y_2 += 20
                    
        if hasattr(player, 'debuff_modifiers'):
            debuffs = []
            for stat, value in player.debuff_modifiers.items():
                if value > 0:
                    duration_text = ""
                    if hasattr(player, 'active_debuffs') and stat in player.active_debuffs:
                        duration = player.active_debuffs[stat]['duration']
                        duration_text = f" ({duration} turns)"
                    stat_name = stat.replace('_', ' ').title()
                    debuffs.append(f"{stat_name} -{value}{duration_text}")
                    
            if debuffs:
                current_y_1 += 10
                self.draw_text("Active Debuffs:", (x + self.config.PADDING, current_y_1))
                current_y_1 += 20
                for debuff_text in debuffs:
                    self.draw_text(debuff_text, (x + self.config.PADDING, current_y_1))
                    current_y_1 += 20

    def draw_battle_log_panel(self, width, height, x, y, scroll_offset=0, show_continue_prompt=False):
        self.draw_panel(width, height, x, y)
        
        if show_continue_prompt:
            self.draw_text("Press ENTER to continue...",
                           (x + width - 100, y + height - 30),
                           'medium', center=True)
        
        # Calculate maximum valid scroll offset
        max_display_lines = int((height - self.config.PADDING * 2) // 25)
        max_scroll = max(0, len(self.text_buffer) - max_display_lines)
        
        # Clamp scroll offset between 0 and max_scroll
        scroll_offset = max(0, min(scroll_offset, max_scroll))
        
        # Show scroll indicator if needed
        if len(self.text_buffer) > max_display_lines:
            self.draw_text(f"UP/DOWN Scroll", (x + width - 100, y + 10), 'small')
        
        # Get visible lines using clamped scroll offset 
        start_idx = len(self.text_buffer) - max_display_lines - scroll_offset
        start_idx = max(0, start_idx)
        visible_lines = self.text_buffer[start_idx:start_idx + max_display_lines]
        
        # Draw visible lines
        for i, line in enumerate(visible_lines):
            self.draw_text(line, 
                        (x + width //2, y + self.config.PADDING + i * 25),
                        'medium', center=True)

    def draw_enemy_status_panel(self, width, height, x, y, enemy):
        self.draw_panel(width, height, x, y)
        
        self.draw_text("Enemy Status Effects:", (x + self.config.PADDING, y + self.config.PADDING))
        if enemy and hasattr(enemy, 'status_effects'):
            current_y = y + 25
            for effect in enemy.status_effects:
                if effect.is_active:
                    effect_text = f"{effect.name} ({effect.remaining_duration} turns)"
                    if hasattr(effect, 'strength') and effect.strength > 1:
                        effect_text += f" ({effect.strength} stacks)"
                    self.draw_text(effect_text, (x + self.config.PADDING, current_y))
                    current_y += 20
                    
                    # Check debuff_modifiers for stat reductions
                    if hasattr(effect, 'stat_changes'):
                        for stat in effect.stat_changes:
                            if stat in enemy.debuff_modifiers and enemy.debuff_modifiers[stat] > 0:
                                reduction_text = f"  {stat.replace('_', ' ').title()}: -{enemy.debuff_modifiers[stat]}"
                                self.draw_text(reduction_text, (x + self.config.PADDING, current_y))
                                current_y += 20

    def draw_player_weapon_buff_panel(self, width, height, x, y, player):
        self.draw_panel(width, height, x, y)
        
        current_y = y + self.config.PADDING
        # Draw section title
        self.draw_text("Weapon Enhancements:", (x + self.config.PADDING, y + self.config.PADDING))
        current_y += 25
        # Draw weapon buff if active
        if player and player.weapon_buff and player.weapon_buff['duration'] > 0:
            for stat, value in player.weapon_buff_modifiers.items():
                if value > 0:
                    stat_name = stat.replace('_', ' ').title()
                    buff_text = f"{stat_name} +{value} ({player.weapon_buff['duration']} turns)"
                    self.draw_text(buff_text, (x + self.config.PADDING, current_y))
                    current_y += 25
            
        # Draw weapon coating if active
        if player and player.weapon_coating and player.weapon_coating['duration'] > 0:
            coating = player.weapon_coating
            coating_text = f"{coating['name']}"
            stack_text = f"{coating['stacks']} stacks"
            duration_text = f"({coating['remaining_duration']} attacks remaining)"
            self.draw_text(coating_text, (x + self.config.PADDING, current_y))
            current_y += 25
            self.draw_text(stack_text, (x + self.config.PADDING, current_y))
            current_y += 25
            self.draw_text(duration_text, (x + self.config.PADDING, current_y))
    
    def draw_panels(self, player, enemy=None, scroll_offset=0):
        layout = self.calculate_layout()
        self.draw_player_status_panel(*layout['player_status_panel'], player)
        self.draw_battle_log_panel(*layout['battle_log_panel'], scroll_offset)
        self.draw_enemy_status_panel(*layout['enemy_status_panel'], enemy)
        self.draw_player_weapon_buff_panel(*layout['player_weapon_buffs_panel'], player)
    
    def draw_command_menu(self, width, height, x, y, location):
        # Command menu
        if location == "Village":
            commands = [
                "[m]ove", "[i]nventory", "[e]quip",
                "[a]lchemist", "[b]lacksmith", "in[n]", "[r]est",
                "[u]se item", "[v]iew map", "[k]ill log", "[s]ave game",
                "autosave [t]oggle", "[q]uit"
            ]
        else:
            commands = [
                "[m]ove", "[i]nventory", "[e]quip",
                "[r]est", "[u]se item", "[v]iew map", "[k]ill log",
                "autosave [t]oggle", "[s]ave game","[q]uit"
            ]
        
        self.draw_panel(width, height, x, y, commands)
        
    def display_movement_options(self, current_location, connected_locations, player_level):
        from world_map import WorldMap
        """Display movement options in the battle log area"""
        self.world_map = WorldMap()
        layout = self.calculate_layout()
        battle_log_x = layout['battle_log_panel'][2]
        battle_log_y = layout['battle_log_panel'][3]
        battle_log_width = layout['battle_log_panel'][0]
        battle_log_height = layout['battle_log_panel'][1]
        
        line_height = 30
        center_x = battle_log_x + (battle_log_width // 2)
        base_y = battle_log_y + battle_log_height // 4
        
        # Clear previous text
        self.draw_panel(battle_log_width, battle_log_height, battle_log_x, battle_log_y)
        
        self.draw_text("Connected locations:", 
                    (center_x, base_y), 
                    'large', center=True)
        
        available_locations = []
        for i, location in enumerate(connected_locations, 1):
            min_level = self.world_map.get_min_level(location)
            y_pos = base_y + (i * line_height)
            
            if player_level >= min_level:
                self.draw_text(f"{i}. {location} (Required Level: {min_level})",
                            (center_x, y_pos),
                            'large', center=True)
                available_locations.append(location)
            else:
                self.draw_text(f"X. {location} (Required Level: {min_level}) [LOCKED]",
                            (center_x, y_pos), 'large',
                            colour='red',
                            center=True)
                
        self.draw_text("Enter location number or press ESC to cancel",
                    (center_x, base_y + ((len(connected_locations) + 2) * line_height)),
                    'large', center=True)
        
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):
                        index = event.key - pygame.K_1
                        if index < len(available_locations):
                            return available_locations[index]
            
            self.clock.tick(self.config.FPS)
        
        return None

    def handle_movement(self, game):
        """Handle player movement between locations"""
        connected_locations = game.world_map.get_connected_locations(game.current_location)
        destination = self.display_movement_options(game.current_location, connected_locations, game.player.level)
        
        if destination:
            min_level = game.world_map.get_min_level(destination)
            layout = self.calculate_layout()
            battle_log_y = layout['battle_log_panel'][3]
            battle_log_x = layout['battle_log_panel'][2]
            battle_log_height = layout['battle_log_panel'][1]
            battle_log_width = layout['battle_log_panel'][0]
            base_y = battle_log_y + battle_log_height // 3
            center_x = battle_log_x + (battle_log_width // 2)
            
            if game.player.stamina < 5:
                self.draw_text("You do not have enough energy to move, please rest up!",
                            (center_x, base_y), size = 'large',
                            colour='red', center=True)
            elif game.player.level >= min_level:
                game.current_location = destination
                game.player.add_visited_location(destination)
                game.player.use_stamina(5)
                self.draw_game_screen(game.player, game.current_location)
                self.draw_panel(battle_log_width, battle_log_height, battle_log_x, battle_log_y)
                self.draw_text(f"You have arrived at the {game.current_location}.",
                            (center_x, base_y), size = 'large', colour='green', center=True)
                if destination == "Village":
                    self.draw_text("Welcome to the Village! You can rest at the Inn, shop, and prepare for your next adventure here.",
                                (center_x, base_y + 25), size = 'large', colour='green', center=True)
                    
                self.draw_text("Press ENTER to continue...",
                            (center_x, base_y + 50), size = 'large', colour='green', center=True)
                
                pygame.display.flip()
                self.wait_for_input()
                return True
        return False
    
    def cleanup(self):
        pygame.quit()
        
@dataclass
class ShopDisplayConfig:
    ITEM_HEIGHT: int = 60
    ITEMS_PER_PAGE: int = 12
    DESCRIPTION_WIDTH: int = 400
    SHOP_PANEL_WIDTH: int = 800
    SHOP_PANEL_HEIGHT: int = 700
    BUTTON_HEIGHT: int = 40
    BUTTON_WIDTH: int = 120
    BUTTON_PADDING: int = 10

class ShopDisplay:
    def __init__(self, display, player):
        self.display = display
        self.config = ShopDisplayConfig()
        self.scroll_offset = 0
        self.selected_item = None
        self.quantity = 1
        self.mode = "buy"
        self.player = player
        
    def draw_shop_interface(self, shop, player):
        location_images = {
            "Alchemist": "assets/area_images/alchemist.jpg",
            "Blacksmith": "assets/area_images/blacksmith.jpg",
            "Inn": "assets/area_images/inn.jpg",
        }
        
        self.player = player
        self.display.screen.fill('black')
        
        if shop.__class__.__name__ in location_images:
            location_image = pygame.image.load(location_images[shop.__class__.__name__])
            location_image = pygame.transform.scale(location_image, (self.display.config.SCREEN_WIDTH, self.display.config.SCREEN_HEIGHT))
            self.display.screen.blit(location_image, (0, 0))
        
        # Draw shop header
        self.display.draw_text(f"=== Welcome to the {shop.__class__.__name__} ===", 
                             (self.display.config.SCREEN_WIDTH // 2, 50), 
                             'title', 'gold', center=True)
        
        # Draw player gold
        self.display.draw_text(f"Gold: {player.gold}", 
                             (50, 100), 'large')
        
        # Mode and controls help
        self.display.draw_text(f"Mode: {self.mode.capitalize()}",
                             (self.display.config.SCREEN_WIDTH // 2, 100), 'large', center=True)
        self.display.draw_text("TAB: Switch Buy/Sell | UP/DOWN: Select item | </>: Quantity | ENTER: Buy/Sell | ESC: Exit", 
                             (self.display.config.SCREEN_WIDTH // 2, self.display.config.SCREEN_HEIGHT - 30), 
                             'medium', center=True)
        
        # Draw items
        items = list(shop.inventory.items()) if self.mode == "buy" else shop.get_sellable_items(player)
        self.draw_item_list(items, shop_x=50, shop_y=150)
        
        # Draw quantity selector if item selected
        if self.selected_item:
            self.draw_quantity_selector(self.display.config.SCREEN_WIDTH - 300, 150)
        
        pygame.display.flip()

    def handle_shop_events(self, shop, player):
        items = list(shop.inventory.items()) if self.mode == "buy" else shop.get_sellable_items(player)
        max_scroll = max(0, len(items) - self.config.ITEMS_PER_PAGE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return "exit"
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not items:
                        continue
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                    if self.selected_item:
                        current_idx = next((i for i, item in enumerate(items) 
                                    if (item[1]['item'] if self.mode == "buy" else item) == self.selected_item), 0)
                        new_idx = (current_idx - 1) % len(items)
                        if new_idx < self.scroll_offset:
                            self.scroll_offset = new_idx
                        elif new_idx >= self.scroll_offset + self.config.ITEMS_PER_PAGE:
                            self.scroll_offset = max(0, new_idx - self.config.ITEMS_PER_PAGE + 1)
                    else:
                        new_idx = 0
                    self.selected_item = items[new_idx][1]['item'] if self.mode == "buy" else items[new_idx]
                    self.quantity = 1
                    
                elif event.key == pygame.K_DOWN:
                    if not items:
                        continue
                    self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                    if self.selected_item:
                        current_idx = next((i for i, item in enumerate(items) 
                                    if (item[1]['item'] if self.mode == "buy" else item) == self.selected_item), 0)
                        new_idx = (current_idx + 1) % len(items)
                        if new_idx >= self.scroll_offset + self.config.ITEMS_PER_PAGE:
                            self.scroll_offset = min(max_scroll, new_idx - self.config.ITEMS_PER_PAGE + 1)
                        elif new_idx < self.scroll_offset:
                            self.scroll_offset = new_idx
                    else:
                        new_idx = 0
                    self.selected_item = items[new_idx][1]['item'] if self.mode == "buy" else items[new_idx]
                    self.quantity = 1

                elif event.key == pygame.K_LEFT:
                    if self.selected_item:
                        self.quantity = max(1, self.quantity - 1)
                        
                elif event.key == pygame.K_RIGHT:
                    if self.selected_item:
                        if self.mode == "sell":
                            matching_items = [i for i in player.inventory 
                                        if i.name == self.selected_item.name and i.type == self.selected_item.type]
                            max_available = sum(i.stack_size if hasattr(i, 'stack_size') else 1 for i in matching_items)
                            self.quantity = min(self.quantity + 1, max_available)
                        else:
                            inventory_item = self.selected_item
                            available = shop.inventory[inventory_item.name]['quantity']
                            self.quantity = min(self.quantity + 1, available)
                        
                elif event.key == pygame.K_TAB:
                    self.mode = "sell" if self.mode == "buy" else "buy"
                    self.selected_item = None
                    self.quantity = 1
                    
                elif event.key == pygame.K_RETURN:
                    if self.selected_item:
                        if self.mode == "buy":
                            self.execute_purchase(shop, player)
                        else:
                            matching_items = [i for i in player.inventory 
                                        if i.name == self.selected_item.name and i.type == self.selected_item.type]
                            available_quantity = sum(i.stack_size if hasattr(i, 'stack_size') else 1 for i in matching_items)
                            
                            if self.quantity <= available_quantity:
                                self.execute_sale(shop, player)
                            else:
                                self.quantity = available_quantity  # Reset to max available
                
                elif event.key == pygame.K_SPACE:
                    self.selected_item = None
                    self.quantity = 1
        
        return None

    def draw_item_list(self, items, shop_x, shop_y):
        visible_items = items[self.scroll_offset:self.scroll_offset + self.config.ITEMS_PER_PAGE]
        
        for i, item_info in enumerate(visible_items):
            if self.mode == "buy":
                item_name, info = item_info
                item = info['item']
                quantity = info['quantity']
            else:
                item = item_info
                if item.type == "soul_crystal":
                    quantity = 1
                else:
                    matching_items = [
                        i for i in self.player.inventory 
                        if i.name == item.name and i.type == item.type
                    ]
                    quantity = sum(i.stack_size if hasattr(i, 'stack_size') else 1 for i in matching_items)
            
            item_y = shop_y + (i * self.config.ITEM_HEIGHT)
            highlighted = self.selected_item == item
            
            if highlighted:
                pygame.draw.rect(self.display.screen, 'gray40', 
                               (shop_x - 5, item_y, 
                                self.config.SHOP_PANEL_WIDTH - 10, 
                                self.config.ITEM_HEIGHT))
            
            quantity_str = f" x{quantity}"
            price = item.value if self.mode == "buy" else item.value // 2
            self.display.draw_text(f"{item.name}{quantity_str}", 
                                 (shop_x + 10, item_y + 10), 'medium')
            item_width = FontManager.get_font('medium').size(item.name)[0]
            self.display.draw_text(f"Price: {price} gold", 
                                 (shop_x + 10, item_y + 35), 'small')
            
            if highlighted:
                stats_x = shop_x - 300 + item_width
                self.draw_item_stats(stats_x + self.config.DESCRIPTION_WIDTH, 
                                   item_y + 10, item)

    def draw_item_stats(self, x, y, item):
        # Collect all item stats
        stats = []
        
        # Basic info
        basic_info = [f"Type: {item.type.capitalize()}", f"Tier: {item.tier.capitalize()}"]
        if item.type == "weapon" and hasattr(item, 'weapon_type'):
            basic_info.extend([
                f"Weapon: {item.weapon_type.capitalize()}", 
                f"Stamina: {self.player.get_weapon_stamina_cost(item.weapon_type)}"
            ])
        stats.append(" | ".join(basic_info))
        
        # Combat stats
        combat_stats = []
        if item.attack > 0:
            combat_stats.append(f"Attack: +{item.attack}")
        if item.defence > 0:
            combat_stats.append(f"Defence: +{item.defence}")
        if item.accuracy > 0:
            combat_stats.append(f"Accuracy: +{item.accuracy}")
        if getattr(item, 'damage_reduction', 0) > 0:
            combat_stats.append(f"DR: +{item.damage_reduction}")
        if getattr(item, 'evasion', 0) > 0:
            combat_stats.append(f"Eva: +{item.evasion}")
        if getattr(item, 'crit_chance', 0) > 0:
            combat_stats.append(f"Crit: +{item.crit_chance}%")
        if getattr(item, 'crit_damage', 0) > 0:
            combat_stats.append(f"CDmg: +{item.crit_damage}%")
        if getattr(item, 'block_chance', 0) > 0:
            combat_stats.append(f"Block: +{item.block_chance}%")
        if getattr(item, 'armour_penetration', 0) > 0:
            combat_stats.append(f"AP: +{item.armour_penetration}")
        
        if combat_stats:
            stats.append(" | ".join(combat_stats))
            
        if item.type in ["consumable", "food", "drink"]:
            effect_stats = self.get_consumable_stats(item)
            if effect_stats:
                stats.extend(effect_stats)

        # Draw stats with wrapping
        line_height = 20
        max_width = self.config.DESCRIPTION_WIDTH - 20
        current_y = y
        
        for stat_line in stats:
            words = stat_line.split(" | ")
            current_line = []
            current_width = 0
            
            for word in words:
                text_width = FontManager.get_font('small').size((" | " if current_line else "") + word)[0]
                if current_width + text_width > max_width and current_line:
                    final_text = " | ".join(current_line)
                    self.display.draw_text(final_text, (x, current_y), 'small')
                    current_y += line_height
                    current_line = [word]
                    current_width = FontManager.get_font('small').size(word)[0]
                else:
                    current_line.append(word)
                    current_width += text_width
            
            if current_line:
                final_text = " | ".join(current_line)
                self.display.draw_text(final_text, (x, current_y), 'small')
                current_y += line_height

    def get_consumable_stats(self, item):
        stats = []
        if item.effect_type == "buff":
            if isinstance(item.effect, list):
                buff_effects = []
                for stat, value in item.effect:
                    stat_name = stat.replace('_', ' ').title()
                    buff_effects.append(f"{stat_name} +{value}")
                stats.append(" | ".join(buff_effects))
                if item.duration:
                    stats.append(f"Duration: {item.duration} turns")
            else:
                stat, value = item.effect if isinstance(item.effect, tuple) else ("Attack", item.effect)
                stats.append(f"{stat.replace('_', ' ').title()}: +{value}")
                if item.duration:
                    stats.append(f"Duration: {item.duration} turns")
        elif item.effect_type == "healing":
            stats.append(f"Healing: {item.effect} HP")
        elif item.effect_type == "hot":
            stats.append(f"Heal {item.tick_effect}/turn for {item.duration} turns")
        elif item.effect_type == "stamina":
            stats.append(f"Restore: {item.stamina_restore} stamina")
        return stats

    def draw_quantity_selector(self, x, y):
        pygame.draw.rect(self.display.screen, 'gray20', 
                        (x, y, 200, 100))
        
        self.display.draw_text("-", (x + 25, y + 50), 'title', center=True)
        self.display.draw_text(str(self.quantity), 
                             (x + 100, y + 50), 'title', center=True)
        self.display.draw_text("+", (x + 175, y + 50), 'title', center=True)
        
    def execute_purchase(self, shop, player):
        if not self.selected_item:
            return
            
        total_cost = self.selected_item.value * self.quantity
        if player.gold >= total_cost:
            if shop.inventory[self.selected_item.name]['quantity'] >= self.quantity:
                player.gold -= total_cost
                new_item = type(self.selected_item)(
                    self.selected_item.name, self.selected_item.type, self.selected_item.value, self.selected_item.tier,
                    attack=self.selected_item.attack,
                    defence=self.selected_item.defence,
                    accuracy=self.selected_item.accuracy,
                    crit_chance=getattr(self.selected_item, 'crit_chance', 0),
                    crit_damage=getattr(self.selected_item, 'crit_damage', 0),
                    armour_penetration=getattr(self.selected_item, 'armour_penetration', 0),
                    damage_reduction=getattr(self.selected_item, 'damage_reduction', 0),
                    evasion=getattr(self.selected_item, 'evasion', 0),
                    block_chance=getattr(self.selected_item, 'block_chance', 0),
                    effect_type=self.selected_item.effect_type,
                    effect=self.selected_item.effect,
                    cooldown=self.selected_item.cooldown,
                    duration=self.selected_item.duration,
                    tick_effect=self.selected_item.tick_effect,
                    weapon_type=self.selected_item.weapon_type,
                    stamina_restore=self.selected_item.stamina_restore
                )
                
                if new_item.is_stackable():
                    new_item.stack_size = self.quantity
                    player.add_item(new_item)
                else:
                    for _ in range(self.quantity):
                        player.add_item(new_item)
                        
                shop.remove_item(self.selected_item.name, self.quantity)
                self.selected_item = None
                self.quantity = 1

    def execute_sale(self, shop, player):
        if not self.selected_item:
            return
            
        sell_value = (self.selected_item.value // 2) * self.quantity
        player.gold += sell_value
        
        if hasattr(self.selected_item, 'stack_size'):
            remaining = self.quantity
            inventory_items = [i for i in player.inventory if i.name == self.selected_item.name]
            for item in inventory_items:
                if remaining <= 0:
                    break
                if item.stack_size <= remaining:
                    player.inventory.remove(item)
                    remaining -= item.stack_size
                else:
                    item.stack_size -= remaining
                    remaining = 0
        else:
            player.inventory.remove(self.selected_item)
            
        shop.add_item(self.selected_item, self.quantity)
        self.selected_item = None
        self.quantity = 1
        
class VisualInput:
    def __init__(self, display, width=400, height=50):
        self.display = display
        self.width = width
        self.height = height
        self.text = ""
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 20

    def draw(self, x, y):
        # Draw input box
        pygame.draw.rect(self.display.screen, 'gray20', 
                        (x, y, self.width, self.height))
        pygame.draw.rect(self.display.screen, 'white' if self.active else 'gray', 
                        (x, y, self.width, self.height), 2)
        
        # Update cursor blink
        self.cursor_timer = (self.cursor_timer + 1) % 60
        self.cursor_visible = self.cursor_timer < 30
        
        # Draw text with cursor
        display_text = self.text + ('|' if self.cursor_visible and self.active else '')
        text_surface = FontManager.get_font('large').render(display_text, True, 'white')
        text_rect = text_surface.get_rect(center=(x + self.width // 2, y + self.height // 2))
        self.display.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = True
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode
            elif event.key == pygame.K_RETURN and self.text.strip():
                return True
        return False
    
class MapDisplay:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.display = Display()
        
        layout = self.display.calculate_layout()
        self.map_area = layout['main_panel']
        self.width = self.display.config.SCREEN_WIDTH
        self.height = self.display.config.SCREEN_HEIGHT
        self.x_offset = 0
        self.y_offset = 0
        
        # Try to load and scale background image
        try:
            self.background = pygame.image.load('assets/world_map/world_map.jpeg').convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except:
            self.background = None
            print("Could not load map background image")
        
        row_spacing = self.height // 5
        col_spacing = self.width // 5
        
        self.locations = {
            'Heavens':          (self.x_offset + col_spacing * 2.5, self.y_offset + row_spacing * 0.5),
            'Ancient Ruins':    (self.x_offset + col_spacing * 0.5, self.y_offset + row_spacing * 1.5),
            'Death Valley':     (self.x_offset + col_spacing * 1.5, self.y_offset + row_spacing * 1.5),
            'Volcanic Valley':  (self.x_offset + col_spacing * 2.5, self.y_offset + row_spacing * 1.5),
            'Dragons Lair':     (self.x_offset + col_spacing * 3.5, self.y_offset + row_spacing * 1.5),
            'Death Caves':      (self.x_offset + col_spacing * 4.5, self.y_offset + row_spacing * 1.5),
            'Ruins':           (self.x_offset + col_spacing * 0.5, self.y_offset + row_spacing * 2.5),
            'Scorching Plains':(self.x_offset + col_spacing * 1.5, self.y_offset + row_spacing * 2.5),
            'Shadowed Valley': (self.x_offset + col_spacing * 2.5, self.y_offset + row_spacing * 2.5),
            'Mountain Peaks':  (self.x_offset + col_spacing * 3.5, self.y_offset + row_spacing * 2.5),
            'Toxic Swamp':     (self.x_offset + col_spacing * 4.5, self.y_offset + row_spacing * 2.5),
            'Temple':          (self.x_offset + col_spacing * 0.5, self.y_offset + row_spacing * 3.5),
            'Desert':          (self.x_offset + col_spacing * 1.5, self.y_offset + row_spacing * 3.5),
            'Valley':          (self.x_offset + col_spacing * 2.5, self.y_offset + row_spacing * 3.5),
            'Mountain':        (self.x_offset + col_spacing * 3.5, self.y_offset + row_spacing * 3.5),
            'Swamp':           (self.x_offset + col_spacing * 4.5, self.y_offset + row_spacing * 3.5),
            'Cave':            (self.x_offset + col_spacing * 0.5, self.y_offset + row_spacing * 4.5),
            'Plains':          (self.x_offset + col_spacing * 1.5, self.y_offset + row_spacing * 4.5),
            'Village':         (self.x_offset + col_spacing * 2.5, self.y_offset + row_spacing * 4.5),
            'Forest':          (self.x_offset + col_spacing * 3.5, self.y_offset + row_spacing * 4.5),
            'Deepwoods':       (self.x_offset + col_spacing * 4.5, self.y_offset + row_spacing * 4.5)
        }
    
    def draw_map(self, current_location, visited_locations, player_level, level_reqs):
        # Draw background image or fallback to solid colour
        if self.background:
            self.screen.blit(self.background, (self.x_offset, self.y_offset))
        else:
            pygame.draw.rect(self.screen, 'gray20', (self.x_offset, self.y_offset, self.width, self.height))
        self._draw_connections()
        
        for loc_name, pos in self.locations.items():
            colour = self._get_location_colour(loc_name, current_location, visited_locations, player_level, level_reqs)
            self._draw_location(loc_name, pos, colour)
            
        self._draw_legend()
    
    def _draw_connections(self):
        connections = {
            'Village': ['Forest', 'Plains'],
            'Deepwoods': ['Forest', 'Swamp'],
            'Cave': ['Plains', 'Temple'],
            'Forest': ['Village', 'Deepwoods', 'Mountain'],
            'Plains': ['Village', 'Cave', 'Desert'],
            'Swamp': ['Deepwoods', 'Toxic Swamp'],
            'Temple': ['Cave', 'Ruins'],
            'Mountain': ['Forest', 'Valley', 'Mountain Peaks'],
            'Desert': ['Plains', 'Scorching Plains', 'Valley'],
            'Valley': ['Mountain', 'Shadowed Valley', 'Desert'],
            'Toxic Swamp': ['Swamp', 'Death Caves'],
            'Ruins': ['Temple', 'Ancient Ruins'],
            'Mountain Peaks': ['Mountain', 'Dragons Lair'],
            'Scorching Plains': ['Desert', 'Death Valley'],
            'Shadowed Valley': ['Valley', 'Volcanic Valley'],
            'Death Caves': ['Toxic Swamp', 'Dragons Lair'],
            'Ancient Ruins': ['Ruins', 'Death Valley'],
            'Death Valley': ['Scorching Plains', 'Volcanic Valley', 'Ancient Ruins'],
            'Dragons Lair': ['Mountain Peaks', 'Death Caves', 'Volcanic Valley'],
            'Volcanic Valley': ['Shadowed Valley', 'Death Valley', 'Dragons Lair', 'Heavens'],
            'Heavens': ['Volcanic Valley']
        }
        
        for loc, connected in connections.items():
            start = self.locations[loc]
            for target in connected:
                if target in self.locations:
                    end = self.locations[target]
                    pygame.draw.line(self.screen, 'gray', start, end, 2)

    def _get_location_colour(self, location, current, visited, level, reqs):
        if location == current:
            return 'blue'
        elif level < reqs[location]:
            return 'red'
        elif location in visited:
            return 'darkgreen'
        return 'gray50'

    def _draw_location(self, name, pos, colour):
        rect_width = 120
        rect_height = 30
        x = pos[0] - rect_width//2
        y = pos[1] - rect_height//2
        
        pygame.draw.rect(self.screen, colour, (x, y, rect_width, rect_height))
        pygame.draw.rect(self.screen, 'white', (x, y, rect_width, rect_height), 1)
        
        font = pygame.font.SysFont("Arial", 12)
        text = font.render(name, True, 'black')
        text_rect = text.get_rect(center=(pos[0], pos[1]))
        self.screen.blit(text, text_rect)

    def _draw_legend(self):
        legend_items = [
            ('Current Location', 'blue'),
            ('Visited Location', 'green'),
            ('Locked Location', 'red')
        ]
        
        y = self.y_offset + self.display.config.PADDING * 2
        for text, colour in legend_items:
            pygame.draw.rect(self.screen, colour, (self.x_offset + 80, y, 15, 15))
            font = pygame.font.SysFont("Arial", 14)
            text_surface = font.render(text, True, 'white')
            self.screen.blit(text_surface, (self.x_offset + 100, y))
            y += 25
            
        self.display.draw_text("Press ENTER to exit map!",
                               (self.x_offset + 80, y),
                               'small', 'white')
            
class ItemUseDisplay:
    def __init__(self, display):
        self.display = display
        self.config = display.config
        self.layout = self.display.calculate_layout()
        
    def show_item_use(self, item, effect_details):
        """Displays the effect of an item use."""
        battle_log = self.layout['battle_log_panel']
        width = battle_log[0]
        height = battle_log[1]
        x = battle_log[2]
        y = battle_log[3]
        
        # Clear the battle log panel
        self.display.draw_panel(width, height, x, y)
        
        # Draw the item use header
        self.display.draw_text(f"Using {item.name}...",
                               (x + width // 2, y + 30),
                               'large', 'white', center=True)
        
        # Show effect based on type
        if item.effect_type == "healing":
            self._show_healing_effect(effect_details, x + width // 2, y + 80)
        elif item.effect_type == "teleport":
            self.display.draw_text("Select destination...",
                                   (x + width // 2, y + 80),
                                   'large', 'white', center=True)
            pygame.display.flip()
            pygame.time.wait(1000)
            return self.player.show_teleport_menu()
        elif item.effect_type == "buff":
            self._show_buff_effect(effect_details, x + width // 2, y + 80)
        elif item.effect_type == "weapon_buff":
            self._show_weapon_buff_effect(effect_details, x + width // 2, y + 80)
        elif item.effect_type == "stamina":
            self._show_stamina_effect(effect_details, x + width // 2, y + 80)
        elif item.effect_type == "hot":
            self._show_hot_effect(effect_details, x + width // 2, y + 80)
            
        pygame.display.flip()
        pygame.time.wait(1000)
        
    def _show_healing_effect(self, heal_amount, x, y):
        self.display.draw_text(f"Restored {heal_amount} HP",
                               (x, y), 'large', 'green', center=True)

    def _show_buff_effect(self, buff_info, x, y):
        if isinstance(buff_info, list):
            for i, (stat, value) in enumerate(buff_info):
                self.display.draw_text(f"{stat.replace('_', ' ').title()} +{value}",
                                       (x, y + i * 40), 'large', 'yellow', center=True)
        else:
            stat, value = buff_info
            self.display.draw_text(f"{stat.replace('_', ' ').title()} +{value}",
                                   (x, y), 'large', 'yellow', center=True)
            
    def _show_weapon_buff_effect(self, buff_info, x, y):
        value, duration = buff_info
        self.display.draw_text(f"Weapon Attack +{value} for {duration} turns",
                               (x, y), 'large', 'blue', center=True)
        
    def _show_stamina_effect(self, stamina_amount, x, y):
        self.display.draw_text(f"Restored {stamina_amount} Stamina",
                               (x, y), 'large', 'cyan', center=True)
        
    def _show_hot_effect(self, hot_info, x, y):
        tick_heal, duration = hot_info
        self.display.draw_text(f"Healing {tick_heal} HP per turn",
                               (x, y), 'large', 'green', center=True)
        self.display.draw_text(f"Duration: {duration} turns",
                               (x, y + 40), 'medium', 'green', center=True)
        
class EquipmentMenu:
    def __init__(self, display, player):
        self.display = display
        self.player = player
        self.config = display.config
        self.selected_slot = None
        self.selected_item = None
        self.scroll_offset = 0
        self.items_per_page_equip = 8
        self.items_per_page_inventory = 10
        
    def show_equipment_menu(self):
        """Main Equipment Menu Loop"""
        layout = self.display.calculate_layout()

        while True:
            self.display.screen.fill('black')
            
            # Draw header
            self.display.draw_text("=== EQUIPMENT MENU ===",
                                   (self.config.SCREEN_WIDTH // 2, 50),
                                   'title', 'gold', center=True)
            
            # Draw equipment slots panel (left side)
            self.draw_equipment_panel(*layout['equipped_equipment_panel'])
            
            # Draw inventory panel (right)
            self.draw_inventory_panel(*layout['equipment_inventory_panel'])
            
            # Draw comparison panel if item selected (middle)
            if self.selected_item:
                self.draw_comparison_panel(*layout['equipment_comparison_panel'])
                
            # Draw Instructions
            self.display.draw_text("UP/DOWN: Navigate | ENTER: Equip/Unequip | ESC: Exit",
                                   (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 50),
                                   'medium', center=True)
            
            pygame.display.flip()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    return
                
                if event.type == pygame.KEYDOWN:
                    self.handle_input(event.key)
            
            self.display.clock.tick(self.config.FPS)
            
    def draw_equipment_panel(self, width, height, x, y):
        """Draw currently equipped items"""
        # Draw Panel Background
        self.display.draw_panel(width, height, x, y)
        
        # Draw title
        self.display.draw_text("Currently Equipped",
                               (x + width // 2, y +30),
                               'large', center=True)
        
        # Draw equipment slots
        current_y = y + 70
        for slot, item in self.player.equipped.items():
            slot_colour = 'gray40' if slot == self.selected_slot else 'gray20'
            pygame.draw.rect(self.display.screen, slot_colour,
                             (x + 10, current_y, width - 20, 50))
            
            # Draw slot name
            self.display.draw_text(f"{slot.capitalize()}: ",
                                   (x + 20, current_y + 15),
                                   'medium')
            
            # Draw item info if equipped
            if item:
                self.display.draw_text(item.name,
                                       (x + 120, current_y + 15),
                                       'medium')
                # Draw item stats
                stats = self.get_stats_string(item)
                self.display.draw_text(stats,
                                       (x + 20, current_y + 35),
                                       'small')
                
                current_y += 60
    
    def draw_inventory_panel(self, width, height, x, y):
        """Draw available equipment in inventory"""
        # Draw panel background
        self.display.draw_panel(width, height, x, y)
        
        # Draw title
        self.display.draw_text("Inventory", 
                            (x + width // 2, y + 30),
                            'large', center=True)
        
        # Get equippable items
        equippable_items = [item for item in self.player.inventory 
                          if item.type in self.player.equipped]
        
        # Draw visible items
        current_y = y + 70
        visible_items = equippable_items[self.scroll_offset:
                                       self.scroll_offset + self.items_per_page_inventory]
        
        for item in visible_items:
            item_colour = 'gray40' if item == self.selected_item else 'gray20'
            pygame.draw.rect(self.display.screen, item_colour,
                           (x + 10, current_y, width - 20, 50))
            
            # Draw item name and type
            self.display.draw_text(f"{item.name} ({item.type.capitalize()})",
                                (x + 20, current_y + 15),
                                'medium')
            
            # Draw basic stats
            stats = self.get_stats_string(item)
            self.display.draw_text(stats,
                                (x + 20, current_y + 35),
                                'small')
            
            current_y += 60
                
    def draw_comparison_panel(self, width, height, x, y):
        """Draw comparison between selected item and equipped item"""
        # Draw Panel Background
        self.display.draw_panel(width, height, x, y)
        
        # Draw title
        self.display.draw_text("Item Comparison",
                               (x + width // 2, y +30),
                               'large', center=True)
        
        # Draw item stats
        stats = self.get_stats_string(self.selected_item)
        self.display.draw_text(stats,
                               (x + 20, y + 70),
                               'small')
        
        current_y = y + 70
        equipped_item = self.player.equipped[self.selected_item.type]
        
        # Compare stats
        stats = ["attack", "defence", "accuracy", "evasion", "crit_chance", "crit_damage",
                 "armour_penetration", "damage_reduction", "block_chance"]
        
        for stat in stats:
            new_val = getattr(self.selected_item, stat, 0)
            old_val = getattr(equipped_item, stat, 0) if equipped_item else 0
            
            if new_val > 0 or old_val > 0:
                diff = new_val - old_val
                colour = 'green' if diff > 0 else 'red' if diff < 0 else 'white'
                
                stat_name = stat.replace('_', ' ').title()
                stat_text = f"{stat_name}: {old_val} -> {new_val}"
                if diff != 0:
                    stat_text += f" ({'+' if diff > 0 else ''}{diff})"
                
                current_y += 30
                   
                self.display.draw_text(stat_text,
                                       (x + 20, current_y),
                                       'medium', colour=colour)
                
        # Show weapon type and stamina cost for weapons
        if self.selected_item.type == "weapon":
            current_y += 30
            new_type = self.selected_item.weapon_type
            old_type = equipped_item.weapon_type if equipped_item else "none"
            
            new_cost = self.player.get_weapon_stamina_cost(new_type)
            old_cost = self.player.get_weapon_stamina_cost(old_type) if equipped_item else 0
            
            self.display.draw_text(f"Weapon Type: {old_type.title()} -> {new_type.title()}",
                                   (x + 20, current_y),
                                   'medium')
            
            current_y += 30
            
            cost_diff = new_cost - old_cost
            colour = 'red' if cost_diff > 0 else 'green' if cost_diff < 0 else 'white'
            cost_text = f"Stamina Cost: {old_cost} -> {new_cost}"
            if cost_diff != 0:
                cost_text += f" ({'+' if cost_diff > 0 else ''}{cost_diff})"
                
            self.display.draw_text(cost_text,
                                   (x + 20, current_y),
                                   'medium', colour=colour)
            
    def get_stats_string(self, item):
        """Get string of item stats"""
        stats = []
        if item.attack > 0:
            stats.append(f"Att: {item.attack}")
        if item.defence > 0:
            stats.append(f"Def: {item.defence}")
        if item.accuracy > 0:
            stats.append(f"Acc: {item.accuracy}")
        if hasattr(item, 'evasion') and item.evasion > 0:
            stats.append(f"Eva: {item.evasion}")
        if hasattr(item, 'crit_chance') and item.crit_chance > 0:
            stats.append(f"Crit: {item.crit_chance}%")
        if hasattr(item, 'crit_damage') and item.crit_damage > 0:
            stats.append(f"CDmg: {item.crit_damage}%")
        if hasattr(item, 'armour_penetration') and item.armour_penetration > 0:
            stats.append(f"AP: {item.armour_penetration}")
        if hasattr(item, 'damage_reduction') and item.damage_reduction > 0:
            stats.append(f"DR: {item.damage_reduction}")
        if hasattr(item, 'block_chance') and item.block_chance > 0:
            stats.append(f"Block: {item.block_chance}%")
        if item.type == "weapon":
            stats.append(f"Type: {item.weapon_type.title()}")
            stats.append(f"Stam: {self.player.get_weapon_stamina_cost(item.weapon_type)}")
        return " | ".join(stats)
    
    def handle_input(self, key):
        if key == pygame.K_UP:
            if self.selected_item:
                equippable_items = [item for item in self.player.inventory 
                                if item.type in self.player.equipped]
                current_idx = equippable_items.index(self.selected_item)
                # Wrap to bottom if at top
                if current_idx == 0:
                    self.selected_item = equippable_items[-1]
                    self.scroll_offset = max(0, len(equippable_items) - self.items_per_page_inventory)
                else:
                    self.selected_item = equippable_items[current_idx - 1]
                    if current_idx - 1 < self.scroll_offset:
                        self.scroll_offset = max(0, self.scroll_offset - 1)
            elif self.selected_slot:
                slots = list(self.player.equipped.keys())
                current_idx = slots.index(self.selected_slot)
                # Wrap to bottom if at top
                self.selected_slot = slots[-1] if current_idx == 0 else slots[current_idx - 1]
            else:
                self.selected_slot = list(self.player.equipped.keys())[0]
                
        elif key == pygame.K_DOWN:
            if self.selected_item:
                equippable_items = [item for item in self.player.inventory 
                                if item.type in self.player.equipped]
                current_idx = equippable_items.index(self.selected_item)
                # Wrap to top if at bottom
                if current_idx == len(equippable_items) - 1:
                    self.selected_item = equippable_items[0]
                    self.scroll_offset = 0
                else:
                    self.selected_item = equippable_items[current_idx + 1]
                    if current_idx + 1 >= self.scroll_offset + self.items_per_page_inventory:
                        self.scroll_offset += 1
            elif self.selected_slot:
                slots = list(self.player.equipped.keys())
                current_idx = slots.index(self.selected_slot)
                # Wrap to top if at bottom
                self.selected_slot = slots[0] if current_idx == len(slots) - 1 else slots[current_idx + 1]
            else:
                self.selected_slot = list(self.player.equipped.keys())[0]
                
        elif key == pygame.K_RETURN:
            if self.selected_item:
                self.player.equip_item(self.selected_item)
                self.selected_item = None
            elif self.selected_slot and self.player.equipped[self.selected_slot]:
                self.player.unequip_item(self.selected_slot)
                
        elif key == pygame.K_TAB:
            # Toggle between equipment and slots
            if self.selected_slot:
                equippable_items = [item for item in self.player.inventory
                                    if item.type in self.player.equipped]
                if equippable_items:
                    self.selected_item = equippable_items[0]
                    self.selected_slot = None
            else:
                self.selected_slot = list(self.player.equipped.keys())[0]
                self.selected_item = None
                
class InventoryDisplay:
    def __init__(self, display, player):
        self.display = display
        self.player = player
        self.config = display.config
        self.equipment_scroll = 0
        self.consumable_scroll = 0
        self.items_per_page = 16  # Items per page per category
        
    def show_inventory(self):
        """Main inventory display loop"""
        while True:
            self.display.screen.fill('black')
            
            # Draw header
            self.display.draw_text("=== INVENTORY ===",
                                 (self.config.SCREEN_WIDTH // 2, 50),
                                 'title', 'gold', center=True)
            
            # Draw player gold
            self.display.draw_text(f"Gold: {self.player.gold}",
                                 (50, 100), 'large')
            
            # Draw categories
            self.draw_equipment_section()
            self.draw_consumable_section()
            
            # Draw instructions
            self.display.draw_text("UP/DOWN: Scroll Equipment | W/S: Scroll Consumables | ESC: Exit",
                                 (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 80),
                                 'medium', center=True)
            
            pygame.display.flip()
            
            # Handle events
            if self.handle_events() == "exit":
                return
            
            self.display.clock.tick(self.display.config.FPS)
    
    def draw_equipment_section(self):
        """Draw equipment items (weapons and armour)"""
        # Draw section header
        self.display.draw_text("Equipment",
                             (50, 150), 'large')
        
        # Get equipment items
        equipment = [item for item in self.player.inventory 
                    if item.type in ["weapon", "helm", "chest", "belt", "legs", 
                                   "boots", "gloves", "shield", "back", "ring"]]
        
        # Draw visible items
        visible_items = equipment[self.equipment_scroll:self.equipment_scroll + self.items_per_page]
        for i, item in enumerate(visible_items):
            y_pos = 190 + (i * 35)
            
            # Draw background
            pygame.draw.rect(self.display.screen, 'gray20',
                           (40, y_pos - 5, self.config.SCREEN_WIDTH // 2 - 60, 30))
            
            # Draw item name and type
            name_width = self.display.calculate_text_dimensions(f"{item.name} [{item.type.title()}]", 'medium')[0]
            name_x = 50
            self.display.draw_text(f"{item.name} [{item.type.title()}]",
                                 (name_x, y_pos), 'medium')
            
            # Draw basic stats
            stats = []
            if item.attack > 0:
                stats.append(f"Atk: {item.attack}")
            if item.defence > 0:
                stats.append(f"Def: {item.defence}")
            if item.accuracy > 0:
                stats.append(f"Acc: {item.accuracy}")
            if hasattr(item, 'damage_reduction') and item.damage_reduction > 0:
                stats.append(f"DR: {item.damage_reduction}")
            if hasattr(item, 'evasion') and item.evasion > 0:
                stats.append(f"Eva: {item.evasion}")
            if hasattr(item, 'crit_chance') and item.crit_chance > 0:
                stats.append(f"Crit: {item.crit_chance}%")
            if hasattr(item, 'crit_damage') and item.crit_damage > 0:
                stats.append(f"Crit Dmg: {item.crit_damage}%")
            if hasattr(item, 'armour_penetration') and item.armour_penetration > 0:
                stats.append(f"AP: {item.armour_penetration}")
            if hasattr(item, 'block_chance') and item.block_chance > 0:
                stats.append(f"Block: {item.block_chance}%")
            
            if stats:
                self.display.draw_text(", ".join(stats),
                                     (name_x + name_width + 20, y_pos), 'small')
    
    def draw_consumable_section(self):
        section_x = self.display.config.SCREEN_WIDTH // 2 + 20
        self.display.draw_text("Consumables", (section_x, 150), 'large')
        
        consumables = {}
        for item in self.player.inventory:
            if item.type in ["consumable", "food", "drink", "weapon coating", "soul_crystal"]:
                if item.name in consumables:
                    if item.is_stackable():
                        consumables[item.name]["count"] += item.stack_size
                else:
                    consumables[item.name] = {
                        "item": item,
                        "count": item.stack_size if item.is_stackable() else 1
                    }
        
        consumable_list = list(consumables.values())
        visible_items = consumable_list[self.consumable_scroll:self.consumable_scroll + self.items_per_page]
        
        max_width = (self.display.config.SCREEN_WIDTH // 2) - 100
        line_height = 30
        current_y = 190
        item_spacing = 10
        
        for item_data in visible_items:
            item = item_data["item"]
            count = item_data["count"]
            
            name_text = f"{item.name} x{count}" if count > 1 else item.name
            full_name = f"{name_text} [{item.type.replace('_', ' ').title()}]"
            name_width = self.display.calculate_text_dimensions(full_name, 'medium')[0]
            
            if isinstance(item, SoulCrystal):
                effect_desc = item.get_effect_description()
            else:
                effect_desc = self.player.get_effect_description(item)
                
            # Calculate wrapped lines
            words = effect_desc.split() if effect_desc else []
            lines = []
            current_line = []
            current_width = 0
            
            for word in words:
                word_width = self.display.calculate_text_dimensions(word + ' ', 'small')[0]
                if current_width + word_width <= max_width - name_width - 20:
                    current_line.append(word)
                    current_width += word_width
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_width = word_width
            if current_line:
                lines.append(' '.join(current_line))
                
            # Calculate box height based on content
            box_height = max(line_height, (len(lines)) * line_height)
            
            # Draw background box
            pygame.draw.rect(self.display.screen, 'gray20',
                            (section_x - 10, current_y - 5,
                            self.display.config.SCREEN_WIDTH // 2 - 60, box_height))
            
            # Draw item name and effects
            self.display.draw_text(full_name, (section_x, current_y), 'medium')
            
            if lines:
                for i, line in enumerate(lines):
                    y_offset = current_y + (i * line_height)
                    self.display.draw_text(line, (section_x + name_width + 20, y_offset), 'small')
                current_y += (len(lines) - 1) * line_height
                
            current_y += line_height + item_spacing
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return "exit"
            
            if event.type == pygame.KEYDOWN:
                # Equipment scrolling
                if event.key == pygame.K_UP:
                    self.equipment_scroll = max(0, self.equipment_scroll - 1)
                elif event.key == pygame.K_DOWN:
                    equipment_count = len([item for item in self.player.inventory 
                                        if item.type in ["weapon", "helm", "chest", "belt", "legs", 
                                                       "boots", "gloves", "shield", "back", "ring"]])
                    max_scroll = max(0, equipment_count - self.items_per_page)
                    self.equipment_scroll = min(max_scroll, self.equipment_scroll + 1)
                
                # Consumable scrolling
                elif event.key == pygame.K_w:
                    self.consumable_scroll = max(0, self.consumable_scroll - 1)
                elif event.key == pygame.K_s:
                    consumable_count = len(set(item.name for item in self.player.inventory 
                                            if item.type in ["consumable", "food", "drink", 
                                                           "weapon coating", "soul_crystal"]))
                    max_scroll = max(0, consumable_count - self.items_per_page)
                    self.consumable_scroll = min(max_scroll, self.consumable_scroll + 1)
        
        return None
    
class KillLogDisplay:
    def __init__(self, display, player):
        self.display = display
        self.player = player
        self.config = display.config
        self.section_spacing = 40
        self.column_width = self.config.SCREEN_WIDTH // 3
        self.items_per_page = 15
        
        # Track scroll position for each column
        self.scroll_positions = {
            'standard': 0,
            'variant': 0,
            'boss': 0,
            'traded_standard': 0,
            'traded_variant': 0,
            'traded_boss': 0
        }
        self.selected_column = 'standard'  # Default selected column
        
    def show_kill_log(self):
        while True:
            self.display.screen.fill('black')
            
            # Draw header and soul calculations
            self.display.draw_text("=== KILL STATISTICS ===",
                                 (self.config.SCREEN_WIDTH // 2, 50),
                                 'title', 'gold', center=True)
            self.draw_soul_summary()
            
            # Calculate column positions
            col1_x = 50
            col2_x = self.config.SCREEN_WIDTH // 3
            col3_x = (self.config.SCREEN_WIDTH // 3) * 2
            current_y = 150
            
            # Get sorted kills
            standard_kills = sorted(self.player.kill_tracker.items(), key=lambda x: (-x[1], x[0])) if self.player.kill_tracker else []
            variant_kills = sorted(self.player.variant_kill_tracker.items(), key=lambda x: (-x[1], x[0])) if self.player.variant_kill_tracker else []
            boss_kills = sorted(self.player.boss_kill_tracker.items(), key=lambda x: (-x[1], x[0])) if self.player.boss_kill_tracker else []
            
            # Draw column headers with selection highlight
            headers = [
                ("Standard Monster Kills", col1_x, 'standard'),
                ("Variant Monster Kills", col2_x, 'variant'),
                ("Boss Monster Kills", col3_x, 'boss')
            ]
            
            for header, x, col_type in headers:
                colour = 'yellow' if self.selected_column == col_type else 'white'
                self.display.draw_text(header,
                                     (x + self.column_width // 2, current_y),
                                     'large', colour, center=True)
            
            current_y += 40
            
            # Draw kills with appropriate scroll positions
            visible_standard = standard_kills[self.scroll_positions['standard']:self.scroll_positions['standard'] + self.items_per_page]
            visible_variant = variant_kills[self.scroll_positions['variant']:self.scroll_positions['variant'] + self.items_per_page]
            visible_boss = boss_kills[self.scroll_positions['boss']:self.scroll_positions['boss'] + self.items_per_page]
            
            # Draw each column
            for i in range(self.items_per_page):
                entry_y = current_y + (i * 25)
                
                if i < len(visible_standard):
                    colour = 'yellow' if self.selected_column == 'standard' else 'white'
                    monster, count = visible_standard[i]
                    self.display.draw_text(f"{monster}: {count}",
                                         (col1_x + 20, entry_y), 'medium', colour)
                
                if i < len(visible_variant):
                    colour = 'yellow' if self.selected_column == 'variant' else 'white'
                    monster, count = visible_variant[i]
                    self.display.draw_text(f"{monster}: {count}",
                                         (col2_x + 20, entry_y), 'medium', colour)
                
                if i < len(visible_boss):
                    colour = 'yellow' if self.selected_column == 'boss' else 'white'
                    monster, count = visible_boss[i]
                    self.display.draw_text(f"{monster}: {count}",
                                         (col3_x + 20, entry_y), 'medium', colour)
            
            # Draw traded kills section similarly...
            if (hasattr(self.player, 'used_kill_tracker') and 
                (self.player.used_kill_tracker or 
                 self.player.used_variant_tracker or 
                 self.player.used_boss_kill_tracker)):
                traded_y = current_y + (self.items_per_page * 25) + self.section_spacing
                
                self.display.draw_text("=== TRADED KILLS ===",
                                     (self.config.SCREEN_WIDTH // 2, traded_y),
                                     'large', center=True)
                traded_y += 40
                
                traded_standard = sorted(self.player.used_kill_tracker.items(), key=lambda x: (-x[1], x[0])) if self.player.used_kill_tracker else []
                traded_variant = sorted(self.player.used_variant_tracker.items(), key=lambda x: (-x[1], x[0])) if self.player.used_variant_tracker else []
                traded_boss = sorted(self.player.used_boss_kill_tracker.items(), key=lambda x: (-x[1], x[0])) if self.player.used_boss_kill_tracker else []
                
                # Draw traded headers with selection highlight
                traded_headers = [
                    ("Traded Standard Kills", col1_x, 'traded_standard'),
                    ("Traded Variant Kills", col2_x, 'traded_variant'),
                    ("Traded Boss Kills", col3_x, 'traded_boss')
                ]
                
                for header, x, col_type in traded_headers:
                    colour = 'yellow' if self.selected_column == col_type else 'white'
                    self.display.draw_text(header,
                                         (x + self.column_width // 2, traded_y),
                                         'large', colour, center=True)
                
                traded_y += 40
                
                visible_traded_standard = traded_standard[self.scroll_positions['traded_standard']:self.scroll_positions['traded_standard'] + self.items_per_page]
                visible_traded_variant = traded_variant[self.scroll_positions['traded_variant']:self.scroll_positions['traded_variant'] + self.items_per_page]
                visible_traded_boss = traded_boss[self.scroll_positions['traded_boss']:self.scroll_positions['traded_boss'] + self.items_per_page]
                
                for i in range(self.items_per_page):
                    entry_y = traded_y + (i * 25)
                    
                    if i < len(visible_traded_standard):
                        colour = 'yellow' if self.selected_column == 'traded_standard' else 'white'
                        monster, count = visible_traded_standard[i]
                        self.display.draw_text(f"{monster}: {count}",
                                             (col1_x + 20, entry_y), 'medium', colour)
                    
                    if i < len(visible_traded_variant):
                        colour = 'yellow' if self.selected_column == 'traded_variant' else 'white'
                        monster, count = visible_traded_variant[i]
                        self.display.draw_text(f"{monster}: {count}",
                                             (col2_x + 20, entry_y), 'medium', colour)
                    
                    if i < len(visible_traded_boss):
                        colour = 'yellow' if self.selected_column == 'traded_boss' else 'white'
                        monster, count = visible_traded_boss[i]
                        self.display.draw_text(f"{monster}: {count}",
                                             (col3_x + 20, entry_y), 'medium', colour)
            
            # Draw instructions
            self.display.draw_text("LEFT/RIGHT: Select Column | UP/DOWN: Scroll | ESC: Exit",
                                 (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 20),
                                 'medium', center=True)
            
            pygame.display.flip()
            
            if self.handle_events() == "exit":
                return
            
            self.display.clock.tick(self.display.config.FPS)
    
    def draw_soul_summary(self):
        """Draw soul calculations summary"""
        # Calculate souls
        current_standard = sum(self.player.kill_tracker.values())
        current_variant = sum(self.player.variant_kill_tracker.values()) if self.player.variant_kill_tracker else 0
        current_boss = sum(self.player.boss_kill_tracker.values()) if self.player.boss_kill_tracker else 0
        
        used_standard = sum(self.player.used_kill_tracker.values()) if hasattr(self.player, 'used_kill_tracker') else 0
        used_variant = sum(self.player.used_variant_tracker.values()) if hasattr(self.player, 'used_variant_tracker') else 0
        used_boss = sum(self.player.used_boss_kill_tracker.values()) if hasattr(self.player, 'used_boss_kill_tracker') else 0
        
        current_souls = (current_standard + (current_variant * 5) + (current_boss * 10))
        used_souls = (used_standard + (used_variant * 5) + (used_boss * 10))
        
        # Draw soul counts
        y = 100
        self.display.draw_text(f"Available Souls: {current_souls}",
                             (50, y), 'large')
        self.display.draw_text(f"Traded Souls: {used_souls}",
                             (350, y), 'large')
        self.display.draw_text(f"Total Souls Earned: {current_souls + used_souls}",
                             (650, y), 'large')
    
    def draw_kill_section(self, title, kill_dict, start_y):
        """Draw a section of kill statistics"""
        if not kill_dict:
            return start_y
            
        # Draw section title
        self.display.draw_text(title,
                             (50, start_y), 'large')
        start_y += 30
        
        # Sort kills by count (descending) then name
        sorted_kills = sorted(kill_dict.items(), key=lambda x: (-x[1], x[0]))
        
        # Draw kill entries
        for monster, count in sorted_kills:
            self.display.draw_text(f"{monster}: {count}",
                                 (70, start_y), 'medium')
            start_y += 25
            
        return start_y + self.section_spacing
    
    def handle_events(self):
        """Handle user input for column selection and scrolling"""
        # Get the kill list for the current column
        kill_lists = {
            'standard': self.player.kill_tracker,
            'variant': self.player.variant_kill_tracker,
            'boss': self.player.boss_kill_tracker,
            'traded_standard': self.player.used_kill_tracker if hasattr(self.player, 'used_kill_tracker') else {},
            'traded_variant': self.player.used_variant_tracker if hasattr(self.player, 'used_variant_tracker') else {},
            'traded_boss': self.player.used_boss_kill_tracker if hasattr(self.player, 'used_boss_kill_tracker') else {}
        }
        
        current_list = kill_lists[self.selected_column]
        max_scroll = max(0, len(current_list) - self.items_per_page)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return "exit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.scroll_positions[self.selected_column] = max(0, self.scroll_positions[self.selected_column] - 1)
                elif event.key == pygame.K_DOWN:
                    self.scroll_positions[self.selected_column] = min(max_scroll, self.scroll_positions[self.selected_column] + 1)
                elif event.key == pygame.K_LEFT:
                    # Cycle through columns left
                    columns = ['standard', 'variant', 'boss', 'traded_standard', 'traded_variant', 'traded_boss']
                    current_idx = columns.index(self.selected_column)
                    self.selected_column = columns[(current_idx - 1) % len(columns)]
                elif event.key == pygame.K_RIGHT:
                    # Cycle through columns right
                    columns = ['standard', 'variant', 'boss', 'traded_standard', 'traded_variant', 'traded_boss']
                    current_idx = columns.index(self.selected_column)
                    self.selected_column = columns[(current_idx + 1) % len(columns)]
        
        return None
    
class SaveMenuDisplay:
    def __init__(self, display, player):
        self.display = display
        self.config = display.config
        self.player = player
        self.visual_input = VisualInput(display)
    
    def show_save_menu(self):
        from save_system import get_save_files
        save_files = get_save_files()
        scroll_offset = 0
        saves_per_page = 8
        
        while True:
            self.display.screen.fill('black')
            
            result = self._draw_main_menu(save_files, scroll_offset, saves_per_page)
            
            if isinstance(result, int):
                scroll_offset = result
            elif result == "new":
                new_save = self._handle_new_save()
                if new_save:
                    return new_save
            elif result is None:
                return None
            elif isinstance(result, str):
                return result
                
            self.display.clock.tick(self.display.config.FPS)
    
    def _draw_main_menu(self, save_files, scroll_offset, saves_per_page):
        self.display.screen.fill('black')
        
        # Draw title
        self.display.draw_text("=== SAVE GAME ===",
                            (self.config.SCREEN_WIDTH // 2, 50),
                            'title', 'gold', center=True)
        
        # Draw existing saves
        current_y = 150
        visible_saves = save_files[scroll_offset:scroll_offset + saves_per_page]
        for i, save in enumerate(visible_saves):
            self.display.draw_text(f"Save {i + 1}: {save}",
                                (self.config.SCREEN_WIDTH // 2, current_y),
                                'large', center=True)
            current_y += 40
        
        # Draw new save option
        self.display.draw_text("Create New Save (Press ENTER)",
                            (self.config.SCREEN_WIDTH // 2, current_y + 20),
                            'large', center=True)
        
        # Draw instructions
        self.display.draw_text("UP/DOWN: Navigate | 1-8: Select Save | Enter: Create New Save | Esc: Cancel",
                            (self.config.SCREEN_WIDTH // 2, self.config.SCREEN_HEIGHT - 50),
                            'medium', center=True)
        
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_RETURN:
                    return "new"
                elif event.key == pygame.K_UP and scroll_offset > 0:
                    return scroll_offset - 1
                elif event.key == pygame.K_DOWN and scroll_offset < len(save_files) - saves_per_page:
                    return scroll_offset + 1
                elif event.key in range(pygame.K_1, pygame.K_9):
                    index = event.key - pygame.K_1
                    if index < len(visible_saves):
                        if self._confirm_overwrite(visible_saves[index]):
                            return visible_saves[index]
        return scroll_offset
    
    def _handle_new_save(self):
        self.visual_input.text = ""  # Reset input text
        while True:
            self.display.screen.fill('black')
            
            # Draw title and instructions
            self.display.draw_text("=== CREATE NEW SAVE ===",
                                 (self.config.SCREEN_WIDTH // 2, 50),
                                 'title', 'gold', center=True)
            self.display.draw_text("Enter Save Name (ESC to cancel):",
                                 (self.config.SCREEN_WIDTH // 2, 150),
                                 'large', center=True)
            
            # Draw input box
            input_x = (self.config.SCREEN_WIDTH - self.visual_input.width) // 2
            input_y = 250
            self.visual_input.draw(input_x, input_y)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
                
                if self.visual_input.handle_event(event):
                    if self.visual_input.text.strip():
                        return f"{self.visual_input.text}.json"
            
            self.display.clock.tick(self.display.config.FPS)
            
    def _confirm_overwrite(self, filename):
        """Confirm overwriting an existing save file"""
        while True:
            self.display.screen.fill('black')
            
            # Draw title
            self.display.draw_text("=== CONFIRM OVERWRITE ===",
                                   (self.config.SCREEN_WIDTH // 2, 50),
                                   'title', 'gold', center=True)
            
            # Draw instructions
            self.display.draw_text(f"Are you sure you want to overwrite this save file? ({filename})",
                                   (self.config.SCREEN_WIDTH // 2, 150),
                                   'large', 'white', center=True)
            
            self.display.draw_text("ENTER: Confirm | ESC: Cancel",
                                   (self.config.SCREEN_WIDTH // 2, 250),
                                   'large', 'white', center=True)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or(
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    return False
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return True
                
            self.display.clock.tick(self.display.config.FPS)
            
class BattleDisplay:
    def __init__(self, display):
        self.display = display
        self.screen = display.screen
        self.config = display.config
        self.layout = display.calculate_layout()
        self.last_enemy = None
    
    STATUS_ICONS = {
        "Burn": pygame.image.load("assets/status_icons/flame.png"),
        "Poison": pygame.image.load("assets/status_icons/poison.png"),
        "Freeze": pygame.image.load("assets/status_icons/freeze.png"),
        "Stun": pygame.image.load("assets/status_icons/stun.png"),
        "Confusion": pygame.image.load("assets/status_icons/confusion.png"),
        "Attack Weaken": pygame.image.load("assets/status_icons/attack_weaken.png"),
        "Defence Break": pygame.image.load("assets/status_icons/defence_break.png"),
        "Damage Reflect": pygame.image.load("assets/status_icons/damage_reflect.png"),
        "Defensive Stance": pygame.image.load("assets/status_icons/defensive_stance.png"),
        "Power Stance": pygame.image.load("assets/status_icons/power_stance.png"),
        "Accuracy Stance": pygame.image.load("assets/status_icons/accuracy_stance.png"),
        "Berserker Stance": pygame.image.load("assets/status_icons/berserker_stance.png"),
        "Evasion Stance": pygame.image.load("assets/status_icons/evasion_stance.png")
    }
        
    def draw_battle_screen(self, player, current_location=None, enemy=None, scroll_offset=0):
        """Draw the battle screen layout"""
        if enemy is not None:
            self.last_enemy = enemy
            
        enemy_to_draw = enemy or self.last_enemy
        
        self.screen.fill('black')
        
        # Get player location
        #current_location = self.game.current_location if hasattr(self, 'game') else None
        
        # Draw Player Panel (left side)
        self.display.draw_player_panel(player, *self.layout['player_panel'], current_location)
        
        #  Draw main combat area
        self.draw_combat_area(*self.layout['battle_panel'])
        
        # Draw Enemy Panel (right side)
        self.draw_enemy_panel(enemy_to_draw, *self.layout['enemy_panel'])
        
        # Draw status panels (bottom)
        self.display.draw_panels(player, enemy_to_draw, scroll_offset)
        
        # Player status bars
        self.draw_status_bars(*self.layout['player_status_bars_panel'], player, True)
        
        # Enemy status bars
        self.draw_status_bars(*self.layout['enemy_status_bars_panel'], enemy_to_draw, False)
        
        # Draw chance to hit
        self.draw_chance_to_hit(self.layout['player_status_bars_panel'][2], self.layout['player_status_bars_panel'][3], player, enemy_to_draw)
        
        pygame.display.flip()
        self.display.clock.tick(self.config.FPS)
        
    def draw_combat_area(self, width, height, x, y):
        """Draw the main combat area with enemy visualisation"""
        self.display.draw_panel(width, height, x, y)
        
        options_y = y + height - 20
        combat_options = ["[A]ttack", "[U]se Item", "[R]un"]
        
        for i, option in enumerate(combat_options):
            option_x = x + (width // 4) + (i * (width // 4))
            self.display.draw_text(option, (option_x, options_y), 'large', center=True)
            
    def draw_enemy_panel(self, enemy, width, height, x, y, during_animation=False):
        """Draw enemy stats panel"""
        if enemy:
            content = []
            # Add enemy level
            content.append(f"Lvl: {enemy.level}")
            # If its a variant add it here
            if hasattr(enemy, 'variant') and enemy.variant:
                content.append(f"Variant: {enemy.variant['name']}")
            # Add enemy name
            content.append(f"{enemy.template['name']}")
            # Add all remaining stats
            content.extend([
                f"HP: {enemy.hp}/{enemy.max_hp}",
                "",
                f"Att: {enemy.attack}",
                f"Acc: {enemy.accuracy}",
                f"Def: {enemy.defence}",
                f"Eva: {enemy.evasion}",
                f"Crit: {enemy.crit_chance}%",
                f"Crit Dmg: {enemy.crit_damage}%",
                f"AP: {enemy.armour_penetration}",
                f"DR: {enemy.damage_reduction}",
                f"BC: {enemy.block_chance}%"
            ])
            
            self.display.draw_panel(width, height, x, y, content, font_colour='red')
                
    def draw_battle_message(self, text):
        self.display.add_message(text)
        layout = self.display.calculate_layout()
        self.display.draw_battle_log_panel(*layout['battle_log_panel'])
        pygame.display.flip()
        
    def display_attack_animation(self, attacker_name, attack_name, is_player=True, duration=2000):
        """Display Visual attack animation"""
        self.wait_for_animation()
        
        # Draw attack announcement
        layout = self.layout['attack_animation_panel']
        width, height, x, y = layout
        
        # Store original surface
        original_surface = self.display.screen.copy()
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((width, height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)  # Partial transparency
        
        # Draw animation
        self.display.screen.blit(overlay, (x, y))
        self.display.draw_panel(width, height, x, y)
        
        # Draw background
        pygame.draw.rect(self.display.screen, 'blue', (x, y, width, height))
        pygame.draw.rect(self.display.screen, 'white', (x, y, width, height), 2)
        
        # Draw attack name centered, using enemy template name instead of full name if not player
        display_name = attacker_name if is_player else attacker_name.split()[-1]
        self.display.draw_text(f"{display_name} used {attack_name}",
                               (x + width // 2, y + height // 2),
                               'large', 'green' if is_player else 'red', center=True)
        
        pygame.display.flip()
        pygame.time.wait(duration)
        
        # Restore original screen
        self.display.screen.blit(original_surface, (0, 0))
        pygame.display.flip()
        
    def display_damage_numbers(self, target, damage, hit_type="normal", is_player=True, is_self_damage=False):
        """Display floating damage numbers"""
        layout = self.layout['battle_panel']
        width, height, x, y = layout
        
        # Store original surface
        original_surface = self.display.screen.copy()
        
        # Set x position based on attacker
        if is_self_damage:
            x_pos = x + (width * 0.1) if is_player else x + (width * 0.9)
        else:
            x_pos = x + (width * 0.9) if is_player else x + (width * 0.1)
        
        # Colour based on hit type
        colour = {
            "normal": 'white',
            "critical": 'red',
            "heal": 'green',
            "miss": 'gray',
            "blocked": 'yellow',
            "self_damage": 'crimson'
        }.get(hit_type, 'white')
        
        # Wait for health bar animation to complete if it's a fatal hit
        if target and target.hp <= 0:
            health_bar_id = f"HP_{self.layout['player_status_bars_panel'][2]}_{self.layout['player_status_bars_panel'][3]}" if is_player else f"HP_{self.layout['enemy_status_bars_panel'][2]}_{self.layout['enemy_status_bars_panel'][3]}"
            while not self.animation_complete.get(health_bar_id, True):
                self.draw_battle_screen(self.display.game.player, self.display.game.current_location, target)
                pygame.time.wait(16)  # Roughly 60 FPS
        
        # Animate number floating up
        for offset in range(0, 100, 2):
            # Restore original screen
            self.display.screen.blit(original_surface, (0, 0))
            
            # Draw damage number
            self.display.draw_text(f"-{damage}", (x_pos, y + height * 0.3 - offset), 'title', colour, center=True)
            pygame.display.flip()
            pygame.time.wait(10)
        
        # Restore original screen
        self.display.screen.blit(original_surface, (0, 0))
        pygame.display.flip()
        
    def display_status_effects(self, target, effect_name):
        """Display status effect application with flashing animatio"""
        self.wait_for_animation()
        
        layout = self.layout['battle_panel']
        width, height, x, y = layout
        
        # Effect colours
        effect_colours = {
            "Burn": (255, 165, 0),  # orange
            "Poison": (0, 255, 0),  # green 
            "Freeze": (0, 255, 255), # cyan
            "Stun": (255, 255, 0),  # yellow
            "Defence Break": (139, 0, 0),  # dark red
            "Attack Weaken": (128, 0, 128),  # purple
            "Confusion": (255, 192, 203),  # pink
            "Damage Reflect": (192, 192, 192),  # silver
            "Self Damage": (220, 20, 60), # crimson
            "Defensive Stance": (128, 128, 128),  # gray
            "Accuracy Stance": (0, 0, 255),  # blue
            "Power Stance": (255, 0, 0),  # red
            "Evasion Stance": (100, 128, 100), # shadow gray
            "Berserker Stance": (255, 0, 255) # magenta
        }
        
        colour = effect_colours.get(effect_name, (255, 255, 255))
        
        # Store original surface
        original_surface = self.display.screen.copy()
        
        # Create flash overlay
        flash_surface = pygame.Surface((width, height))
        flash_surface.fill(colour)
        
        # Flash animation (3 flashes)
        for _ in range(3):
            # Show flash
            for alpha in range(0, 128, 32):  # Fade in
                flash_surface.set_alpha(alpha)
                self.display.screen.blit(original_surface, (0, 0))
                self.display.screen.blit(flash_surface, (x, y))
                self.display.draw_text(f"{effect_name} applied to {target.name}!",
                                (x + width // 2, y + height // 3),
                                'large', pygame.Color(*colour), center=True)
                pygame.display.flip()
                pygame.time.wait(100)
                
            for alpha in range(128, 0, -32):  # Fade out
                flash_surface.set_alpha(alpha)
                self.display.screen.blit(original_surface, (0, 0))
                self.display.screen.blit(flash_surface, (x, y))
                self.display.draw_text(f"{effect_name} applied to {target.name}!",
                                (x + width // 2, y + height // 3),
                                'large', pygame.Color(*colour), center=True)
                pygame.display.flip()
                pygame.time.wait(100)
        
        # Restore original screen
        self.display.screen.blit(original_surface, (0, 0))
        pygame.display.flip()
        
    def draw_chance_to_hit(self, x, y, player, enemy):
        from player import Player
        """Draw chance to hit"""
        layout = self.display.calculate_layout()
        enemy_panel_x = layout['enemy_panel'][2]  # Enemy panel x position
        
        # Calculate hit chances
        player_chance_to_hit = max(5, min(95, player.accuracy - enemy.evasion))
        enemy_chance_to_hit = max(5, min(95, enemy.accuracy - player.evasion))
        
        # Left padding for player text
        player_padding = 10
        self.display.draw_text(f"{player.name}'s chance to hit {enemy.name}: {player_chance_to_hit}%", 
                             (x + player_padding, y + 10), 'large', 'white')
        
        # Right align enemy text with padding from enemy panel
        enemy_padding = 20
        enemy_text = f"{enemy.name}'s chance to hit {player.name}: {enemy_chance_to_hit}%"
        enemy_text_width = self.display.calculate_text_dimensions(enemy_text, 'large')[0]
        enemy_x = enemy_panel_x - enemy_text_width - enemy_padding
        
        self.display.draw_text(enemy_text, (enemy_x, y + 10), 'large', 'white')
        
    def draw_status_bars(self, width, height, x, y, entity, is_player=True):
        """Draw status bars for the player and enemy"""
        # Constants
        BAR_HEIGHT = 25
        BAR_SPACING = 35
        
        # HP Bar
        hp_percent = entity.hp / entity.max_hp
        self.draw_bar(x + 10, y + 30, width - 20, BAR_HEIGHT,
                      hp_percent, "HP", 'darkgreen', f"{entity.hp}/{entity.max_hp}")
        
        # Stamina bar for player
        if is_player:
            stamina_percent = entity.stamina / entity.max_stamina
            self.draw_bar(x + 10, y + 30 + BAR_SPACING, width - 20, BAR_HEIGHT,
                          stamina_percent, "SP", 'teal', f"{entity.stamina}/{entity.max_stamina}")
            status_start_y = y + 30 + (BAR_SPACING * 2)
        else:
            status_start_y = y + 30 + BAR_SPACING
        
        # Status icons
        self.draw_status_effects(x + 10, status_start_y, width - 20, entity)
        
    def draw_bar(self, x, y, width, height, fill_percent, label, colour, value_text, animate=True):
        """Draw a bar with a label and value"""
        # Store current and target percentages
        if not hasattr(self, 'current_fills'):
            self.current_fills = {}
            self.animation_complete = {}
        
        bar_id = f"{label}_{x}_{y}"
        if bar_id not in self.current_fills:
            initial_fill = 1.0 if label in ["HP", "SP"] else 0.0
            self.current_fills[bar_id] = initial_fill
            self.animation_complete[bar_id] = True
            
        target = fill_percent
        current = self.current_fills[bar_id]
        
        # Animate towards target
        if animate and abs(current - target) > 0.001:
            step = (target - current) * 0.1
            self.current_fills[bar_id] += step
            current = self.current_fills[bar_id]
            self.animation_complete[bar_id] = False
        else:
            self.current_fills[bar_id] = target
            current = target
            self.animation_complete[bar_id] = True
            
        # Background
        if label == "HP":
            pygame.draw.rect(self.screen, 'red', (x, y, width, height))
        elif label == "SP":
            pygame.draw.rect(self.screen, 'darkblue', (x, y, width, height))
        else:
            pygame.draw.rect(self.screen, 'gray20', (x, y, width, height))
        
        # Fill bar
        fill_width = int(current * width)
        pygame.draw.rect(self.screen, colour, (x, y, fill_width, height))
        
        # Draw Border
        pygame.draw.rect(self.screen, 'white', (x, y, width, height), 2)
        
        # Draw label
        self.display.draw_text(f"{label}: {value_text}",
                               (x + width // 2, y + height // 2),
                               'medium', center=True)
        
    def wait_for_animation(self):
        """Wait for all status bars animations to complete"""
        while not all(self.animation_complete.values()):
            self.draw_battle_screen(self.display.game.player, self.display.game.current_location, self.last_enemy)
            pygame.time.wait(16)        
        
    def draw_status_effects(self, x, y, width, entity):
        """Draw status effects with icons and details"""
        ICON_SIZE = 50
        ICONS_PER_ROW = width // (ICON_SIZE + 5)
        
        if not entity or not hasattr(entity, 'status_effects'):
            return

        current_x = x
        current_y = y
        icon_count = 0

        for effect in entity.status_effects:
            if effect.is_active:
                # Calculate position for new row if needed
                if icon_count > 0 and icon_count % ICONS_PER_ROW == 0:
                    current_y += ICON_SIZE + 5
                    current_x = x
                    
                # Draw icon background
                pygame.draw.rect(self.screen, 'gray20', 
                            (current_x, current_y, ICON_SIZE, ICON_SIZE))
                
                # Draw icon if available
                if effect.name in self.STATUS_ICONS:
                    icon = pygame.transform.scale(
                        self.STATUS_ICONS[effect.name],
                        (ICON_SIZE, ICON_SIZE)
                    )
                    self.screen.blit(icon, (current_x, current_y))
                
                # Draw duration
                if effect.remaining_duration > 0:
                    self.display.draw_text(f"{effect.remaining_duration}",
                                        (current_x + ICON_SIZE - 5, 
                                        current_y + ICON_SIZE - 5),
                                        'small')
                
                # Draw stacks if applicable
                if hasattr(effect, 'strength') and effect.strength > 1:
                    stack_text = f"x{effect.strength}"
                    self.display.draw_text(stack_text,
                                        (current_x + 5, 
                                        current_y + 5),
                                        'small')
                    
                # Draw stat changes
                stat_y = current_y + ICON_SIZE + 5
                
                # Handle regular status effects
                if hasattr(effect, 'stat_changes') and hasattr(effect, 'total_reductions'):
                    for stat, value in effect.total_reductions.items():
                        stat_text = f"{stat[:3].upper()}: -{value}"
                        self.display.draw_text(stat_text,
                                            (current_x, stat_y),
                                            'small', 'red')
                        stat_y += 15
                
                # Handle stance effects
                if hasattr(effect, 'buff_percents'):
                    for stat, value in effect.buff_percents.items():
                        stat_text = f"{stat.replace('_', ' ').title()}: +{value}%"
                        self.display.draw_text(stat_text,
                                            (current_x, stat_y + 15),
                                            'small', 'green')
                        stat_y += 15
                        
                if hasattr(effect, 'debuff_percents'):
                    for stat, value in effect.debuff_percents.items():
                        stat_text = f"{stat.replace('_', ' ').title()}: -{value}%"
                        self.display.draw_text(stat_text,
                                            (current_x, stat_y + 15),
                                            'small', 'red')
                        stat_y += 15
                
                current_x += ICON_SIZE + 15
                icon_count += 1
                
class LocationActionsMenu:
    def __init__(self, display, player):
        self.display = display
        self.player = player
        self.config = display.config
        
    def show_actions_menu(self, game):
        layout = self.display.calculate_layout()
        battle_log = layout['battle_log_panel']
        width = battle_log[0]
        height = battle_log[1]
        x = battle_log[2]
        y = battle_log[3]
        
        game.display.draw_game_screen(game.player, game.current_location)
        
        while True:
            # Draw action menu panel
            if game.current_location == "Village":
                return False
            self.display.draw_panel(width, height, x, y)
            
            # Draw title
            self.display.draw_text("Location Actions:", 
                               (x + width // 2, y + 30),
                               'large', center=True)
            
            # Draw actions
            actions = [
                "[E]xplore the area",
                "[U]se an item",
                "[R]est to recover",
                "[L]eave this area"
            ]
            
            for i, action in enumerate(actions):
                self.display.draw_text(action,
                                   (x + width // 2, y + 80 + (i * 40)),
                                   'medium', center=True)
            
            pygame.display.flip()
            
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        game.encounter()
                        #self.display.pause()
                        return "explore"
                    elif event.key == pygame.K_u:
                        used_item = game.use_item_menu()
                        if used_item:
                            game.player.show_cooldowns()
                        self.display.pause()
                        return True
                    elif event.key == pygame.K_r:
                        game.rest()
                        self.display.pause()
                        return True
                    elif event.key == pygame.K_l:
                        return False
            
            game.display.clock.tick(game.display.config.FPS)
            
class RandomEventDisplay:
    def __init__(self, display):
        self.display = display
    
    def show_event(self, random_event):
        # Capture the current game screen
        original_screen = self.display.screen.copy()
        
        # Get layout and main panel dimensions
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        # Create overlay surface
        overlay = pygame.Surface((main_panel[0], main_panel[1]))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        
        while True:
            # Restore the original game screen
            self.display.screen.blit(original_screen, (0, 0))
            
            # Draw overlay on top of the background
            self.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
            
            # Calculate panel center positions
            panel_center_x = main_panel[2] + (main_panel[0] // 2)
            base_y = main_panel[3] + 50
            
            # Draw event content
            self._draw_event_content(random_event, panel_center_x, base_y, main_panel)
            
            pygame.display.update()
            self.display.clock.tick(self.display.config.FPS)
            
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    try:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            choice = event.key - pygame.K_1
                            if choice < len(random_event.choices):
                                return choice
                    except ValueError:
                        continue

    def _draw_event_content(self, random_event, panel_center_x, base_y, main_panel):
        # Draw event title
        self.display.draw_text(f"=== {random_event.name} ===",
                            (panel_center_x, base_y),
                            'title', 'gold', center=True)
        
        # Draw description with word wrap
        words = random_event.description.split()
        lines = []
        current_line = []
        line_width = 0
        max_width = main_panel[0] - 40
        
        for word in words:
            word_width = self.display.calculate_text_dimensions(word + " ", 'medium')[0]
            if line_width + word_width <= max_width:
                current_line.append(word)
                line_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                line_width = word_width
                
        if current_line:
            lines.append(' '.join(current_line))
            
        desc_y = base_y + 60
        for line in lines:
            self.display.draw_text(line, (panel_center_x, desc_y),
                                'medium', center=True)
            desc_y += 30
        
        # Draw choices
        choice_y = desc_y + 40
        for i, (choice_text, _) in enumerate(random_event.choices, 1):
            self.display.draw_text(f"{i}: {choice_text}",
                                (panel_center_x, choice_y),
                                'large', center=True)
            choice_y += 40
            
    def show_outcome(self, text, duration=2000):
        layout = self.display.calculate_layout()
        panel = layout['battle_log_panel']
        
        self.display.draw_battle_log_panel(*panel)
        self.display.draw_text(text, (panel[2] + panel[0] // 2, panel[3] + 30), 'large', center=True)
        pygame.display.flip()
        pygame.time.wait(duration)
        
    def display_event_message(self, text):
        layout = self.display.calculate_layout()
        panel = layout['battle_log_panel']
        self.display.add_message(text)
        self.display.draw_battle_log_panel(*panel)
        pygame.display.flip()
        
        
class ComplexEventDisplay(RandomEventDisplay):
    def show_complex_event(self, event_type, player, game):
        """Display complex event interface with multiple choices"""
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        event_settings = {
            'storm': {
                'title': "=== STORM NEXUS ===",
                'description': "Lightning converges in the sky above you, forming a nexus of power...",
                'choices': [
                    "Attempt to channel the storm's power",
                    "Collect storm crystals",
                    "Embrace the storm's power",
                    "Seek shelter"
                ]
            },
            'forge': {
                'title': "=== SOUL FORGE ===",
                'description': "An ancient forge stands before you, emanating a powerful aura...",
                'choices': [
                    "Forge equipment with souls",
                    "Create a soul crystal",
                    "Enhance abilities",
                    "Challenge the forge guardian"
                ]
            },
            'shrine': {
                'title': "=== CURSED SHRINE ===",
                'description': "A dark shrine stands before you, beckoning you to its power...",
                'choices': [
                    "Make a blood sacrifice",
                    "Offer gold",
                    "Attempt to destroy the shrine",
                    "Attempt to leave"
                ]
            },
            'collector': {
                'title': "=== SOUL COLLECTOR ===",
                'description': "A mysterious figure appears before you, offering a deal...",
                'choices': [
                    "Trade monster souls",
                    "Sacrifice boss souls",
                    "Offer your essence",
                    "Reject the offer"
                ]
            }
        }
        
        settings = event_settings[event_type]
        
        # Capture the current game screen
        original_screen = self.display.screen.copy()
        
        # Get layout and main panel dimensions
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        # Create overlay surface
        overlay = pygame.Surface((main_panel[0], main_panel[1]))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        
        while True:
            # Restore the original game screen
            self.display.screen.blit(original_screen, (0, 0))
            
            # Draw overlay on top of the background
            self.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
            
            panel_center_x = main_panel[2] + (main_panel[0] // 2)
            base_y = main_panel[3] + 50
            
            # Draw title
            self.display.draw_text(settings['title'],
                                 (panel_center_x, base_y),
                                 'title', 'gold', center=True)
            
            # Draw description with wrapping
            wrapped_text = self._wrap_text(settings['description'], main_panel[0] - 40)
            for i, line in enumerate(wrapped_text):
                self.display.draw_text(line,
                                     (panel_center_x, base_y + 60 + (i * 25)),
                                     'medium', center=True)
            
            # Draw choices
            choice_y = base_y + 140
            for i, choice_text in enumerate(settings['choices'], 1):
                self.display.draw_text(f"{i}: {choice_text}",
                                     (panel_center_x, choice_y + (i * 40)),
                                     'large', center=True)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    try:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            choice = event.key - pygame.K_1
                            if choice < len(settings['choices']):
                                return choice
                    except ValueError:
                        continue
                        
            self.display.clock.tick(self.display.config.FPS)

    def show_progress(self, title, current, maximum, description="", duration=3000):
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        # Draw base game screen with overlay
        self.display.draw_game_screen(self.display.game.player, self.display.game.current_location)
        overlay = pygame.Surface((main_panel[0], main_panel[1]))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
        
        panel_center_x = main_panel[2] + (main_panel[0] // 2)
        base_y = main_panel[3] + 50
        
        self.display.draw_text(title,
                             (panel_center_x, base_y),
                             'title', 'gold', center=True)
        
        self.display.draw_text(f"Progress: {current}/{maximum}",
                             (panel_center_x, base_y + 50),
                             'large', center=True)
        
        if description:
            wrapped_text = self._wrap_text(description, main_panel[0] - 40)
            for i, line in enumerate(wrapped_text):
                self.display.draw_text(line, 
                                     (panel_center_x, base_y + 100 + (i * 25)),
                                     'medium', center=True)
        
        pygame.display.flip()
        pygame.time.wait(duration)

    def show_choice(self, title, choices, description="", custom_y=None):
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        # Create main game screen
        self.display.draw_game_screen(self.display.game.player, self.display.game.current_location)
        
        # Capture the current game screen
        original_screen = self.display.screen.copy()
        
        # Get layout and main panel dimensions
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        # Create overlay surface
        overlay = pygame.Surface((main_panel[0], main_panel[1]))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        
        while True:
            # Restore the original game screen
            self.display.screen.blit(original_screen, (0, 0))
            
            # Draw overlay on top of the background
            self.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
            
            panel_center_x = main_panel[2] + (main_panel[0] // 2)
            if custom_y is not None:
                base_y = custom_y
            else:
                base_y = main_panel[3] + 50
            
            self.display.draw_text(title,
                                 (panel_center_x, base_y),
                                 'title', 'gold', center=True)
            
            if description:
                wrapped_text = self._wrap_text(description, main_panel[0] - 40)
                for i, line in enumerate(wrapped_text):
                    self.display.draw_text(line,
                                         (panel_center_x, base_y + 50 + (i * 25)),
                                         'medium', center=True)
                choice_y = base_y + 50 + (len(wrapped_text) * 25)
            else:
                choice_y = base_y + 50
                
            for i, choice_text in enumerate(choices):
                self.display.draw_text(f"{i+1}. {choice_text}",
                                     (panel_center_x, choice_y + (i * 40)),
                                     'large', center=True)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    try:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            choice = event.key - pygame.K_1
                            if choice < len(choices):
                                return choice
                    except ValueError:
                        continue
            
            self.display.clock.tick(self.display.config.FPS)

    def show_outcome(self, text, duration=2000):
        """Display an outcome message in the battle log panel"""
        game = self.display.game
        
        self.display.draw_game_screen(game.player, game.current_location)
        self.display.clock.tick(3000)
        
        layout = self.display.calculate_layout()
        panel = layout['battle_log_panel']
        self.display.text_buffer.clear()
        self.display.draw_battle_log_panel(*panel)
        self.display.draw_text(text, (panel[2] + panel[0] // 2, panel[3] + 30), 'large', center=True)
        pygame.display.flip()
        pygame.time.wait(duration)
    
    def show_crystal_description(self, crystal):
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        self.display.draw_game_screen(self.display.game.player, self.display.game.current_location)
        
        # Precise panel positioning
        panel_center_x = main_panel[2] + (main_panel[0] // 2)
        base_y = main_panel[3] + 20  # Start near top of main panel
        max_width = main_panel[0] - 80  # More generous width

        overlay = pygame.Surface((main_panel[0], main_panel[1]))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        
        self.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
        
        # Draw crystal name at the very top
        self.display.draw_text(crystal.name, 
                            (panel_center_x, base_y), 
                            'title', 'gold', center=True)
        
        base_y += 50

        # Get full description and split into sections
        full_description = crystal.get_description()

        lines = str(full_description).split("\n")
        for i, line in enumerate(lines):
            self.display.draw_text(line, 
                                (panel_center_x, base_y + 50 + (i * 30)),
                                'medium', center=True)
            
        pygame.display.flip()
        self.display.pause()

        # Choices closer to bottom
        """choices = ["Close"]
        self.show_choice(
            "Crystal Details", 
            choices, 
            "", 
            custom_y=current_y + 20
        )"""
        
    def show_forged_item_description(self, item, game, souls_used=None, preferred_stats=None):
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        self.display.draw_game_screen(game.player, game.current_location)
        
        panel_center_x = main_panel[2] + (main_panel[0] // 2)
        base_y = main_panel[3] + 20

        overlay = pygame.Surface((main_panel[0], main_panel[1]))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        
        self.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
        
        # Draw item name
        quality_colour = 'gold' if hasattr(item, 'soulbound') and item.soulbound else 'white'
        self.display.draw_text(f"Created: {item.name} ({item.type.title()})", 
                            (panel_center_x, base_y), 
                            'title', quality_colour, center=True)
        
        base_y += 50

        # Get item stats
        stats = []
        stats.append("Stats:")
        if item.attack > 0:
            stats.append(f"Attack: {item.attack}")
        if item.defence > 0:
            stats.append(f"Defence: {item.defence}")
        if item.accuracy > 0:
            stats.append(f"Accuracy: {item.accuracy}")
        if hasattr(item, 'damage_reduction') and item.damage_reduction > 0:
            stats.append(f"Damage Reduction: {item.damage_reduction}")
        if hasattr(item, 'evasion') and item.evasion > 0:
            stats.append(f"Evasion: {item.evasion}")
        if hasattr(item, 'crit_chance') and item.crit_chance > 0:
            stats.append(f"Critical Chance: {item.crit_chance}%")
        if hasattr(item, 'crit_damage') and item.crit_damage > 0:
            stats.append(f"Critical Damage: {item.crit_damage}%")
        if hasattr(item, 'block_chance') and item.block_chance > 0:
            stats.append(f"Block Chance: {item.block_chance}%")
        if hasattr(item, 'armour_penetration') and item.armour_penetration > 0:
            stats.append(f"Armour Penetration: {item.armour_penetration}")

        # Add weapon-specific info
        if item.type == "weapon":
            stats.append(f"Weapon Type: {item.weapon_type.title()}")
            stamina_cost = game.player.get_weapon_stamina_cost(item.weapon_type)
            stats.append(f"Stamina Cost: {stamina_cost}")

        # Display stats
        for i, stat in enumerate(stats):
            self.display.draw_text(stat, 
                                (panel_center_x, base_y + (i * 30)),
                                'medium', center=True)
            
        current_y = base_y + (len(stats) * 30) + 30
        
        # Display soulbound info if applicable
        if hasattr(item, 'soulbound') and item.soulbound:
            self.display.draw_text("Soulbound Properties",
                                (panel_center_x, current_y),
                                'large', 'gold', center=True)
            current_y += 30
            
            self.display.draw_text("- Grows with player level",
                                (panel_center_x, current_y),
                                'medium', center=True)
            current_y += 30
            
            if preferred_stats:
                formatted_stats = ", ".join(stat.replace('_', ' ').title() for stat in preferred_stats)
                self.display.draw_text(f"- Preferred growth stats: {formatted_stats}",
                                    (panel_center_x, current_y),
                                    'medium', center=True)
                current_y += 30
                
        # Display soul sources if available
        if souls_used:
            soul_sources = []
            if isinstance(souls_used, dict):
                if "standard" in souls_used and souls_used["standard"]:
                    soul_sources.extend(souls_used["standard"].keys())
                if "variant" in souls_used and souls_used["variant"]:
                    soul_sources.extend(f"{variant} (Variant)" for variant in souls_used["variant"].keys())
                if "boss" in souls_used and souls_used["boss"]:
                    soul_sources.extend(f"{boss} (Boss)" for boss in souls_used["boss"].keys())
                
            if soul_sources:
                self.display.draw_text("Forged using souls of:",
                                    (panel_center_x, current_y),
                                    'medium', 'gold', center=True)
                current_y += 30
                
                # Split soul sources into chunks for better display
                souls_per_line = 3
                for i in range(0, len(soul_sources), souls_per_line):
                    chunk = soul_sources[i:i + souls_per_line]
                    self.display.draw_text(", ".join(chunk),
                                        (panel_center_x, current_y),
                                        'small', center=True)
                    current_y += 25
        
        pygame.display.flip()
        pygame.time.wait(2000)
        
    def show_forge_message(self, message, game, duration=2000):
        """Display a message in the main panel"""
        layout = self.display.calculate_layout()
        main_panel = layout['main_panel']
        
        # Create overlay
        overlay = pygame.Surface((main_panel[0], main_panel[1]))
        overlay.fill('black')
        overlay.set_alpha(200)
        
        # Draw background and overlay
        self.display.draw_game_screen(game.player, game.current_location)
        self.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
        
        # Draw message
        panel_center_x = main_panel[2] + (main_panel[0] // 2)
        panel_center_y = main_panel[3] + (main_panel[1] // 2)
        self.display.draw_text(message, 
                            (panel_center_x, panel_center_y), 
                            'title', 'gold', center=True)
        
        pygame.display.flip()
        pygame.time.wait(duration)
            
    def _wrap_text(self, text, max_width):
        """Helper method for text wrapping"""
        words = text.split()
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_width = self.display.calculate_text_dimensions(word + " ", 'medium')[0]
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines