# Just the variant names, used for kill tracking
VARIANT_TYPES = {
    "Frenzied", "Ancient", "Ethereal", "Colossal", "Corrupted", 
    "Swift", "Vampiric", "Armoured", "Void-Touched"
}

# Monster Types to be used with new custom equipment and Crystals
MONSTER_TYPES = {
    "dragon": {
        "stat_preferences": ["attack", "crit_damage", "armour_penetration", "crit_chance", "accuracy"],
        "equipment_affinities": ["weapon", "chest", "helm", "gloves", "ring"],
        "members": [
            "Dragon", "Shadow Dragon", "Elder Dragon", 
            "Chromatic Dragon", "Dragonlord", "Abyssal Wyrm", 
            "Ancient Wyvern"
        ]
    },
    
    # Undead Types
    "undead": {
        "stat_preferences": ["defence", "damage_reduction", "block_chance", "max_hp", "attack"],
        "equipment_affinities": ["shield", "chest", "helm", "boots", "gloves"],
        "members": [
            "Mummy", "Dried Mummy", "Cursed Pharaoh", "Eternal Pharaoh",
            "Bone Colossus", "Necropolis Guardian", "Lich King", "Twisted Mesquite",
            "Plague Bearer", "Toxic Shambler", "Mummy Emperor"
        ]
    },
    "spirit": {
        "stat_preferences": ["evasion", "accuracy", "crit_chance", "armour_penetration", "crit_damage"],
        "equipment_affinities": ["ring", "back", "gloves", "weapon", "boots"],
        "members": [
            "Echo Wraith", "Ruin Wraith", "Ethereal Banshee",
            "Tree Sprite", "Wood Spirit", "Soul Reaver",
            "Spectral Devourer", "Treant", "Dust Devil",
            "Dustier Devil", "Sandstorm Djinn", "Ethereal Leviathan"
        ]
    },
    
    # Elemental Types
    "wind": {
        "stat_preferences": ["evasion", "accuracy", "crit_damage", "attack", "crit_chance"],
        "equipment_affinities": ["back", "boots", "gloves", "helm", "ring"],
        "members": [
            "Plains Hawk", "Forest Hawk", "Bat", "Deep Bat",
            "Locust", "Mosquito Swarm", "Harpy", "Giant Firefly",
            "Mountain Wyvern"
        ]
    },
    "fire": {
        "stat_preferences": ["attack", "crit_damage", "armour_penetration", "accuracy", "crit_chance"],
        "equipment_affinities": ["weapon", "ring", "gloves", "chest", "helm"],
        "members": [
            "Fire Elemental", "Magma Colossus", "Phoenix Overlord",
            "Volcanic Titan", "Cinder Archfiend", "Phoenix", "Sunburst Phoenix",
            "Inferno Wyrm"
        ]
    },
    "ice": {
        "stat_preferences": ["defence", "damage_reduction", "block_chance", "max_hp", "attack"],
        "equipment_affinities": ["shield", "chest", "helm", "gloves", "boots"],
        "members": [
            "Frost Giant", "Yeti", "Yeti Alpha", 
            "Avalanche Elemental", "Eternity Warden", "Elemental Drake"
        ]
    },
    "earth": {
        "stat_preferences": ["defence", "damage_reduction", "block_chance", "max_hp", "armour_penetration"],
        "equipment_affinities": ["shield", "chest", "helm", "gloves", "boots"],
        "members": [
            "Mountain Lion", "Canyon Cougar", 
            "Strider", "Stone Golem", "Ancient Golem", "Animated Statue",
            "Living Obelisk", "Temple Guardian", "Rock Elemental", "Sand Wurm"
        ]
    },
    "grass": {
        "stat_preferences": ["evasion", "accuracy", "crit_chance", "attack", "crit_damage"],
        "equipment_affinities": ["boots", "back", "gloves", "weapon", "ring"],
        "members": [
            "Valley Tiger", "Spider", "Snake", "Deepwood Stalker", "Leopard",
            "Rat", "Boar", "Bull", "Nightmare Stalker"
        ]
    },
    "water": {
        "stat_preferences": ["evasion", "defence", "block_chance", "damage_reduction", "attack"],
        "equipment_affinities": ["boots", "shield", "chest", "helm", "gloves"],
        "members": [
            "Frog", "Alligator", "Poison Frog", "Slime", "Swamp Troll",
            "Bog Witch", "Swamp Hag", "Venomous Hydra", "Mire Leviathan"
        ]
    },
    "lightning": {
        "stat_preferences": ["accuracy", "evasion", "crit_damage", "attack", "crit_chance"],
        "equipment_affinities": ["weapon", "ring", "back", "gloves", "boots"],
        "members": [
            "Storm Harpy", "Thunderbird", "Storm Drake",
            "Tempest Elemental"
        ]
    },
    
    # Magical Types
    "arcane": {
        "stat_preferences": ["attack", "accuracy", "crit_damage", "armour_penetration", "crit_chance"],
        "equipment_affinities": ["ring", "weapon", "back", "gloves", "helm"],
        "members": [
            "Crystal Guardian", "Soul Forgemaster", "Divine Architect", "Timeless Sphinx",
            "Cultist", "Anubis Reborn", "Galatic Leviathan", "Nebula Colossus", "Celestial Titan",
            "Celestial Arbiter"
        ]
    },
    "void": {
        "stat_preferences": ["evasion", "accuracy", "crit_damage", "armour_penetration", "attack"],
        "equipment_affinities": ["ring", "weapon", "back", "gloves", "helm"],
        "members": [
            "Void Walker", "Empowered Void Walker", "Void Titan", 
            "Void Weaver", "Cosmic Devourer", "Astral Behemoth",
            "Temporal Anomaly", "Abyssal Behemoth", "Chaos Incarnate",
            "Astral Demiurge"
        ]
    },
    
    # Warrior Types
    "warrior": {
        "stat_preferences": ["attack", "defence", "block_chance", "damage_reduction", "armour_penetration"],
        "equipment_affinities": ["weapon", "shield", "chest", "helm", "boots"],
        "members": [
            "Petrified Warrior", "Desert Bandit", "Forgotten Titan"
            "Orc", "Apocalypse Horseman", "Goblin", "Leprechaun",
            "Mirage Assassin", "Desert Colossus", "Seraphim Guardian",
            "Shrine Guardian"
        ]
    },
    
    # Test Type
    "test": {
        "stat_preferences": ["attack", "defence", "evasion", "accuracy", "crit_chance"],
        "equipment_affinities": ["weapon", "chest", "gloves", "boots", "helm"],
        "members": [
            "Test Monster"
        ]
    }
}