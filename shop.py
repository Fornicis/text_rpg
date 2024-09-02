import random
from player import Player
from items import Item

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