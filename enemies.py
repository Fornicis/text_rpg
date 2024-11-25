from player import Character
from game_config import MONSTER_TYPES
from status_effects import *
import random

class Enemy(Character):
    def __init__(self, name=None, hp=None, attack=None, defence=None, accuracy=None, evasion=None, 
             crit_chance=None, crit_damage=None, armour_penetration=None, damage_reduction=None, 
             block_chance=None, exp=None, gold=None, tier=None, level=0, attack_types=None, template=None, player=None):
        
        if template and player:
            self.template = template
            self.debug_info = {}  # Store debug calculation info
            
            # Calculate stats and store debug info
            stats = self._calculate_stats_with_debug(player, template)
            
            hp = stats['hp']
            attack = stats['attack']
            defence = stats['defence']
            accuracy = stats['accuracy']
            evasion = stats['evasion']
            crit_chance = stats['crit_chance']
            crit_damage = stats['crit_damage']
            armour_penetration = stats['armour_penetration']
            damage_reduction = stats['damage_reduction']
            block_chance = stats['block_chance']
            exp = stats['exp']
            gold = stats['gold']
            level = stats['level']
            tier = template["tier"]
            final_name = stats['name']
            base_attack_types = stats['attack_types']

        super().__init__(final_name, hp, attack, defence, accuracy, evasion, 
                        crit_chance, crit_damage, armour_penetration, 
                        damage_reduction, block_chance)
        
        self.exp = exp
        self.gold = gold
        self.tier = tier
        self.level = level
        self.stunned = False
        self.monster_type = self._determine_monster_type(final_name)
        
        # Update attack types initialization
        if template and player:
            self.attack_types = {attack_type: ENEMY_ATTACK_TYPES[attack_type] 
                            for attack_type in stats['attack_types']}
        elif attack_types:
            self.attack_types = {attack_type: ENEMY_ATTACK_TYPES[attack_type] 
                            for attack_type in attack_types}
        else:
            self.attack_types = {"normal": ENEMY_ATTACK_TYPES["normal"]}
            
    def _calculate_stats_with_debug(self, player, template):
        stats = {}
        debug = self.debug_info
        
        # Store base percentages and modifications
        debug['base_percentages'] = {
            "hp_percent": 100,
            "attack_percent": 100,
            "defence_percent": 100,
            "accuracy_percent": 100,
            "evasion_percent": 100,
            "crit_chance_percent": 100,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 100,
            "block_chance_percent": 100
        }
        
        # Store template modifications
        debug['template_mods'] = template["stats"].copy()
        base_percentages = debug['base_percentages'].copy()
        base_percentages.update(debug['template_mods'])
        
        # Handle variant
        stats['name'] = template['name']
        # Store and track attack types
        debug['attack_types'] = {
            'base': template["attack_types"].copy(),
            'final': template["attack_types"].copy()
        }
        
        stats['attack_types'] = template["attack_types"].copy()
        debug['variant_roll'] = random.random()
        
        if debug['variant_roll'] < 10.1:
            debug['available_variants'] = [(name, var_data["chance"]) 
                                         for name, var_data in MONSTER_VARIANTS.items()]
            
            total_weight = sum(weight for _, weight in debug['available_variants'])
            variant_roll = random.random() * total_weight
            current_weight = 0
            
            for variant_name, weight in debug['available_variants']:
                current_weight += weight
                if variant_roll <= current_weight:
                    variant = MONSTER_VARIANTS[variant_name]
                    self.variant = {
                        'name': variant_name,
                        'stats': variant.get('stats', {}).copy(),
                        'loot_modifiers': variant.get('loot_modifiers', {}).copy()
                    }
                    stats['name'] = f"{variant_name} {template['name']}"
                    
                    debug['variant_mods'] = variant.get('stats', {}).copy()
                    if "stats" in self.variant:
                        for stat, modifier in self.variant["stats"].items():
                            if stat in base_percentages:
                                base_percentages[stat] = int(base_percentages[stat] * (modifier / 100))
                    
                    if "additional_attacks" in variant:
                        variant_attacks = variant["additional_attacks"]
                        stats['attack_types'].extend(variant_attacks)
                        debug['attack_types']['variant_added'] = variant_attacks
                        debug['attack_types']['final'] = stats['attack_types']
                    break
            else:
                self.variant = None
        else:
            self.variant = None
            debug['variant_mods'] = {}

        # Level calculations        
        level_min = max(1, player.level - random.randint(1, 2))
        level_max = player.level + random.randint(1, 2)
        stats['level'] = random.randint(level_min, level_max)
        debug['level_calc'] = {
            'min': level_min,
            'max': level_max,
            'chosen': stats['level']
        }
        
        # Store level scaling
        debug['level_diff'] = max(1, stats['level'] + 2 - player.level)
        debug['level_scale'] = min(1.5, 1 + (debug['level_diff'] * 0.1))
        
        # Store player base stats for calculations
        debug['player_stats'] = {
            'max_hp': player.max_hp,
            'base_attack': player.base_attack,
            'level_attack': player.level_modifiers.get("attack", 0),
            'equipment_attack': player.equipment_modifiers.get("attack", 0),
            'base_defence': player.base_defence,
            'level_defence': player.level_modifiers.get("defence", 0),
            'equipment_defence': player.equipment_modifiers.get("defence", 0)
        }

        # Calculate and store main stats
        stats['hp'] = int(player.max_hp * base_percentages["hp_percent"] / 100)
        stats['attack'] = int((player.base_attack + player.level_modifiers.get("attack") + 
                    (player.equipment_modifiers.get("attack") * 0.6)) * 
                    (base_percentages["attack_percent"] / 100) * debug['level_scale'])
        stats['defence'] = int((player.base_defence + player.level_modifiers.get("defence") + 
                    (player.equipment_modifiers.get("defence") * 0.6)) * 
                    (base_percentages["defence_percent"] / 100) * debug['level_scale'])
                    
        # Store final percentages used
        debug['final_percentages'] = base_percentages.copy()
        
        # Calculate remaining stats with caps
        stats.update(self._calculate_secondary_stats(player, base_percentages))
        
        # Calculate rewards
        debug['exp_roll'] = random.randint(random.randint(8, 20), random.randint(12, 30))
        debug['gold_roll'] = random.randint(random.randint(8, 20), random.randint(12, 30))
        stats['exp'] = debug['exp_roll'] * max(1, player.level)
        stats['gold'] = debug['gold_roll'] * max(1, player.level)
        
        if self.variant:
            stats['exp'] = int(stats['exp'] * 1.5)
            if 'loot_modifiers' in self.variant and 'gold_multiplier' in self.variant['loot_modifiers']:
                stats['gold'] = int(stats['gold'] * self.variant['loot_modifiers']['gold_multiplier'])
        
        return stats
    
    def _calculate_secondary_stats(self, player, base_percentages):
        """Calculate secondary stats with caps and store debug information"""
        stats = {}
        self.debug_info['secondary_calc'] = {}
        debug = self.debug_info['secondary_calc']
        
        # Accuracy calculation
        base_accuracy = (player.base_accuracy + player.level_modifiers.get("accuracy", 0) + 
                        (player.equipment_modifiers.get("accuracy", 0) * 0.5))
        accuracy = int(base_accuracy * base_percentages["accuracy_percent"] / 100)
        stats['accuracy'] = min(95, accuracy)
        debug['accuracy'] = {
            'base': player.base_accuracy,
            'level_mod': player.level_modifiers.get("accuracy", 0),
            'equipment_mod': player.equipment_modifiers.get("accuracy", 0),
            'equipment_scaled': player.equipment_modifiers.get("accuracy", 0) * 0.5,
            'total_base': base_accuracy,
            'percent_mod': base_percentages["accuracy_percent"],
            'calculated': accuracy,
            'final': stats['accuracy']
        }
        
        # Evasion calculation
        base_evasion = (player.base_evasion + player.level_modifiers.get("evasion", 0) + 
                    (player.equipment_modifiers.get("evasion", 0) * 0.6))
        evasion = int(base_evasion * base_percentages["evasion_percent"] / 100)
        stats['evasion'] = min(50, evasion)
        debug['evasion'] = {
            'base': player.base_evasion,
            'level_mod': player.level_modifiers.get("evasion", 0),
            'equipment_mod': player.equipment_modifiers.get("evasion", 0),
            'equipment_scaled': player.equipment_modifiers.get("evasion", 0) * 0.6,
            'total_base': base_evasion,
            'percent_mod': base_percentages["evasion_percent"],
            'calculated': evasion,
            'final': stats['evasion']
        }
        
        # Crit chance calculation
        base_crit_chance = (player.base_crit_chance + player.level_modifiers.get("crit_chance", 0) + 
                        (player.equipment_modifiers.get("crit_chance", 0) * 0.6))
        crit_chance = int(base_crit_chance * base_percentages["crit_chance_percent"] / 100)
        stats['crit_chance'] = min(50, crit_chance)
        debug['crit_chance'] = {
            'base': player.base_crit_chance,
            'level_mod': player.level_modifiers.get("crit_chance", 0),
            'equipment_mod': player.equipment_modifiers.get("crit_chance", 0),
            'equipment_scaled': player.equipment_modifiers.get("crit_chance", 0) * 0.6,
            'total_base': base_crit_chance,
            'percent_mod': base_percentages["crit_chance_percent"],
            'calculated': crit_chance,
            'final': stats['crit_chance']
        }
        
        # Crit damage calculation
        base_crit_damage = (player.base_crit_damage + player.level_modifiers.get("crit_damage", 0) + 
                        (player.equipment_modifiers.get("crit_damage", 0) * 0.6))
        crit_damage = int(base_crit_damage * base_percentages["crit_damage_percent"] / 100)
        stats['crit_damage'] = min(250, max(100, crit_damage))  # Minimum 100%, maximum 250%
        debug['crit_damage'] = {
            'base': player.base_crit_damage,
            'level_mod': player.level_modifiers.get("crit_damage", 0),
            'equipment_mod': player.equipment_modifiers.get("crit_damage", 0),
            'equipment_scaled': player.equipment_modifiers.get("crit_damage", 0) * 0.6,
            'total_base': base_crit_damage,
            'percent_mod': base_percentages["crit_damage_percent"],
            'calculated': crit_damage,
            'final': stats['crit_damage']
        }
        
        # Armour penetration calculation
        base_armour_pen = (player.base_armour_penetration + 
                        player.level_modifiers.get("armour_penetration", 0) + 
                        (player.equipment_modifiers.get("armour_penetration", 0) * 0.6))
        armour_pen = int(base_armour_pen * base_percentages["armour_penetration_percent"] / 100)
        stats['armour_penetration'] = min(50, armour_pen)
        debug['armour_penetration'] = {
            'base': player.base_armour_penetration,
            'level_mod': player.level_modifiers.get("armour_penetration", 0),
            'equipment_mod': player.equipment_modifiers.get("armour_penetration", 0),
            'equipment_scaled': player.equipment_modifiers.get("armour_penetration", 0) * 0.6,
            'total_base': base_armour_pen,
            'percent_mod': base_percentages["armour_penetration_percent"],
            'calculated': armour_pen,
            'final': stats['armour_penetration']
        }
        
        # Damage reduction calculation
        base_damage_red = (player.base_damage_reduction + 
                        player.level_modifiers.get("damage_reduction", 0) + 
                        (player.equipment_modifiers.get("damage_reduction", 0) * 0.6))
        damage_red = int(base_damage_red * base_percentages["damage_reduction_percent"] / 100)
        stats['damage_reduction'] = min(30, damage_red)
        debug['damage_reduction'] = {
            'base': player.base_damage_reduction,
            'level_mod': player.level_modifiers.get("damage_reduction", 0),
            'equipment_mod': player.equipment_modifiers.get("damage_reduction", 0),
            'equipment_scaled': player.equipment_modifiers.get("damage_reduction", 0) * 0.6,
            'total_base': base_damage_red,
            'percent_mod': base_percentages["damage_reduction_percent"],
            'calculated': damage_red,
            'final': stats['damage_reduction']
        }
        
        # Block chance calculation
        base_block = (player.base_block_chance + 
                    player.level_modifiers.get("block_chance", 0) + 
                    (player.equipment_modifiers.get("block_chance", 0) * 0.6))
        block = int(base_block * base_percentages["block_chance_percent"] / 100)
        stats['block_chance'] = min(30, block)
        debug['block_chance'] = {
            'base': player.base_block_chance,
            'level_mod': player.level_modifiers.get("block_chance", 0),
            'equipment_mod': player.equipment_modifiers.get("block_chance", 0),
            'equipment_scaled': player.equipment_modifiers.get("block_chance", 0) * 0.6,
            'total_base': base_block,
            'percent_mod': base_percentages["block_chance_percent"],
            'calculated': block,
            'final': stats['block_chance']
        }
        
        return stats

    def debug_stat_calculation(self, player):
        """Display full calculation process using stored debug info"""
        debug = []
        debug.append(f"\n=== Detailed Stat Calculation for {self.name} ===\n")
        
        # Base percentages
        debug.append("1. Initial Base Percentages:")
        for stat, value in self.debug_info['base_percentages'].items():
            debug.append(f"{stat}: {value}%")
        
        # Template modifications
        debug.append("\n2. Template Modifications:")
        for stat, value in self.debug_info['template_mods'].items():
            debug.append(f"{stat} modified to: {value}%")
            
        # Variant modifications if any
        if self.variant:
            debug.append("\n3. Variant Modifications:")
            for stat, modifier in self.debug_info['variant_mods'].items():
                debug.append(f"{stat}: {modifier}%")
                
        # Level scaling
        debug.append("\n4. Level Scaling:")
        debug.append(f"Level range: {self.debug_info['level_calc']['min']} - {self.debug_info['level_calc']['max']}")
        debug.append(f"Chosen level: {self.debug_info['level_calc']['chosen']}")
        debug.append(f"Level difference: {self.debug_info['level_diff']}")
        debug.append(f"Level scale: {self.debug_info['level_scale']:.2f}")
        
        # Main stat calculations
        debug.append("\n5. Main Stat Calculations:")
        
        # HP calculation
        base_hp = self.debug_info['player_stats']['max_hp']
        hp_percent = self.debug_info['final_percentages']['hp_percent']
        debug.append(f"HP Calculation:")
        debug.append(f"Base HP (from player): {base_hp}")
        debug.append(f"Percentage modifier: {hp_percent}%")
        debug.append(f"Final HP: {base_hp} * {hp_percent}% = {self.hp}")
        
        # Attack calculation
        attack_base = self.debug_info['player_stats']['base_attack']
        attack_level = self.debug_info['player_stats']['level_attack']
        attack_equipment = self.debug_info['player_stats']['equipment_attack']
        attack_percent = self.debug_info['final_percentages']['attack_percent']
        
        debug.append(f"\nAttack Calculation:")
        debug.append(f"Base attack: {attack_base}")
        debug.append(f"Level modifier: {attack_level}")
        debug.append(f"Equipment modifier (60%): {attack_equipment * 0.6}")
        debug.append(f"Combined base: {attack_base + attack_level + (attack_equipment * 0.6)}")
        debug.append(f"Percentage modifier: {attack_percent}%")
        debug.append(f"Level scaling: {self.debug_info['level_scale']:.2f}")
        debug.append(f"Final attack: {self.attack}")
        
        # Defence Calculation
        defence_base = self.debug_info['player_stats']['base_defence']
        defence_level = self.debug_info['player_stats']['level_defence']
        defence_equipment = self.debug_info['player_stats']['equipment_defence']
        defence_percent = self.debug_info['final_percentages']['defence_percent']
        
        debug.append(f"\nDefence Calculation:")
        debug.append(f"Base defence: {defence_base}")
        debug.append(f"Level modifier: {defence_level}")
        debug.append(f"Equipment modifier (60%): {defence_equipment * 0.6}")
        debug.append(f"Combined base: {defence_base + defence_level + (defence_equipment * 0.6)}")
        debug.append(f"Percentage modifier: {defence_percent}%")
        debug.append(f"Level scaling: {self.debug_info['level_scale']:.2f}")
        debug.append(f"Final defence: {self.defence}")
        
        # Secondary stats calculations
        debug.append("\n6. Secondary Stats Calculations:")
        
        secondary_stats = self.debug_info['secondary_calc']
        for stat_name, stat_info in secondary_stats.items():
            debug.append(f"\n{stat_name.replace('_', ' ').title()} Calculation:")
            debug.append(f"Base: {stat_info['base']}")
            debug.append(f"Level modifier: {stat_info['level_mod']}")
            debug.append(f"Equipment modifier: {stat_info['equipment_mod']}")
            debug.append(f"Equipment scaled: {stat_info['equipment_scaled']}")
            debug.append(f"Total base: {stat_info['total_base']}")
            debug.append(f"Percentage modifier: {stat_info['percent_mod']}%")
            debug.append(f"Calculated value: {stat_info['calculated']}")
            debug.append(f"Final value (after caps): {stat_info['final']}")
            
        # Add attack types section
        debug.append("\n7. Attack Types:")
        debug.append("Base attack types:")
        for attack in self.debug_info['attack_types']['base']:
            attack_info = ENEMY_ATTACK_TYPES[attack]
            debug.append(f"- {attack_info['name']}:")
            debug.append(f"  Damage modifier: {attack_info['damage_modifier']}")
            if 'effect' in attack_info and attack_info['effect']:
                debug.append(f"  Effect: {attack_info['effect']}")
            if 'extra_attacks' in attack_info:
                debug.append(f"  Extra attacks: {attack_info['extra_attacks']}")
        
        if 'variant_added' in self.debug_info['attack_types']:
            debug.append("\nVariant added attack types:")
            for attack in self.debug_info['attack_types']['variant_added']:
                attack_info = ENEMY_ATTACK_TYPES[attack]
                debug.append(f"- {attack_info['name']}:")
                debug.append(f"  Damage modifier: {attack_info['damage_modifier']}")
                if 'effect' in attack_info and attack_info['effect']:
                    debug.append(f"  Effect: {attack_info['effect']}")
                if 'extra_attacks' in attack_info:
                    debug.append(f"  Extra attacks: {attack_info['extra_attacks']}")
        
        debug.append("\nFinal available attacks:")
        debug.append(f"Total unique attacks: {len(set(self.debug_info['attack_types']['final']))}")
        for attack in set(self.debug_info['attack_types']['final']):
            attack_info = ENEMY_ATTACK_TYPES[attack]
            debug.append(f"- {attack_info['name']}:")
            debug.append(f"  Damage modifier: {attack_info['damage_modifier']}")
            if 'effect' in attack_info and attack_info['effect']:
                debug.append(f"  Effect: {attack_info['effect']}")
            if 'extra_attacks' in attack_info:
                debug.append(f"  Extra attacks: {attack_info['extra_attacks']}")
        
        return "\n".join(debug)
    
    def _determine_monster_type(self, name):
        """Determine monster type based on name"""
        for type_name, type_data in MONSTER_TYPES.items():
            if name in type_data["members"]:
                return type_name
        return "unknown"
    
    def choose_attack(self):
        """Choose a random attack from available attack types"""
        if self.stunned:
            self.stunned = False
            return None
            
        # Get all available attack types
        available_attacks = list(self.attack_types.keys())
        
        # Choose random attack
        if available_attacks:
            return random.choice(available_attacks)
        
        # Fallback to normal attack if somehow no attacks available
        return "normal"

    def get_level_appropriate_attacks(self):
        """Get attacks available at current level"""
        attack_unlocks = {
            1: ["normal", "double", "power"],
            5: ["stunning", "poison", "burn", "freeze"],
            10: ["draining", "vampiric", "attack_weaken"],
            15: ["reckless", "defence_break", "confusion"],
            20: ["triple", "damage_reflect"]
        }
        
        available_attacks = []
        for req_level, attacks in attack_unlocks.items():
            if self.level >= req_level:
                available_attacks.extend(attacks)
                
        return [attack for attack in available_attacks if attack in self.attack_types]

