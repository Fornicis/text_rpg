import random
import pygame
from player import Player
from items import Item, SoulCrystal
from display import Display, ShopDisplay

class BaseShop:
    # Standard shop class, this will allow easy addition of other shops without having to rewrite lots of code
    def __init__(self, all_items):
        self.display = Display()
        self.inventory = {} # Dictionary of items in the shop
        self.all_items = all_items 
        self.restock_counter = 0 # Counter to check if its time for new items to be stocked
        self.restock_frequency = 10 # Amount counter needs to reach before restock occurs

    def add_item(self, item, quantity):
        # Helper function add sold items to shop inventory
        if item.name in self.inventory:
            if item.is_stackable():
                self.inventory[item.name]['quantity'] += quantity
            else:
                self.inventory[item.name]['quantity'] += 1
        else:
            self.inventory[item.name] = {'item': item, 'quantity': quantity}

    def remove_item(self, item_name, quantity):
        # Helper function to remove sold items from shop inventory
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] -= quantity
            if self.inventory[item_name]['quantity'] <= 0:
                del self.inventory[item_name]

    def display_inventory(self, player):
        # Displays the shop inventory, sorted in descending value, with each item assigned a number for each of buying
        print(f"\n{self.__class__.__name__} Inventory:")
        sorted_inventory = sorted(
            self.inventory.items(),
            key=lambda x: x[1]['item'].value,
            reverse=False
        )
        for i, (item_name, info) in enumerate(sorted_inventory, 1):
            if self.is_item_available(info['item'], player.level):
                item = info['item']
                quantity_str = f" x{info['quantity']}" if item.is_stackable() else ""
                print(f"{i}. {item_name}{quantity_str} (Price: {info['item'].value} gold)")
                self.display_item_stats(item, player)
                
    def display_sellable_items(self, player):
        print("\nItems you can sell:")
        sellable_items = self.get_sellable_items(player)
        
        # Sort items - soul crystals last, everything else alphabetically
        sorted_items = sorted(sellable_items, key=lambda x: (x.type == "soul_crystal", x.name))
        
        display_items = []
        current_group = None
        
        # Group consecutive stackable items with same name, keep soul crystals individual
        for item in sorted_items:
            if item.type == "soul_crystal":
                display_items.append({'item': item, 'quantity': 1, 'is_group': False})
            else:
                if current_group and current_group['item'].name == item.name:
                    current_group['quantity'] += item.stack_size
                else:
                    current_group = {'item': item, 'quantity': item.stack_size, 'is_group': True}
                    display_items.append(current_group)
        
        # Display items
        for i, info in enumerate(display_items, 1):
            item = info['item']
            quantity_str = f" x{info['quantity']}" if info['is_group'] and info['quantity'] > 1 else ""
            print(f"{i}. {item.name}{quantity_str} (Sell value: {item.value // 2} gold each)")
            
            # Show stats for soul crystals using the class method
            if item.type == "soul_crystal":
                print(item.get_description())
                print()  # Add blank line for readability
            
        return display_items
            
    def display_item_stats(self, item, player):
        print(f"   Type: {item.type.capitalize()}")
        print(f"   Tier: {item.tier.capitalize()}")

        stats = [
            ("Attack", item.attack),
            ("Defence", item.defence),
            ("Accuracy", item.accuracy),
            ("Damage Reduction", getattr(item, 'damage_reduction', 0)),
            ("Evasion", getattr(item, 'evasion', 0)),
            ("Crit Chance", getattr(item, 'crit_chance', 0)),
            ("Crit Damage", getattr(item, 'crit_damage', 0)),
            ("Block Chance", getattr(item, 'block_chance', 0)),
        ]

        for stat_name, stat_value in stats:
            if stat_value > 0:
                if stat_name == "Crit Damage":
                    print(f"   {stat_name}: +{stat_value}%")
                else:
                    print(f"   {stat_name}: +{stat_value}")
        
        if item.type == "weapon":
            stamina_cost = player.get_weapon_stamina_cost(item.weapon_type)
            print(f"   Weapon Type: {item.weapon_type.capitalize()}")
            print(f"   Stamina Cost: {stamina_cost}")

        if item.stamina_restore > 0:
            print(f"   Stamina Restore: {item.stamina_restore}")

        if item.type in ["consumable", "food", "drink"]:
            self.display_consumable_stats(item)
        elif item.type == "weapon coating":
            self.display_coating_stats(item)

        if item.cooldown:
            print(f"   Cooldown: {item.cooldown} turns")

    def display_consumable_stats(self, item):
        if item.effect_type == "buff":
            if isinstance(item.effect, list):
                # Handle multiple stat buffs
                buff_effects = []
                for stat, value in item.effect:
                    stat_name = stat.replace('_', ' ').title()
                    buff_effects.append(f"{stat_name} +{value}")
                buff_str = ", ".join(buff_effects)
                duration_str = f" for {item.duration} turns" if item.duration > 0 else " (Combat Only)"
                print(f"   Effect: {buff_str}{duration_str}")
            else:
                # Handle single stat buff
                stat, value = item.effect if isinstance(item.effect, tuple) else ("Attack", item.effect)
                stat_name = stat.replace('_', ' ').title()
                duration_str = f" for {item.duration} turns" if item.duration > 0 else " (Combat Only)"
                print(f"   Effect: {stat_name} +{value}{duration_str}")
        elif item.effect_type == "healing":
            print(f"   Effect: Healing ({item.effect} HP)")
        elif item.effect_type == "hot":
            total_healing = item.tick_effect * item.duration
            print(f"   Effect: Heal {item.tick_effect} HP/turn for {item.duration} turns (Total: {total_healing} HP)")
        elif item.effect_type == "damage":
            print(f"   Effect: Damage ({item.effect})")
        elif item.effect_type == "weapon_buff":
            stat, value = item.effect if isinstance(item.effect, tuple) else ("Attack", item.effect)
            print(f"   Effect: Increases weapon {stat} by {value} for {item.duration} turns")
        elif item.effect_type == "stamina":
            print(f"   Effect: Restores {item.stamina_restore} stamina")

    def display_coating_stats(self, item):
        if isinstance(item.effect, tuple):
            stack, duration = item.effect
            print(f"   Poison Stacks: {stack} for {duration} turns")

    def rotate_stock(self, player_level):
        # Helper function which increases the restock counter when called and calls stock_shop based on player level when counter reaches frequency, clears old stock
        self.restock_counter += 1
        if self.restock_counter >= self.restock_frequency:
            print(f"\nThe {self.__class__.__name__} has restocked with new items!")
            self.restock_counter = 0
            self.inventory.clear()
            self.stock_shop(player_level)

    def stock_shop(self, player_level=1):
        # Helper function to stack a random range of items which are available based on the player level
        """Stock shop with stackable items"""
        num_items = random.randint(8, 15)
        available_items = [item for item in self.all_items.values() 
                         if self.is_item_available(item, player_level)]
        
        # Ensure at least one item of each rarity (if available)
        rarities = ['common', 'uncommon', 'rare', 'epic', 'masterwork', 'legendary', 'mythical']
        for rarity in rarities:
            rarity_items = [item for item in available_items if item.tier == rarity]
            if rarity_items:
                item = random.choice(rarity_items)
                if item.is_stackable():
                    self.add_item(item, random.randint(1, 5))
                else:
                    self.add_item(item, 1)
                num_items -= 1

        # Fill remaining slots with random items
        for _ in range(num_items):
            item = random.choice(available_items)
            if item.is_stackable():
                self.add_item(item, random.randint(1, 5))
            else:
                self.add_item(item, 1)

    def is_item_available(self, item, player_level):
        # Stocks items based on the level of the player ensuring high level items aren't buyable until required level is met
        tier_levels = {
            "starter": 1,
            "common": 1,
            "uncommon": 3,
            "rare": 6,
            "epic": 10,
            "masterwork": 15,
            "legendary": 20,
            "mythical": 25
        }
        return player_level >= tier_levels.get(item.tier, 1)

    def buy_items(self, player):
        """Handle buying items with stack support"""
        while True:
            self.display.clear_screen(self)
            self.display_inventory(player)
            print(f"\nYour gold: {player.gold}")
            print("\nEnter the numbers of items you want to buy, followed by quantity.")
            print("Examples:")
            print("  '1 5' to buy 5 of item 1")
            print("  '1' to buy 1 of item 1")
            print("  '1,2 3' to buy 1 of item 1 and 3 of item 2")
            print("Type 'q' to finish shopping")

            choice = input("\nYour choice: ").lower()
            
            if choice == 'q':
                break
                
            try:
                # Parse input for multiple items
                parts = choice.split()
                if len(parts) == 1:
                    # Single item, quantity 1
                    items_to_buy = [(int(parts[0]) - 1, 1)]
                elif len(parts) == 2 and ',' in parts[0]:
                    # Multiple items, same quantity
                    item_nums = [int(x) - 1 for x in parts[0].split(',')]
                    quantity = int(parts[1])
                    items_to_buy = [(num, quantity) for num in item_nums]
                elif len(parts) == 2:
                    # Single item with quantity
                    items_to_buy = [(int(parts[0]) - 1, int(parts[1]))]
                else:
                    print("Invalid input format.")
                    input("\nPress Enter to continue...")
                    continue
                
                # Process items
                sorted_inventory = sorted(self.inventory.items(), 
                                       key=lambda x: x[1]['item'].value,
                                       reverse=False)
                
                total_cost = 0
                purchase_list = []
                
                # Validate purchases
                for item_idx, quantity in items_to_buy:
                    if 0 <= item_idx < len(sorted_inventory):
                        item_name, item_data = sorted_inventory[item_idx]
                        
                        if quantity > item_data['quantity']:
                            print(f"Only {item_data['quantity']} {item_name} available!")
                            input("\nPress Enter to continue...")
                            continue
                            
                        cost = item_data['item'].value * quantity
                        total_cost += cost
                        purchase_list.append((item_name, item_data['item'], quantity))
                    else:
                        print(f"Invalid item number: {item_idx + 1}")
                        input("\nPress Enter to continue...")
                        continue
                
                if not purchase_list:
                    continue
                
                # Check if player can afford everything
                if player.gold < total_cost:
                    print(f"You need {total_cost} gold but only have {player.gold}!")
                    input("\nPress Enter to continue...")
                    continue
                
                # Show purchase summary
                print("\nPurchase Summary:")
                for item_name, item, quantity in purchase_list:
                    print(f"- {quantity}x {item_name} @ {item.value} gold each")
                print(f"Total cost: {total_cost} gold")
                
                confirm = input("\nConfirm purchase? (y/n): ").lower()
                if confirm == 'y':
                    player.gold -= total_cost
                    
                    for item_name, item, quantity in purchase_list:
                        # Create new item with proper stack size
                        new_item = type(item)(
                            item.name, item.type, item.value, item.tier,
                            attack=item.attack,
                            defence=item.defence,
                            accuracy=item.accuracy,
                            crit_chance=getattr(item, 'crit_chance', 0),
                            crit_damage=getattr(item, 'crit_damage', 0),
                            armour_penetration=getattr(item, 'armour_penetration', 0),
                            damage_reduction=getattr(item, 'damage_reduction', 0),
                            evasion=getattr(item, 'evasion', 0),
                            block_chance=getattr(item, 'block_chance', 0),
                            effect_type=item.effect_type,
                            effect=item.effect,
                            cooldown=item.cooldown,
                            duration=item.duration,
                            tick_effect=item.tick_effect,
                            weapon_type=item.weapon_type,
                            stamina_restore=item.stamina_restore
                        )
                        
                        if new_item.is_stackable():
                            new_item.stack_size = quantity
                            player.add_item(new_item)
                        else:
                            for _ in range(quantity):
                                player.add_item(new_item)
                                
                        self.remove_item(item_name, quantity)
                    
                    print("\nPurchase complete!")
            
            except ValueError:
                print("Invalid input. Please enter numbers.")
            
            input("\nPress Enter to continue...")

    def sell_items(self, player):
        while True:
            self.display.clear_screen()
            display_items = self.display_sellable_items(player)
            
            print("\nEnter item number to sell (or 'q' to quit):")
            choice = input().lower()
            
            if choice == 'q':
                break
                
            try:
                item_idx = int(choice) - 1
                if 0 <= item_idx < len(display_items):
                    item_info = display_items[item_idx]
                    item = item_info['item']
                    max_quantity = item_info['quantity']
                    
                    if max_quantity > 1:
                        print(f"\nHow many {item.name} to sell? (1-{max_quantity}):")
                        quantity = int(input())
                        if quantity < 1 or quantity > max_quantity:
                            print("Invalid quantity!")
                            input("\nPress Enter to continue...")
                            continue
                    else:
                        quantity = 1
                    
                    sell_value = (item.value // 2) * quantity
                    print(f"\nSelling {quantity}x {item.name} for {sell_value} gold")
                    if input("Confirm? (y/n): ").lower() != 'y':
                        continue
                    
                    # Remove items from inventory
                    if item_info['is_group']:
                        remaining = quantity
                        inventory_items = [i for i in player.inventory if i.name == item.name]
                        for inv_item in inventory_items:
                            if remaining <= 0:
                                break
                            if inv_item.stack_size <= remaining:
                                player.inventory.remove(inv_item)
                                remaining -= inv_item.stack_size
                            else:
                                inv_item.stack_size -= remaining
                                remaining = 0
                    else:
                        player.inventory.remove(item)
                    
                    player.gold += sell_value
                    print(f"Sold {quantity}x {item.name} for {sell_value} gold!")
                    self.add_item(item, quantity)
                    
                else:
                    print("Invalid item number!")
            except ValueError:
                print("Invalid input!")
            
            input("\nPress Enter to continue...")
            
    def get_sellable_items(self, player):
        """Return grouped sellable items from player inventory"""
        sellable_items = [item for item in player.inventory if self.can_sell_item(item)]
        grouped_items = {}
        
        for item in sellable_items:
            if item.type == "soul_crystal":
                # Soul crystals don't stack, add individually
                sellable_items.append(item)
            else:
                # Group stackable items by name and type
                key = (item.name, item.type)
                if key not in grouped_items:
                    grouped_items[key] = item
        
        # Return soul crystals and one instance of each stackable item
        return list(grouped_items.values()) + [item for item in sellable_items if item.type == "soul_crystal"]

    def can_sell_item(self, item):
        # Check if item can be sold, to be overwritten in child classes
        return True

    def shop_menu(self, player):
        # Shows the shop menu offering player option to buy, sell, or exit
        while True:
            self.rotate_stock(player.level)
            print(f"\n--- {self.__class__.__name__} Menu ---")
            print("1. Buy items")
            print("2. Sell items")
            print("3. Exit shop")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.buy_items(player)
            elif choice == '2':
                self.sell_items(player)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def visual_shop_menu(self, player):
        shop_display = ShopDisplay(self.display, player)
        while True:
            shop_display.draw_shop_interface(self, player)
            result = shop_display.handle_shop_events(self, player)
            if result == "exit":
                break
            self.display.clock.tick(self.display.config.FPS)

class Blacksmith(BaseShop):
    # Child class of shop called Armour, sells weapons and armour
    def __init__(self, all_items):
        super().__init__({k: v for k, v in all_items.items() if v.type in ["weapon", "shield", "helm", "chest", "boots", "gloves", "back", "legs", "belt", "ring"] or "Sharpening Stone" in v.name})

    def can_sell_item(self, item):
        # Allows player to sell armour and weapons
        return item.type in ["weapon", "shield", "helm", "chest", "boots", "gloves", "back", "legs", "belt", "ring"] or "Sharpening Stone" in item.name

class Alchemist(BaseShop):
    # Child class of Shop called Alchemist, sells potions
    def __init__(self, all_items):
        super().__init__({k: v for k, v in all_items.items() if v.type in ["consumable", "weapon coating", "soul_crystal"] and "Sharpening Stone" not in v.name})

    def can_sell_item(self, item):
        # Allows player to sell consumables
        return item.type in ["consumable", "weapon coating", "soul_crystal"] and "Sharpening Stone" not in item.name

class Inn(BaseShop):
    # Shop class for inn selling food and drink and offering improved rest functions
    def __init__(self, all_items):
        super().__init__({k: v for k, v in all_items.items() if v.type == "food" or v.type == "drink"})
        self.shop_display = None

    def can_sell_item(self, item):
        # Checks if item can be solde to the inn
        return item.type in ["food", "drink"]
    
    def inn_menu(self, player):
        shop_display = ShopDisplay(self.display, player)
        rest_cost = player.level * 10
        
        location_image = pygame.image.load("assets/area_images/inn.jpg")
        location_image = pygame.transform.scale(location_image, (self.display.config.SCREEN_WIDTH, self.display.config.SCREEN_HEIGHT))
        
        while True:
            self.display.screen.fill('black')
            self.display.screen.blit(location_image, (0, 0))
            # Draw inn header
            self.display.draw_text("=== WELCOME TO THE INN ===",
                                   (self.display.config.SCREEN_WIDTH // 2, 50),
                                   'title', 'gold', center = True)
            
            # Draw player stats
            self.display.draw_text(f"Gold: {player.gold}",
                                   (50,100), 'large')
            self.display.draw_text(f"HP: {player.hp}/{player.max_hp}",
                                   (50, 130), 'large')
            self.display.draw_text(f"Stamina: {player.stamina}/{player.max_stamina}",
                                   (50, 160), 'large')
            
            # Draw rest option
            self.display.draw_text(f"Press R to rest for {rest_cost} gold",
                                   (self.display.config.SCREEN_WIDTH // 2, 200),
                                   'huge', center=True)
            
            self.display.draw_text(f"Press B to buy/sell items",
                                   (self.display.config.SCREEN_WIDTH // 2, 250),
                                   'huge', center=True)
            # Handle events
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if player.gold >= rest_cost:
                            player.gold -= rest_cost
                            player.hp = player.max_hp
                            player.stamina = player.max_stamina
                            player.days += 1
                            
                            # Add pause
                            waiting = True
                            while waiting:
                                for pause_event in pygame.event.get():
                                    if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_RETURN:
                                        waiting = False
                                    elif pause_event.type == pygame.QUIT:
                                        return
                                # Display rest message
                                self.display.screen.fill('black')
                                self.display.draw_text("You have rested at the Inn, fully restoring your HP and Stamina.", 
                                                    (self.display.config.SCREEN_WIDTH // 2, 300), 
                                                    'large', 'gold', center=True)
                                self.display.draw_text(f"Gold remaining: {player.gold}", 
                                                    (self.display.config.SCREEN_WIDTH // 2, 330), 
                                                    'large', 'gold', center=True)
                                self.display.draw_text(f"Days passed: {player.days}", 
                                                    (self.display.config.SCREEN_WIDTH // 2, 360), 
                                                    'large', 'gold', center=True)
                                self.display.draw_text("Press ENTER to continue...", 
                                                    (self.display.config.SCREEN_WIDTH // 2, 400), 
                                                    'medium', center=True)
                                pygame.display.flip()
                                self.display.clock.tick(self.display.config.FPS)
                    
                    elif event.key == pygame.K_b:
                        # Handle player buying/selling items
                        while True:
                            shop_display.draw_shop_interface(self, player)
                            result = shop_display.handle_shop_events(self, player)
                            if result == "exit":
                                break
                            self.display.clock.tick(self.display.config.FPS)
                            
            pygame.display.flip()
            self.display.clock.tick