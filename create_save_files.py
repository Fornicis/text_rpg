import json
import os

def create_save_files():
    # Create saves directory if it doesn't exist
    SAVE_DIRECTORY = "saves"
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

    level_setups = [
        {
    "level": 5,
    "gold": 500,
    "equipment": {
        "weapon": {
            "name": "Iron Shortsword",
            "type": "weapon",
            "value": 90,
            "tier": "uncommon",
            "stats": {
                "attack": 25,
                "accuracy": 23,
                "crit_chance": 5,
                "crit_damage": 130,
                "armour_penetration": 2,
                "weapon_type": "light"
            }
        },
        "helm": {
            "name": "Bronze Sallet",
            "type": "helm",
            "value": 40,
            "tier": "uncommon",
            "stats": {
                "defence": 3,
                "accuracy": 3,
                "crit_chance": 1
            }
        },
        "chest": {
            "name": "Bronze Battle Cuirass",
            "type": "chest",
            "value": 60,
            "tier": "uncommon",
            "stats": {
                "defence": 5,
                "attack": 4,
                "crit_chance": 1
            }
        },
        "legs": {
            "name": "Bronze Defender Greaves",
            "type": "legs",
            "value": 50,
            "tier": "uncommon",
            "stats": {
                "defence": 5,
                "damage_reduction": 3
            }
        },
        "boots": {
            "name": "Bronze Striker Boots",
            "type": "boots",
            "value": 35,
            "tier": "uncommon",
            "stats": {
                "defence": 3,
                "attack": 3
            }
        },
        "gloves": {
            "name": "Bronze Striker Gloves",
            "type": "gloves",
            "value": 30,
            "tier": "uncommon",
            "stats": {
                "defence": 2,
                "attack": 4
            }
        },
        "shield": {
            "name": "Bronze Kite Shield",
            "type": "shield",
            "value": 32,
            "tier": "uncommon",
            "stats": {
                "defence": 4,
                "block_chance": 3
            }
        },
        "belt": {
            "name": "Bronze Skirmisher's Strap",
            "type": "belt",
            "value": 35,
            "tier": "uncommon",
            "stats": {
                "defence": 2,
                "evasion": 3
            }
        },
        "back": {
            "name": "Shadowed Cape",
            "type": "back",
            "value": 45,
            "tier": "uncommon",
            "stats": {
                "defence": 2,
                "crit_chance": 4
            }
        },
        "ring": {
            "name": "Bronze Ring of Power",
            "type": "ring",
            "value": 60,
            "tier": "uncommon",
            "stats": {
                "attack": 3,
                "defence": 3
            }   
        }
    },
    "modifiers": {
        "attack": 18,
        "defence": 13,
        "accuracy": 15,
        "evasion": 5,
        "crit_chance": 7,
        "crit_damage": 15,
        "armour_penetration": 5,
        "damage_reduction": 5,
        "block_chance": 5
    },
    "consumables": [
        "Health Potion",
        "Strength Tonic",
        "Iron Skin Elixir",
        "Accuracy Tonic",
        "Guard Tonic",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation"
    ]
},
{
    "level": 10,
    "gold": 1500,
    "equipment": {
        "weapon": {
            "name": "Steel Sword",
            "type": "weapon",
            "value": 240,
            "tier": "rare",
            "stats": {
                "attack": 40,
                "accuracy": 23,
                "crit_chance": 5,
                "crit_damage": 140,
                "armour_penetration": 3,
                "weapon_type": "medium"
            }
        },
        "helm": {
            "name": "Steel Fortress Helm",
            "type": "helm",
            "value": 80,
            "tier": "rare",
            "stats": {
                "defence": 7,
                "damage_reduction": 4
            }
        },
        "chest": {
            "name": "Steel Warlord's Cuirass",
            "type": "chest",
            "value": 125,
            "tier": "rare",
            "stats": {
                "defence": 7,
                "attack": 5,
                "crit_chance": 2
            }
        },
        "legs": {
            "name": "Steel Berserker Cuisses",
            "type": "legs",
            "value": 115,
            "tier": "rare",
            "stats": {
                "defence": 5,
                "attack": 4,
                "crit_damage": 2
            }
        },
        "boots": {
            "name": "Steel Bulwark Greaves",
            "type": "boots",
            "value": 78,
            "tier": "rare",
            "stats": {
                "defence": 4,
                "damage_reduction": 4
            }
        },
        "gloves": {
            "name": "Steel Crushing Fists",
            "type": "gloves",
            "value": 95,
            "tier": "rare",
            "stats": {
                "attack": 5,
                "defence": 3
            }
        },
        "shield": {
            "name": "Steel Guardian Shield",
            "type": "shield",
            "value": 48,
            "tier": "rare",
            "stats": {
                "defence": 5,
                "block_chance": 4
            }
        },
        "belt": {
            "name": "Steel Shadowdancer's Belt",
            "type": "belt",
            "value": 88,
            "tier": "rare",
            "stats": {
                "defence": 3,
                "evasion": 4
            }
        },
        "back": {
            "name": "Mantle of the Unseen Strike",
            "type": "back",
            "value": 105,
            "tier": "rare",
            "stats": {
                "defence": 3,
                "crit_chance": 5
            }
        },
        "ring": {
            "name": "Steel Signet of the Warrior",
            "type": "ring",
            "value": 155,
            "tier": "rare",
            "stats": {
                "attack": 4,
                "defence": 4
            }   
        }
    },
    "modifiers": {
        "attack": 30,
        "defence": 25,
        "accuracy": 30,
        "evasion": 10,
        "crit_chance": 15,
        "crit_damage": 30,
        "armour_penetration": 10,
        "damage_reduction": 10,
        "block_chance": 10
    },
    "consumables": [
        "Greater Health Potion",
        "Greater Strength Tonic",
        "Greater Iron Skin Elixir", 
        "Greater Accuracy Tonic",
        "Greater Guard Tonic",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation"
    ]
},
        {
    "level": 15,
    "gold": 3000,
    "equipment": {
        "weapon": {
            "name": "Mithril Sword",
            "type": "weapon",
            "value": 600,
            "tier": "epic",
            "stats": {
                "attack": 53,
                "accuracy": 25,
                "crit_chance": 6,
                "crit_damage": 145,
                "armour_penetration": 4,
                "weapon_type": "medium"
            }
        },
        "helm": {
            "name": "Mithril Juggernaut Helm",
            "type": "helm",
            "value": 280,
            "tier": "epic",
            "stats": {
                "defence": 9,
                "damage_reduction": 4
            }
        },
        "chest": {
            "name": "Mithril Commander's Armor",
            "type": "chest",
            "value": 360,
            "tier": "epic",
            "stats": {
                "defence": 9,
                "attack": 6,
                "crit_chance": 3
            }
        },
        "legs": {
            "name": "Mithril Juggernaut Legguards",
            "type": "legs",
            "value": 340,
            "tier": "epic",
            "stats": {
                "defence": 9,
                "damage_reduction": 5
            }
        },
        "boots": {
            "name": "Mithril Juggernaut Sabatons",
            "type": "boots",
            "value": 310,
            "tier": "epic",
            "stats": {
                "defence": 5,
                "damage_reduction": 5
            }
        },
        "gloves": {
            "name": "Mithril Warlord's Fists",
            "type": "gloves",
            "value": 280,
            "tier": "epic",
            "stats": {
                "defence": 4,
                "attack": 6
            }
        },
        "shield": {
            "name": "Mithril Fortress Shield",
            "type": "shield",
            "value": 230,
            "tier": "epic",
            "stats": {
                "defence": 6,
                "damage_reduction": 5
            }
        },
        "belt": {
            "name": "Mithril Whisperwind Cincture",
            "type": "belt",
            "value": 300,
            "tier": "epic",
            "stats": {
                "defence": 4,
                "evasion": 5
            }
        },
        "back": {
            "name": "Cloak of Deadly Precision",
            "type": "back",
            "value": 330,
            "tier": "epic",
            "stats": {
                "defence": 4,
                "crit_chance": 6
            }
        },
        "ring": {
            "name": "Mithril Ring of Conquest",
            "type": "ring",
            "value": 350,
            "tier": "epic",
            "stats": {
                "attack": 5,
                "defence": 5
            }   
        }
    },
    "modifiers": {
        "attack": 45,
        "defence": 27,
        "accuracy": 45,
        "evasion": 15,
        "crit_chance": 22,
        "crit_damage": 45,
        "armour_penetration": 15,
        "damage_reduction": 15,
        "block_chance": 15
    },
    "consumables": [
        "Epic Strength Tonic",
        "Epic Iron Skin Elixir",
        "Epic Accuracy Tonic",
        "Epic Guard Tonic",
        "Supreme Health Potion",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation"
    ]
},
{
    "level": 20,
    "gold": 5000,
    "equipment": {
        "weapon": {
            "name": "Adamantite Sword",
            "type": "weapon",
            "value": 2400,
            "tier": "legendary",
            "stats": {
                "attack": 79,
                "accuracy": 28,
                "crit_chance": 8,
                "crit_damage": 155,
                "armour_penetration": 6,
                "weapon_type": "medium"
            }
        },
        "helm": {
            "name": "Adamantite Helm of the Unbreakable",
            "type": "helm",
            "value": 1100,
            "tier": "legendary",
            "stats": {
                "defence": 13,
                "damage_reduction": 6
            }
        },
        "chest": {
            "name": "Adamantite Godplate of the Unassailable",
            "type": "chest",
            "value": 1350,
            "tier": "legendary",
            "stats": {
                "defence": 19,
                "damage_reduction": 7
            }
        },
        "legs": {
            "name": "Adamantite Fortress Legguards",
            "type": "legs",
            "value": 1300,
            "tier": "legendary",
            "stats": {
                "defence": 13,
                "damage_reduction": 7
            }
        },
        "boots": {
            "name": "Adamantite Fortress Greaves",
            "type": "boots",
            "value": 1220,
            "tier": "legendary",
            "stats": {
                "defence": 7,
                "damage_reduction": 7
            }
        },
        "gloves": {
            "name": "Adamantite Worldbreaker Fists",
            "type": "gloves",
            "value": 1180,
            "tier": "legendary",
            "stats": {
                "defence": 6,
                "attack": 8
            }
        },
        "shield": {
            "name": "Adamantite Invincible Rampart",
            "type": "shield",
            "value": 980,
            "tier": "legendary",
            "stats": {
                "defence": 8,
                "damage_reduction": 7
            }
        },
        "belt": {
            "name": "Adamantite Shadowmeld Belt",
            "type": "belt",
            "value": 1200,
            "tier": "legendary",
            "stats": {
                "defence": 6,
                "evasion": 7
            }
        },
        "back": {
            "name": "Cloak of Devastating Strikes",
            "type": "back",
            "value": 1270,
            "tier": "legendary",
            "stats": {
                "defence": 6,
                "crit_chance": 8
            }
        },
        "ring": {
            "name": "Adamantite Loop of Supreme Power",
            "type": "ring",
            "value": 1550,
            "tier": "legendary",
            "stats": {
                "attack": 7,
                "defence": 7
            }   
        }
    },
    "modifiers": {
        "attack": 60,
        "defence": 36,
        "accuracy": 60,
        "evasion": 20,
        "crit_chance": 30,
        "crit_damage": 60,
        "armour_penetration": 20,
        "damage_reduction": 20,
        "block_chance": 20
    },
    "consumables": [
        "Legendary Strength Tonic",
        "Legendary Iron Skin Elixir",
        "Legendary Guard Tonic",
        "Legendary Critical Tonic",
        "Godly Health Potion",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation"
    ]
},
        {
    "level": 25,
    "gold": 8000,
    "equipment": {
        "weapon": {
            "name": "Worldsplitter",
            "type": "weapon",
            "value": 5400,
            "tier": "mythical",
            "stats": {
                "attack": 92,
                "accuracy": 25,
                "crit_chance": 9,
                "crit_damage": 170,
                "armour_penetration": 9,
                "weapon_type": "heavy"
            }
        },
        "helm": {
            "name": "Crown of Eternal Fortitude",
            "type": "helm",
            "value": 5200,
            "tier": "mythical",
            "stats": {
                "defence": 15,
                "damage_reduction": 7
            }
        },
        "chest": {
            "name": "Vestment of Cosmic Fortitude",
            "type": "chest",
            "value": 5600,
            "tier": "mythical",
            "stats": {
                "defence": 22,
                "damage_reduction": 8
            }
        },
        "legs": {
            "name": "Legplates of Cosmic Fortitude",
            "type": "legs",
            "value": 5400,
            "tier": "mythical",
            "stats": {
                "defence": 15,
                "damage_reduction": 8
            }
        },
        "boots": {
            "name": "Sabatons of Cosmic Fortitude",
            "type": "boots",
            "value": 5350,
            "tier": "mythical",
            "stats": {
                "defence": 8,
                "damage_reduction": 8
            }
        },
        "gloves": {
            "name": "Fists of Reality's Wrath",
            "type": "gloves",
            "value": 5150,
            "tier": "mythical",
            "stats": {
                "defence": 7,
                "attack": 9
            }
        },
        "shield": {
            "name": "Bulwark of Cosmic Fortitude",
            "type": "shield",
            "value": 4900,
            "tier": "mythical",
            "stats": {
                "defence": 9,
                "damage_reduction": 8
            }
        },
        "belt": {
            "name": "Belt of Dimensional Flux",
            "type": "belt",
            "value": 5300,
            "tier": "mythical",
            "stats": {
                "defence": 7,
                "evasion": 8
            }
        },
        "back": {
            "name": "Shroud of Universal Precision",
            "type": "back",
            "value": 5450,
            "tier": "mythical",
            "stats": {
                "defence": 7,
                "crit_chance": 9
            }
        },
        "ring": {
            "name": "Band of Divine Providence",
            "type": "ring",
            "value": 6100,
            "tier": "mythical",
            "stats": {
                "attack": 8,
                "defence": 8
            }   
        }
    },
    "modifiers": {
        "attack": 75,
        "defence": 45,
        "accuracy": 75,
        "evasion": 25,
        "crit_chance": 30,
        "crit_damage": 75,
        "armour_penetration": 25,
        "damage_reduction": 25,
        "block_chance": 25
    },
    "consumables": [
        "Godly Strength Tonic",
        "Godly Iron Skin Elixir",
        "Godly Guard Tonic",
        "Godly Critical Tonic",
        "Essence of Eternity",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation",
        "Scroll of Teleportation"
    ]
}
    ]

    for setup in level_setups:
        level = setup["level"]
        base_hp = 100 + (level * 50)
        base_stamina = 100 + (level * 10)
        
        # Calculate equipment modifiers
        equipment_modifiers = {
            "attack": 0,
            "defence": 0,
            "accuracy": 0,
            "evasion": 0,
            "crit_chance": 0,
            "crit_damage": 0,
            "armour_penetration": 0,
            "damage_reduction": 0,
            "block_chance": 0
        }

        for item in setup["equipment"].values():
            if item is not None:
                for stat, value in item["stats"].items():
                    if stat != "weapon_type" and value > 0:
                        equipment_modifiers[stat] = equipment_modifiers.get(stat, 0) + value
        
        # Calculate actual stats including base + level modifiers
        save = {
            "player": {
                "name": f"Level{level}Character",
                "level": level,
                "exp": 0,
                "hp": base_hp,
                "max_hp": base_hp,
                "stamina": base_stamina,
                "max_stamina": base_stamina,
                "attack": 10 + setup["modifiers"]["attack"] + equipment_modifiers["attack"],
                "defence": 5 + setup["modifiers"]["defence"] + equipment_modifiers["defence"],
                "accuracy": 70 + setup["modifiers"]["accuracy"] + equipment_modifiers["accuracy"],
                "evasion": 5 + setup["modifiers"]["evasion"] + equipment_modifiers["evasion"],
                "crit_chance": 5 + setup["modifiers"]["crit_chance"] + equipment_modifiers["crit_chance"],
                "crit_damage": 150 + setup["modifiers"]["crit_damage"] + equipment_modifiers["crit_damage"],
                "armour_penetration": level + equipment_modifiers["armour_penetration"],
                "damage_reduction": level + equipment_modifiers["damage_reduction"],
                "block_chance": 5 + level + equipment_modifiers["block_chance"],
                "gold": setup["gold"],
                "base_attack": 10,
                "base_defence": 5,
                "respawn_counter": 5,
                "days": level * 2,
                "visited_locations": ["Village", "Forest", "Cave", "Mountain", "Deepwoods", "Plains", "Swamp", "Temple", "Desert", "Valley", "Toxic Swamp", "Ruins", "Mountain Peaks", "Scorching Plains", "Shadowed Valley", "Death Caves", "Ancient Ruins", "Death Valley", "Dragons Lair", "Volcanic Valley", "Heavens"],
                "level_modifiers": setup["modifiers"],
                "equipment_modifiers": equipment_modifiers,
                "buff_modifiers": {"attack": 0, "defence": 0, "evasion": 0, "accuracy": 0, "crit_damage": 0, "crit_chance": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0},
                "combat_buff_modifiers": {"attack": 0, "defence": 0, "evasion": 0, "accuracy": 0, "crit_damage": 0, "crit_chance": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0},
                "weapon_buff_modifiers": {},
                "debuff_modifiers": {"attack": 0, "defence": 0, "evasion": 0, "accuracy": 0, "crit_damage": 0, "crit_chance": 0, "armour_penetration": 0, "damage_reduction": 0, "block_chance": 0},
                "cooldowns": {},
                "active_buffs": {},
                "combat_buffs": {},
                "weapon_buff": {"value": 0, "duration": 0},
                "soul_crystal_effects": {},
                "weapon_coating": None,
                "active_hots": {},
                "kill_tracker": {},
                "variant_kill_tracker": {},
                "boss_kill_tracker": {},
                "used_kill_tracker": {},
                "used_variant_tracker": {},
                "used_boss_kill_tracker": {},
                "status_effects": [],
                "inventory": setup["consumables"],
                "equipped": setup["equipment"]
            },
            "current_location": "Village"
        }

        filename = f"level_{level}_save.json"
        filepath = os.path.join(SAVE_DIRECTORY, filename)
        with open(filepath, 'w') as f:
            json.dump(save, f, indent=2)
        print(f"Created save file for level {level}")

if __name__ == "__main__":
    create_save_files()