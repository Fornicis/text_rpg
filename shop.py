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
        #Adds purchased item to inventory of the shop
        if item.name in self.inventory:
            self.inventory[item.name]['quantity'] += quantity
        else:
            self.inventory[item.name] = {'item': item, 'quantity': quantity}

    def remove_item(self, item_name, quantity):
        #Removes purchased item from inventory of shop
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
        #Rotates the stock every 10 game actions
        self.restock_counter += 1
        if self.restock_counter >= self.restock_frequency:
            print("\nThe shop has restocked with new items!")
            self.restock_counter = 0
            self.inventory.clear()
            self.stock_shop()

    def stock_shop(self):
        #Stocks the shop with 5-10 random items, with a random amount between 1-5 for consumables and only 1 if anything else
        num_items = random.randint(5, 10) 
        available_items = list(self.all_items.values())
        for _ in range(num_items):
            item = random.choice(available_items)
            if item.type == "consumable":
                quantity = random.randint(1, 5)
            else:
                quantity = 1
            self.add_item(item, quantity)