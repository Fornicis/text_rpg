import random
from items import Item, initialise_items

class Character:
    def __init__(self, name, hp, attack, defence):
        # Initialize basic character attributes
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        
    def show_status(self):
        #Shows the status and equipment of the player, 
        print(f"\n{self.name} (Level {self.level}):")
        print(f"HP: {self.hp}/{self.max_hp}, EXP: {self.exp}/{self.level*100}, Gold: {self.gold}, "
              f"Attack: {self.attack}, Defence: {self.defence}")
        if self.active_hots:
                print("\nActive Heal Over Time Effects:")
                for hot_name, hot_info in self.active_hots.items():
                    print(f"  {hot_name}: {hot_info['tick_effect']} HP/turn for {hot_info['duration']} more turns")
        print("\nEquipped Items:")
        for slot, item in self.equipped.items():
            if item:
                print(f"{slot.capitalize()}: {item.name} (Tier: {item.tier.capitalize()})")
                if item.attack > 0:
                    print(f"  Attack: +{item.attack}")
                if item.defence > 0:
                    print(f"  Defence: +{item.defence}")
                if item.effect_type:
                    print(f"  Effect: {item.effect_type.capitalize()} - ", end="")
                    if isinstance(item.effect, tuple):
                        print(f"{item.effect[0].capitalize()} +{item.effect[1]}")
                    else:
                        print(f"{item.effect}")
                    if item.cooldown > 0:
                        print(f"  Cooldown: {item.cooldown} turns")
            else:
                print(f"{slot.capitalize()}: None")
            

    def is_alive(self):
        # Check if character is still alive
        return self.hp > 0

    def take_damage(self, damage):
        # Reduce HP when taking damage, minimum 0
        self.hp = max(0, self.hp - damage)

    def heal(self, amount):
        # Heal character, not exceeding max HP
        self.hp = min(self.max_hp, self.hp + amount)

