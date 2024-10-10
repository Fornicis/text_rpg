from player import Character
import random

class Enemy(Character):
    def __init__(self, name, hp, attack, defence, exp, gold, tier, level=0, attack_types=None):
        super().__init__(name, hp, attack, defence)
        self.exp = exp
        self.gold = gold
        self.tier = tier
        self.level = level
        if attack_types:
            self.attack_types = {attack_type: ENEMY_ATTACK_TYPES[attack_type] for attack_type in attack_types}
        else:
            self.attack_types = {"normal": ENEMY_ATTACK_TYPES["normal"]}
        
        
    def choose_attack(self):
        return random.choice(list(self.attack_types.keys()))
        
    """ Effects to add
            "confusion": f"{player.name} is confused! They might hurt themselves on their next turn.",
            "defense_break": f"{player.name}'s armor is shattered! Their defense is temporarily lowered.",
            "double_attack": f"{self.name} strikes one more time!",
            "triple_attack": f"{self.name} strikes two more times!",
            "execute_low_health": f"The attack deals extra damage due to {player.name}'s low health!",
            "damage_share": f"{player.name} is linked with {self.name}! They'll share some of the damage they deal.",
            "mana_drain": f"{player.name}'s energy is drained! They lose some stamina.",
            "weaken": f"{player.name} has been cursed! Their attacks will be weaker for a few turns.",
            "absorb_buff": f"{self.name} absorbs some of {player.name}'s power, growing stronger!",
            "random_effect": "A chaotic energy surges through the battlefield!",
            # Add descriptions for boss-specific effects
            "divine_smite": "Divine energy rains down, dealing massive damage!",
            "random_debuff": "Reality shifts around you, applying random negative effects!",
            "ignore_defense": "The cosmic energy bypasses your defenses completely!",
            "heal_damage": f"{self.name} consumes the void, healing itself!",
            "alter_stats": "The fabric of reality changes, altering your stats!",
            "invulnerability": f"{self.name} is surrounded by an impenetrable divine shield!",
            "ultimate_damage": "Cosmic forces converge to deal devastating damage!"
        }"""
    
