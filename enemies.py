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
            # Easy Enemies
            "Rat": Enemy("Rat", 28, 11, 1, 10, random.randrange(3, 10), "low", 1),
            "Boar": Enemy("Boar", 35, 11, 4, 15, random.randrange(5, 15), "low", 2),
            "Plains Hawk": Enemy("Plains Hawk", 25, 13, 3, 20, random.randrange(8, 18), "low", 1),
            "Strider": Enemy("Strider", 42, 10, 3, 25, random.randrange(10, 20), "low", 2),
            "Bull": Enemy("Bull", 49, 11, 4, 30, random.randrange(12, 24), "low", 3),
            
            "Bat": Enemy("Bat", 28, 11, 3, 10, random.randrange(3, 10), "low", 1),
            "Goblin": Enemy("Goblin", 35, 13, 4, 15, random.randrange(5, 15), "low", 2),
            "Spider": Enemy("Spider", 25, 13, 3, 20, random.randrange(8, 18), "low", 1),
            "Slime": Enemy("Slime", 49, 10, 6, 25, random.randrange(10, 20), "low", 2),
            "Frog": Enemy("Frog", 42, 12, 3, 30, random.randrange(12, 24), "low", 3),
            
            "Tree Sprite": Enemy("Tree Sprite", 25, 11, 4, 10, random.randrange(3, 10), "low", 1),
            "Snake": Enemy("Snake", 28, 14, 2, 15, random.randrange(5, 15), "low", 1),
            "Forest Hawk": Enemy("Forest Hawk", 35, 12, 3, 20, random.randrange(8, 18), "low", 2),
            "Locust": Enemy("Locust", 32, 18, 3, 25, random.randrange(10, 20), "low", 2),
            "Leprechaun": Enemy("Leprechaun", 53, 13, 2, 30, random.randrange(12, 24), "low", 3),
            
            "Wood Spirit": Enemy("Wood Spirit", 28, 11, 3, 10, random.randrange(3, 10), "low", 1),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 35, 11, 4, 15, random.randrange(5, 15), "low", 2),
            "Deep Bat": Enemy("Deep Bat", 32, 13, 2, 20, random.randrange(8, 18), "low", 2),
            "Giant Firefly": Enemy("Giant Firefly", 42, 11, 4, 25, random.randrange(10, 20), "low", 2),
            "Treant": Enemy("Treant", 70, 13, 4, 30, random.randrange(12, 24), "low", 3),
            
            # Medium Enemies
            "Alligator": Enemy("Alligator", 74, 19, 13, 35, random.randrange(30, 41), "medium", 5),
            "Poison Frog": Enemy("Poison Frog", 56, 22, 6, 40, random.randrange(35, 46), "medium", 4),
            "Swamp Troll": Enemy("Swamp Troll", 91, 15, 16, 45, random.randrange(40, 51), "medium", 6),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 63, 18, 8, 35, random.randrange(30, 41), "medium", 4),
            "Bog Witch": Enemy("Bog Witch", 70, 20, 9, 50, random.randrange(45, 56), "medium", 5),
            
            "Stone Golem": Enemy("Stone Golem", 105, 15, 20, 55, random.randrange(50, 61), "medium", 6),
            "Cultist": Enemy("Cultist", 67, 19, 11, 40, random.randrange(35, 46), "medium", 4),
            "Mummy": Enemy("Mummy", 77, 18, 13, 45, random.randrange(40, 51), "medium", 5),
            "Animated Statue": Enemy("Animated Statue", 84, 17, 16, 50, random.randrange(45, 56), "medium", 5),
            "Temple Guardian": Enemy("Temple Guardian", 91, 19, 15, 55, random.randrange(50, 61), "medium", 6),
            
            "Mountain Lion": Enemy("Mountain Lion", 70, 20, 10, 40, random.randrange(35, 46), "medium", 4),
            "Rock Elemental": Enemy("Rock Elemental", 98, 15, 20, 50, random.randrange(45, 56), "medium", 6),
            "Harpy": Enemy("Harpy", 67, 22, 9, 45, random.randrange(40, 51), "medium", 4),
            "Yeti": Enemy("Yeti", 88, 19, 13, 50, random.randrange(45, 56), "medium", 6),
            "Orc": Enemy("Orc", 77, 18, 11, 40, random.randrange(35, 46), "medium", 5),
            
            "Sand Wurm": Enemy("Sand Wurm", 91, 19, 13, 45, random.randrange(40, 51), "medium", 6),
            "Dried Mummy": Enemy("Dried Mummy", 81, 17, 15, 40, random.randrange(35, 46), "medium", 5),
            "Dust Devil": Enemy("Dust Devil", 63, 22, 10, 45, random.randrange(40, 51), "medium", 4),
            "Desert Bandit": Enemy("Desert Bandit", 70, 20, 11, 50, random.randrange(45, 56), "medium", 5),
            "Leopard": Enemy("Leopard", 67, 21, 8, 35, random.randrange(30, 41), "medium", 3),
            
            # Medium-Hard Enemies
            "Canyon Cougar": Enemy("Canyon Cougar", 98, 30, 14, 70, random.randrange(65, 81), "medium-hard", 7),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 133, 23, 25, 75, random.randrange(70, 86), "medium-hard", 9),
            "Dust Devil": Enemy("Dust Devil", 119, 27, 21, 80, random.randrange(75, 91), "medium-hard", 8),
            "Petrified Warrior": Enemy("Petrified Warrior", 112, 25, 23, 85, random.randrange(80, 96), "medium-hard", 7),
            "Thunderbird": Enemy("Thunderbird", 126, 28, 19, 90, random.randrange(85, 101), "medium-hard", 8),
            
            # Hard Enemies
            "Venomous Hydra": Enemy("Venomous Hydra", 175, 39, 28, 120, random.randrange(95, 116), "hard", 10),
            "Plague Bearer": Enemy("Plague Bearer", 161, 42, 25, 125, random.randrange(100, 121), "hard", 11),
            "Mire Leviathan": Enemy("Mire Leviathan", 210, 35, 32, 130, random.randrange(105, 126), "hard", 12),
            "Toxic Shambler": Enemy("Toxic Shambler", 154, 46, 21, 135, random.randrange(110, 131), "hard", 13),
            "Swamp Hag": Enemy("Swamp Hag", 168, 41, 26, 140, random.randrange(115, 136), "hard", 14),
            
            "Ancient Golem": Enemy("Ancient Golem", 245, 32, 40, 120, random.randrange(120, 141), "hard", 10),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 189, 42, 29, 125, random.randrange(125, 146), "hard", 11),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 161, 49, 26, 130, random.randrange(130, 151), "hard", 12),
            "Ruin Wraith": Enemy("Ruin Wraith", 175, 46, 29, 135, random.randrange(135, 156), "hard", 13),
            "Forgotten Titan": Enemy("Forgotten Titan", 231, 39, 37, 140, random.randrange(140, 161), "hard", 14),
            
            "Frost Giant": Enemy("Frost Giant", 231, 42, 34, 100, random.randrange(145, 166), "hard", 10),
            "Storm Harpy": Enemy("Storm Harpy", 168, 53, 23, 105, random.randrange(150, 171), "hard", 11),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 210, 39, 41, 110, random.randrange(155, 176), "hard", 12),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 189, 49, 30, 115, random.randrange(160, 181), "hard", 13),
            "Yeti Alpha": Enemy("Yeti Alpha", 217, 46, 38, 120, random.randrange(165, 186), "hard", 14),
            
            "Fire Elemental": Enemy("Fire Elemental", 196, 56, 28, 100, random.randrange(170, 191), "hard", 10),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 182, 53, 32, 105, random.randrange(175, 196), "hard", 11),
            "Mirage Assassin": Enemy("Mirage Assassin", 175, 60, 25, 110, random.randrange(180, 201), "hard", 12),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 203, 49, 35, 115, random.randrange(185, 206), "hard", 13),
            "Desert Colossus": Enemy("Desert Colossus", 245, 46, 49, 120, random.randrange(190, 211), "hard", 14),
            
            "Nightmare Stalker": Enemy("Nightmare Stalker", 189, 56, 32, 110, random.randrange(195, 216), "hard", 10),
            "Void Weaver": Enemy("Void Weaver", 175, 63, 28, 115, random.randrange(200, 221), "hard", 11),
            "Shadow Dragon": Enemy("Shadow Dragon", 231, 55, 39, 120, random.randrange(205, 226), "hard", 12),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 168, 67, 32, 125, random.randrange(210, 231), "hard", 13),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 259, 56, 46, 130, random.randrange(215, 236), "hard", 14),
            
            # Very Hard Enemies
            "Necropolis Guardian": Enemy("Necropolis Guardian", 336, 74, 56, 300, random.randrange(240, 271), "very-hard", 15),
            "Soul Reaver": Enemy("Soul Reaver", 301, 84, 49, 325, random.randrange(250, 281), "very-hard", 16),
            "Bone Colossus": Enemy("Bone Colossus", 371, 70, 63, 350, random.randrange(260, 291), "very-hard", 17),
            "Spectral Devourer": Enemy("Spectral Devourer", 322, 81, 53, 375, random.randrange(270, 301), "very-hard", 18),
            "Lich King": Enemy("Lich King", 350, 77, 60, 400, random.randrange(280, 311), "very-hard", 19),
            
            "Timeless Sphinx": Enemy("Timeless Sphinx", 357, 76, 62, 300, random.randrange(290, 321), "very-hard", 15),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 336, 81, 56, 325, random.randrange(300, 331), "very-hard", 16),
            "Anubis Reborn": Enemy("Anubis Reborn", 350, 78, 57, 350, random.randrange(310, 341), "very-hard", 17),
            "Mummy Emperor": Enemy("Mummy Emperor", 371, 74, 63, 375, random.randrange(320, 351), "very-hard", 18),
            "Living Obelisk": Enemy("Living Obelisk", 406, 70, 67, 400, random.randrange(330, 361), "very-hard", 19),
            
            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 364, 84, 63, 300, random.randrange(340, 371), "very-hard", 15),
            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 392, 77, 67, 325, random.randrange(350, 381), "very-hard", 16),
            "Void Titan": Enemy("Void Titan", 420, 74, 70, 350, random.randrange(360, 391), "very-hard", 17),
            "Chaos Incarnate": Enemy("Chaos Incarnate", 378, 81, 67, 375, random.randrange(370, 401), "very-hard", 18),
            "Eternity Warden": Enemy("Eternity Warden", 406, 78, 69, 400, random.randrange(380, 411), "very-hard", 19),
            
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