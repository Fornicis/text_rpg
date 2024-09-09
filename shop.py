import random
from player import Player
from items import Item
from display import clear_screen

class Shop:
    def __init__(self, all_items):
        self.inventory = {}  # Stores items and their quantities
        self.all_items = all_items  # All possible items in the game
        self.restock_counter = 0  # Tracks actions since last restock
        self.restock_frequency = 10  # Restock every 10 game actions

    def add_item(self, item, quantity):
        # Add an item to the inventory or increase its quantity
        if item.name in self.inventory:
            self.inventory[item.name]['quantity'] += quantity
        else:
            self.inventory[item.name] = {'item': item, 'quantity': quantity}

    def remove_item(self, item_name, quantity):
        # Remove an item from the inventory or decrease its quantity
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] -= quantity
            if self.inventory[item_name]['quantity'] <= 0:
                del self.inventory[item_name]

    def display_inventory(self, player_level):
        print("\nShop Inventory:")
        sorted_inventory = sorted(
            self.inventory.items(),
            key=lambda x: x[1]['item'].value,
            reverse=False
        )
        for i, (item_name, info) in enumerate(sorted_inventory, 1):
            if self.is_item_available(info['item'], player_level):
                print(f"{i}. {item_name}: {info['quantity']} available (Price: {info['item'].value} gold)")

    def rotate_stock(self, player_level):
        # Restock shop after a certain number of actions
        self.restock_counter += 1
        if self.restock_counter >= self.restock_frequency:
            print("\nThe shop has restocked with new items!")
            self.restock_counter = 0
            self.inventory.clear()
            self.stock_shop(player_level)

    def stock_shop(self, player_level=1):
        # Randomly stock the shop with items appropriate for the player's level
        num_items = random.randint(5, 10)
        available_items = [item for item in self.all_items.values() if self.is_item_available(item, player_level)]
        for _ in range(num_items):
            item = random.choice(available_items)
            quantity = random.randint(1, 5) if item.type == "consumable" else 1
            self.add_item(item, quantity)

    def is_item_available(self, item, player_level):
        # Determine if an item is available based on player level and item tier
        tier_levels = {
            "starter": 1,
            "common": 1,
            "uncommon": 5,
            "rare": 10,
            "epic": 20,
            "legendary": 30,
            "mythical": 40
        }
        return player_level >= tier_levels.get(item.tier, 1)

    def buy_items(self, player):
        while True:
            clear_screen()
            self.display_inventory(player.level)
            print(f"\nYour gold: {player.gold}")
            print("\nEnter the numbers of the items you want to buy, separated by spaces.")
            print("For example, to buy items 1, 3, and 5, type: 1 3 5")
            print("Type 'q' when you're finished buying items.")

            choice = input("\nYour choice: ").lower()
            
            if choice == 'q':
                break
            
            try:
                item_indices = [int(i) - 1 for i in choice.split()]
                sorted_inventory = sorted(self.inventory.items(), key=lambda x: x[1]['item'].value, reverse=False)
                items_to_buy = [sorted_inventory[i][1]['item'] for i in item_indices if 0 <= i < len(sorted_inventory)]
                
                if not items_to_buy:
                    print("No valid items selected.")
                    continue
                
                total_cost = sum(item.value for item in items_to_buy)
                
                print("\nYou're about to buy:")
                for item in items_to_buy:
                    print(f"- {item.name} for {item.value} gold")
                print(f"\nTotal cost: {total_cost} gold")
                
                if player.gold < total_cost:
                    print("You don't have enough gold to buy these items.")
                    input("\nPress Enter to continue...")
                    continue
                
                confirm = input("Do you want to proceed? (y/n): ").lower()
                if confirm == 'y':
                    for item in items_to_buy:
                        player.gold -= item.value
                        player.inventory.append(item)
                        self.remove_item(item.name, 1)
                    print(f"You bought {len(items_to_buy)} items for a total of {total_cost} gold.")
                else:
                    print("Purchase cancelled.")
            
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid item numbers separated by spaces.")
            
            input("\nPress Enter to continue...")

    def sell_items(self, player):
        while True:
            clear_screen()
            player.show_inventory()
            print("\nEnter the numbers of the items you want to sell, separated by spaces.")
            print("For example, to sell items 1, 3, and 5, type: 1 3 5")
            print("Type 'q' when you're finished selling items.")

            choice = input("\nYour choice: ").lower()
            
            if choice == 'q':
                break
            
            try:
                item_indices = [int(i) - 1 for i in choice.split()]
                items_to_sell = [player.inventory[i] for i in item_indices if 0 <= i < len(player.inventory)]
                
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
                        player.gold += sell_price
                        player.inventory.remove(item)
                        self.add_item(item, 1)
                    print(f"You sold {len(items_to_sell)} items for a total of {total_value} gold.")
                else:
                    print("Sale cancelled.")
            
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
            
            input("\nPress Enter to continue...")

    def shop_menu(self, player):
        while True:
            self.rotate_stock(player.level)  # Check if it's time to rotate stock
            print("\n--- Shop Menu ---")
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
