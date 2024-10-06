import random
from items import Item, initialise_items
from display import pause, title_screen
from status_effects import *

class Character:
    def __init__(self, name, hp, attack, defence):
        # Initialize basic character attributes
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.status_effects = []
        self.poison_stack = 0
        self.poison_duration = 0
        self.frozen = False
        self.stunned = False
        self.pause = pause
        self.title_screen = title_screen
        
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
        if self.weapon_buff['duration'] > 0:
            print(f"Weapon buff: +{self.weapon_buff['value']} attack for {self.weapon_buff['duration']} more turns")
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
    
    def show_stats(self):
        #Shows the status of the player, 
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
        if self.weapon_buff['duration'] > 0:
            print(f"Weapon buff: +{self.weapon_buff['value']} attack for {self.weapon_buff['duration']} more turns")
        if self.active_hots:
                print("\nActive Heal Over Time Effects:")
                for hot_name, hot_info in self.active_hots.items():
                    print(f"  {hot_name}: {hot_info['tick_effect']} HP/turn for {hot_info['duration']} more turns")
    
    def is_alive(self):
        # Check if character is still alive
        return self.hp > 0

    def take_damage(self, damage):
        # Reduce HP when taking damage, minimum 0
        self.hp = max(0, self.hp - int(damage))

    def heal(self, amount):
        # Heal character, not exceeding max HP
        self.hp = min(self.max_hp, self.hp + int(amount))
        
    def apply_status_effect(self, effect):
        existing_effect = next((e for e in self.status_effects if e.name == effect.name), None)
        if existing_effect:
            existing_effect.duration = max(existing_effect.duration, effect.duration)
            existing_effect.strength = max(existing_effect.strength, effect.strength)
        else:
            self.status_effects.append(effect)
        if effect.duration > 1:
            print(f"{self.name} is affected by {effect.name} for {effect.duration} turns!")
        else:
            print(f"{self.name} is affected by {effect.name}!")

    def remove_status_effect(self, effect_name):
        self.status_effects = [e for e in self.status_effects if e.name != effect_name]

    def update_status_effects(self):
        for effect in self.status_effects[:]:
            effect.apply(self)
            effect.duration -= 1
            if effect.duration <= 0:
                self.status_effects.remove(effect)
                print(f"{effect.name} has worn off from {self.name}.")

    def get_status_effects_display(self):
        return ", ".join(str(effect) for effect in self.status_effects)
        
