from player import Character
import random

class Enemy(Character):
    def __init__(self, name, hp, attack, defence, exp, gold, tier, level=0):
        super().__init__(name, hp, attack, defence)
        self.exp = exp
        self.gold = gold
        self.tier = tier
        self.level = level
        
def initialise_enemies():
    return {
            # Easy Enemies (Levels 1-4)
            "Rat": Enemy("Rat", 30, 12, 2, 10, random.randrange(3, 10), "low", 1),
            "Boar": Enemy("Boar", 40, 14, 5, 15, random.randrange(5, 15), "low", 2),
            "Plains Hawk": Enemy("Plains Hawk", 28, 15, 3, 20, random.randrange(8, 18), "low", 1),
            "Strider": Enemy("Strider", 45, 13, 4, 25, random.randrange(10, 20), "low", 2),
            "Bull": Enemy("Bull", 55, 16, 6, 30, random.randrange(12, 24), "low", 3),
            
            "Bat": Enemy("Bat", 32, 14, 3, 10, random.randrange(3, 10), "low", 1),
            "Goblin": Enemy("Goblin", 38, 15, 4, 15, random.randrange(5, 15), "low", 2),
            "Spider": Enemy("Spider", 30, 16, 3, 20, random.randrange(8, 18), "low", 1),
            "Slime": Enemy("Slime", 52, 12, 7, 25, random.randrange(10, 20), "low", 2),
            "Frog": Enemy("Frog", 48, 15, 4, 30, random.randrange(12, 24), "low", 3),
            
            "Tree Sprite": Enemy("Tree Sprite", 28, 13, 5, 10, random.randrange(3, 10), "low", 1),
            "Snake": Enemy("Snake", 32, 17, 2, 15, random.randrange(5, 15), "low", 1),
            "Forest Hawk": Enemy("Forest Hawk", 38, 14, 3, 20, random.randrange(8, 18), "low", 2),
            "Locust": Enemy("Locust", 35, 20, 3, 25, random.randrange(10, 20), "low", 2),
            "Leprechaun": Enemy("Leprechaun", 58, 15, 3, 30, random.randrange(12, 24), "low", 3),
            
            "Wood Spirit": Enemy("Wood Spirit", 32, 13, 4, 10, random.randrange(3, 10), "low", 1),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 40, 14, 5, 15, random.randrange(5, 15), "low", 2),
            "Deep Bat": Enemy("Deep Bat", 35, 16, 2, 20, random.randrange(8, 18), "low", 2),
            "Giant Firefly": Enemy("Giant Firefly", 45, 13, 5, 25, random.randrange(10, 20), "low", 2),
            "Treant": Enemy("Treant", 75, 15, 6, 30, random.randrange(12, 24), "low", 3),
            
            # Medium Enemies (Levels 5-9)
            "Alligator": Enemy("Alligator", 85, 24, 15, 35, random.randrange(30, 41), "medium", 5),
            "Poison Frog": Enemy("Poison Frog", 65, 28, 8, 40, random.randrange(35, 46), "medium", 4),
            "Swamp Troll": Enemy("Swamp Troll", 100, 20, 18, 45, random.randrange(40, 51), "medium", 6),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 70, 23, 10, 35, random.randrange(30, 41), "medium", 4),
            "Bog Witch": Enemy("Bog Witch", 80, 26, 12, 50, random.randrange(45, 56), "medium", 5),
            
            "Stone Golem": Enemy("Stone Golem", 115, 22, 22, 55, random.randrange(50, 61), "medium", 6),
            "Cultist": Enemy("Cultist", 75, 25, 13, 40, random.randrange(35, 46), "medium", 4),
            "Mummy": Enemy("Mummy", 85, 24, 15, 45, random.randrange(40, 51), "medium", 5),
            "Animated Statue": Enemy("Animated Statue", 95, 23, 18, 50, random.randrange(45, 56), "medium", 5),
            "Temple Guardian": Enemy("Temple Guardian", 105, 26, 17, 55, random.randrange(50, 61), "medium", 6),
            
            "Mountain Lion": Enemy("Mountain Lion", 80, 27, 12, 40, random.randrange(35, 46), "medium", 4),
            "Rock Elemental": Enemy("Rock Elemental", 110, 21, 22, 50, random.randrange(45, 56), "medium", 6),
            "Harpy": Enemy("Harpy", 75, 29, 11, 45, random.randrange(40, 51), "medium", 4),
            "Yeti": Enemy("Yeti", 100, 25, 15, 50, random.randrange(45, 56), "medium", 6),
            "Orc": Enemy("Orc", 90, 24, 13, 40, random.randrange(35, 46), "medium", 5),
            
            "Sand Wurm": Enemy("Sand Wurm", 105, 26, 15, 45, random.randrange(40, 51), "medium", 6),
            "Dried Mummy": Enemy("Dried Mummy", 95, 23, 17, 40, random.randrange(35, 46), "medium", 5),
            "Dust Devil": Enemy("Dust Devil", 70, 30, 12, 45, random.randrange(40, 51), "medium", 4),
            "Desert Bandit": Enemy("Desert Bandit", 85, 26, 13, 50, random.randrange(45, 56), "medium", 5),
            "Leopard": Enemy("Leopard", 75, 28, 10, 35, random.randrange(30, 41), "medium", 3),
            
            # Medium-Hard Enemies (Levels 10-12)
            "Canyon Cougar": Enemy("Canyon Cougar", 110, 38, 16, 70, random.randrange(65, 81), "medium-hard", 7),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 145, 30, 28, 75, random.randrange(70, 86), "medium-hard", 9),
            "Dust Devil": Enemy("Dust Devil", 130, 35, 23, 80, random.randrange(75, 91), "medium-hard", 8),
            "Petrified Warrior": Enemy("Petrified Warrior", 125, 33, 25, 85, random.randrange(80, 96), "medium-hard", 7),
            "Thunderbird": Enemy("Thunderbird", 140, 36, 21, 90, random.randrange(85, 101), "medium-hard", 8),
            
            # Hard Enemies (Levels 13-17)
            "Venomous Hydra": Enemy("Venomous Hydra", 190, 48, 30, 120, random.randrange(95, 116), "hard", 10),
            "Plague Bearer": Enemy("Plague Bearer", 175, 52, 27, 125, random.randrange(100, 121), "hard", 11),
            "Mire Leviathan": Enemy("Mire Leviathan", 230, 44, 34, 130, random.randrange(105, 126), "hard", 12),
            "Toxic Shambler": Enemy("Toxic Shambler", 170, 56, 23, 135, random.randrange(110, 131), "hard", 13),
            "Swamp Hag": Enemy("Swamp Hag", 185, 50, 28, 140, random.randrange(115, 136), "hard", 14),
            
            "Ancient Golem": Enemy("Ancient Golem", 265, 42, 42, 120, random.randrange(120, 141), "hard", 10),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 205, 52, 31, 125, random.randrange(125, 146), "hard", 11),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 180, 58, 28, 130, random.randrange(130, 151), "hard", 12),
            "Ruin Wraith": Enemy("Ruin Wraith", 195, 54, 31, 135, random.randrange(135, 156), "hard", 13),
            "Forgotten Titan": Enemy("Forgotten Titan", 250, 48, 39, 140, random.randrange(140, 161), "hard", 14),
            
            "Frost Giant": Enemy("Frost Giant", 250, 52, 36, 100, random.randrange(145, 166), "hard", 10),
            "Storm Harpy": Enemy("Storm Harpy", 185, 62, 25, 105, random.randrange(150, 171), "hard", 11),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 230, 48, 43, 110, random.randrange(155, 176), "hard", 12),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 210, 58, 32, 115, random.randrange(160, 181), "hard", 13),
            "Yeti Alpha": Enemy("Yeti Alpha", 240, 54, 40, 120, random.randrange(165, 186), "hard", 14),
            
            "Fire Elemental": Enemy("Fire Elemental", 215, 64, 30, 100, random.randrange(170, 191), "hard", 10),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 200, 60, 34, 105, random.randrange(175, 196), "hard", 11),
            "Mirage Assassin": Enemy("Mirage Assassin", 190, 68, 27, 110, random.randrange(180, 201), "hard", 12),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 225, 56, 37, 115, random.randrange(185, 206), "hard", 13),
            "Desert Colossus": Enemy("Desert Colossus", 265, 54, 51, 120, random.randrange(190, 211), "hard", 14),
            
            "Nightmare Stalker": Enemy("Nightmare Stalker", 210, 64, 34, 110, random.randrange(195, 216), "hard", 10),
            "Void Weaver": Enemy("Void Weaver", 195, 70, 30, 115, random.randrange(200, 221), "hard", 11),
            "Shadow Dragon": Enemy("Shadow Dragon", 255, 62, 41, 120, random.randrange(205, 226), "hard", 12),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 185, 74, 34, 125, random.randrange(210, 231), "hard", 13),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 280, 64, 48, 130, random.randrange(215, 236), "hard", 14),
            
            # Very Hard Enemies (Levels 18-22)
            "Necropolis Guardian": Enemy("Necropolis Guardian", 360, 82, 58, 300, random.randrange(240, 271), "very-hard", 15),
            "Soul Reaver": Enemy("Soul Reaver", 330, 92, 51, 325, random.randrange(250, 281), "very-hard", 16),
            "Bone Colossus": Enemy("Bone Colossus", 400, 78, 65, 350, random.randrange(260, 291), "very-hard", 17),
            "Spectral Devourer": Enemy("Spectral Devourer", 350, 88, 55, 375, random.randrange(270, 301), "very-hard", 18),
            "Lich King": Enemy("Lich King", 380, 84, 62, 400, random.randrange(280, 311), "very-hard", 19),
            
            "Timeless Sphinx": Enemy("Timeless Sphinx", 385, 84, 64, 300, random.randrange(290, 321), "very-hard", 15),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 365, 88, 58, 325, random.randrange(300, 331), "very-hard", 16),
            "Anubis Reborn": Enemy("Anubis Reborn", 380, 86, 59, 350, random.randrange(310, 341), "very-hard", 17),
            "Mummy Emperor": Enemy("Mummy Emperor", 400, 82, 65, 375, random.randrange(320, 351), "very-hard", 18),
            "Living Obelisk": Enemy("Living Obelisk", 435, 78, 69, 400, random.randrange(330, 361), "very-hard", 19),
            
            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 390, 92, 65, 300, random.randrange(340, 371), "very-hard", 15),
            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 420, 86, 69, 325, random.randrange(350, 381), "very-hard", 16),
            "Void Titan": Enemy("Void Titan", 450, 82, 72, 350, random.randrange(360, 391), "very-hard", 17),
            "Chaos Incarnate": Enemy("Chaos Incarnate", 410, 88, 69, 375, random.randrange(370, 401), "very-hard", 18),
            "Eternity Warden": Enemy("Eternity Warden", 435, 86, 71, 400, random.randrange(380, 411), "very-hard", 19),
            
            #Dragon's Lair
            "Ancient Wyvern": Enemy("Ancient Wyvern", 392, 88, 74, 300, random.randrange(390, 421), "very-hard", 16),
            "Elemental Drake": Enemy("Elemental Drake", 378, 91, 70, 325, random.randrange(400, 431), "very-hard", 15),
            "Dragonlord": Enemy("Dragonlord", 406, 90, 75, 350, random.randrange(410, 441), "very-hard", 17),
            "Chromatic Dragon": Enemy("Chromatic Dragon", 420, 88, 76, 375, random.randrange(420, 451), "very-hard", 18),
            "Elder Dragon": Enemy("Elder Dragon", 441, 91, 77, 400, random.randrange(440, 471), "very-hard", 19),
            
            # Extreme Enemies
            "Magma Colossus": Enemy("Magma Colossus", 630, 133, 84, 500, random.randrange(480, 531), "extreme", 21),
            "Phoenix Overlord": Enemy("Phoenix Overlord", 595, 154, 84, 520, random.randrange(500, 551), "extreme", 20),
            "Volcanic Titan": Enemy("Volcanic Titan", 700, 119, 91, 540, random.randrange(520, 571), "extreme", 24),
            "Inferno Wyrm": Enemy("Inferno Wyrm", 665, 140, 105, 560, random.randrange(540, 591), "extreme", 22),
            "Cinder Archfiend": Enemy("Cinder Archfiend", 616, 147, 102, 580, random.randrange(560, 611), "extreme", 23),
            
            # Boss Monsters
            "Seraphim Guardian": Enemy("Seraphim Guardian", 980, 158, 140, 1000, random.randrange(950, 1051), "boss", 25),
            "Celestial Arbiter": Enemy("Celestial Arbiter", 910, 154, 133, 1100, random.randrange(1050, 1151), "boss", 25),
            "Astral Demiurge": Enemy("Astral Demiurge", 1050, 151, 137, 1200, random.randrange(1150, 1251), "boss", 25),
            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1120, 172, 119, 1300, random.randrange(1250, 1351), "boss", 25),
            "Divine Architect": Enemy("Divine Architect", 1190, 175, 144, 1500, random.randrange(1450, 1551), "boss", 25),
    }