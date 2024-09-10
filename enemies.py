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
        #Easy Enemies
            
            #Plains
            "Rat": Enemy("Rat", 40, 15, 2, 10, random.randrange(3, 10), "low", 1),
            "Boar": Enemy("Boar", 50, 16, 5, 15, random.randrange(5, 15), "low", 2),
            "Plains Hawk": Enemy("Plains Hawk", 35, 18, 4, 20, random.randrange(8, 18), "low", 1),
            "Strider": Enemy("Strider", 60, 14, 4, 25, random.randrange(10, 20), "low", 2),
            "Bull": Enemy("Bull", 70, 16, 5, 30, random.randrange(12, 24), "low", 3),
            
            #Cave
            "Bat": Enemy("Bat", 40, 15, 4, 10, random.randrange(3, 10), "low", 1),
            "Goblin": Enemy("Goblin", 50, 18, 5, 15, random.randrange(5, 15), "low", 2),
            "Spider": Enemy("Spider", 35, 18, 4, 20, random.randrange(8, 18), "low", 1),
            "Slime": Enemy("Slime", 70, 14, 8, 25, random.randrange(10, 20), "low", 2),
            "Frog": Enemy("Frog", 60, 17, 4, 30, random.randrange(12, 24), "low", 3),
            
            #Forest
            "Tree Sprite": Enemy("Tree Sprite", 35, 15, 5, 10, random.randrange(3, 10), "low", 1),
            "Snake": Enemy("Snake", 40, 20, 3, 15, random.randrange(5, 15), "low", 1),
            "Forest Hawk": Enemy("Forest Hawk", 50, 17, 4, 20, random.randrange(8, 18), "low", 2),
            "Locust": Enemy("Locust", 45, 25, 4, 25, random.randrange(10, 20), "low", 2),
            "Leprechaun": Enemy("Leprechaun", 75, 18, 3, 30, random.randrange(12, 24), "low", 3),
            
            #Deepwoods
            "Wood Spirit": Enemy("Wood Spirit", 40, 16, 4, 10, random.randrange(3, 10), "low", 1),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 50, 15, 6, 15, random.randrange(5, 15), "low", 2),
            "Deep Bat": Enemy("Deep Bat", 45, 18, 3, 20, random.randrange(8, 18), "low", 2),
            "Giant Firefly": Enemy("Giant Firefly", 60, 15, 5, 25, random.randrange(10, 20), "low", 2),
            "Treant": Enemy("Treant", 100, 19, 6, 30, random.randrange(12, 24), "low", 3),
            
            #Medium Enemies
            
            #Swamp
            "Alligator": Enemy("Alligator", 105, 27, 18, 35, random.randrange(30, 41), "medium", 5),
            "Poison Frog": Enemy("Poison Frog", 80, 32, 8, 40, random.randrange(35, 46), "medium", 4),
            "Swamp Troll": Enemy("Swamp Troll", 130, 22, 23, 45, random.randrange(40, 51), "medium", 6),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 90, 25, 11, 35, random.randrange(30, 41), "medium", 4),
            "Bog Witch": Enemy("Bog Witch", 100, 29, 13, 50, random.randrange(45, 56), "medium", 5),
            
            #Temple
            "Stone Golem": Enemy("Stone Golem", 150, 22, 28, 55, random.randrange(50, 61), "medium", 6),
            "Cultist": Enemy("Cultist", 95, 27, 15, 40, random.randrange(35, 46), "medium", 4),
            "Mummy": Enemy("Mummy", 110, 25, 18, 45, random.randrange(40, 51), "medium", 5),
            "Animated Statue": Enemy("Animated Statue", 120, 24, 23, 50, random.randrange(45, 56), "medium", 5),
            "Temple Guardian": Enemy("Temple Guardian", 130, 27, 21, 55, random.randrange(50, 61), "medium", 6),
            
            #Mountain
            "Mountain Lion": Enemy("Mountain Lion", 100, 29, 14, 40, random.randrange(35, 46), "medium", 4),
            "Rock Elemental": Enemy("Rock Elemental", 140, 22, 29, 50, random.randrange(45, 56), "medium", 6),
            "Harpy": Enemy("Harpy", 95, 32, 13, 45, random.randrange(40, 51), "medium", 4),
            "Yeti": Enemy("Yeti", 125, 27, 19, 50, random.randrange(45, 56), "medium", 6),
            "Orc": Enemy("Orc", 110, 25, 16, 40, random.randrange(35, 46), "medium", 5),
            
            #Desert
            "Sand Wurm": Enemy("Sand Wurm", 130, 27, 19, 45, random.randrange(40, 51), "medium", 6),
            "Dried Mummy": Enemy("Dried Mummy", 115, 24, 22, 40, random.randrange(35, 46), "medium", 5),
            "Dust Devil": Enemy("Dust Devil", 90, 32, 14, 45, random.randrange(40, 51), "medium", 4),
            "Desert Bandit": Enemy("Desert Bandit", 100, 29, 16, 50, random.randrange(45, 56), "medium", 5),
            "Leopard": Enemy("Leopard", 95, 30, 12, 35, random.randrange(30, 41), "medium", 3),
            
            #Medium-Hard Enemies
            
            #Valley
            "Canyon Cougar": Enemy("Canyon Cougar", 140, 43, 20, 70, random.randrange(65, 81), "medium-hard", 7),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 190, 33, 35, 75, random.randrange(70, 86), "medium-hard", 9),
            "Dust Devil": Enemy("Dust Devil", 170, 38, 30, 80, random.randrange(75, 91), "medium-hard", 8),
            "Petrified Warrior": Enemy("Petrified Warrior", 160, 36, 33, 85, random.randrange(80, 96), "medium-hard", 7),
            "Thunderbird": Enemy("Thunderbird", 180, 40, 27, 90, random.randrange(85, 101), "medium-hard", 8),
            
            #Hard Enemies
            
            #Toxic Swamp
            "Venomous Hydra": Enemy("Venomous Hydra", 250, 55, 40, 120, random.randrange(95, 116), "hard", 10),
            "Plague Bearer": Enemy("Plague Bearer", 230, 60, 35, 125, random.randrange(100, 121), "hard", 11),
            "Mire Leviathan": Enemy("Mire Leviathan", 300, 50, 45, 130, random.randrange(105, 126), "hard", 12),
            "Toxic Shambler": Enemy("Toxic Shambler", 220, 65, 30, 135, random.randrange(110, 131), "hard", 13),
            "Swamp Hag": Enemy("Swamp Hag", 240, 58, 37, 140, random.randrange(115, 136), "hard", 14),
            
            #Ruins
            "Ancient Golem": Enemy("Ancient Golem", 350, 45, 57, 120, random.randrange(120, 141), "hard", 10),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 270, 60, 42, 125, random.randrange(125, 146), "hard", 11),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 230, 70, 37, 130, random.randrange(130, 151), "hard", 12),
            "Ruin Wraith": Enemy("Ruin Wraith", 250, 65, 42, 135, random.randrange(135, 156), "hard", 13),
            "Forgotten Titan": Enemy("Forgotten Titan", 330, 55, 53, 140, random.randrange(140, 161), "hard", 14),
            
            #Mountain Peaks
            "Frost Giant": Enemy("Frost Giant", 330, 60, 48, 100, random.randrange(145, 166), "hard", 10),
            "Storm Harpy": Enemy("Storm Harpy", 240, 75, 33, 105, random.randrange(150, 171), "hard", 11),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 300, 55, 58, 110, random.randrange(155, 176), "hard", 12),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 270, 70, 43, 115, random.randrange(160, 181), "hard", 13),
            "Yeti Alpha": Enemy("Yeti Alpha", 310, 65, 54, 120, random.randrange(165, 186), "hard", 14),
            
            #Scorching Plains
            "Fire Elemental": Enemy("Fire Elemental", 280, 80, 40, 100, random.randrange(170, 191), "hard", 10),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 260, 75, 45, 105, random.randrange(175, 196), "hard", 11),
            "Mirage Assassin": Enemy("Mirage Assassin", 250, 85, 35, 110, random.randrange(180, 201), "hard", 12),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 290, 70, 50, 115, random.randrange(185, 206), "hard", 13),
            "Desert Colossus": Enemy("Desert Colossus", 350, 65, 70, 120, random.randrange(190, 211), "hard", 14),
            
            #Shadowed Valley
            "Nightmare Stalker": Enemy("Nightmare Stalker", 270, 80, 45, 110, random.randrange(195, 216), "hard", 10),
            "Void Weaver": Enemy("Void Weaver", 250, 90, 40, 115, random.randrange(200, 221), "hard", 11),
            "Shadow Dragon": Enemy("Shadow Dragon", 330, 79, 55, 120, random.randrange(205, 226), "hard", 12),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 240, 95, 45, 125, random.randrange(210, 231), "hard", 13),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 370, 80, 65, 130, random.randrange(215, 236), "hard", 14),
            
            #Very Hard Enemies
            
            #Death Caves
            "Necropolis Guardian": Enemy("Necropolis Guardian", 480, 105, 80, 300, random.randrange(240, 271), "very-hard", 15),
            "Soul Reaver": Enemy("Soul Reaver", 430, 120, 70, 325, random.randrange(250, 281), "very-hard", 16),
            "Bone Colossus": Enemy("Bone Colossus", 530, 100, 90, 350, random.randrange(260, 291), "very-hard", 17),
            "Spectral Devourer": Enemy("Spectral Devourer", 460, 115, 75, 375, random.randrange(270, 301), "very-hard", 18),
            "Lich King": Enemy("Lich King", 500, 110, 85, 400, random.randrange(280, 311), "very-hard", 19),
            
            #Ancient Ruins
            "Timeless Sphinx": Enemy("Timeless Sphinx", 510, 108, 88, 300, random.randrange(290, 321), "very-hard", 15),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 480, 115, 80, 325, random.randrange(300, 331), "very-hard", 16),
            "Anubis Reborn": Enemy("Anubis Reborn", 500, 112, 82, 350, random.randrange(310, 341), "very-hard", 17),
            "Mummy Emperor": Enemy("Mummy Emperor", 530, 105, 90, 375, random.randrange(320, 351), "very-hard", 18),
            "Living Obelisk": Enemy("Living Obelisk", 580, 100, 95, 400, random.randrange(330, 361), "very-hard", 19),
            
            #Death Valley
            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 520, 120, 90, 300, random.randrange(340, 371), "very-hard", 15),
            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 560, 110, 95, 325, random.randrange(350, 381), "very-hard", 16),
            "Void Titan": Enemy("Void Titan", 600, 105, 100, 350, random.randrange(360, 391), "very-hard", 17),
            "Chaos Incarnate": Enemy("Chaos Incarnate", 540, 115, 95, 375, random.randrange(370, 401), "very-hard", 18),
            "Eternity Warden": Enemy("Eternity Warden", 580, 112, 98, 400, random.randrange(380, 411), "very-hard", 19),
            
            #Dragon's Lair
            "Ancient Wyvern": Enemy("Ancient Wyvern", 560, 125, 105, 300, random.randrange(390, 421), "very-hard", 16),
            "Elemental Drake": Enemy("Elemental Drake", 540, 130, 100, 325, random.randrange(400, 431), "very-hard", 15),
            "Dragonlord": Enemy("Dragonlord", 580, 128, 107, 350, random.randrange(410, 441), "very-hard", 17),
            "Chromatic Dragon": Enemy("Chromatic Dragon", 600, 126, 109, 375, random.randrange(420, 451), "very-hard", 18),
            "Elder Dragon": Enemy("Elder Dragon", 630, 130, 110, 400, random.randrange(440, 471), "very-hard", 19),
            
            #Extreme Enemies
            
            #Volcanic Valley
            "Magma Colossus": Enemy("Magma Colossus", 900, 190, 120, 500, random.randrange(480, 531), "extreme", 21),
            "Phoenix Overlord": Enemy("Phoenix Overlord", 850, 220, 120, 520, random.randrange(500, 551), "extreme", 20),
            "Volcanic Titan": Enemy("Volcanic Titan", 1000, 170, 130, 540, random.randrange(520, 571), "extreme", 24),
            "Inferno Wyrm": Enemy("Inferno Wyrm", 950, 200, 150, 560, random.randrange(540, 591), "extreme", 22),
            "Cinder Archfiend": Enemy("Cinder Archfiend", 880, 210, 145, 580, random.randrange(560, 611), "extreme", 23),
            
            #Boss Monsters
            
            #The Heavens
            "Seraphim Guardian": Enemy("Seraphim Guardian", 1400, 225, 200, 1000, random.randrange(950, 1051), "boss", 25),
            "Celestial Arbiter": Enemy("Celestial Arbiter", 1300, 220, 190, 1100, random.randrange(1050, 1151), "boss", 25),
            "Astral Demiurge": Enemy("Astral Demiurge", 1500, 215, 195, 1200, random.randrange(1150, 1251), "boss", 25),
            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1600, 245, 170, 1300, random.randrange(1250, 1351), "boss", 25),
            "Divine Architect": Enemy("Divine Architect", 1700, 250, 205, 1500, random.randrange(1450, 1551), "boss", 25),
    }