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
            
            "Bat": Enemy("Bat", 32, 25, 15, 10, random.randrange(3, 10), "low", 1),
            "Goblin": Enemy("Goblin", 38, 30, 18, 15, random.randrange(5, 15), "low", 2),
            "Spider": Enemy("Spider", 30, 28, 15, 20, random.randrange(8, 18), "low", 1),
            "Slime": Enemy("Slime", 92, 24, 18, 25, random.randrange(10, 20), "low", 2),
            "Frog": Enemy("Frog", 68, 29, 15, 30, random.randrange(12, 24), "low", 3),
            
            "Tree Sprite": Enemy("Tree Sprite", 28, 13, 5, 10, random.randrange(3, 10), "low", 1),
            "Snake": Enemy("Snake", 32, 17, 2, 15, random.randrange(5, 15), "low", 1),
            "Forest Hawk": Enemy("Forest Hawk", 38, 14, 3, 20, random.randrange(8, 18), "low", 2),
            "Locust": Enemy("Locust", 35, 20, 3, 25, random.randrange(10, 20), "low", 2),
            "Leprechaun": Enemy("Leprechaun", 58, 15, 3, 30, random.randrange(12, 24), "low", 3),
            
            "Wood Spirit": Enemy("Wood Spirit", 32, 27, 16, 10, random.randrange(3, 10), "low", 1),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 40, 28, 17, 15, random.randrange(5, 15), "low", 2),
            "Deep Bat": Enemy("Deep Bat", 35, 29, 15, 20, random.randrange(8, 18), "low", 2),
            "Giant Firefly": Enemy("Giant Firefly", 45, 25, 17, 25, random.randrange(10, 20), "low", 2),
            "Treant": Enemy("Treant", 75, 28, 18, 30, random.randrange(12, 24), "low", 3),
            
             # Medium Enemies (Levels 5-9)
            "Alligator": Enemy("Alligator", 98, 32, 28, 35, random.randrange(30, 41), "medium", 5),
            "Poison Frog": Enemy("Poison Frog", 75, 27, 21, 40, random.randrange(35, 46), "medium", 4),
            "Swamp Troll": Enemy("Swamp Troll", 115, 35, 37, 45, random.randrange(40, 51), "medium", 6),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 81, 28, 20, 35, random.randrange(30, 41), "medium", 4),
            "Bog Witch": Enemy("Bog Witch", 92, 33, 27, 50, random.randrange(45, 56), "medium", 5),
            
            "Stone Golem": Enemy("Stone Golem", 132, 33, 39, 55, random.randrange(50, 61), "medium", 6),
            "Cultist": Enemy("Cultist", 86, 26, 22, 40, random.randrange(35, 46), "medium", 4),
            "Mummy": Enemy("Mummy", 98, 31, 29, 45, random.randrange(40, 51), "medium", 5),
            "Animated Statue": Enemy("Animated Statue", 109, 29, 31, 50, random.randrange(45, 56), "medium", 5),
            "Temple Guardian": Enemy("Temple Guardian", 121, 34, 38, 55, random.randrange(50, 61), "medium", 6),
            
            "Mountain Lion": Enemy("Mountain Lion", 92, 28, 20, 40, random.randrange(35, 46), "medium", 4),
            "Rock Elemental": Enemy("Rock Elemental", 127, 32, 40, 50, random.randrange(45, 56), "medium", 6),
            "Harpy": Enemy("Harpy", 86, 29, 19, 45, random.randrange(40, 51), "medium", 4),
            "Yeti": Enemy("Yeti", 115, 36, 36, 50, random.randrange(45, 56), "medium", 6),
            "Orc": Enemy("Orc", 104, 33, 27, 40, random.randrange(35, 46), "medium", 5),
            
            "Sand Wurm": Enemy("Sand Wurm", 121, 36, 36, 45, random.randrange(40, 51), "medium", 6),
            "Dried Mummy": Enemy("Dried Mummy", 109, 31, 29, 40, random.randrange(35, 46), "medium", 5),
            "Dust Devil": Enemy("Dust Devil", 81, 29, 19, 45, random.randrange(40, 51), "medium", 4),
            "Desert Bandit": Enemy("Desert Bandit", 98, 32, 28, 50, random.randrange(45, 56), "medium", 5),
            "Leopard": Enemy("Leopard", 86, 20, 16, 35, random.randrange(30, 41), "medium", 3),
            
            # Medium-Hard Enemies (Levels 10-12)
            "Canyon Cougar": Enemy("Canyon Cougar", 121, 64, 58, 70, random.randrange(65, 81), "medium-hard", 7),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 160, 61, 69, 75, random.randrange(70, 86), "medium-hard", 9),
            "Dust Devil": Enemy("Dust Devil", 143, 67, 65, 80, random.randrange(75, 91), "medium-hard", 8),
            "Petrified Warrior": Enemy("Petrified Warrior", 138, 59, 63, 85, random.randrange(80, 96), "medium-hard", 7),
            "Thunderbird": Enemy("Thunderbird", 154, 69, 63, 90, random.randrange(85, 101), "medium-hard", 8),
            
            # Hard Enemies (Levels 13-17)
            "Venomous Hydra": Enemy("Venomous Hydra", 209, 82, 74, 120, random.randrange(95, 116), "hard", 10),
            "Plague Bearer": Enemy("Plague Bearer", 193, 87, 79, 125, random.randrange(100, 121), "hard", 11),
            "Mire Leviathan": Enemy("Mire Leviathan", 253, 85, 91, 130, random.randrange(105, 126), "hard", 12),
            "Toxic Shambler": Enemy("Toxic Shambler", 187, 99, 93, 135, random.randrange(110, 131), "hard", 13),
            "Swamp Hag": Enemy("Swamp Hag", 204, 104, 100, 140, random.randrange(115, 136), "hard", 14),
            
            "Ancient Golem": Enemy("Ancient Golem", 292, 74, 82, 120, random.randrange(120, 141), "hard", 10),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 226, 85, 81, 125, random.randrange(125, 146), "hard", 11),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 198, 94, 86, 130, random.randrange(130, 151), "hard", 12),
            "Ruin Wraith": Enemy("Ruin Wraith", 215, 100, 92, 135, random.randrange(135, 156), "hard", 13),
            "Forgotten Titan": Enemy("Forgotten Titan", 275, 96, 108, 140, random.randrange(140, 161), "hard", 14),
            
            "Frost Giant": Enemy("Frost Giant", 275, 76, 80, 100, random.randrange(145, 166), "hard", 10),
            "Storm Harpy": Enemy("Storm Harpy", 204, 89, 77, 105, random.randrange(150, 171), "hard", 11),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 253, 87, 93, 110, random.randrange(155, 176), "hard", 12),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 231, 101, 91, 115, random.randrange(160, 181), "hard", 13),
            "Yeti Alpha": Enemy("Yeti Alpha", 264, 98, 106, 120, random.randrange(165, 186), "hard", 14),
            
            "Fire Elemental": Enemy("Fire Elemental", 237, 83, 73, 100, random.randrange(170, 191), "hard", 10),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 220, 88, 78, 105, random.randrange(175, 196), "hard", 11),
            "Mirage Assassin": Enemy("Mirage Assassin", 209, 95, 85, 110, random.randrange(180, 201), "hard", 12),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 248, 102, 90, 115, random.randrange(185, 206), "hard", 13),
            "Desert Colossus": Enemy("Desert Colossus", 292, 97, 107, 120, random.randrange(190, 211), "hard", 14),
            
            "Nightmare Stalker": Enemy("Nightmare Stalker", 231, 82, 74, 110, random.randrange(195, 216), "hard", 10),
            "Void Weaver": Enemy("Void Weaver", 215, 87, 79, 115, random.randrange(200, 221), "hard", 11),
            "Shadow Dragon": Enemy("Shadow Dragon", 281, 94, 86, 120, random.randrange(205, 226), "hard", 12),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 204, 101, 91, 125, random.randrange(210, 231), "hard", 13),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 308, 97, 107, 130, random.randrange(215, 236), "hard", 14),
            
            # Very Hard Enemies (Levels 18-22)
            "Necropolis Guardian": Enemy("Necropolis Guardian", 396, 106, 110, 300, random.randrange(240, 271), "very-hard", 15),
            "Soul Reaver": Enemy("Soul Reaver", 363, 120, 104, 325, random.randrange(250, 281), "very-hard", 16),
            "Bone Colossus": Enemy("Bone Colossus", 440, 114, 122, 350, random.randrange(260, 291), "very-hard", 17),
            "Spectral Devourer": Enemy("Spectral Devourer", 385, 128, 120, 375, random.randrange(270, 301), "very-hard", 18),
            "Lich King": Enemy("Lich King", 418, 124, 136, 400, random.randrange(280, 311), "very-hard", 19),
            
            "Timeless Sphinx": Enemy("Timeless Sphinx", 424, 107, 109, 300, random.randrange(290, 321), "very-hard", 15),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 402, 116, 108, 325, random.randrange(300, 331), "very-hard", 16),
            "Anubis Reborn": Enemy("Anubis Reborn", 418, 116, 120, 350, random.randrange(310, 341), "very-hard", 17),
            "Mummy Emperor": Enemy("Mummy Emperor", 440, 120, 128, 375, random.randrange(320, 351), "very-hard", 18),
            "Living Obelisk": Enemy("Living Obelisk", 479, 118, 142, 400, random.randrange(330, 361), "very-hard", 19),
            
            #Dragon's Lair
            "Ancient Wyvern": Enemy("Ancient Wyvern", 431, 122, 102, 300, random.randrange(390, 421), "very-hard", 16),
            "Elemental Drake": Enemy("Elemental Drake", 416, 114, 102, 325, random.randrange(400, 431), "very-hard", 15),
            "Dragonlord": Enemy("Dragonlord", 447, 126, 110, 350, random.randrange(410, 441), "very-hard", 17),
            "Chromatic Dragon": Enemy("Chromatic Dragon", 462, 128, 120, 375, random.randrange(420, 451), "very-hard", 18),
            "Elder Dragon": Enemy("Elder Dragon", 485, 126, 134, 400, random.randrange(440, 471), "very-hard", 19),
            
            # Extreme Enemies
            "Magma Colossus": Enemy("Magma Colossus", 693, 132, 146, 500, random.randrange(480, 531), "extreme", 21),
            "Phoenix Overlord": Enemy("Phoenix Overlord", 655, 144, 128, 520, random.randrange(500, 551), "extreme", 20),
            "Volcanic Titan": Enemy("Volcanic Titan", 770, 138, 152, 540, random.randrange(520, 571), "extreme", 24),
            "Inferno Wyrm": Enemy("Inferno Wyrm", 732, 142, 136, 560, random.randrange(540, 591), "extreme", 22),
            "Cinder Archfiend": Enemy("Cinder Archfiend", 678, 148, 130, 580, random.randrange(560, 611), "extreme", 23),
            
            # Boss Monsters
            "Seraphim Guardian": Enemy("Seraphim Guardian", 1078, 154, 162, 1000, random.randrange(950, 1051), "boss", 25),
            "Celestial Arbiter": Enemy("Celestial Arbiter", 1001, 166, 150, 1100, random.randrange(1050, 1151), "boss", 25),
            "Astral Demiurge": Enemy("Astral Demiurge", 1155, 158, 158, 1200, random.randrange(1150, 1251), "boss", 25),
            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1232, 170, 146, 1300, random.randrange(1250, 1351), "boss", 25),
            "Divine Architect": Enemy("Divine Architect", 1309, 162, 154, 1500, random.randrange(1450, 1551), "boss", 25),
    }