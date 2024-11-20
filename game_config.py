# Just the variant names, used for kill tracking
VARIANT_TYPES = {
    "Frenzied", "Ancient", "Ethereal", "Colossal", "Corrupted", 
    "Swift", "Vampiric", "Armoured", "Void-Touched"
}

# Monster Types to be used with new custom equipment and Crystals

MONSTER_TYPES = {
    # Beast Types
    "beast": {
        "stat_preferences": ["attack", "crit_chance", "crit_damage"],
        "equipment_affinities": ["weapon", "gloves", "boots"],
        "members": [
            "Rat", "Boar", "Bull", "Mountain Lion", "Valley Tiger", 
            "Canyon Cougar", "Leopard", "Plains Hawk", "Forest Hawk",
            "Bat", "Deep Bat"
        ]
    },
    "dragon": {
        "stat_preferences": ["attack", "crit_damage", "armour_penetration"],
        "equipment_affinities": ["weapon", "chest", "helm"],
        "members": [
            "Dragon", "Shadow Dragon", "Elder Dragon", 
            "Chromatic Dragon", "Dragonlord", "Abyssal Wyrm", 
            "Inferno Wyrm", "Ancient Wyvern"
        ]
    },
    
    # Undead Types
    "undead": {
        "stat_preferences": ["defence", "damage_reduction", "block_chance"],
        "equipment_affinities": ["shield", "chest", "helm"],
        "members": [
            "Mummy", "Dried Mummy", "Cursed Pharaoh", "Eternal Pharaoh",
            "Bone Colossus", "Necropolis Guardian", "Lich King"
        ]
    },
    "spirit": {
        "stat_preferences": ["evasion", "accuracy", "crit_chance"],
        "equipment_affinities": ["ring", "back", "gloves"],
        "members": [
            "Echo Wraith", "Ruin Wraith", "Ethereal Banshee",
            "Tree Sprite", "Wood Spirit", "Soul Reaver",
            "Spectral Devourer"
        ]
    },
    
    # Elemental Types
    "fire": {
        "stat_preferences": ["attack", "crit_damage", "armour_penetration"],
        "equipment_affinities": ["weapon", "ring", "gloves"],
        "members": [
            "Fire Elemental", "Magma Colossus", "Phoenix Overlord",
            "Volcanic Titan", "Cinder Archfiend", "Phoenix"
        ]
    },
    "ice": {
        "stat_preferences": ["defence", "damage_reduction", "block_chance"],
        "equipment_affinities": ["shield", "chest", "helm"],
        "members": [
            "Frost Giant", "Yeti", "Yeti Alpha", 
            "Avalanche Elemental"
        ]
    },
    "storm": {
        "stat_preferences": ["accuracy", "evasion", "crit_damage"],
        "equipment_affinities": ["weapon", "ring", "back"],
        "members": [
            "Storm Harpy", "Thunderbird", "Storm Drake",
            "Tempest Elemental"
        ]
    },
    
    # Magical Types
    "arcane": {
        "stat_preferences": ["attack", "accuracy", "armour_penetration"],
        "equipment_affinities": ["ring", "weapon", "back"],
        "members": [
            "Bog Witch", "Swamp Hag", "Crystal Guardian", 
            "Soul Forgemaster", "Divine Architect", "Timeless Sphinx"
        ]
    },
    "void": {
        "stat_preferences": ["evasion", "accuracy", "crit_damage"],
        "equipment_affinities": ["ring", "weapon", "back"],
        "members": [
            "Void Walker", "Empowered Void Walker", "Void Titan", 
            "Void Weaver", "Cosmic Devourer", "Astral Behemoth",
            "Temporal Anomaly"
        ]
    },
    
    # Warrior Types
    "warrior": {
        "stat_preferences": ["attack", "defence", "block_chance"],
        "equipment_affinities": ["weapon", "shield", "chest"],
        "members": [
            "Temple Guardian", "Petrified Warrior", "Desert Bandit",
            "Cultist", "Orc", "Apocalypse Horseman"
        ]
    },
    
    # Construct Types
    "construct": {
        "stat_preferences": ["defence", "damage_reduction", "block_chance"],
        "equipment_affinities": ["shield", "chest", "helm"],
        "members": [
            "Stone Golem", "Ancient Golem", "Animated Statue",
            "Living Obelisk"
        ]
    },
    
    # Corrupted Types
    "corrupted": {
        "stat_preferences": ["attack", "armour_penetration", "crit_damage"],
        "equipment_affinities": ["weapon", "chest", "gloves"],
        "members": [
            "Plague Bearer", "Toxic Shambler", "Cursed Pharaoh",
            "Corrupted Guardian"
        ]
    }
}