def initialise_enemies():
    return {
            # Easy Enemies (Levels 1-4)
            "Rat": Enemy("Rat", 21, 21, 5, 10, random.randrange(3, 10), "low", 1, ["normal", "double", "poison"]),
            "Boar": Enemy("Boar", 30, 24, 7, 15, random.randrange(5, 15), "low", 2, ["normal", "power", "reckless"]),
            "Plains Hawk": Enemy("Plains Hawk", 19, 26, 4, 20, random.randrange(8, 18), "low", 1, ["normal", "double", "stunning"]),
            "Strider": Enemy("Strider", 34, 25, 8, 25, random.randrange(10, 20), "low", 2, ["normal", "double", "power"]),
            "Bull": Enemy("Bull", 43, 27, 10, 30, random.randrange(12, 24), "low", 3, ["normal", "power", "reckless"]),
            
            "Bat": Enemy("Bat", 24, 23, 6, 10, random.randrange(3, 10), "low", 1, ["normal", "double", "vampiric"]),
            "Goblin": Enemy("Goblin", 27, 25, 8, 15, random.randrange(5, 15), "low", 2, ["normal", "double", "poison"]),
            "Spider": Enemy("Spider", 22, 26, 5, 20, random.randrange(8, 18), "low", 1, ["normal", "double", "poison"]),
            "Slime": Enemy("Slime", 38, 22, 9, 25, random.randrange(10, 20), "low", 2, ["normal", "poison", "stunning"]),
            "Frog": Enemy("Frog", 36, 26, 8, 30, random.randrange(12, 24), "low", 3, ["normal", "double", "poison"]),
            
            "Tree Sprite": Enemy("Tree Sprite", 20, 24, 6, 10, random.randrange(3, 10), "low", 1, ["normal", "double", "draining"]),
            "Snake": Enemy("Snake", 24, 27, 5, 15, random.randrange(5, 15), "low", 1, ["normal", "double", "poison"]),
            "Forest Hawk": Enemy("Forest Hawk", 29, 25, 7, 20, random.randrange(8, 18), "low", 2, ["normal", "double", "stunning"]),
            "Locust": Enemy("Locust", 26, 26, 6, 25, random.randrange(10, 20), "low", 2, ["normal", "double", "poison"]),
            "Leprechaun": Enemy("Leprechaun", 41, 23, 9, 30, random.randrange(12, 24), "low", 3, ["normal", "double", "stunning"]),
            
            "Wood Spirit": Enemy("Wood Spirit", 26, 24, 7, 10, random.randrange(3, 10), "low", 1, ["normal", "draining", "stunning"]),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 32, 26, 9, 15, random.randrange(5, 15), "low", 2, ["normal", "double", "poison"]),
            "Deep Bat": Enemy("Deep Bat", 27, 27, 7, 20, random.randrange(8, 18), "low", 2, ["normal", "double", "vampiric"]),
            "Giant Firefly": Enemy("Giant Firefly", 34, 24, 8, 25, random.randrange(10, 20), "low", 2, ["normal", "double", "poison"]),
            "Treant": Enemy("Treant", 51, 25, 12, 30, random.randrange(12, 24), "low", 3, ["normal", "power", "stunning"]),
            
            # Medium Enemies (Levels 5-9)
            "Alligator": Enemy("Alligator", 77, 43, 30, 35, random.randrange(30, 41), "medium", 5, ["normal", "power", "reckless"]),
            "Poison Frog": Enemy("Poison Frog", 60, 45, 28, 40, random.randrange(35, 46), "medium", 4, ["normal", "double", "poison"]),
            "Swamp Troll": Enemy("Swamp Troll", 89, 44, 32, 45, random.randrange(40, 51), "medium", 6, ["normal", "power", "poison"]),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 64, 47, 26, 35, random.randrange(30, 41), "medium", 4, ["normal", "double", "poison"]),
            "Bog Witch": Enemy("Bog Witch", 72, 43, 29, 50, random.randrange(45, 56), "medium", 5, ["normal", "poison", "stunning"]),
            
            "Stone Golem": Enemy("Stone Golem", 102, 42, 34, 55, random.randrange(50, 61), "medium", 6, ["normal", "power", "stunning"]),
            "Cultist": Enemy("Cultist", 68, 46, 28, 40, random.randrange(35, 46), "medium", 4, ["normal", "draining", "poison"]),
            "Mummy": Enemy("Mummy", 81, 44, 31, 45, random.randrange(40, 51), "medium", 5, ["normal", "draining", "stunning"]),
            "Animated Statue": Enemy("Animated Statue", 85, 43, 32, 50, random.randrange(45, 56), "medium", 5, ["normal", "power", "stunning"]),
            "Temple Guardian": Enemy("Temple Guardian", 94, 43, 33, 55, random.randrange(50, 61), "medium", 6, ["normal", "power", "stunning"]),
            
            "Mountain Lion": Enemy("Mountain Lion", 72, 48, 29, 40, random.randrange(35, 46), "medium", 4, ["normal", "double", "reckless"]),
            "Rock Elemental": Enemy("Rock Elemental", 98, 41, 35, 50, random.randrange(45, 56), "medium", 6, ["normal", "power", "stunning"]),
            "Harpy": Enemy("Harpy", 68, 48, 27, 45, random.randrange(40, 51), "medium", 4, ["normal", "double", "stunning"]),
            "Yeti": Enemy("Yeti", 89, 45, 33, 50, random.randrange(45, 56), "medium", 6, ["normal", "power", "reckless", "freeze"]),
            "Orc": Enemy("Orc", 81, 46, 30, 40, random.randrange(35, 46), "medium", 5, ["normal", "power", "reckless"]),
            
            "Sand Wurm": Enemy("Sand Wurm", 94, 44, 34, 45, random.randrange(40, 51), "medium", 6, ["normal", "power", "poison"]),
            "Dried Mummy": Enemy("Dried Mummy", 85, 43, 31, 40, random.randrange(35, 46), "medium", 5, ["normal", "draining", "poison"]),
            "Dust Devil": Enemy("Dust Devil", 64, 49, 28, 45, random.randrange(40, 51), "medium", 4, ["normal", "double", "stunning"]),
            "Desert Bandit": Enemy("Desert Bandit", 77, 47, 30, 50, random.randrange(45, 56), "medium", 5, ["normal", "double", "poison"]),
            "Leopard": Enemy("Leopard", 68, 40, 27, 35, random.randrange(30, 41), "medium", 3, ["normal", "double", "reckless"]),
            
            # Medium-Hard Enemies (Levels 10-14)
            "Canyon Cougar": Enemy("Canyon Cougar", 111, 60, 50, 70, random.randrange(65, 81), "medium-hard", 10, ["normal", "double", "reckless"]),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 136, 57, 52, 75, random.randrange(70, 86), "medium-hard", 12, ["normal", "poison", "stunning"]),
            "Dustier Devil": Enemy("Dustier Devil", 123, 61, 49, 80, random.randrange(75, 91), "medium-hard", 11, ["normal", "double", "stunning"]),
            "Petrified Warrior": Enemy("Petrified Warrior", 119, 60, 48, 85, random.randrange(80, 96), "medium-hard", 10, ["normal", "power", "stunning"]),
            "Thunderbird": Enemy("Thunderbird", 132, 63, 49, 90, random.randrange(85, 101), "medium-hard", 11, ["normal", "double", "stunning"]),
            
            # Hard Enemies (Levels 15-19)
            "Venomous Hydra": Enemy("Venomous Hydra", 170, 78, 87, 120, random.randrange(95, 116), "hard", 15, ["normal", "power", "poison"]),
            "Plague Bearer": Enemy("Plague Bearer", 162, 81, 84, 125, random.randrange(100, 121), "hard", 16, ["normal", "poison", "vampiric"]),
            "Mire Leviathan": Enemy("Mire Leviathan", 204, 83, 86, 130, random.randrange(105, 126), "hard", 17, ["normal", "power", "stunning"]),
            "Toxic Shambler": Enemy("Toxic Shambler", 153, 87, 82, 135, random.randrange(110, 131), "hard", 18, ["normal", "poison", "vampiric"]),
            "Swamp Hag": Enemy("Swamp Hag", 166, 89, 80, 140, random.randrange(115, 136), "hard", 19, ["normal", "poison", "stunning"]),
            
            "Ancient Golem": Enemy("Ancient Golem", 230, 75, 90, 120, random.randrange(120, 141), "hard", 15, ["normal", "power", "stunning"]),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 187, 79, 86, 125, random.randrange(125, 146), "hard", 16, ["normal", "poison", "stunning"]),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 170, 84, 83, 130, random.randrange(130, 151), "hard", 17, ["normal", "double", "stunning"]),
            "Ruin Wraith": Enemy("Ruin Wraith", 179, 86, 81, 135, random.randrange(135, 156), "hard", 18, ["normal", "draining", "vampiric"]),
            "Forgotten Titan": Enemy("Forgotten Titan", 221, 88, 85, 140, random.randrange(140, 161), "hard", 19, ["normal", "power", "reckless"]),
            
            "Frost Giant": Enemy("Frost Giant", 221, 76, 89, 100, random.randrange(145, 166), "hard", 15, ["normal", "power", "stunning", "freeze"]),
            "Storm Harpy": Enemy("Storm Harpy", 170, 83, 82, 105, random.randrange(150, 171), "hard", 16, ["normal", "double", "stunning"]),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 204, 85, 84, 110, random.randrange(155, 176), "hard", 17, ["normal", "power", "freeze"]),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 187, 88, 79, 115, random.randrange(160, 181), "hard", 18, ["normal", "double", "reckless"]),
            "Yeti Alpha": Enemy("Yeti Alpha", 213, 90, 81, 120, random.randrange(165, 186), "hard", 19, ["normal", "power", "reckless"]),
            
            "Fire Elemental": Enemy("Fire Elemental", 196, 77, 88, 100, random.randrange(170, 191), "hard", 15, ["normal", "power", "reckless"]),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 179, 82, 83, 105, random.randrange(175, 196), "hard", 16, ["normal", "double", "stunning"]),
            "Mirage Assassin": Enemy("Mirage Assassin", 170, 86, 80, 110, random.randrange(180, 201), "hard", 17, ["normal", "double", "poison"]),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 196, 89, 78, 115, random.randrange(185, 206), "hard", 18, ["normal", "power", "reckless"]),
            "Desert Colossus": Enemy("Desert Colossus", 230, 91, 76, 120, random.randrange(190, 211), "hard", 19, ["normal", "power", "stunning"]),

            "Nightmare Stalker": Enemy("Nightmare Stalker", 187, 80, 85, 110, random.randrange(195, 216), "hard", 15, ["normal", "double", "vampiric"]),
            "Void Weaver": Enemy("Void Weaver", 179, 84, 81, 115, random.randrange(200, 221), "hard", 16, ["normal", "draining", "stunning"]),
            "Shadow Dragon": Enemy("Shadow Dragon", 221, 87, 82, 120, random.randrange(205, 226), "hard", 17, ["normal", "power", "poison"]),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 170, 90, 77, 125, random.randrange(210, 231), "hard", 18, ["normal", "draining", "stunning"]),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 238, 91, 79, 130, random.randrange(215, 236), "hard", 19, ["normal", "power", "reckless"]),
            
            # Very Hard Enemies (Levels 20-24) - 4 attacks each
            "Necropolis Guardian": Enemy("Necropolis Guardian", 323, 106, 93, 300, random.randrange(240, 271), "very-hard", 20, ["normal", "power", "stunning", "draining"]),
            "Soul Reaver": Enemy("Soul Reaver", 298, 112, 88, 325, random.randrange(250, 281), "very-hard", 21, ["normal", "double", "vampiric", "draining"]),
            "Bone Colossus": Enemy("Bone Colossus", 357, 117, 90, 350, random.randrange(260, 291), "very-hard", 22, ["normal", "power", "stunning", "reckless"]),
            "Spectral Devourer": Enemy("Spectral Devourer", 315, 122, 84, 375, random.randrange(270, 301), "very-hard", 23, ["normal", "vampiric", "poison", "draining"]),
            "Lich King": Enemy("Lich King", 340, 125, 87, 400, random.randrange(280, 311), "very-hard", 24, ["normal", "draining", "poison", "freeze"]),
            
            "Timeless Sphinx": Enemy("Timeless Sphinx", 340, 104, 95, 300, random.randrange(290, 321), "very-hard", 20, ["normal", "stunning", "draining", "poison"]),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 323, 110, 90, 325, random.randrange(300, 331), "very-hard", 21, ["normal", "power", "poison", "draining"]),
            "Anubis Reborn": Enemy("Anubis Reborn", 340, 115, 92, 350, random.randrange(310, 341), "very-hard", 22, ["normal", "vampiric", "stunning", "double"]),
            "Mummy Emperor": Enemy("Mummy Emperor", 357, 120, 86, 375, random.randrange(320, 351), "very-hard", 23, ["normal", "draining", "poison", "stunning"]),
            "Living Obelisk": Enemy("Living Obelisk", 383, 124, 89, 400, random.randrange(330, 361), "very-hard", 24, ["normal", "power", "stunning", "reckless"]),
            
            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 340, 114, 91, 350, random.randrange(310, 341), "very-hard", 22, ["normal", "reckless", "poison", "draining"]),
            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 357, 119, 85, 375, random.randrange(320, 351), "very-hard", 23, ["normal", "power", "poison", "stunning"]),
            "Void Titan": Enemy("Void Titan", 383, 123, 88, 400, random.randrange(330, 361), "very-hard", 24, ["normal", "reckless", "stunning", "draining"]),
            "Chaos Incarnate": Enemy("Chaos Incarnate", 366, 121, 83, 425, random.randrange(340, 371), "very-hard", 23, ["normal", "double", "poison", "vampiric"]),
            "Eternity Warden": Enemy("Eternity Warden", 400, 125, 86, 450, random.randrange(350, 381), "very-hard", 24, ["normal", "power", "stunning", "freeze"]),

            "Ancient Wyvern": Enemy("Ancient Wyvern", 349, 111, 89, 300, random.randrange(390, 421), "very-hard", 21, ["normal", "double", "poison", "reckless"]),
            "Elemental Drake": Enemy("Elemental Drake", 340, 108, 92, 325, random.randrange(400, 431), "very-hard", 20, ["normal", "power", "poison", "freeze"]),
            "Dragonlord": Enemy("Dragonlord", 366, 116, 91, 350, random.randrange(410, 441), "very-hard", 22, ["normal", "power", "reckless", "stunning"]),
            "Chromatic Dragon": Enemy("Chromatic Dragon", 374, 121, 85, 375, random.randrange(420, 451), "very-hard", 23, ["normal", "double", "poison", "freeze"]),
            "Elder Dragon": Enemy("Elder Dragon", 391, 124, 88, 400, random.randrange(440, 471), "very-hard", 24, ["normal", "power", "stunning", "draining"]),
            
            # Extreme Enemies (Levels 25+) - 5 attacks each
            "Magma Colossus": Enemy("Magma Colossus", 589, 115, 118, 500, random.randrange(480, 531), "extreme", 21, ["normal", "power", "reckless", "stunning", "draining"]),
            "Phoenix Overlord": Enemy("Phoenix Overlord", 557, 122, 115, 520, random.randrange(500, 551), "extreme", 20, ["normal", "double", "stunning", "vampiric", "reckless"]),
            "Volcanic Titan": Enemy("Volcanic Titan", 655, 117, 122, 540, random.randrange(520, 571), "extreme", 24, ["normal", "power", "reckless", "stunning", "draining"]),
            "Inferno Wyrm": Enemy("Inferno Wyrm", 622, 121, 116, 560, random.randrange(540, 591), "extreme", 22, ["normal", "double", "poison", "reckless", "stunning"]),
            "Cinder Archfiend": Enemy("Cinder Archfiend", 576, 126, 111, 580, random.randrange(560, 611), "extreme", 23, ["normal", "power", "poison", "vampiric", "draining"]),
            
            # Boss Monsters - 6 attacks each
            "Seraphim Guardian": Enemy("Seraphim Guardian", 916, 131, 137, 1000, random.randrange(950, 1051), "boss", 25, ["normal", "power", "stunning", "draining", "reckless", "freeze"]),
            "Celestial Arbiter": Enemy("Celestial Arbiter", 851, 141, 128, 1100, random.randrange(1050, 1151), "boss", 25, ["normal", "double", "draining", "stunning", "poison", "vampiric"]),
            "Astral Demiurge": Enemy("Astral Demiurge", 982, 134, 136, 1200, random.randrange(1150, 1251), "boss", 25, ["normal", "power", "poison", "freeze", "stunning", "vampiric"]),
            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1047, 145, 126, 1300, random.randrange(1250, 1351), "boss", 25, ["normal", "reckless", "draining", "double", "poison", "stunning"]),
            "Divine Architect": Enemy("Divine Architect", 1113, 138, 132, 1500, random.randrange(1450, 1551), "boss", 25, ["normal", "power", "stunning", "freeze", "draining", "reckless"]),
    }
    
