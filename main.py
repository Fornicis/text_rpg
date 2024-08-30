import random
#Item class
class Item:
    def __init__(self, name, item_type, value, tier, attack=0, defence=0, effect=0):
        self.name = name
        self.type = item_type
        self.value = value
        self.tier = tier
        self.attack = attack
        self.defence = defence
        self.effect = effect
#Character class, both player and enemy use this with child classes
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
            "shield": None
        }

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
    #Equips item to given slot as specified in item, unequips current item from that slot
    def equip_item(self, item):
        if item.type in self.equipped:
            if self.equipped[item.type]:
                self.unequip_item(item.type)
            self.equipped[item.type] = item
            if item.type == "weapon":
                self.attack += item.attack
            else:
                self.defence += item.defence
            self.inventory.remove(item)
            print(f"You equipped {item.name}.")
        else:
            print("You can't equip that item.")
    #Helper function for equip_item
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
    #Use potions
    def use_item(self, item):
        if item.type == "consumable":
            self.heal(item.effect)
            self.inventory.remove(item)
            print(f"You used {item.name} and restored {item.effect} HP.")
        else:
            print("You can't use that item.")
    #Lists inventory
    def show_inventory(self):
        print("\nInventory:")
        for item in self.inventory:
            print(f"- {item.name} (Value: {item.value} gold)")
        print("\nEquipped:")
        for slot, item in self.equipped.items():
            print(f"{slot.capitalize()}: {item.name if item else 'None'}")

class Enemy(Character):
    def __init__(self, name, hp, attack, defence, exp, gold, tier):
        super().__init__(name, hp, attack, defence)
        self.exp = exp
        self.gold = gold
        self.tier = tier