class Player(Character):
    def __init__(self, name):
        # Initialise player with default stats
        super().__init__(name, hp=100, attack=10, defence=5)
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.base_attack = 10
        self.base_defence = 5
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.respawn_counter = 5
        self.days = 1
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
        self.weapon_buff = {'value': 0, 'duration': 0}
        self.weapon_coating = None
        self.items = initialise_items()
        self.give_starter_items()
        self.active_hots = {}
        self.visited_locations = set(["Village"])
        self.kill_tracker = {}
        self.weapon_stamina_cost = {"light": 2, "medium": 4, "heavy": 6}
        self.attack_types = {
            "normal": {"name": "Normal Attack", "stamina_modifier": 0, "damage_modifier": 1},
            "power": {"name": "Power Attack", "stamina_modifier": 3, "damage_modifier": 1.5},
            "quick": {"name": "Quick Attack", "stamina_modifier": 1, "damage_modifier": 0.8, "extra_attacks": 1},
            "defensive": {"name": "Defensive Stance", "stamina_modifier": 2, "damage_modifier": 0, "defence_boost_percentage": 25, "duration": 5}
        }
        self.defensive_stance = {"boost": 0, "duration": 0}
    
    def give_starter_items(self):
        #Gives starter items to the player
        starter_items = [
            "Wooden Sword",
            "Peasants Top",
            "Peasants Bottoms",
            "Minor Health Potion",
            "Small Bomb",
            "Quick Warrior's Drop",
            "Basic Sharpening Stone"
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
        if level_difference == 0:
            scaling_factor = 1 #Full exp if player is equal level
        elif level_difference == -1:
            scaling_factor = 1.5 #50% extra exp for enemy one level above
        elif level_difference <= -2:
            scaling_factor = 2.0 #100% extra exp for enemy two or more levels above
        else:
            #Reduce exp by 30% for every level above enemy level, minimum 10%
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
    
    def lose_level(self):
        #Players lose a level and all related stats if they lose a battle, can not go below level 1 or lose more than base stats
        if self.level > 1:
            self.level -= 1
            self.max_hp -= 10
            self.attack = max(self.base_attack, self.attack - 1)
            self.defence = max(self.base_defence, self.defence - 1)
            self.max_stamina -= 5
            print(f"You've lost a level. You are now {self.level}")
        else:
            print("You're only a puny level 1. We won't take any levels from you...peasant.")
            
    def lose_gold(self):
        #Players lose half their gold
        lost_gold = self.gold // 2
        self.gold -= lost_gold
        print(f"You've lost {lost_gold} gold. You now have {self.gold} remaining.")
        
    def respawn(self):
        #Player respawns back with half their max HP and stamina, lose one respawn chance
        self.hp = self.max_hp // 2
        self.stamina = self.max_stamina // 2
        self.respawn_counter -= 1
        if self.respawn_counter >= 1:
            print(f"You've been resurrected with {self.hp} HP and {self.stamina} stamina. Do not take this opportunity lightly, you only have {self.respawn_counter} chances left.")
        elif self.respawn_counter == 0:
            print(f"You've been resurrected with {self.hp} HP and {self.stamina} stamina. Do not take this opportunity lightly, this is your final chance, lose again and you lose forever.")
        else:
            self.game_over()

    def game_over(self):
        #Tells the player their final stats after their last death, brings player back to the title_screen
        print("You have been defeated for the final time, the deities have given up on you and you have met the forever death.")
        print("Your final stats are:")
        self.final_stats()
        self.pause()
        print("Now it's time to try again, appease the deities through prowess this time.")
        self.pause()
        self.title_screen()
        
    def final_stats(self):
        # Prepare the stats
        stats = [
            f"The final stats of the adventurer {self.name}",
            f"You managed to reach the lofty level of {self.level}",
            f"Your vitality was massive at a powerful {self.max_hp}",
            f"You had a mighty attack power of {self.attack}",
            f"You were a bulwark of defence with {self.defence}",
            f"With your mighty reserves of energy at {self.max_stamina}",
            f"Your adventure lasted for {self.days} days"
        ]

        # Find the longest line to determine box width
        max_length = max(len(line) for line in stats)
        box_width = max_length + 4  # Add 4 for padding

        # Create the box
        horizontal_border = "═" * (box_width + 2)
        print(f"╔{horizontal_border}╗")

        for stat in stats:
            padded_stat = stat.center(box_width)
            print(f"║ {padded_stat} ║")

        print(f"╚{horizontal_border}╝")
        
        print("\nEnemy Kill Statistics:")
        if not self.kill_tracker:
            print("You didn't manage to defeat any enemies.")
        else:
            total_kills = sum(self.kill_tracker.values())
            print(f"Total enemies defeated: {total_kills}")
            print("Top 5 most defeated enemies:")
            for enemy, count in sorted(self.kill_tracker.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {enemy}: {count}")
    
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
        #Applies the buff of a given item, places them in the appropriate area if they are a combat_only item
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

    def apply_hot(self, item):
        #Applies any HoT items and displays the length of the effect
        if item.effect_type == "hot":
            self.active_hots[item.name] = {
                "duration": item.duration,
                "tick_effect": item.tick_effect
            }
            return True, f"Applied {item.name}. You will heal for {item.tick_effect} HP every turn for {item.duration} turns."
        return False, "This item does not have a heal over time effect."
    
    def apply_defensive_stance(self):
        attack_info = self.attack_types["defensive"]
        defence_boost = int(self.defence * attack_info["defence_boost_percentage"] / 100)
        self.defensive_stance = {
            "boost": defence_boost,
            "duration": attack_info["duration"]
        }
        self.defence += self.defensive_stance["boost"]
        print(f"Your defence increased by {self.defensive_stance['boost']} ({attack_info['defence_boost_percentage']}%) for the next {self.defensive_stance['duration']} turns.")
    
    def apply_poison(self, stacks, duration):
        #Applies the appropriate stacks and duration of poison
        self.poison_stack += stacks
        self.poison_duration = max(self.poison_duration, duration)
        
    def update_poison(self):
        #Updates the poison duration and inflicts poison damage
        if self.poison_duration > 0:
            poison_damage = self.poison_stack
            self.take_damage(poison_damage)
            print(f"{self.name} suffers {poison_damage} poison damage!")
            self.poison_duration -= 1
            if self.poison_duration == 0:
                self.poison_stack = 0
                print("The poison has worn off.")
    
    def update_buffs(self):
        #Reduces the duration of any duration based buffs (Such as HoTs or sharpening stones)
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
        if self.weapon_buff['duration'] > 0:
            self.weapon_buff['duration'] -= 1
            if self.weapon_buff['duration'] <= 0:
                self.attack -= self.weapon_buff['value']
                print(f"Your weapon's sharpening effect has worn off")
                self.weapon_buff = {'value': 0, 'duration': 0}
                    
    def update_cooldowns(self):
        # Decrease cooldowns each turn
        for item, cooldown in list(self.cooldowns.items()):
            if cooldown > 0:
                self.cooldowns[item] -= 1
            else:
                del self.cooldowns[item]
    
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
    
    def update_defensive_stance(self):
        if self.defensive_stance["duration"] > 0:
            self.defensive_stance["duration"] -= 1
            if self.defensive_stance["duration"] == 0:
                self.defence -= self.defensive_stance["boost"]
                print(f"Your defence boost from Defensive Stance has worn off.")
                self.defensive_stance = {"boost": 0, "duration": 0}
            else:
                print(f"\nDefensive Stance remains active for {self.defensive_stance['duration']} more turns.\n")
    
    def update_weapon_coating(self):
        if self.weapon_coating:
            self.weapon_coating['remaining_duration'] -= 1
            if self.weapon_coating['remaining_duration'] <= 0:
                print(f"The {self.weapon_coating['name']} on your weapon has worn off.")
                self.weapon_coating = None
    
    def remove_combat_buffs(self):
        #Removes any combat related buffs at the end of the battle
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
        
    def use_item(self, item, game=None):
        #Allows the player to use an item based on current state, be that cooldown, combat_only items, teleport scrolls etc.
        if item.name in self.cooldowns and self.cooldowns[item.name] > 0:
            print(f"You can't use {item.name} yet. Cooldown: {self.cooldowns[item.name]} turns.")
            return False, f"Couldn't use {item.name} due to cooldown!"

        if item.type in ["consumable", "food", "drink", "weapon coating"]:
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
            elif item.effect_type == "weapon_buff":
                if self.equipped['weapon']:
                    stat, value = item.effect
                    self.weapon_buff['value'] = value
                    self.weapon_buff['duration'] = item.duration
                    self.attack += value
                    message += f"You used {item.name} on your {self.equipped['weapon'].name}. It's attack is increased by {value} for {item.duration} turns"
                else:
                    return False, "You don't have a weapon equipped to use this item on."
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
            elif item.effect_type == "poison" and item.type == "weapon coating":
                if self.equipped['weapon']:
                    if self.equipped['weapon'].weapon_type == "light":
                        self.weapon_coating = {
                            'name': item.name,
                            'stacks': item.effect[0],
                            'duration': item.effect[1],
                            'remaining_duration': item.duration
                        }
                        self.inventory.remove(item)
                        self.cooldowns[item.name] = item.cooldown
                        return True, f"You applied {item.name} to your weapon. It will apply {item.effect[0]} poison stacks for {item.effect[1]} turns on your next {item.duration} attacks."
                    else:
                        return False, f"You can only apply {item.name} to light weapons. Your current weapon is a {self.equipped['weapon'].weapon_type.title()} Weapon!"
                else:
                    return False, "You don't have a weapon equipped to apply the poison coating."    
        
            self.inventory.remove(item)  # Remove the item from inventory after use
            self.cooldowns[item.name] = item.cooldown
            return True, message
            
        else:
            message = f"You can't use {item.name}."
            return False, message
        
    def use_teleport_scroll(self, game):
        #Allows the use of the teleport scroll to move to any previously visited location
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

    def show_usable_items(self):
        #Shows a list of usable items if available, else prints that none are available
        usable_items = [item for item in self.inventory if item.type in ["consumable", "food", "drink", "weapon coating"]]
        if not usable_items:
            print("You have no usable items.")
            return None
        
        print("\nUsable Items:")
        for i, item in enumerate(usable_items, 1):
            effect_description = self.get_effect_description(item)
            print(f"{i}. {item.name}: {effect_description}")
        return usable_items

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
                print(f"{i}. {item.name} (Attack: {item.attack}) (Stamina use: {stamina_cost}) (Weapon type: {item.weapon_type.title()}) (Value: {item.value} gold)")
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
        elif item.effect_type == "weapon_buff":
            if isinstance(item.effect, tuple):
                stat, value = item.effect
                return f"Increases weapon {stat} by {value} for {item.duration} turns"
        elif item.effect_type == "poison" and item.type == "weapon coating":
            return f"Applies {item.effect[0]} poison stacks for {item.effect[1]} turns on your next {item.duration} attacks (Light weapons only)"
        elif item.effect_type == "stamina":
            return f"Restores {item.stamina_restore} stamina"
        elif item.effect_type == "teleport":
            return f"Teleports player to previously visited location of choice."
        else:
            return "Unknown effect"
                
    def use_stamina(self, amount):
        #Reduces the stamina by the given amount
        self.stamina = max(0, self.stamina - amount)

    def restore_stamina(self, amount):
        #Restores the player stamina by the given amount
        self.stamina = min(self.max_stamina, self.stamina + amount)

    def get_weapon_stamina_cost(self, weapon_type):
        #Returns the stamina cost of the given weapon, based on its type
        return self.weapon_stamina_cost.get(weapon_type, 0)
    
    def can_attack(self):
        #Checks to see if the player has enough stamina to attack
        equipped_weapon = self.equipped.get('weapon')
        if equipped_weapon:
            weapon_type = equipped_weapon.weapon_type
        else:
            weapon_type = 'light'  # Default to light weapon if no weapon is equipped
        
        stamina_cost = self.get_weapon_stamina_cost(weapon_type)
        return self.stamina >= stamina_cost
    
    def get_available_attack_types(self):
        if self.defensive_stance["duration"] > 0:
            return {"normal": self.attack_types["normal"]}
        return self.attack_types

    def display_attack_options(self):
        print("\nChoose your attack type:")
        available_attacks = self.get_available_attack_types()
        for i, (key, value) in enumerate(available_attacks.items(), 1):
            weapon_type = self.equipped.get("weapon", {"weapon_type": "light"}).weapon_type
            base_stamina_cost = self.get_weapon_stamina_cost(weapon_type)
            total_stamina_cost = base_stamina_cost + value['stamina_modifier']
            print(f"[{i}] {value['name']} (Stamina cost: {total_stamina_cost})")
            
        if self.defensive_stance["duration"] > 0:
            print("\n(You can only use Normal Attack while in Defensive Stance)")

    def display_kill_stats(self):
        #Displays all the enemies the player has killed
        print("\n=== Enemy Kill Statistics ===")
        if not self.kill_tracker:
            print("You haven't defeated any enemies yet.")
        else:
            for enemy, count in sorted(self.kill_tracker.items(), key = lambda x: x[1], reverse=True):
                print(f"{enemy}: {count}")
    
    def record_kill(self, enemy_name):
        #Records a kill for a given enemy type
        if enemy_name in self.kill_tracker:
            self.kill_tracker[enemy_name] += 1
        else:
            self.kill_tracker[enemy_name] = 1
            
    def add_visited_location(self, location):
        #Adds the current location to the visited_locations to help work with teleport scrolls
        self.visited_locations.add(location)