ENEMY_ATTACK_TYPES = {
    "normal": {"name": "Normal Attack", "damage_modifier": 1, "effect": None},
    "power": {"name": "Power Attack", "damage_modifier": 1.5, "effect": None},
    "double": {"name": "Double Strike", "damage_modifier": 0.85, "effect": None, "extra_attacks": 1},
    "triple": {"name": "Triple Strike", "damage_modifier": 0.85, "effect": "self_damage", "extra_attacks": 2},
    "vampiric": {"name": "Vampiric Strike", "damage_modifier": 0.9, "effect": "lifesteal"},
    "reckless": {"name": "Reckless Assault", "damage_modifier": 2, "effect": "self_damage"},
    "draining": {"name": "Draining Touch", "damage_modifier": 0.9, "effect": "stamina_drain"},
    "stunning": {"name": "Stunning Blow", "damage_modifier": 0.7, "effect": "stun"},
    "poison": {"name": "Poison Strike", "damage_modifier": 0.9, "effect": "poison"},
    "freeze": {"name": "Frozen Strike", "damage_modifier": 0.9, "effect": "freeze"},
    "burn": {"name": "Burning Strike", "damage_modifier": 0.9, "effect": "burn"},
    "damage_reflect": {"name": "Reflective Shield", "damage_modifier": 0.5, "effect": "damage_reflect"}
}