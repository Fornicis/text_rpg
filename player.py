import random, time
from items import Item, initialise_items
from display import pause, title_screen
from status_effects import *

class Character:
    def __init__(self, name, hp, attack, defence, accuracy=70, evasion=5, crit_chance=5, crit_damage=150, armour_penetration=0, damage_reduction=0, block_chance=0):
        # Initialize basic character attributes
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.attack_types = {
            "normal": {"name": "Normal Attack", "stamina_modifier": 0, "damage_modifier": 1},
        }
        self.defence = defence
        self.accuracy = accuracy
        self.evasion = evasion
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        self.armour_penetration = armour_penetration
        self.damage_reduction = damage_reduction
        self.block_chance = block_chance
        self.stunned = False
        self.confused = False
        self.status_effects = []
        self.pause = pause
        self.title_screen = title_screen
    
    def display_attack_animation(self, attacker_name, attack_name):
        #Shows the enemy attacking in a dramatic way!
        print(f"\n{attacker_name} is preparing to attack...")
        time.sleep(1)  # Pause for dramatic effect
        print(f">>> {attack_name.upper()} <<<")
        time.sleep(0.5)
        
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
              f"Att: {self.attack}, Def: {self.defence}, Eva: {int(self.evasion)}, Acc: {self.accuracy}, Crit%: {self.crit_chance}, Crit Dmg: {self.crit_damage}%, DR: {self.damage_reduction}, BC: {self.block_chance} Stamina: {self.stamina}/{self.max_stamina}")
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
    
    def calculate_damage(self, attacker, defender, attack_type):
        # Calculate hit chance
        hit_chance = max(5, min(95, attacker.accuracy - defender.evasion))
        
        # Check if the attack hits
        if random.randint(1, 100) > hit_chance:
            return 0, "miss", hit_chance  # Attack missed
        
        # Check if the attack is blocked
        if random.randint(1, 100) <= defender.block_chance:
            return 0, "blocked", hit_chance  # Attack blocked

        attack_info = attacker.attack_types[attack_type]
        base_damage = attacker.attack * attack_info["damage_modifier"]
        random_damage = random.randint(int(base_damage * 0.9), int(base_damage * 1.1))
        
        # Apply armour penetration
        effective_defence = max(0, defender.defence - attacker.armour_penetration)
        
        # Calculate initial damage
        damage = max(0, random_damage - effective_defence)
        
        # Check for critical hit
        is_critical = random.randint(1, 100) <= attacker.crit_chance
        if is_critical:
            damage = int(damage * (attacker.crit_damage / 100))
        
        # Apply damage reduction
        damage = int(damage * (1 - defender.damage_reduction / 100))
        
        # Ensure minimum damage of 1 if the attack hits
        damage = max(1, damage)
        
        return damage, "critical" if is_critical else "normal", hit_chance

    def perform_attack(self, target, attack_type):
        attack_info = self.attack_types[attack_type]
        message = f"{self.name} used {attack_info['name']}."
        total_damage = 0
        hits = 1 + attack_info.get("extra_attacks", 0)
        attack_hit = False

        for i in range(hits):
            damage, hit_type, hit_chance = self.calculate_damage(self, target, attack_type)
            
            if hit_type == "miss":
                message += f"\n{self.name}'s attack missed {target.name}!"
            elif hit_type == "blocked":
                message += f"\n{self.name}'s attack was blocked by {target.name}!"
            else:
                attack_hit = True
                target.take_damage(damage)
                total_damage += damage
                if i == 0:
                    message += f"\n{self.name} dealt {damage} damage to {target.name}."
                else:
                    message += f"\n{self.name} dealt an additional {damage} damage to {target.name}."
                
                if hit_type == "critical":
                    message += " Critical hit!"

        if total_damage > 0 and hits > 1:
            message += f"\nTotal damage dealt: {total_damage}"

        self.display_attack_animation(self.name, attack_info['name'])
        
        self_damage_info = None
        if attack_hit and attack_type in ["reckless", "triple"]:
            self_damage = int(total_damage * 0.2)  # 20% of total damage as self-damage
            self_damage_info = {"type": attack_type, "damage": self_damage}
            self.take_damage(self_damage)
            message += f"\n{self.name} takes {self_damage} self-damage from the {attack_type} attack!"
        
        print(message.rstrip())
        
        self.remove_status_effect("Freeze")

        return message, total_damage, self_damage_info, attack_hit

    def is_alive(self):
        # Check if character is still alive
        return self.hp > 0

    def take_damage(self, damage):
        # Reduce HP when taking damage, minimum 0
        self.hp = max(0, self.hp - int(damage))

    def heal(self, amount):
        # Heal character, not exceeding max HP
        self.hp = min(self.max_hp, self.hp + int(amount))
    
    def use_stamina(self, amount):
        # Default implementation that does nothing
        pass
    
    def apply_status_effect(self, new_effect):
        existing_effect = next((e for e in self.status_effects if e.name == new_effect.name), None)
        
        if existing_effect:
            if existing_effect.stackable:
                existing_effect.strength += new_effect.strength
                existing_effect.remaining_duration = max(existing_effect.remaining_duration, new_effect.initial_duration)
                existing_effect.is_active = True
                print(f"{self.name}'s {existing_effect.name} is stacked to {existing_effect.strength} and refreshed for {existing_effect.remaining_duration} turns!")
            else:
                existing_effect.remaining_duration = max(existing_effect.remaining_duration, new_effect.initial_duration)
                existing_effect.strength = max(existing_effect.strength, new_effect.strength)
                existing_effect.is_active = True
                #print(f"{self.name}'s {existing_effect.name} is refreshed to strength {existing_effect.strength} for {existing_effect.remaining_duration} turns!")
        else:
            self.status_effects.append(new_effect)
            apply_result = new_effect.apply(self)
            if apply_result:
                if new_effect.stackable:
                    print(f"{self.name} is affected by {new_effect.name} with {new_effect.strength} stack(s) for {new_effect.remaining_duration} turns!")
                else:
                    print(f"{self.name} is affected by {new_effect.name} for {new_effect.remaining_duration} turns!")
            else:
                self.status_effects.remove(new_effect)

    def update_status_effects(self, character):
        for effect in character.status_effects[:]:
            if effect.is_active:
                is_active, remove_message = effect.update(character)
                if not is_active:
                    if remove_message:
                        print(remove_message)
                    self.remove_status_effect(effect.name)
                    print(f"{effect.name} has worn off from {character.name}.")
            else:
                self.remove_status_effect(effect.name)
   
    def remove_status_effect(self, effect_name):
        self.status_effects = [e for e in self.status_effects if e.name != effect_name]

    def get_status_effects_display(self):
        return ", ".join(str(effect) for effect in self.status_effects)
        
