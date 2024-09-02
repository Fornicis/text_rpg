from player import Character
import random

class Enemy(Character):
    def __init__(self, name, hp, attack, defence, exp, gold, tier):
        super().__init__(name, hp, attack, defence)
        self.exp = exp
        self.gold = gold
        self.tier = tier
        
def initialise_enemies():
    return {
        #Easy Enemies
            
            #Plains
            "Rat": Enemy("Rat", 20, 10, 1, 10, random.randrange(3, 10), "low"),
            "Boar": Enemy("Boar", 30, 11, 3, 15, random.randrange(5, 15), "low"),
            "Plains Hawk": Enemy("Plains Hawk", 15, 13, 2, 20, random.randrange(8, 18), "low"),
            "Strider": Enemy("Strider", 40, 9, 2, 25, random.randrange(10, 20), "low"),
            "Bull": Enemy("Bull", 50, 11, 3, 30, random.randrange(12, 24), "low"),
            
            #Cave
            "Bat": Enemy("Bat", 20, 10, 2, 10, random.randrange(3, 10), "low"),
            "Goblin": Enemy("Goblin", 30, 13, 3, 15, random.randrange(5, 15), "low"),
            "Spider": Enemy("Spider", 15, 13, 2, 20, random.randrange(8, 18), "low"),
            "Slime": Enemy("Slime", 50, 9, 6, 25, random.randrange(10, 20), "low"),
            "Frog": Enemy("Frog", 40, 12, 2, 30, random.randrange(12, 24), "low"),
            
            #Forest
            "Tree Sprite": Enemy("Tree Sprite", 15, 10, 3, 10, random.randrange(3, 10), "low"),
            "Snake": Enemy("Snake", 20, 15, 1, 15, random.randrange(5, 15), "low"),
            "Forest Hawk": Enemy("Forest Hawk", 30, 12, 2, 20, random.randrange(8, 18), "low"),
            "Locust": Enemy("Locust", 25, 20, 2, 25, random.randrange(10, 20), "low"),
            "Leprechaun": Enemy("Leprechaun", 55, 13, 1, 30, random.randrange(12, 24), "low"),
            
            #Deepwoods
            "Wood Spirit": Enemy("Wood Spirit", 20, 11, 2, 10, random.randrange(3, 10), "low"),
            "Deepwood Stalker": Enemy("Deepwood Stalker", 30, 10, 4, 15, random.randrange(5, 15), "low"),
            "Deep Bat": Enemy("Deep Bat", 25, 13, 1, 20, random.randrange(8, 18), "low"),
            "Giant Firefly": Enemy("Giant Firefly", 40, 10, 3, 25, random.randrange(10, 20), "low"),
            "Treant": Enemy("Treant", 80, 14, 4, 30, random.randrange(12, 24), "low"),
            
            #Medium Enemies
            
            #Swamp
            "Alligator": Enemy("Alligator", 75, 20, 15, 35, random.randrange(30, 41), "medium"),
            "Poison Frog": Enemy("Poison Frog", 50, 25, 5, 40, random.randrange(35, 46), "medium"),
            "Swamp Troll": Enemy("Swamp Troll", 100, 15, 20, 45, random.randrange(40, 51), "medium"),
            "Mosquito Swarm": Enemy("Mosquito Swarm", 60, 18, 8, 35, random.randrange(30, 41), "medium"),
            "Bog Witch": Enemy("Bog Witch", 70, 22, 10, 50, random.randrange(45, 56), "medium"),
            
            #Temple
            "Stone Golem": Enemy("Stone Golem", 120, 15, 25, 55, random.randrange(50, 61), "medium"),
            "Cultist": Enemy("Cultist", 65, 20, 12, 40, random.randrange(35, 46), "medium"),
            "Mummy": Enemy("Mummy", 80, 18, 15, 45, random.randrange(40, 51), "medium"),
            "Animated Statue": Enemy("Animated Statue", 90, 17, 20, 50, random.randrange(45, 56), "medium"),
            "Temple Guardian": Enemy("Temple Guardian", 100, 20, 18, 55, random.randrange(50, 61), "medium"),
            
            #Mountain
            "Mountain Lion": Enemy("Mountain Lion", 70, 22, 10, 40, random.randrange(35, 46), "medium"),
            "Rock Elemental": Enemy("Rock Elemental", 110, 15, 25, 50, random.randrange(45, 56), "medium"),
            "Harpy": Enemy("Harpy", 65, 25, 8, 45, random.randrange(40, 51), "medium"),
            "Yeti": Enemy("Yeti", 95, 20, 15, 50, random.randrange(45, 56), "medium"),
            "Orc": Enemy("Orc", 80, 18, 12, 40, random.randrange(35, 46), "medium"),
            
            #Desert
            "Sand Wurm": Enemy("Sand Wurm", 85, 20, 15, 45, random.randrange(40, 51), "medium"),
            "Dried Mummy": Enemy("Dried Mummy", 75, 17, 18, 40, random.randrange(35, 46), "medium"),
            "Dust Devil": Enemy("Dust Devil", 60, 25, 10, 45, random.randrange(40, 51), "medium"),
            "Desert Bandit": Enemy("Desert Bandit", 70, 22, 12, 50, random.randrange(45, 56), "medium"),
            "Leopard": Enemy("Leopard", 65, 23, 8, 35, random.randrange(30, 41), "medium"),
            
            #Medium-Hard Enemies
            
            #Valley
            "Canyon Cougar": Enemy("Canyon Cougar", 100, 35, 15, 70, random.randrange(65, 81), "medium-hard"),
            "Twisted Mesquite": Enemy("Twisted Mesquite", 150, 25, 30, 75, random.randrange(70, 86), "medium-hard"),
            "Dust Devil": Enemy("Dust Devil", 130, 30, 25, 80, random.randrange(75, 91), "medium-hard"),
            "Petrified Warrior": Enemy("Petrified Warrior", 120, 28, 28, 85, random.randrange(80, 96), "medium-hard"),
            "Thunderbird": Enemy("Thunderbird", 140, 32, 22, 90, random.randrange(85, 101), "medium-hard"),
            
            #Hard Enemies
            
            #Toxic Swamp
            "Venomous Hydra": Enemy("Venomous Hydra", 200, 45, 35, 120, random.randrange(95, 116), "hard"),
            "Plague Bearer": Enemy("Plague Bearer", 180, 50, 30, 125, random.randrange(100, 121), "hard"),
            "Mire Leviathan": Enemy("Mire Leviathan", 250, 40, 40, 130, random.randrange(105, 126), "hard"),
            "Toxic Shambler": Enemy("Toxic Shambler", 170, 55, 25, 135, random.randrange(110, 131), "hard"),
            "Swamp Hag": Enemy("Swamp Hag", 190, 48, 32, 140, random.randrange(115, 136), "hard"),
            
            #Ruins
            "Ancient Golem": Enemy("Ancient Golem", 300, 35, 50, 120, random.randrange(120, 141), "hard"),
            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 220, 50, 35, 125, random.randrange(125, 146), "hard"),
            "Temporal Anomaly": Enemy("Temporal Anomaly", 180, 60, 30, 130, random.randrange(130, 151), "hard"),
            "Ruin Wraith": Enemy("Ruin Wraith", 200, 55, 35, 135, random.randrange(135, 156), "hard"),
            "Forgotten Titan": Enemy("Forgotten Titan", 280, 45, 45, 140, random.randrange(140, 161), "hard"),
            
            #Mountain Peaks
            "Frost Giant": Enemy("Frost Giant", 280, 50, 40, 100, random.randrange(145, 166), "hard"),
            "Storm Harpy": Enemy("Storm Harpy", 190, 65, 25, 105, random.randrange(150, 171), "hard"),
            "Avalanche Elemental": Enemy("Avalanche Elemental", 250, 45, 50, 110, random.randrange(155, 176), "hard"),
            "Mountain Wyvern": Enemy("Mountain Wyvern", 220, 60, 35, 115, random.randrange(160, 181), "hard"),
            "Yeti Alpha": Enemy("Yeti Alpha", 260, 55, 45, 120, random.randrange(165, 186), "hard"),
            
            #Scorching Plains
            "Fire Elemental": Enemy("Fire Elemental", 230, 70, 30, 100, random.randrange(170, 191), "hard"),
            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 210, 65, 35, 105, random.randrange(175, 196), "hard"),
            "Mirage Assassin": Enemy("Mirage Assassin", 200, 75, 25, 110, random.randrange(180, 201), "hard"),
            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 240, 60, 40, 115, random.randrange(185, 206), "hard"),
            "Desert Colossus": Enemy("Desert Colossus", 300, 55, 50, 120, random.randrange(190, 211), "hard"),
            
            #Shadowed Valley
            "Nightmare Stalker": Enemy("Nightmare Stalker", 220, 70, 35, 110, random.randrange(195, 216), "hard"),
            "Void Weaver": Enemy("Void Weaver", 200, 75, 30, 115, random.randrange(200, 221), "hard"),
            "Shadow Dragon": Enemy("Shadow Dragon", 280, 65, 45, 120, random.randrange(205, 226), "hard"),
            "Ethereal Banshee": Enemy("Ethereal Banshee", 190, 80, 25, 125, random.randrange(210, 231), "hard"),
            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 320, 60, 55, 130, random.randrange(215, 236), "hard"),
            
            #Very Hard Enemies
            
            #Death Caves
            "Necropolis Guardian": Enemy("Necropolis Guardian", 400, 85, 70, 300, random.randrange(240, 271), "very-hard"),
            "Soul Reaver": Enemy("Soul Reaver", 350, 100, 60, 325, random.randrange(250, 281), "very-hard"),
            "Bone Colossus": Enemy("Bone Colossus", 450, 80, 80, 350, random.randrange(260, 291), "very-hard"),
            "Spectral Devourer": Enemy("Spectral Devourer", 380, 95, 65, 375, random.randrange(270, 301), "very-hard"),
            "Lich King": Enemy("Lich King", 420, 90, 75, 400, random.randrange(280, 311), "very-hard"),
            
            #Ancient Ruins
            "Timeless Sphinx": Enemy("Timeless Sphinx", 430, 88, 78, 300, random.randrange(290, 321), "very-hard"),
            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 400, 95, 70, 325, random.randrange(300, 331), "very-hard"),
            "Anubis Reborn": Enemy("Anubis Reborn", 420, 92, 72, 350, random.randrange(310, 341), "very-hard"),
            "Mummy Emperor": Enemy("Mummy Emperor", 450, 85, 80, 375, random.randrange(320, 351), "very-hard"),
            "Living Obelisk": Enemy("Living Obelisk", 500, 80, 85, 400, random.randrange(330, 361), "very-hard"),
            
            #Death Valley
            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 440, 100, 70, 300, random.randrange(340, 371), "very-hard"),
            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 480, 90, 75, 325, random.randrange(350, 381), "very-hard"),
            "Void Titan": Enemy("Void Titan", 520, 85, 80, 350, random.randrange(360, 391), "very-hard"),
            "Chaos Incarnate": Enemy("Chaos Incarnate", 460, 95, 75, 375, random.randrange(370, 401), "very-hard"),
            "Eternity Warden": Enemy("Eternity Warden", 500, 92, 78, 400, random.randrange(380, 411), "very-hard"),
            
            #Dragon's Lair
            "Ancient Wyvern": Enemy("Ancient Wyvern", 480, 95, 75, 300, random.randrange(390, 421), "very-hard"),
            "Elemental Drake": Enemy("Elemental Drake", 460, 100, 70, 325, random.randrange(400, 431), "very-hard"),
            "Dragonlord": Enemy("Dragonlord", 500, 98, 77, 350, random.randrange(410, 441), "very-hard"),
            "Chromatic Dragon": Enemy("Chromatic Dragon", 520, 96, 79, 375, random.randrange(420, 451), "very-hard"),
            "Elder Dragon": Enemy("Elder Dragon", 550, 100, 80, 400, random.randrange(440, 471), "very-hard"),
            
            #Extreme Enemies
            
            #Volcanic Valley
            "Magma Colossus": Enemy("Magma Colossus", 800, 150, 120, 500, random.randrange(480, 531), "extreme"),
            "Phoenix Overlord": Enemy("Phoenix Overlord", 750, 180, 100, 520, random.randrange(500, 551), "extreme"),
            "Volcanic Titan": Enemy("Volcanic Titan", 900, 140, 140, 540, random.randrange(520, 571), "extreme"),
            "Inferno Wyrm": Enemy("Inferno Wyrm", 850, 160, 110, 560, random.randrange(540, 591), "extreme"),
            "Cinder Archfiend": Enemy("Cinder Archfiend", 780, 170, 130, 580, random.randrange(560, 611), "extreme"),
            
            #Boss Monsters
            
            #The Heavens
            "Seraphim Guardian": Enemy("Seraphim Guardian", 1200, 200, 180, 1000, random.randrange(950, 1051), "boss"),
            "Celestial Arbiter": Enemy("Celestial Arbiter", 1100, 220, 160, 1100, random.randrange(1050, 1151), "boss"),
            "Astral Demiurge": Enemy("Astral Demiurge", 1300, 190, 190, 1200, random.randrange(1150, 1251), "boss"),
            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1400, 210, 170, 1300, random.randrange(1250, 1351), "boss"),
            "Divine Architect": Enemy("Divine Architect", 1500, 230, 200, 1500, random.randrange(1450, 1551), "boss"),
    }