# Helper function to create enemies
def create_enemy(enemy_type, player=None):
    """Create a new enemy either from template + player scaling or from ENEMY_TEMPLATES directly"""
    if enemy_type in ENEMY_TEMPLATES:
        template = ENEMY_TEMPLATES[enemy_type]
        enemy = Enemy(template=template, player=player)
        enemy.soultype = template.get("soultype", "standard")
        enemy.monster_type = template.get("monster_type", "unknown")
        print(enemy.debug_stat_calculation(player))
        return enemy
    return None

ENEMY_TEMPLATES = {
    # Easy Enemies
    "Rat": {
        "name": "Rat",
        "stats": {
            "hp_percent": random.randint(50, 70),      # Small but quick
            "attack_percent": random.randint(80, 90),  
            "defence_percent": random.randint(50, 70),  # Poor defense
            "accuracy_percent": random.randint(90, 100), 
            "evasion_percent": random.randint(90, 110), # High evasion
            "crit_chance_percent": random.randint(70, 90),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(40, 60),
            "block_chance_percent": random.randint(30, 50)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "grass"
    },

    "Boar": {
        "name": "Boar",
        "stats": {
            "hp_percent": random.randint(100, 120),     # Tanky
            "attack_percent": random.randint(90, 100),  # Strong
            "defence_percent": random.randint(90, 100), 
            "accuracy_percent": random.randint(70, 80), 
            "evasion_percent": random.randint(40, 60),  # Poor evasion
            "crit_chance_percent": random.randint(50, 70),
            "crit_damage_percent": random.randint(100, 120),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(70, 90),
            "block_chance_percent": random.randint(50, 70)
        },
        "tier": "low",
        "attack_types": ["normal", "power", "reckless", "stunning"],
        "soultype": "standard",
        "monster_type": "grass"
    },

    "Plains Hawk": {
        "name": "Plains Hawk",
        "stats": {
            "hp_percent": random.randint(50, 70),       # Very fragile
            "attack_percent": random.randint(90, 100),  
            "defence_percent": random.randint(40, 60),  # Poor defense
            "accuracy_percent": random.randint(100, 120), # Highly accurate
            "evasion_percent": random.randint(100, 120), # Very evasive
            "crit_chance_percent": random.randint(80, 100),
            "crit_damage_percent": random.randint(100, 120),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(30, 50),
            "block_chance_percent": random.randint(20, 40)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "triple", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Strider": {
        "name": "Strider",
        "stats": {
            "hp_percent": random.randint(70, 90),     # Balanced HP
            "attack_percent": random.randint(80, 90), # Balanced attack
            "defence_percent": random.randint(60, 80),
            "accuracy_percent": random.randint(80, 100),
            "evasion_percent": random.randint(80, 100), 
            "crit_chance_percent": random.randint(60, 80),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(50, 70),
            "block_chance_percent": random.randint(40, 60)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Bull": {
        "name": "Bull",
        "stats": {
            "hp_percent": random.randint(100, 120),    # Very tanky
            "attack_percent": random.randint(100, 120), # Very strong
            "defence_percent": random.randint(80, 100),
            "accuracy_percent": random.randint(50, 70), # Poor accuracy
            "evasion_percent": random.randint(30, 50),  # Very poor evasion
            "crit_chance_percent": random.randint(40, 60),
            "crit_damage_percent": random.randint(100, 120),
            "armour_penetration_percent": random.randint(60, 80),
            "damage_reduction_percent": random.randint(70, 90),
            "block_chance_percent": random.randint(40, 60)
        },
        "tier": "low",
        "attack_types": ["normal", "power", "reckless", "stunning"],
        "soultype": "standard",
        "monster_type": "grass"
    },

    "Bat": {
        "name": "Bat",
        "stats": {
            "hp_percent": random.randint(50, 70),      # Fragile
            "attack_percent": random.randint(80, 90),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(90, 110),
            "evasion_percent": random.randint(100, 120), # Very evasive
            "crit_chance_percent": random.randint(70, 90),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(30, 50),
            "block_chance_percent": random.randint(20, 40)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "vampiric", "draining"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Goblin": {
        "name": "Goblin",
        "stats": {
            "hp_percent": random.randint(60, 80),
            "attack_percent": random.randint(80, 90),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(80, 100),
            "evasion_percent": random.randint(70, 90),
            "crit_chance_percent": random.randint(70, 90),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(40, 60),
            "block_chance_percent": random.randint(30, 50)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Spider": {
        "name": "Spider",
        "stats": {
            "hp_percent": random.randint(50, 70),       # Fragile
            "attack_percent": random.randint(80, 100),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(100, 120), # Very accurate
            "evasion_percent": random.randint(90, 110),
            "crit_chance_percent": random.randint(80, 100),
            "crit_damage_percent": random.randint(90, 110),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(30, 50),
            "block_chance_percent": random.randint(20, 40)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Slime": {
        "name": "Slime",
        "stats": {
            "hp_percent": random.randint(100, 120),     # High HP
            "attack_percent": random.randint(80, 90),   
            "defence_percent": random.randint(90, 110), # High defense
            "accuracy_percent": random.randint(60, 80),
            "evasion_percent": random.randint(40, 60),
            "crit_chance_percent": random.randint(30, 50),
            "crit_damage_percent": random.randint(70, 90),
            "armour_penetration_percent": random.randint(30, 50),
            "damage_reduction_percent": random.randint(90, 110),
            "block_chance_percent": random.randint(50, 70)
        },
        "tier": "low",
        "attack_types": ["normal", "poison", "draining", "defence_break"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Frog": {
        "name": "Frog",
        "stats": {
            "hp_percent": random.randint(70, 90),
            "attack_percent": random.randint(80, 90),
            "defence_percent": random.randint(60, 80),
            "accuracy_percent": random.randint(80, 100),
            "evasion_percent": random.randint(90, 110),
            "crit_chance_percent": random.randint(60, 80),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(50, 70),
            "block_chance_percent": random.randint(30, 50)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "stunning"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Tree Sprite": {
        "name": "Tree Sprite",
        "stats": {
            "hp_percent": random.randint(60, 80),
            "attack_percent": random.randint(80, 90),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(80, 100),
            "evasion_percent": random.randint(80, 100),
            "crit_chance_percent": random.randint(60, 80),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(50, 70),
            "block_chance_percent": random.randint(40, 60)
        },
        "tier": "low",
        "attack_types": ["normal", "draining", "stunning", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Snake": {
        "name": "Snake",
        "stats": {
            "hp_percent": random.randint(60, 80),
            "attack_percent": random.randint(90, 100),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(90, 110),
            "evasion_percent": random.randint(90, 110),
            "crit_chance_percent": random.randint(70, 90),
            "crit_damage_percent": random.randint(90, 110),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(30, 50),
            "block_chance_percent": random.randint(20, 40)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Forest Hawk": {
        "name": "Forest Hawk",
        "stats": {
            "hp_percent": random.randint(50, 70),
            "attack_percent": random.randint(90, 100),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(100, 120),
            "evasion_percent": random.randint(100, 120),
            "crit_chance_percent": random.randint(80, 100),
            "crit_damage_percent": random.randint(100, 120),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(30, 50),
            "block_chance_percent": random.randint(20, 40)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "stunning", "triple"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Locust": {
        "name": "Locust",
        "stats": {
            "hp_percent": random.randint(50, 70),
            "attack_percent": random.randint(80, 90),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(90, 110),
            "evasion_percent": random.randint(90, 110),
            "crit_chance_percent": random.randint(60, 80),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(30, 50),
            "block_chance_percent": random.randint(20, 40)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "triple"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Leprechaun": {
        "name": "Leprechaun",
        "stats": {
            "hp_percent": random.randint(70, 90),
            "attack_percent": random.randint(85, 95),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(90, 110),
            "evasion_percent": random.randint(100, 120),
            "crit_chance_percent": random.randint(90, 110),
            "crit_damage_percent": random.randint(100, 120),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(40, 60),
            "block_chance_percent": random.randint(50, 70)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "stunning", "draining"],
        "soultype": "standard",
        "monster_type": "warrior"
    },
    
    "Deep Bat": {
        "name": "Deep Bat",
        "stats": {
            "hp_percent": random.randint(60, 80),
            "attack_percent": random.randint(80, 95),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(90, 110),
            "evasion_percent": random.randint(100, 120),
            "crit_chance_percent": random.randint(80, 100),
            "crit_damage_percent": random.randint(90, 110),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(30, 50),
            "block_chance_percent": random.randint(20, 40)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "vampiric", "draining"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Giant Firefly": {
        "name": "Giant Firefly",
        "stats": {
            "hp_percent": random.randint(60, 80),
            "attack_percent": random.randint(85, 95),
            "defence_percent": random.randint(50, 70),
            "accuracy_percent": random.randint(90, 110),
            "evasion_percent": random.randint(100, 120),
            "crit_chance_percent": random.randint(70, 90),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(30, 50),
            "block_chance_percent": random.randint(20, 40)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "burn", "poison"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Deepwood Stalker": {
        "name": "Deepwood Stalker",
        "stats": {
            "hp_percent": random.randint(70, 90),
            "attack_percent": random.randint(85, 100),
            "defence_percent": random.randint(60, 80),
            "accuracy_percent": random.randint(90, 110),
            "evasion_percent": random.randint(80, 100),
            "crit_chance_percent": random.randint(80, 100),
            "crit_damage_percent": random.randint(90, 110),
            "armour_penetration_percent": random.randint(50, 70),
            "damage_reduction_percent": random.randint(40, 60),
            "block_chance_percent": random.randint(30, 50)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Wood Spirit": {
        "name": "Wood Spirit",
        "stats": {
            "hp_percent": random.randint(70, 90),
            "attack_percent": random.randint(86, 95),
            "defence_percent": random.randint(60, 80),
            "accuracy_percent": random.randint(80, 100),
            "evasion_percent": random.randint(70, 90),
            "crit_chance_percent": random.randint(60, 80),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(50, 70),
            "block_chance_percent": random.randint(50, 70)
        },
        "tier": "low",
        "attack_types": ["normal", "draining", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Treant": {
        "name": "Treant",
        "stats": {
            "hp_percent": random.randint(100, 120),     # High HP
            "attack_percent": random.randint(80, 95),
            "defence_percent": random.randint(90, 110), # High defense
            "accuracy_percent": random.randint(50, 70),  # Poor accuracy
            "evasion_percent": random.randint(30, 50),  # Very poor evasion
            "crit_chance_percent": random.randint(40, 60),
            "crit_damage_percent": random.randint(80, 100),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(80, 100),
            "block_chance_percent": random.randint(60, 80)
        },
        "tier": "low",
        "attack_types": ["normal", "power", "stunning", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "spirit"
    },
    # Medium Enemies
    "Alligator": {
        "name": "Alligator",
        "stats": {
            "hp_percent": random.randint(95, 120),     # Very tough hide
            "attack_percent": random.randint(90, 115),  # Strong bite
            "defence_percent": random.randint(95, 120), # Armored scales
            "accuracy_percent": random.randint(55, 80), # Not the most accurate
            "evasion_percent": random.randint(40, 65),   # Slow on land
            "crit_chance_percent": random.randint(50, 75), 
            "crit_damage_percent": random.randint(95, 120), # Powerful bite
            "armour_penetration_percent": random.randint(80, 105), # Strong jaws
            "damage_reduction_percent": random.randint(90, 115),   # Thick scales
            "block_chance_percent": random.randint(75, 100)        # Tough hide
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "reckless", "stunning"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Poison Frog": {
        "name": "Poison Frog",
        "stats": {
            "hp_percent": random.randint(55, 80),       # Small and fragile
            "attack_percent": random.randint(85, 100),
            "defence_percent": random.randint(50, 75),   # Soft body
            "accuracy_percent": random.randint(85, 110),
            "evasion_percent": random.randint(95, 120), # Very jumpy
            "crit_chance_percent": random.randint(75, 100),
            "crit_damage_percent": random.randint(70, 95),
            "armour_penetration_percent": random.randint(65, 90),
            "damage_reduction_percent": random.randint(50, 75),    # No natural armor
            "block_chance_percent": random.randint(40, 65)        # Dodges instead
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Swamp Troll": {
        "name": "Swamp Troll",
        "stats": {
            "hp_percent": random.randint(105, 130),    # Very tough
            "attack_percent": random.randint(95, 120),
            "defence_percent": random.randint(100, 125),
            "accuracy_percent": random.randint(60, 85), # Not very precise
            "evasion_percent": random.randint(50, 75), # Slow
            "crit_chance_percent": random.randint(55, 80),
            "crit_damage_percent": random.randint(100, 125),
            "armour_penetration_percent": random.randint(85, 110),
            "damage_reduction_percent": random.randint(95, 120), # Tough hide
            "block_chance_percent": random.randint(80, 105)      # Uses size to block
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "poison", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Mosquito Swarm": {
        "name": "Mosquito Swarm",
        "stats": {
            "hp_percent": random.randint(55, 80),        # Fragile insects
            "attack_percent": random.randint(85, 110),
            "defence_percent": random.randint(50, 75),   # Very weak individually
            "accuracy_percent": random.randint(105, 130), # Hard to miss as a swarm
            "evasion_percent": random.randint(105, 130), # Hard to hit
            "crit_chance_percent": random.randint(90, 115),
            "crit_damage_percent": random.randint(70, 95),
            "armour_penetration_percent": random.randint(80, 105), # Can find gaps
            "damage_reduction_percent": random.randint(50, 75),    # No protection
            "block_chance_percent": random.randint(40, 65)        # Can't block
        },
        "tier": "medium",
        "attack_types": ["normal", "triple", "poison", "draining"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Bog Witch": {
        "name": "Bog Witch",
        "stats": {
            "hp_percent": random.randint(80, 105),
            "attack_percent": random.randint(90, 115),
            "defence_percent": random.randint(75, 100),
            "accuracy_percent": random.randint(95, 120), # Magical accuracy
            "evasion_percent": random.randint(85, 110),
            "crit_chance_percent": random.randint(80, 105),
            "crit_damage_percent": random.randint(95, 120),
            "armour_penetration_percent": random.randint(85, 110), # Magic ignores armor
            "damage_reduction_percent": random.randint(80, 105),   # Magical protection
            "block_chance_percent": random.randint(70, 95)       # Magical barriers
        },
        "tier": "medium",
        "attack_types": ["normal", "poison", "burn", "draining"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Stone Golem": {
        "name": "Stone Golem",
        "stats": {
            "hp_percent": random.randint(105, 130),    # Stone body
            "attack_percent": random.randint(80, 105),
            "defence_percent": random.randint(105, 130), # Made of stone
            "accuracy_percent": random.randint(60, 85), # Slow
            "evasion_percent": random.randint(50, 75),  # Very slow
            "crit_chance_percent": random.randint(50, 75),
            "crit_damage_percent": random.randint(100, 125),
            "armour_penetration_percent": random.randint(85, 110),
            "damage_reduction_percent": random.randint(105, 130), # Stone body
            "block_chance_percent": random.randint(90, 115)     # Good at blocking
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Cultist": {
        "name": "Cultist",
        "stats": {
            "hp_percent": random.randint(75, 100),
            "attack_percent": random.randint(90, 115),
            "defence_percent": random.randint(70, 95),
            "accuracy_percent": random.randint(90, 115), # Trained fighter
            "evasion_percent": random.randint(85, 110),
            "crit_chance_percent": random.randint(85, 110),
            "crit_damage_percent": random.randint(95, 120),
            "armour_penetration_percent": random.randint(85, 110), # Ritual weapons
            "damage_reduction_percent": random.randint(75, 100),   # Dark magic protection
            "block_chance_percent": random.randint(80, 105)       # Combat training
        },
        "tier": "medium",
        "attack_types": ["normal", "burn", "poison", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "arcane"
    },
    
    "Mummy": {
        "name": "Mummy",
        "stats": {
            "hp_percent": random.randint(90, 115),     # Undead durability
            "attack_percent": random.randint(85, 110),
            "defence_percent": random.randint(95, 120), # Wrapped protection
            "accuracy_percent": random.randint(70, 95), # Stiff movement
            "evasion_percent": random.randint(60, 85),  # Slow
            "crit_chance_percent": random.randint(65, 90),
            "crit_damage_percent": random.randint(90, 115),
            "armour_penetration_percent": random.randint(75, 100),
            "damage_reduction_percent": random.randint(95, 120), # Ancient preservation
            "block_chance_percent": random.randint(85, 110)      # Good at blocking
        },
        "tier": "medium",
        "attack_types": ["normal", "draining", "stunning", "poison"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Animated Statue": {
        "name": "Animated Statue",
        "stats": {
            "hp_percent": random.randint(100, 125),     # Stone construction
            "attack_percent": random.randint(85, 110),
            "defence_percent": random.randint(105, 130), # Made of stone
            "accuracy_percent": random.randint(65, 90), # Rigid movement
            "evasion_percent": random.randint(55, 70),  # Very stiff
            "crit_chance_percent": random.randint(55, 80),
            "crit_damage_percent": random.randint(95, 120),
            "armour_penetration_percent": random.randint(90, 115), # Stone strength
            "damage_reduction_percent": random.randint(100, 125),   # Stone body
            "block_chance_percent": random.randint(95, 120)       # Excellent blocker
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Temple Guardian": {
        "name": "Temple Guardian",
        "stats": {
            "hp_percent": random.randint(100, 125),     # Enchanted durability
            "attack_percent": random.randint(90, 115),  # Combat training
            "defence_percent": random.randint(100, 125), # Magical protection
            "accuracy_percent": random.randint(85, 110), # Well trained
            "evasion_percent": random.randint(70, 95),
            "crit_chance_percent": random.randint(75, 100),
            "crit_damage_percent": random.randint(95, 120),
            "armour_penetration_percent": random.randint(85, 110),
            "damage_reduction_percent": random.randint(95, 120), # Magical wards
            "block_chance_percent": random.randint(100, 125)     # Trained defender
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Mountain Lion": {
        "name": "Mountain Lion",
        "stats": {
            "hp_percent": random.randint(80, 105),
            "attack_percent": random.randint(100, 125),   # Strong predator
            "defence_percent": random.randint(75, 100),   # Light armor
            "accuracy_percent": random.randint(95, 120), # Hunter's precision
            "evasion_percent": random.randint(100, 125), # Very agile
            "crit_chance_percent": random.randint(95, 120), # Knows vital spots
            "crit_damage_percent": random.randint(105, 130), # Powerful pounce
            "armour_penetration_percent": random.randint(90, 115), # Sharp claws
            "damage_reduction_percent": random.randint(65, 90),    # Light hide
            "block_chance_percent": random.randint(50, 75)         # Prefers dodging
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "reckless", "power"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Rock Elemental": {
        "name": "Rock Elemental",
        "stats": {
            "hp_percent": random.randint(105, 130),    # Stone body
            "attack_percent": random.randint(80, 105),
            "defence_percent": random.randint(105, 130), # Stone form
            "accuracy_percent": random.randint(55, 80),  # Slow
            "evasion_percent": random.randint(50, 75),  # Very slow
            "crit_chance_percent": random.randint(50, 75),
            "crit_damage_percent": random.randint(100, 125),
            "armour_penetration_percent": random.randint(95, 120), # Stone crushing
            "damage_reduction_percent": random.randint(105, 130),   # Stone body
            "block_chance_percent": random.randint(95, 120)       # Natural shield
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Harpy": {
        "name": "Harpy",
        "stats": {
            "hp_percent": random.randint(70, 95),      # Light frame
            "attack_percent": random.randint(90, 115),
            "defence_percent": random.randint(65, 90),  # Light bones
            "accuracy_percent": random.randint(100, 125), # Aerial precision
            "evasion_percent": random.randint(105, 130), # Aerial agility
            "crit_chance_percent": random.randint(85, 110),
            "crit_damage_percent": random.randint(95, 120),
            "armour_penetration_percent": random.randint(80, 105),
            "damage_reduction_percent": random.randint(55, 80),    # No armor
            "block_chance_percent": random.randint(55, 70)        # Dodges instead
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "stunning", "triple"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Yeti": {
        "name": "Yeti",
        "stats": {
            "hp_percent": random.randint(100, 125),    # Large and tough
            "attack_percent": random.randint(95, 120), # Strong
            "defence_percent": random.randint(90, 115), # Thick fur
            "accuracy_percent": random.randint(65, 90),
            "evasion_percent": random.randint(60, 85),  # Bulky
            "crit_chance_percent": random.randint(65, 90),
            "crit_damage_percent": random.randint(100, 125), # Powerful strikes
            "armour_penetration_percent": random.randint(85, 110),
            "damage_reduction_percent": random.randint(90, 115), # Thick hide
            "block_chance_percent": random.randint(75, 100)      # Uses size
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "reckless", "freeze"],
        "soultype": "ice",
        "monster_type": "earth"
    },

    "Orc": {
        "name": "Orc",
        "stats": {
            "hp_percent": random.randint(90, 115),    # Tough
            "attack_percent": random.randint(95, 120), # Strong
            "defence_percent": random.randint(85, 110), # Hardy
            "accuracy_percent": random.randint(70, 95), # Unrefined
            "evasion_percent": random.randint(65, 90), # Not agile
            "crit_chance_percent": random.randint(75, 100),
            "crit_damage_percent": random.randint(95, 120),
            "armour_penetration_percent": random.randint(90, 115), # Brutal strength
            "damage_reduction_percent": random.randint(80, 105),    # Tough skin
            "block_chance_percent": random.randint(75, 100)        # Combat trained
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "reckless", "stunning"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Sand Wurm": {
        "name": "Sand Wurm",
        "stats": {
            "hp_percent": random.randint(105, 130),    # Large creature
            "attack_percent": random.randint(90, 115),
            "defence_percent": random.randint(100, 125), # Tough scales
            "accuracy_percent": random.randint(75, 100), # Burrow attack
            "evasion_percent": random.randint(80, 105), # Good at hiding
            "crit_chance_percent": random.randint(70, 95),
            "crit_damage_percent": random.randint(100, 125),
            "armour_penetration_percent": random.randint(95, 120), # Strong bite
            "damage_reduction_percent": random.randint(95, 120),   # Scales
            "block_chance_percent": random.randint(80, 105)        # Scales help block
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "poison", "stunning"],
        "soultype": "standard",
        "monster_type": "earth"
    },
    
    "Dried Mummy": {
        "name": "Dried Mummy",
        "stats": {
            "hp_percent": random.randint(95, 120),     # Preserved durability
            "attack_percent": random.randint(85, 110),
            "defence_percent": random.randint(90, 115), # Bandage wrapping
            "accuracy_percent": random.randint(65, 90), # Stiff movement
            "evasion_percent": random.randint(60, 85),  # Very stiff
            "crit_chance_percent": random.randint(65, 90),
            "crit_damage_percent": random.randint(90, 115),
            "armour_penetration_percent": random.randint(75, 100),
            "damage_reduction_percent": random.randint(95, 120), # Magical preservation
            "block_chance_percent": random.randint(80, 105)      # Ancient training
        },
        "tier": "medium",
        "attack_types": ["normal", "draining", "poison", "burn"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Dust Devil": {
        "name": "Dust Devil",
        "stats": {
            "hp_percent": random.randint(60, 85),       # Ethereal form
            "attack_percent": random.randint(95, 120),
            "defence_percent": random.randint(65, 90),  # Hard to hit but not tough
            "accuracy_percent": random.randint(100, 125),
            "evasion_percent": random.randint(105, 130), # Wind form
            "crit_chance_percent": random.randint(80, 105),
            "crit_damage_percent": random.randint(85, 110),
            "armour_penetration_percent": random.randint(90, 115), # Wind penetration
            "damage_reduction_percent": random.randint(50, 75),    # No physical form
            "block_chance_percent": random.randint(50, 75)        # Can't really block
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "attack_weaken", "triple"],
        "soultype": "standard",
        "monster_type": "spirit"
    },
    
    "Phoenix": {
        "name": "Phoenix",
        "stats": {
            "hp_percent": random.randint(150, 160),       # High HP to represent rebirth
            "attack_percent": random.randint(95, 120),
            "defence_percent": random.randint(65, 90),  # Hard to hit but not tough
            "accuracy_percent": random.randint(100, 125),
            "evasion_percent": random.randint(105, 130), # Wind form
            "crit_chance_percent": random.randint(100, 130),
            "crit_damage_percent": random.randint(100, 125),
            "armour_penetration_percent": random.randint(100, 125), # Fire penetration
            "damage_reduction_percent": random.randint(30, 55),    # Weak physical form
            "block_chance_percent": random.randint(50, 75)        # Can't really block
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "burn", "triple"],
        "soultype": "standard",
        "monster_type": "fire"
    },

    "Desert Bandit": {
        "name": "Desert Bandit",
        "stats": {
            "hp_percent": random.randint(75, 100),
            "attack_percent": random.randint(90, 115),  # Combat trained
            "defence_percent": random.randint(80, 105),  # Light armor
            "accuracy_percent": random.randint(95, 120), # Well practiced
            "evasion_percent": random.randint(90, 115), # Agile fighter
            "crit_chance_percent": random.randint(85, 110), # Knows weak spots
            "crit_damage_percent": random.randint(95, 120),
            "armour_penetration_percent": random.randint(90, 115), # Knows where to strike
            "damage_reduction_percent": random.randint(70, 95),    # Light armor
            "block_chance_percent": random.randint(80, 105)        # Combat training
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Leopard": {
        "name": "Leopard",
        "stats": {
            "hp_percent": random.randint(75, 100),       # Lean predator
            "attack_percent": random.randint(100, 125),  # Strong hunter
            "defence_percent": random.randint(65, 90),  # Light frame
            "accuracy_percent": random.randint(105, 130), # Expert hunter
            "evasion_percent": random.randint(105, 130), # Extremely agile
            "crit_chance_percent": random.randint(100, 125), # Precise strikes
            "crit_damage_percent": random.randint(105, 130), # Deadly pounce
            "armour_penetration_percent": random.randint(95, 120), # Sharp claws
            "damage_reduction_percent": random.randint(55, 80),     # Light hide
            "block_chance_percent": random.randint(50, 75)         # Dodges instead
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "reckless", "triple"],
        "soultype": "standard",
        "monster_type": "grass"
    },
    
    # Medium-Hard enemies
    "Canyon Cougar": {
        "name": "Canyon Cougar",
        "stats": {
            "hp_percent": random.randint(90, 120),
            "attack_percent": random.randint(110, 140),   # Very strong attack
            "defence_percent": random.randint(80, 110),
            "accuracy_percent": random.randint(105, 135), # Good hunter
            "evasion_percent": random.randint(110, 140),  # Extremely agile
            "crit_chance_percent": random.randint(100, 130), # Good at vital spots
            "crit_damage_percent": random.randint(110, 140), # Powerful strikes
            "armour_penetration_percent": random.randint(95, 125), # Sharp claws
            "damage_reduction_percent": random.randint(65, 95),    # Not very armored
            "block_chance_percent": random.randint(50, 80)         # Dodges rather than blocks
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "double", "reckless", "power", "stunning"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Twisted Mesquite": {
        "name": "Twisted Mesquite",
        "stats": {
            "hp_percent": random.randint(110, 140),     # Very tough, ancient tree
            "attack_percent": random.randint(90, 120),
            "defence_percent": random.randint(105, 135), # Hard bark
            "accuracy_percent": random.randint(75, 105), # Slow but deliberate
            "evasion_percent": random.randint(50, 70),  # Stationary tree
            "crit_chance_percent": random.randint(70, 100),
            "crit_damage_percent": random.randint(95, 125),
            "armour_penetration_percent": random.randint(80, 110),
            "damage_reduction_percent": random.randint(100, 130), # Very resistant
            "block_chance_percent": random.randint(90, 120)     # Good at blocking
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "poison", "stunning", "draining", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Dustier Devil": {
        "name": "Dustier Devil",
        "stats": {
            "hp_percent": random.randint(75, 105),      # Insubstantial form
            "attack_percent": random.randint(100, 130),
            "defence_percent": random.randint(65, 95),  # Hard to hit but not tough
            "accuracy_percent": random.randint(110, 140),
            "evasion_percent": random.randint(110, 140), # Extremely evasive
            "crit_chance_percent": random.randint(90, 120),
            "crit_damage_percent": random.randint(100, 130),
            "armour_penetration_percent": random.randint(85, 115),
            "damage_reduction_percent": random.randint(50, 80),  # No physical armor
            "block_chance_percent": random.randint(50, 70)      # Doesn't block, evades
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "double", "stunning", "triple", "draining"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Petrified Warrior": {
        "name": "Petrified Warrior",
        "stats": {
            "hp_percent": random.randint(100, 130),
            "attack_percent": random.randint(95, 125),
            "defence_percent": random.randint(110, 140),  # Stone body
            "accuracy_percent": random.randint(80, 110),  # Trained warrior
            "evasion_percent": random.randint(50, 80),   # Heavy stone form
            "crit_chance_percent": random.randint(75, 105), # Trained
            "crit_damage_percent": random.randint(100, 130),
            "armour_penetration_percent": random.randint(90, 120),
            "damage_reduction_percent": random.randint(105, 135), # Stone body
            "block_chance_percent": random.randint(95, 125)     # Skilled defender
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "power", "stunning", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Thunderbird": {
        "name": "Thunderbird",
        "stats": {
            "hp_percent": random.randint(85, 115),
            "attack_percent": random.randint(105, 135),
            "defence_percent": random.randint(65, 95),   # Light bones
            "accuracy_percent": random.randint(110, 140), # Excellent vision
            "evasion_percent": random.randint(110, 140), # Aerial agility
            "crit_chance_percent": random.randint(100, 130),
            "crit_damage_percent": random.randint(110, 140),
            "armour_penetration_percent": random.randint(95, 125), # Lightning attacks
            "damage_reduction_percent": random.randint(60, 90),    # Light frame
            "block_chance_percent": random.randint(50, 80)         # Dodges instead
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "double", "stunning", "triple", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "lightning"
    },

    "Valley Tiger": {
        "name": "Valley Tiger",
        "stats": {
            "hp_percent": random.randint(95, 125),
            "attack_percent": random.randint(110, 140),   # Apex predator
            "defence_percent": random.randint(75, 105),   # Medium hide
            "accuracy_percent": random.randint(105, 135), # Expert hunter
            "evasion_percent": random.randint(100, 130),  # Very agile
            "crit_chance_percent": random.randint(105, 135), # Knows vital spots
            "crit_damage_percent": random.randint(110, 140), # Powerful strikes
            "armour_penetration_percent": random.randint(100, 130), # Sharp claws/teeth
            "damage_reduction_percent": random.randint(65, 95),    # Hide only
            "block_chance_percent": random.randint(55, 85)         # Prefers evasion
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "double", "reckless", "triple", "power"],
        "soultype": "standard",
        "monster_type": "grass"
    },
    
    # Hard Enemies
    "Venomous Hydra": {
        "name": "Venomous Hydra",
        "stats": {
            "hp_percent": random.randint(115, 150),      # Multiple heads = high HP
            "attack_percent": random.randint(110, 145),  # Multiple attacks
            "defence_percent": random.randint(95, 130), # Tough but not invincible
            "accuracy_percent": random.randint(100, 135), # Multiple heads help aim
            "evasion_percent": random.randint(60, 95),  # Large target
            "crit_chance_percent": random.randint(95, 130), # Good at finding weak spots
            "crit_damage_percent": random.randint(120, 150), # Devastating bites
            "armour_penetration_percent": random.randint(100, 135), # Sharp fangs
            "damage_reduction_percent": random.randint(85, 120),    # Scales
            "block_chance_percent": random.randint(50, 85)         # Too aggressive to block
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "poison", "double", "triple"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Plague Bearer": {
        "name": "Plague Bearer",
        "stats": {
            "hp_percent": random.randint(85, 120),       # Diseased form
            "attack_percent": random.randint(80, 115),   # Not physically strong
            "defence_percent": random.randint(75, 110),
            "accuracy_percent": random.randint(105, 140), # Disease spreads easily
            "evasion_percent": random.randint(65, 100),  # Shambling
            "crit_chance_percent": random.randint(100, 135), # Finds weak spots
            "crit_damage_percent": random.randint(110, 145), # Infection damage
            "armour_penetration_percent": random.randint(115, 150), # Disease ignores armor
            "damage_reduction_percent": random.randint(70, 105),    # Decaying body
            "block_chance_percent": random.randint(50, 85)         # Doesn't block much
        },
        "tier": "hard",
        "attack_types": ["normal", "poison", "vampiric", "draining", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Mire Leviathan": {
        "name": "Mire Leviathan",
        "stats": {
            "hp_percent": random.randint(120, 150),      # Massive size
            "attack_percent": random.randint(115, 150),  # Incredible strength
            "defence_percent": random.randint(110, 145), # Natural armor
            "accuracy_percent": random.randint(65, 100),  # Unwieldy
            "evasion_percent": random.randint(50, 85),   # Too big to dodge
            "crit_chance_percent": random.randint(60, 95), # Not precise
            "crit_damage_percent": random.randint(115, 150), # Crushing force
            "armour_penetration_percent": random.randint(105, 140), # Pure strength
            "damage_reduction_percent": random.randint(110, 145),   # Thick hide
            "block_chance_percent": random.randint(100, 135)       # Uses size to block
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "stunning", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Toxic Shambler": {
        "name": "Toxic Shambler",
        "stats": {
            "hp_percent": random.randint(80, 115),       # Rotting form
            "attack_percent": random.randint(75, 110),   # Not strong
            "defence_percent": random.randint(65, 100),  # Decaying
            "accuracy_percent": random.randint(90, 125),
            "evasion_percent": random.randint(55, 90),  # Shambling
            "crit_chance_percent": random.randint(95, 130),
            "crit_damage_percent": random.randint(105, 140),
            "armour_penetration_percent": random.randint(110, 145), # Toxic corrodes
            "damage_reduction_percent": random.randint(100, 135),   # Numb to pain
            "block_chance_percent": random.randint(55, 90)        # Poor coordination
        },
        "tier": "hard",
        "attack_types": ["normal", "poison", "vampiric", "draining", "double"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Swamp Hag": {
        "name": "Swamp Hag",
        "stats": {
            "hp_percent": random.randint(75, 110),       # Frail form
            "attack_percent": random.randint(110, 145),  # Magical power
            "defence_percent": random.randint(70, 105),  # Physically weak
            "accuracy_percent": random.randint(115, 150), # Magical precision
            "evasion_percent": random.randint(100, 135), # Unnatural movement
            "crit_chance_percent": random.randint(105, 140), # Knows weaknesses
            "crit_damage_percent": random.randint(110, 145), # Hexes
            "armour_penetration_percent": random.randint(120, 150), # Magic ignores armor
            "damage_reduction_percent": random.randint(85, 120),    # Magical wards
            "block_chance_percent": random.randint(60, 95)        # Magical barriers
        },
        "tier": "hard",
        "attack_types": ["normal", "poison", "stunning", "draining", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Ancient Golem": {
        "name": "Ancient Golem",
        "stats": {
            "hp_percent": random.randint(120, 150),      # Stone construction
            "attack_percent": random.randint(105, 140),
            "defence_percent": random.randint(120, 150), # Stone body
            "accuracy_percent": random.randint(60, 95),  # Slow
            "evasion_percent": random.randint(55, 80),   # Very slow
            "crit_chance_percent": random.randint(55, 90), # Not precise
            "crit_damage_percent": random.randint(110, 145), # Crushing blows
            "armour_penetration_percent": random.randint(110, 145), # Stone strength
            "damage_reduction_percent": random.randint(115, 150),   # Nearly impervious
            "block_chance_percent": random.randint(110, 145)       # Living wall
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "stunning", "damage_reflect", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },
    
    "Cursed Pharaoh": {
        "name": "Cursed Pharaoh",
        "stats": {
            "hp_percent": random.randint(100, 135),      # Undead durability
            "attack_percent": random.randint(85, 120),   # Not physically strong
            "defence_percent": random.randint(95, 130), # Ancient wrappings
            "accuracy_percent": random.randint(80, 115),  # Stiff movement
            "evasion_percent": random.randint(55, 90),  # Very stiff
            "crit_chance_percent": random.randint(75, 110),
            "crit_damage_percent": random.randint(90, 125),
            "armour_penetration_percent": random.randint(120, 150), # Curse ignores armor
            "damage_reduction_percent": random.randint(105, 140),   # Ancient magic protection
            "block_chance_percent": random.randint(90, 125)       # Ancient combat training
        },
        "tier": "hard",
        "attack_types": ["normal", "poison", "stunning", "draining", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Temporal Anomaly": {
        "name": "Temporal Anomaly",
        "stats": {
            "hp_percent": random.randint(65, 100),       # Unstable form
            "attack_percent": random.randint(85, 120),   # Not physically strong
            "defence_percent": random.randint(60, 95),  # Barely physical
            "accuracy_percent": random.randint(115, 150), # Time manipulation
            "evasion_percent": random.randint(120, 150), # Phase shifting
            "crit_chance_percent": random.randint(105, 140), # Time strikes
            "crit_damage_percent": random.randint(110, 145),
            "armour_penetration_percent": random.randint(115, 150), # Time ignores armor
            "damage_reduction_percent": random.randint(50, 85),     # Unstable form
            "block_chance_percent": random.randint(55, 80)         # Dodges instead
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "stunning", "defence_break", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "void"
    },

    "Ruin Wraith": {
        "name": "Ruin Wraith",
        "stats": {
            "hp_percent": random.randint(70, 105),       # Spectral form
            "attack_percent": random.randint(105, 140),  # Spectral power
            "defence_percent": random.randint(60, 95),  # Incorporeal
            "accuracy_percent": random.randint(110, 145), # Ghostly precision
            "evasion_percent": random.randint(115, 150), # Phase through attacks
            "crit_chance_percent": random.randint(100, 135), # Strike through souls
            "crit_damage_percent": random.randint(110, 145),
            "armour_penetration_percent": random.randint(120, 150), # Ghost through armor
            "damage_reduction_percent": random.randint(55, 90),    # Can't block physical
            "block_chance_percent": random.randint(55, 80)         # Phases instead
        },
        "tier": "hard",
        "attack_types": ["normal", "draining", "vampiric", "stunning", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Forgotten Titan": {
        "name": "Forgotten Titan",
        "stats": {
            "hp_percent": random.randint(120, 150),      # Colossal size
            "attack_percent": random.randint(115, 150),  # Immense strength
            "defence_percent": random.randint(110, 145), # Ancient armor
            "accuracy_percent": random.randint(60, 95),  # Too big to aim well
            "evasion_percent": random.randint(55, 80),   # Massive target
            "crit_chance_percent": random.randint(55, 90), # Not precise
            "crit_damage_percent": random.randint(115, 150), # Devastating blows
            "armour_penetration_percent": random.randint(105, 140), # Pure strength
            "damage_reduction_percent": random.randint(110, 145),   # Ancient protection
            "block_chance_percent": random.randint(100, 135)       # Uses size
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Frost Giant": {
        "name": "Frost Giant",
        "stats": {
            "hp_percent": random.randint(115, 150),      # Giant size
            "attack_percent": random.randint(110, 145),  # Giant strength
            "defence_percent": random.randint(105, 140), # Ice armor
            "accuracy_percent": random.randint(65, 100),  # Slow attacks
            "evasion_percent": random.randint(50, 85),   # Too big
            "crit_chance_percent": random.randint(60, 95), # Not precise
            "crit_damage_percent": random.randint(110, 145), # Crushing blows
            "armour_penetration_percent": random.randint(100, 135),
            "damage_reduction_percent": random.randint(105, 140),   # Ice protection
            "block_chance_percent": random.randint(95, 130)       # Ice shield
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "stunning", "freeze", "defence_break"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Storm Harpy": {
        "name": "Storm Harpy",
        "stats": {
            "hp_percent": random.randint(75, 110),       # Light frame
            "attack_percent": random.randint(100, 135),
            "defence_percent": random.randint(65, 100),  # Fragile
            "accuracy_percent": random.randint(110, 145), # Aerial precision
            "evasion_percent": random.randint(115, 150), # Aerial mastery
            "crit_chance_percent": random.randint(105, 140), # Diving strikes
            "crit_damage_percent": random.randint(110, 145),
            "armour_penetration_percent": random.randint(105, 140), # Lightning
            "damage_reduction_percent": random.randint(55, 90),    # No armor
            "block_chance_percent": random.randint(50, 85)         # Dodges instead
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "stunning", "triple", "attack_weaken"],
        "soultype": "lightning",
        "monster_type": "earth"
    },
    
    "Avalanche Elemental": {
        "name": "Avalanche Elemental",
        "stats": {
            "hp_percent": random.randint(110, 145),      # Mass of ice and snow
            "attack_percent": random.randint(105, 140),  # Crushing force
            "defence_percent": random.randint(115, 150), # Ice armor
            "accuracy_percent": random.randint(55, 90),  # Wild force
            "evasion_percent": random.randint(55, 80),   # Slow moving mass
            "crit_chance_percent": random.randint(60, 95), # Not precise
            "crit_damage_percent": random.randint(110, 145), # Overwhelming force
            "armour_penetration_percent": random.randint(105, 140), # Pure mass
            "damage_reduction_percent": random.randint(110, 145),   # Ice protection
            "block_chance_percent": random.randint(100, 135)       # Natural shield
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "freeze", "stunning", "damage_reflect"],
        "soultype": "ice",
        "monster_type": "earth"
    },

    "Mountain Wyvern": {
        "name": "Mountain Wyvern",
        "stats": {
            "hp_percent": random.randint(100, 135),      # Tough but agile
            "attack_percent": random.randint(110, 145),  # Powerful hunter
            "defence_percent": random.randint(85, 120),  # Dragon scales
            "accuracy_percent": random.randint(105, 140), # Hunter's eye
            "evasion_percent": random.randint(100, 135), # Aerial agility
            "crit_chance_percent": random.randint(95, 130), # Precise strikes
            "crit_damage_percent": random.randint(110, 145), # Devastating attacks
            "armour_penetration_percent": random.randint(105, 140), # Sharp claws
            "damage_reduction_percent": random.randint(80, 115),    # Dragon hide
            "block_chance_percent": random.randint(60, 95)        # Prefers dodging
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "reckless", "stunning", "poison"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Yeti Alpha": {
        "name": "Yeti Alpha",
        "stats": {
            "hp_percent": random.randint(115, 150),      # Massive earth
            "attack_percent": random.randint(110, 145),  # Primal strength
            "defence_percent": random.randint(100, 135), # Thick fur
            "accuracy_percent": random.randint(75, 110),  # Wild swings
            "evasion_percent": random.randint(60, 95),  # Bulky
            "crit_chance_percent": random.randint(75, 110),
            "crit_damage_percent": random.randint(115, 150), # Crushing blows
            "armour_penetration_percent": random.randint(100, 135), # Raw power
            "damage_reduction_percent": random.randint(95, 130),   # Thick hide
            "block_chance_percent": random.randint(85, 120)        # Uses size
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "freeze", "stunning"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Fire Elemental": {
        "name": "Fire Elemental",
        "stats": {
            "hp_percent": random.randint(85, 120),       # Unstable form
            "attack_percent": random.randint(115, 150),  # Intense heat
            "defence_percent": random.randint(70, 105),  # Fluid form
            "accuracy_percent": random.randint(100, 135),
            "evasion_percent": random.randint(100, 135), # Fluid movement
            "crit_chance_percent": random.randint(95, 130),
            "crit_damage_percent": random.randint(115, 150), # Melting strikes
            "armour_penetration_percent": random.randint(115, 150), # Heat pierces armor
            "damage_reduction_percent": random.randint(60, 95),    # Can't block physical
            "block_chance_percent": random.randint(50, 85)         # Fluid form
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "burn", "stunning"],
        "soultype": "standard",
        "monster_type": "fire"
    },

    "Sandstorm Djinn": {
        "name": "Sandstorm Djinn",
        "stats": {
            "hp_percent": random.randint(75, 110),       # Ethereal being
            "attack_percent": random.randint(95, 130),
            "defence_percent": random.randint(65, 100),  # Insubstantial
            "accuracy_percent": random.randint(110, 145), # Sand control
            "evasion_percent": random.randint(115, 150), # Wind form
            "crit_chance_percent": random.randint(100, 135),
            "crit_damage_percent": random.randint(105, 140),
            "armour_penetration_percent": random.randint(110, 145), # Sand penetrates
            "damage_reduction_percent": random.randint(55, 90),    # Can't block physical
            "block_chance_percent": random.randint(50, 85)         # Dodges instead
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "stunning", "damage_reflect", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Mirage Assassin": {
        "name": "Mirage Assassin",
        "stats": {
            "hp_percent": random.randint(65, 100),       # Light frame
            "attack_percent": random.randint(110, 145),  # Lethal strikes
            "defence_percent": random.randint(60, 95),  # No armor
            "accuracy_percent": random.randint(115, 150), # Expert precision
            "evasion_percent": random.randint(120, 150), # Nearly invisible
            "crit_chance_percent": random.randint(115, 150), # Vital strikes
            "crit_damage_percent": random.randint(115, 150), # Assassination
            "armour_penetration_percent": random.randint(110, 145), # Finds weak points
            "damage_reduction_percent": random.randint(50, 85),     # No armor
            "block_chance_percent": random.randint(55, 80)         # Pure evasion
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "poison", "triple", "stunning"],
        "soultype": "standard",
        "monster_type": "warrior"
    },
    
    "Sunburst Phoenix": {
        "name": "Sunburst Phoenix",
        "stats": {
            "hp_percent": random.randint(85, 120),       # Magical but fragile
            "attack_percent": random.randint(110, 145),  # Solar power
            "defence_percent": random.randint(70, 105),  # Light frame
            "accuracy_percent": random.randint(105, 140), # Precise striker
            "evasion_percent": random.randint(110, 145), # Aerial master
            "crit_chance_percent": random.randint(100, 135),
            "crit_damage_percent": random.randint(115, 150), # Solar fury
            "armour_penetration_percent": random.randint(115, 150), # Heat melts armor
            "damage_reduction_percent": random.randint(60, 95),    # Light frame
            "block_chance_percent": random.randint(50, 85)         # Dodges instead
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "burn", "stunning"],
        "soultype": "standard",
        "monster_type": "fire"
    },

    "Desert Colossus": {
        "name": "Desert Colossus",
        "stats": {
            "hp_percent": random.randint(120, 150),      # Massive size
            "attack_percent": random.randint(110, 145),  # Giant strength
            "defence_percent": random.randint(115, 150), # Ancient stone
            "accuracy_percent": random.randint(60, 95),  # Slow
            "evasion_percent": random.randint(55, 80),   # Too large
            "crit_chance_percent": random.randint(55, 90), # Not precise
            "crit_damage_percent": random.randint(110, 145), # Crushing force
            "armour_penetration_percent": random.randint(105, 140), # Pure strength
            "damage_reduction_percent": random.randint(110, 145),   # Stone body
            "block_chance_percent": random.randint(100, 135)       # Living wall
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "stunning", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Nightmare Stalker": {
        "name": "Nightmare Stalker",
        "stats": {
            "hp_percent": random.randint(75, 110),       # Shadow form
            "attack_percent": random.randint(105, 140),  # Terror strikes
            "defence_percent": random.randint(65, 100),  # No physical form
            "accuracy_percent": random.randint(110, 145), # Strikes fears
            "evasion_percent": random.randint(115, 150), # Shadow movement
            "crit_chance_percent": random.randint(110, 145), # Knows fears
            "crit_damage_percent": random.randint(110, 145), # Terror damage
            "armour_penetration_percent": random.randint(115, 150), # Fear ignores armor
            "damage_reduction_percent": random.randint(55, 90),    # No physical form
            "block_chance_percent": random.randint(55, 80)         # Phases through
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "vampiric", "stunning", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "grass"
    },

    "Void Weaver": {
        "name": "Void Weaver",
        "stats": {
            "hp_percent": random.randint(70, 105),       # Ethereal
            "attack_percent": random.randint(105, 140),  # Void power
            "defence_percent": random.randint(60, 95),  # No physical form
            "accuracy_percent": random.randint(105, 140), # Reality warping
            "evasion_percent": random.randint(115, 150), # Space bending
            "crit_chance_percent": random.randint(105, 140),
            "crit_damage_percent": random.randint(110, 145),
            "armour_penetration_percent": random.randint(120, 150), # Void piercing
            "damage_reduction_percent": random.randint(60, 95),    # Can't block physical
            "block_chance_percent": random.randint(50, 85)         # Warps space instead
        },
        "tier": "hard",
        "attack_types": ["normal", "draining", "stunning", "attack_weaken", "poison"],
        "soultype": "standard",
        "monster_type": "void"
    },

    "Shadow Dragon": {
        "name": "Shadow Dragon",
        "stats": {
            "hp_percent": random.randint(105, 140),      # Dragon might
            "attack_percent": random.randint(110, 145),  # Dragon strength
            "defence_percent": random.randint(90, 125), # Shadow scales
            "accuracy_percent": random.randint(100, 135), # Dragon precision
            "evasion_percent": random.randint(105, 140), # Shadow form
            "crit_chance_percent": random.randint(100, 135),
            "crit_damage_percent": random.randint(110, 145), # Dragon fury
            "armour_penetration_percent": random.randint(105, 140), # Shadow penetration
            "damage_reduction_percent": random.randint(85, 120),    # Shadow defense
            "block_chance_percent": random.randint(65, 100)        # Prefers evasion
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "triple", "stunning", "draining"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Ethereal Banshee": {
        "name": "Ethereal Banshee",
        "stats": {
            "hp_percent": random.randint(65, 100),       # Spirit form
            "attack_percent": random.randint(110, 145),  # Sonic power
            "defence_percent": random.randint(55, 90),  # Incorporeal
            "accuracy_percent": random.randint(115, 150), # Sonic precision
            "evasion_percent": random.randint(115, 150), # Spirit movement
            "crit_chance_percent": random.randint(105, 140), # Sonic resonance
            "crit_damage_percent": random.randint(115, 150), # Deadly screams
            "armour_penetration_percent": random.randint(120, 150), # Sound ignores armor
            "damage_reduction_percent": random.randint(50, 85),     # No physical form
            "block_chance_percent": random.randint(50, 75)         # Can't block
        },
        "tier": "hard",
        "attack_types": ["normal", "draining", "stunning", "attack_weaken", "double"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Abyssal Behemoth": {
        "name": "Abyssal Behemoth",
        "stats": {
            "hp_percent": random.randint(120, 150),      # Massive size
            "attack_percent": random.randint(115, 150),  # Overwhelming force
            "defence_percent": random.randint(110, 145), # Ancient hide
            "accuracy_percent": random.randint(60, 95),  # Unwieldy
            "evasion_percent": random.randint(55, 80),   # Too massive
            "crit_chance_percent": random.randint(65, 100),
            "crit_damage_percent": random.randint(115, 150), # Crushing force
            "armour_penetration_percent": random.randint(105, 140), # Pure power
            "damage_reduction_percent": random.randint(110, 145),   # Ancient protection
            "block_chance_percent": random.randint(100, 135)       # Natural barrier
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "void"
    },
    
    # Very Hard Enemies
    "Necropolis Guardian": {
        "name": "Necropolis Guardian",
        "stats": {
            "hp_percent": random.randint(120, 160),      # Ancient power
            "attack_percent": random.randint(110, 150),  # Death strength
            "defence_percent": random.randint(125, 160), # Undead fortification
            "accuracy_percent": random.randint(80, 120),  # Slow but purposeful
            "evasion_percent": random.randint(60, 100),  # Massive form
            "crit_chance_percent": random.randint(75, 115), # Not precise
            "crit_damage_percent": random.randint(120, 160), # Death blows
            "armour_penetration_percent": random.randint(115, 155), # Ancient weapons
            "damage_reduction_percent": random.randint(120, 160),   # Death's protection
            "block_chance_percent": random.randint(110, 150)       # Guardian's duty
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "draining", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Soul Reaver": {
        "name": "Soul Reaver",
        "stats": {
            "hp_percent": random.randint(90, 130),      # Spirit form
            "attack_percent": random.randint(120, 160),  # Soul stealing
            "defence_percent": random.randint(75, 115),  # Ethereal
            "accuracy_percent": random.randint(115, 155), # Soul seeking
            "evasion_percent": random.randint(120, 160), # Spirit movement
            "crit_chance_percent": random.randint(115, 155), # Soul weak points
            "crit_damage_percent": random.randint(120, 160), # Soul rending
            "armour_penetration_percent": random.randint(125, 160), # Spirit piercing
            "damage_reduction_percent": random.randint(70, 110),    # No physical form
            "block_chance_percent": random.randint(60, 100)        # Phases through
        },
        "tier": "very-hard",
        "attack_types": ["normal", "triple", "vampiric", "draining", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Bone Colossus": {
        "name": "Bone Colossus",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Massive construct
            "attack_percent": random.randint(120, 160),  # Enormous strength
            "defence_percent": random.randint(125, 160), # Wall of bone
            "accuracy_percent": random.randint(70, 110),  # Unwieldy size
            "evasion_percent": random.randint(55, 95),  # Too big
            "crit_chance_percent": random.randint(65, 105), # Not precise
            "crit_damage_percent": random.randint(125, 160), # Crushing force
            "armour_penetration_percent": random.randint(115, 155), # Pure mass
            "damage_reduction_percent": random.randint(120, 160),   # Bone fortress
            "block_chance_percent": random.randint(110, 150)       # Living wall
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "reckless", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Spectral Devourer": {
        "name": "Spectral Devourer",
        "stats": {
            "hp_percent": random.randint(85, 125),       # Spirit essence
            "attack_percent": random.randint(120, 160),  # Consuming force
            "defence_percent": random.randint(70, 110),  # No physical form
            "accuracy_percent": random.randint(120, 160), # Spirit hunting
            "evasion_percent": random.randint(125, 160), # Ghost-like
            "crit_chance_percent": random.randint(120, 160), # Vital consumption
            "crit_damage_percent": random.randint(120, 160), # Soul devouring
            "armour_penetration_percent": random.randint(125, 160), # Spirit teeth
            "damage_reduction_percent": random.randint(65, 105),    # Ethereal form
            "block_chance_percent": random.randint(55, 95)        # Can't block
        },
        "tier": "very-hard",
        "attack_types": ["normal", "vampiric", "poison", "draining", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Lich King": {
        "name": "Lich King",
        "stats": {
            "hp_percent": random.randint(110, 150),      # Undead resilience
            "attack_percent": random.randint(120, 160),  # Death magic
            "defence_percent": random.randint(105, 145), # Magical barriers
            "accuracy_percent": random.randint(115, 155), # Ancient precision
            "evasion_percent": random.randint(105, 145), # Teleportation
            "crit_chance_percent": random.randint(115, 155), # Death knowledge
            "crit_damage_percent": random.randint(120, 160), # Fatal magic
            "armour_penetration_percent": random.randint(125, 160), # Death touch
            "damage_reduction_percent": random.randint(115, 155),   # Magical wards
            "block_chance_percent": random.randint(100, 140)       # Spell shields
        },
        "tier": "very-hard",
        "attack_types": ["normal", "draining", "poison", "freeze", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "undead"
    },
    
    "Timeless Sphinx": {
        "name": "Timeless Sphinx",
        "stats": {
            "hp_percent": random.randint(100, 140),      # Ancient but not physical
            "attack_percent": random.randint(115, 155),  # Time manipulation
            "defence_percent": random.randint(95, 135), # Temporal shields
            "accuracy_percent": random.randint(125, 160), # Sees all time
            "evasion_percent": random.randint(120, 160), # Time shifting
            "crit_chance_percent": random.randint(120, 160), # Knows weak moments
            "crit_damage_percent": random.randint(120, 160), # Temporal strikes
            "armour_penetration_percent": random.randint(125, 160), # Time piercing
            "damage_reduction_percent": random.randint(105, 145),   # Time warping
            "block_chance_percent": random.randint(80, 120)        # Prefers evasion
        },
        "tier": "very-hard",
        "attack_types": ["normal", "stunning", "draining", "poison", "attack_weaken", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "arcane"
    },

    "Eternal Pharaoh": {
        "name": "Eternal Pharaoh",
        "stats": {
            "hp_percent": random.randint(115, 155),      # Immortal body
            "attack_percent": random.randint(110, 150),  # Ancient might
            "defence_percent": random.randint(120, 160), # Divine protection
            "accuracy_percent": random.randint(100, 140), # Measured strikes
            "evasion_percent": random.randint(75, 115),  # Regal movement
            "crit_chance_percent": random.randint(105, 145), # Divine precision
            "crit_damage_percent": random.randint(115, 155), # God's wrath
            "armour_penetration_percent": random.randint(120, 160), # Divine power
            "damage_reduction_percent": random.randint(120, 160),   # Sacred wards
            "block_chance_percent": random.randint(110, 150)       # Divine shield
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "poison", "draining", "defence_break", "stunning"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Anubis Reborn": {
        "name": "Anubis Reborn",
        "stats": {
            "hp_percent": random.randint(110, 150),      # Divine form
            "attack_percent": random.randint(120, 160),  # Death god's might
            "defence_percent": random.randint(105, 145), 
            "accuracy_percent": random.randint(120, 160), # Death's precision
            "evasion_percent": random.randint(115, 155), # Divine grace
            "crit_chance_percent": random.randint(120, 160), # Death's knowledge
            "crit_damage_percent": random.randint(120, 160), # Divine strikes
            "armour_penetration_percent": random.randint(115, 155), # Soul rending
            "damage_reduction_percent": random.randint(100, 140),   # Divine form
            "block_chance_percent": random.randint(90, 130)       # Death's shield
        },
        "tier": "very-hard",
        "attack_types": ["normal", "vampiric", "stunning", "double", "defence_break", "triple"],
        "soultype": "standard",
        "monster_type": "arcane"
    },

    "Mummy Emperor": {
        "name": "Mummy Emperor",
        "stats": {
            "hp_percent": random.randint(120, 160),      # Imperial preservation
            "attack_percent": random.randint(105, 145),  # Ancient strength
            "defence_percent": random.randint(125, 160), # Royal wrappings
            "accuracy_percent": random.randint(85, 125),  # Stiff movement
            "evasion_percent": random.randint(65, 105),  # Very stiff
            "crit_chance_percent": random.randint(90, 130),
            "crit_damage_percent": random.randint(110, 150),
            "armour_penetration_percent": random.randint(115, 155), # Ancient weapons
            "damage_reduction_percent": random.randint(120, 160),   # Magical preservation
            "block_chance_percent": random.randint(115, 155)       # Royal guard training
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "poison", "stunning", "damage_reflect", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Living Obelisk": {
        "name": "Living Obelisk",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Stone construct
            "attack_percent": random.randint(115, 155),  # Massive weight
            "defence_percent": random.randint(130, 160), # Solid stone
            "accuracy_percent": random.randint(70, 110),  # Immobile
            "evasion_percent": random.randint(55, 95),  # Can't dodge
            "crit_chance_percent": random.randint(65, 105), # Not precise
            "crit_damage_percent": random.randint(120, 160), # Crushing weight
            "armour_penetration_percent": random.randint(120, 160), # Stone force
            "damage_reduction_percent": random.randint(125, 160),   # Stone body
            "block_chance_percent": random.randint(120, 160)       # Living wall
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "reckless", "damage_reflect", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Apocalypse Horseman": {
        "name": "Apocalypse Horseman",
        "stats": {
            "hp_percent": random.randint(110, 150),      # Supernatural being
            "attack_percent": random.randint(125, 160),  # Harbinger of doom
            "defence_percent": random.randint(100, 140), 
            "accuracy_percent": random.randint(120, 160), # Never misses
            "evasion_percent": random.randint(115, 155), # Supernatural grace
            "crit_chance_percent": random.randint(120, 160), # Death strikes
            "crit_damage_percent": random.randint(125, 160), # Apocalyptic force
            "armour_penetration_percent": random.randint(120, 160), # Divine weapon
            "damage_reduction_percent": random.randint(105, 145),   # Supernatural form
            "block_chance_percent": random.randint(90, 130)       # Prefers offense
        },
        "tier": "very-hard",
        "attack_types": ["normal", "reckless", "poison", "draining", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "warrior"
    },
    
    "Abyssal Wyrm": {
        "name": "Abyssal Wyrm",
        "stats": {
            "hp_percent": random.randint(115, 155),      # Massive dragon
            "attack_percent": random.randint(120, 160),  # Ancient dragon might
            "defence_percent": random.randint(110, 150), # Dragon scales
            "accuracy_percent": random.randint(110, 150), # Hunting instinct
            "evasion_percent": random.randint(90, 130), # Large target
            "crit_chance_percent": random.randint(115, 155), # Deadly precision
            "crit_damage_percent": random.randint(120, 160), # Dragon fury
            "armour_penetration_percent": random.randint(120, 160), # Dragon fangs
            "damage_reduction_percent": random.randint(105, 145),   # Dragon hide
            "block_chance_percent": random.randint(85, 125)        # Uses size
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "poison", "stunning", "defence_break", "reckless"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Void Titan": {
        "name": "Void Titan",
        "stats": {
            "hp_percent": random.randint(125, 160),      # Colossal size
            "attack_percent": random.randint(120, 160),  # Void strength
            "defence_percent": random.randint(115, 155), # Void armor
            "accuracy_percent": random.randint(75, 115),  # Too massive
            "evasion_percent": random.randint(65, 105),  # Huge target
            "crit_chance_percent": random.randint(80, 120),
            "crit_damage_percent": random.randint(125, 160), # Crushing void
            "armour_penetration_percent": random.randint(120, 160), # Reality breaking
            "damage_reduction_percent": random.randint(115, 155),   # Void protection
            "block_chance_percent": random.randint(110, 150)       # Living barrier
        },
        "tier": "very-hard",
        "attack_types": ["normal", "reckless", "stunning", "draining", "defence_break", "confusion"],
        "soultype": "standard",
        "monster_type": "void"
    },

    "Chaos Incarnate": {
        "name": "Chaos Incarnate",
        "stats": {
            "hp_percent": random.randint(100, 140),      # Unstable form
            "attack_percent": random.randint(125, 160),  # Chaotic power
            "defence_percent": random.randint(80, 120),  # Shifting form
            "accuracy_percent": random.randint(120, 160), # Reality warping
            "evasion_percent": random.randint(120, 160), # Chaos shifting
            "crit_chance_percent": random.randint(120, 160), # Chaos strikes
            "crit_damage_percent": random.randint(125, 160), # Reality breaking
            "armour_penetration_percent": random.randint(125, 160), # Chaos piercing
            "damage_reduction_percent": random.randint(75, 115),    # Unstable defense
            "block_chance_percent": random.randint(60, 100)        # Can't focus
        },
        "tier": "very-hard",
        "attack_types": ["normal", "double", "poison", "vampiric", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "void"
    },

    "Eternity Warden": {
        "name": "Eternity Warden",
        "stats": {
            "hp_percent": random.randint(120, 160),      # Timeless being
            "attack_percent": random.randint(110, 150),  # Time strength
            "defence_percent": random.randint(120, 160), # Eternal defense
            "accuracy_percent": random.randint(115, 155), # Time sight
            "evasion_percent": random.randint(105, 145), # Time shifting
            "crit_chance_percent": random.randint(110, 150), # Knows weakpoints
            "crit_damage_percent": random.randint(115, 155), # Time strikes
            "armour_penetration_percent": random.randint(115, 155), # Time piercing
            "damage_reduction_percent": random.randint(120, 160),   # Time shield
            "block_chance_percent": random.randint(115, 155)       # Guardian's duty
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "freeze", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Ancient Wyvern": {
        "name": "Ancient Wyvern",
        "stats": {
            "hp_percent": random.randint(115, 155),      # Ancient dragon
            "attack_percent": random.randint(125, 160),  # Dragon might
            "defence_percent": random.randint(105, 145), # Old scales
            "accuracy_percent": random.randint(115, 155), # Hunter's eye
            "evasion_percent": random.randint(110, 150), # Aerial grace
            "crit_chance_percent": random.randint(115, 155), # Experienced hunter
            "crit_damage_percent": random.randint(120, 160), # Ancient fury
            "armour_penetration_percent": random.randint(115, 155), # Ancient claws
            "damage_reduction_percent": random.randint(100, 140),   # Aged scales
            "block_chance_percent": random.randint(80, 120)        # Dodges instead
        },
        "tier": "very-hard",
        "attack_types": ["normal", "triple", "poison", "reckless", "stunning", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Elemental Drake": {
        "name": "Elemental Drake",
        "stats": {
            "hp_percent": random.randint(110, 150),      # Dragon form
            "attack_percent": random.randint(120, 160),  # Elemental fury
            "defence_percent": random.randint(100, 140), # Dragon hide
            "accuracy_percent": random.randint(115, 155), # Elemental precision
            "evasion_percent": random.randint(110, 150), # Elemental flight
            "crit_chance_percent": random.randint(115, 155), # Elemental mastery
            "crit_damage_percent": random.randint(120, 160), # Elemental burst
            "armour_penetration_percent": random.randint(120, 160), # Element piercing
            "damage_reduction_percent": random.randint(105, 145),   # Elemental shield
            "block_chance_percent": random.randint(75, 115)        # Avoids instead
        },
        "tier": "very-hard",
        "attack_types": ["normal", "burn", "poison", "freeze", "stunning", "confusion"],
        "soultype": "standard",
        "monster_type": "ice"
    },
    
    "Dragonlord": {
        "name": "Dragonlord",
        "stats": {
            "hp_percent": random.randint(120, 160),      # Dragon emperor
            "attack_percent": random.randint(125, 160),  # Supreme dragon might
            "defence_percent": random.randint(110, 150), # Royal scales
            "accuracy_percent": random.randint(115, 155), # Ancient precision
            "evasion_percent": random.randint(100, 140), # Royal grace
            "crit_chance_percent": random.randint(120, 160), # Dragon mastery
            "crit_damage_percent": random.randint(125, 160), # Supreme power
            "armour_penetration_percent": random.randint(120, 160), # Royal fangs
            "damage_reduction_percent": random.randint(110, 150),   # Dragon lord's hide
            "block_chance_percent": random.randint(95, 135)       # Prefers domination
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "reckless", "stunning", "damage_reflect", "confusion"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Chromatic Dragon": {
        "name": "Chromatic Dragon",
        "stats": {
            "hp_percent": random.randint(115, 155),      # Powerful dragon
            "attack_percent": random.randint(120, 160),  # Multi-element power
            "defence_percent": random.randint(105, 145), # Shifting scales
            "accuracy_percent": random.randint(120, 160), # Elemental precision
            "evasion_percent": random.randint(115, 155), # Color shifting
            "crit_chance_percent": random.randint(120, 160), # Elemental mastery
            "crit_damage_percent": random.randint(120, 160), # Prismatic fury
            "armour_penetration_percent": random.randint(125, 160), # Element piercing
            "damage_reduction_percent": random.randint(100, 140),   # Shifting defense
            "block_chance_percent": random.randint(80, 120)        # Relies on evasion
        },
        "tier": "very-hard",
        "attack_types": ["normal", "burn", "poison", "freeze", "stunning", "confusion"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Elder Dragon": {
        "name": "Elder Dragon",
        "stats": {
            "hp_percent": random.randint(125, 160),      # Ancient vitality
            "attack_percent": random.randint(125, 160),  # Primordial strength
            "defence_percent": random.randint(120, 160), # Ancient scales
            "accuracy_percent": random.randint(105, 145), # Old but deadly
            "evasion_percent": random.randint(85, 125),  # Ancient weight
            "crit_chance_percent": random.randint(115, 155), # Ancient wisdom
            "crit_damage_percent": random.randint(125, 160), # Primordial fury
            "armour_penetration_percent": random.randint(120, 160), # Ancient fangs
            "damage_reduction_percent": random.randint(120, 160),   # Primordial hide
            "block_chance_percent": random.randint(105, 145)       # Ancient defenses
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "draining", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "dragon"
    },
    
    # Extreme Enemies
    "Magma Colossus": {
        "name": "Magma Colossus",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Massive molten form
            "attack_percent": random.randint(130, 160),  # Magma strength
            "defence_percent": random.randint(130, 160), # Molten armor
            "accuracy_percent": random.randint(80, 110),  # Slow moving
            "evasion_percent": random.randint(70, 100),  # Too massive
            "crit_chance_percent": random.randint(85, 115), # Not precise
            "crit_damage_percent": random.randint(130, 160), # Melting strikes
            "armour_penetration_percent": random.randint(130, 160), # Melts armor
            "damage_reduction_percent": random.randint(130, 160),   # Molten body
            "block_chance_percent": random.randint(120, 150)       # Living wall
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "reckless", "burn", "stunning", "damage_reflect", "defence_break"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Phoenix Overlord": {
        "name": "Phoenix Overlord",
        "stats": {
            "hp_percent": random.randint(110, 140),      # Immortal but fragile
            "attack_percent": random.randint(130, 160),  # Solar might
            "defence_percent": random.randint(100, 130), # Light frame
            "accuracy_percent": random.randint(130, 160), # Perfect sight
            "evasion_percent": random.randint(130, 160), # Solar flight
            "crit_chance_percent": random.randint(130, 160), # Vital strikes
            "crit_damage_percent": random.randint(130, 160), # Solar fury
            "armour_penetration_percent": random.randint(130, 160), # Burning through
            "damage_reduction_percent": random.randint(90, 120),    # Light body
            "block_chance_percent": random.randint(80, 110)        # Dodges instead
        },
        "tier": "extreme",
        "attack_types": ["normal", "double", "stunning", "triple", "burn", "attack_weaken", "vampiric"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Volcanic Titan": {
        "name": "Volcanic Titan",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Mountain size
            "attack_percent": random.randint(130, 160),  # Volcanic might
            "defence_percent": random.randint(130, 160), # Stone body
            "accuracy_percent": random.randint(85, 115),  # Slow attacks
            "evasion_percent": random.randint(70, 100),  # Mountain sized
            "crit_chance_percent": random.randint(90, 120), # Raw power
            "crit_damage_percent": random.randint(130, 160), # Eruption
            "armour_penetration_percent": random.randint(130, 160), # Melting strikes
            "damage_reduction_percent": random.randint(130, 160),   # Stone hide
            "block_chance_percent": random.randint(120, 150)       # Mountain shield
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "stunning", "damage_reflect", "burn", "defence_break", "reckless"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Inferno Wyrm": {
        "name": "Inferno Wyrm",
        "stats": {
            "hp_percent": random.randint(120, 150),      # Dragon frame
            "attack_percent": random.randint(130, 160),  # Infernal might
            "defence_percent": random.randint(110, 140), # Fire scales
            "accuracy_percent": random.randint(125, 155), # Hunter's eye
            "evasion_percent": random.randint(120, 150), # Fire flight
            "crit_chance_percent": random.randint(125, 155), # Vital hunting
            "crit_damage_percent": random.randint(130, 160), # Infernal strikes
            "armour_penetration_percent": random.randint(130, 160), # Melting fangs
            "damage_reduction_percent": random.randint(110, 140),   # Fire resistance
            "block_chance_percent": random.randint(90, 120)        # Aggressive nature
        },
        "tier": "extreme",
        "attack_types": ["normal", "double", "power", "reckless", "defence_break" "burn", "attack_weaken"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Cinder Archfiend": {
        "name": "Cinder Archfiend",
        "stats": {
            "hp_percent": random.randint(115, 145),      # Demon form
            "attack_percent": random.randint(130, 160),  # Hellfire power
            "defence_percent": random.randint(105, 135), # Demon hide
            "accuracy_percent": random.randint(130, 160), # Demonic precision
            "evasion_percent": random.randint(125, 155), # Fire teleport
            "crit_chance_percent": random.randint(130, 160), # Fatal strikes
            "crit_damage_percent": random.randint(130, 160), # Demon power
            "armour_penetration_percent": random.randint(130, 160), # Hellfire piercing
            "damage_reduction_percent": random.randint(100, 130),   # Demon resistance
            "block_chance_percent": random.randint(85, 115)        # Offensive nature
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "confusion", "vampiric", "attack_weaken", "burn", "defence_break"],
        "soultype": "boss",
        "monster_type": "fire"
    },
    
    "Cosmic Devourer": {
        "name": "Cosmic Devourer",
        "stats": {
            "hp_percent": random.randint(115, 145),      # Void entity
            "attack_percent": random.randint(130, 160),  # Reality consuming
            "defence_percent": random.randint(100, 130), # Ethereal form
            "accuracy_percent": random.randint(130, 160), # Space warping
            "evasion_percent": random.randint(130, 160), # Reality shifting
            "crit_chance_percent": random.randint(130, 160), # Reality tears
            "crit_damage_percent": random.randint(130, 160), # Cosmic destruction
            "armour_penetration_percent": random.randint(130, 160), # Reality piercing
            "damage_reduction_percent": random.randint(90, 120),    # Unstable form
            "block_chance_percent": random.randint(80, 110)        # Can't block reality
        },
        "tier": "extreme",
        "attack_types": ["normal", "double", "triple", "confusion", "stunning", "draining", "attack_weaken"],
        "soultype": "boss",
        "monster_type": "void"
    },

    "Astral Behemoth": {
        "name": "Astral Behemoth",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Star-forged body
            "attack_percent": random.randint(130, 160),  # Stellar might
            "defence_percent": random.randint(130, 160), # Cosmic armor
            "accuracy_percent": random.randint(90, 120),  # Massive form
            "evasion_percent": random.randint(75, 105),  # Too huge
            "crit_chance_percent": random.randint(95, 125), # Raw power
            "crit_damage_percent": random.randint(130, 160), # Star crushing
            "armour_penetration_percent": random.randint(130, 160), # Gravity force
            "damage_reduction_percent": random.randint(130, 160),   # Star forge
            "block_chance_percent": random.randint(115, 145)       # Cosmic shield
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "confusion", "reckless", "defence_break", "stunning", "damage_reflect"],
        "soultype": "boss",
        "monster_type": "void"
    },

    "Galactic Leviathan": {
        "name": "Galactic Leviathan",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Cosmic whale
            "attack_percent": random.randint(130, 160),  # Space crushing
            "defence_percent": random.randint(125, 155), # Stellar hide
            "accuracy_percent": random.randint(115, 145), # Space sensing
            "evasion_percent": random.randint(110, 140), # Space swimming
            "crit_chance_percent": random.randint(110, 140), # Void strikes
            "crit_damage_percent": random.randint(130, 160), # Stellar force
            "armour_penetration_percent": random.randint(130, 160), # Space teeth
            "damage_reduction_percent": random.randint(120, 150),   # Void shield
            "block_chance_percent": random.randint(110, 140)       # Cosmic mass
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "poison", "stunning", "defence_break"],
        "soultype": "boss",
        "monster_type": "arcane"
    },

    "Nebula Colossus": {
        "name": "Nebula Colossus",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Star born
            "attack_percent": random.randint(125, 155),  # Star force
            "defence_percent": random.randint(130, 160), # Nebula form
            "accuracy_percent": random.randint(85, 115),  # Diffuse form
            "evasion_percent": random.randint(80, 110),  # Too massive
            "crit_chance_percent": random.randint(90, 120), # Star power
            "crit_damage_percent": random.randint(130, 160), # Stellar crush
            "armour_penetration_percent": random.randint(120, 150), # Star piercing
            "damage_reduction_percent": random.randint(130, 160),   # Nebula shield
            "block_chance_percent": random.randint(120, 150)       # Gas giant
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "confusion", "damage_reflect", "reckless", "stunning", "defence_break"],
        "soultype": "boss",
        "monster_type": "arcane"
    },

    "Celestial Titan": {
        "name": "Celestial Titan",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Divine form
            "attack_percent": random.randint(130, 160),  # Heaven's might
            "defence_percent": random.randint(130, 160), # Divine armor
            "accuracy_percent": random.randint(120, 150), # Divine sight
            "evasion_percent": random.randint(100, 130), # Massive form
            "crit_chance_percent": random.randint(120, 150), # Divine precision
            "crit_damage_percent": random.randint(130, 160), # God's wrath
            "armour_penetration_percent": random.randint(130, 160), # Divine pierce
            "damage_reduction_percent": random.randint(125, 155),   # Holy shield
            "block_chance_percent": random.randint(115, 145)       # Divine guard
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "confusion", "double", "stunning", "draining", "defence_break"],
        "soultype": "boss",
        "monster_type": "arcane"
    },
    
    # Boss Monsters
    "Seraphim Guardian": {
        "name": "Seraphim Guardian",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Divine vitality
            "attack_percent": random.randint(130, 160),  # Holy might
            "defence_percent": random.randint(130, 160), # Divine protection
            "accuracy_percent": random.randint(120, 150), # All-seeing
            "evasion_percent": random.randint(115, 145), # Divine grace
            "crit_chance_percent": random.randint(120, 150), # Divine judgment
            "crit_damage_percent": random.randint(130, 160), # Holy smite
            "armour_penetration_percent": random.randint(125, 155), # Holy pierce
            "damage_reduction_percent": random.randint(130, 160),   # Divine ward
            "block_chance_percent": random.randint(125, 155)       # Holy shield
        },
        "tier": "boss",
        "attack_types": ["normal", "power", "stunning", "draining", "reckless", "damage_reflect", "triple"],
        "soultype": "boss",
        "monster_type": "warrior"
    },

    "Celestial Arbiter": {
        "name": "Celestial Arbiter",
        "stats": {
            "hp_percent": random.randint(120, 150),      # Divine form
            "attack_percent": random.randint(130, 160),  # Justice's might
            "defence_percent": random.randint(115, 145), # Celestial form
            "accuracy_percent": random.randint(130, 160), # Perfect judgment
            "evasion_percent": random.randint(130, 160), # Divine movement
            "crit_chance_percent": random.randint(130, 160), # Finding guilt
            "crit_damage_percent": random.randint(130, 160), # Divine punishment
            "armour_penetration_percent": random.randint(130, 160), # Justice pierces
            "damage_reduction_percent": random.randint(110, 140),   # Light form
            "block_chance_percent": random.randint(100, 130)       # Dodges instead
        },
        "tier": "boss",
        "attack_types": ["normal", "double", "draining", "stunning", "triple", "vampiric", "attack_weaken"],
        "soultype": "boss",
        "monster_type": "arcane"
    },

    "Astral Demiurge": {
        "name": "Astral Demiurge",
        "stats": {
            "hp_percent": random.randint(125, 155),      # Creator's form
            "attack_percent": random.randint(130, 160),  # Creation power
            "defence_percent": random.randint(125, 155), # Reality shield
            "accuracy_percent": random.randint(130, 160), # Perfect sight
            "evasion_percent": random.randint(120, 150), # Reality shift
            "crit_chance_percent": random.randint(125, 155), # Finding weakness
            "crit_damage_percent": random.randint(130, 160), # Reality strike
            "armour_penetration_percent": random.randint(130, 160), # Unmaking
            "damage_reduction_percent": random.randint(120, 150),   # Reality ward
            "block_chance_percent": random.randint(115, 145)       # Creation shield
        },
        "tier": "boss",
        "attack_types": ["normal", "power", "poison", "freeze", "stunning", "vampiric", "defence_break"],
        "soultype": "boss",
        "monster_type": "void"
    },

    "Ethereal Leviathan": {
        "name": "Ethereal Leviathan",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Cosmic mass
            "attack_percent": random.randint(130, 160),  # Reality crusher
            "defence_percent": random.randint(115, 145), # Spirit form
            "accuracy_percent": random.randint(120, 150), # Void sense
            "evasion_percent": random.randint(130, 160), # Phase shifting
            "crit_chance_percent": random.randint(125, 155), # Reality rend
            "crit_damage_percent": random.randint(130, 160), # Cosmic force
            "armour_penetration_percent": random.randint(130, 160), # Reality pierce
            "damage_reduction_percent": random.randint(110, 140),   # Spirit shield
            "block_chance_percent": random.randint(100, 130)       # Phase through
        },
        "tier": "boss",
        "attack_types": ["normal", "reckless", "draining", "double", "poison", "triple", "damage_reflect"],
        "soultype": "boss",
        "monster_type": "spirit"
    },

    "Divine Architect": {
        "name": "Divine Architect",
        "stats": {
            "hp_percent": random.randint(130, 160),      # Creator's vitality
            "attack_percent": random.randint(130, 160),  # Divine power
            "defence_percent": random.randint(130, 160), # Perfect defense
            "accuracy_percent": random.randint(125, 155), # Divine precision
            "evasion_percent": random.randint(115, 145), # Reality bend
            "crit_chance_percent": random.randint(125, 155), # Perfect strike
            "crit_damage_percent": random.randint(130, 160), # Divine force
            "armour_penetration_percent": random.randint(130, 160), # Creation pierce
            "damage_reduction_percent": random.randint(130, 160),   # Perfect ward
            "block_chance_percent": random.randint(125, 155)       # Divine shield
        },
        "tier": "boss",
        "attack_types": ["normal", "power", "stunning", "freeze", "draining", "reckless", "defence_break"],
        "soultype": "boss",
        "monster_type": "arcane"
    },
    
    # Event Enemies
    "Shrine Guardian": {
        "name": "Shrine Guardian",
        "stats": {
            "hp_percent": random.randint(105, 130),
            "attack_percent": random.randint(75, 100),
            "defence_percent": random.randint(65, 90),
            "accuracy_percent": random.randint(70, 95),
            "evasion_percent": random.randint(60, 85),
            "crit_chance_percent": random.randint(65, 90),
            "crit_damage_percent": random.randint(75, 100),
            "armour_penetration_percent": random.randint(60, 85),
            "damage_reduction_percent": random.randint(70, 95),
            "block_chance_percent": random.randint(75, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "damage_reflect", "defence_break"],
        "soultype": "standard",
        "monster_type": "warrior"
    },
    
    "Echo Wraith": {
        "name": "Echo Wraith",
        "stats": {
            "hp_percent": random.randint(75, 100),
            "attack_percent": random.randint(90, 115),
            "defence_percent": random.randint(55, 80),
            "accuracy_percent": random.randint(85, 110),
            "evasion_percent": random.randint(105, 130),
            "crit_chance_percent": random.randint(115, 140),
            "crit_damage_percent": random.randint(105, 130),
            "armour_penetration_percent": random.randint(75, 100),
            "damage_reduction_percent": random.randint(45, 70),
            "block_chance_percent": random.randint(35, 60)
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "vampiric", "draining", "attack_weaken"],
        "soultype": "boss",
        "monster_type": "spirit"
    },
    
    "Crystal Guardian": {
        "name": "Crystal Guardian",
        "stats": {
            "hp_percent": random.randint(100, 125),
            "attack_percent": random.randint(80, 100),
            "defence_percent": random.randint(100, 120),
            "accuracy_percent": random.randint(60, 90),
            "evasion_percent": random.randint(30, 50),
            "crit_chance_percent": random.randint(120, 140),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(140, 150),
            "block_chance_percent": random.randint(70, 80)
        },
        "tier": "medium-hard",
        "attack_types": ["power", "reckless", "attack_weaken", "defence_break", "damage_reflect"],
        "soultype": "boss",
        "monster_type": "arcane"
    },
    
    "Void Walker": {
        "name": "Void Walker",
        "stats": {
            # High evasion/accuracy to match void theme
            "hp_percent": random.randint(85, 115),      # Ethereal form - moderate HP
            "attack_percent": random.randint(110, 135),  # Void-enhanced strikes
            "defence_percent": random.randint(70, 95),   # Insubstantial - lower defense
            "accuracy_percent": random.randint(130, 155), # Highly precise void attacks
            "evasion_percent": random.randint(140, 165), # Phase shifting makes it hard to hit
            "crit_chance_percent": random.randint(110, 135), # Finds weaknesses in reality
            "crit_damage_percent": random.randint(120, 145), # Devastating void strikes
            "armour_penetration_percent": random.randint(120, 145), # Void pierces armor
            "damage_reduction_percent": random.randint(60, 85),    # Not physically tough
            "block_chance_percent": random.randint(50, 75)        # Dodges rather than blocks
        },
        "tier": "hard",  # Makes it a significant threat
        "attack_types": ["normal", "double", "triple", "vampiric", "void_drain", "reality_rend"],
        "soultype": "boss",
        "monster_type": "void"
    },

    "Empowered Void Walker": {
        "name": "Empowered Void Walker",
        "stats": {
            # Enhanced version of regular Void Walker
            "hp_percent": random.randint(100, 130),      # More substantial form
            "attack_percent": random.randint(125, 150),  # Stronger void energies
            "defence_percent": random.randint(85, 110),  # Better control of form
            "accuracy_percent": random.randint(140, 165), # Master of void precision
            "evasion_percent": random.randint(150, 175), # Superior phase shifting
            "crit_chance_percent": random.randint(120, 145), # Expert at finding weaknesses
            "crit_damage_percent": random.randint(130, 155), # Devastating void mastery
            "armour_penetration_percent": random.randint(130, 155), # Enhanced void penetration
            "damage_reduction_percent": random.randint(70, 95),     # Better void protection
            "block_chance_percent": random.randint(60, 85)         # Still prefers dodging
        },
        "tier": "very-hard",
        "attack_types": ["normal", "double", "triple", "reckless", "damage_reflect", "vampiric", "void_drain", "reality_rend"],
        "soultype": "boss",
        "monster_type": "void"
    },
    
    "Soul Forgemaster": {
        "name": "Soul Forgemaster",
        "stats": {
            "hp_percent": random.randint(120, 150),
            "attack_percent": random.randint(110, 140),
            "defence_percent": random.randint(120, 150),
            "accuracy_percent": random.randint(90, 120),
            "evasion_percent": random.randint(80, 110),
            "crit_chance_percent": random.randint(90, 120),
            "crit_damage_percent": random.randint(120, 150),
            "armour_penetration_percent": random.randint(100, 130),
            "damage_reduction_percent": random.randint(110, 140),
            "block_chance_percent": random.randint(100, 130)
        },
        "tier": "boss",
        "attack_types": ["attack_weaken", "power", "double", "reckless", "defence_break", "damage_reflect", "burn"],
        "soultype": "boss",
        "monster_type": "arcane"
    },

    
    # Test monster (used for testing purposes only)
    
    "Test Monster": {
        "name": "Test Monster",
        "stats": {
            "hp_percent": 1,
            "attack_percent": 3,
            "defence_percent": 50,
            "accuracy_percent": 3,
            "evasion_percent": 1,
            "crit_chance_percent": 1,
            "crit_damage_percent": 1,
            "armour_penetration_percent": 1,
            "damage_reduction_percent": 1,
            "block_chance_percent": 1
        },
        "tier": "medium",
        "attack_types": ["confusion"],
        "soultype": "standard",
        "monster_type": "test"
    }
}

ENEMY_ATTACK_TYPES = {
    "normal": {
        "name": "Normal Attack",
        "damage_modifier": 1,
        "effect": None
    },
    "power": {
        "name": "Power Attack",
        "damage_modifier": 1.5,
        "effect": None
    },
    "double": {
        "name": "Double Strike",
        "damage_modifier": 0.9,
        "effect": None,
        "extra_attacks": 1
    },
    "triple": {
        "name": "Triple Strike",
        "damage_modifier": 0.9,
        "extra_attacks": 2
    },
    "vampiric": {
        "name": "Vampiric Strike",
        "damage_modifier": 0.9,
        "effect": "lifesteal"
    },
    "reckless": {
        "name": "Reckless Assault",
        "damage_modifier": 2
    },
    "draining": {
        "name": "Draining Touch",
        "damage_modifier": 0.9,
        "effect": "stamina_drain"
    },
    "stunning": {
        "name": "Stunning Blow",
        "damage_modifier": 0.8,
        "effect": "stun"
    },
    "confusion": {
        "name": "Confounding Blow",
        "damage_modifier": 0.8,
        "effect": "confusion"
    },
    "poison": {
        "name": "Poison Strike",
        "damage_modifier": 0.9,
        "effect": "poison",
    },
    "freeze": {
        "name": "Frozen Strike",
        "damage_modifier": 0.9,
        "effect": "freeze"
    },
    "burn": {
        "name": "Burning Strike",
        "damage_modifier": 0.9,
        "effect": "burn"
    },
    "damage_reflect": {
        "name": "Reflective Shield",
        "damage_modifier": 0.5,
        "effect": "damage_reflect"
    },
    "defence_break": {
        "name": "Defence Shatter",
        "damage_modifier": 1,
        "effect": "defence_break"
    },
    "attack_weaken": {
        "name": "Attack Weaken",
        "damage_modifier": 1,
        "effect": "attack_weaken"
    },
    "reality_rend": {
        "name": "Reality Rend",
        "damage_modifier": 1.2,
        "effect": "defence_break",
        "extra_effects": ["confusion"]
    },
    "void_drain": {
        "name": "Void Drain",
        "damage_modifier": 1,
        "effect": "stamina_drain",
        "extra_effects": ["attack_weaken"]
    }
}

# Monster variant modifiers with stat changes and spawn chances
MONSTER_VARIANTS = {
    "Frenzied": {
        "chance": 0.1, # 10% chance to spawn
        "stats": {
            # Increases stat by amount / 100 (150 = 1.5x stat)
            "hp_percent": 80,
            "attack_percent": 150,
            "defence_percent": 70,
            "accuracy_percent": 120,
            "evasion_percent": 100,
            "crit_chance_percent": 130,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 100,
            "block_chance_percent": 100
        },
        "lore": "Driven mad by dark energies, this creature attacks with unnatural ferocity!",
        "additional_attacks": ["reckless"],
        "loot_modifiers": {
            """
            quantity_bonus = extra items, quality_boost = chance for item tier up, gold_multiplier = self explanatory
            """
            "quantity_bonus": 1,
            "quality_boost": 0.15,
            "gold_multiplier": 1.3
        }
    },
    "Ancient": {
        "chance": 0.08,
        "stats": {
            "hp_percent": 150,
            "attack_percent": 80,
            "defence_percent": 140,
            "accuracy_percent": 100,
            "evasion_percent": 70,
            "crit_chance_percent": 100,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 130,
            "block_chance_percent": 60
        },
        "lore": "This creature has lived for centuries, growing ever stronger with age!",
        "additional_attacks": ["draining", "confusion"],
        "loot_modifiers": {
            """
            guaranteed_drops = guaranteed item of given tier/type
            """
            "quantity_bonus": 2,
            "quality_boost": 1.0,
            "gold_multiplier": 1.5,
            "guaranteed_drops": ["rare"]
        }
    },
    "Ethereal": {
        "chance": 0.07,
        "stats": {
            "hp_percent": 50,
            "attack_percent": 100,
            "defence_percent": 60,
            "accuracy_percent": 150,
            "evasion_percent": 200,
            "crit_chance_percent": 100,
            "crit_damage_percent": 140,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 100,
            "block_chance_percent": 100
        },
        "lore": "Partially phased into another dimension, this being is incredibly hard to hit!",
        "additional_attacks": ["attack_weaken", "defence_break"],
        "loot_modifiers": {
            "quanitity_bonus": 1,
            "quality_boost": 0.2,
            "gold_multiplier": 1.4,
            "guaranteed_drops": ["consumable"]
        }
    },
    "Colossal": {
        "chance": 0.06,
        "stats": {
            "hp_percent": 200,
            "attack_percent": 100,
            "defence_percent": 150,
            "accuracy_percent": 75,
            "evasion_percent": 25,
            "crit_chance_percent": 100,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 130,
            "block_chance_percent": 100
        },
        "lore": "This monster has grown to an enourmous size, becoming a true titan!",
        "additional_attacks": ["power"],
        "loot_modifiers": {
            "quanitity_bonus": random.randint(1, 2),
            "quality_boost": 0.3,
            "gold_multiplier": 1.5,
            "guaranteed_drops": random.choice(["rare", "epic"])
        }
    },
    "Corrupted": {
        "chance": 0.09,
        "stats": {
            "hp_percent": 120,
            "attack_percent": 130,
            "defence_percent": 70,
            "accuracy_percent": 80,
            "evasion_percent": 100,
            "crit_chance_percent": 100,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 150,
            "damage_reduction_percent": 60,
            "block_chance_percent": 80
        },
        "lore": "Dark energies have twisted this creature, granting both power and instability",
        "additional_attacks": ["poison", "burn"],
        "loot_modifiers": {
            "quantity_bonus": 1,
            "quality_boost": random.randint(10, 50) / 100,
            "gold_multiplier": random.randint(130, 170) / 100,
            "guaranteed_drops": ["consumable"]
        }
    },
    "Swift": {
        "chance": 0.1,
        "stats": {
            "hp_percent": 100,
            "attack_percent": 90,
            "defence_percent": 80,
            "accuracy_percent": 150,
            "evasion_percent": 150,
            "crit_chance_percent": 130,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 60,
            "block_chance_percent": 70
        },
        "lore": "Moving with supernatural speed, this creature sticks with deadly precision!",
        "additional_attacks": ["double", "triple"],
        "loot_modifiers": {
            "quanitity_bonus": 2,
            "quality_boost": 0.25,
            "gold_multiplier": 1.5,
            "guaranteed_drops": random.choice(["uncommon", "rare", "epic", "masterwork"])
        }
    },
    "Vampiric": {
        "chance": 0.08,
        "stats": {
            "hp_percent": 120,
            "attack_percent": 130,
            "defence_percent": 90,
            "accuracy_percent": 100,
            "evasion_percent": 75,
            "crit_chance_percent": 140,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 100,
            "block_chance_percent": 100
        },
        "lore": "This being drains the life force of its victims, growing stronger with each strike!",
        "additional_attacks": ["vampiric"],
        "loot_modifiers": {
            "quanitity_bonus": 1,
            "quality_boost": 0.15,
            "gold_multiplier": 1.3,
            "guaranteed_drops": ["consumable"]
        }
    },
    "Armoured": {
        "chance": 0.08,
        "stats": {
            "hp_percent": 100,
            "attack_percent": 70,
            "defence_percent": 180,
            "accuracy_percent": 80,
            "evasion_percent": 75,
            "crit_chance_percent": 100,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 150,
            "block_chance_percent": 140
        },
        "lore": "Covered in thick natural armour, this creature is incredibly difficult to harm!",
        "additional_attacks": ["damage_reflect"],
        "loot_modifiers": {
            "quantity_bonus": random.randint(1, 3),
            "quality_boost": random.randint(15, 40) / 100,
            "gold_modifier": random.randint(120, 160) / 100,
            "guaranteed_drops": ["epic"]
        }
    },
    "Void-Touched": {
        "chance": 0.08,  # 8% chance to spawn
        "stats": {
            "hp_percent": 85,
            "attack_percent": 130,
            "defence_percent": 75,
            "accuracy_percent": 140,
            "evasion_percent": 140,
            "crit_chance_percent": 120,
            "crit_damage_percent": 100,
            "armour_penetration_percent": 100,
            "damage_reduction_percent": 100,
            "block_chance_percent": 100
        },
        "lore": "This being has been altered by void energy, gaining supernatural precision but becoming more unstable!",
        "additional_attacks": ["reality_rend", "void_drain"],
        "loot_modifiers": {
            "quantity_bonus": 1,
            "quality_boost": 0.25,  # 25% chance to upgrade item tier
            "gold_multiplier": 1.4,
            "guaranteed_drops": ["rare", "epic"]  # Always drops at least rare/epic item
        }
    }
}

def guaranteed_drops(min_chance, max_chance, item=[]):
    """Chance for a guaranteed drop of a certain tier item"""
    if random.random < random.randint(min_chance, max_chance):
        drop = random.choice(item)
        return drop
    return None

def apply_variant_modifiers(template_stats, variant):
    """Apply variant stat modifiers to template stats"""
    modified_stats = template_stats.copy()
    
    for stat, modifier in variant["stats"].items():
        if stat in modified_stats:
            # Convert percentages to multiplier
            multiplier = modifier / 100
            modified_stats[stat] = int(modified_stats[stat] * multiplier)
            
    return modified_stats

# Helper functions for type-based mechanics
def get_type_stat_preferences(monster_type):
    """Get preferred stats for a monster type"""
    if monster_type in MONSTER_TYPES:
        return MONSTER_TYPES[monster_type]["stat_preferences"]
    return ["attack", "defence", "accuracy"]  # Default preferences

def get_type_equipment_affinities(monster_type):
    """Get equipment affinities for a monster type"""
    if monster_type in MONSTER_TYPES:
        return MONSTER_TYPES[monster_type]["equipment_affinities"]
    return ["weapon", "chest", "shield"]  # Default affinities

def get_monster_types_for_element(element):
    """Get all monsters of a specific elemental type"""
    if element in MONSTER_TYPES:
        return MONSTER_TYPES[element]["members"]
    return []

def get_type_for_monster(monster_name):
    """Get the type of a specific monster"""
    for type_name, type_data in MONSTER_TYPES.items():
        if monster_name in type_data["members"]:
            return type_name
    return "unknown"

def are_monsters_same_type(monster1, monster2):
    """Check if two monsters are the same type"""
    type1 = get_type_for_monster(monster1)
    type2 = get_type_for_monster(monster2)
    return type1 == type2 and type1 != "unknown"

def get_opposing_types():
    """Define type matchups for resistances/weaknesses"""
    return {
        "fire": "ice",
        "ice": "wind",
        "wind": "grass",
        "grass": "earth",
        "earth": "lightning",
        "lightning": "water",
        "water": "dragon",
        "dragon": "warrior",
        "warrior": "undead",
        "undead": "spirit",
        "spirit": "arcane",
        "arcane": "void",
        "void": "fire"
    }