class Player(Character):
    def __init__(self, name):
        # Initialise player with default stats
        super().__init__(name, hp=100, attack=10, defence=5, accuracy=70, evasion=5, crit_chance=5, crit_damage=0, armour_penetration=0, damage_reduction=0, block_chance=5)
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.base_attack = 10
        self.base_defence = 5
        self.base_accuracy = 70
        self.base_evasion = 5
        self.base_crit_chance = 5
        self.base_crit_damage = 0
        self.base_armour_penetration = 0
        self.base_damage_reduction = 5
        self.base_block_chance = 5
        self.level_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.equipment_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.buff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.combat_buff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.debuff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.weapon_buff_modifiers = {"attack": 0, "accuracy": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "block_chance": 0}
        self.cooldowns = {}
        self.active_buffs = {}
        self.active_hots = {}
        self.combat_buffs = {}
        self.weapon_buff = {'value': 0, 'duration': 0}
        self.weapon_coating = None
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
        self.items = initialise_items()
        self.give_starter_items()
        self.visited_locations = set(["Village"])
        self.kill_tracker = {}
        self.weapon_stamina_cost = {"light": 2, "medium": 4, "heavy": 6}
        self.attack_types = {
            "normal": {"name": "Normal Attack", "stamina_modifier": 0, "damage_modifier": 1},
            "power": {"name": "Power Attack", "stamina_modifier": 3, "damage_modifier": 1.5},
            "quick": {"name": "Quick Attack", "stamina_modifier": 1, "damage_modifier": 0.8, "extra_attacks": 1},
            "stunning": {"name": "Stunning Blow", "stamina_modifier": 2, "damage_modifier": 0.8},
            "defensive": {"name": "Defensive Stance", "stamina_modifier": 2, "damage_modifier": 0, "defence_boost_percentage": 33, "duration": 5},
            "power_stance": {"name": "Power Stance", "stamina_modifier": 2, "damage_modifier": 0, "attack_boost_percentage": 33, "duration": 5},
            "accuracy_stance": {"name": "Accuracy Stance", "stamina_modifier": 2, "damage_modifier": 0, "accuracy_boost_percentage": 33, "duration": 5}
        }
    
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
        self.level_modifiers["attack"] += 1
        self.level_modifiers["defence"] += 1
        self.level_modifiers["accuracy"] += 2
        self.level_modifiers["evasion"] += 0.5
        self.level_modifiers["crit_chance"] += 1
        self.level_modifiers["crit_damage"] += 2
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
            self.level_modifiers["attack"] -= 1
            self.level_modifiers["defence"] -= 1
            self.level_modifiers["accuracy"] -= 2
            self.level_modifiers["evasion"] -= 0.5
            self.level_modifiers["crit_chance"] -= 1
            self.level_modifiers["crit_damage"] -= 2
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
    
    def recalculate_stats(self):
        # Initialize stats with base values
        stats = {
            "attack": self.base_attack,
            "defence": self.base_defence,
            "evasion": self.base_evasion,
            "accuracy": self.base_accuracy,
            "crit_chance": self.base_crit_chance,
            "crit_damage": self.base_crit_damage,
            "damage_reduction": self.base_damage_reduction,
            "armour_penetration": self.base_armour_penetration,
            "block_chance": self.base_block_chance
        }

        # Apply modifiers from various sources
        modifier_sources = [
            self.level_modifiers,
            self.equipment_modifiers,
            self.buff_modifiers,
            self.combat_buff_modifiers,
            self.weapon_buff_modifiers
        ]

        for modifier_dict in modifier_sources:
            for stat in stats:
                if stat in modifier_dict:
                    stats[stat] += modifier_dict[stat]

        # Apply debuffs
        for stat in stats:
            if stat in self.debuff_modifiers:
                stats[stat] = max(0, stats[stat] - self.debuff_modifiers[stat])

        # Update character stats
        self.attack = stats["attack"]
        self.defence = stats["defence"]
        self.evasion = stats["evasion"]
        self.accuracy = stats["accuracy"]
        self.crit_chance = stats["crit_chance"]
        self.crit_damage = stats["crit_damage"]
        self.damage_reduction = stats["damage_reduction"]
        self.armour_penetration = stats["armour_penetration"]
        self.block_chance = stats["block_chance"]

        # Ensure crit_chance and crit_damage stay within reasonable bounds
        self.crit_chance = max(0, min(100, self.crit_chance))
        self.crit_damage = max(100, self.crit_damage)  # Minimum 100% crit damage
    
    def cleanup_after_battle(self):
        for effect in self.status_effects[:]:
            effect.remove(self)
            self.remove_status_effect(effect.name)
        
        self.remove_combat_buffs()
        self.combat_buff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.debuff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.recalculate_stats()
    
    def equip_item(self, item):
    # Equip an item and apply its stats to the appropriate dictionary
        if item.type in self.equipped:
            if self.equipped[item.type]:
                self.unequip_item(item.type)
            self.equipped[item.type] = item
            if item.type == "weapon":
                self.equipment_modifiers["attack"] += getattr(item, "attack", 0)
                self.equipment_modifiers["accuracy"] += getattr(item, "accuracy", 0)
                self.equipment_modifiers["crit_chance"] += getattr(item, "crit_chance", 0)
                self.equipment_modifiers["crit_damage"] += getattr(item, "crit_damage", 0)
                self.equipment_modifiers["armour_penetration"] += getattr(item, "armour_penetration", 0)
                self.equipment_modifiers["block_chance"] += getattr(item, "block_chance", 0)
            elif item.type == "ring":
                self.equipment_modifiers["attack"] += getattr(item, "attack", 0)
                self.equipment_modifiers["crit_chance"] += getattr(item, "crit_chance", 0)
                self.equipment_modifiers["crit_damage"] += getattr(item, "crit_damage", 0)
                self.equipment_modifiers["defence"] += getattr(item, "defence", 0)
                self.equipment_modifiers["evasion"] += getattr(item, "evasion", 0)
                self.equipment_modifiers["damage_reduction"] += getattr(item, "damage_reduction", 0)
                # Add any additional ring stats here if needed
            else:
                self.equipment_modifiers["attack"] += getattr(item, "attack", 0)
                self.equipment_modifiers["defence"] += getattr(item, "defence", 0)
                self.equipment_modifiers["accuracy"] += getattr(item, "accuracy", 0)
                self.equipment_modifiers["crit_chance"] += getattr(item, "crit_chance", 0)
                self.equipment_modifiers["crit_damage"] += getattr(item, "crit_damage", 0)
                self.equipment_modifiers["evasion"] += getattr(item, "evasion", 0)
                self.equipment_modifiers["damage_reduction"] += getattr(item, "damage_reduction", 0)
                self.equipment_modifiers["block_chance"] += getattr(item, "block_chance", 0)
                # Add any additional armour stats here if needed
            self.recalculate_stats()
            if item in self.inventory:
                self.inventory.remove(item)
            print(f"You equipped {item.name}.")
        else:
            print("You can't equip that item.")

    def unequip_item(self, slot):
        # Unequip an item and remove its stats from the appropriate dictionary
        item = self.equipped[slot]
        if item:
            if slot == "weapon":
                self.equipment_modifiers["attack"] -= getattr(item, "attack", 0)
                self.equipment_modifiers["accuracy"] -= getattr(item, "accuracy", 0)
                self.equipment_modifiers["crit_chance"] -= getattr(item, "crit_chance", 0)
                self.equipment_modifiers["crit_damage"] -= getattr(item, "crit_damage", 0)
                self.equipment_modifiers["armour_penetration"] -= getattr(item, "armour_penetration", 0)
                self.equipment_modifiers["block_chance"] -= getattr(item, "block_chance", 0)
            elif item.type == "ring":
                self.equipment_modifiers["attack"] -= getattr(item, "attack", 0)
                self.equipment_modifiers["crit_chance"] -= getattr(item, "crit_chance", 0)
                self.equipment_modifiers["crit_damage"] -= getattr(item, "crit_damage", 0)
                self.equipment_modifiers["defence"] -= getattr(item, "defence", 0)
                self.equipment_modifiers["evasion"] -= getattr(item, "evasion", 0)
                self.equipment_modifiers["damage_reduction"] -= getattr(item, "damage_reduction", 0)
                # Remove any additional ring stats here if needed
            else:
                self.equipment_modifiers["attack"] -= getattr(item, "attack", 0)
                self.equipment_modifiers["defence"] -= getattr(item, "defence", 0)
                self.equipment_modifiers["accuracy"] -= getattr(item, "accuracy", 0)
                self.equipment_modifiers["crit_chance"] -= getattr(item, "crit_chance", 0)
                self.equipment_modifiers["crit_damage"] -= getattr(item, "crit_damage", 0)
                self.equipment_modifiers["evasion"] -= getattr(item, "evasion", 0)
                self.equipment_modifiers["damage_reduction"] -= getattr(item, "damage_reduction", 0)
                self.equipment_modifiers["block_chance"] -= getattr(item, "block_chance", 0)
                # Remove any additional armour stats here if needed
            self.recalculate_stats()
            self.inventory.append(item)
            self.equipped[slot] = None
            print(f"You unequipped {item.name}.")
            
    def apply_buff(self, stat, value, duration, combat_only=True):
        #Applies the buff of a given item, places them in the appropriate area if they are a combat_only item
        if stat == "all stats":
            self.apply_buff("attack", value, duration, combat_only)
            self.apply_buff("defence", value, duration, combat_only)
        else:
            if combat_only:
                self.combat_buff_modifiers[stat] += value
                if stat in self.combat_buffs:
                    self.combat_buffs[stat]['value'] += value
                else:
                    self.combat_buffs[stat] = {'value': value}
            else:
                self.buff_modifiers[stat] += value
                if stat in self.active_buffs:
                    if isinstance(self.active_buffs[stat], dict):
                        self.active_buffs[stat]['value'] += value
                        self.active_buffs[stat]['duration'] = max(self.active_buffs[stat]['duration'], duration)
                    else:
                        self.active_buffs[stat] += value
                else:
                    self.active_buffs[stat] = {'value': value, 'duration': duration} if duration > 0 else value

        self.recalculate_stats()

    def apply_debuff(self, stat, value):
        self.debuff_modifiers[stat] += value
        self.recalculate_stats()

    def remove_debuff(self, stat, value):
        self.debuff_modifiers[stat] -= value
        self.recalculate_stats()
    
    def apply_weapon_buff(self, value, duration):
        self.weapon_buff_modifiers["attack"] += value
        self.weapon_buff = {'value': value, 'duration': duration}
        self.recalculate_stats()
        print(f"Applied a weapon buff of {value} attack for {duration} turns.")
    
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
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Defensive Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
            #print(f"Your Defensive Stance has been refreshed for {attack_info['duration']} turns.")
        else:
            defensive_stance_effect = DEFENSIVE_STANCE(
                attack_info["duration"], 
                attack_info["defence_boost_percentage"]
            )
            self.apply_status_effect(defensive_stance_effect)
            #print(f"You've entered a Defensive Stance for {attack_info['duration']} turns.")
            
    def apply_power_stance(self):
        attack_info = self.attack_types["power_stance"]
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Power Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
            #print(f"Your Power Stance has been refreshed for {attack_info['duration']} turns.")
        else:
            power_stance_effect = POWER_STANCE(
                attack_info["duration"], 
                attack_info["attack_boost_percentage"]
            )
            self.apply_status_effect(power_stance_effect)
            #print(f"You've entered a power Stance for {attack_info['duration']} turns.")
            
    def apply_accuracy_stance(self):
        attack_info = self.attack_types["accuracy_stance"]
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Accuracy Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
            #print(f"Your Accuracy Stance has been refreshed for {attack_info['duration']} turns.")
        else:
            accuracy_stance_effect = ACCURACY_STANCE(
                attack_info["duration"], 
                attack_info["accuracy_boost_percentage"]
            )
            self.apply_status_effect(accuracy_stance_effect)
            #print(f"You've entered a accuracy Stance for {attack_info['duration']} turns.")
    
    def update_buffs(self):
        """
        Updates duration-based buffs and removes expired ones.
        Handles all possible player stats and modifiers.
        """
        # Define all possible stats that can be buffed
        all_stats = [
            "attack", "defence", "accuracy", "evasion", "crit_chance",
            "crit_damage", "armour_penetration", "damage_reduction"
        ]

        # Update regular buffs
        for stat, buff_info in list(self.active_buffs.items()):
            if isinstance(buff_info, dict) and 'duration' in buff_info:
                buff_info['duration'] -= 1
                
                if buff_info['duration'] <= 0:
                    # Handle "all stats" buff
                    if stat == "all stats":
                        for base_stat in ["attack", "defence"]:  # Keep all stats limited to basic stats
                            self.buff_modifiers[base_stat] -= buff_info['value']
                    # Handle individual stat buffs
                    elif stat in all_stats:
                        self.buff_modifiers[stat] -= buff_info['value']
                    
                    del self.active_buffs[stat]
                    # Format the stat name for display
                    display_stat = stat.replace('_', ' ').title()
                    print(f"Your {display_stat} buff has worn off.")

        # Update weapon buff
        if self.weapon_buff['duration'] > 0:
            self.weapon_buff['duration'] -= 1
            if self.weapon_buff['duration'] <= 0:
                self.weapon_buff_modifiers["attack"] -= self.weapon_buff['value']
                print("Your weapon's sharpening effect has worn off")
                self.weapon_buff = {'value': 0, 'duration': 0}
        
        self.recalculate_stats()            
    
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

    def update_weapon_coating(self):
        if self.weapon_coating:
            self.weapon_coating['remaining_duration'] -= 1
            if self.weapon_coating['remaining_duration'] <= 0:
                print(f"\nThe {self.weapon_coating['name']} on your weapon has worn off.")
                self.weapon_coating = None
    
    def remove_combat_buffs(self):
        #Removes any combat related buffs at the end of the battle
        for stat, buff_info in self.combat_buffs.items():
            self.combat_buff_modifiers[stat] -= buff_info['value']
        self.combat_buffs.clear()
        self.recalculate_stats()
        print("Any combat buffs you had have worn off.")
        
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
                    self.apply_weapon_buff(value, item.duration)
                    message += f"You used {item.name} on your {self.equipped['weapon'].name}. Its attack is increased by {value} for {item.duration} turns. "
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
        print("\nInventory:")
        for i, item in enumerate(self.inventory, 1):
            stats = []
            effects = []
            
            # Equipment stats
            if item.attack > 0:
                stats.append(f"Attack: {item.attack}")
            if item.accuracy > 0:
                stats.append(f"Accuracy: {item.accuracy}")
            if item.defence > 0:
                stats.append(f"Defence: {item.defence}")
            if hasattr(item, 'damage_reduction') and item.damage_reduction > 0:
                stats.append(f"DR: {item.damage_reduction}")
            if hasattr(item, 'evasion') and item.evasion > 0:
                stats.append(f"Evasion: {item.evasion}")
            if hasattr(item, 'crit_chance') and item.crit_chance > 0:
                stats.append(f"Crit%: {item.crit_chance}")
            if hasattr(item, 'crit_damage') and item.crit_damage > 0:
                stats.append(f"CritDmg: {item.crit_damage}")
            if hasattr(item, 'block_chance') and item.block_chance > 0:
                stats.append(f"Block%: {item.block_chance}")
            
            # Weapon-specific info
            if item.type == "weapon":
                weapon_type = getattr(item, 'weapon_type', 'light')
                stamina_cost = self.get_weapon_stamina_cost(weapon_type)
                stats.append(f"Stamina: {stamina_cost}")
                stats.append(f"Type: {item.weapon_type.title()}")
            
            # Consumable effects
            if item.type in ["consumable", "food", "drink"]:
                if item.effect_type == "healing":
                    effects.append(f"Heal: {item.effect}")
                elif item.effect_type == "hot":
                    effects.append(f"HoT: {item.tick_effect}/turn for {item.duration} turns")
                elif item.effect_type == "damage":
                    effects.append(f"Damage: {item.effect}")
                elif item.effect_type == "buff":
                    if isinstance(item.effect, tuple):
                        stat, value = item.effect
                        duration = "until end of combat" if item.duration == 0 else f"for {item.duration} turns"
                        effects.append(f"Buff: {stat.capitalize()} +{value} {duration}")
                    else:
                        duration = "until end of combat" if item.duration == 0 else f"for {item.duration} turns"
                        effects.append(f"Buff: Attack +{item.effect} {duration}")
                elif item.effect_type == "weapon_buff":
                    if isinstance(item.effect, tuple):
                        stat, value = item.effect
                        effects.append(f"Weapon Buff: {stat.capitalize()} +{value} for {item.duration} turns")
            
            # Weapon coating
            elif item.type == "weapon coating":
                if isinstance(item.effect, tuple):
                    stack, duration = item.effect
                    effects.append(f"Poison: {stack} stacks for {duration} turns")
            
            stats_str = ", ".join(stats)
            effects_str = ", ".join(effects)
            
            print(f"{i}. {item.name} ", end="")
            if stats_str:
                print(f"({stats_str}) ", end="")
            if effects_str:
                print(f"[{effects_str}] ", end="")
            print(f"(Value: {item.value} gold)")
            
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
        if any(effect.name == "Defensive Stance" for effect in self.status_effects):
            return {"normal": self.attack_types["normal"]}
        if any(effect.name == "Power Stance" for effect in self.status_effects):
            return {"normal": self.attack_types["normal"], "power": self.attack_types["power"]}
        if any(effect.name == "Accuracy Stance" for effect in self.status_effects):
            return {"normal": self.attack_types["normal"], "quick": self.attack_types["quick"], "stunning": self.attack_types["stunning"]}
        return self.attack_types

    def display_attack_options(self):
        print("\nChoose your attack type:")
        available_attacks = self.get_available_attack_types()
        for i, (key, value) in enumerate(available_attacks.items(), 1):
            weapon_type = self.equipped.get("weapon", {"weapon_type": "light"}).weapon_type
            base_stamina_cost = self.get_weapon_stamina_cost(weapon_type)
            total_stamina_cost = base_stamina_cost + value['stamina_modifier']
            print(f"[{i}] {value['name']} (Stamina cost: {total_stamina_cost})")
        
        if any(effect.name == "Defensive Stance" for effect in self.status_effects):
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
        
        

    def print_debug_modifiers(self):
        print("\n=== DEBUG: Player Modifiers ===")
        print(f"Base Attack: {self.base_attack}")
        print(f"Base Defence: {self.base_defence}")
        print(f"Current Attack: {self.attack}")
        print(f"Current Defence: {self.defence}")
        
        print("\nEquipment Modifiers:")
        for stat, value in self.equipment_modifiers.items():
            print(f"  {stat.capitalize()}: {value}")
        
        print("\nBuff Modifiers:")
        for stat, value in self.buff_modifiers.items():
            print(f"  {stat.capitalize()}: {value}")
        
        print("\nCombat Buff Modifiers:")
        for stat, value in self.combat_buff_modifiers.items():
            print(f"  {stat.capitalize()}: {value}")
        
        print("\nWeapon Buff Modifiers:")
        for stat, value in self.weapon_buff_modifiers.items():
            print(f"  {stat.capitalize()}: {value}")
        
        print("\nDebuff Modifiers:")
        for stat, value in self.debuff_modifiers.items():
            print(f"  {stat.capitalize()}: {value}")
        
        print("\nActive Buffs:")
        for stat, buff_info in self.active_buffs.items():
            if isinstance(buff_info, dict):
                print(f"  {stat.capitalize()}: +{buff_info['value']} for {buff_info['duration']} turns")
            else:
                print(f"  {stat.capitalize()}: +{buff_info}")
        
        print("\nCombat Buffs:")
        for stat, buff_info in self.combat_buffs.items():
            print(f"  {stat.capitalize()}: +{buff_info['value']}")
        
        print("\nWeapon Buff:")
        print(f"  Value: {self.weapon_buff['value']}")
        print(f"  Duration: {self.weapon_buff['duration']}")
        
        print("\nStatus Effects:")
        for effect in self.status_effects:
            print(f"  {effect}")