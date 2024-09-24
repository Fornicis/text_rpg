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
            "Rat": Enemy("Rat", 21, 21, 5, 10, random.randrange(3, 10), "low", 1),
            "Boar": Enemy("Boar", 30, 24, 7, 15, random.randrange(5, 15), "low", 2),
            "Plains Hawk": Enemy("Plains Hawk", 19, 26, 4, 20, random.randrange(8, 18), "low", 1),
            "Strider": Enemy("Strider", 34, 25, 8, 25, random.randrange(10, 20), "low", 2),
            "Bull": Enemy("Bull", 43, 27, 10, 30, random.randrange(12, 24), "low", 3),
            
            "Bat": Enemy("Bat", 24, 23, 6, 10, random.randrange(3, 10), "low", 1),
            "Goblin": Enemy("Goblin", 27, 25, 8, 15, random.randrange(5, 15), "low", 2),
            "Spider": Enemy("Spider", 22, 26, 5, 20, random.randrange(8, 18), "low", 1),
            "Slime": Enemy("Slime", 38, 22, 9, 25, random.randrange(10, 20), "low", 2),
            "Frog": Enemy("Frog", 36, 26, 8, 30, random.randrange(12, 24), "low", 3),
            
            "Tree Sprite": Enemy("Tree Sprite", 20, 24, 6, 10, random.randrange(3, 10), "low", 1),
            "Snake": Enemy("Snake", 24, 27, 5, 15, random.randrange(5, 15), "low", 1),
            "Forest Hawk": Enemy("Forest Hawk", 29, 25, 7, 20, random.randrange(8, 18), "low", 2),
            "Locust": Enemy("Locust", 26, 26, 6, 25, random.randrange(10, 20), "low", 2),
            "Leprechaun": Enemy("Leprechaun", 41, 23, 9, 30, random.randrange(12, 24), "low", 3),
            
            "Wood Spirit": Enemy("Wood Spirit", 26, 24, 7, 10, random.randrange(3, 10), "low", 1),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 32, 26, 9, 15, random.randrange(5, 15), "low", 2),
            "Deep Bat": Enemy("Deep Bat", 27, 27, 7, 20, random.randrange(8, 18), "low", 2),
            "Giant Firefly": Enemy("Giant Firefly", 34, 24, 8, 25, random.randrange(10, 20), "low", 2),
            "Treant": Enemy("Treant", 51, 25, 12, 30, random.randrange(12, 24), "low", 3),
            
             # Medium Enemies (Levels 5-9)
            "Alligator": Enemy("Alligator", 77, 43, 30, 35, random.randrange(30, 41), "medium", 5),
            "Poison Frog": Enemy("Poison Frog", 60, 45, 28, 40, random.randrange(35, 46), "medium", 4),
            "Swamp Troll": Enemy("Swamp Troll", 89, 44, 32, 45, random.randrange(40, 51), "medium", 6),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 64, 47, 26, 35, random.randrange(30, 41), "medium", 4),
            "Bog Witch": Enemy("Bog Witch", 72, 43, 29, 50, random.randrange(45, 56), "medium", 5),
            
            "Stone Golem": Enemy("Stone Golem", 102, 42, 34, 55, random.randrange(50, 61), "medium", 6),
            "Cultist": Enemy("Cultist", 68, 46, 28, 40, random.randrange(35, 46), "medium", 4),
            "Mummy": Enemy("Mummy", 81, 44, 31, 45, random.randrange(40, 51), "medium", 5),
            "Animated Statue": Enemy("Animated Statue", 85, 43, 32, 50, random.randrange(45, 56), "medium", 5),
            "Temple Guardian": Enemy("Temple Guardian", 94, 43, 33, 55, random.randrange(50, 61), "medium", 6),
            
            "Mountain Lion": Enemy("Mountain Lion", 72, 48, 29, 40, random.randrange(35, 46), "medium", 4),
            "Rock Elemental": Enemy("Rock Elemental", 98, 41, 35, 50, random.randrange(45, 56), "medium", 6),
            "Harpy": Enemy("Harpy", 68, 48, 27, 45, random.randrange(40, 51), "medium", 4),
            "Yeti": Enemy("Yeti", 89, 45, 33, 50, random.randrange(45, 56), "medium", 6),
            "Orc": Enemy("Orc", 81, 46, 30, 40, random.randrange(35, 46), "medium", 5),
            
            "Sand Wurm": Enemy("Sand Wurm", 94, 44, 34, 45, random.randrange(40, 51), "medium", 6),
            "Dried Mummy": Enemy("Dried Mummy", 85, 43, 31, 40, random.randrange(35, 46), "medium", 5),
            "Dust Devil": Enemy("Dust Devil", 64, 49, 28, 45, random.randrange(40, 51), "medium", 4),
            "Desert Bandit": Enemy("Desert Bandit", 77, 47, 30, 50, random.randrange(45, 56), "medium", 5),
            "Leopard": Enemy("Leopard", 68, 48, 27, 35, random.randrange(30, 41), "medium", 3),
            
            # Medium-Hard Enemies (Levels 10-14)
            "Canyon Cougar": Enemy("Canyon Cougar", 111, 60, 50, 70, random.randrange(65, 81), "medium-hard", 10),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 136, 57, 52, 75, random.randrange(70, 86), "medium-hard", 12),
            "Dust Devil": Enemy("Dust Devil", 123, 61, 49, 80, random.randrange(75, 91), "medium-hard", 11),
            "Petrified Warrior": Enemy("Petrified Warrior", 119, 60, 48, 85, random.randrange(80, 96), "medium-hard", 10),
            "Thunderbird": Enemy("Thunderbird", 132, 63, 49, 90, random.randrange(85, 101), "medium-hard", 11),
            
            #Hard Enemies (Levels 15-19)
            "Venomous Hydra": Enemy("Venomous Hydra", 170, 78, 87, 120, random.randrange(95, 116), "hard", 15),
            "Plague Bearer": Enemy("Plague Bearer", 162, 81, 84, 125, random.randrange(100, 121), "hard", 16),
            "Mire Leviathan": Enemy("Mire Leviathan", 204, 83, 86, 130, random.randrange(105, 126), "hard", 17),
            "Toxic Shambler": Enemy("Toxic Shambler", 153, 87, 82, 135, random.randrange(110, 131), "hard", 18),
            "Swamp Hag": Enemy("Swamp Hag", 166, 89, 80, 140, random.randrange(115, 136), "hard", 19),
            
            "Ancient Golem": Enemy("Ancient Golem", 230, 75, 90, 120, random.randrange(120, 141), "hard", 15),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 187, 79, 86, 125, random.randrange(125, 146), "hard", 16),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 170, 84, 83, 130, random.randrange(130, 151), "hard", 17),
            "Ruin Wraith": Enemy("Ruin Wraith", 179, 86, 81, 135, random.randrange(135, 156), "hard", 18),
            "Forgotten Titan": Enemy("Forgotten Titan", 221, 88, 85, 140, random.randrange(140, 161), "hard", 19),
            
            "Frost Giant": Enemy("Frost Giant", 221, 76, 89, 100, random.randrange(145, 166), "hard", 15),
            "Storm Harpy": Enemy("Storm Harpy", 170, 83, 82, 105, random.randrange(150, 171), "hard", 16),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 204, 85, 84, 110, random.randrange(155, 176), "hard", 17),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 187, 88, 79, 115, random.randrange(160, 181), "hard", 18),
            "Yeti Alpha": Enemy("Yeti Alpha", 213, 90, 81, 120, random.randrange(165, 186), "hard", 19),
            
            "Fire Elemental": Enemy("Fire Elemental", 196, 77, 88, 100, random.randrange(170, 191), "hard", 15),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 179, 82, 83, 105, random.randrange(175, 196), "hard", 16),
            "Mirage Assassin": Enemy("Mirage Assassin", 170, 86, 80, 110, random.randrange(180, 201), "hard", 17),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 196, 89, 78, 115, random.randrange(185, 206), "hard", 18),
            "Desert Colossus": Enemy("Desert Colossus", 230, 91, 76, 120, random.randrange(190, 211), "hard", 19),

            "Nightmare Stalker": Enemy("Nightmare Stalker", 187, 80, 85, 110, random.randrange(195, 216), "hard", 15),
            "Void Weaver": Enemy("Void Weaver", 179, 84, 81, 115, random.randrange(200, 221), "hard", 16),
            "Shadow Dragon": Enemy("Shadow Dragon", 221, 87, 82, 120, random.randrange(205, 226), "hard", 17),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 170, 90, 77, 125, random.randrange(210, 231), "hard", 18),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 238, 91, 79, 130, random.randrange(215, 236), "hard", 19),
            
            # Necropolis
            "Necropolis Guardian": Enemy("Necropolis Guardian", 323, 106, 93, 300, random.randrange(240, 271), "very-hard", 20),
            "Soul Reaver": Enemy("Soul Reaver", 298, 112, 88, 325, random.randrange(250, 281), "very-hard", 21),
            "Bone Colossus": Enemy("Bone Colossus", 357, 117, 90, 350, random.randrange(260, 291), "very-hard", 22),
            "Spectral Devourer": Enemy("Spectral Devourer", 315, 122, 84, 375, random.randrange(270, 301), "very-hard", 23),
            "Lich King": Enemy("Lich King", 340, 125, 87, 400, random.randrange(280, 311), "very-hard", 24),
            
            # Ancient Ruins
            "Timeless Sphinx": Enemy("Timeless Sphinx", 340, 104, 95, 300, random.randrange(290, 321), "very-hard", 20),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 323, 110, 90, 325, random.randrange(300, 331), "very-hard", 21),
            "Anubis Reborn": Enemy("Anubis Reborn", 340, 115, 92, 350, random.randrange(310, 341), "very-hard", 22),
            "Mummy Emperor": Enemy("Mummy Emperor", 357, 120, 86, 375, random.randrange(320, 351), "very-hard", 23),
            "Living Obelisk": Enemy("Living Obelisk", 383, 124, 89, 400, random.randrange(330, 361), "very-hard", 24),
            
            # Death Valley
            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 340, 114, 91, 350, random.randrange(310, 341), "very-hard", 22),
            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 357, 119, 85, 375, random.randrange(320, 351), "very-hard", 23),
            "Void Titan": Enemy("Void Titan", 383, 123, 88, 400, random.randrange(330, 361), "very-hard", 24),
            "Chaos Incarnate": Enemy("Chaos Incarnate", 366, 121, 83, 425, random.randrange(340, 371), "very-hard", 23),
            "Eternity Warden": Enemy("Eternity Warden", 400, 125, 86, 450, random.randrange(350, 381), "very-hard", 24),

            # Dragon's Lair
            "Ancient Wyvern": Enemy("Ancient Wyvern", 349, 111, 89, 300, random.randrange(390, 421), "very-hard", 21),
            "Elemental Drake": Enemy("Elemental Drake", 340, 108, 92, 325, random.randrange(400, 431), "very-hard", 20),
            "Dragonlord": Enemy("Dragonlord", 366, 116, 91, 350, random.randrange(410, 441), "very-hard", 22),
            "Chromatic Dragon": Enemy("Chromatic Dragon", 374, 121, 85, 375, random.randrange(420, 451), "very-hard", 23),
            "Elder Dragon": Enemy("Elder Dragon", 391, 124, 88, 400, random.randrange(440, 471), "very-hard", 24),
            
            # Extreme Enemies
            "Magma Colossus": Enemy("Magma Colossus", 589, 115, 118, 500, random.randrange(480, 531), "extreme", 21),
            "Phoenix Overlord": Enemy("Phoenix Overlord", 557, 122, 115, 520, random.randrange(500, 551), "extreme", 20),
            "Volcanic Titan": Enemy("Volcanic Titan", 655, 117, 122, 540, random.randrange(520, 571), "extreme", 24),
            "Inferno Wyrm": Enemy("Inferno Wyrm", 622, 121, 116, 560, random.randrange(540, 591), "extreme", 22),
            "Cinder Archfiend": Enemy("Cinder Archfiend", 576, 126, 111, 580, random.randrange(560, 611), "extreme", 23),
            
            # Boss Monsters
            "Seraphim Guardian": Enemy("Seraphim Guardian", 916, 131, 137, 1000, random.randrange(950, 1051), "boss", 25),
            "Celestial Arbiter": Enemy("Celestial Arbiter", 851, 141, 128, 1100, random.randrange(1050, 1151), "boss", 25),
            "Astral Demiurge": Enemy("Astral Demiurge", 982, 134, 136, 1200, random.randrange(1150, 1251), "boss", 25),
            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1047, 145, 126, 1300, random.randrange(1250, 1351), "boss", 25),
            "Divine Architect": Enemy("Divine Architect", 1113, 138, 132, 1500, random.randrange(1450, 1551), "boss", 25),
    }