import random
import os
import platform

def clear_screen():
    operating_system = platform.system()
    #Windows
    if operating_system != 'Win64' and operating_system != 'Windows':
        os.system('clear')
    #Mac and Linux
    else:
        os.system('cls')

def pause():
    input("\nPress Enter to continue...")

def display_message(message):
    clear_screen()
    print(message)
    pause()

class Item:
    def __init__(self, name, item_type, value, tier, attack=0, defence=0, effect_type=None, effect=0, cooldown=0):
        self.name = name
        self.type = item_type
        self.value = value
        self.tier = tier
        self.attack = attack
        self.defence = defence
        self.effect_type = effect_type
        self.effect = effect
        self.cooldown = cooldown

class Character:
    def __init__(self, name, hp, attack, defence):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=10, defence=5)
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.inventory = []
        self.equipped = {
            "weapon": None,
            "helm": None,
            "chest": None,
            "legs": None,
            "boots": None,
            "gloves": None,
            "shield": None,
            "back": None
        }
        self.cooldowns = {}

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defence += 3
        print(f"Congratulations! You reached level {self.level}!")
        print("Your stats have increased.")

    def equip_item(self, item):
        if item.type in self.equipped:
            if self.equipped[item.type]:
                self.unequip_item(item.type)
            self.equipped[item.type] = item
            if item.type == "weapon":
                self.attack += item.attack
            else:
                self.defence += item.defence
            if item in self.inventory:
                self.inventory.remove(item)
            print(f"You equipped {item.name}.")
        else:
            print("You can't equip that item.")

    def unequip_item(self, slot):
        item = self.equipped[slot]
        if item:
            if slot == "weapon":
                self.attack -= item.attack
            else:
                self.defence -= item.defence
            self.inventory.append(item)
            self.equipped[slot] = None
            print(f"You unequipped {item.name}.")

    def use_item(self, item):
        if item.name in self.cooldowns and self.cooldowns[item.name] > 0:
            print(f"You can't use {item.name} yet. Cooldown: {self.cooldowns[item.name]} turns.")
            return False

        if item.type == "consumable":
            if item.effect_type == "healing":
                heal_amount = min(item.effect, self.max_hp - self.hp)
                self.heal(heal_amount)
                print(f"You used {item.name} and restored {heal_amount} HP.")
            elif item.effect_type == "damage":
                print(f"You can't use {item.name} outside of battle.")
                return False
            elif item.effect_type == "buff":
                self.apply_buff(item.effect[0], item.effect[1], item.duration)
                print(f"You used {item.name} and gained a temporary buff.")
            
            self.inventory.remove(item)
            self.cooldowns[item.name] = item.cooldown
            return True
        else:
            print(f"You can't use {item.name}.")
            return False

    def update_cooldowns(self):
        for item, cooldown in list(self.cooldowns.items()):
            if cooldown > 0:
                self.cooldowns[item] -= 1
            else:
                del self.cooldowns[item]

    def show_cooldowns(self):
        if not self.cooldowns:
            print("No items are on cooldown.")
        else:
            print("Items on cooldown:")
            for item, cooldown in self.cooldowns.items():
                print(f"- {item}: {cooldown} turns")
    
    def show_inventory(self):
        print("\nInventory:")
        for item in self.inventory:
            print(f"- {item.name} (Value: {item.value} gold)")
        print("\nEquipped:")
        for slot, item in self.equipped.items():
            print(f"{slot.capitalize()}: {item.name if item else 'None'}")
            
    def show_consumables(self):
        consumables = [item for item in self.inventory if item.type == "consumable"]
        if consumables:
            print("\nConsumable Items:")
            for item in consumables:
                effect_description = self.get_effect_description(item)
                print(f"- {item.name}: {effect_description}")
        else:
            print("\nYou have no consumable items.")

    def get_effect_description(self, item):
        if item.effect_type == "healing":
            return f"Restores {item.effect} HP"
        elif item.effect_type == "damage":
            return f"Deals {item.effect} damage"
        elif item.effect_type == "buff":
            return f"Increases attack by {item.effect}"
        else:
            return "Unknown effect"

class Enemy(Character):
    def __init__(self, name, hp, attack, defence, exp, gold, tier):
        super().__init__(name, hp, attack, defence)
        self.exp = exp
        self.gold = gold
        self.tier = tier

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

