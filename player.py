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
        
    def show_stats(self):
        # Show basic stats
        print(f"\n{self.name} (Level {self.level}):")
        print(f"HP: {self.hp}/{self.max_hp}, Stamina: {self.stamina}/{self.max_stamina}, EXP: {self.exp}/{self.level*100}, Gold: {self.gold}")
        print(f"Att: {self.attack}, Acc: {self.accuracy}, Crit: {self.crit_chance}%, Crit Dmg: {self.crit_damage}%, AP: {self.armour_penetration}")
        print(f"Def: {self.defence}, Eva: {int(self.evasion)}, DR: {self.damage_reduction}, Block: {self.block_chance}%")

        # Show active buffs
        if self.active_buffs or self.combat_buffs:
            # Group buffs by type (offensive, defensive, etc.)
            offensive_buffs = []
            defensive_buffs = []
            utility_buffs = []
            other_buffs = []

            # Process regular buffs
            for stat, buff_info in self.active_buffs.items():
                buff_str = self._format_buff_string(stat, buff_info, False)
                self._categorize_buff(buff_str, stat, offensive_buffs, defensive_buffs, utility_buffs, other_buffs)

            # Process combat buffs
            for stat, buff_info in self.combat_buffs.items():
                buff_str = self._format_buff_string(stat, buff_info, True)
                self._categorize_buff(buff_str, stat, offensive_buffs, defensive_buffs, utility_buffs, other_buffs)

            # Display buffs by category
            if any([offensive_buffs, defensive_buffs, utility_buffs, other_buffs]):
                print("\nActive Buffs:")
                if offensive_buffs:
                    print("  Offensive:")
                    print("   " + "\n   ".join(offensive_buffs))
                if defensive_buffs:
                    print("  Defensive:")
                    print("   " + "\n   ".join(defensive_buffs))
                if utility_buffs:
                    print("  Utility:")
                    print("   " + "\n   ".join(utility_buffs))
                if other_buffs:
                    print("  Other:")
                    print("   " + "\n   ".join(other_buffs))

        # Show weapon buff separately if active
        if self.weapon_buff['duration'] > 0:
            print(f"Weapon Enhancement: +{self.weapon_buff['value']} Attack ({self.weapon_buff['duration']} turns remaining)")

        # Show active HoTs if any
        if self.active_hots:
            print("\nActive Healing Effects:")
            for hot_name, hot_info in self.active_hots.items():
                print(f"  {hot_name}: {hot_info['tick_effect']} HP/turn ({hot_info['duration']} turns remaining)")

    def _format_buff_string(self, stat, buff_info, is_combat_buff=False):
        """Helper method to format buff strings consistently"""
        # Format the stat name
        stat_display = {
            'attack': 'Attack',
            'defence': 'Defense',
            'accuracy': 'Accuracy',
            'evasion': 'Evasion',
            'crit_chance': 'Critical Chance',
            'crit_damage': 'Critical Damage',
            'block_chance': 'Block Chance',
            'damage_reduction': 'Damage Reduction',
            'armour_penetration': 'Armour Penetration',
            'all stats': 'All Stats'
        }.get(stat, stat.replace('_', ' ').title())

        # Format the buff value and duration
        if isinstance(buff_info, dict):
            value = buff_info['value']
            if 'duration' in buff_info:
                return f"{stat_display} +{value} ({buff_info['duration']} turns)"
            else:
                return f"{stat_display} +{value} (Combat)" if is_combat_buff else f"{stat_display} +{value}"
        else:
            return f"{stat_display} +{buff_info} (Combat)" if is_combat_buff else f"{stat_display} +{buff_info}"

    def _categorize_buff(self, buff_str, stat, offensive_buffs, defensive_buffs, utility_buffs, other_buffs):
        """Helper method to categorize buffs"""
        offensive_stats = {'attack', 'crit_chance', 'crit_damage', 'accuracy', 'armour_penetration'}
        defensive_stats = {'defence', 'block_chance', 'damage_reduction', 'evasion'}
        utility_stats = {'all stats'}

        if stat in offensive_stats:
            offensive_buffs.append(buff_str)
        elif stat in defensive_stats:
            defensive_buffs.append(buff_str)
        elif stat in utility_stats:
            utility_buffs.append(buff_str)
        else:
            other_buffs.append(buff_str)
    
    def calculate_damage(self, attacker, defender, attack_type):
        # Calculate hit chance
        hit_chance = max(5, min(95, attacker.accuracy - defender.evasion))
        
        # Check if the attack hits
        if random.randint(1, 100) > hit_chance:
            return 0, "miss", hit_chance, False  # Attack missed
        
        # Check if the attack is blocked, can't block if frozen
        is_frozen = any(effect.name == "Freeze" for effect in defender.status_effects)
        if not is_frozen and random.randint(1, 100) <= defender.block_chance:
            return 0, "blocked", hit_chance, False  # Attack blocked

        attack_info = attacker.attack_types[attack_type]
        base_damage = attacker.attack * attack_info["damage_modifier"]
        random_damage = random.randint(int(base_damage * 0.9), int(base_damage * 1.1))
        
        # Apply armour penetration
        effective_defence = max(0, defender.defence - attacker.armour_penetration)
        
        # Calculate initial damage
        damage = max(0, random_damage - effective_defence)
        
        # Check for critical hit with increased crit chance if target is frozen
        base_crit_chance = attacker.crit_chance
        if is_frozen:
            base_crit_chance += 25 # 25% increased crit chance against frozen targets
        
        is_critical = random.randint(1, 100) <= base_crit_chance
        shattered_freeze = False
        
        if is_critical:
            damage = int(damage * (attacker.crit_damage / 100))
            if is_frozen:
                shattered_freeze = True
                defender.remove_status_effect("Freeze")
        
        # Apply damage reduction
        damage = int(damage * (1 - (defender.damage_reduction / 100)))
        
        # Ensure minimum damage of 1 if the attack hits
        damage = max(1, damage)
        
        return damage, "critical" if is_critical else "normal", hit_chance, shattered_freeze

    def perform_attack(self, target, attack_type):
        attack_info = self.attack_types[attack_type]
        message = f"{self.name} used {attack_info['name']}."
        total_damage = 0
        hits = 1 + attack_info.get("extra_attacks", 0)
        attack_hit = False
        shattered_freeze = False

        for i in range(hits):
            damage, hit_type, hit_chance, freeze_shatter = self.calculate_damage(self, target, attack_type)
            shattered_freeze = shattered_freeze or freeze_shatter
            
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
                    if shattered_freeze:
                        message += "\nThe frozen state shatters with the critical hit!"
                    
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
                if new_effect.name != "Stun" and new_effect.initial_duration > 1:
                    print(f"{self.name}'s {existing_effect.name} is refreshed for {existing_effect.remaining_duration} turns!")
                #print(f"{self.name}'s {existing_effect.name} is refreshed to strength {existing_effect.strength} for {existing_effect.remaining_duration} turns!")
        else:
            self.status_effects.append(new_effect)
            apply_result = new_effect.on_apply(self)
            if apply_result and new_effect.remaining_duration > 1:
                if new_effect.stackable:
                    #print(f"{self.name} is affected by {new_effect.name} with {new_effect.strength} stack(s) for {new_effect.remaining_duration} turns!")
                    pass
                elif new_effect.name != "Stun":
                    if new_effect.initial_duration > 1:
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
        self.buff_modifiers = {"temp_max_hp": 0, "temp_max_stamina": 0, "attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
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
            "berserker_stance": {"name": "Berserker Stance", "stamina_modifier": 4, "damage_modifier": 0, "attack_boost_percentage": 50, "duration": 5},
            "accuracy_stance": {"name": "Accuracy Stance", "stamina_modifier": 2, "damage_modifier": 0, "accuracy_boost_percentage": 33, "duration": 5},
            "evasion_stance": {"name": "Evasion Stance", "stamina_modifier": 2, "damage_modifier": 0, "evasion_boost_percentage": 33, "duration": 5}
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
            effect.on_remove(self)
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
        """
        Applies buff(s) to the player.
        stat: string or list of tuples [(stat, value), ...]
        value: int or None if stat is a list of tuples
        duration: int
        combat_only: boolean
        """
        # Handle "all stats" buff
        if stat == "all stats":
            self.apply_buff("attack", value, duration, combat_only)
            self.apply_buff("defence", value, duration, combat_only)
            self.apply_buff("accuracy", value*3, duration, combat_only)
            self.apply_buff("evasion", value, duration, combat_only)
            return

        # Handle list of stat buffs (for items that buff multiple stats)
        if isinstance(stat, list):
            for stat_tuple in stat:
                sub_stat, sub_value = stat_tuple
                self.apply_single_buff(sub_stat, sub_value, duration, combat_only)
            return

        # Handle single stat buff
        self.apply_single_buff(stat, value, duration, combat_only)

    def apply_single_buff(self, stat, value, duration, combat_only):
        """Helper method to apply a single stat buff"""
        if combat_only:
            if stat not in self.combat_buff_modifiers:
                self.combat_buff_modifiers[stat] = 0
            self.combat_buff_modifiers[stat] += value
            
            if stat in self.combat_buffs:
                self.combat_buffs[stat]['value'] += value
            else:
                self.combat_buffs[stat] = {'value': value}
        else:
            if stat not in self.buff_modifiers:
                self.buff_modifiers[stat] = 0
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
        print(f"Your {stat} has been reduced by {value} until end of next combat.")
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
            
    def apply_berserker_stance(self):
        attack_info = self.attack_types["berserker_stance"]
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Berserker Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
            #print(f"Your Power Stance has been refreshed for {attack_info['duration']} turns.")
        else:
            berserker_stance_effect = BERSERKER_STANCE(
                attack_info["duration"], 
                attack_info["attack_boost_percentage"]
            )
            self.apply_status_effect(berserker_stance_effect)
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
            
    def apply_evasion_stance(self):
        attack_info = self.attack_types["evasion_stance"]
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Evasion Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
        else:
            evasion_stance_effect = EVASION_STANCE(
                attack_info["duration"],
                attack_info["evasion_boost_percentage"]
            )
            self.apply_status_effect(evasion_stance_effect)
            
    def update_buffs(self):
        """
        Updates duration-based buffs and removes expired ones.
        Handles all possible player stats and modifiers.
        """
        # Define all possible stats that can be buffed
        all_stats = [
            "attack", "defence", "accuracy", "evasion", "crit_chance",
            "crit_damage", "armour_penetration", "damage_reduction", "block_chance"
        ]

        # Update regular buffs
        for stat, buff_info in list(self.active_buffs.items()):
            if isinstance(buff_info, dict) and 'duration' in buff_info and stat in all_stats:
                buff_info['duration'] -= 1
                
                if buff_info['duration'] <= 0:
                    # Handle "all stats" buff
                    if stat == "all stats":
                        for base_stat in ["attack", "defence", "evasion"]:  # Keep all stats limited to basic stats
                            self.buff_modifiers[base_stat] -= buff_info['value']
                        self.buff_modifiers["accuracy"] -= buff_info['value' * 5]
                    # Handle individual stat buffs
                    elif stat in all_stats:
                        self.buff_modifiers[stat] -= buff_info['value']
                    
                    del self.active_buffs[stat]
                    # Format the stat name for display
                    display_stat = stat.replace('_', ' ').title()
                    print(f"Your {display_stat} buff has worn off.")

        # Handle temporary max increases
        for stat in ["temp_max_hp", "temp_max_stamina"]:
            if stat in self.active_buffs:
                buff_info = self.active_buffs[stat]
                buff_info['duration'] -= 1
                
                if buff_info['duration'] <= 0:
                    # Remove the temporary boost
                    buff_info['remove_func']()
                    del self.active_buffs[stat]
                    
                    # Format the stat name for display
                    display_stat = "HP" if stat == "temp_max_hp" else "Stamina"
                    print(f"Your temporary maximum {display_stat} increase has worn off.")
        
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
        
    def add_item(self, item):
        """Add an item to inventory, handling stacks"""
        if not item.is_stackable():
            self.inventory.append(item)
            return
            
        # Try to stack with existing items
        for inv_item in self.inventory:
            if inv_item.name == item.name and inv_item.is_stackable():
                # Check if we can add to this stack
                space_in_stack = inv_item.max_stack - inv_item.stack_size
                if space_in_stack > 0:
                    # Add as much as we can to this stack
                    amount_to_add = min(space_in_stack, item.stack_size)
                    inv_item.stack_size += amount_to_add
                    item.stack_size -= amount_to_add
                    
                    # If we've used all of the new item, we're done
                    if item.stack_size == 0:
                        return
                    
        # If we get here, either:
        # 1. No existing stack was found
        # 2. We still have items left after filling existing stacks
        if item.stack_size > 0:
            self.inventory.append(item)
        
    def remove_item(self, item, amount=1):
        """Remove an item from inventory, handling stacks properly"""
        if not item.is_stackable():
            self.inventory.remove(item)
            return item
        
        for inv_item in self.inventory:
            if inv_item.name == item.name:
                if inv_item.stack_size <= amount:
                    self.inventory.remove(inv_item)
                    return inv_item
                else:
                    return inv_item.split_stack(amount)
                
        return None
        
    def use_item(self, item, game=None):
        """Use an item from inventory, handling stacks properly"""
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
                duration = getattr(item, 'duration', 0)
                combat_only = getattr(item, 'combat_only', True)
                
                if isinstance(item.effect, list):  # Handle multiple stat buffs
                    for stat, value in item.effect:
                        self.apply_buff(stat, value, duration, combat_only)
                    message += f"You used {item.name} and gained multiple buffs. "
                else:  # Handle single stat buff
                    stat, value = item.effect if isinstance(item.effect, tuple) else ("all stats", item.effect)
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
                        # Handle stack removal
                        if item.stack_size > 1:
                            item.stack_size -= 1
                        else:
                            self.inventory.remove(item)
                        self.cooldowns[item.name] = item.cooldown
                        return True, f"You applied {item.name} to your weapon. It will apply {item.effect[0]} poison stacks for {item.effect[1]} turns on your next {item.duration} attacks."
                    else:
                        return False, f"You can only apply {item.name} to light weapons. Your current weapon is a {self.equipped['weapon'].weapon_type.title()} Weapon!"
                else:
                    return False, "You don't have a weapon equipped to apply the poison coating."
            
            # Handle stack removal for successful item use
            if item.stack_size > 1:
                item.stack_size -= 1
            else:
                self.inventory.remove(item)
                
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
        """Display inventory with stack sizes"""
        print("\nInventory:")
        
        # Group stackable items
        item_counts = {}
        for item in self.inventory:
            if item.is_stackable():
                if item.name in item_counts:
                    item_counts[item.name]["count"] += item.stack_size
                else:
                    item_counts[item.name] = {
                        "item": item,
                        "count": item.stack_size
                    }
                    
        # Display non-stackable items and stacks
        idx = 1
        for i, item in enumerate(self.inventory, 1):
            if not item.is_stackable():
                self._display_item(idx, item)
                idx += 1
                
        # Display stacked items
        for name, data in item_counts.items():
            if data["count"] > 0:
                self._display_stacked_item(idx, data["item"], data["count"])
                idx += 1
    
    def _display_item(self, idx, item):
        """Helper method to display a single item"""
        stats = []
        effects = []
        if item.attack > 0:
            stats.append(f"Attack: {item.attack}")
        if item.defence > 0:
            stats.append(f"Defence: {item.defence}")
        if item.accuracy > 0:
            stats.append(f"Accuracy: {item.accuracy}")
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
            effect_desc = self.get_effect_description(item)
            if effect_desc:
                effects.append(effect_desc)
            
        stats_str = ", ".join(stats)
        effect_desc = self.get_effect_description(item)
    
        print(f"{idx}. {item.name} ", end="")
        if stats_str:
            print(f"({stats_str}) ", end="")
        if effect_desc:
            print(f"[{effect_desc}] ", end="")
        print(f"(Value: {item.value} gold)")
            
    def _display_stacked_item(self, idx, item, count):
        """Helper method to displa a stacked item"""
        effect_desc = self.get_effect_description(item)
        print(f"{idx}. {item.name} x{count} [{effect_desc}] (Value: {item.value} gold each)")
    
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
            if isinstance(item.effect, list):
                # Handle multiple stat buffs
                buff_effects = []
                for stat, value in item.effect:
                    stat_name = stat.replace('_', ' ').title()
                    if item.duration > 0:
                        buff_effects.append(f"{stat_name} +{value} for {item.duration} turns")
                    else:
                        buff_effects.append(f"{stat_name} +{value}")
                return "Buff: " + ", ".join(buff_effects)
            elif isinstance(item.effect, tuple):
                stat, value = item.effect
                stat_name = stat.replace('_', ' ').title()
                if item.duration > 0:
                    if item.stamina_restore > 0:
                        return f"Buff: {stat_name} +{value} for {item.duration} turns and restores {item.stamina_restore} stamina"
                    else:
                        return f"Buff: {stat_name} +{value} for {item.duration} turns"
                else:
                    return f"Buff: {stat_name} +{value} until combat ends"
            else:
                return f"Buff: Attack +{item.effect}"
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
        # Get the current weapon_type
        equipped_weapon = self.equipped.get("weapon")
        weapon_type = equipped_weapon.weapon_type
        
        if any(effect.name == "Defensive Stance" for effect in self.status_effects):
            return {"normal": self.attack_types["normal"]}
        if any(effect.name == "Power Stance" for effect in self.status_effects):
            return {"normal": self.attack_types["normal"], "power": self.attack_types["power"]}
        if any(effect.name == "Berserker Stance" for effect in self.status_effects):
            return {"normal": self.attack_types["normal"], "power": self.attack_types["power"]}
        if any(effect.name == "Accuracy Stance" for effect in self.status_effects):
            return {"normal": self.attack_types["normal"], "quick": self.attack_types["quick"], "stunning": self.attack_types["stunning"]}
        if any(effect.name == "Evasion Stance" for effect in self.status_effects):
            return{"normal": self.attack_types["normal"], "quick": self.attack_types["quick"]}
        
        if weapon_type == "light":
            available_attacks = {
                "normal": self.attack_types["normal"],
                "quick": self.attack_types["quick"],
                "accuracy_stance": self.attack_types["accuracy_stance"],
                "evasion_stance": self.attack_types["evasion_stance"]
            }
            return available_attacks
        elif weapon_type == "medium":
            available_attacks = {
                "normal": self.attack_types["normal"],
                "power": self.attack_types["power"],
                "stunning": self.attack_types["stunning"],
                "defensive": self.attack_types["defensive"],
                "power_stance": self.attack_types["power_stance"]
            }
            return available_attacks
        elif weapon_type == "heavy":
            available_attacks = {
                "normal": self.attack_types["normal"],
                "power": self.attack_types["power"],
                "stunning": self.attack_types["stunning"],
                "defensive": self.attack_types["defensive"],
                "power_stance": self.attack_types["power_stance"],
                "berserker_stance": self.attack_types["berserker_stance"]
            }
            return available_attacks
        
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