import random
from player import Player
from items import Item
from display import clear_screen

class BaseShop:
    # Standard shop class, this will allow easy addition of other shops without having to rewrite lots of code
    def __init__(self, all_items):
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
        # Shows a list of items the player can sell, offers half item value
        print("\nItems you can sell:")
        sellable_items = self.get_sellable_items(player)
        
        # Group stackable items
        item_groups = {}
        for item in sellable_items:
            if item.name in item_groups:
                if item.is_stackable():
                    item_groups[item.name]['quantity'] += item.stack_size
            else:
                item_groups[item.name] = {
                    'item': item,
                    'quantity': item.stack_size if item.is_stackable() else 1
                }
                
        # Display items
        for i, (name, info) in enumerate(item_groups.items(), 1):
            item = info['item']
            quantity_str = f" x{info['quantity']}" if item.is_stackable() else ""
            print(f"{i}. {name}{quantity_str} (Sell value: {item.value // 2} gold each)")
            
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
            clear_screen()
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
                            effect_type=item.effect_type, effect=item.effect,
                            cooldown=item.cooldown, duration=item.duration,
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
        """Handle selling items with stack support"""
        while True:
            clear_screen()
            self.display_sellable_items(player)
            print("\nEnter the item number and quantity to sell.")
            print("Examples:")
            print("  '1 5' to sell 5 of item 1")
            print("  '1' to sell 1 of item 1")
            print("Type 'q' to finish selling")

            choice = input("\nYour choice: ").lower()
            
            if choice == 'q':
                break
                
            try:
                parts = choice.split()
                if len(parts) == 1:
                    item_idx = int(parts[0]) - 1
                    quantity = 1
                elif len(parts) == 2:
                    item_idx = int(parts[0]) - 1
                    quantity = int(parts[1])
                else:
                    print("Invalid input format.")
                    continue
                
                sellable_items = self.get_sellable_items(player)
                
                # Group items by name for stacked display
                item_groups = {}
                for item in sellable_items:
                    if item.name in item_groups:
                        if item.is_stackable():
                            item_groups[item.name]['quantity'] += item.stack_size
                            item_groups[item.name]['items'].append(item)
                    else:
                        item_groups[item.name] = {
                            'items': [item],
                            'quantity': item.stack_size if item.is_stackable() else 1
                        }
                
                sorted_groups = sorted(item_groups.items())
                
                if 0 <= item_idx < len(sorted_groups):
                    item_name, group_data = sorted_groups[item_idx]
                    total_available = group_data['quantity']
                    
                    if quantity > total_available:
                        print(f"You only have {total_available} {item_name}!")
                        input("\nPress Enter to continue...")
                        continue
                    
                    items = group_data['items']
                    first_item = items[0]
                    sell_value = (first_item.value // 2) * quantity
                    
                    print(f"\nSelling {quantity}x {item_name} for {sell_value} gold")
                    confirm = input("Confirm? (y/n): ").lower()
                    
                    if confirm == 'y':
                        remaining_to_sell = quantity
                        
                        for item in items:
                            if remaining_to_sell <= 0:
                                break
                                
                            if item.is_stackable():
                                if item.stack_size <= remaining_to_sell:
                                    player.inventory.remove(item)
                                    remaining_to_sell -= item.stack_size
                                else:
                                    item.stack_size -= remaining_to_sell
                                    remaining_to_sell = 0
                            else:
                                player.inventory.remove(item)
                                remaining_to_sell -= 1
                                
                        player.gold += sell_value
                        print(f"Sold {quantity}x {item_name} for {sell_value} gold!")
                        
                        # Add items back to shop inventory
                        base_item = first_item
                        self.add_item(base_item, quantity)
                else:
                    print("Invalid item number!")
            
            except ValueError:
                print("Invalid input. Please enter numbers.")
            
            input("\nPress Enter to continue...")
            
    def get_sellable_items(self, player):
        # Shows items the player can sell
        return [item for item in player.inventory if self.can_sell_item(item)]

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

class Armourer(BaseShop):
    # Child class of shop called Armour, sells weapons and armour
    def __init__(self, all_items):
        super().__init__({k: v for k, v in all_items.items() if v.type in ["weapon", "shield", "helm", "chest", "boots", "gloves", "back", "legs", "belt", "ring"] or "Sharpening Stone" in v.name})

    def can_sell_item(self, item):
        # Allows player to sell armour and weapons
        return item.type in ["weapon", "shield", "helm", "chest", "boots", "gloves", "back", "legs", "belt", "ring"] or "Sharpening Stone" in item.name

class Alchemist(BaseShop):
    # Child class of Shop called Alchemist, sells potions
    def __init__(self, all_items):
        super().__init__({k: v for k, v in all_items.items() if v.type in ["consumable", "weapon coating"] and "Sharpening Stone" not in v.name})

    def can_sell_item(self, item):
        # Allows player to sell consumables
        return item.type in ["consumable", "weapon coating"] and "Sharpening Stone" not in item.name

class Inn(BaseShop):
    # Shop class for inn selling food and drink and offering improved rest functions
    def __init__(self, all_items):
        super().__init__({k: v for k, v in all_items.items() if v.type == "food" or v.type == "drink"})

    def can_sell_item(self, item):
        # Checks if item can be solde to the inn
        return item.type in ["food", "drink"]
    
    def inn_menu(self, player):
        # Displays the menu for the inn with numerical choices
        while True:
            clear_screen()
            print("\n--- Welcome to the Inn ---")
            print(f"Your gold: {player.gold}")
            print(f"Your stamina: {player.stamina}/{player.max_stamina}")
            print(f"\n1. Rest (Restore full HP and Stamina) - {player.level * 10} gold")
            print("2. Buy food and drinks")
            print("3. Exit Inn")

            choice = input("Enter your choice: ")

            if choice == '1':
                if player.gold >= (player.level * 10):
                    player.gold -= (player.level * 10)
                    player.hp = player.max_hp
                    player.stamina = player.max_stamina
                    player.days += 1
                    print(f"You rest at the inn, fully restoring your HP and Stamina.")
                    print(f"It is now day {player.days}.")
                else:
                    print("You don't have enough gold to rest at the inn.")
            elif choice == '2':
                self.buy_items(player)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

            input("\nPress Enter to continue...")