class Game:
    def __init__(self):
        self.player = None
        self.current_location = "Village"
        self.initialise_items()
        self.initialise_enemies()
        self.initialise_map()

    def initialise_items(self):
        self.items = {
            #Low tier items
            "Rusty Sword": Item("Rusty Sword", "weapon", 20, "low", attack=5),
            "Wooden Shield": Item("Wooden Shield", "shield", 15, "low", defence=3),
            "Leather Helm": Item("Leather Helm", "helm", 10, "low", defence=2),
            "Health Potion": Item("Health Potion", "consumable", 15, "low", effect=20),
            #Medium tier items
            "Steel Sword": Item("Steel Sword", "weapon", 100, "medium", attack=15),
            "Kite Shield": Item("Kite Shield", "shield", 80, "medium", defence=8),
            #High tier items
            "Enchanted Blade": Item("Enchanted Blade", "weapon", 300, "high", attack=25),
            "Dragon Shield": Item("Dragon Shield", "shield", 250, "high", defence=15),
            "Elixir of Life": Item("Elixir of Life", "consumable", 120, "high", effect=100),
        }

    def initialise_enemies(self):
        self.enemies = {
            #Low tier enemies
            "Rat": Enemy("Rat", 20, 5, 1, 10, 5, "low"),
            "Goblin": Enemy("Goblin", 30, 8, 3, 15, 10, "low"),
            #Medium tier enemies
            "Wolf": Enemy("Wolf", 60, 15, 8, 30, 25, "medium"),
            "Orc": Enemy("Orc", 80, 18, 12, 40, 35, "medium"),
            #High tier enemies
            "Dragon": Enemy("Dragon", 200, 30, 25, 100, 200, "high"),
        }

    def initialise_map(self):
        self.game_map = {
            "Village": {"enemies": [], "connected_to": ["Forest", "Plains"]},
            "Forest": {"enemies": ["Rat", "Goblin", "Wolf"], "connected_to": ["Village", "Mountain"]},
            "Plains": {"enemies": ["Goblin", "Wolf"], "connected_to": ["Village", "Desert"]},
            "Mountain": {"enemies": ["Wolf", "Orc"], "connected_to": ["Forest", "Dragon's Lair"]},
            "Desert": {"enemies": ["Orc"], "connected_to": ["Plains", "Ancient Ruins"]},
            "Dragon's Lair": {"enemies": ["Dragon"], "connected_to": ["Mountain"]},
            "Ancient Ruins": {"enemies": ["Orc", "Dragon"], "connected_to": ["Desert"]}
        }

    def create_character(self):
        name = input("Enter your character's name: ")
        self.player = Player(name)
        print(f"Welcome, {self.player.name}! Your adventure begins in the Village.")

    def show_status(self):
        print(f"\n{self.player.name} (Level {self.player.level}):")
        print(f"HP: {self.player.hp}/{self.player.max_hp}")
        print(f"EXP: {self.player.exp}")
        print(f"Gold: {self.player.gold}")
        print(f"Attack: {self.player.attack}")
        print(f"defence: {self.player.defence}")
        print(f"Current location: {self.current_location}")

    def move(self):
        print("\nConnected locations:")
        for location in self.game_map[self.current_location]["connected_to"]:
            print(f"- {location}")
        destination = input("Where do you want to go? ")
        if destination in self.game_map[self.current_location]["connected_to"]:
            self.current_location = destination
            print(f"You have arrived at {self.current_location}.")
            self.encounter()
        else:
            print("You can't go there from here.")
    #Spawns random enemy depending on location
    def encounter(self):
        if self.game_map[self.current_location]["enemies"] and random.random() < 0.7:
            enemy_name = random.choice(self.game_map[self.current_location]["enemies"])
            enemy = self.enemies[enemy_name]
            print(f"You encountered a {enemy.name}!")
            self.battle(enemy)
        else:
            print("You found nothing of interest.")
    #Combat logic, random damage within attack range
    def battle(self, enemy):
        print(f"\nBattle start! {self.player.name} vs {enemy.name}")
        
        while self.player.is_alive() and enemy.is_alive():
            print(f"\n{self.player.name} HP: {self.player.hp}")
            print(f"{enemy.name} HP: {enemy.hp}")
            action = input("Do you want to [a]ttack or [r]un? ")
            
            if action.lower() == "a":
                damage_to_enemy = max(0, (random.randint(self.player.attack // 2, self.player.attack * 2) - enemy.defence))
                damage_to_player = max(0, (random.randint(enemy.attack // 2, enemy.attack * 2) - self.player.defence))
                
                enemy.take_damage(damage_to_enemy)
                print(f"You dealt {damage_to_enemy} damage to {enemy.name}.")
                
                if not enemy.is_alive():
                    print(f"You defeated the {enemy.name}!")
                    self.player.gain_exp(enemy.exp)
                    self.player.gold += enemy.gold
                    print(f"You gained {enemy.exp} EXP and {enemy.gold} gold.")
                    self.loot_drop(enemy.tier)
                    break
                
                self.player.take_damage(damage_to_player)
                print(f"{enemy.name} dealt {damage_to_player} damage to you.")
                
                if not self.player.is_alive():
                    print("You have been defeated. Game over.")
                    return
            
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
    #Random chance of loot, loot is dependant on enemy tier
    def loot_drop(self, enemy_tier):
        if random.random() < 0.3:  # 30% chance of loot drop
            if enemy_tier == "low":
                loot_pool = [item for item in self.items.values() if item.tier == "low"]
            elif enemy_tier == "medium":
                loot_pool = [item for item in self.items.values() if item.tier in ["low", "medium"]]
            else:  # high tier
                loot_pool = list(self.items.values())
            
            item = random.choice(loot_pool)
            self.player.inventory.append(item)
            print(f"You found a {item.name}!")
    
    def game_loop(self):
        self.create_character()
        
        while True:
            self.show_status()
            action = input("\nWhat do you want to do? [m]ove, [i]nventory, [e]quip, [u]se item, [q]uit: ")
            
            if action.lower() == "m":
                self.move()
            elif action.lower() == "i":
                self.player.show_inventory()
            elif action.lower() == "e":
                self.equip_menu()
            elif action.lower() == "u":
                self.use_item_menu()
            elif action.lower() == "q":
                print("Thanks for playing!")
                break
            else:
                print("Invalid action. Try again.")

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
                self.player.use_item(item)
                return
        print("You don't have that item.")

if __name__ == "__main__":
    game = Game()
    game.game_loop()