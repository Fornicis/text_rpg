import pygame
import random, time
from items import Item, initialise_items, SoulCrystal
from display import Display, ItemUseDisplay, InventoryDisplay, BattleDisplay
from game_config import VARIANT_TYPES
from status_effects import *

PLAYER_ATTACK_TYPES = {
    "normal": {
        "name": "Normal Attack",
        "stamina_modifier": 0,
        "damage_modifier": 1,
        "effect": None
    },
    "power": {
        "name": "Power Attack",
        "stamina_modifier": 3,
        "damage_modifier": 1.5,
        "effect": None
    },
    "quick": {
        "name": "Quick Attack",
        "stamina_modifier": 1,
        "damage_modifier": 0.8,
        "extra_attacks": 1,
        "effect": None
    },
    "stunning": {
        "name": "Stunning Blow",
        "stamina_modifier": 2,
        "damage_modifier": 0.8,
        "effect": "stun"
    },
    "triple": {
        "name": "Triple Strike",
        "stamina_modifier": 4,
        "damage_modifier": 0.9,
        "extra_attacks": 2,
        "effect": "self_damage"
    },
    "reckless": {
        "name": "Reckless Attack",
        "stamina_modifier": 5,
        "damage_modifier": 2.0,
        "effect": "self_damage"
    },
    "precision": {
        "name": "Precision Strike",
        "stamina_modifier": 3,
        "damage_modifier": 1.2,
        "stat_buffs": {
            "accuracy": 30,
            "crit_chance": 20
        }
    },
    "flurry": {
        "name": "Flurry of Blows",
        "stamina_modifier": 6,
        "damage_modifier": 0.6,
        "extra_attacks": 4
    },
    "sweep": {
        "name": "Sweeping Strike",
        "stamina_modifier": 4,
        "damage_modifier": 1.3,
        "stat_buffs": {
            "defence": 15
        }
    },
    "balanced": {
        "name": "Balanced Strike",
        "stamina_modifier": 3,
        "damage_modifier": 1.1,
        "stat_buffs": {
            "accuracy": 15,
            "block_chance": 15
        }
    },
    "crushing": {
        "name": "Crushing Blow",
        "stamina_modifier": 5,
        "damage_modifier": 1.6,
        "effect": "defence_break"
    },
    "cleave": {
        "name": "Mighty Cleave",
        "stamina_modifier": 7,
        "damage_modifier": 1.8,
        "stat_buffs": {
            "armour_penetration": 30
        },
        "effect": "self_damage"
    },
    # Stance attacks
    "defensive_stance": {
        "name": "Defensive Stance",
        "stamina_modifier": 2,
        "damage_modifier": 0,
        "duration": 5,
        "stance_type": "defensive",
        "defence_boost_percentage": 33
    },
    "power_stance": {
        "name": "Power Stance",
        "stamina_modifier": 2,
        "damage_modifier": 0,
        "duration": 5,
        "stance_type": "power",
        "attack_boost_percentage": 33
    },
    "berserker_stance": {
        "name": "Berserker Stance",
        "stamina_modifier": 4,
        "damage_modifier": 0,
        "duration": 5,
        "stance_type": "berserker",
        "attack_boost_percentage": 50
    },
    "accuracy_stance": {
        "name": "Accuracy Stance",
        "stamina_modifier": 2,
        "damage_modifier": 0,
        "duration": 5,
        "stance_type": "accuracy",
        "accuracy_boost_percentage": 33
    },
    "evasion_stance": {
        "name": "Evasion Stance",
        "stamina_modifier": 2,
        "damage_modifier": 0,
        "duration": 5,
        "stance_type": "evasion",
        "evasion_boost_percentage": 33
    }
}

# Define weapon type attack availability
WEAPON_ATTACK_TYPES = {
    "light": [
        "normal", "quick", "triple", "precision", 
        "flurry", "accuracy_stance", "evasion_stance"
    ],
    "medium": [
        "normal", "power", "stunning", "reckless", "sweep",
        "balanced", "defensive_stance", "power_stance"
    ],
    "heavy": [
        "normal", "power", "stunning", "reckless", "crushing",
        "cleave", "defensive_stance", "power_stance", "berserker_stance"
    ],
    "soulbound": [
        "normal", "quick", "triple", "precision", "flurry",
        "power", "reckless", "stunning", "crushing", "sweep", "cleave", "balanced", "defensive_stance",
        "power_stance", "berserker_stance", "accuracy_stance", "evasion_stance"
    ]
}