class Player(Character):
    def __init__(self, name):
        # Initialise player with default stats
        super().__init__(name, hp=100, attack=10, defence=5)
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.inventory = []
        # Initialise equipment slots
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
        self.active_buffs = {}
        self.items = initialise_items()
        self.give_starter_items()
        self.active_hots = {}
    
    def give_starter_items(self):
        #Gives starter items to the player
        starter_items = [
            "Wooden Sword",
            "Peasants Top",
            "Peasants Bottoms",
            "Minor Health Potion",
            "Small Bomb",
            "Quick Warrior's Drop"
        ]
        
        for item_name in starter_items:
            #Adds starter items to the players inventory
            item = self.items[item_name]
            self.inventory.append(item)
            print(f"Added {item.name} to inventory.")
            
            if item.type in ["weapon", "helm", "chest", "waist", "legs", "boots", "gloves", "shield", "back", "ring"]:
                #Auto equips the players start equipment to save time
                self.equip_item(item)
        
        print("\nStarter items added and equipped:")
        self.show_inventory()
        
    def gain_exp(self, amount, enemy_level):
        # Gain experience and level up if threshold reached, scales down with overlevelling
        level_difference = self.level - enemy_level
        #Define the scaling factor
        if level_difference <= 0:
            scaling_factor = 1 #Full exp if player is equal or lower level
        else:
            #Reduce exp by 10% for every level above enemy level, minimum 10%
            scaling_factor = max(0.1, 1 - (level_difference * 0.1))
        #Applies scaling factor    
        scaled_exp = int(amount * scaling_factor)
        #Gain exp based on scaled exp
        self.exp += scaled_exp
        print(f"You gained {scaled_exp} experience!")
        #Check for level up
        if self.exp >= self.level * 100:
            self.level_up()

    def level_up(self):
        # Increase player stats on level up
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 3
        self.defence += 1
        self.exp = self.exp // 2
        print(f"Congratulations! You reached level {self.level}!")
        print("Your stats have increased.")

    def equip_item(self, item):
        # Equip an item and apply its stats
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
        # Unequip an item and remove its stats
        item = self.equipped[slot]
        if item:
            if slot == "weapon":
                self.attack -= item.attack
            elif item.type == "ring":
                self.attack -= item.attack
                self.defence -= item.defence
            else:
                self.defence -= item.defence
            self.inventory.append(item)
            self.equipped[slot] = None
            print(f"You unequipped {item.name}.")
            
    def apply_buff(self, stat, value):
        # Apply a temporary stat buff
        if stat == "attack":
            self.attack += value
        elif stat == "defence":
            self.defence += value
        elif stat == "all stats":
            self.defence += value
            self.attack += value
        self.active_buffs[stat] = value

    def remove_all_buffs(self):
    #Remove all active buffs from the player
        if self.active_buffs:
            for stat, value in self.active_buffs.items():
                if stat == "attack":
                    self.attack -= value
                elif stat == "defence":
                    self.defence -= value
                elif stat == "all stats":
                    self.defence -= value
                    self.attack -= value
            buff_count = len(self.active_buffs)
            self.active_buffs.clear()
            print(f"{buff_count} battle buff{'s' if buff_count > 1 else ''} removed.")
        # If there are no active buffs, the method will silently do nothing

    def use_item(self, item):
        # Use a consumable item if not on cooldown
        if item.name in self.cooldowns and self.cooldowns[item.name] > 0:
            print(f"You can't use {item.name} yet. Cooldown: {self.cooldowns[item.name]} turns.")
            return False

        if item.type == "consumable":
            #Ensures player can only use appropriate items outside of battle, no point damaging the environment with damaging effects
            if item.effect_type == "healing":
                heal_amount = min(item.effect, self.max_hp - self.hp)
                self.heal(heal_amount)
                message = f"You used {item.name} and restored {heal_amount} HP."
            elif item.effect_type == "damage":
                message = f"You can't use {item.name} outside of battle."
                return False, message
            elif item.effect_type == "buff":
                stat, value = item.effect
                self.apply_buff(stat, value)
                message = f"You used {item.name} and gained a temporary {stat} buff of {value}."
            elif item.effect_type == "hot":
                return self.apply_hot(item)
            
            self.inventory.remove(item)
            self.cooldowns[item.name] = item.cooldown
            return True, message
        else:
            message = f"You can't use {item.name}."
            return False, message

    def update_cooldowns(self):
        # Decrease cooldowns each turn
        for item, cooldown in list(self.cooldowns.items()):
            if cooldown > 0:
                self.cooldowns[item] -= 1
            else:
                del self.cooldowns[item]

    def show_cooldowns(self):
        # Display items currently on cooldown
        if not self.cooldowns:
            print("No items are on cooldown.")
        else:
            print("Items on cooldown:")
            for item, cooldown in self.cooldowns.items():
                print(f"- {item}: {cooldown} turns")
    
    def show_inventory(self):
        # Display inventory and equipped items
        print("\nInventory:")
        for i, item in enumerate(self.inventory, 1):
            if item.type == "weapon":
                print(f"{i}. {item.name} (Attack: {item.attack}) (Value: {item.value} gold)")
            elif item.type == "ring":
                print(f"{i}. {item.name} (Attack: {item.attack} Defence: {item.defence}) (Value: {item.value})")
            elif item.type in ["helm", "chest", "belt", "legs", "shield", "back", "gloves", "boots"]:
                print(f"{i}. {item.name} (Defence: {item.defence})(Value: {item.value} gold)")
            else:
                print(f"{i}. {item.name} (Value: {item.value} gold)")
        print("\nEquipped:")
        for slot, item in self.equipped.items():
            print(f"{slot.capitalize()}: {item.name if item else 'None'}")
            
    def show_consumables(self):
        # Display consumable items in inventory
        consumables = [item for item in self.inventory if item.type == "consumable"]
        if consumables:
            print("\nConsumable Items:")
            for item in consumables:
                effect_description = self.get_effect_description(item)
                print(f"- {item.name}: {effect_description} (Cooldown: {item.cooldown} turns)")
        else:
            print("\nYou have no consumable items.")

    def get_effect_description(self, item):
        # Get description of item effect
        if item.effect_type == "healing":
            return f"Restores {item.effect} HP"
        elif item.effect_type == "hot":
            total_healing = item.tick_effect * item.duration
            return f"Heals {item.tick_effect} HP per turn for {item.duration} turns (Total: {total_healing} HP)"
        elif item.effect_type == "damage":
            return f"Deals {item.effect} damage"
        elif item.effect_type == "buff":
            if isinstance(item.effect, tuple):
                stat, value = item.effect
                return f"Increases {stat} by {value}"
            else:
                return f"Increases attack by {item.effect}"
        else:
            return "Unknown effect"
        
    def show_usable_items(self):
        #Shows a list of usable items if available, else prints that none are available
        usable_items = [item for item in self.inventory if item.type == "consumable"]
        if not usable_items:
            print("You have no usable items.")
            return None
        
        print("\nUsable Items:")
        for i, item in enumerate(usable_items, 1):
            effect_description = self.get_effect_description(item)
            print(f"{i}. {item.name}: {effect_description}")
        return usable_items
    
    def apply_hot(self, item):
        if item.effect_type == "hot":
            self.active_hots[item.name] = {
                "duration": item.duration,
                "tick_effect": item.tick_effect
            }
            return True, f"Applied {item.name}. You will heal for {item.tick_effect} HP every turn for {item.duration} turns."
        return False, "This item does not have a heal over time effect."

    def update_hots(self):
        for hot_name, hot_info in list(self.active_hots.items()):
            heal_amount = min(hot_info["tick_effect"], self.max_hp - self.hp)
            self.heal(heal_amount)
            hot_info["duration"] -= 1
            
            if hot_info["duration"] > 0:
                print(f"{hot_name} healed you for {heal_amount} HP. ({hot_info['duration']} turns remaining)")
            else:
                print(f"{hot_name} healed you for {heal_amount} HP and has worn off.")
                del self.active_hots[hot_name]