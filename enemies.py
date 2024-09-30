from player import Character
import random

class Enemy(Character):
    def __init__(self, name, hp, attack, defence, exp, gold, tier, level=0, attack_types=None):
        super().__init__(name, hp, attack, defence)
        self.exp = exp
        self.gold = gold
        self.tier = tier
        self.level = level
        self.attack_types = attack_types if attack_types is not None else ["normal"]
        
    def choose_attack(self):
        chosen_attack = random.choice(self.attack_types)
        return chosen_attack
        
def initialise_enemies():
    return {
            # Easy Enemies (Levels 1-4)
            "Rat": Enemy("Rat", 21, 21, 5, 10, random.randrange(3, 10), "low", 1, ["normal", "quick", "draining"]),
            "Boar": Enemy("Boar", 30, 24, 7, 15, random.randrange(5, 15), "low", 2, ["normal", "power", "reckless"]),
            "Plains Hawk": Enemy("Plains Hawk", 19, 26, 4, 20, random.randrange(8, 18), "low", 1, ["normal", "quick", "stunning"]),
            "Strider": Enemy("Strider", 34, 25, 8, 25, random.randrange(10, 20), "low", 2, ["normal", "quick", "power"]),
            "Bull": Enemy("Bull", 43, 27, 10, 30, random.randrange(12, 24), "low", 3, ["normal", "power", "reckless"]),
            
            "Bat": Enemy("Bat", 24, 23, 6, 10, random.randrange(3, 10), "low", 1, ["normal", "quick", "vampiric"]),
            "Goblin": Enemy("Goblin", 27, 25, 8, 15, random.randrange(5, 15), "low", 2, ["normal", "quick", "draining"]),
            "Spider": Enemy("Spider", 22, 26, 5, 20, random.randrange(8, 18), "low", 1, ["normal", "quick", "vampiric"]),
            "Slime": Enemy("Slime", 38, 22, 9, 25, random.randrange(10, 20), "low", 2, ["normal", "draining", "stunning"]),
            "Frog": Enemy("Frog", 36, 26, 8, 30, random.randrange(12, 24), "low", 3, ["normal", "quick", "stunning"]),
            
            "Tree Sprite": Enemy("Tree Sprite", 20, 24, 6, 10, random.randrange(3, 10), "low", 1, ["normal", "quick", "draining"]),
            "Snake": Enemy("Snake", 24, 27, 5, 15, random.randrange(5, 15), "low", 1, ["normal", "quick", "vampiric"]),
            "Forest Hawk": Enemy("Forest Hawk", 29, 25, 7, 20, random.randrange(8, 18), "low", 2, ["normal", "quick", "stunning"]),
            "Locust": Enemy("Locust", 26, 26, 6, 25, random.randrange(10, 20), "low", 2, ["normal", "quick", "draining"]),
            "Leprechaun": Enemy("Leprechaun", 41, 23, 9, 30, random.randrange(12, 24), "low", 3, ["normal", "quick", "stunning"]),
            
            "Wood Spirit": Enemy("Wood Spirit", 26, 24, 7, 10, random.randrange(3, 10), "low", 1, ["normal", "draining", "stunning"]),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 32, 26, 9, 15, random.randrange(5, 15), "low", 2, ["normal", "quick", "vampiric"]),
            "Deep Bat": Enemy("Deep Bat", 27, 27, 7, 20, random.randrange(8, 18), "low", 2, ["normal", "quick", "vampiric"]),
            "Giant Firefly": Enemy("Giant Firefly", 34, 24, 8, 25, random.randrange(10, 20), "low", 2, ["normal", "quick", "stunning"]),
            "Treant": Enemy("Treant", 51, 25, 12, 30, random.randrange(12, 24), "low", 3, ["normal", "power", "stunning"]),
            
            # Medium Enemies (Levels 5-9)
            "Alligator": Enemy("Alligator", 77, 43, 30, 35, random.randrange(30, 41), "medium", 5, ["normal", "power", "reckless"]),
            "Poison Frog": Enemy("Poison Frog", 60, 45, 28, 40, random.randrange(35, 46), "medium", 4, ["normal", "quick", "vampiric"]),
            "Swamp Troll": Enemy("Swamp Troll", 89, 44, 32, 45, random.randrange(40, 51), "medium", 6, ["normal", "power", "reckless"]),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 64, 47, 26, 35, random.randrange(30, 41), "medium", 4, ["normal", "quick", "draining"]),
            "Bog Witch": Enemy("Bog Witch", 72, 43, 29, 50, random.randrange(45, 56), "medium", 5, ["normal", "draining", "stunning"]),
            
            "Stone Golem": Enemy("Stone Golem", 102, 42, 34, 55, random.randrange(50, 61), "medium", 6, ["normal", "power", "stunning"]),
            "Cultist": Enemy("Cultist", 68, 46, 28, 40, random.randrange(35, 46), "medium", 4, ["normal", "draining", "vampiric"]),
            "Mummy": Enemy("Mummy", 81, 44, 31, 45, random.randrange(40, 51), "medium", 5, ["normal", "draining", "stunning"]),
            "Animated Statue": Enemy("Animated Statue", 85, 43, 32, 50, random.randrange(45, 56), "medium", 5, ["normal", "power", "stunning"]),
            "Temple Guardian": Enemy("Temple Guardian", 94, 43, 33, 55, random.randrange(50, 61), "medium", 6, ["normal", "power", "stunning"]),
            
            "Mountain Lion": Enemy("Mountain Lion", 72, 48, 29, 40, random.randrange(35, 46), "medium", 4, ["normal", "quick", "reckless"]),
            "Rock Elemental": Enemy("Rock Elemental", 98, 41, 35, 50, random.randrange(45, 56), "medium", 6, ["normal", "power", "stunning"]),
            "Harpy": Enemy("Harpy", 68, 48, 27, 45, random.randrange(40, 51), "medium", 4, ["normal", "quick", "stunning"]),
            "Yeti": Enemy("Yeti", 89, 45, 33, 50, random.randrange(45, 56), "medium", 6, ["normal", "power", "reckless"]),
            "Orc": Enemy("Orc", 81, 46, 30, 40, random.randrange(35, 46), "medium", 5, ["normal", "power", "reckless"]),
            
            "Sand Wurm": Enemy("Sand Wurm", 94, 44, 34, 45, random.randrange(40, 51), "medium", 6, ["normal", "power", "stunning"]),
            "Dried Mummy": Enemy("Dried Mummy", 85, 43, 31, 40, random.randrange(35, 46), "medium", 5, ["normal", "draining", "stunning"]),
            "Dust Devil": Enemy("Dust Devil", 64, 49, 28, 45, random.randrange(40, 51), "medium", 4, ["normal", "quick", "stunning"]),
            "Desert Bandit": Enemy("Desert Bandit", 77, 47, 30, 50, random.randrange(45, 56), "medium", 5, ["normal", "quick", "draining"]),
            "Leopard": Enemy("Leopard", 68, 40, 27, 35, random.randrange(30, 41), "medium", 3, ["normal", "quick", "reckless"]),
            
            # Medium-Hard Enemies (Levels 10-14)
            "Canyon Cougar": Enemy("Canyon Cougar", 111, 60, 50, 70, random.randrange(65, 81), "medium-hard", 10, ["normal", "quick", "reckless"]),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 136, 57, 52, 75, random.randrange(70, 86), "medium-hard", 12, ["normal", "draining", "stunning"]),
            "Dustier Devil": Enemy("Dustier Devil", 123, 61, 49, 80, random.randrange(75, 91), "medium-hard", 11, ["normal", "quick", "stunning"]),
            "Petrified Warrior": Enemy("Petrified Warrior", 119, 60, 48, 85, random.randrange(80, 96), "medium-hard", 10, ["normal", "power", "stunning"]),
            "Thunderbird": Enemy("Thunderbird", 132, 63, 49, 90, random.randrange(85, 101), "medium-hard", 11, ["normal", "quick", "stunning"]),
            
            # Hard Enemies (Levels 15-19)
            "Venomous Hydra": Enemy("Venomous Hydra", 170, 78, 87, 120, random.randrange(95, 116), "hard", 15, ["normal", "power", "vampiric"]),
            "Plague Bearer": Enemy("Plague Bearer", 162, 81, 84, 125, random.randrange(100, 121), "hard", 16, ["normal", "draining", "vampiric"]),
            "Mire Leviathan": Enemy("Mire Leviathan", 204, 83, 86, 130, random.randrange(105, 126), "hard", 17, ["normal", "power", "stunning"]),
            "Toxic Shambler": Enemy("Toxic Shambler", 153, 87, 82, 135, random.randrange(110, 131), "hard", 18, ["normal", "draining", "vampiric"]),
            "Swamp Hag": Enemy("Swamp Hag", 166, 89, 80, 140, random.randrange(115, 136), "hard", 19, ["normal", "draining", "stunning"]),
            
            "Ancient Golem": Enemy("Ancient Golem", 230, 75, 90, 120, random.randrange(120, 141), "hard", 15, ["normal", "power", "stunning"]),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 187, 79, 86, 125, random.randrange(125, 146), "hard", 16, ["normal", "draining", "stunning"]),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 170, 84, 83, 130, random.randrange(130, 151), "hard", 17, ["normal", "quick", "stunning"]),
            "Ruin Wraith": Enemy("Ruin Wraith", 179, 86, 81, 135, random.randrange(135, 156), "hard", 18, ["normal", "draining", "vampiric"]),
            "Forgotten Titan": Enemy("Forgotten Titan", 221, 88, 85, 140, random.randrange(140, 161), "hard", 19, ["normal", "power", "reckless"]),
            
            "Frost Giant": Enemy("Frost Giant", 221, 76, 89, 100, random.randrange(145, 166), "hard", 15, ["normal", "power", "stunning"]),
            "Storm Harpy": Enemy("Storm Harpy", 170, 83, 82, 105, random.randrange(150, 171), "hard", 16, ["normal", "quick", "stunning"]),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 204, 85, 84, 110, random.randrange(155, 176), "hard", 17, ["normal", "power", "stunning"]),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 187, 88, 79, 115, random.randrange(160, 181), "hard", 18, ["normal", "quick", "reckless"]),
            "Yeti Alpha": Enemy("Yeti Alpha", 213, 90, 81, 120, random.randrange(165, 186), "hard", 19, ["normal", "power", "reckless"]),
            
            "Fire Elemental": Enemy("Fire Elemental", 196, 77, 88, 100, random.randrange(170, 191), "hard", 15, ["normal", "power", "reckless"]),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 179, 82, 83, 105, random.randrange(175, 196), "hard", 16, ["normal", "quick", "stunning"]),
            "Mirage Assassin": Enemy("Mirage Assassin", 170, 86, 80, 110, random.randrange(180, 201), "hard", 17, ["normal", "quick", "vampiric"]),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 196, 89, 78, 115, random.randrange(185, 206), "hard", 18, ["normal", "power", "reckless"]),
            "Desert Colossus": Enemy("Desert Colossus", 230, 91, 76, 120, random.randrange(190, 211), "hard", 19, ["normal", "power", "stunning"]),

            "Nightmare Stalker": Enemy("Nightmare Stalker", 187, 80, 85, 110, random.randrange(195, 216), "hard", 15, ["normal", "quick", "vampiric"]),
            "Void Weaver": Enemy("Void Weaver", 179, 84, 81, 115, random.randrange(200, 221), "hard", 16, ["normal", "draining", "stunning"]),
            "Shadow Dragon": Enemy("Shadow Dragon", 221, 87, 82, 120, random.randrange(205, 226), "hard", 17, ["normal", "power", "vampiric"]),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 170, 90, 77, 125, random.randrange(210, 231), "hard", 18, ["normal", "draining", "stunning"]),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 238, 91, 79, 130, random.randrange(215, 236), "hard", 19, ["normal", "power", "reckless"]),
            
            "Necropolis Guardian": Enemy("Necropolis Guardian", 323, 106, 93, 300, random.randrange(240, 271), "very-hard", 20, ["normal", "power", "stunning", "vampiric"]),
            "Soul Reaver": Enemy("Soul Reaver", 298, 112, 88, 325, random.randrange(250, 281), "very-hard", 21, ["normal", "quick", "vampiric", "draining"]),
            "Bone Colossus": Enemy("Bone Colossus", 357, 117, 90, 350, random.randrange(260, 291), "very-hard", 22, ["normal", "power", "stunning", "reckless"]),
            "Spectral Devourer": Enemy("Spectral Devourer", 315, 122, 84, 375, random.randrange(270, 301), "very-hard", 23, ["normal", "vampiric", "draining", "stunning"]),
            "Lich King": Enemy("Lich King", 340, 125, 87, 400, random.randrange(280, 311), "very-hard", 24, ["normal", "draining", "stunning", "vampiric"]),
            
            "Timeless Sphinx": Enemy("Timeless Sphinx", 340, 104, 95, 300, random.randrange(290, 321), "very-hard", 20, ["normal", "stunning", "draining", "quick"]),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 323, 110, 90, 325, random.randrange(300, 331), "very-hard", 21, ["normal", "power", "stunning", "draining"]),
            "Anubis Reborn": Enemy("Anubis Reborn", 340, 115, 92, 350, random.randrange(310, 341), "very-hard", 22, ["normal", "vampiric", "stunning", "quick"]),
            "Mummy Emperor": Enemy("Mummy Emperor", 357, 120, 86, 375, random.randrange(320, 351), "very-hard", 23, ["normal", "draining", "stunning", "power"]),
            "Living Obelisk": Enemy("Living Obelisk", 383, 124, 89, 400, random.randrange(330, 361), "very-hard", 24, ["normal", "power", "stunning", "reckless"]),
            
            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 340, 114, 91, 350, random.randrange(310, 341), "very-hard", 22, ["normal", "reckless", "stunning", "vampiric"]),
            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 357, 119, 85, 375, random.randrange(320, 351), "very-hard", 23, ["normal", "power", "draining", "stunning"]),
            "Void Titan": Enemy("Void Titan", 383, 123, 88, 400, random.randrange(330, 361), "very-hard", 24, ["normal", "reckless", "stunning", "vampiric"]),
            "Chaos Incarnate": Enemy("Chaos Incarnate", 366, 121, 83, 425, random.randrange(340, 371), "very-hard", 23, ["normal", "quick", "stunning", "vampiric"]),
            "Eternity Warden": Enemy("Eternity Warden", 400, 125, 86, 450, random.randrange(350, 381), "very-hard", 24, ["normal", "power", "stunning", "draining"]),

            "Ancient Wyvern": Enemy("Ancient Wyvern", 349, 111, 89, 300, random.randrange(390, 421), "very-hard", 21, ["normal", "quick", "reckless", "stunning"]),
            "Elemental Drake": Enemy("Elemental Drake", 340, 108, 92, 325, random.randrange(400, 431), "very-hard", 20, ["normal", "power", "draining", "stunning"]),
            "Dragonlord": Enemy("Dragonlord", 366, 116, 91, 350, random.randrange(410, 441), "very-hard", 22, ["normal", "power", "reckless", "stunning"]),
            "Chromatic Dragon": Enemy("Chromatic Dragon", 374, 121, 85, 375, random.randrange(420, 451), "very-hard", 23, ["normal", "quick", "vampiric", "stunning"]),
            "Elder Dragon": Enemy("Elder Dragon", 391, 124, 88, 400, random.randrange(440, 471), "very-hard", 24, ["normal", "power", "reckless", "stunning"]),
            
            # Extreme Enemies (Levels 25+)
            "Magma Colossus": Enemy("Magma Colossus", 589, 115, 118, 500, random.randrange(480, 531), "extreme", 21, ["normal", "power", "reckless", "stunning"]),
            "Phoenix Overlord": Enemy("Phoenix Overlord", 557, 122, 115, 520, random.randrange(500, 551), "extreme", 20, ["normal", "quick", "vampiric", "stunning"]),
            "Volcanic Titan": Enemy("Volcanic Titan", 655, 117, 122, 540, random.randrange(520, 571), "extreme", 24, ["normal", "power", "reckless", "stunning"]),
            "Inferno Wyrm": Enemy("Inferno Wyrm", 622, 121, 116, 560, random.randrange(540, 591), "extreme", 22, ["normal", "quick", "vampiric", "stunning"]),
            "Cinder Archfiend": Enemy("Cinder Archfiend", 576, 126, 111, 580, random.randrange(560, 611), "extreme", 23, ["normal", "power", "draining", "stunning"]),
            
            # Boss Monsters
            "Seraphim Guardian": Enemy("Seraphim Guardian", 916, 131, 137, 1000, random.randrange(950, 1051), "boss", 25, ["normal", "power", "stunning", "vampiric"]),
            "Celestial Arbiter": Enemy("Celestial Arbiter", 851, 141, 128, 1100, random.randrange(1050, 1151), "boss", 25, ["normal", "quick", "draining", "stunning"]),
            "Astral Demiurge": Enemy("Astral Demiurge", 982, 134, 136, 1200, random.randrange(1150, 1251), "boss", 25, ["normal", "power", "vampiric", "stunning"]),
            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1047, 145, 126, 1300, random.randrange(1250, 1351), "boss", 25, ["normal", "reckless", "draining", "stunning"]),
            "Divine Architect": Enemy("Divine Architect", 1113, 138, 132, 1500, random.randrange(1450, 1551), "boss", 25, ["normal", "power", "vampiric", "stunning"]),
    }
    
ENEMY_ATTACK_TYPES = {
    "normal": {"name": "Normal Attack", "damage_modifier": 1, "effect": None},
    "power": {"name": "Power Attack", "damage_modifier": 1.5, "effect": None},
    "quick": {"name": "Quick Attack", "damage_modifier": 0.85, "effect": "double_attack"},
    "vampiric": {"name": "Vampiric Strike", "damage_modifier": 0.8, "effect": "lifesteal"},
    "reckless": {"name": "Reckless Assault", "damage_modifier": 2, "effect": "self_damage"},
    "draining": {"name": "Draining Touch", "damage_modifier": 0.9, "effect": "stamina_drain"},
    "stunning": {"name": "Stunning Blow", "damage_modifier": 0.7, "effect": "stun"},
}