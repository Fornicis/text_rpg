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
              f"Attack: {self.attack}, Defence: {self.defence}, Stamina: {self.stamina}/{self.max_stamina}")
        if self.active_buffs or self.combat_buffs:
            print("\nActive Buffs:")
            for stat, buff_info in self.active_buffs.items():
                if isinstance(buff_info, dict):
                    print(f"  {stat.capitalize()}: +{buff_info['value']} for {buff_info['duration']} more turns")
                else:
                    print(f"  {stat.capitalize()}: +{buff_info} (Permanent)")
            for stat, buff_info in self.combat_buffs.items():
                print(f"  {stat.capitalize()}: +{buff_info['value']} (Combat Only)")
        if self.active_hots:
                print("\nActive Heal Over Time Effects:")
                for hot_name, hot_info in self.active_hots.items():
                    print(f"  {hot_name}: {hot_info['tick_effect']} HP/turn for {hot_info['duration']} more turns")
        print("\nEquipped Items:")
        for slot, item in self.equipped.items():
            if item:
                print(f"{slot.capitalize()}: {item.name} (Tier: {item.tier.capitalize()})")
                if item.attack > 0:
                    print(f"  Attack: +{item.attack} ({item.weapon_type})")
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
        self.hp = max(0, self.hp - int(damage))

    def heal(self, amount):
        # Heal character, not exceeding max HP
        self.hp = min(self.max_hp, self.hp + int(amount))

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
        self.combat_buffs = {}
        self.items = initialise_items()
        self.give_starter_items()
        self.active_hots = {}
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.weapon_stamina_cost = {"light": 2, "medium": 4, "heavy": 6}
        self.visited_locations = set(["Village"])
    
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
            #Reduce exp by 30% for every level above enemy level, minimum 10%
            scaling_factor = max(0.1, 1 - (level_difference * 0.3))
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
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 1
        self.defence += 1
        self.max_stamina += 5
        stamina_restore = self.max_stamina // 4
        self.restore_stamina(stamina_restore)
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
            
    def apply_buff(self, stat, value, duration, combat_only=True):
        if stat == "attack":
            self.attack += value
        elif stat == "defence":
            self.defence += value
        elif stat == "all stats":
            self.attack += value
            self.defence += value
        
        if combat_only:
            if stat in self.combat_buffs:
                self.combat_buffs[stat]['value'] += value
            else:
                self.combat_buffs[stat] = {'value': value}
        else:
            if stat in self.active_buffs:
                if isinstance(self.active_buffs[stat], dict):
                    self.active_buffs[stat]['value'] += value
                    self.active_buffs[stat]['duration'] = max(self.active_buffs[stat]['duration'], duration)
                else:
                    self.active_buffs[stat] += value
            else:
                self.active_buffs[stat] = {'value': value, 'duration': duration} if duration > 0 else value

    def update_buffs(self):
        for stat, buff_info in list(self.active_buffs.items()):
            if isinstance(buff_info, dict) and 'duration' in buff_info:
                buff_info['duration'] -= 1
                if buff_info['duration'] <= 0:
                    if stat == "attack":
                        self.attack -= buff_info['value']
                    elif stat == "defence":
                        self.defence -= buff_info['value']
                    elif stat == "all stats":
                        self.attack -= buff_info['value']
                        self.defence -= buff_info['value']
                    del self.active_buffs[stat]
                    print(f"Your {stat} buff has worn off.")
                    
    def remove_combat_buffs(self):
        for stat, buff_info in self.combat_buffs.items():
            if stat == "attack":
                self.attack -= buff_info['value']
            elif stat == "defence":
                self.defence -= buff_info['value']
            elif stat == "all stats":
                self.attack -= buff_info['value']
                self.defence -= buff_info['value']
            print(f"Your combat {stat} buff has worn off.")
        self.combat_buffs.clear()
        
    def add_visited_location(self, location):
        self.visited_locations.add(location)

    def use_item(self, item, game=None):
        if item.name in self.cooldowns and self.cooldowns[item.name] > 0:
            print(f"You can't use {item.name} yet. Cooldown: {self.cooldowns[item.name]} turns.")
            return False, f"Couldn't use {item.name} due to cooldown!"

        if item.type in ["consumable", "food", "drink"]:
            message = ""
            if item.effect_type == "healing":
                heal_amount = min(item.effect, self.max_hp - self.hp)
                self.heal(heal_amount)
                message += f"You used {item.name} and restored {heal_amount} HP. "
            elif item.effect_type == "stamina":
                stamina_restore = min(item.stamina_restore, self.max_stamina - self.stamina)
                self.restore_stamina(stamina_restore)
                message += f"You used {item.name} and restored {stamina_restore} Stamina. "
            elif item.effect_type == "buff":
                stat, value = item.effect
                duration = getattr(item, 'duration', 0)
                combat_only = getattr(item, 'combat_only', True)
                self.apply_buff(stat, value, duration, combat_only)
                if combat_only:
                    message += f"You used {item.name} and gained a combat-only {stat} buff of {value}. "
                elif duration > 0:
                    message += f"You used {item.name} and gained a temporary {stat} buff of {value} for {duration} turns. "
                else:
                    message += f"You used {item.name} and gained a permanent {stat} buff of {value}. "
            elif item.effect_type == "hot":
                success, hot_message = self.apply_hot(item)
                if success:
                    message += hot_message
                else:
                    return False, hot_message
            elif item.effect_type == "teleport":
                if game:
                    return self.use_teleport_scroll(game)
                else:
                    return False, "Cannot use teleport scroll outside of game context!"

            self.inventory.remove(item)  # Remove the item from inventory after use
            self.cooldowns[item.name] = item.cooldown
            return True, message
        else:
            message = f"You can't use {item.name}."
            return False, message
        
    def use_teleport_scroll(self, game):
        print("\nVisited locations:")
        for i, location in enumerate(sorted(self.visited_locations), 1):
            print(f"{i}. {location}")
        
        while True:
            choice = input("\nEnter the number of the location you want to teleport to (or 'c' to cancel): ")
            if choice.lower() == 'c':
                return False, "Teleportation cancelled."
            
            try:
                index = int(choice) - 1
                locations = sorted(self.visited_locations)
                if 0 <= index < len(locations):
                    destination = locations[index]
                    game.current_location = destination
                    return True, f"You have teleported to {destination}."
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'c' to cancel.")

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
                weapon_type = getattr(item, 'weapon_type', 'light')
                stamina_cost = self.get_weapon_stamina_cost(weapon_type)
                print(f"{i}. {item.name} (Attack: {item.attack}) (Stamina use: {stamina_cost}) (Value: {item.value} gold)")
            elif item.type == "ring":
                print(f"{i}. {item.name} (Attack: {item.attack} Defence: {item.defence}) (Value: {item.value})")
            elif item.type in ["helm", "chest", "belt", "legs", "shield", "back", "gloves", "boots"]:
                print(f"{i}. {item.name} (Defence: {item.defence})(Value: {item.value} gold)")
            else:
                print(f"{i}. {item.name} (Value: {item.value} gold)")
            
    def show_consumables(self):
        # Display consumable items in inventory
        consumables = [item for item in self.inventory if item.type in ["consumable", "buff", "food", "drink"]]
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
                if item.duration > 0:
                    if item.stamina_restore > 0:
                        return f"Increases {stat} by {value} for {item.duration} turns and restores {item.stamina_restore} stamina."
                    else:
                        return f"Increases {stat} by {value} for {item.duration} turns."
                else:
                    return f"Increases {stat} by {value} until end of combat."
            else:
                return f"Increases attack by {item.effect}"
        elif item.effect_type == "stamina":
            return f"Restores {item.stamina_restore} stamina"
        elif item.effect_type == "teleport":
            return f"Teleports player to previously visited location of choice."
        else:
            return "Unknown effect"
        
    def show_usable_items(self):
        #Shows a list of usable items if available, else prints that none are available
        usable_items = [item for item in self.inventory if item.type in ["consumable", "food", "drink"]]
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
        #Updates the duration of any hots aswell as displaying to the player how many turns are left and informing them they have worn off once duration is over
        for hot_name, hot_info in list(self.active_hots.items()):
            heal_amount = min(hot_info["tick_effect"], self.max_hp - self.hp)
            self.heal(heal_amount)
            hot_info["duration"] -= 1
            
            if hot_info["duration"] > 0:
                print(f"{hot_name} healed you for {heal_amount} HP. ({hot_info['duration']} turns remaining)")
            else:
                print(f"{hot_name} healed you for {heal_amount} HP and has worn off.")
                del self.active_hots[hot_name]
                
    def use_stamina(self, amount):
        self.stamina = max(0, self.stamina - amount)

    def restore_stamina(self, amount):
        self.stamina = min(self.max_stamina, self.stamina + amount)

    def get_weapon_stamina_cost(self, weapon_type):
        return self.weapon_stamina_cost.get(weapon_type, 0)
    
    def can_attack(self):
        equipped_weapon = self.equipped.get('weapon')
        if equipped_weapon:
            weapon_type = equipped_weapon.weapon_type
        else:
            weapon_type = 'light'  # Default to light weapon if no weapon is equipped
        
        stamina_cost = self.get_weapon_stamina_cost(weapon_type)
        return self.stamina >= stamina_cost