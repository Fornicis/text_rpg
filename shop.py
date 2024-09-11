import random
from player import Player
from items import Item
from display import clear_screen

class BaseShop:
    #Standard shop class, this will allow easy addition of other shops without having to rewrite lots of code
    def __init__(self, all_items):
        self.inventory = {} #Dictionary of items in the shop
        self.all_items = all_items 
        self.restock_counter = 0 #Counter to check if its time for new items to be stocked
        self.restock_frequency = 10 #Amount counter needs to reach before restock occurs

    def add_item(self, item, quantity):
        #Helper function add sold items to shop inventory
        if item.name in self.inventory:
            self.inventory[item.name]['quantity'] += quantity
        else:
            self.inventory[item.name] = {'item': item, 'quantity': quantity}

    def remove_item(self, item_name, quantity):
        #Helper function to remove sold items from shop inventory
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] -= quantity
            if self.inventory[item_name]['quantity'] <= 0:
                del self.inventory[item_name]

    def display_inventory(self, player_level):
        #Displays the shop inventory, sorted in descending value, with each item assigned a number for each of buying
        print(f"\n{self.__class__.__name__} Inventory:")
        sorted_inventory = sorted(
            self.inventory.items(),
            key=lambda x: x[1]['item'].value,
            reverse=False
        )
        for i, (item_name, info) in enumerate(sorted_inventory, 1):
            if self.is_item_available(info['item'], player_level):
                item = info['item']
                print(f"{i}. {item_name}: {info['quantity']} available (Price: {info['item'].value} gold)")
                self.display_item_stats(item)
                
    def display_item_stats(self, item):
        #Shows the stats and effect of different items
        print(f"   Type: {item.type.capitalize()}")
        print(f"   Tier: {item.tier.capitalize()}")
        if item.attack > 0:
            print(f"   Attack: +{item.attack}")
        if item.defence > 0:
            print(f"   Defence: +{item.defence}")
        if item.effect_type:
            print(f"   Effect: {item.effect_type.capitalize()} ({item.effect})")
            print(f"   Cooldown: {item.cooldown} turns")

    def rotate_stock(self, player_level):
        #Helper function which increases the restock counter when called and calls stock_shop based on player level when counter reaches frequency, clears old stock
        self.restock_counter += 1
        if self.restock_counter >= self.restock_frequency:
            print(f"\nThe {self.__class__.__name__} has restocked with new items!")
            self.restock_counter = 0
            self.inventory.clear()
            self.stock_shop(player_level)

    def stock_shop(self, player_level=1):
        #Function which restocks shop based on player level, random amount of items between 5 and 10, only stocks one of weapons and armour
        num_items = random.randint(5, 10)
        available_items = [item for item in self.all_items.values() if self.is_item_available(item, player_level)]
        for _ in range(num_items):
            item = random.choice(available_items)
            quantity = random.randint(1, 5) if item.type == "consumable" else 1
            self.add_item(item, quantity)

    def is_item_available(self, item, player_level):
        #Stocks items based on the level of the player ensuring high level items aren't buyable until required level is met
        tier_levels = {
            "starter": 1,
            "common": 1,
            "uncommon": 5,
            "rare": 10,
            "epic": 15,
            "legendary": 20,
            "mythical": 25
        }
        return player_level >= tier_levels.get(item.tier, 1)

    def buy_items(self, player):
        #Allows the player to buy items from the shop
        while True:
            clear_screen()
            self.display_inventory(player.level)
            print(f"\nYour gold: {player.gold}")
            #Allows player to buy multiple items by typing the related item numbers
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
                print(f"\nTotal cost: {total_cost} gold") #Shows total cost of the items player has selected
                
                if player.gold < total_cost:
                    #Refuses sale if player is too poor
                    print("You don't have enough gold to buy these items.")
                    input("\nPress Enter to continue...")
                    continue
                
                confirm = input("Do you want to proceed? (y/n): ").lower() #Confirms player wants to buy the items
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
        #Same as buy items but for selling, shop buys for half the item value
        while True:
            clear_screen()
            self.display_sellable_items(player)
            print("\nEnter the numbers of the items you want to sell, separated by spaces.")
            print("For example, to sell items 1, 3, and 5, type: 1 3 5")
            print("Type 'q' when you're finished selling items.")

            choice = input("\nYour choice: ").lower()
            
            if choice == 'q':
                break
            
            try:
                item_indices = [int(i) - 1 for i in choice.split()]
                sellable_items = self.get_sellable_items(player)
                items_to_sell = [sellable_items[i] for i in item_indices if 0 <= i < len(sellable_items)]
                
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

    def display_sellable_items(self, player):
        #Shows a list of items the player can sell, offers half item value
        print("\nItems you can sell:")
        sellable_items = self.get_sellable_items(player)
        for i, item in enumerate(sellable_items, 1):
            print(f"{i}. {item.name} (Sell value: {item.value // 2} gold)")

    def get_sellable_items(self, player):
        #Shows items the player can sell
        return [item for item in player.inventory if self.can_sell_item(item)]

    def can_sell_item(self, item):
        # This method should be overridden in child classes
        return True

    def shop_menu(self, player):
        #Shows the shop menu offering player option to buy, sell, or exit
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
    #Child class of shop called Armour, sells weapons and armour
    def __init__(self, all_items):
        super().__init__({k: v for k, v in all_items.items() if v.type in ["weapon", "shield", "helm", "chest", "boots", "gloves", "back", "legs", "belt", "ring"]})

    def can_sell_item(self, item):
        #Allows player to sell armour and weapons
        return item.type in ["weapon", "shield", "helm", "chest", "boots", "gloves", "back", "legs", "belt", "ring"]

class Alchemist(BaseShop):
    #Child class of Shop called Alchemist, sells potions
    def __init__(self, all_items):
        super().__init__({k: v for k, v in all_items.items() if v.type == "consumable"})

    def can_sell_item(self, item):
        #Allows player to sell consumables
        return item.type == "consumable"