class Game:
    def __init__(self):
        self.player = None
        self.current_location = "Village"
        self.initialise_items()
        self.initialise_enemies()
        self.initialise_map()
        self.shop = Shop(self.items)
        self.shop.stock_shop()

    def initialise_items(self):
        self.items = {
            #Starter items
            "Peasants Top": Item("Peasants Top", "chest", 0, "starter", defence=1),
            "Peasants Bottoms": Item("Peasants Bottoms", "legs", 0, "starter", defence=1),
            "Wooden Sword": Item("Wooden Sword", "weapon", 0, "starter", attack=2),
            #Low tier weapons
            "Rusty Sword": Item("Rusty Sword", "weapon", 20, "common", attack=5),
            "Wooden Club": Item("Wooden Club", "weapon", 15, "common", attack=4),
            "Farmer's Pitchfork": Item("Farmer's Pitchfork", "weapon", 18, "common", attack=6),
            "Sling": Item("Sling", "weapon", 22, "common", attack=3),
            "Rusty Dagger": Item("Rusty Dagger", "weapon", 16, "common", attack=4),

            #Low tier armour
            "Wooden Shield": Item("Wooden Shield", "shield", 15, "common", defence=2),
            "Leather Helm": Item("Leather Helm", "helm", 10, "common", defence=1),
            "Padded Vest": Item("Padded Vest", "chest", 25, "common", defence=3),
            "Leather Boots": Item("Leather Boots", "boots", 12, "common", defence=1),
            "Cloth Gloves": Item("Cloth Gloves", "gloves", 8, "common", defence=1),
            "Tattered Cloak": Item("Tattered Cloak", "back", 14, "common", defence=1),
            "Leather Leggins": Item("Leather Leggings", "legs", 12, "common", defence=2),
            #Low tier consumables
            "Basic Health Potion": Item("Basic Health Potion", "consumable", 15, "common", effect_type="healing", effect=20, cooldown=3),
            "Fire Bomb": Item("Fire Bomb", "consumable", 30, "common",effect_type="damage", effect=20, cooldown=2),
            "Stone of Courage": Item("Stone of Courage", "consumable", 35, "common", effect_type="buff", effect=("attack", 5), duration=3, cooldown=6),
            #Medium tier items
            "Steel Sword": Item("Steel Sword", "weapon", 100, "uncommon", attack=15),
            "Kite Shield": Item("Kite Shield", "shield", 80, "uncommon", defence=8),
            #High tier
            "Enchanted Blade": Item("Enchanted Blade", "weapon", 300, "rare", attack=25),
            "Dragon Shield": Item("Dragon Shield", "shield", 250, "rare", defence=15),
            "Elixir of Life": Item("Elixir of Life", "consumable", 120, "rare", effect_type="healing", effect=100, cooldown=3),
        }

    def initialise_enemies(self):
        self.enemies = {
            #Easy Enemies
            
            #Plains
            "Rat": Enemy("Rat", 20, 10, 1, 10, random.randrange(3, 10), "low"),
            "Boar": Enemy("Boar", 30, 11, 3, 15, random.randrange(5, 15), "low"),
            "Plains Hawk": Enemy("Plains Hawk", 15, 13, 2, 20, random.randrange(8, 18), "low"),
            "Strider": Enemy("Strider", 40, 9, 2, 25, random.randrange(10, 20), "low"),
            "Bull": Enemy("Bull", 50, 11, 3, 30, random.randrange(12, 24), "low"),
            
            #Cave
            "Bat": Enemy("Bat", 20, 10, 2, 10, random.randrange(3, 10), "low"),
            "Goblin": Enemy("Goblin", 30, 13, 3, 15, random.randrange(5, 15), "low"),
            "Spider": Enemy("Spider", 15, 13, 2, 20, random.randrange(8, 18), "low"),
            "Slime": Enemy("Slime", 50, 9, 6, 25, random.randrange(10, 20), "low"),
            "Frog": Enemy("Frog", 40, 12, 2, 30, random.randrange(12, 24), "low"),
            
            #Forest
            "Tree Sprite": Enemy("Tree Sprite", 15, 10, 3, 10, random.randrange(3, 10), "low"),
            "Snake": Enemy("Snake", 20, 15, 1, 15, random.randrange(5, 15), "low"),
            "Forest Hawk": Enemy("Forest Hawk", 30, 12, 2, 20, random.randrange(8, 18), "low"),
            "Locust": Enemy("Locust", 25, 20, 2, 25, random.randrange(10, 20), "low"),
            "Leprechaun": Enemy("Leprechaun", 55, 13, 1, 30, random.randrange(12, 24), "low"),
            
            #Deepwoods
            "Wood Spirit": Enemy("Wood Spirit", 20, 11, 2, 10, random.randrange(3, 10), "low"),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 30, 10, 4, 15, random.randrange(5, 15), "low"),
            "Deep Bat": Enemy("Deep Bat", 25, 13, 1, 20, random.randrange(8, 18), "low"),
            "Giant Firefly": Enemy("Giant Firefly", 40, 10, 3, 25, random.randrange(10, 20), "low"),
            "Treant": Enemy("Treant", 80, 14, 4, 30, random.randrange(12, 24), "low"),
            
            #Medium Enemies
            
            #Swamp
            "Alligator": Enemy("Alligator", 75, 20, 15, 35, random.randrange(30, 41), "medium"),
            "Poison Frog": Enemy("Poison Frog", 50, 25, 5, 40, random.randrange(35, 46), "medium"),
            "Swamp Troll": Enemy("Swamp Troll", 100, 15, 20, 45, random.randrange(40, 51), "medium"),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 60, 18, 8, 35, random.randrange(30, 41), "medium"),
            "Bog Witch": Enemy("Bog Witch", 70, 22, 10, 50, random.randrange(45, 56), "medium"),
            
            #Temple
            "Stone Golem": Enemy("Stone Golem", 120, 15, 25, 55, random.randrange(50, 61), "medium"),
            "Cultist": Enemy("Cultist", 65, 20, 12, 40, random.randrange(35, 46), "medium"),
            "Mummy": Enemy("Mummy", 80, 18, 15, 45, random.randrange(40, 51), "medium"),
            "Animated Statue": Enemy("Animated Statue", 90, 17, 20, 50, random.randrange(45, 56), "medium"),
            "Temple Guardian": Enemy("Temple Guardian", 100, 20, 18, 55, random.randrange(50, 61), "medium"),
            
            #Mountain
            "Mountain Lion": Enemy("Mountain Lion", 70, 22, 10, 40, random.randrange(35, 46), "medium"),
            "Rock Elemental": Enemy("Rock Elemental", 110, 15, 25, 50, random.randrange(45, 56), "medium"),
            "Harpy": Enemy("Harpy", 65, 25, 8, 45, random.randrange(40, 51), "medium"),
            "Yeti": Enemy("Yeti", 95, 20, 15, 50, random.randrange(45, 56), "medium"),
            "Orc": Enemy("Orc", 80, 18, 12, 40, random.randrange(35, 46), "medium"),
            
            #Desert
            "Sand Wurm": Enemy("Sand Wurm", 85, 20, 15, 45, random.randrange(40, 51), "medium"),
            "Dried Mummy": Enemy("Dried Mummy", 75, 17, 18, 40, random.randrange(35, 46), "medium"),
            "Dust Devil": Enemy("Dust Devil", 60, 25, 10, 45, random.randrange(40, 51), "medium"),
            "Desert Bandit": Enemy("Desert Bandit", 70, 22, 12, 50, random.randrange(45, 56), "medium"),
            "Leopard": Enemy("Leopard", 65, 23, 8, 35, random.randrange(30, 41), "medium"),
            
            #Medium-Hard Enemies
            
            #Valley
            "Canyon Cougar": Enemy("Canyon Cougar", 100, 35, 15, 70, random.randrange(65, 81), "medium-hard"),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 150, 25, 30, 75, random.randrange(70, 86), "medium-hard"),
            "Dust Devil": Enemy("Dust Devil", 130, 30, 25, 80, random.randrange(75, 91), "medium-hard"),
            "Petrified Warrior": Enemy("Petrified Warrior", 120, 28, 28, 85, random.randrange(80, 96), "medium-hard"),
            "Thunderbird": Enemy("Thunderbird", 140, 32, 22, 90, random.randrange(85, 101), "medium-hard"),
            
            #Hard Enemies
            
            #Toxic Swamp
            "Venomous Hydra": Enemy("Venomous Hydra", 200, 45, 35, 120, random.randrange(95, 116), "hard"),
            "Plague Bearer": Enemy("Plague Bearer", 180, 50, 30, 125, random.randrange(100, 121), "hard"),
            "Mire Leviathan": Enemy("Mire Leviathan", 250, 40, 40, 130, random.randrange(105, 126), "hard"),
            "Toxic Shambler": Enemy("Toxic Shambler", 170, 55, 25, 135, random.randrange(110, 131), "hard"),
            "Swamp Hag": Enemy("Swamp Hag", 190, 48, 32, 140, random.randrange(115, 136), "hard"),
            
            #Ruins
            "Ancient Golem": Enemy("Ancient Golem", 300, 35, 50, 120, random.randrange(120, 141), "hard"),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 220, 50, 35, 125, random.randrange(125, 146), "hard"),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 180, 60, 30, 130, random.randrange(130, 151), "hard"),
            "Ruin Wraith": Enemy("Ruin Wraith", 200, 55, 35, 135, random.randrange(135, 156), "hard"),
            "Forgotten Titan": Enemy("Forgotten Titan", 280, 45, 45, 140, random.randrange(140, 161), "hard"),
            
            #Mountain Peaks
            "Frost Giant": Enemy("Frost Giant", 280, 50, 40, 100, random.randrange(145, 166), "hard"),
            "Storm Harpy": Enemy("Storm Harpy", 190, 65, 25, 105, random.randrange(150, 171), "hard"),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 250, 45, 50, 110, random.randrange(155, 176), "hard"),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 220, 60, 35, 115, random.randrange(160, 181), "hard"),
            "Yeti Alpha": Enemy("Yeti Alpha", 260, 55, 45, 120, random.randrange(165, 186), "hard"),
            
            #Scorching Plains
            "Fire Elemental": Enemy("Fire Elemental", 230, 70, 30, 100, random.randrange(170, 191), "hard"),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 210, 65, 35, 105, random.randrange(175, 196), "hard"),
            "Mirage Assassin": Enemy("Mirage Assassin", 200, 75, 25, 110, random.randrange(180, 201), "hard"),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 240, 60, 40, 115, random.randrange(185, 206), "hard"),
            "Desert Colossus": Enemy("Desert Colossus", 300, 55, 50, 120, random.randrange(190, 211), "hard"),
            
            #Shadowed Valley
            "Nightmare Stalker": Enemy("Nightmare Stalker", 220, 70, 35, 110, random.randrange(195, 216), "hard"),
            "Void Weaver": Enemy("Void Weaver", 200, 75, 30, 115, random.randrange(200, 221), "hard"),
            "Shadow Dragon": Enemy("Shadow Dragon", 280, 65, 45, 120, random.randrange(205, 226), "hard"),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 190, 80, 25, 125, random.randrange(210, 231), "hard"),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 320, 60, 55, 130, random.randrange(215, 236), "hard"),
            
            #Very Hard Enemies
            
            #Death Caves
            "Necropolis Guardian": Enemy("Necropolis Guardian", 400, 85, 70, 300, random.randrange(240, 271), "very-hard"),
            "Soul Reaver": Enemy("Soul Reaver", 350, 100, 60, 325, random.randrange(250, 281), "very-hard"),
            "Bone Colossus": Enemy("Bone Colossus", 450, 80, 80, 350, random.randrange(260, 291), "very-hard"),
            "Spectral Devourer": Enemy("Spectral Devourer", 380, 95, 65, 375, random.randrange(270, 301), "very-hard"),
            "Lich King": Enemy("Lich King", 420, 90, 75, 400, random.randrange(280, 311), "very-hard"),
            
            #Ancient Ruins
            "Timeless Sphinx": Enemy("Timeless Sphinx", 430, 88, 78, 300, random.randrange(290, 321), "very-hard"),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 400, 95, 70, 325, random.randrange(300, 331), "very-hard"),
            "Anubis Reborn": Enemy("Anubis Reborn", 420, 92, 72, 350, random.randrange(310, 341), "very-hard"),
            "Mummy Emperor": Enemy("Mummy Emperor", 450, 85, 80, 375, random.randrange(320, 351), "very-hard"),
            "Living Obelisk": Enemy("Living Obelisk", 500, 80, 85, 400, random.randrange(330, 361), "very-hard"),
            
            #Death Valley
            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 440, 100, 70, 300, random.randrange(340, 371), "very-hard"),
            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 480, 90, 75, 325, random.randrange(350, 381), "very-hard"),
            "Void Titan": Enemy("Void Titan", 520, 85, 80, 350, random.randrange(360, 391), "very-hard"),
            "Chaos Incarnate": Enemy("Chaos Incarnate", 460, 95, 75, 375, random.randrange(370, 401), "very-hard"),
            "Eternity Warden": Enemy("Eternity Warden", 500, 92, 78, 400, random.randrange(380, 411), "very-hard"),
            
            #Dragon's Lair
            "Ancient Wyvern": Enemy("Ancient Wyvern", 480, 95, 75, 300, random.randrange(390, 421), "very-hard"),
            "Elemental Drake": Enemy("Elemental Drake", 460, 100, 70, 325, random.randrange(400, 431), "very-hard"),
            "Dragonlord": Enemy("Dragonlord", 500, 98, 77, 350, random.randrange(410, 441), "very-hard"),
            "Chromatic Dragon": Enemy("Chromatic Dragon", 520, 96, 79, 375, random.randrange(420, 451), "very-hard"),
            "Elder Dragon": Enemy("Elder Dragon", 550, 100, 80, 400, random.randrange(440, 471), "very-hard"),
            
            #Extreme Enemies
            
            #Volcanic Valley
            "Magma Colossus": Enemy("Magma Colossus", 800, 150, 120, 500, random.randrange(480, 531), "extreme"),
            "Phoenix Overlord": Enemy("Phoenix Overlord", 750, 180, 100, 520, random.randrange(500, 551), "extreme"),
            "Volcanic Titan": Enemy("Volcanic Titan", 900, 140, 140, 540, random.randrange(520, 571), "extreme"),
            "Inferno Wyrm": Enemy("Inferno Wyrm", 850, 160, 110, 560, random.randrange(540, 591), "extreme"),
            "Cinder Archfiend": Enemy("Cinder Archfiend", 780, 170, 130, 580, random.randrange(560, 611), "extreme"),
            
            #Boss Monsters
            
            #The Heavens
            "Seraphim Guardian": Enemy("Seraphim Guardian", 1200, 200, 180, 1000, random.randrange(950, 1051), "boss"),
            "Celestial Arbiter": Enemy("Celestial Arbiter", 1100, 220, 160, 1100, random.randrange(1050, 1151), "boss"),
            "Astral Demiurge": Enemy("Astral Demiurge", 1300, 190, 190, 1200, random.randrange(1150, 1251), "boss"),
            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1400, 210, 170, 1300, random.randrange(1250, 1351), "boss"),
            "Divine Architect": Enemy("Divine Architect", 1500, 230, 200, 1500, random.randrange(1450, 1551), "boss"),
        }

    def initialise_map(self):
        self.game_map = {
            #Home
            "Village": {"enemies": [], "connected_to": ["Forest", "Plains"]},
            #Easy Monster Areas
            "Deepwoods": {"enemies": ["Wood Spirit", "Deepwood Stalker", "Deep Bat", "Giant Firefly", "Treant"], "connected_to": ["Forest", "Swamp"]},
            "Cave": {"enemies": ["Bat", "Goblin", "Spider", "Slime", "Frog"], "connected_to": ["Plains", "Temple"]},
            "Forest": {"enemies": ["Tree Sprite", "Snake", "Forest Hawk", "Locust", "Leprechaun"], "connected_to": ["Village", "Mountain"]},
            "Plains": {"enemies": ["Rat", "Boar", "Plains Hawk", "Strider", "Bull"], "connected_to": ["Village", "Desert"]},
            #Medium Monster Areas
            "Swamp": {"enemies": ["Alligator", "Poison Frog", "Swamp Troll", "Mosquito Swarm", "Bog Witch"], "connected_to": ["Deepwoods", "Toxic Swamp"]},
            "Temple": {"enemies": ["Stone Golem", "Cultist", "Mummy", "Animated Statue", "Temple Guardian"], "connected_to": ["Cave", "Ruins"]},
            "Mountain": {"enemies": ["Mountain Lion", "Rock Elemental", "Harpy", "Yeti", "Orc"], "connected_to": ["Forest", "Valley", "Mountain Peaks"]},
            "Desert": {"enemies": ["Sand Wurm", "Dried Mummy", "Dust Devil", "Desert Bandit", "Leopard"], "connected_to": ["Plains", "Valley", "Scorching Plains"]},
            #Medium-Hard Monster Areas
            "Valley": {"enemies": ["Canyon Cougar", "Twisted Mesquite", "Dust Devil", "Petrified Warrior", "Thunderbird"], "connected_to": ["Mountain", "Desert", "Shadowed Valley"]},
            #Hard Monster Areas
            "Toxic Swamp": {"enemies": ["Venomous Hydra", "Plague Bearer", "Mire Leviathan", "Toxic Shambler", "Swamp Hag"], "connected_to": ["Swamp", "Death Caves"]},
            "Ruins": {"enemies": ["Ancient Golem", "Cursed Pharaoh", "Temporal Anomaly", "Ruin Wraith", "Forgotten Titan"], "connected_to": ["Temple", "Ancient Ruins"]},
            "Mountain Peaks": {"enemies": ["Frost Giant", "Storm Harpy", "Avalanche Elemental", "Mountain Wyvern", "Yeti Alpha"], "connected_to": ["Mountain", "Dragons Lair"]},
            "Scorching Plains": {"enemies": ["Fire Elemental", "Sandstorm Djinn", "Mirage Assassin", "Sunburst Phoenix", "Desert Colossus"], "connected_to": ["Desert", "Death Valley"]},
            "Shadowed Valley": {"enemies": ["Nightmare Stalker", "Void Weaver", "Shadow Dragon", "Ethereal Banshee", "Abyssal Behemoth"], "connected_to": ["Valley", "Volcanic Valley"]},
            #Very Hard Monster Areas
            "Death Caves": {"enemies": ["Necropolis Guardian", "Soul Reaver", "Bone Colossus", "Spectral Devourer", "Lich King"], "connected_to": []},
            "Ancient Ruins": {"enemies": ["Timeless Sphinx", "Eternal Pharaoh", "Anubis Reborn", "Mummy Emperor", "Living Obelisk"], "connected_to": ["Desert"]},
            "Death Valley": {"enemies": ["Apocalypse Horseman", "Abyssal Wyrm", "Void Titan", "Chaos Incarnate", "Eternity Warden"], "connected_to": ["Scorching Plains", "Ancient Ruins", "Volcanic Valley"]},
            "Dragons Lair": {"enemies": ["Ancient Wyvern", "Elemental Drake", "Dragonlord", "Chromatic Dragon", "Elder Dragon"], "connected_to": ["Mountain Peaks", "Death Caves", "Volcanic Valley"]},
            #Extreme Monster Areas
            "Volcanic Valley": {"enemies": ["Magma Colossus", "Phoenix Overlord", "Volcanic Titan", "Inferno Wyrm", "Cinder Archfiend"], "connected_to": ["Shadowed Valley", "Death Valley", "Dragons Lair", "The Heavens"]},
            #Boss Monster Area
            "The Heavens": {"enemies": ["Seraphim Guardian", "Celestial Arbiter", "Astral Demiurge", "Ethereal Leviathan", "Divine Architect"], "connected_to": ["Volcanic Valley"]}
        }

    def create_character(self):
        name = input("Enter your character's name: ")
        self.player = Player(name)
        # Give the player a Peasants Outfit to start with
        starting_items = [self.items["Wooden Sword"], self.items["Peasants Top"], self.items["Peasants Bottoms"]]
        self.player.inventory.append(self.items["Basic Health Potion"])
        for item in starting_items:
            self.player.equip_item(item)
        print(f"Welcome, {self.player.name}! Your adventure begins in the Village.")
        print("You start with a Peasants Outfit equipped and a Basic Health Potion in your inventory.")

    def show_status(self):
        clear_screen()
        print(f"\n{self.player.name} (Level {self.player.level}):")
        print(f"HP: {self.player.hp}/{self.player.max_hp}")
        print(f"EXP: {self.player.exp}")
        print(f"Gold: {self.player.gold}")
        print(f"Attack: {self.player.attack}")
        print(f"Defence: {self.player.defence}")
        print(f"Current location: {self.current_location}")
        print("\nEquipped Items:")
        for slot, item in self.player.equipped.items():
            if item:
                print(f"{slot.capitalize()}: {item.name}")

    def move(self):
        clear_screen()
        print("\nConnected locations:")
        for location in self.game_map[self.current_location]["connected_to"]:
            print(f"- {location}")
        destination = input("Where do you want to go? ").strip().title()
        if destination in self.game_map[self.current_location]["connected_to"]:
            self.current_location = destination
            print(f"You have arrived at {self.current_location}.")
            self.location_actions()
        else:
            print("You can't go there from here.")

    def location_actions(self):
        while True:
            action = input("\nWhat would you like to do? [e]xplore, [r]est, [m]ove, [l]eave: ")
            if action.lower() == 'e':
                self.encounter()
            elif action.lower() == 'r':
                self.rest()
            elif action.lower() == 'm':
                self.move()
            elif action.lower() == 'l':
                break
            else:
                print("Invalid action. Try again.")

    def encounter(self):
        if self.game_map[self.current_location]["enemies"] and random.random() < 0.7:
            enemy_type = random.choice(self.game_map[self.current_location]["enemies"])
            enemy_template = self.enemies[enemy_type]
            # Create a new instance of the enemy
            enemy = Enemy(
                enemy_template.name,
                enemy_template.hp,
                enemy_template.attack,
                enemy_template.defence,
                enemy_template.exp,
                enemy_template.gold,
                enemy_template.tier
            )
            print(f"You encountered a {enemy.name}!")
            self.battle(enemy)
        else:
            print("You explored the area but found nothing of interest.")

    def rest(self):
        heal_amount = self.player.max_hp // 4  # Heal 25% of max HP
        self.player.heal(heal_amount)
        print(f"You rest and recover {heal_amount} HP.")

    def calculate_damage(self, base_attack):
        min_damage = max(1, base_attack - 5)
        max_damage = base_attack + 5
        damage = random.randint(min_damage, max_damage)
        #Critical hit chance 10%
        if random.random() < 0.1:
            damage *= 2
            print("You dealt a critical hit!")
            if damage == 0:
                print("Too bad 0 * 2 is still 0!")
        return damage
    
    def use_battle_item(self, item, target):
        if item.type == "consumable":
            if item.effect_type == "healing":
                heal_amount = item.effect
                target.heal(heal_amount)
                print(f"{target.name} used {item.name} and restored {heal_amount} HP.")
            elif item.effect_type == "damage":
                damage = item.effect
                target.take_damage(damage)
                print(f"{target.name} used {item.name} and dealt {damage} damage.")
            elif item.effect_type == "buff":
                buff_amount = item.effect
                target.attack += buff_amount
                print(f"{target.name} used {item.name} and increased attack by {buff_amount}.")
            self.player.inventory.remove(item)
        else:
            print(f"{item.name} cannot be used in battle.")

    def battle(self, enemy):
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
            self.player.update_cooldowns()
            print(f"\n{self.player.name} HP: {self.player.hp}")
            print(f"{enemy.name} HP: {enemy.hp}")
            action = input("Do you want to [a]ttack, [u]se item, or [r]un? ")
            
            if action.lower() == "a":
                player_base_damage = self.calculate_damage(self.player.attack)
                enemy_base_damage = self.calculate_damage(enemy.attack)
                
                player_damage = max(0, player_base_damage - enemy.defence)
                enemy_damage = max(0, enemy_base_damage - self.player.defence)
                
                enemy.take_damage(player_damage)
                print(f"You dealt {player_damage} damage to {enemy.name}.")
                
                if not enemy.is_alive():
                    print(f"You defeated the {enemy.name}!")
                    self.player.gain_exp(enemy.exp)
                    self.player.gold += enemy.gold
                    print(f"You gained {enemy.exp} EXP and {enemy.gold} gold.")
                    self.loot_drop(enemy.tier)
                    break
                
                self.player.take_damage(enemy_damage)
                print(f"{enemy.name} dealt {enemy_damage} damage to you.")
                
                if not self.player.is_alive():
                    print("You have been defeated. Game over.")
                    return
            
            elif action.lower() == "u":
                self.player.show_consumables()
                item_name = input("Enter the name of the item you want to use (or 'cancel'): ")
                if item_name.lower() == 'cancel':
                    continue
                
                item = next((item for item in self.player.inventory if item.name.lower() == item_name.lower()), None)
                if item:
                    target = self.player if item.effect_type in ["healing", "buff"] else enemy
                    self.use_battle_item(item, target)
                else:
                    print("You don't have that item.")
                pause()
            
            elif action.lower() == "r":
                if random.random() < 0.5:
                    print("You successfully ran away!")
                    return
                else:
                    print("You failed to run away.")
                    self.player.take_damage(max(0, enemy.attack - self.player.defence))
                    print(f"{enemy.name} dealt {max(0, enemy.attack - self.player.defence)} damage to you.")
            
            else:
                print("Invalid action. You lose your turn.")

    def loot_drop(self, enemy_tier):
        if random.random() < 0.3:  # 30% chance of loot drop
            if enemy_tier == "low":
                loot_pool = [item for item in self.items.values() if item.tier == "common"]
            elif enemy_tier in ["medium", "medium-hard"]:
                loot_pool = [item for item in self.items.values() if item.tier == "medium"]
            elif enemy_tier in ["medium-hard", "hard"]:  # high tier
                loot_pool = [item for item in self.items.values() if item.tier == "rare"]
            elif enemy_tier == "very-hard":
                loot_pool = [item for item in self.items.values() if item.tier == "epic"]
            elif enemy_tier == "extreme":
                loot_pool = [item for item in self.items.values() if item.tier == "legendary"]
            else:
                loot_pool = [item for item in self.items.values() if item.tier == "mythical"]
                
            
            item = random.choice(loot_pool)
            self.player.inventory.append(item)
            print(f"You found a {item.name}!")
            
    def shop_menu(self):
        while True:
            clear_screen()
            self.shop.rotate_stock()  # Check if it's time to rotate stock
            print("\n--- Shop Menu ---")
            print("1. Buy items")
            print("2. Sell items")
            print("3. Exit shop")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.buy_item()
            elif choice == '2':
                self.sell_item()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def buy_item(self):
        self.shop.display_inventory()
        item_name = input("Enter the name of the item you want to buy (or 'cancel'): ")
        if item_name.lower() == 'cancel':
            return

        # Create a case-insensitive dictionary of inventory items
        inventory_lower = {name.lower(): info for name, info in self.shop.inventory.items()}

        if item_name.lower() in inventory_lower:
            item_info = inventory_lower[item_name.lower()]
            if self.player.gold >= item_info['item'].value:
                self.player.gold -= item_info['item'].value
                self.player.inventory.append(item_info['item'])
                self.shop.remove_item(item_info['item'].name, 1)
                print(f"You bought {item_info['item'].name} for {item_info['item'].value} gold.")
            else:
                print("You don't have enough gold to buy this item.")
        else:
            print("This item is not available in the shop.")


    def sell_item(self):
        self.player.show_inventory()
        item_name = input("Enter the name of the item you want to sell (or 'cancel'): ")
        if item_name.lower() == 'cancel':
            return

        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                sell_price = item.value // 2  # Sell for half the buy price
                self.player.gold += sell_price
                self.player.inventory.remove(item)
                self.shop.add_item(item, 1)
                print(f"You sold {item.name} for {sell_price} gold.")
                return
        print("You don't have that item.")

    def equip_menu(self):
        self.player.show_inventory()
        item_name = input("Enter the name of the item you want to equip (or 'cancel'): ")
        if item_name.lower() == "cancel":
            return
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                self.player.equip_item(item)
                return
        print("You don't have that item.")

    def use_item_menu(self):
        self.player.show_inventory()
        item_name = input("Enter the name of the item you want to use (or 'cancel'): ")
        if item_name.lower() == "cancel":
            return
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                if self.player.use_item(item):
                    print(f"You used {item.name}.")
                return
        print("You don't have that item.")
        pause()

    def use_item(self, item):
        if item.effect_type == "healing":
            heal_amount = min(item.effect, self.player.max_hp - self.player.hp)
            self.player.heal(heal_amount)
            print(f"You used {item.name} and restored {heal_amount} HP.")
        elif item.effect_type == "buff":
            self.player.attack += item.effect
            print(f"You used {item.name} and increased your attack by {item.effect}.")
        else:
            print(f"You can't use {item.name} outside of battle.")
            return
        self.player.inventory.remove(item)

    def game_loop(self):
        self.create_character()
        
        while True:
            self.player.update_cooldowns()
            self.show_status()
            action = input("\nWhat do you want to do? [m]ove, [i]nventory, [c]onsumbales, [e]quip, [l]ocation actions, [u]se item, [s]hop (Village only), [q]uit: ")
            
            if action.lower() == "m":
                self.move()
            elif action.lower() == "i":
                clear_screen()
                self.player.show_inventory()
                pause()
            elif action.lower() == "c":
                clear_screen()
                self.player.show_consumables()
                self.player.show_cooldowns()
                pause()
            elif action.lower() == "e":
                clear_screen()
                self.equip_menu()
            elif action.lower() == "l":
                clear_screen()
                self.location_actions()
            elif action.lower() == "u":
                clear_screen()
                self.use_item_menu()
            elif action.lower() == "s":
                if self.current_location == "Village":
                    self.shop_menu()
                else:
                    print("You can only access the shop in the Village.")
            elif action.lower() == "q":
                print("Thanks for playing!")
                break
            else:
                print("Invalid action. Try again.")
                
            self.shop.rotate_stock()  # Check if it's time to rotate stock after each action

if __name__ == "__main__":
    game = Game()
    game.game_loop()