class Character:
    def __init__(self, name, hp, attack, defence, accuracy=70, evasion=5, crit_chance=5, crit_damage=150, armour_penetration=0, damage_reduction=0, block_chance=0):
        # Initialize basic character attributes
        self.name = name
        self.hp = hp
        self._prev_hp = hp
        self.max_hp = hp
        self.attack_types = {
            "normal": {"name": "Normal Attack", "stamina_modifier": 0, "damage_modifier": 1},
        }
        # Base stats
        self.base_attack = attack
        self.base_defence = defence
        self.base_accuracy = accuracy
        self.base_evasion = evasion
        self.base_crit_chance = crit_chance
        self.base_crit_damage = crit_damage
        self.base_armour_penetration = armour_penetration
        self.base_damage_reduction = damage_reduction
        self.base_block_chance = block_chance
        # Current stats (will be calculated)
        self.attack = attack
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
        self.display = Display()
        self.pause = Display.pause
        self.title_screen = Display.display_title
        self.battle_display = BattleDisplay(self.display)
        self.buff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, 
                              "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, 
                              "damage_reduction": 0, "block_chance": 0}
        self.combat_buff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, 
                                     "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, 
                                     "damage_reduction": 0, "block_chance": 0}
        self.debuff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, 
                                "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, 
                                "damage_reduction": 0, "block_chance": 0}
        
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
                
        # Add soul crystal effects display
        if self.soul_crystal_effects:
            print("\nSoul Crystal Effects:")
            self.show_soul_crystal_effects()

    def _format_buff_string(self, stat, buff_info, is_combat_buff=False):
        """Helper method to format buff strings consistently"""
        # Format the stat name
        stat_display = {
            'attack': 'Attack',
            'defence': 'Defence',
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
    
    def apply_special_effects(self, attacker, defender):
        """Apply any special combat modifiers based on the target"""
        modifiers = {}
        
        # Check soul crystal effects for relevant effects
        if hasattr(attacker, 'soul_crystal_effects') and attacker.soul_crystal_effects:
            for effect_name, effect_data in attacker.soul_crystal_effects.items():
                # Boss resonance
                if effect_name == "boss_resonance":
                # Check if the defender's soultype is "boss"
                    soultype = defender.soultype
                    if soultype == "boss":
                        for stat, value in effect_data.items():
                            if stat != "target" and stat != "combats_remaining":
                                modifiers[stat] = modifiers.get(stat, 0) + value
                            
                # Variant affinity
                if effect_name == "variant_affinity":
                    # Get the first word of the defender's name as the variant type
                    defender_name_parts = defender.name.split()
                    if len(defender_name_parts) > 1:
                        variant_type = defender_name_parts[0]
                        target_variant = effect_data.get("target")
                        
                        if variant_type == target_variant:
                            # print(f"Applying variant affinity against {variant_type} monster") # Debug
                            for stat, value in effect_data.items():
                                if stat != "target" and stat != "combats_remaining":
                                    modifiers[stat] = modifiers.get(stat, 0) + value
                                
                # Soul echo
                if effect_name == "soul_echo":
                    target = effect_data.get("target", "").lower()
                    if hasattr(defender, 'monster_type') and defender.monster_type.lower() == target:
                        modifiers["damage_multiplier"] = 1 + (effect_data["damage_multiplier"] / 100)
                        # print(f"Soul Echo active! Adding damage multiplier: {modifiers['damage_multiplier']}") Debug Print
        
        """if modifiers:
            print(f"Applied special effects modifiers: {modifiers}")""" # Debug Print
        
        return modifiers
    
    def calculate_damage(self, attacker, defender, attack_type):
        from enemies import ENEMY_ATTACK_TYPES
        # Get attack info based on attacker type
        if isinstance(attacker, Player):
            attack_info = PLAYER_ATTACK_TYPES[attack_type]
            damage_modifier = attack_info["damage_modifier"]
        else:
            attack_info = ENEMY_ATTACK_TYPES[attack_type]
            damage_modifier = attack_info["damage_modifier"]
        # Get any special effects that apply to this combat
        soul_crystal_modifiers = self.apply_special_effects(attacker, defender)
        # print(f"Soul crystal modifiers: {soul_crystal_modifiers}") Debug print
        # Calculate hit chance with modifiers
        hit_chance = max(5, min(95, attacker.accuracy + getattr(soul_crystal_modifiers, "accuracy", 0) - (defender.evasion + getattr(soul_crystal_modifiers, "evasion", 0))))
        
        # Check if the attack hits
        if random.randint(1, 100) > hit_chance:
            return 0, "miss", hit_chance, False  # Attack missed
        
        # Check for block
        if not defender.stunned and random.randint(1, 100) <= (defender.block_chance + getattr(soul_crystal_modifiers, "block_chance", 0)):
            return 0, "blocked", hit_chance, False  # Attack blocked

        # Calculate base damage
        base_damage = (attacker.attack + getattr(soul_crystal_modifiers, "attack", 0)) * damage_modifier
        # print(f"Base Damage: {base_damage}") Debug Print
        random_damage = random.randint(int(base_damage * 0.9), int(base_damage * 1.1))
        # print(f"Random Damage: {random_damage}") Debug Print
        
        # Apply armour penetration
        effective_defence = max(0, (defender.defence + getattr(soul_crystal_modifiers, "defence", 0)) - (attacker.armour_penetration + getattr(soul_crystal_modifiers, "armour_penetration", 0)))
        
        # Calculate initial damage
        damage = max(0, random_damage - effective_defence)
        # print(f"Initial damage (random damage - effective defence): {damage}") Debug Print
        # Check for critical hit
        base_crit_chance = attacker.crit_chance + getattr(soul_crystal_modifiers, "crit_chance", 0)
        if defender.stunned:
            base_crit_chance += 25  # 25% increased crit chance against stunned targets
            
        is_critical = random.randint(1, 100) <= base_crit_chance
        shattered_stun = False
        
        if is_critical:
            damage = int(damage * ((attacker.crit_damage + getattr(soul_crystal_modifiers, "crit_damage", 0)) / 100))
            if defender.stunned:
                shattered_stun = True
                defender.stunned = False
        
        # Apply damage multiplier from soul echo if present
        if "damage_multiplier" in soul_crystal_modifiers:
            print(f"Before damage multiplier: {damage}")
            # print(f"Applying multiplier: {soul_crystal_modifiers['damage_multiplier']}") Debug Print
            damage = int(damage * soul_crystal_modifiers["damage_multiplier"])
            # print(f"After damage multiplier: {damage}") Debug Print
        # Apply damage reduction
        # print(f"{(1 - ((defender.damage_reduction + getattr(soul_crystal_modifiers, 'damage_reduction', 0)) / 100))}") Debug Print
        damage = int(damage * (1 - ((defender.damage_reduction + getattr(soul_crystal_modifiers, "damage_reduction", 0)) / 100)))
        # print(f"Damage after damage reduction: {damage}") Debug Print
        # Ensure minimum damage of 1 if the attack hits
        damage = max(1, damage)
        
        return damage, "critical" if is_critical else "normal", hit_chance, shattered_stun

    def perform_attack(self, target, attack_type):
        from enemies import ENEMY_ATTACK_TYPES
        # Check to see who is attacking
        if isinstance(self, Player):
            attack_info = PLAYER_ATTACK_TYPES[attack_type]
            self.battle_display.display_attack_animation(self.name, attack_info['name'])
        else:  # Enemy attacker
            attack_info = ENEMY_ATTACK_TYPES[attack_type]
            self.battle_display.display_attack_animation(self.name, attack_info['name'], is_player=False)
        message = f"{self.name} used {attack_info['name']}."
        total_damage = 0
        hits = 1 + attack_info.get("extra_attacks", 0)
        attack_hit = False
        shattered_freeze = False
        successful_hits = 0 # Track successful hits for weapon_coating effects
        
        # Apply attack-specific buffs before damage calculation (player only)
        if isinstance(self, Player) and 'stat_buffs' in attack_info:
            self.apply_attack_buffs(attack_info['stat_buffs'])

        for i in range(hits):
            damage, hit_type, hit_chance, freeze_shatter = self.calculate_damage(self, target, attack_type)
            shattered_freeze = shattered_freeze or freeze_shatter
            
            # Display hit animation and damage
            self.battle_display.display_damage_numbers(target, damage, hit_type, isinstance(self, Player))
            
            # Handle self_damage display
            if attack_info.get('effect') == 'self_damage':
                self_damage = int(damage * 0.2)  # 20% of the damage dealt
                self.battle_display.display_damage_numbers(self, self_damage, "self_damage", isinstance(self, Player), True)
            
            if hit_type == "miss":
                message += f"\n{self.name}'s attack missed {target.name}!"
            elif hit_type == "blocked":
                message += f"\n{self.name}'s attack was blocked by {target.name}!"
            else:
                attack_hit = True
                target.take_damage(damage)
                total_damage += damage
                if damage > 0:
                    successful_hits += 1 # Increment by 1 on successful hit
                if i == 0:
                    message += f"\n{self.name} dealt {damage} damage to {target.name}!"
                else:
                    message += f"\n{self.name} dealt an additional {damage} damage to {target.name}!"
                
                if hit_type == "critical":
                    message += " Critical hit!"
                    shattered_freeze = True
                    if "Freeze" in [effect.name for effect in target.status_effects] and shattered_freeze:
                        target.remove_status_effect("Freeze")
                        message += "\nThe frozen state shatters with the critical hit!"
                
                if attack_info.get('effect') == 'self_damage':
                    # Create red flash for self damage
                    self_damage = int(damage * 0.2)
                    layout = self.battle_display.layout['battle_panel']
                    width, height, x, y = layout
                    original_surface = self.battle_display.display.screen.copy()
                    flash_surface = pygame.Surface((width, height))
                    flash_surface.fill((255, 0, 0))
                    
                    for _ in range(3):
                        # Show flash
                        for alpha in range(0, 128, 32): # Fade in
                            flash_surface.set_alpha(alpha)
                            self.battle_display.display.screen.blit(original_surface, (0, 0))
                            self.battle_display.display.screen.blit(flash_surface, (x, y))
                            self.display.draw_text(f"{self.name} takes {self_damage} damage as recoil from their {attack_info['name']} attack!", 
                                                   (x + width // 2, y + height // 5), 'large', 'white', center=True)
                            pygame.display.flip()
                            pygame.time.wait(100)
                            
                        for alpha in range(128, 0, -32): # Fade out
                            flash_surface.set_alpha(alpha)
                            self.battle_display.display.screen.blit(original_surface, (0, 0))
                            self.battle_display.display.screen.blit(flash_surface, (x, y))
                            self.display.draw_text(f"{self.name} takes {self_damage} damage as recoil from their {attack_info['name']} attack!", 
                                                   (x + width // 2, y + height // 5), 'large', 'white', center=True)
                            pygame.display.flip()
                            pygame.time.wait(100)
                        
                        self.battle_display.display.screen.blit(original_surface, (0, 0))
                        pygame.display.flip()
                    
        if total_damage > 0 and hits > 1:
            message += f"\nTotal damage dealt: {total_damage}"

        #self.battle_display.display_attack_animation(self.name, attack_info['name'])
        
        #print(message.rstrip())
                
        if isinstance(self, Player) and self.weapon_coating and successful_hits > 0:
            total_stacks = self.weapon_coating['stacks'] * successful_hits
            message += f"\n{target.name} is poisoned by your coated weapon!"
            message += f"\n({successful_hits} hits, {total_stacks} total poison stacks)"
            poison_effect = POISON(
                duration=self.weapon_coating['duration'],
                strength= total_stacks
            )
            target.apply_status_effect(poison_effect)
        
        if isinstance(self, Player) and successful_hits > 0:
            self.update_weapon_buff()
        
        self.remove_status_effect("Freeze")
        
        # Remove attack-specific buffs after damage calculation (player only)
        if isinstance(self, Player) and 'stat_buffs' in attack_info:
            self.remove_attack_buffs(attack_info['stat_buffs'])

        return message, total_damage, None, attack_hit

    def is_alive(self):
        # Check if character is still alive
        return self.hp > 0

    def take_damage(self, damage):
        # Reduce HP when taking damage, minimum 0
        self._prev_hp = self.hp
        self.hp = max(0, self.hp - int(damage))

    def heal(self, amount):
        # Heal character, not exceeding max HP
        self.hp = min(self.max_hp, self.hp + int(amount))
    
    def apply_status_effect(self, new_effect):
        #print("Battle display object:", self.battle_display)
        #print("Trying to draw message")
        existing_effect = next((e for e in self.status_effects if e.name == new_effect.name), None)
        
        if existing_effect:
            #print(f"DEBUG: Updating existing effect: {existing_effect.name}")
            
            # Handle DoT effects
            if isinstance(new_effect, DotEffect):
                existing_effect.strength += new_effect.strength
                existing_effect.remaining_duration = max(existing_effect.remaining_duration, new_effect.initial_duration)
                self.battle_display.draw_battle_message(f"\n{self.name}'s {existing_effect.name} is intensified to {existing_effect.strength} stacks!")
                return True
                
            # Handle stat-based effects
            if hasattr(new_effect, 'stat_changes'):
                for stat, value in new_effect.stat_changes.items():
                    if hasattr(existing_effect, 'total_reductions'):
                        existing_effect.total_reductions[stat] = existing_effect.total_reductions.get(stat, 0) + value
                        
                        if new_effect.is_debuff:
                            self.debuff_modifiers[stat] = 0
                            self.debuff_modifiers[stat] = existing_effect.total_reductions[stat]
                            self.battle_display.draw_battle_message(f"\n{self.name}'s {stat.replace('_', ' ').title()} is reduced by an additional {value}!")
                            
                existing_effect.remaining_duration = max(existing_effect.remaining_duration, new_effect.initial_duration)
                self.recalculate_stats()
            return True

        else:
            """if hasattr(new_effect, 'total_reductions'):
                print(f"DEBUG: New total reductions: {new_effect.total_reductions}")"""
            apply_result = new_effect.on_apply(self)
            #print(f"DEBUG: Apply result: {apply_result}")
            if apply_result:
                self.status_effects.append(new_effect)
                #print(f"DEBUG: Status effect added: {new_effect.name}")
                self.battle_display.display_status_effects(self, new_effect.name)
                return True

        return True

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
    
    def apply_buff(self, stat, value, duration=0, combat_only=True):
        """Apply a buff to a stat"""
        if stat in self.buff_modifiers:
            self.buff_modifiers[stat] += value
            self.recalculate_stats()

    def remove_buff(self, stat, value):
        """Remove a buff from a stat"""
        if stat in self.buff_modifiers:
            self.buff_modifiers[stat] = max(0, self.buff_modifiers[stat] - value)
            self.recalculate_stats()

    def apply_debuff(self, stat, value):
        """Apply a debuff to a stat"""
        if stat in self.debuff_modifiers:
            self.debuff_modifiers[stat] = value
            self.recalculate_stats()

    def remove_debuff(self, stat, value):
        """Remove a debuff from a stat"""
        if stat in self.debuff_modifiers:
            self.debuff_modifiers[stat] = max(0, self.debuff_modifiers[stat] - value)
            self.recalculate_stats()
            
    def apply_attack_buffs(self, stat_buffs):
        """Apply temporary stat buffs from an attack"""
        for stat, value in stat_buffs.items():
            self.combat_buff_modifiers[stat] += value
            #print(stat_buffs.items(), stat_buffs.values()) Debug Print
        self.recalculate_stats()

    def remove_attack_buffs(self, stat_buffs):
        """Remove temporary stat buffs after an attack"""
        for stat, value in stat_buffs.items():
            self.combat_buff_modifiers[stat] -= value
            #print(stat_buffs.items(), stat_buffs.values()) Debug Print
        self.recalculate_stats()

    def recalculate_stats(self):
        # Initialize with base values
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

        # Apply all modifiers
        for stat in stats:
            # Add buffs and combat buffs
            stats[stat] += self.buff_modifiers.get(stat, 0)
            stats[stat] += self.combat_buff_modifiers.get(stat, 0)
            # Subtract debuffs
            stats[stat] = max(0, stats[stat] - self.debuff_modifiers.get(stat, 0))

        # Update current stats with calculated values
        for stat, value in stats.items():
            if stat == "crit_damage":
                value = max(100, value)
            elif stat in ["damage_reduction", "armour_penetration", "block_chance"]:
                value = max(0, value)
            else:
                value = max(1, value)
            setattr(self, stat, value)
        
class Player(Character):
    def __init__(self, name):
        # Initialise player with default stats
        super().__init__(name, hp=100, attack=10, defence=5, accuracy=70, evasion=5, crit_chance=5, crit_damage=0, armour_penetration=0, damage_reduction=0, block_chance=5)
        self.days = 1
        self.level = 1
        self.inventory = []
        self.max_stamina = 100
        self.stamina = self.max_stamina
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
        self.respawn_counter = 5
        self.visited_locations = set(["Village"])
        self.level_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.equipment_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.buff_modifiers = {"temp_max_hp": 0, "temp_max_stamina": 0, "attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.combat_buff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.debuff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.weapon_buff_modifiers = {'attack': 0, 'accuracy': 0, 'crit_chance': 0, 'crit_damage': 0, 'armour_penetration': 0, 'block_chance': 0}
        self.cooldowns = {}
        self.active_buffs = {}
        self.active_hots = {}
        self.combat_buffs = {}
        self.active_debuffs = {}
        self.weapon_buff = {'value': 0, 'duration': 0}
        self.soul_crystal_effects = {}
        self.weapon_coating = None
        self.kill_tracker = {}
        self.variant_kill_tracker = {}
        self.boss_kill_tracker = {}
        self.used_kill_tracker = {}
        self.used_variant_tracker = {}
        self.used_boss_kill_tracker = {}
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
        #self.give_starter_items()
        
    def give_starter_items(self):
        starter_items = [
            "Wooden Sword",
            "Peasants Top", 
            "Peasants Bottoms",
            "Minor Health Potion",
            "Small Bomb",
            "Quick Warrior's Drop",
            "Basic Sharpening Stone"
        ]
        
        # Clear screen and setup
        self.display.screen.fill('black')
        self.display.draw_text("=== STARTER ITEMS ===", 
                            (self.display.config.SCREEN_WIDTH // 2, 50), 
                            'title', center=True)
        
        # Display items one by one with animation
        for i, item_name in enumerate(starter_items):
            item = self.items[item_name]
            self.inventory.append(item)
            
            # Calculate position
            y_pos = 150 + (i * 40)
            
            # Draw item name and type
            self.display.draw_text(f"{item.name} [{item.type.title()}]",
                                (self.display.config.SCREEN_WIDTH // 2, y_pos),
                                'large', center=True)
            
            # Auto-equip if equipment
            if item.type in ["weapon", "helm", "chest", "waist", "legs", "boots", "gloves", "shield", "back", "ring"]:
                self.equip_item(item)
                self.display.draw_text("(Auto-equipped)",
                                    (self.display.config.SCREEN_WIDTH // 2 + 200, y_pos),
                                    'medium', colour='green', center=True)
            
            pygame.display.flip()
            pygame.time.wait(500)  # Delay between items
        
        # Show completion message
        self.display.draw_text("Press ENTER to continue...",
                            (self.display.config.SCREEN_WIDTH // 2, y_pos + 80),
                            'medium', center=True)
        pygame.display.flip()
        
        # Wait for ENTER
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    return
        
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
            #Reduce exp by 20% for every level above enemy level, minimum 10%
            scaling_factor = max(0.1, 1 - (level_difference * 0.2))
        #Applies scaling factor    
        scaled_exp = int(amount * scaling_factor)
        #Gain exp based on scaled exp
        self.exp += scaled_exp
        self.battle_display.draw_battle_message(f"You gained {scaled_exp} experience!")
        #Check for level up
        if self.exp >= self.level * 100:
            self.level_up()
    
    def level_up(self):
        # Capture previous stats for comparison
        old_stats = {
            'max_hp': self.max_hp,
            'attack': self.attack,
            'defence': self.defence,
            'accuracy': self.accuracy,
            'evasion': self.evasion,
            'crit_chance': self.crit_chance,
            'crit_damage': self.crit_damage,
            'armour_penetration': self.armour_penetration,
            'damage_reduction': self.damage_reduction,
            'block_chance': self.block_chance,
            'max_stamina': self.max_stamina
        }
        
        # Increase player stats on level up
        self.level += 1
        max_hp = random.randint(40, 60)
        self.max_hp += max_hp
        self.hp = self.max_hp
        attack = random.randint(2, 5)
        self.level_modifiers["attack"] += attack
        defence = random.randint(1, 4)
        self.level_modifiers["defence"] += defence
        accuracy = random.randint(2, 4)
        self.level_modifiers["accuracy"] += accuracy
        evasion = round(random.uniform(0.5, 1.5), 1)
        self.level_modifiers["evasion"] += evasion
        crit_chance = random.randint(1, 2)
        self.level_modifiers["crit_chance"] += crit_chance
        crit_damage = random.randint(2, 4)
        self.level_modifiers["crit_damage"] += crit_damage
        armour_penetration = 1
        self.level_modifiers["armour_penetration"] += armour_penetration
        damage_reduction = 1
        self.level_modifiers["damage_reduction"] += damage_reduction
        block_chance = round(random.uniform(0.5, 1.5), 1)
        self.level_modifiers["block_chance"] += block_chance
        self.max_stamina += 10
        stamina_restore = self.max_stamina // 4
        self.restore_stamina(stamina_restore)
        
        # Update equipment stats and remaining exp
        self.update_equipment_stats()
        self.exp = self.exp // 4
        self.recalculate_stats()
        
        # Get layout of main panel
        layout = self.display.calculate_layout()
        main_panel = layout['battle_panel']
        width, height, x, y = main_panel
        
        base_y = y
        
        # Create overlay for main panel
        overlay = pygame.Surface((width, height))
        overlay.fill(('black'))
        overlay.set_alpha(200)
        
        # Draw overlay
        self.display.screen.blit(overlay, (x, base_y))
        
        # Display level up message
        self.display.draw_text(" === LEVEL UP ===",
                               (x + width // 2, base_y + 50),
                               'title', 'gold', center=True)
        
        base_y += 100
        
        self.display.draw_text(f"You have reached level {self.level}!",
                               (x + width // 2, base_y),
                               'large', 'white', center=True)
        
        base_y += 50
        
        stat_changes = [
            (f"Max HP: {old_stats['max_hp']} -> {self.max_hp}", max_hp),
            (f"Attack: {old_stats['attack']} -> {self.attack}", attack),
            (f"Accuracy: {old_stats['accuracy']} -> {self.accuracy}", accuracy),
            (f"Armour Penetration: {old_stats['armour_penetration']} -> {self.armour_penetration}", armour_penetration),
            (f"Crit Chance: {old_stats['crit_chance']} -> {self.crit_chance}", crit_chance),
            (f"Crit Damage: {old_stats['crit_damage']} -> {self.crit_damage}", crit_damage),
            (f"Defence: {old_stats['defence']} -> {self.defence}", defence),
            (f"Evasion: {old_stats['evasion']} -> {self.evasion}", evasion),
            (f"Block Chance: {old_stats['block_chance']} -> {self.block_chance}", block_chance),
            (f"Damage Reduction: {old_stats['damage_reduction']} -> {self.damage_reduction}", damage_reduction),
            (f"Max Stamina: {old_stats['max_stamina']} -> {self.max_stamina}", 10)
        ]
        
        for stat_text, increase in stat_changes:
            self.display.draw_text(stat_text + f" (+{increase})",
                                   (x + width // 2, base_y),
                                   'medium', 'green', center=True)
            base_y += 30
            
        # Display continue prompt
        self.display.draw_text("Press ENTER to continue",
                               (x + width // 2, base_y),
                               'medium', 'white', center=True)
        
        pygame.display.flip()
        self.display.pause(show_prompt=False)
        
        """self.battle_display.draw_battle_message(f"Congratulations! You reached level {self.level}!")
        self.battle_display.draw_battle_message(f"Your stats have increased:\nAttack: +{attack}\nDefence: +{defence}\nEvasion: +{evasion}\nAccuracy: +{accuracy}\nCrit Chance: +{crit_chance}%\nCrit Damage: +{crit_damage}%\nArmour Pentration: +{armour_penetration}\nDamage Reduction: +{damage_reduction}\nBlock Chance: +{block_chance}%")"""
    
    def lose_level(self):
        if self.level <= 1:
            # Display level 1 message
            layout = self.display.calculate_layout()
            main_panel = layout['main_panel']
            width, height, x, y = main_panel
            
            overlay = pygame.Surface((width, height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(200)
            self.display.screen.blit(overlay, (x, y))
            
            self.display.draw_text("=== DIVINE PROTECTION ===",
                                (x + width // 2, y + height // 2 - 30),
                                'title', 'gold', center=True)
            self.display.draw_text("You're only level 1. The deities protect you from losing any power.",
                                (x + width // 2, y + height // 2 + 30),
                                'large', 'white', center=True)
            
            pygame.display.flip()
            self.display.pause()
            return
            
        # Capture previous stats
        old_stats = {
            "level": self.level,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defence": self.defence,
            "accuracy": self.accuracy,
            "evasion": self.evasion,
            "crit_chance": self.crit_chance,
            "crit_damage": self.crit_damage,
            "armour_penetration": self.armour_penetration,
            "damage_reduction": self.damage_reduction,
            "block_chance": self.block_chance,
            "max_stamina": self.max_stamina
        }
        
        # Perform stat decreases
        self.level -= 1
        max_hp = random.randint(40, 60)
        self.max_hp -= max_hp
        self.hp = self.max_hp
        attack = random.randint(2, 5)
        self.level_modifiers["attack"] -= attack
        defence = random.randint(1, 4)
        self.level_modifiers["defence"] -= defence
        accuracy = random.randint(2, 6)
        self.level_modifiers["accuracy"] -= accuracy
        evasion = round(random.uniform(0.5, 1.5), 1)
        self.level_modifiers["evasion"] -= evasion
        crit_chance = random.randint(1, 3)
        self.level_modifiers["crit_chance"] -= crit_chance
        crit_damage = random.randint(2, 6)
        self.level_modifiers["crit_damage"] -= crit_damage
        armour_penetration = random.randint(1, 3)
        self.level_modifiers["armour_penetration"] -= armour_penetration
        damage_reduction = random.randint(1, 2)
        self.level_modifiers["damage_reduction"] -= damage_reduction
        block_chance = round(random.uniform(0.5, 1.5), 1)
        self.level_modifiers["block_chance"] -= block_chance
        self.max_stamina -= 10
        
        # Update stats
        self.update_equipment_stats()
        self.recalculate_stats()
        
        # Display level loss information
        layout = self.display.calculate_layout()
        main_panel = layout['battle_panel']
        width, height, x, y = main_panel
        
        # Create overlay
        overlay = pygame.Surface((width, height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        
        # Draw overlay
        self.display.screen.blit(overlay, (x, y))
        
        # Display level loss message
        self.display.draw_text("=== LEVEL LOST ===",
                            (x + width // 2, y + 50),
                            'title', 'red', center=True)
        self.display.draw_text(f"You have fallen to level {self.level}",
                            (x + width // 2, y + 100),
                            'large', 'white', center=True)
        
        # Display stat changes
        current_y = y + 150
        stat_changes = [
            (f"Max HP: {old_stats['max_hp']} -> {self.max_hp}", -max_hp),
            (f"Attack: {old_stats['attack']} -> {self.attack}", -attack),
            (f"Accuracy: {old_stats['accuracy']} -> {self.accuracy}", -accuracy),
            (f"Armour Pen: {old_stats['armour_penetration']} -> {self.armour_penetration}", -armour_penetration),
            (f"Crit Chance: {old_stats['crit_chance']}% -> {self.crit_chance}%", -crit_chance),
            (f"Crit Damage: {old_stats['crit_damage']}% -> {self.crit_damage}%", -crit_damage),
            (f"Defence: {old_stats['defence']} -> {self.defence}", -defence),
            (f"Evasion: {old_stats['evasion']} -> {self.evasion}", -evasion),
            (f"Block Chance: {old_stats['block_chance']}% -> {self.block_chance}%", -block_chance),
            (f"Damage Red: {old_stats['damage_reduction']} -> {self.damage_reduction}", -damage_reduction),
            (f"Max Stamina: {old_stats['max_stamina']} -> {self.max_stamina}", -10)
        ]
        
        for stat_text, decrease in stat_changes:
            colour = 'red' if decrease < 0 else 'white'
            self.display.draw_text(stat_text + f" ({decrease})",
                                (x + width // 2, current_y),
                                'medium', colour, center=True)
            current_y += 30
        
        # Display continue prompt
        self.display.draw_text("Press ENTER to continue...",
                            (x + width // 2, y + height - 50),
                            'medium', center=True)
        
        pygame.display.flip()
            
    def lose_gold(self):
        #Players lose half their gold
        lost_gold = self.gold // 2
        self.gold -= lost_gold
        self.battle_display.draw_battle_message(f"You've lost {lost_gold} gold. You now have {self.gold} remaining.")
        
    def respawn(self):
        #Player respawns back with half their max HP and stamina, lose one respawn chance
        self.hp = self.max_hp // 2
        self.stamina = self.max_stamina // 2
        self.respawn_counter -= 1
        if self.respawn_counter >= 1:
            self.battle_display.draw_battle_message(f"You've been resurrected with {self.hp} HP and {self.stamina} stamina. Do not take this opportunity lightly, you only have {self.respawn_counter} chances left.")
        elif self.respawn_counter == 0:
            self.battle_display.draw_battle_message(f"You've been resurrected with {self.hp} HP and {self.stamina} stamina. Do not take this opportunity lightly, this is your final chance, lose again and you lose forever.")
        else:
            self.game_over()

    def game_over(self):
        #Tells the player their final stats after their last death, brings player back to the title_screen
        self.battle_display.draw_battle_message("You have been defeated for the final time, the deities have given up on you and you have met the forever death.")
        self.battle_display.draw_battle_message("Your final stats are:")
        self.final_stats()
        self.pause()
        self.battle_display.draw_battle_message("Now it's time to try again, appease the deities through prowess this time.")
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
            print("Top 5 most defeated variants:")
            for enemy, count in sorted(self.variant_kill_tracker.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   {enemy}: {count}")
    
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

        # First add level modifiers
        for stat in stats:
            if stat in self.level_modifiers:
                stats[stat] += round(self.level_modifiers[stat], 2)

        # Then add equipment modifiers
        for stat in stats:
            if stat in self.equipment_modifiers:
                stats[stat] += self.equipment_modifiers[stat]

        # Apply all other modifiers
        for stat in stats:
            # Add buff modifiers
            stats[stat] += self.buff_modifiers.get(stat, 0)
            # Add combat buff modifiers
            stats[stat] += self.combat_buff_modifiers.get(stat, 0)
            # Add weapon buff modifiers
            stats[stat] += self.weapon_buff_modifiers.get(stat, 0)
            # Subtract debuff modifiers
            stats[stat] = max(0, stats[stat] - self.debuff_modifiers.get(stat, 0))

        # Update character stats with calculated values
        for stat, value in stats.items():
            if stat == "crit_damage":
                value = max(100, value)
            elif stat in ["damage_reduction", "armour_penetration", "block_chance"]:
                value = max(0, value)
            else:
                value = max(1, value)
            setattr(self, stat, value)

        # Ensure crit_chance and crit_damage stay within reasonable bounds
        self.crit_chance = max(0, min(100, self.crit_chance))
        self.crit_damage = max(100, self.crit_damage)  # Minimum 100% crit damage
    
    def cleanup_after_battle(self):
        for effect in self.status_effects[:]:
            effect.on_remove(self)
            self.remove_status_effect(effect.name)
        
        self.remove_combat_buffs()
        self.combat_buff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        # Update soul crystal effects durations
        for effect_name, effect_data in list(self.soul_crystal_effects.items()):
            if "combats_remaining" in effect_data:
                effect_data["combats_remaining"] -= 1
                if effect_data["combats_remaining"] <= 0:
                    del self.soul_crystal_effects[effect_name]
                    print(f"The {effect_name} effect has worn off!")
        self.debuff_modifiers = {"attack": 0, "defence": 0, "accuracy": 0, "evasion": 0, "crit_chance": 0, "crit_damage": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0}
        self.recalculate_stats()
    
    def show_soul_crystal_effects(self):
        if not self.soul_crystal_effects:
            print("No active soul crystal effects.")
            return
            
        print("\nActive Soul Crystal Effects:")
        for effect_name, effect_data in self.soul_crystal_effects.items():
            effect_type = effect_name.replace("_", " ").title()
            target = effect_data["target"]
            combats = effect_data["combats_remaining"]
            
            if effect_name == "boss_resonance":
                print(f"- {effect_type}: +{effect_data['attack']} Attack and Defence vs Bosses ({combats} combats remaining)")
            elif effect_name == "variant_affinity":
                print(f"- {effect_type}: +{effect_data['accuracy']} and +{effect_data['crit_chance']} vs {target.title()} variants ({combats} combats remaining)")
            elif effect_name == "soul_echo":
                print(f"- {effect_type}: +{effect_data['damage_multiplier']}% damage vs {target.title()} type enemies ({combats} combats remaining)")
    
    def equip_item(self, item):
    # Equip an item and apply its stats to the appropriate dictionary
        if item.type in self.equipped:
            if self.equipped[item.type]:
                self.unequip_item(item.type)
            self.equipped[item.type] = item
            self.equipment_modifiers["attack"] += getattr(item, "attack", 0)
            self.equipment_modifiers["accuracy"] += getattr(item, "accuracy", 0)
            self.equipment_modifiers["crit_chance"] += getattr(item, "crit_chance", 0)
            self.equipment_modifiers["crit_damage"] += getattr(item, "crit_damage", 0)
            self.equipment_modifiers["armour_penetration"] += getattr(item, "armour_penetration", 0)
            self.equipment_modifiers["block_chance"] += getattr(item, "block_chance", 0)
            self.equipment_modifiers["defence"] += getattr(item, "defence", 0)
            self.equipment_modifiers["evasion"] += getattr(item, "evasion", 0)
            self.equipment_modifiers["damage_reduction"] += getattr(item, "damage_reduction", 0)
            self.recalculate_stats()
            if item in self.inventory:
                self.inventory.remove(item)
            print(f"You equipped {item.name}.")
        else:
            print("You can't equip that item.")

    def update_equipment_stats(self):
        """Update equipment stats and check for soulbound growth"""
        for slot, item in self.equipped.items():
            if item and hasattr(item, 'soulbound') and item.soulbound:
                if item.grow_with_player(self.level):
                    print(f"\nYour {item.name} grows stronger with you!")
                    print(item.get_growth_info())
    
    def unequip_item(self, slot):
        # Unequip an item and remove its stats from the appropriate dictionary
        item = self.equipped[slot]
        if item:
            
            self.equipment_modifiers["attack"] -= getattr(item, "attack", 0)
            self.equipment_modifiers["accuracy"] -= getattr(item, "accuracy", 0)
            self.equipment_modifiers["crit_chance"] -= getattr(item, "crit_chance", 0)
            self.equipment_modifiers["crit_damage"] -= getattr(item, "crit_damage", 0)
            self.equipment_modifiers["armour_penetration"] -= getattr(item, "armour_penetration", 0)
            self.equipment_modifiers["block_chance"] -= getattr(item, "block_chance", 0)
            self.equipment_modifiers["defence"] -= getattr(item, "defence", 0)
            self.equipment_modifiers["evasion"] -= getattr(item, "evasion", 0)
            self.equipment_modifiers["damage_reduction"] -= getattr(item, "damage_reduction", 0)        
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
    
    def apply_debuff(self, stat, value, duration=0):
        # Initialise the key if it doesn't exist
        if stat not in self.debuff_modifiers:
            self.debuff_modifiers[stat] = 0
            
        self.debuff_modifiers[stat] += value
        if duration > 0:
            self.active_debuffs[stat] = {'value': value, 'duration': duration}
        self.recalculate_stats()

    def remove_debuff(self, stat, value):
        self.debuff_modifiers[stat] -= value
        self.recalculate_stats()
    
    def apply_weapon_buff(self, value, duration, stat):
        if stat not in self.weapon_buff_modifiers:
            self.weapon_buff_modifiers[stat] = 0
            
        self.weapon_buff_modifiers[stat] += value
        self.weapon_buff = {'value': value, 'duration': duration}
        self.recalculate_stats()
        print(f"Applied a weapon buff of {value} {stat} for {duration} turns.")
    
    def apply_hot(self, item):
        #Applies any HoT items and displays the length of the effect
        if item.effect_type == "hot":
            self.active_hots[item.name] = {
                "duration": item.duration,
                "tick_effect": item.tick_effect
            }
            return True, f"Applied {item.name}. You will heal for {item.tick_effect} HP every turn for {item.duration} turns."
        return False, "This item does not have a heal over time effect."
    
    def apply_defensive_stance(self, duration, boost_percentage):
        """Apply defensive stance with specified duration and boost percentage"""
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Defensive Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
        else:
            defensive_stance_effect = DEFENSIVE_STANCE(duration, boost_percentage)
            self.apply_status_effect(defensive_stance_effect)

    def apply_power_stance(self, duration, boost_percentage):
        """Apply power stance with specified duration and boost percentage"""
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Power Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
        else:
            power_stance_effect = POWER_STANCE(duration, boost_percentage)
            self.apply_status_effect(power_stance_effect)

    def apply_berserker_stance(self, duration, boost_percentage):
        """Apply berserker stance with specified duration and boost percentage"""
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Berserker Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
        else:
            berserker_stance_effect = BERSERKER_STANCE(duration, boost_percentage)
            self.apply_status_effect(berserker_stance_effect)

    def apply_accuracy_stance(self, duration, boost_percentage):
        """Apply accuracy stance with specified duration and boost percentage"""
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Accuracy Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
        else:
            accuracy_stance_effect = ACCURACY_STANCE(duration, boost_percentage)
            self.apply_status_effect(accuracy_stance_effect)

    def apply_evasion_stance(self, duration, boost_percentage):
        """Apply evasion stance with specified duration and boost percentage"""
        existing_effect = next((effect for effect in self.status_effects if effect.name == "Evasion Stance"), None)
        if existing_effect:
            existing_effect.reset_duration()
        else:
            evasion_stance_effect = EVASION_STANCE(duration, boost_percentage)
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
                    
        # Update debuffs
        for stat, debuff_info in list(self.active_debuffs.items()):
            if 'duration' in debuff_info:
                debuff_info['duration'] -= 1
                if debuff_info['duration'] <= 0:
                    self.debuff_modifiers[stat] -= debuff_info['value']
                    del self.active_debuffs[stat]
                    # Format the stat name for display
                    display_stat = stat.replace('_', ' ').title()
                    print(f"Your {display_stat} debuff has worn off.")

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
                     
    def update_weapon_buff(self):
        # Update weapon buff
        if self.weapon_buff['duration'] > 0:
            self.weapon_buff['duration'] -= 1
            if self.weapon_buff['duration'] <= 0:
                self.weapon_buff_modifiers["attack"] -= self.weapon_buff['value']
                print("Your weapon's enhancing effect has worn off")
                self.weapon_buff = {'value': 0, 'duration': 0}
                self.recalculate_stats()
                
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
        self.battle_display.draw_battle_message("Any combat buffs you had have worn off.")
        
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
        """Use an item from inventory with visual feedback"""
        item_display = ItemUseDisplay(self.display)
        
        if item.type == "soul_crystal":
            success, message = item.use(self)
            return success, message
            
        if item.name in self.cooldowns and self.cooldowns[item.name] > 0:
            print(f"You can't use {item.name} yet. Cooldown: {self.cooldowns[item.name]} turns.")
            return False, f"Couldn't use {item.name} due to cooldown!"

        if item.type in ["consumable", "food", "drink", "weapon coating"]:
            message = ""
            success = True
            
            if item.effect_type == "healing":
                heal_amount = min(item.effect, self.max_hp - self.hp)
                self.heal(heal_amount)
                item_display.show_item_use(item, heal_amount)
                message += f"You used {item.name} and restored {heal_amount} HP. "
                
            elif item.effect_type == "stamina":
                stamina_restore = min(item.stamina_restore, self.max_stamina - self.stamina)
                self.restore_stamina(stamina_restore)
                item_display.show_item_use(item, stamina_restore)
                message += f"You used {item.name} and restored {stamina_restore} Stamina. "
                
            elif item.effect_type == "buff":
                duration = getattr(item, 'duration', 0)
                combat_only = getattr(item, 'combat_only', True)
                
                if isinstance(item.effect, list):
                    for stat, value in item.effect:
                        self.apply_buff(stat, value, duration, combat_only)
                    item_display.show_item_use(item, item.effect)
                    message += f"You used {item.name} and gained multiple buffs. "
                else:
                    stat, value = item.effect if isinstance(item.effect, tuple) else ("all stats", item.effect)
                    self.apply_buff(stat, value, duration, combat_only)
                    item_display.show_item_use(item, (stat, value))
                    message += f"You used {item.name} and gained a buff. "
                    
            elif item.effect_type == "weapon_buff":
                if self.equipped['weapon']:
                    stat, value = item.effect
                    self.apply_weapon_buff(value, item.duration, stat)
                    item_display.show_item_use(item, (value, item.duration))
                    message += f"You used {item.name} on your weapon. "
                else:
                    return False, "You don't have a weapon equipped to use this item on."
                    
            elif item.effect_type == "hot":
                success, hot_message = self.apply_hot(item)
                if success:
                    item_display.show_item_use(item, (item.tick_effect, item.duration))
                    message += hot_message
                else:
                    return False, hot_message
                    
            elif item.effect_type == "teleport":
                if item.stack_size > 1:
                    item.stack_size -= 1
                else:
                    self.inventory.remove(item)
                self.cooldowns[item.name] = item.cooldown
                return True, f"You used {item.name} and teleported to that location."
                
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
            if success:
                if item.stack_size > 1:
                    item.stack_size -= 1
                else:
                    self.inventory.remove(item)
                    
                self.cooldowns[item.name] = item.cooldown
                return True, message
            return False, message
        else:
            message = f"You can't use {item.name}."
            return False, message
        
    def use_teleport_scroll(self, game):
        if not self.visited_locations:
            return False, "You haven't visited any locations yet!"
            
        destination = self.show_teleport_menu()
        if destination:
            game.current_location = destination
            self.display.draw_text(f"You teleported to {destination}.", (self.display.config.SCREEN_WIDTH // 2, self.display.config.SCREEN_HEIGHT - 250), 'large', center=True)
            return destination
        self.display.draw_text("You cancel your teleport scroll.", (self.display.config.SCREEN_WIDTH // 2, self.display.config.SCREEN_HEIGHT - 30), 'large', center=True)
        pygame.display.flip()
        pygame.time.wait(1000)
        return

    def show_teleport_menu(self):
        """Display visual menu for teleport scroll selection"""
        from world_map import WorldMap
        self.world_map = WorldMap()

        layout = self.display.calculate_layout()
        battle_log = layout['battle_log_panel']
        width = battle_log[0]
        height = battle_log[1] 
        x = battle_log[2]
        y = battle_log[3]
        
        # Sort locations by level requirement
        locations_by_level = []
        for loc in sorted(self.visited_locations):
            level_req = self.world_map.get_min_level(loc)
            locations_by_level.append((loc, level_req))
        locations_by_level.sort(key=lambda x: x[1])  # Sort by level requirement
        
        items_per_page = 6
        scroll_offset = 0
        available_locations = []

        while True:
            self.display.draw_panel(width, height, x, y)
            self.display.draw_text("=== TELEPORT LOCATIONS ===",
                                    (x + width // 2, y + 20),
                                    'large', center=True)
            
            visible_items = locations_by_level[scroll_offset:scroll_offset + items_per_page]
            for i, (location, min_level) in enumerate(visible_items, 1):
                if self.level >= min_level:
                    self.display.draw_text(f"{i}. {location} (Level {min_level})",
                                            (x + width // 2, y + 30 + i * 30),
                                            'medium', center=True)
                    available_locations.append(location)
                else:
                    self.display.draw_text(f"X. {location} (Level {min_level}) [LOCKED]",
                                            (x + width // 2, y + 30 + i * 30),
                                            'medium', colour='red', center=True)
            
            nav_text = "UP/DOWN: Scroll | 1-6: Select | ESC: Cancel" if len(locations_by_level) > items_per_page else "1-6: Select | ESC: Cancel"
            self.display.draw_text(nav_text, (x + width // 2, y + height - 30), 'medium', center=True)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    return None
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and scroll_offset > 0:
                        scroll_offset -= 1
                    elif event.key == pygame.K_DOWN:
                        if scroll_offset < len(locations_by_level) - items_per_page:
                            scroll_offset += 1
                    elif event.key in range(pygame.K_1, pygame.K_7):
                        index = event.key - pygame.K_1
                        if index < len(visible_items):
                            location = visible_items[index][0]
                            if location in available_locations:
                                self.display.draw_panel(width, height, x, y)
                                return location
                            
            self.display.clock.tick(self.display.config.FPS)
    
    def show_usable_items(self):
        """Shows a list of usable items if available, else prints that none are available"""
        usable_items = [item for item in self.inventory 
                        if item.type in ["consumable", "food", "drink", "weapon coating", "soul_crystal"]]
        if not usable_items:
            print("You have no usable items.")
            return None
        
        print("\nUsable Items:")
        for i, item in enumerate(usable_items, 1):
            if isinstance(item, SoulCrystal):
                # Special handling for soul crystals with expanded details
                if item.used:
                    print(f"{i}. {item.name}: Depleted")
                else:
                    effect_desc = item.get_effect_description()
                    # Print the item number and name first
                    print(f"{i}. {item.name}:")
                    # Then print the effect description indented for better readability
                    for line in effect_desc.split('\n'):
                        print(f"   {line}")
            else:
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
        inventory_display = InventoryDisplay(self.display, self)
        inventory_display.show_inventory()
    
    def _display_item(self, idx, item):
        """Helper method to display a single item"""
        stats = []
        if isinstance(item, SoulCrystal):
        # Call soul crystal's own effect description method
            effect_desc = item.get_effect_description()
            print(f"{idx}. {item.name} [{item.type.title()} - {item.tier.title()}]")
            # Print effect description indented for readability
            for line in effect_desc.split('\n'):
                print(f"    {line}")
            return

        # Regular item display logic
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
            
        stats_str = ", ".join(stats)
        effect_desc = self.get_effect_description(item)

        print(f"{idx}. {item.name} [{item.type.title()} - {item.tier.title()}] ", end="")
        if stats_str:
            print(f"({stats_str}) ", end="")
        if effect_desc and effect_desc != "Unknown effect":
            print(f"[{effect_desc}] ", end="")
        print(f"(Value: {item.value} gold)")
            
    def _display_stacked_item(self, idx, item, count):
        """Helper method to displa a stacked item"""
        effect_desc = self.get_effect_description(item)
        print(f"{idx}. {item.name} x{count} [{item.type.title()} - {item.tier.title()}] [{effect_desc}] (Value: {item.value} gold each)")
    
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
        """Get stamina cost for weapon type"""
        weapon_costs = {
            "light": 3,
            "medium": 5,
            "heavy": 7,
            "soulbound": 6  # Special cost for soulbound weapons
        }
        return weapon_costs.get(weapon_type, 5)  # Default to medium cost if type unknown
    
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
        equipped_weapon = self.equipped.get("weapon")
        weapon_type = equipped_weapon.weapon_type if equipped_weapon else "light"
        
        available_attack_names = WEAPON_ATTACK_TYPES[weapon_type]
        available_attacks = {}
        
        # Check if any stance is active
        active_stance = any(effect.name.endswith("Stance") for effect in self.status_effects)
        
        # Add each available attack, filtering out stances if one is active
        for name in available_attack_names:
            attack = PLAYER_ATTACK_TYPES[name]
            if active_stance and "stance_type" in attack:
                continue
            available_attacks[name] = attack
        
        return available_attacks
            
    def display_attack_options(self):
        """Display available attack options with costs using PyGame"""
        available_attacks = self.get_available_attack_types()
        weapon_type = self.equipped.get("weapon", {"weapon_type": "light"}).weapon_type
        base_stamina = self.get_weapon_stamina_cost(weapon_type)
        
        # Use main battle log area for attack options
        layout = self.display.calculate_layout()
        battle_log = layout['battle_log_panel']
        x = battle_log[2]
        y = battle_log[3]
        width = battle_log[0]
        height = battle_log[1]
        
        # Clear and redraw battle log panel
        self.display.draw_panel(width, height, x, y)
        
        # Draw title
        self.display.draw_text("Choose your attack:",
                            (x + width // 2, y + 20),
                            'large', center=True)
        
        # Draw each attack option
        current_y = y + 60
        for i, (_, attack) in enumerate(available_attacks.items(), 1):
            cost = base_stamina + attack['stamina_modifier']
            
            # Format attack info
            info = [f"Stamina: {cost}"]
            if attack['damage_modifier'] > 0:
                info.append(f"Damage: {int(attack['damage_modifier'] * 100)}%")
            if 'extra_attacks' in attack:
                info.append(f"Hits: {attack['extra_attacks'] + 1}")
            if 'stat_buffs' in attack and attack['stat_buffs']:
                buffs = [f"{stat.replace('_', ' ').title()} +{value}" 
                        for stat, value in attack['stat_buffs'].items()]
                info.append("Buffs: " + ", ".join(buffs))
            if 'effect' in attack and attack['effect']:
                info.append(f"Effect: {attack['effect'].replace('_', ' ').title()}")
            if 'stance_type' in attack:
                # Get stance effect from status_effects.py mappings
                stance_effects = {
                    'defensive': {
                        'buffs': {'def': 33, 'bc': 33, 'dr': 33},
                        'debuffs': {'att': 16, 'crit%': 16}
                    },
                    'power': {
                        'buffs': {'att': 33, 'ap': 33, 'cdmg': 33},
                        'debuffs': {'def': 16, 'eva': 16}
                    },
                    'berserker': {
                        'buffs': {'att': 100, 'ap': 50, 'crit%': 50, 'cdmg': 100},
                        'debuffs': {'def': 50, 'eva': 50, 'bc': 50, 'dr': 50}
                    },
                    'accuracy': {
                        'buffs': {'acc': 66, 'crit%': 33},
                        'debuffs': {'bc': 16, 'eva': 16}
                    },
                    'evasion': {
                        'buffs': {'eva': 66, 'crit%': 33, 'cdmg': 33},
                        'debuffs': {'def': 33, 'bc': 33, 'dr': 33}
                    }
                }
                
                stance = stance_effects[attack['stance_type']]
                if stance['buffs']:
                    buffs = [f"{stat.replace('_', ' ').title()} +{value}%" 
                            for stat, value in stance['buffs'].items()]
                    info.append("Buffs: " + ", ".join(buffs))
                if stance['debuffs']:
                    debuffs = [f"{stat.replace('_', ' ').title()} -{value}%" 
                             for stat, value in stance['debuffs'].items()]
                    info.append("Debuffs: " + ", ".join(debuffs))
                info.append(f"Duration: {attack['duration']} turns")
                
            
            # Draw attack option
            self.display.draw_text(f"{i}. {attack['name']} ({', '.join(info)})",
                                (x + 20, current_y),
                                'small')
            current_y += 30
        
        pygame.display.flip()

    def display_kill_stats(self):
        from display import KillLogDisplay
        """
        Displays kill statistics organized by type and includes used souls
        """
        kill_display = KillLogDisplay(self.display, self)
        kill_display.show_kill_log()
    
    def record_kill(self, enemy_name):
        """
        Records kills for monsters, variants, and bosses separately.
        - Standard kills go to kill_tracker (1 soul)
        - Variant kills go to variant_kill_tracker (5 souls)
        - Boss kills (including variant bosses) go to boss_kill_tracker (10 souls)
        Boss kills are not recorded in the standard kill tracker.
        """
        # Define boss monsters to track seperately
        boss_types = {
            "Echo Wraith", "Crystal Guardian", "Void Walker", "Empowered Void Walker", "Divine Architect",
            "Ethereal Leviathan", "Astral Demiurge", "Celestial Arbiter", "Seraphim Guardian", "Celestial Titan",
            "Nebula Colossus", "Galatic Leviathan", "Astral Behemoth", "Cosmic Devourer", "Cinder Archfiend",
            "Inferno Wyrm", "Volcanic Titan", "Phoenix Overlord", "Magma Colossus", "Soul Forgemaster"
        }
        
        # Split the enemy name into parts to separate variant from base name
        name_parts = enemy_name.split()
        
         # Check for variant first
        if len(name_parts) > 1 and name_parts[0] in VARIANT_TYPES:
            variant_type = name_parts[0]
            base_monster = " ".join(name_parts[1:])
            
            # Record the variant kill
            if variant_type not in self.variant_kill_tracker:
                self.variant_kill_tracker[variant_type] = 1
            else:
                self.variant_kill_tracker[variant_type] += 1
            
            # Check if the base monster (without variant) is a boss
            if base_monster in boss_types:
                # Record the boss kill
                if base_monster in self.boss_kill_tracker:
                    self.boss_kill_tracker[base_monster] += 1
                else:
                    self.boss_kill_tracker[base_monster] = 1
            else:
                # Only record in kill_tracker if it's not a boss
                if base_monster in self.kill_tracker:
                    self.kill_tracker[base_monster] += 1
                else:
                    self.kill_tracker[base_monster] = 1
                
        else:
            # Non-variant enemy, check if it's a boss
            if enemy_name in boss_types:
                if enemy_name in self.boss_kill_tracker:
                    self.boss_kill_tracker[enemy_name] += 1
                else:
                    self.boss_kill_tracker[enemy_name] = 1
            else:
                # Only record in kill_tracker if it's not a boss
                if enemy_name in self.kill_tracker:
                    self.kill_tracker[enemy_name] += 1
                else:
                    self.kill_tracker[enemy_name] = 1
            
    def add_visited_location(self, location):
        # Adds the current location to the visited_locations to help work with teleport scrolls
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