import random
from player import Player
from items import Item

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
        # Display available items sorted by value
        print("\nShop Inventory:")
        sorted_inventory = sorted(
            self.inventory.items(),
            key=lambda x: x[1]['item'].value,
            reverse=False
        )
        for item_name, info in sorted_inventory:
            if self.is_item_available(info['item'], player_level):
                print(f"- {item_name}: {info['quantity']} available (Price: {info['item'].value} gold)")

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
