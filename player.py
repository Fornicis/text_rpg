import random
from items import Item

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
            "belt": None,
            "legs": None,
            "boots": None,
            "gloves": None,
            "shield": None,
            "back": None,
            "ring": None,
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
        self.attack += 3
        self.defence += 1
        self.exp = self.exp // 2
        print(f"Congratulations! You reached level {self.level}!")
        print("Your stats have increased.")

    def equip_item(self, item):
        if item.type in self.equipped:
            if self.equipped[item.type]:
                self.unequip_item(item.type)
            self.equipped[item.type] = item
            if item.type == "weapon":
                self.attack += item.attack
            elif item.type == "ring":
                self.attack += item.attack
                self.defence += item.defence
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
            elif item.type == "ring":
                self.attack += item.attack
                self.defence += item.defence
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
            if item.type == "weapon":
                print(f"- {item.name} (Attack: {item.attack}) (Value: {item.value} gold)")
            elif item.type == "ring":
                print(f"- {item.name} (Attack: {item.attack} Defence: {item.defence}) (Value: {item.value})")
            elif item.type in ["helm", "chest", "belt", "legs", "shield", "back", "gloves", "boots"]:
                print(f"- {item.name} (Defence: {item.defence})(Value: {item.value} gold)")
            else:
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