from player import Character
import random

class Enemy(Character):
    def __init__(self, name, hp, attack, defence, accuracy, evasion, crit_chance, crit_damage, armour_penetration, damage_reduction, block_chance, exp, gold, tier, level=0, attack_types=None):
        super().__init__(name, hp, attack, defence, accuracy, evasion, crit_chance, crit_damage, armour_penetration, damage_reduction, block_chance)
        self.exp = exp
        self.gold = gold
        self.tier = tier
        self.level = level
        self.stunned = False
        if attack_types:
            self.attack_types = {attack_type: ENEMY_ATTACK_TYPES[attack_type] for attack_type in attack_types}
        else:
            self.attack_types = {"normal": ENEMY_ATTACK_TYPES["normal"]}
        
        
    def choose_attack(self):
        if self.stunned:
            self.stunned = False
            return None
        return random.choice(list(self.attack_types.keys()))
        
    """ Effects to add
            "execute_low_health": f"The attack deals extra damage due to {player.name}'s low health!",
            "mana_drain": f"{player.name}'s energy is drained! They lose some stamina.",
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
            "Rat": Enemy("Rat", 21, 21, 5, 76, 12, 5, 118, 0, 0, 0, 10, random.randrange(3, 10), "low", 1, 
                        ["normal", "double", "poison", "double"]),

            "Boar": Enemy("Boar", 30, 24, 7, 71, 6, 7, 128, 2, 4, 0, 15, random.randrange(5, 15), "low", 2, 
                        ["normal", "power", "reckless", "stunning"]),

            "Plains Hawk": Enemy("Plains Hawk", 19, 26, 4, 84, 16, 8, 137, 1, 0, 0, 20, random.randrange(8, 18), "low", 1, 
                                ["normal", "double", "stunning", "triple"]),

            "Strider": Enemy("Strider", 34, 25, 8, 79, 13, 6, 123, 1, 2, 3, 25, random.randrange(10, 20), "low", 2, 
                            ["normal", "double", "power", "defence_break"]),

            "Bull": Enemy("Bull", 43, 27, 10, 69, 4, 5, 146, 3, 6, 0, 30, random.randrange(12, 24), "low", 3, 
                        ["normal", "power", "reckless", "stunning"]),

            "Bat": Enemy("Bat", 24, 23, 6, 81, 19, 7, 127, 0, 0, 0, 10, random.randrange(3, 10), "low", 1, 
                        ["normal", "double", "vampiric", "draining"]),

            "Goblin": Enemy("Goblin", 27, 25, 8, 74, 11, 6, 122, 1, 2, 3, 15, random.randrange(5, 15), "low", 2, 
                            ["normal", "double", "poison", "stunning"]),

            "Spider": Enemy("Spider", 22, 26, 5, 83, 14, 8, 132, 1, 0, 0, 20, random.randrange(8, 18), "low", 1, 
                            ["normal", "double", "poison", "attack_weaken"]),

            "Slime": Enemy("Slime", 38, 22, 9, 68, 7, 3, 109, 0, 6, 0, 25, random.randrange(10, 20), "low", 2, 
                        ["normal", "poison", "stunning", "draining"]),

            "Frog": Enemy("Frog", 36, 26, 8, 73, 17, 5, 119, 0, 3, 0, 30, random.randrange(12, 24), "low", 3, 
                        ["normal", "double", "poison", "stunning"]),

            "Tree Sprite": Enemy("Tree Sprite", 20, 24, 6, 78, 13, 6, 121, 0, 2, 2, 10, random.randrange(3, 10), "low", 1, 
                                ["normal", "double", "draining", "stunning"]),

            "Snake": Enemy("Snake", 24, 27, 5, 82, 18, 7, 136, 2, 0, 0, 15, random.randrange(5, 15), "low", 1, 
                        ["normal", "double", "poison", "double"]),

            "Forest Hawk": Enemy("Forest Hawk", 29, 25, 7, 87, 21, 8, 141, 1, 0, 0, 20, random.randrange(8, 18), "low", 2, 
                                ["normal", "double", "stunning", "triple"]),

            "Locust": Enemy("Locust", 26, 26, 6, 80, 16, 6, 126, 1, 1, 0, 25, random.randrange(10, 20), "low", 2, 
                            ["normal", "double", "poison", "triple"]),

            "Leprechaun": Enemy("Leprechaun", 41, 23, 9, 85, 24, 10, 147, 0, 0, 5, 30, random.randrange(12, 24), "low", 3, 
                                ["normal", "double", "stunning", "draining"]),

            "Wood Spirit": Enemy("Wood Spirit", 26, 24, 7, 77, 11, 5, 117, 0, 3, 3, 10, random.randrange(3, 10), "low", 1, 
                                ["normal", "draining", "stunning", "double"]),

            "Deepwood Stalker": Enemy("Deepwood Stalker", 32, 26, 9, 83, 15, 7, 131, 2, 2, 0, 15, random.randrange(5, 15), "low", 2, 
                                    ["normal", "double", "poison", "attack_weaken"]),

            "Deep Bat": Enemy("Deep Bat", 27, 27, 7, 79, 20, 8, 135, 1, 0, 0, 20, random.randrange(8, 18), "low", 2, 
                            ["normal", "double", "vampiric", "draining"]),

            "Giant Firefly": Enemy("Giant Firefly", 34, 24, 8, 86, 19, 6, 124, 0, 1, 0, 25, random.randrange(10, 20), "low", 2, 
                                ["normal", "double", "poison", "burn"]),

            "Treant": Enemy("Treant", 51, 25, 12, 67, 2, 3, 116, 0, 6, 4, 30, random.randrange(12, 24), "low", 3, 
                            ["normal", "power", "stunning", "draining"]),
            
            # Medium Enemies (Levels 5-9)
            "Alligator": Enemy("Alligator", 77, 43, 30, 74, 6, 6, 142, 5, 8, 7, 35, random.randrange(30, 41), "medium", 5, 
                            ["normal", "power", "reckless", "stunning"]),

            "Poison Frog": Enemy("Poison Frog", 60, 45, 28, 81, 16, 8, 131, 2, 3, 0, 40, random.randrange(35, 46), "medium", 4, 
                                ["normal", "double", "poison", "defence_break"]),

            "Swamp Troll": Enemy("Swamp Troll", 89, 44, 32, 69, 4, 5, 148, 3, 10, 4, 45, random.randrange(40, 51), "medium", 6, 
                                ["normal", "power", "poison", "damage_reflect"]),

            "Mosquito Swarm": Enemy("Mosquito Swarm", 64, 47, 26, 92, 27, 10, 118, 0, 0, 0, 35, random.randrange(30, 41), "medium", 4, 
                                    ["normal", "triple", "poison", "draining"]),

            "Bog Witch": Enemy("Bog Witch", 72, 43, 29, 83, 11, 7, 136, 2, 4, 0, 50, random.randrange(45, 56), "medium", 5, 
                            ["normal", "poison", "burn", "draining"]),

            "Stone Golem": Enemy("Stone Golem", 102, 42, 34, 66, 1, 3, 157, 5, 10, 9, 55, random.randrange(50, 61), "medium", 6, 
                                ["normal", "power", "stunning", "defence_break"]),

            "Cultist": Enemy("Cultist", 68, 46, 28, 79, 13, 8, 139, 3, 2, 3, 40, random.randrange(35, 46), "medium", 4, 
                            ["normal", "burn", "poison", "attack_weaken"]),

            "Mummy": Enemy("Mummy", 81, 44, 31, 73, 7, 6, 132, 2, 7, 6, 45, random.randrange(40, 51), "medium", 5, 
                        ["normal", "draining", "stunning", "poison"]),

            "Animated Statue": Enemy("Animated Statue", 85, 43, 32, 71, 2, 4, 143, 4, 9, 8, 50, random.randrange(45, 56), "medium", 5, 
                                    ["normal", "power", "stunning", "damage_reflect"]),

            "Temple Guardian": Enemy("Temple Guardian", 94, 43, 33, 76, 5, 5, 141, 3, 8, 10, 55, random.randrange(50, 61), "medium", 6, 
                                    ["normal", "power", "stunning", "defence_break"]),

            "Mountain Lion": Enemy("Mountain Lion", 72, 48, 29, 86, 19, 10, 151, 3, 2, 0, 40, random.randrange(35, 46), "medium", 4, 
                                ["normal", "double", "reckless", "power"]),

            "Rock Elemental": Enemy("Rock Elemental", 98, 41, 35, 64, 1, 3, 154, 5, 10, 8, 50, random.randrange(45, 56), "medium", 6, 
                                    ["normal", "power", "stunning", "damage_reflect"]),

            "Harpy": Enemy("Harpy", 68, 48, 27, 89, 21, 9, 138, 2, 0, 0, 45, random.randrange(40, 51), "medium", 4, 
                        ["normal", "double", "stunning", "triple"]),

            "Yeti": Enemy("Yeti", 89, 45, 33, 72, 6, 6, 146, 4, 7, 5, 50, random.randrange(45, 56), "medium", 6, 
                        ["normal", "power", "reckless", "freeze"]),

            "Orc": Enemy("Orc", 81, 46, 30, 74, 9, 7, 137, 3, 6, 4, 40, random.randrange(35, 46), "medium", 5, 
                        ["normal", "power", "reckless", "stunning"]),

            "Sand Wurm": Enemy("Sand Wurm", 94, 44, 34, 68, 4, 5, 149, 5, 9, 6, 45, random.randrange(40, 51), "medium", 6, 
                            ["normal", "power", "poison", "stunning"]),

            "Dried Mummy": Enemy("Dried Mummy", 85, 43, 31, 72, 7, 6, 133, 2, 8, 5, 40, random.randrange(35, 46), "medium", 5, 
                                ["normal", "draining", "poison", "burn"]),

            "Dust Devil": Enemy("Dust Devil", 64, 49, 28, 87, 23, 8, 129, 1, 2, 0, 45, random.randrange(40, 51), "medium", 4, 
                                ["normal", "double", "attack_weaken", "triple"]),

            "Desert Bandit": Enemy("Desert Bandit", 77, 47, 30, 82, 17, 9, 141, 3, 3, 2, 50, random.randrange(45, 56), "medium", 5, 
                                ["normal", "double", "poison", "defence_break"]),

            "Leopard": Enemy("Leopard", 68, 40, 27, 91, 22, 12, 158, 2, 0, 0, 35, random.randrange(30, 41), "medium", 3, 
                            ["normal", "double", "reckless", "triple"]),
            
            # Medium-Hard Enemies (Levels 10-14)
            "Canyon Cougar": Enemy("Canyon Cougar", 111, 60, 50, 87, 22, 11, 152, 4, 3, 0, 70, random.randrange(65, 81), "medium-hard", 10, 
                                ["normal", "double", "reckless", "power", "stunning"]),

            "Twisted Mesquite": Enemy("Twisted Mesquite", 136, 57, 52, 78, 8, 7, 138, 2, 11, 6, 75, random.randrange(70, 86), "medium-hard", 12, 
                                    ["normal", "poison", "stunning", "draining", "damage_reflect"]),

            "Dustier Devil": Enemy("Dustier Devil", 123, 61, 49, 92, 26, 9, 143, 3, 2, 0, 80, random.randrange(75, 91), "medium-hard", 11, 
                                ["normal", "double", "stunning", "triple", "draining"]),

            "Petrified Warrior": Enemy("Petrified Warrior", 119, 60, 48, 81, 5, 8, 147, 5, 13, 9, 85, random.randrange(80, 96), "medium-hard", 10, 
                                    ["normal", "power", "stunning", "defence_break", "damage_reflect"]),

            "Thunderbird": Enemy("Thunderbird", 132, 63, 49, 93, 24, 12, 155, 3, 1, 0, 90, random.randrange(85, 101), "medium-hard", 11, 
                                ["normal", "double", "stunning", "triple", "attack_weaken"]),
            
            # Hard Enemies (Levels 15-19)
            "Venomous Hydra": Enemy("Venomous Hydra", 170, 78, 87, 86, 13, 10, 158, 7, 12, 5, 120, random.randrange(95, 116), "hard", 15, 
                                    ["normal", "power", "poison", "double", "triple"]),

            "Plague Bearer": Enemy("Plague Bearer", 162, 81, 84, 89, 11, 12, 163, 5, 15, 3, 125, random.randrange(100, 121), "hard", 16, 
                                ["normal", "poison", "vampiric", "draining", "attack_weaken"]),

            "Mire Leviathan": Enemy("Mire Leviathan", 204, 83, 86, 82, 8, 9, 167, 8, 18, 7, 130, random.randrange(105, 126), "hard", 17, 
                                    ["normal", "power", "stunning", "poison", "defence_break"]),

            "Toxic Shambler": Enemy("Toxic Shambler", 153, 87, 82, 88, 15, 13, 170, 6, 14, 2, 135, random.randrange(110, 131), "hard", 18, 
                                    ["normal", "poison", "vampiric", "draining", "double"]),

            "Swamp Hag": Enemy("Swamp Hag", 166, 89, 80, 91, 18, 14, 172, 4, 11, 0, 140, random.randrange(115, 136), "hard", 19, 
                            ["normal", "poison", "stunning", "draining", "attack_weaken"]),

            "Ancient Golem": Enemy("Ancient Golem", 230, 75, 90, 79, 5, 7, 165, 9, 18, 10, 120, random.randrange(120, 141), "hard", 15, 
                                ["normal", "power", "stunning", "damage_reflect", "defence_break"]),

            "Cursed Pharaoh": Enemy("Cursed Pharaoh", 187, 79, 86, 87, 12, 11, 168, 6, 16, 6, 125, random.randrange(125, 146), "hard", 16, 
                                    ["normal", "poison", "stunning", "draining", "attack_weaken"]),

            "Temporal Anomaly": Enemy("Temporal Anomaly", 170, 84, 83, 93, 22, 15, 175, 5, 8, 0, 130, random.randrange(130, 151), "hard", 17, 
                                    ["normal", "double", "stunning", "defence_break", "attack_weaken"]),

            "Ruin Wraith": Enemy("Ruin Wraith", 179, 86, 81, 90, 20, 13, 171, 7, 10, 0, 135, random.randrange(135, 156), "hard", 18, 
                                ["normal", "draining", "vampiric", "stunning", "attack_weaken"]),

            "Forgotten Titan": Enemy("Forgotten Titan", 221, 88, 85, 84, 7, 8, 169, 10, 17, 8, 140, random.randrange(140, 161), "hard", 19, 
                                    ["normal", "power", "reckless", "stunning", "defence_break"]),

            "Frost Giant": Enemy("Frost Giant", 221, 76, 89, 81, 6, 9, 166, 8, 18, 9, 100, random.randrange(145, 166), "hard", 15, 
                                ["normal", "power", "stunning", "freeze", "defence_break"]),

            "Storm Harpy": Enemy("Storm Harpy", 170, 83, 82, 94, 23, 14, 173, 5, 7, 0, 105, random.randrange(150, 171), "hard", 16, 
                                ["normal", "double", "stunning", "triple", "attack_weaken"]),

            "Avalanche Elemental": Enemy("Avalanche Elemental", 204, 85, 84, 83, 9, 10, 168, 7, 17, 7, 110, random.randrange(155, 176), "hard", 17, 
                                        ["normal", "power", "freeze", "stunning", "damage_reflect"]),

            "Mountain Wyvern": Enemy("Mountain Wyvern", 187, 88, 79, 92, 19, 13, 174, 6, 11, 3, 115, random.randrange(160, 181), "hard", 18, 
                                    ["normal", "double", "reckless", "stunning", "poison"]),

            "Yeti Alpha": Enemy("Yeti Alpha", 213, 90, 81, 85, 10, 11, 170, 8, 16, 6, 120, random.randrange(165, 186), "hard", 19, 
                                ["normal", "power", "reckless", "freeze", "stunning"]),

            "Fire Elemental": Enemy("Fire Elemental", 196, 77, 88, 88, 14, 12, 171, 7, 15, 0, 100, random.randrange(170, 191), "hard", 15, 
                                    ["normal", "power", "reckless", "burn", "stunning"]),

            "Sandstorm Djinn": Enemy("Sandstorm Djinn", 179, 82, 83, 91, 21, 13, 169, 5, 9, 0, 105, random.randrange(175, 196), "hard", 16, 
                                    ["normal", "double", "stunning", "damage_reflect", "attack_weaken"]),

            "Mirage Assassin": Enemy("Mirage Assassin", 170, 86, 80, 95, 24, 15, 176, 6, 6, 0, 110, random.randrange(180, 201), "hard", 17, 
                                    ["normal", "double", "poison", "triple", "stunning"]),

            "Sunburst Phoenix": Enemy("Sunburst Phoenix", 196, 89, 78, 93, 18, 14, 175, 7, 13, 0, 115, random.randrange(185, 206), "hard", 18, 
                                    ["normal", "power", "reckless", "burn", "stunning"]),

            "Desert Colossus": Enemy("Desert Colossus", 230, 91, 76, 80, 4, 8, 167, 9, 18, 8, 120, random.randrange(190, 211), "hard", 19, 
                                    ["normal", "power", "stunning", "defence_break", "damage_reflect"]),

            "Nightmare Stalker": Enemy("Nightmare Stalker", 187, 80, 85, 92, 20, 14, 172, 6, 12, 0, 110, random.randrange(195, 216), "hard", 15, 
                                    ["normal", "double", "vampiric", "stunning", "attack_weaken"]),

            "Void Weaver": Enemy("Void Weaver", 179, 84, 81, 90, 19, 13, 170, 7, 14, 0, 115, random.randrange(200, 221), "hard", 16, 
                                ["normal", "draining", "stunning", "attack_weaken", "poison"]),

            "Shadow Dragon": Enemy("Shadow Dragon", 221, 87, 82, 89, 16, 12, 173, 8, 16, 5, 120, random.randrange(205, 226), "hard", 17, 
                                ["normal", "power", "triple", "stunning", "draining"]),

            "Ethereal Banshee": Enemy("Ethereal Banshee", 170, 90, 77, 94, 22, 15, 177, 5, 8, 0, 125, random.randrange(210, 231), "hard", 18, 
                                    ["normal", "draining", "stunning", "attack_weaken", "double"]),

            "Abyssal Behemoth": Enemy("Abyssal Behemoth", 238, 91, 79, 83, 6, 9, 168, 10, 18, 7, 130, random.randrange(215, 236), "hard", 19, 
                                    ["normal", "power", "reckless", "stunning", "defence_break"]),
            
            # Very Hard Enemies (Levels 20-24) - 6 attacks each
            "Necropolis Guardian": Enemy("Necropolis Guardian", 323, 106, 93, 88, 9, 11, 175, 12, 22, 15, 300, random.randrange(240, 271), "very-hard", 20, 
                                        ["normal", "power", "stunning", "draining", "defence_break", "damage_reflect"]),

            "Soul Reaver": Enemy("Soul Reaver", 298, 112, 88, 95, 18, 14, 182, 10, 15, 5, 325, random.randrange(250, 281), "very-hard", 21, 
                                ["normal", "triple", "vampiric", "draining", "stunning", "attack_weaken"]),

            "Bone Colossus": Enemy("Bone Colossus", 357, 117, 90, 85, 7, 10, 178, 14, 20, 12, 350, random.randrange(260, 291), "very-hard", 22, 
                                ["normal", "power", "stunning", "reckless", "defence_break", "damage_reflect"]),

            "Spectral Devourer": Enemy("Spectral Devourer", 315, 122, 84, 93, 20, 15, 185, 11, 14, 0, 375, random.randrange(270, 301), "very-hard", 23, 
                                    ["normal", "vampiric", "poison", "draining", "stunning", "attack_weaken"]),

            "Lich King": Enemy("Lich King", 340, 125, 87, 91, 13, 13, 180, 13, 18, 8, 400, random.randrange(280, 311), "very-hard", 24, 
                            ["normal", "draining", "poison", "freeze", "stunning", "attack_weaken"]),

            "Timeless Sphinx": Enemy("Timeless Sphinx", 340, 104, 95, 94, 16, 12, 177, 9, 19, 10, 300, random.randrange(290, 321), "very-hard", 20, 
                                    ["normal", "stunning", "draining", "poison", "attack_weaken", "damage_reflect"]),

            "Eternal Pharaoh": Enemy("Eternal Pharaoh", 323, 110, 90, 92, 14, 13, 179, 11, 21, 11, 325, random.randrange(300, 331), "very-hard", 21, 
                                    ["normal", "power", "poison", "draining", "stunning", "defence_break"]),

            "Anubis Reborn": Enemy("Anubis Reborn", 340, 115, 92, 93, 17, 14, 181, 12, 20, 9, 350, random.randrange(310, 341), "very-hard", 22, 
                                ["normal", "vampiric", "stunning", "double", "triple", "defence_break"]),

            "Mummy Emperor": Enemy("Mummy Emperor", 357, 120, 86, 90, 12, 12, 176, 13, 22, 13, 375, random.randrange(320, 351), "very-hard", 23, 
                                ["normal", "draining", "poison", "stunning", "defence_break", "damage_reflect"]),

            "Living Obelisk": Enemy("Living Obelisk", 383, 124, 89, 87, 8, 11, 174, 15, 22, 14, 400, random.randrange(330, 361), "very-hard", 24, 
                                    ["normal", "power", "stunning", "reckless", "defence_break", "damage_reflect"]),

            "Apocalypse Horseman": Enemy("Apocalypse Horseman", 340, 114, 91, 94, 19, 15, 183, 12, 17, 7, 350, random.randrange(310, 341), "very-hard", 22, 
                                        ["normal", "reckless", "poison", "draining", "stunning", "attack_weaken"]),

            "Abyssal Wyrm": Enemy("Abyssal Wyrm", 357, 119, 85, 92, 15, 14, 180, 14, 19, 8, 375, random.randrange(320, 351), "very-hard", 23, 
                                ["normal", "power", "poison", "stunning", "defence_break", "reckless"]),

            "Void Titan": Enemy("Void Titan", 383, 123, 88, 89, 10, 13, 178, 15, 21, 11, 400, random.randrange(330, 361), "very-hard", 24, 
                                ["normal", "reckless", "stunning", "draining", "defence_break", "damage_reflect"]),

            "Chaos Incarnate": Enemy("Chaos Incarnate", 366, 121, 83, 96, 22, 16, 186, 13, 16, 0, 425, random.randrange(340, 371), "very-hard", 23, 
                                    ["normal", "double", "poison", "vampiric", "stunning", "attack_weaken"]),

            "Eternity Warden": Enemy("Eternity Warden", 400, 125, 86, 91, 13, 14, 181, 14, 20, 12, 450, random.randrange(350, 381), "very-hard", 24, 
                                    ["normal", "power", "stunning", "freeze", "defence_break", "damage_reflect"]),

            "Ancient Wyvern": Enemy("Ancient Wyvern", 349, 111, 89, 93, 18, 15, 182, 13, 18, 6, 300, random.randrange(390, 421), "very-hard", 21, 
                                    ["normal", "triple", "poison", "reckless", "stunning", "attack_weaken"]),

            "Elemental Drake": Enemy("Elemental Drake", 340, 108, 92, 92, 16, 14, 179, 12, 19, 9, 325, random.randrange(400, 431), "very-hard", 20, 
                                    ["normal", "burn", "poison", "freeze", "stunning", "defence_break"]),

            "Dragonlord": Enemy("Dragonlord", 366, 116, 91, 94, 17, 15, 183, 14, 20, 10, 350, random.randrange(410, 441), "very-hard", 22, 
                                ["normal", "power", "reckless", "stunning", "poison", "damage_reflect"]),

            "Chromatic Dragon": Enemy("Chromatic Dragon", 374, 121, 85, 95, 19, 16, 184, 13, 18, 7, 375, random.randrange(420, 451), "very-hard", 23, 
                                    ["normal", "burn", "poison", "freeze", "stunning", "attack_weaken"]),

            "Elder Dragon": Enemy("Elder Dragon", 391, 124, 88, 93, 15, 15, 182, 15, 21, 11, 400, random.randrange(440, 471), "very-hard", 24, 
                                ["normal", "power", "stunning", "draining", "defence_break", "damage_reflect"]),
            
            # Extreme Enemies (Levels 25+) - 7 attacks each
            "Magma Colossus": Enemy("Magma Colossus", 589, 115, 118, 88, 6, 13, 185, 18, 25, 15, 500, random.randrange(480, 531), "extreme", 25, 
                                    ["normal", "power", "reckless", "stunning", "draining", "burn", "damage_reflect"]),

            "Phoenix Overlord": Enemy("Phoenix Overlord", 557, 122, 115, 96, 22, 17, 190, 16, 18, 8, 520, random.randrange(500, 551), "extreme", 26, 
                                    ["normal", "double", "stunning", "triple", "reckless", "burn", "attack_weaken"]),

            "Volcanic Titan": Enemy("Volcanic Titan", 655, 117, 122, 90, 8, 14, 188, 19, 24, 14, 540, random.randrange(520, 571), "extreme", 27, 
                                    ["normal", "power", "reckless", "stunning", "draining", "burn", "defence_break"]),

            "Inferno Wyrm": Enemy("Inferno Wyrm", 622, 121, 116, 94, 18, 16, 192, 17, 20, 10, 560, random.randrange(540, 591), "extreme", 28, 
                                ["normal", "double", "triple", "reckless", "stunning", "burn", "attack_weaken"]),

            "Cinder Archfiend": Enemy("Cinder Archfiend", 576, 126, 111, 93, 15, 18, 195, 18, 22, 12, 580, random.randrange(560, 611), "extreme", 29, 
                                    ["normal", "power", "poison", "vampiric", "draining", "burn", "defence_break"]),

            "Cosmic Devourer": Enemy("Cosmic Devourer", 610, 128, 120, 95, 20, 19, 198, 20, 23, 11, 600, random.randrange(580, 631), "extreme", 30, 
                                    ["normal", "double", "stunning", "draining", "reckless", "poison", "attack_weaken"]),

            "Astral Behemoth": Enemy("Astral Behemoth", 643, 130, 125, 92, 12, 15, 193, 21, 25, 13, 620, random.randrange(600, 651), "extreme", 31, 
                                    ["normal", "power", "defence_break", "stunning", "vampiric", "damage_reflect", "reckless"]),

            "Galactic Leviathan": Enemy("Galactic Leviathan", 678, 133, 128, 91, 10, 16, 196, 22, 24, 14, 640, random.randrange(620, 671), "extreme", 32, 
                                        ["normal", "power", "poison", "stunning", "draining", "defence_break", "attack_weaken"]),

            "Nebula Colossus": Enemy("Nebula Colossus", 712, 136, 131, 89, 8, 14, 191, 23, 25, 15, 660, random.randrange(640, 691), "extreme", 33, 
                                    ["normal", "power", "reckless", "stunning", "vampiric", "damage_reflect", "defence_break"]),

            "Celestial Titan": Enemy("Celestial Titan", 745, 139, 134, 93, 14, 17, 197, 24, 23, 13, 680, random.randrange(660, 711), "extreme", 34, 
                                    ["normal", "double", "stunning", "vampiric", "draining", "attack_weaken", "defence_break"]),
            
            # Boss Monsters - 7 attacks each
            "Seraphim Guardian": Enemy("Seraphim Guardian", 916, 131, 137, 97, 15, 18, 200, 25, 28, 20, 1000, random.randrange(950, 1051), "boss", 35, 
                                    ["normal", "power", "stunning", "draining", "reckless", "freeze", "damage_reflect"]),

            "Celestial Arbiter": Enemy("Celestial Arbiter", 851, 141, 128, 99, 20, 20, 210, 22, 25, 15, 1100, random.randrange(1050, 1151), "boss", 36, 
                                    ["normal", "double", "draining", "stunning", "triple", "vampiric", "attack_weaken"]),

            "Astral Demiurge": Enemy("Astral Demiurge", 982, 134, 136, 98, 18, 19, 205, 24, 27, 18, 1200, random.randrange(1150, 1251), "boss", 37, 
                                    ["normal", "power", "poison", "freeze", "stunning", "vampiric", "defence_break"]),

            "Ethereal Leviathan": Enemy("Ethereal Leviathan", 1047, 145, 126, 96, 22, 21, 215, 26, 24, 12, 1300, random.randrange(1250, 1351), "boss", 38, 
                                        ["normal", "reckless", "draining", "double", "poison", "triple", "damage_reflect"]),

            "Divine Architect": Enemy("Divine Architect", 1113, 138, 132, 95, 17, 17, 208, 28, 30, 22, 1500, random.randrange(1450, 1551), "boss", 39, 
                                    ["normal", "power", "stunning", "freeze", "draining", "reckless", "defence_break"])
    }
    
ENEMY_ATTACK_TYPES = {
    "normal": {"name": "Normal Attack", "damage_modifier": 1, "effect": None},
    "power": {"name": "Power Attack", "damage_modifier": 1.5, "effect": None},
    "double": {"name": "Double Strike", "damage_modifier": 0.8, "effect": None, "extra_attacks": 1},
    "triple": {"name": "Triple Strike", "damage_modifier": 0.8, "extra_attacks": 2},
    "vampiric": {"name": "Vampiric Strike", "damage_modifier": 0.9, "effect": "lifesteal"},
    "reckless": {"name": "Reckless Assault", "damage_modifier": 2},
    "draining": {"name": "Draining Touch", "damage_modifier": 0.9, "effect": "stamina_drain"},
    "stunning": {"name": "Stunning Blow", "damage_modifier": 0.7, "effect": "stun"},
    "confusion": {"name": "Confounding Blow", "damage_modifier": 0.8, "effect": "confusion"},
    "poison": {"name": "Poison Strike", "damage_modifier": 0.9, "effect": "poison"},
    "freeze": {"name": "Frozen Strike", "damage_modifier": 0.9, "effect": "freeze"},
    "burn": {"name": "Burning Strike", "damage_modifier": 0.9, "effect": "burn"},
    "damage_reflect": {"name": "Reflective Shield", "damage_modifier": 0.5, "effect": "damage_reflect"},
    "defence_break": {"name": "Defence Shatter", "damage_modifier": 0.7, "effect": "defence_break"},
    "attack_weaken": {"name": "Attack Weaken", "damage_modifier": 0.7, "effect": "attack_weaken"}
}