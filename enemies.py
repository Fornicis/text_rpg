from player import Character
from game_config import MONSTER_TYPES
from status_effects import *
import random

ENEMY_TEMPLATES = {
        # Easy Enemies
        "Rat": {
        "name": "Rat",
        "stats": {
            "hp_percent": random.randint(80, 85),        # Small and fragile
            "attack_percent": random.randint(90, 95),    # Decent attack
            "defence_percent": random.randint(80, 85),   # Poor defense
            "accuracy_percent": random.randint(95, 100), # Good accuracy
            "evasion_percent": random.randint(105, 110), # Very evasive
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "grass"
    },

    "Boar": {
        "name": "Boar",
        "stats": {
            "hp_percent": random.randint(105, 110),     # Sturdy
            "attack_percent": random.randint(100, 105), # Strong
            "defence_percent": random.randint(95, 100),
            "accuracy_percent": random.randint(85, 90), # Not very accurate
            "evasion_percent": random.randint(80, 85),  # Poor evasion
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(100, 105),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(95, 100),
            "block_chance_percent": random.randint(90, 95)
        },
        "tier": "low",
        "attack_types": ["normal", "power", "reckless", "stunning"],
        "soultype": "standard",
        "monster_type": "grass"
    },

    "Plains Hawk": {
        "name": "Plains Hawk",
        "stats": {
            "hp_percent": random.randint(80, 85),       # Very fragile
            "attack_percent": random.randint(95, 100),  # Good attack
            "defence_percent": random.randint(80, 85),  # Poor defense
            "accuracy_percent": random.randint(110, 115), # Excellent accuracy
            "evasion_percent": random.randint(110, 115), # Very evasive
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(100, 105),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "triple", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Strider": {
        "name": "Strider",
        "stats": {
            "hp_percent": random.randint(90, 95),      # Average health
            "attack_percent": random.randint(90, 95),  # Average attack
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(95, 100),
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Bull": {
        "name": "Bull",
        "stats": {
            "hp_percent": random.randint(110, 115),    # Very tough
            "attack_percent": random.randint(105, 110), # Strong
            "defence_percent": random.randint(95, 100),
            "accuracy_percent": random.randint(80, 85), # Poor accuracy
            "evasion_percent": random.randint(80, 85),  # Poor evasion
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(95, 100),
            "damage_reduction_percent": random.randint(95, 100),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "low",
        "attack_types": ["normal", "power", "reckless", "stunning"],
        "soultype": "standard",
        "monster_type": "grass"
    },

    "Bat": {
        "name": "Bat",
        "stats": {
            "hp_percent": random.randint(80, 85),      # Very fragile
            "attack_percent": random.randint(85, 90),
            "defence_percent": random.randint(80, 85),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(105, 110), # Very evasive
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "vampiric", "draining"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Goblin": {
        "name": "Goblin",
        "stats": {
            "hp_percent": random.randint(85, 90),
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(90, 95),
            "evasion_percent": random.randint(95, 100),
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Spider": {
        "name": "Spider",
        "stats": {
            "hp_percent": random.randint(80, 85),       # Fragile
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(80, 85),
            "accuracy_percent": random.randint(105, 110), # Very accurate
            "evasion_percent": random.randint(100, 105),
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(95, 100),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Slime": {
        "name": "Slime",
        "stats": {
            "hp_percent": random.randint(105, 110),     # High HP
            "attack_percent": random.randint(85, 90),   
            "defence_percent": random.randint(100, 105), # Good defense
            "accuracy_percent": random.randint(85, 90),
            "evasion_percent": random.randint(80, 85),  # Poor evasion
            "crit_chance_percent": random.randint(80, 85),
            "crit_damage_percent": random.randint(85, 90),
            "armour_penetration_percent": random.randint(80, 85),
            "damage_reduction_percent": random.randint(100, 105), # Good reduction
            "block_chance_percent": random.randint(90, 95)
        },
        "tier": "low",
        "attack_types": ["normal", "poison", "draining", "defence_break"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Frog": {
        "name": "Frog",
        "stats": {
            "hp_percent": random.randint(90, 95),
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(100, 105),
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "stunning"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Tree Sprite": {
        "name": "Tree Sprite",
        "stats": {
            "hp_percent": random.randint(85, 90),
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(95, 100),
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(90, 95),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "low",
        "attack_types": ["normal", "draining", "stunning", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Snake": {
        "name": "Snake",
        "stats": {
            "hp_percent": random.randint(85, 90),
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(80, 85),
            "accuracy_percent": random.randint(100, 105),
            "evasion_percent": random.randint(100, 105),
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(95, 100),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["attack_weaken", "normal", "double", "poison"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Forest Hawk": {
        "name": "Forest Hawk",
        "stats": {
            "hp_percent": random.randint(80, 85),
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(80, 85),
            "accuracy_percent": random.randint(105, 110),
            "evasion_percent": random.randint(105, 110),
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(100, 105),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "stunning", "triple"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Locust": {
        "name": "Locust",
        "stats": {
            "hp_percent": random.randint(80, 85),
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(80, 85),
            "accuracy_percent": random.randint(100, 105),
            "evasion_percent": random.randint(100, 105),
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "triple"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Leprechaun": {
        "name": "Leprechaun",
        "stats": {
            "hp_percent": random.randint(90, 95),
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(100, 105),
            "evasion_percent": random.randint(105, 110),
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(100, 105),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(90, 95)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "stunning", "draining"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Deep Bat": {
        "name": "Deep Bat",
        "stats": {
            "hp_percent": random.randint(85, 90),
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(80, 85),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(105, 110),
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(95, 100),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "vampiric", "draining"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Giant Firefly": {
        "name": "Giant Firefly",
        "stats": {
            "hp_percent": random.randint(85, 90),
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(80, 85),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(105, 110),
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "burn", "poison"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Deepwood Stalker": {
        "name": "Deepwood Stalker",
        "stats": {
            "hp_percent": random.randint(90, 95),
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(95, 100),
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(95, 100),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "low",
        "attack_types": ["normal", "double", "poison", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Wood Spirit": {
        "name": "Wood Spirit",
        "stats": {
            "hp_percent": random.randint(90, 95),
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(95, 100),
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(90, 95),
            "block_chance_percent": random.randint(90, 95)
        },
        "tier": "low",
        "attack_types": ["normal", "draining", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Treant": {
        "name": "Treant",
        "stats": {
            "hp_percent": random.randint(105, 110),    # High HP
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(100, 105), # High defense
            "accuracy_percent": random.randint(80, 85),  # Poor accuracy
            "evasion_percent": random.randint(80, 85),  # Poor evasion
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(85, 90),
            "damage_reduction_percent": random.randint(95, 100),
            "block_chance_percent": random.randint(95, 100)
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
            "hp_percent": random.randint(105, 110),     # Tough hide
            "attack_percent": random.randint(100, 105),  # Strong bite
            "defence_percent": random.randint(105, 110), # Armored scales
            "accuracy_percent": random.randint(85, 90),  # Not very accurate
            "evasion_percent": random.randint(80, 85),   # Slow on land
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(105, 110), # Powerful bite
            "armour_penetration_percent": random.randint(100, 105), # Strong jaws
            "damage_reduction_percent": random.randint(105, 110),   # Tough scales
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "reckless", "stunning"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Poison Frog": {
        "name": "Poison Frog",
        "stats": {
            "hp_percent": random.randint(85, 90),       # Small and fragile
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(100, 105),
            "evasion_percent": random.randint(105, 110), # Very jumpy
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(95, 100),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Swamp Troll": {
        "name": "Swamp Troll",
        "stats": {
            "hp_percent": random.randint(110, 115),    # Very tough
            "attack_percent": random.randint(105, 110),
            "defence_percent": random.randint(105, 110),
            "accuracy_percent": random.randint(85, 90), # Not precise
            "evasion_percent": random.randint(85, 90), # Slow
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(105, 110),
            "block_chance_percent": random.randint(100, 105)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "poison", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Mosquito Swarm": {
        "name": "Mosquito Swarm",
        "stats": {
            "hp_percent": random.randint(85, 90),        # Fragile insects
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(110, 115), # Hard to miss as swarm
            "evasion_percent": random.randint(110, 115), # Hard to hit
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(90, 95),
            "armour_penetration_percent": random.randint(100, 105), # Find gaps
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "medium",
        "attack_types": ["normal", "triple", "poison", "draining"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Bog Witch": {
        "name": "Bog Witch",
        "stats": {
            "hp_percent": random.randint(95, 100),
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(90, 95),
            "accuracy_percent": random.randint(105, 110), # Magical accuracy
            "evasion_percent": random.randint(100, 105),
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105), # Magic ignores armor
            "damage_reduction_percent": random.randint(95, 100),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "poison", "burn", "draining"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Stone Golem": {
        "name": "Stone Golem",
        "stats": {
            "hp_percent": random.randint(110, 115),    # Stone body
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(110, 115), # Made of stone
            "accuracy_percent": random.randint(85, 90), # Slow
            "evasion_percent": random.randint(80, 85),  # Very slow
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(110, 115),
            "block_chance_percent": random.randint(105, 110)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Cultist": {
        "name": "Cultist",
        "stats": {
            "hp_percent": random.randint(95, 100),
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(90, 95),
            "accuracy_percent": random.randint(100, 105), # Trained fighter
            "evasion_percent": random.randint(95, 100),
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(95, 100),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "burn", "draining", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "arcane"
    },

    "Mummy": {
        "name": "Mummy",
        "stats": {
            "hp_percent": random.randint(100, 105),     # Undead durability
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(105, 110), # Wrapped protection
            "accuracy_percent": random.randint(90, 95),  # Stiff movement
            "evasion_percent": random.randint(85, 90),   # Slow
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(100, 105),
            "armour_penetration_percent": random.randint(95, 100),
            "damage_reduction_percent": random.randint(105, 110),
            "block_chance_percent": random.randint(100, 105)
        },
        "tier": "medium",
        "attack_types": ["normal", "draining", "stunning", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Animated Statue": {
        "name": "Animated Statue",
        "stats": {
            "hp_percent": random.randint(105, 110),     # Stone construction
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(110, 115), # Made of stone
            "accuracy_percent": random.randint(85, 90),  # Rigid movement
            "evasion_percent": random.randint(80, 85),   # Very stiff
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(110, 115),
            "block_chance_percent": random.randint(105, 110)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Temple Guardian": {
        "name": "Temple Guardian",
        "stats": {
            "hp_percent": random.randint(105, 110),
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(105, 110),
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(90, 95),
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(105, 110),
            "block_chance_percent": random.randint(110, 115) # Trained defender
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Mountain Lion": {
        "name": "Mountain Lion",
        "stats": {
            "hp_percent": random.randint(95, 100),
            "attack_percent": random.randint(105, 110),   # Strong predator
            "defence_percent": random.randint(90, 95),
            "accuracy_percent": random.randint(105, 110), # Hunter's precision
            "evasion_percent": random.randint(105, 110), # Very agile
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(90, 95),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "reckless", "triple"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Rock Elemental": {
        "name": "Rock Elemental",
        "stats": {
            "hp_percent": random.randint(110, 115),    # Stone body
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(110, 115), # Stone form
            "accuracy_percent": random.randint(85, 90),  # Slow
            "evasion_percent": random.randint(80, 85),   # Very slow
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(110, 115),
            "block_chance_percent": random.randint(105, 110)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "stunning", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Harpy": {
        "name": "Harpy",
        "stats": {
            "hp_percent": random.randint(90, 95),      # Light frame
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(90, 95),
            "accuracy_percent": random.randint(105, 110), # Aerial precision
            "evasion_percent": random.randint(110, 115), # Aerial agility
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(95, 100),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "stunning", "triple"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Yeti": {
        "name": "Yeti",
        "stats": {
            "hp_percent": random.randint(105, 110),    # Large and tough
            "attack_percent": random.randint(105, 110),
            "defence_percent": random.randint(100, 105), # Thick fur
            "accuracy_percent": random.randint(90, 95),
            "evasion_percent": random.randint(85, 90),  # Bulky
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(100, 105),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "reckless", "freeze"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Orc": {
        "name": "Orc",
        "stats": {
            "hp_percent": random.randint(100, 105),   # Tough
            "attack_percent": random.randint(105, 110), # Strong
            "defence_percent": random.randint(95, 100),
            "accuracy_percent": random.randint(90, 95), # Unrefined
            "evasion_percent": random.randint(90, 95), # Not agile
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(95, 100),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "reckless", "stunning"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Sand Wurm": {
        "name": "Sand Wurm",
        "stats": {
            "hp_percent": random.randint(110, 115),    # Large creature
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(105, 110), # Tough scales
            "accuracy_percent": random.randint(95, 100), # Burrow attack
            "evasion_percent": random.randint(95, 100), # Good at hiding
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(105, 110),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "power", "poison", "stunning"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Dried Mummy": {
        "name": "Dried Mummy",
        "stats": {
            "hp_percent": random.randint(100, 105),     # Preserved durability
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(100, 105), # Bandage wrapping
            "accuracy_percent": random.randint(90, 95),  # Stiff movement
            "evasion_percent": random.randint(85, 90),   # Very stiff
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(100, 105),
            "armour_penetration_percent": random.randint(95, 100),
            "damage_reduction_percent": random.randint(105, 110),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "draining", "poison", "burn"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Dust Devil": {
        "name": "Dust Devil",
        "stats": {
            "hp_percent": random.randint(85, 90),       # Ethereal form
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(90, 95),
            "accuracy_percent": random.randint(105, 110),
            "evasion_percent": random.randint(110, 115), # Wind form
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(95, 100),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "attack_weaken", "triple"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Phoenix": {
        "name": "Phoenix",
        "stats": {
            "hp_percent": random.randint(105, 110),    # Rebirth ability
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(90, 95),
            "accuracy_percent": random.randint(105, 110),
            "evasion_percent": random.randint(110, 115), # Aerial agility
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "burn", "triple"],
        "soultype": "standard",
        "monster_type": "fire"
    },

    "Desert Bandit": {
        "name": "Desert Bandit",
        "stats": {
            "hp_percent": random.randint(95, 100),
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(95, 100),
            "accuracy_percent": random.randint(105, 110), # Well trained
            "evasion_percent": random.randint(100, 105), # Agile fighter
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(90, 95),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "medium",
        "attack_types": ["normal", "double", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Leopard": {
        "name": "Leopard",
        "stats": {
            "hp_percent": random.randint(95, 100),      # Lean predator
            "attack_percent": random.randint(105, 110),  # Strong hunter
            "defence_percent": random.randint(90, 95),
            "accuracy_percent": random.randint(110, 115), # Expert hunter
            "evasion_percent": random.randint(110, 115), # Very agile
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
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
            "hp_percent": random.randint(95, 100),      # Lean but tough
            "attack_percent": random.randint(110, 115),  # Strong hunter
            "defence_percent": random.randint(85, 90),   # Light frame
            "accuracy_percent": random.randint(105, 110), # Good hunter
            "evasion_percent": random.randint(105, 110), # Very agile
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(95, 100),
            "damage_reduction_percent": random.randint(85, 90),     # Light protection
            "block_chance_percent": random.randint(80, 85)         # Dodges instead
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "double", "reckless", "triple", "stunning"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Twisted Mesquite": {
        "name": "Twisted Mesquite",
        "stats": {
            "hp_percent": random.randint(110, 115),     # Ancient tree
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(105, 110), # Hard bark
            "accuracy_percent": random.randint(85, 90),  # Slow moving
            "evasion_percent": random.randint(80, 85),   # Stationary
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(95, 100),
            "armour_penetration_percent": random.randint(90, 95),
            "damage_reduction_percent": random.randint(105, 110), # Very resistant
            "block_chance_percent": random.randint(100, 105)     # Natural shield
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "poison", "stunning", "damage_reflect", "draining"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Dustier Devil": {
        "name": "Dustier Devil",
        "stats": {
            "hp_percent": random.randint(85, 90),       # Insubstantial
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(85, 90),   # No physical form
            "accuracy_percent": random.randint(105, 110),
            "evasion_percent": random.randint(110, 115), # Wind form
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(100, 105),
            "armour_penetration_percent": random.randint(95, 100),
            "damage_reduction_percent": random.randint(80, 85),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "double", "triple", "draining", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Petrified Warrior": {
        "name": "Petrified Warrior",
        "stats": {
            "hp_percent": random.randint(105, 110),
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(110, 115), # Stone body
            "accuracy_percent": random.randint(90, 95),  # Combat training
            "evasion_percent": random.randint(80, 85),   # Stone form
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(100, 105),
            "armour_penetration_percent": random.randint(95, 100),
            "damage_reduction_percent": random.randint(105, 110),
            "block_chance_percent": random.randint(105, 110)     # Skilled defender
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "power", "stunning", "damage_reflect", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Thunderbird": {
        "name": "Thunderbird",
        "stats": {
            "hp_percent": random.randint(90, 95),
            "attack_percent": random.randint(105, 110),
            "defence_percent": random.randint(85, 90),    # Light frame
            "accuracy_percent": random.randint(105, 110), # Keen eyes
            "evasion_percent": random.randint(110, 115),  # Aerial agility
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(80, 85)
        },
        "tier": "medium-hard",
        "attack_types": ["normal", "double", "stunning", "triple", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "lightning"
    },

    "Valley Tiger": {
        "name": "Valley Tiger",
        "stats": {
            "hp_percent": random.randint(95, 100),
            "attack_percent": random.randint(110, 115),   # Apex predator
            "defence_percent": random.randint(90, 95),    # Medium hide
            "accuracy_percent": random.randint(105, 110), # Expert hunter
            "evasion_percent": random.randint(100, 105),  # Very agile
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(80, 85)
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
            "hp_percent": random.randint(115, 120),      # Multiple heads
            "attack_percent": random.randint(110, 115),  # Multiple attacks
            "defence_percent": random.randint(95, 100),
            "accuracy_percent": random.randint(100, 105), # Multiple heads help aim
            "evasion_percent": random.randint(85, 90),   # Large target
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(95, 100),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "poison", "double", "triple"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Plague Bearer": {
        "name": "Plague Bearer",
        "stats": {
            "hp_percent": random.randint(90, 95),       # Diseased form
            "attack_percent": random.randint(85, 90),    # Not physically strong
            "defence_percent": random.randint(85, 90),
            "accuracy_percent": random.randint(105, 110), # Disease spreads easily
            "evasion_percent": random.randint(85, 90),   # Shambling
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(115, 120), # Disease ignores armor
            "damage_reduction_percent": random.randint(90, 95),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "poison", "vampiric", "draining", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Mire Leviathan": {
        "name": "Mire Leviathan",
        "stats": {
            "hp_percent": random.randint(120, 125),      # Massive size
            "attack_percent": random.randint(115, 120),  # Incredible strength
            "defence_percent": random.randint(110, 115),
            "accuracy_percent": random.randint(85, 90),   # Unwieldy
            "evasion_percent": random.randint(85, 90),   # Too big to dodge
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(115, 120),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(110, 115),
            "block_chance_percent": random.randint(105, 110)
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "stunning", "poison", "defence_break"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Toxic Shambler": {
        "name": "Toxic Shambler",
        "stats": {
            "hp_percent": random.randint(90, 95),        # Rotting form
            "attack_percent": random.randint(85, 90),    # Not strong
            "defence_percent": random.randint(85, 90),   # Decaying
            "accuracy_percent": random.randint(95, 100),
            "evasion_percent": random.randint(85, 90),   # Shambling
            "crit_chance_percent": random.randint(95, 100),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(110, 115), # Toxic corrodes
            "damage_reduction_percent": random.randint(105, 110),   # Numb to pain
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "poison", "draining", "defence_break", "double"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Swamp Hag": {
        "name": "Swamp Hag",
        "stats": {
            "hp_percent": random.randint(85, 90),        # Frail form
            "attack_percent": random.randint(110, 115),  # Magical power
            "defence_percent": random.randint(85, 90),   # Physically weak
            "accuracy_percent": random.randint(115, 120), # Magical precision
            "evasion_percent": random.randint(100, 105),
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(115, 120), # Magic ignores armor
            "damage_reduction_percent": random.randint(95, 100),    # Magical wards
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "poison", "stunning", "draining", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "water"
    },

    "Ancient Golem": {
        "name": "Ancient Golem",
        "stats": {
            "hp_percent": random.randint(120, 125),      # Stone construction
            "attack_percent": random.randint(105, 110),
            "defence_percent": random.randint(120, 125), # Stone body
            "accuracy_percent": random.randint(85, 90),  # Slow
            "evasion_percent": random.randint(85, 90),   # Very slow
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(110, 115),
            "damage_reduction_percent": random.randint(115, 120),   # Nearly impervious
            "block_chance_percent": random.randint(110, 115)       # Living wall
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "stunning", "damage_reflect", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Cursed Pharaoh": {
        "name": "Cursed Pharaoh",
        "stats": {
            "hp_percent": random.randint(100, 105),      # Undead durability
            "attack_percent": random.randint(90, 95),    # Not physically strong
            "defence_percent": random.randint(95, 100),
            "accuracy_percent": random.randint(90, 95),
            "evasion_percent": random.randint(85, 90),   # Stiff movement
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(95, 100),
            "armour_penetration_percent": random.randint(115, 120), # Curse ignores armor
            "damage_reduction_percent": random.randint(105, 110),   # Ancient magic
            "block_chance_percent": random.randint(100, 105)       # Combat training
        },
        "tier": "hard",
        "attack_types": ["normal", "poison", "stunning", "draining", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Temporal Anomaly": {
        "name": "Temporal Anomaly",
        "stats": {
            "hp_percent": random.randint(85, 90),        # Unstable form
            "attack_percent": random.randint(90, 95),
            "defence_percent": random.randint(85, 90),   # Barely physical
            "accuracy_percent": random.randint(115, 120), # Time manipulation
            "evasion_percent": random.randint(115, 120), # Phase shifting
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(115, 120),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "stunning", "defence_break", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "void"
    },

    "Ruin Wraith": {
        "name": "Ruin Wraith",
        "stats": {
            "hp_percent": random.randint(85, 90),        # Spectral form
            "attack_percent": random.randint(105, 110),  # Spectral power
            "defence_percent": random.randint(85, 90),   # Incorporeal
            "accuracy_percent": random.randint(110, 115), # Ghostly precision
            "evasion_percent": random.randint(115, 120), # Phase through attacks
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(115, 120), # Ghost through armor
            "damage_reduction_percent": random.randint(85, 90),     # Can't block physical
            "block_chance_percent": random.randint(85, 90)         # Phases instead
        },
        "tier": "hard",
        "attack_types": ["normal", "draining", "vampiric", "stunning", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Forgotten Titan": {
        "name": "Forgotten Titan",
        "stats": {
            "hp_percent": random.randint(120, 125),      # Colossal size
            "attack_percent": random.randint(115, 120),  # Immense strength
            "defence_percent": random.randint(110, 115),
            "accuracy_percent": random.randint(85, 90),   # Too big to aim well
            "evasion_percent": random.randint(85, 90),   # Massive target
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(115, 120),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(110, 115),
            "block_chance_percent": random.randint(105, 110)
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "stunning", "defence_break"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Frost Giant": {
        "name": "Frost Giant",
        "stats": {
            "hp_percent": random.randint(115, 120),      # Giant size
            "attack_percent": random.randint(110, 115),  # Giant strength
            "defence_percent": random.randint(105, 110), # Ice armor
            "accuracy_percent": random.randint(85, 90),   # Slow attacks
            "evasion_percent": random.randint(85, 90),   # Too big
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(105, 110),   # Ice protection
            "block_chance_percent": random.randint(100, 105)       # Ice shield
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "stunning", "freeze", "defence_break"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Storm Harpy": {
        "name": "Storm Harpy",
        "stats": {
            "hp_percent": random.randint(90, 95),        # Light frame
            "attack_percent": random.randint(100, 105),
            "defence_percent": random.randint(85, 90),   # Fragile
            "accuracy_percent": random.randint(110, 115), # Aerial precision
            "evasion_percent": random.randint(115, 120), # Aerial mastery
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "stunning", "triple", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "lightning"
    },

    "Avalanche Elemental": {
        "name": "Avalanche Elemental",
        "stats": {
            "hp_percent": random.randint(110, 115),      # Mass of ice and snow
            "attack_percent": random.randint(105, 110),  # Crushing force
            "defence_percent": random.randint(115, 120), # Ice armor
            "accuracy_percent": random.randint(85, 90),   # Wild force
            "evasion_percent": random.randint(85, 90),   # Slow moving mass
            "crit_chance_percent": random.randint(85, 90),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(110, 115),   # Ice protection
            "block_chance_percent": random.randint(105, 110)       # Natural shield
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "freeze", "stunning", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Mountain Wyvern": {
        "name": "Mountain Wyvern",
        "stats": {
            "hp_percent": random.randint(100, 105),      # Dragon frame
            "attack_percent": random.randint(110, 115),  # Dragon strength
            "defence_percent": random.randint(95, 100),  # Dragon scales
            "accuracy_percent": random.randint(105, 110), # Hunter's eye
            "evasion_percent": random.randint(100, 105), # Aerial agility
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(110, 115),
            "armour_penetration_percent": random.randint(105, 110),
            "damage_reduction_percent": random.randint(95, 100),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "reckless", "stunning", "poison"],
        "soultype": "standard",
        "monster_type": "wind"
    },

    "Yeti Alpha": {
        "name": "Yeti Alpha",
        "stats": {
            "hp_percent": random.randint(115, 120),      # Massive bulk
            "attack_percent": random.randint(110, 115),  # Primal strength
            "defence_percent": random.randint(100, 105),
            "accuracy_percent": random.randint(90, 95),   # Wild swings
            "evasion_percent": random.randint(85, 90),   # Bulky
            "crit_chance_percent": random.randint(90, 95),
            "crit_damage_percent": random.randint(115, 120),
            "armour_penetration_percent": random.randint(100, 105),
            "damage_reduction_percent": random.randint(100, 105),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "freeze", "stunning"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Fire Elemental": {
        "name": "Fire Elemental",
        "stats": {
            "hp_percent": random.randint(90, 95),        # Unstable form
            "attack_percent": random.randint(115, 120),  # Intense heat
            "defence_percent": random.randint(85, 90),   # Fluid form
            "accuracy_percent": random.randint(100, 105),
            "evasion_percent": random.randint(100, 105), # Fluid movement
            "crit_chance_percent": random.randint(100, 105),
            "crit_damage_percent": random.randint(115, 120),
            "armour_penetration_percent": random.randint(115, 120), # Heat pierces
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "burn", "stunning"],
        "soultype": "standard",
        "monster_type": "fire"
    },

    "Sandstorm Djinn": {
        "name": "Sandstorm Djinn",
        "stats": {
            "hp_percent": random.randint(85, 90),        # Ethereal being
            "attack_percent": random.randint(95, 100),
            "defence_percent": random.randint(85, 90),   # Insubstantial
            "accuracy_percent": random.randint(110, 115), # Sand control
            "evasion_percent": random.randint(115, 120), # Wind form
            "crit_chance_percent": random.randint(105, 110),
            "crit_damage_percent": random.randint(105, 110),
            "armour_penetration_percent": random.randint(110, 115),
            "damage_reduction_percent": random.randint(85, 90),
            "block_chance_percent": random.randint(85, 90)
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "stunning", "damage_reflect", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Mirage Assassin": {
        "name": "Mirage Assassin",
        "stats": {
            "hp_percent": random.randint(90, 110),
            "attack_percent": random.randint(105, 125),
            "defence_percent": random.randint(80, 100),
            "accuracy_percent": random.randint(105, 125),
            "evasion_percent": random.randint(115, 135),
            "crit_chance_percent": random.randint(105, 125),
            "crit_damage_percent": random.randint(105, 125),
            "armour_penetration_percent": random.randint(105, 125),
            "damage_reduction_percent": random.randint(70, 90),
            "block_chance_percent": random.randint(65, 85)
        },
        "tier": "hard",
        "attack_types": ["normal", "double", "poison", "stunning", "vampiric"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Void Weaver": {
        "name": "Void Weaver",
        "stats": {
            "hp_percent": random.randint(85, 105),
            "attack_percent": random.randint(100, 120),
            "defence_percent": random.randint(75, 95),
            "accuracy_percent": random.randint(100, 120),
            "evasion_percent": random.randint(110, 130),
            "crit_chance_percent": random.randint(100, 120),
            "crit_damage_percent": random.randint(105, 125),
            "armour_penetration_percent": random.randint(115, 135),
            "damage_reduction_percent": random.randint(75, 95),
            "block_chance_percent": random.randint(60, 80)
        },
        "tier": "hard",
        "attack_types": ["normal", "draining", "stunning", "attack_weaken", "void_drain"],
        "soultype": "standard",
        "monster_type": "void"
    },

    "Abyssal Behemoth": {
        "name": "Abyssal Behemoth",
        "stats": {
            "hp_percent": random.randint(115, 135),
            "attack_percent": random.randint(110, 130),
            "defence_percent": random.randint(105, 125),
            "accuracy_percent": random.randint(75, 95),
            "evasion_percent": random.randint(65, 85),
            "crit_chance_percent": random.randint(80, 100),
            "crit_damage_percent": random.randint(110, 130),
            "armour_penetration_percent": random.randint(100, 120),
            "damage_reduction_percent": random.randint(105, 125),
            "block_chance_percent": random.randint(95, 115)
        },
        "tier": "hard",
        "attack_types": ["normal", "power", "reckless", "stunning", "reality_rend"],
        "soultype": "standard",
        "monster_type": "void"
    },
    # Very Hard Enemies
    "Necropolis Guardian": {
        "name": "Necropolis Guardian",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(110, 125),
            "defence_percent": random.randint(125, 130),
            "accuracy_percent": random.randint(90, 110),
            "evasion_percent": random.randint(88, 100),
            "crit_chance_percent": random.randint(88, 105),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(115, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(110, 125)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "draining", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Soul Reaver": {
        "name": "Soul Reaver",
        "stats": {
            "hp_percent": random.randint(90, 120),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(88, 105),
            "accuracy_percent": random.randint(115, 130),
            "evasion_percent": random.randint(120, 130),
            "crit_chance_percent": random.randint(115, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(125, 130),
            "damage_reduction_percent": random.randint(88, 100),
            "block_chance_percent": random.randint(88, 100)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "triple", "vampiric", "draining", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Bone Colossus": {
        "name": "Bone Colossus",
        "stats": {
            "hp_percent": random.randint(130, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(125, 130),
            "accuracy_percent": random.randint(88, 100),
            "evasion_percent": random.randint(88, 95),
            "crit_chance_percent": random.randint(88, 95),
            "crit_damage_percent": random.randint(125, 130),
            "armour_penetration_percent": random.randint(115, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(110, 125)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "reckless", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Spectral Devourer": {
        "name": "Spectral Devourer",
        "stats": {
            "hp_percent": random.randint(88, 115),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(88, 100),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(125, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(125, 130),
            "damage_reduction_percent": random.randint(88, 100),
            "block_chance_percent": random.randint(88, 95)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "vampiric", "poison", "draining", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "spirit"
    },

    "Lich King": {
        "name": "Lich King",
        "stats": {
            "hp_percent": random.randint(110, 125),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(105, 120),
            "accuracy_percent": random.randint(115, 130),
            "evasion_percent": random.randint(105, 120),
            "crit_chance_percent": random.randint(115, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(125, 130),
            "damage_reduction_percent": random.randint(115, 130),
            "block_chance_percent": random.randint(100, 125)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "draining", "poison", "freeze", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Timeless Sphinx": {
        "name": "Timeless Sphinx",
        "stats": {
            "hp_percent": random.randint(100, 125),
            "attack_percent": random.randint(115, 130),
            "defence_percent": random.randint(95, 120),
            "accuracy_percent": random.randint(125, 130),
            "evasion_percent": random.randint(120, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(125, 130),
            "damage_reduction_percent": random.randint(105, 120),
            "block_chance_percent": random.randint(88, 110)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "stunning", "draining", "poison", "attack_weaken", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "arcane"
    },

    "Eternal Pharaoh": {
        "name": "Eternal Pharaoh",
        "stats": {
            "hp_percent": random.randint(115, 130),
            "attack_percent": random.randint(110, 125),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(100, 125),
            "evasion_percent": random.randint(88, 105),
            "crit_chance_percent": random.randint(105, 120),
            "crit_damage_percent": random.randint(115, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(110, 125)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "poison", "draining", "defence_break", "stunning"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Anubis Reborn": {
        "name": "Anubis Reborn",
        "stats": {
            "hp_percent": random.randint(110, 125),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(105, 120),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(115, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(115, 130),
            "damage_reduction_percent": random.randint(100, 125),
            "block_chance_percent": random.randint(90, 120)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "vampiric", "stunning", "double", "defence_break", "triple"],
        "soultype": "standard",
        "monster_type": "arcane"
    },

    "Mummy Emperor": {
        "name": "Mummy Emperor",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(105, 120),
            "defence_percent": random.randint(125, 130),
            "accuracy_percent": random.randint(88, 115),
            "evasion_percent": random.randint(88, 95),
            "crit_chance_percent": random.randint(90, 120),
            "crit_damage_percent": random.randint(110, 125),
            "armour_penetration_percent": random.randint(115, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(115, 130)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "poison", "stunning", "damage_reflect", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "undead"
    },

    "Living Obelisk": {
        "name": "Living Obelisk",
        "stats": {
            "hp_percent": random.randint(130, 130),
            "attack_percent": random.randint(115, 130),
            "defence_percent": random.randint(130, 130),
            "accuracy_percent": random.randint(88, 100),
            "evasion_percent": random.randint(88, 95),
            "crit_chance_percent": random.randint(88, 95),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(125, 130),
            "block_chance_percent": random.randint(120, 130)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "reckless", "damage_reflect", "defence_break"],
        "soultype": "standard",
        "monster_type": "earth"
    },

    "Apocalypse Horseman": {
        "name": "Apocalypse Horseman",
        "stats": {
            "hp_percent": random.randint(110, 125),
            "attack_percent": random.randint(125, 130),
            "defence_percent": random.randint(100, 125),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(115, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(125, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(105, 120),
            "block_chance_percent": random.randint(90, 120)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "reckless", "poison", "draining", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "warrior"
    },

    "Abyssal Wyrm": {
        "name": "Abyssal Wyrm",
        "stats": {
            "hp_percent": random.randint(115, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(110, 125),
            "accuracy_percent": random.randint(110, 125),
            "evasion_percent": random.randint(90, 120),
            "crit_chance_percent": random.randint(115, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(105, 120),
            "block_chance_percent": random.randint(88, 115)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "poison", "stunning", "defence_break", "reckless"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Void Titan": {
        "name": "Void Titan",
        "stats": {
            "hp_percent": random.randint(125, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(115, 130),
            "accuracy_percent": random.randint(88, 105),
            "evasion_percent": random.randint(88, 95),
            "crit_chance_percent": random.randint(88, 110),
            "crit_damage_percent": random.randint(125, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(115, 130),
            "block_chance_percent": random.randint(110, 125)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "reckless", "stunning", "draining", "defence_break", "confusion"],
        "soultype": "standard",
        "monster_type": "void"
    },

    "Chaos Incarnate": {
        "name": "Chaos Incarnate",
        "stats": {
            "hp_percent": random.randint(100, 125),
            "attack_percent": random.randint(125, 130),
            "defence_percent": random.randint(88, 110),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(120, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(125, 130),
            "armour_penetration_percent": random.randint(125, 130),
            "damage_reduction_percent": random.randint(88, 105),
            "block_chance_percent": random.randint(88, 100)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "double", "poison", "vampiric", "attack_weaken", "stunning"],
        "soultype": "standard",
        "monster_type": "void"
    },

    "Eternity Warden": {
        "name": "Eternity Warden",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(110, 125),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(115, 130),
            "evasion_percent": random.randint(105, 120),
            "crit_chance_percent": random.randint(110, 125),
            "crit_damage_percent": random.randint(115, 130),
            "armour_penetration_percent": random.randint(115, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(115, 130)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "stunning", "freeze", "defence_break", "damage_reflect"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Ancient Wyvern": {
        "name": "Ancient Wyvern",
        "stats": {
            "hp_percent": random.randint(115, 130),
            "attack_percent": random.randint(125, 130),
            "defence_percent": random.randint(105, 120),
            "accuracy_percent": random.randint(115, 130),
            "evasion_percent": random.randint(110, 125),
            "crit_chance_percent": random.randint(115, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(115, 130),
            "damage_reduction_percent": random.randint(100, 125),
            "block_chance_percent": random.randint(88, 110)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "triple", "poison", "reckless", "stunning", "attack_weaken"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Elemental Drake": {
        "name": "Elemental Drake",
        "stats": {
            "hp_percent": random.randint(110, 125),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(100, 125),
            "accuracy_percent": random.randint(115, 130),
            "evasion_percent": random.randint(110, 125),
            "crit_chance_percent": random.randint(115, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(105, 120),
            "block_chance_percent": random.randint(88, 105)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "burn", "poison", "freeze", "stunning", "confusion"],
        "soultype": "standard",
        "monster_type": "ice"
    },

    "Dragonlord": {
        "name": "Dragonlord",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(125, 130),
            "defence_percent": random.randint(110, 125),
            "accuracy_percent": random.randint(115, 130),
            "evasion_percent": random.randint(100, 125),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(125, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(110, 125),
            "block_chance_percent": random.randint(95, 120)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "power", "reckless", "stunning", "damage_reflect", "confusion"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Chromatic Dragon": {
        "name": "Chromatic Dragon",
        "stats": {
            "hp_percent": random.randint(115, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(105, 120),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(115, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(125, 130),
            "damage_reduction_percent": random.randint(100, 125),
            "block_chance_percent": random.randint(88, 110)
        },
        "tier": "very-hard",
        "attack_types": ["normal", "burn", "poison", "freeze", "stunning", "confusion"],
        "soultype": "standard",
        "monster_type": "dragon"
    },

    "Elder Dragon": {
        "name": "Elder Dragon",
        "stats": {
            "hp_percent": random.randint(125, 130),
            "attack_percent": random.randint(125, 130),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(105, 120),
            "evasion_percent": random.randint(88, 115),
            "crit_chance_percent": random.randint(115, 130),
            "crit_damage_percent": random.randint(125, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(105, 120)
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
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(90, 100),
            "evasion_percent": random.randint(90, 100),
            "crit_chance_percent": random.randint(90, 110),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(115, 125)
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "reckless", "burn", "stunning", "damage_reflect", "defence_break"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Phoenix Overlord": {
        "name": "Phoenix Overlord",
        "stats": {
            "hp_percent": random.randint(100, 110),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(100, 110),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(120, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(90, 100),
            "block_chance_percent": random.randint(90, 100)
        },
        "tier": "extreme",
        "attack_types": ["normal", "double", "stunning", "triple", "burn", "attack_weaken", "vampiric"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Volcanic Titan": {
        "name": "Volcanic Titan",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(90, 105),
            "evasion_percent": random.randint(90, 100),
            "crit_chance_percent": random.randint(95, 110),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(115, 125)
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "stunning", "damage_reflect", "burn", "defence_break", "reckless"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Inferno Wyrm": {
        "name": "Inferno Wyrm",
        "stats": {
            "hp_percent": random.randint(110, 120),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(110, 120),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(120, 125),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(110, 120),
            "block_chance_percent": random.randint(95, 100)
        },
        "tier": "extreme",
        "attack_types": ["normal", "double", "power", "reckless", "defence_break", "burn", "attack_weaken"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Cinder Archfiend": {
        "name": "Cinder Archfiend",
        "stats": {
            "hp_percent": random.randint(105, 115),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(105, 115),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(120, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(100, 110),
            "block_chance_percent": random.randint(95, 105)
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "confusion", "vampiric", "attack_weaken", "burn", "defence_break"],
        "soultype": "boss",
        "monster_type": "fire"
    },

    "Cosmic Devourer": {
        "name": "Cosmic Devourer",
        "stats": {
            "hp_percent": random.randint(105, 115),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(100, 110),
            "accuracy_percent": random.randint(120, 130),
            "evasion_percent": random.randint(120, 130),
            "crit_chance_percent": random.randint(120, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(90, 100),
            "block_chance_percent": random.randint(90, 100)
        },
        "tier": "extreme",
        "attack_types": ["normal", "double", "triple", "confusion", "stunning", "draining", "attack_weaken"],
        "soultype": "boss",
        "monster_type": "void"
    },

    "Astral Behemoth": {
        "name": "Astral Behemoth",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(95, 105),
            "evasion_percent": random.randint(95, 100),
            "crit_chance_percent": random.randint(100, 110),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(110, 115)
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "confusion", "reckless", "defence_break", "stunning", "damage_reflect"],
        "soultype": "boss",
        "monster_type": "void"
    },

    "Galactic Leviathan": {
        "name": "Galactic Leviathan",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(115, 120),
            "evasion_percent": random.randint(110, 120),
            "crit_chance_percent": random.randint(110, 120),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(115, 125),
            "block_chance_percent": random.randint(110, 120)
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "poison", "stunning", "defence_break"],
        "soultype": "boss",
        "monster_type": "arcane"
    },

    "Nebula Colossus": {
        "name": "Nebula Colossus",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(90, 105),
            "evasion_percent": random.randint(90, 100),
            "crit_chance_percent": random.randint(95, 110),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(115, 120),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(115, 120)
        },
        "tier": "extreme",
        "attack_types": ["normal", "power", "confusion", "damage_reflect", "reckless", "stunning", "defence_break"],
        "soultype": "boss",
        "monster_type": "arcane"
    },

    "Celestial Titan": {
        "name": "Celestial Titan",
        "stats": {
            "hp_percent": random.randint(120, 130),
            "attack_percent": random.randint(120, 130),
            "defence_percent": random.randint(120, 130),
            "accuracy_percent": random.randint(115, 120),
            "evasion_percent": random.randint(100, 110),
            "crit_chance_percent": random.randint(115, 120),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(120, 130),
            "damage_reduction_percent": random.randint(120, 130),
            "block_chance_percent": random.randint(110, 115)
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
            "hp_percent": random.randint(105, 130),
            "attack_percent": random.randint(105, 130),
            "defence_percent": random.randint(105, 130),
            "accuracy_percent": random.randint(105, 120),
            "evasion_percent": random.randint(105, 115),
            "crit_chance_percent": random.randint(105, 120),
            "crit_damage_percent": random.randint(105, 130),
            "armour_penetration_percent": random.randint(110, 125),
            "damage_reduction_percent": random.randint(105, 130),
            "block_chance_percent": random.randint(110, 125)
        },
        "tier": "boss",
        "attack_types": ["normal", "power", "stunning", "draining", "reckless", "damage_reflect", "triple", "freeze"],
        "soultype": "boss",
        "monster_type": "warrior"
    },

    "Celestial Arbiter": {
        "name": "Celestial Arbiter",
        "stats": {
            "hp_percent": random.randint(105, 120),
            "attack_percent": random.randint(105, 130),
            "defence_percent": random.randint(105, 115),
            "accuracy_percent": random.randint(105, 130),
            "evasion_percent": random.randint(105, 130),
            "crit_chance_percent": random.randint(105, 130),
            "crit_damage_percent": random.randint(105, 130),
            "armour_penetration_percent": random.randint(105, 130),
            "damage_reduction_percent": random.randint(105, 110),
            "block_chance_percent": random.randint(100, 110)
        },
        "tier": "boss",
        "attack_types": ["normal", "double", "draining", "stunning", "triple", "vampiric", "attack_weaken", "damage_reflect"],
        "soultype": "boss",
        "monster_type": "arcane"
    },

    "Astral Demiurge": {
        "name": "Astral Demiurge",
        "stats": {
            "hp_percent": random.randint(110, 125),
            "attack_percent": random.randint(105, 130),
            "defence_percent": random.randint(110, 125),
            "accuracy_percent": random.randint(105, 130),
            "evasion_percent": random.randint(105, 120),
            "crit_chance_percent": random.randint(110, 125),
            "crit_damage_percent": random.randint(105, 130),
            "armour_penetration_percent": random.randint(105, 130),
            "damage_reduction_percent": random.randint(105, 120),
            "block_chance_percent": random.randint(105, 115)
        },
        "tier": "boss",
        "attack_types": ["normal", "power", "poison", "freeze", "stunning", "vampiric", "defence_break", "reality_rend"],
        "soultype": "boss",
        "monster_type": "void"
    },

    "Ethereal Leviathan": {
        "name": "Ethereal Leviathan",
        "stats": {
            "hp_percent": random.randint(105, 130),
            "attack_percent": random.randint(105, 130),
            "defence_percent": random.randint(105, 115),
            "accuracy_percent": random.randint(105, 120),
            "evasion_percent": random.randint(105, 130),
            "crit_chance_percent": random.randint(110, 125),
            "crit_damage_percent": random.randint(105, 130),
            "armour_penetration_percent": random.randint(105, 130),
            "damage_reduction_percent": random.randint(105, 110),
            "block_chance_percent": random.randint(100, 110)
        },
        "tier": "boss",
        "attack_types": ["normal", "reckless", "draining", "double", "poison", "triple", "damage_reflect", "void_drain"],
        "soultype": "boss",
        "monster_type": "spirit"
    },

    "Divine Architect": {
        "name": "Divine Architect",
        "stats": {
            "hp_percent": random.randint(105, 130),
            "attack_percent": random.randint(105, 130),
            "defence_percent": random.randint(105, 130),
            "accuracy_percent": random.randint(110, 125),
            "evasion_percent": random.randint(105, 115),
            "crit_chance_percent": random.randint(110, 125),
            "crit_damage_percent": random.randint(105, 130),
            "armour_penetration_percent": random.randint(105, 130),
            "damage_reduction_percent": random.randint(105, 130),
            "block_chance_percent": random.randint(110, 125)
        },
        "tier": "boss",
        "attack_types": ["normal", "power", "stunning", "freeze", "draining", "reckless", "defence_break", "confusion"],
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
            "crit_chance_percent": random.randint(110, 130),
            "crit_damage_percent": random.randint(120, 130),
            "armour_penetration_percent": random.randint(40, 60),
            "damage_reduction_percent": random.randint(110, 120),
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
            "attack_percent": random.randint(105, 130),  # Void-enhanced strikes
            "defence_percent": random.randint(70, 95),   # Insubstantial - lower defense
            "accuracy_percent": random.randint(110, 130), # Highly precise void attacks
            "evasion_percent": random.randint(110, 125), # Phase shifting makes it hard to hit
            "crit_chance_percent": random.randint(105, 130), # Finds weaknesses in reality
            "crit_damage_percent": random.randint(105, 130), # Devastating void strikes
            "armour_penetration_percent": random.randint(100, 125), # Void pierces armor
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
            "attack_percent": random.randint(125, 130),  # Stronger void energies
            "defence_percent": random.randint(85, 110),  # Better control of form
            "accuracy_percent": random.randint(120, 130), # Master of void precision
            "evasion_percent": random.randint(120, 130), # Superior phase shifting
            "crit_chance_percent": random.randint(105, 125), # Expert at finding weaknesses
            "crit_damage_percent": random.randint(100, 125), # Devastating void mastery
            "armour_penetration_percent": random.randint(105, 130), # Enhanced void penetration
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
            "hp_percent": random.randint(110, 130),
            "attack_percent": random.randint(110, 130),
            "defence_percent": random.randint(105, 125),
            "accuracy_percent": random.randint(90, 120),
            "evasion_percent": random.randint(80, 110),
            "crit_chance_percent": random.randint(90, 120),
            "crit_damage_percent": random.randint(90, 115),
            "armour_penetration_percent": random.randint(100, 130),
            "damage_reduction_percent": random.randint(100, 125),
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

TIER_RANGES = {
    "low": (80, 95),
    "medium": (85, 105),
    "medium-hard": (90, 115),
    "hard": (95, 120),
    "very-hard": (100, 125),
    "extreme": (105, 130),
    "boss": (110, 130)
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
        "extra_attacks": 2,
        "effect": "self_damage"
    },
    "vampiric": {
        "name": "Vampiric Strike",
        "damage_modifier": 0.9,
        "effect": "lifesteal"
    },
    "reckless": {
        "name": "Reckless Assault",
        "damage_modifier": 2,
        "effect": "self_damage"
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

class Enemy(Character):
    def __init__(self, name=None, hp=None, attack=None, defence=None, accuracy=None, evasion=None, 
             crit_chance=None, crit_damage=None, armour_penetration=None, damage_reduction=None, 
             block_chance=None, exp=None, gold=None, tier=None, level=0, attack_types=None, template=None, player=None):
        
        if template and player:
            self.template = template
            self.tier = template["tier"]
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
            
    def get_hybrid_level_scale(self, player_level, enemy_level):
        """Calculate scaling based on level difference and enemy tier"""
        level_diff = enemy_level - player_level
        base_scale = 1.0
        
        # Expanded scaling based on wider level ranges
        if level_diff <= -5: base_scale = 0.88
        elif level_diff <= -3: base_scale = 0.91
        elif level_diff <= -2: base_scale = 0.94
        elif level_diff <= 0: base_scale = 0.97
        elif level_diff <= 2: base_scale = 1.0
        elif level_diff <= 4: base_scale = 1.03
        elif level_diff <= 6: base_scale = 1.06
        elif level_diff <= 8: base_scale = 1.09
        else: base_scale = 1.12

        # Tier multipliers adjusted for wider ranges
        tier_multipliers = {
            "low": 0.95,        # Reduced to prevent low-tier from being too strong
            "medium": 1.0,
            "medium-hard": 1.05,
            "hard": 1.1,
            "very-hard": 1.15,
            "extreme": 1.2,
            "boss": 1.25
        }
        
        tier_scale = tier_multipliers.get(self.tier, 1.0)
        
        # Cap based on tier to prevent low-tier enemies from being too strong
        tier_caps = {
            "low": 1.05,
            "medium": 1.1,
            "medium-hard": 1.15,
            "hard": 1.2,
            "very-hard": 1.25,
            "extreme": 1.3,
            "boss": 1.35
        }
        
        final_scale = min(tier_caps.get(self.tier, 1.4), base_scale * tier_scale)
        return final_scale
    
    def _calculate_stats_with_debug(self, player, template):
        stats = {}
        debug = self.debug_info
        
        # Use balanced stat generation
        template_stats = generate_balanced_stats(template["tier"])
        
        # Store base percentages and modifications
        debug['base_percentages'] = template_stats.copy()
        debug['template_mods'] = template_stats.copy()
        base_percentages = template_stats.copy()
        
        # Handle variant
        stats['name'] = template['name']
        # Store and track attack types
        debug['attack_types'] = {
            'base': template["attack_types"].copy(),
            'final': template["attack_types"].copy()
        }
        
        stats['attack_types'] = template["attack_types"].copy()
        debug['variant_roll'] = random.random()
        
        if debug['variant_roll'] < 0.1:
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

        # Level ranges based on tier
        tier_level_ranges = {
            "low": (1, 2),
            "medium": (2, 3),
            "medium-hard": (3, 4),
            "hard": (4, 6),
            "very-hard": (5, 7),
            "extreme": (6, 8),
            "boss": (7, 9)
        }
        
        level_range = tier_level_ranges.get(self.tier, (2, 3))
        level_min = max(1, player.level - level_range[0])
        level_max = player.level + level_range[1]
        stats['level'] = random.randint(level_min, level_max)
        
        # Get scaling factor
        level_scale = self.get_hybrid_level_scale(player.level, stats['level'])
        
        debug['level_calc'] = {
            'min': level_min,
            'max': level_max,
            'chosen': stats['level'],
            'scale': level_scale,
            'tier': self.tier
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
                    (player.equipment_modifiers.get("attack") * 0.75)) * 
                    (base_percentages["attack_percent"] / 100) * debug['level_scale'])
        stats['defence'] = int((player.base_defence + player.level_modifiers.get("defence") + 
                    (player.equipment_modifiers.get("defence") * 0.75)) * 
                    (base_percentages["defence_percent"] / 100) * debug['level_scale'])
                    
        # Store final percentages used
        debug['final_percentages'] = base_percentages.copy()
        
        # Calculate remaining stats with caps
        stats.update(self._calculate_secondary_stats(player, base_percentages))
        
        # Calculate rewards
        debug['exp_roll'] = random.randint(8, 20)
        debug['gold_roll'] = random.randint(8, 20)
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
                        (player.equipment_modifiers.get("accuracy", 0) * 0.7))
        accuracy = int(base_accuracy * base_percentages["accuracy_percent"] / 100)
        stats['accuracy'] = min(130, accuracy)
        debug['accuracy'] = {
            'base': player.base_accuracy,
            'level_mod': player.level_modifiers.get("accuracy", 0),
            'equipment_mod': player.equipment_modifiers.get("accuracy", 0),
            'equipment_scaled': player.equipment_modifiers.get("accuracy", 0) * 0.7,
            'total_base': base_accuracy,
            'percent_mod': base_percentages["accuracy_percent"],
            'calculated': accuracy,
            'final': stats['accuracy']
        }
        
        # Evasion calculation
        base_evasion = (player.base_evasion + player.level_modifiers.get("evasion", 0) + 
                    (player.equipment_modifiers.get("evasion", 0) * 0.75))
        evasion = int(base_evasion * base_percentages["evasion_percent"] / 100)
        stats['evasion'] = min(50, evasion)
        debug['evasion'] = {
            'base': player.base_evasion,
            'level_mod': player.level_modifiers.get("evasion", 0),
            'equipment_mod': player.equipment_modifiers.get("evasion", 0),
            'equipment_scaled': player.equipment_modifiers.get("evasion", 0) * 0.75,
            'total_base': base_evasion,
            'percent_mod': base_percentages["evasion_percent"],
            'calculated': evasion,
            'final': stats['evasion']
        }
        
        # Crit chance calculation
        base_crit_chance = (player.base_crit_chance + player.level_modifiers.get("crit_chance", 0) + 
                        (player.equipment_modifiers.get("crit_chance", 0) * 0.75))
        crit_chance = int(base_crit_chance * base_percentages["crit_chance_percent"] / 100)
        stats['crit_chance'] = min(50, crit_chance)
        debug['crit_chance'] = {
            'base': player.base_crit_chance,
            'level_mod': player.level_modifiers.get("crit_chance", 0),
            'equipment_mod': player.equipment_modifiers.get("crit_chance", 0),
            'equipment_scaled': player.equipment_modifiers.get("crit_chance", 0) * 0.75,
            'total_base': base_crit_chance,
            'percent_mod': base_percentages["crit_chance_percent"],
            'calculated': crit_chance,
            'final': stats['crit_chance']
        }
        
        # Crit damage calculation
        base_crit_damage = (player.base_crit_damage + player.level_modifiers.get("crit_damage", 0) + 
                        (player.equipment_modifiers.get("crit_damage", 0) * 0.75))
        crit_damage = int(base_crit_damage * base_percentages["crit_damage_percent"] / 100)
        stats['crit_damage'] = min(250, max(100, crit_damage))  # Minimum 100%, maximum 250%
        debug['crit_damage'] = {
            'base': player.base_crit_damage,
            'level_mod': player.level_modifiers.get("crit_damage", 0),
            'equipment_mod': player.equipment_modifiers.get("crit_damage", 0),
            'equipment_scaled': player.equipment_modifiers.get("crit_damage", 0) * 0.75,
            'total_base': base_crit_damage,
            'percent_mod': base_percentages["crit_damage_percent"],
            'calculated': crit_damage,
            'final': stats['crit_damage']
        }
        
        # Armour penetration calculation
        base_armour_pen = (player.base_armour_penetration + 
                        player.level_modifiers.get("armour_penetration", 0) + 
                        (player.equipment_modifiers.get("armour_penetration", 0) * 0.75))
        armour_pen = int(base_armour_pen * base_percentages["armour_penetration_percent"] / 100)
        stats['armour_penetration'] = min(50, armour_pen)
        debug['armour_penetration'] = {
            'base': player.base_armour_penetration,
            'level_mod': player.level_modifiers.get("armour_penetration", 0),
            'equipment_mod': player.equipment_modifiers.get("armour_penetration", 0),
            'equipment_scaled': player.equipment_modifiers.get("armour_penetration", 0) * 0.75,
            'total_base': base_armour_pen,
            'percent_mod': base_percentages["armour_penetration_percent"],
            'calculated': armour_pen,
            'final': stats['armour_penetration']
        }
        
        # Damage reduction calculation
        base_damage_red = (player.base_damage_reduction + 
                        player.level_modifiers.get("damage_reduction", 0) + 
                        (player.equipment_modifiers.get("damage_reduction", 0) * 0.75))
        damage_red = int(base_damage_red * base_percentages["damage_reduction_percent"] / 100)
        stats['damage_reduction'] = min(30, damage_red)
        debug['damage_reduction'] = {
            'base': player.base_damage_reduction,
            'level_mod': player.level_modifiers.get("damage_reduction", 0),
            'equipment_mod': player.equipment_modifiers.get("damage_reduction", 0),
            'equipment_scaled': player.equipment_modifiers.get("damage_reduction", 0) * 0.75,
            'total_base': base_damage_red,
            'percent_mod': base_percentages["damage_reduction_percent"],
            'calculated': damage_red,
            'final': stats['damage_reduction']
        }
        
        # Block chance calculation
        base_block = (player.base_block_chance + 
                    player.level_modifiers.get("block_chance", 0) + 
                    (player.equipment_modifiers.get("block_chance", 0) * 0.75))
        block = int(base_block * base_percentages["block_chance_percent"] / 100)
        stats['block_chance'] = min(30, block)
        debug['block_chance'] = {
            'base': player.base_block_chance,
            'level_mod': player.level_modifiers.get("block_chance", 0),
            'equipment_mod': player.equipment_modifiers.get("block_chance", 0),
            'equipment_scaled': player.equipment_modifiers.get("block_chance", 0) * 0.75,
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
        debug.append(f"Equipment modifier (60%): {attack_equipment * 0.75}")
        debug.append(f"Combined base: {attack_base + attack_level + (attack_equipment * 0.75)}")
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
        debug.append(f"Equipment modifier (60%): {defence_equipment * 0.75}")
        debug.append(f"Combined base: {defence_base + defence_level + (defence_equipment * 0.75)}")
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

def get_stat_range(tier, stat_type):
    """Get the appropriate stat range based on tier and stat type"""
    base_min, base_max = TIER_RANGES.get(tier, (80, 95))
    
    stat_modifiers = {
        "hp_percent": (0, 10),
        "attack_percent": (0, 5),
        "defence_percent": (0, 5),
        "accuracy_percent": (-5, 5),
        "evasion_percent": (-5, 5),
        "crit_chance_percent": (-10, 0),
        "crit_damage_percent": (0, 5),
        "armour_penetration_percent": (-5, 5),
        "damage_reduction_percent": (-5, 5),
        "block_chance_percent": (-5, 5)
    }
    
    mod_min, mod_max = stat_modifiers.get(stat_type, (0, 0))
    return (base_min + mod_min, base_max + mod_max)

def generate_balanced_stats(tier):
    """Generate balanced stats with ±5% randomization"""
    stats = {}
    for stat in [
        "hp_percent", "attack_percent", "defence_percent", 
        "accuracy_percent", "evasion_percent", "crit_chance_percent",
        "crit_damage_percent", "armour_penetration_percent", 
        "damage_reduction_percent", "block_chance_percent"
    ]:
        min_val, max_val = get_stat_range(tier, stat)
        base_value = random.randint(min_val, max_val)
        # Add ±5% randomization
        random_factor = random.uniform(0.95, 1.05)
        stats[stat] = int(base_value * random_factor)
    return stats

# Helper function to create enemies
def create_enemy(enemy_type, player=None):
    """Create a new enemy either from template + player scaling or from ENEMY_TEMPLATES directly"""
    if enemy_type in ENEMY_TEMPLATES:
        template = ENEMY_TEMPLATES[enemy_type]
        enemy = Enemy(template=template, player=player)
        enemy.soultype = template.get("soultype", "standard")
        enemy.monster_type = template.get("monster_type", "unknown")
        # print(enemy.debug_stat_calculation(player))
        return enemy
    return None

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