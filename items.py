class Item:
    def __init__(self, name, item_type, value, tier,
                 attack=0, defence=0, accuracy=0, crit_chance=0, crit_damage=0, armour_penetration=0, damage_reduction=0, evasion=0, block_chance=0,
                 effect_type=None, effect=0, cooldown=0, duration=0, tick_effect=0,
                 weapon_type=None, stamina_restore=0, combat_only=False):
        self.name = name
        self.type = item_type
        self.value = value
        self.tier = tier
        self.attack = attack
        self.defence = defence
        self.accuracy = accuracy
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage
        self.armour_penetration = armour_penetration
        self.damage_reduction = damage_reduction
        self.evasion = evasion
        self.block_chance = block_chance
        self.effect_type = effect_type
        self.effect = effect
        self.cooldown = cooldown
        self.duration = duration
        self.tick_effect = tick_effect
        self.weapon_type = weapon_type
        self.stamina_restore = stamina_restore
        self.combat_only = combat_only
        
def initialise_items():
    return {
        # Starter items
        "Peasants Top": Item("Peasants Top", "chest", 0, "starter", defence=1),
        "Peasants Bottoms": Item("Peasants Bottoms", "legs", 0, "starter", defence=1),
        "Wooden Sword": Item("Wooden Sword", "weapon", 0, "starter", attack=5, accuracy=20, crit_chance=2, crit_damage=120, armour_penetration=0, weapon_type="light"),

        # Common (Bronze) Weapons level 1-3
        "Bronze Dagger": Item("Bronze Dagger", "weapon", 20, "common", attack=10, accuracy=23, crit_chance=5, crit_damage=130, armour_penetration=3, weapon_type="light"),
        "Bronze Shortsword": Item("Bronze Shortsword", "weapon", 25, "common", attack=12, accuracy=22, crit_chance=4, crit_damage=125, armour_penetration=1, weapon_type="light"),
        "Bronze Sword": Item("Bronze Sword", "weapon", 30, "common", attack=14, accuracy=20, crit_chance=3, crit_damage=130, armour_penetration=1, weapon_type="medium"),
        "Bronze Axe": Item("Bronze Axe", "weapon", 35, "common", attack=16, accuracy=18, crit_chance=3, crit_damage=140, armour_penetration=2, weapon_type="medium"),
        "Bronze Longsword": Item("Bronze Longsword", "weapon", 40, "common", attack=18, accuracy=17, crit_chance=2, crit_damage=135, armour_penetration=1, weapon_type="heavy"),
        "Bronze Mace": Item("Bronze Mace", "weapon", 45, "common", attack=20, accuracy=15, crit_chance=2, crit_damage=140, armour_penetration=3, weapon_type="heavy"),

        # Uncommon (Iron) Weapons level 4-6
        "Iron Dagger": Item("Iron Dagger", "weapon", 80, "uncommon", attack=23, accuracy=24, crit_chance=6, crit_damage=135, armour_penetration=4, weapon_type="light"),
        "Iron Shortsword": Item("Iron Shortsword", "weapon", 90, "uncommon", attack=25, accuracy=23, crit_chance=5, crit_damage=130, armour_penetration=2, weapon_type="light"),
        "Iron Sword": Item("Iron Sword", "weapon", 100, "uncommon", attack=27, accuracy=22, crit_chance=4, crit_damage=135, armour_penetration=2, weapon_type="medium"),
        "Iron Axe": Item("Iron Axe", "weapon", 110, "uncommon", attack=29, accuracy=19, crit_chance=4, crit_damage=145, armour_penetration=3, weapon_type="medium"),
        "Iron Longsword": Item("Iron Longsword", "weapon", 120, "uncommon", attack=31, accuracy=18, crit_chance=3, crit_damage=140, armour_penetration=2, weapon_type="heavy"),
        "Iron Mace": Item("Iron Mace", "weapon", 130, "uncommon", attack=33, accuracy=17, crit_chance=3, crit_damage=145, armour_penetration=4, weapon_type="heavy"),

        # Rare (Steel) Weapons level 7-10
        "Steel Dagger": Item("Steel Dagger", "weapon", 200, "rare", attack=36, accuracy=26, crit_chance=7, crit_damage=140, armour_penetration=5, weapon_type="light"),
        "Steel Shortsword": Item("Steel Shortsword", "weapon", 220, "rare", attack=38, accuracy=25, crit_chance=6, crit_damage=135, armour_penetration=3, weapon_type="light"),
        "Steel Sword": Item("Steel Sword", "weapon", 240, "rare", attack=40, accuracy=23, crit_chance=5, crit_damage=140, armour_penetration=3, weapon_type="medium"),
        "Steel Axe": Item("Steel Axe", "weapon", 260, "rare", attack=42, accuracy=21, crit_chance=5, crit_damage=150, armour_penetration=4, weapon_type="medium"),
        "Steel Longsword": Item("Steel Longsword", "weapon", 280, "rare", attack=44, accuracy=20, crit_chance=4, crit_damage=145, armour_penetration=3, weapon_type="heavy"),
        "Steel Mace": Item("Steel Mace", "weapon", 300, "rare", attack=46, accuracy=18, crit_chance=4, crit_damage=150, armour_penetration=5, weapon_type="heavy"),

        # Epic (Mithril) Weapons level 11-14
        "Mithril Dagger": Item("Mithril Dagger", "weapon", 500, "epic", attack=49, accuracy=27, crit_chance=8, crit_damage=145, armour_penetration=6, weapon_type="light"),
        "Mithril Shortsword": Item("Mithril Shortsword", "weapon", 550, "epic", attack=51, accuracy=26, crit_chance=7, crit_damage=140, armour_penetration=4, weapon_type="light"),
        "Mithril Sword": Item("Mithril Sword", "weapon", 600, "epic", attack=53, accuracy=25, crit_chance=6, crit_damage=145, armour_penetration=4, weapon_type="medium"),
        "Mithril Axe": Item("Mithril Axe", "weapon", 650, "epic", attack=55, accuracy=22, crit_chance=6, crit_damage=155, armour_penetration=5, weapon_type="medium"),
        "Mithril Longsword": Item("Mithril Longsword", "weapon", 700, "epic", attack=57, accuracy=21, crit_chance=5, crit_damage=150, armour_penetration=4, weapon_type="heavy"),
        "Mithril Mace": Item("Mithril Mace", "weapon", 750, "epic", attack=59, accuracy=20, crit_chance=5, crit_damage=155, armour_penetration=6, weapon_type="heavy"),

        # Masterwork (Aluthril) Weapons level 15-19
        "Aluthril Dagger": Item("Aluthril Dagger", "weapon", 1000, "masterwork", attack=62, accuracy=29, crit_chance=9, crit_damage=150, armour_penetration=7, weapon_type="light"),
        "Aluthril Shortsword": Item("Aluthril Shortsword", "weapon", 1100, "masterwork", attack=64, accuracy=28, crit_chance=8, crit_damage=145, armour_penetration=5, weapon_type="light"),
        "Aluthril Sword": Item("Aluthril Sword", "weapon", 1200, "masterwork", attack=66, accuracy=26, crit_chance=7, crit_damage=150, armour_penetration=5, weapon_type="medium"),
        "Aluthril Axe": Item("Aluthril Axe", "weapon", 1300, "masterwork", attack=68, accuracy=24, crit_chance=7, crit_damage=160, armour_penetration=6, weapon_type="medium"),
        "Aluthril Longsword": Item("Aluthril Longsword", "weapon", 1400, "masterwork", attack=70, accuracy=23, crit_chance=6, crit_damage=155, armour_penetration=5, weapon_type="heavy"),
        "Aluthril Mace": Item("Aluthril Mace", "weapon", 1500, "masterwork", attack=72, accuracy=21, crit_chance=6, crit_damage=160, armour_penetration=7, weapon_type="heavy"),

        # Legendary (Adamantite) Weapons level 20-24
        "Adamantite Dagger": Item("Adamantite Dagger", "weapon", 2000, "legendary", attack=75, accuracy=30, crit_chance=10, crit_damage=155, armour_penetration=8, weapon_type="light"),
        "Adamantite Shortsword": Item("Adamantite Shortsword", "weapon", 2200, "legendary", attack=77, accuracy=29, crit_chance=9, crit_damage=150, armour_penetration=6, weapon_type="light"),
        "Adamantite Sword": Item("Adamantite Sword", "weapon", 2400, "legendary", attack=79, accuracy=28, crit_chance=8, crit_damage=155, armour_penetration=6, weapon_type="medium"),
        "Adamantite Axe": Item("Adamantite Axe", "weapon", 2600, "legendary", attack=81, accuracy=25, crit_chance=8, crit_damage=165, armour_penetration=7, weapon_type="medium"),
        "Adamantite Longsword": Item("Adamantite Longsword", "weapon", 2800, "legendary", attack=83, accuracy=24, crit_chance=7, crit_damage=160, armour_penetration=6, weapon_type="heavy"),
        "Adamantite Warhammer": Item("Adamantite Warhammer", "weapon", 3000, "legendary", attack=85, accuracy=23, crit_chance=7, crit_damage=165, armour_penetration=8, weapon_type="heavy"),

        # Mythical Weapons level 25+
        "Whisper of the Void": Item("Whisper of the Void", "weapon", 5000, "mythical", attack=88, accuracy=32, crit_chance=11, crit_damage=160, armour_penetration=9, weapon_type="light"),
        "Destiny's Call": Item("Destiny's Call", "weapon", 5200, "mythical", attack=90, accuracy=29, crit_chance=9, crit_damage=160, armour_penetration=7, weapon_type="medium"),
        "Worldsplitter": Item("Worldsplitter", "weapon", 5400, "mythical", attack=92, accuracy=25, crit_chance=9, crit_damage=170, armour_penetration=9, weapon_type="heavy"),
        "Fang of the Cosmos": Item("Fang of the Cosmos", "weapon", 5600, "mythical", attack=94, accuracy=33, crit_chance=12, crit_damage=165, armour_penetration=10, weapon_type="light"),
        "Harmony's Discord": Item("Harmony's Discord", "weapon", 5800, "mythical", attack=96, accuracy=30, crit_chance=10, crit_damage=165, armour_penetration=8, weapon_type="medium"),
        "Apocalypse Incarnate": Item("Apocalypse Incarnate", "weapon", 6000, "mythical", attack=98, accuracy=26, crit_chance=10, crit_damage=175, armour_penetration=10, weapon_type="heavy"),
        
        # Common Helms (4 points total)
        "Sturdy Leather Cap": Item("Sturdy Leather Cap", "helm", 10, "common", defence=3, damage_reduction=1),
        "Balanced Leather Helm": Item("Balanced Leather Helm", "helm", 10, "common", defence=2, accuracy=2),
        "Sharpshooter's Leather Hood": Item("Sharpshooter's Leather Hood", "helm", 10, "common", defence=1, accuracy=2, crit_chance=1),

        # Uncommon Helms (7 points total)
        "Bronze Greathelm": Item("Bronze Greathelm", "helm", 40, "uncommon", defence=5, damage_reduction=2),
        "Bronze Sallet": Item("Bronze Sallet", "helm", 40, "uncommon", defence=3, accuracy=3, crit_chance=1),
        "Bronze Hawk Helm": Item("Bronze Hawk Helm", "helm", 40, "uncommon", defence=2, accuracy=3, crit_chance=2),

        # Rare Helms (10 points total)
        "Steel Fortress Helm": Item("Steel Fortress Helm", "helm", 80, "rare", defence=7, damage_reduction=3),
        "Steel Armet": Item("Steel Armet", "helm", 80, "rare", defence=4, accuracy=4, crit_chance=2),
        "Steel Sniper's Helm": Item("Steel Sniper's Helm", "helm", 80, "rare", defence=3, accuracy=4, crit_chance=3),

        # Epic Helms (13 points total)
        "Mithril Juggernaut Helm": Item("Mithril Juggernaut Helm", "helm", 280, "epic", defence=9, damage_reduction=4),
        "Mithril Winged Helm": Item("Mithril Winged Helm", "helm", 280, "epic", defence=5, accuracy=5, crit_chance=3),
        "Mithril Crown of Precision": Item("Mithril Crown of Precision", "helm", 280, "epic", defence=4, accuracy=5, crit_chance=4),

        # Masterwork Helms (16 points total)
        "Aluthril Titan's Visage": Item("Aluthril Titan's Visage", "helm", 580, "masterwork", defence=11, damage_reduction=5),
        "Aluthril Helm of the Valiant": Item("Aluthril Helm of the Valiant", "helm", 580, "masterwork", defence=6, accuracy=6, crit_chance=4),
        "Aluthril Crown of the Marksman": Item("Aluthril Crown of the Marksman", "helm", 580, "masterwork", defence=5, accuracy=6, crit_chance=5),

        # Legendary Helms (19 points total)
        "Adamantite Helm of the Unbreakable": Item("Adamantite Helm of the Unbreakable", "helm", 1100, "legendary", defence=13, damage_reduction=6),
        "Adamantite Crown of the Conqueror": Item("Adamantite Crown of the Conqueror", "helm", 1100, "legendary", defence=7, accuracy=7, crit_chance=5),
        "Adamantite Diadem of the Deadeye": Item("Adamantite Diadem of the Deadeye", "helm", 1100, "legendary", defence=6, accuracy=7, crit_chance=6),

        # Mythical Helms (22 points total)
        "Crown of Eternal Fortitude": Item("Crown of Eternal Fortitude", "helm", 5200, "mythical", defence=15, damage_reduction=7),
        "Diadem of Cosmic Balance": Item("Diadem of Cosmic Balance", "helm", 5200, "mythical", defence=8, accuracy=8, crit_chance=6),
        "Crown of Infinite Precision": Item("Crown of Infinite Precision", "helm", 5200, "mythical", defence=7, accuracy=8, crit_chance=7),

        # Common Chest (6 points total)
        "Sturdy Leather Vest": Item("Sturdy Leather Vest", "chest", 25, "common", defence=4, damage_reduction=2),
        "Reinforced Leather Chest": Item("Reinforced Leather Chest", "chest", 25, "common", defence=3, attack=3),
        "Agile Leather Jerkin": Item("Agile Leather Jerkin", "chest", 25, "common", defence=2, attack=2, crit_chance=2),

        # Uncommon Chest (10 points total)
        "Bronze Fortress Plate": Item("Bronze Fortress Plate", "chest", 60, "uncommon", defence=7, damage_reduction=3),
        "Bronze Battle Cuirass": Item("Bronze Battle Cuirass", "chest", 60, "uncommon", defence=5, attack=4, crit_chance=1),
        "Bronze Skirmisher's Mail": Item("Bronze Skirmisher's Mail", "chest", 60, "uncommon", defence=4, attack=3, crit_chance=3),

        # Rare Chest (14 points total)
        "Steel Bulwark Breastplate": Item("Steel Bulwark Breastplate", "chest", 125, "rare", defence=10, damage_reduction=4),
        "Steel Warlord's Cuirass": Item("Steel Warlord's Cuirass", "chest", 125, "rare", defence=7, attack=5, crit_chance=2),
        "Steel Assassin's Hauberk": Item("Steel Assassin's Hauberk", "chest", 125, "rare", defence=6, attack=4, crit_chance=4),

        # Epic Chest (18 points total)
        "Mithril Juggernaut Plate": Item("Mithril Juggernaut Plate", "chest", 360, "epic", defence=13, damage_reduction=5),
        "Mithril Commander's Armor": Item("Mithril Commander's Armor", "chest", 360, "epic", defence=9, attack=6, crit_chance=3),
        "Mithril Shadow Vest": Item("Mithril Shadow Vest", "chest", 360, "epic", defence=8, attack=5, crit_chance=5),

        # Masterwork Chest (22 points total)
        "Aluthril Titan's Chestguard": Item("Aluthril Titan's Chestguard", "chest", 760, "masterwork", defence=16, damage_reduction=6),
        "Aluthril Dragonslayer Cuirass": Item("Aluthril Dragonslayer Cuirass", "chest", 760, "masterwork", defence=11, attack=7, crit_chance=4),
        "Aluthril Nighthawk Vest": Item("Aluthril Nighthawk Vest", "chest", 760, "masterwork", defence=10, attack=6, crit_chance=6),

        # Legendary Chest (26 points total)
        "Adamantite Godplate of the Unassailable": Item("Adamantite Godplate of the Unassailable", "chest", 1350, "legendary", defence=19, damage_reduction=7),
        "Adamantite Vanguard of the Conqueror": Item("Adamantite Vanguard of the Conqueror", "chest", 1350, "legendary", defence=13, attack=8, crit_chance=5),
        "Adamantite Shadowmeld Armor": Item("Adamantite Shadowmeld Armor", "chest", 1350, "legendary", defence=12, attack=7, crit_chance=7),

        # Mythical Chest (30 points total)
        "Vestment of Cosmic Fortitude": Item("Vestment of Cosmic Fortitude", "chest", 5600, "mythical", defence=22, damage_reduction=8),
        "Cuirass of Universal Dominion": Item("Cuirass of Universal Dominion", "chest", 5600, "mythical", defence=15, attack=9, crit_chance=6),
        "Chestpiece of the Celestial Assassin": Item("Chestpiece of the Celestial Assassin", "chest", 5600, "mythical", defence=14, attack=8, crit_chance=8),

        # Common Belts (3 points total)
        "Sturdy Leather Belt": Item("Sturdy Leather Belt", "belt", 10, "common", defence=2, damage_reduction=1),
        "Balanced Leather Girdle": Item("Balanced Leather Girdle", "belt", 10, "common", defence=1, crit_damage=2),
        "Swift Leather Strap": Item("Swift Leather Strap", "belt", 10, "common", defence=1, evasion=2),

        # Uncommon Belts (5 points total)
        "Bronze Defender's Girdle": Item("Bronze Defender's Girdle", "belt", 35, "uncommon", defence=3, damage_reduction=2),
        "Bronze Striker's Belt": Item("Bronze Striker's Belt", "belt", 35, "uncommon", defence=2, crit_damage=3),
        "Bronze Skirmisher's Strap": Item("Bronze Skirmisher's Strap", "belt", 35, "uncommon", defence=2, evasion=3),

        # Rare Belts (7 points total)
        "Steel Bulwark Fauld": Item("Steel Bulwark Fauld", "belt", 88, "rare", defence=4, damage_reduction=3),
        "Steel Ravager's Girdle": Item("Steel Ravager's Girdle", "belt", 88, "rare", defence=3, crit_damage=4),
        "Steel Shadowdancer's Belt": Item("Steel Shadowdancer's Belt", "belt", 88, "rare", defence=3, evasion=4),

        # Epic Belts (9 points total)
        "Mithril Juggernaut Waistguard": Item("Mithril Juggernaut Waistguard", "belt", 300, "epic", defence=5, damage_reduction=4),
        "Mithril Destroyer's Tasset": Item("Mithril Destroyer's Tasset", "belt", 300, "epic", defence=4, crit_damage=5),
        "Mithril Whisperwind Cincture": Item("Mithril Whisperwind Cincture", "belt", 300, "epic", defence=4, evasion=5),

        # Masterwork Belts (11 points total)
        "Aluthril Titan's Waistguard": Item("Aluthril Titan's Waistguard", "belt", 600, "masterwork", defence=6, damage_reduction=5),
        "Aluthril Executioner's Tasset": Item("Aluthril Executioner's Tasset", "belt", 600, "masterwork", defence=5, crit_damage=6),
        "Aluthril Phantom Belt": Item("Aluthril Phantom Belt", "belt", 600, "masterwork", defence=5, evasion=6),

        # Legendary Belts (13 points total)
        "Adamantite Fortress Cinch": Item("Adamantite Fortress Cinch", "belt", 1200, "legendary", defence=7, damage_reduction=6),
        "Adamantite Annihilator's Girdle": Item("Adamantite Annihilator's Girdle", "belt", 1200, "legendary", defence=6, crit_damage=7),
        "Adamantite Shadowmeld Belt": Item("Adamantite Shadowmeld Belt", "belt", 1200, "legendary", defence=6, evasion=7),

        # Mythical Belts (15 points total)
        "Girdle of Cosmic Fortitude": Item("Girdle of Cosmic Fortitude", "belt", 5300, "mythical", defence=8, damage_reduction=7),
        "Cincture of Devastating Strikes": Item("Cincture of Devastating Strikes", "belt", 5300, "mythical", defence=7, crit_damage=8),
        "Belt of Dimensional Flux": Item("Belt of Dimensional Flux", "belt", 5300, "mythical", defence=7, evasion=8),

        # Common Legs (5 points total)
        "Sturdy Leather Leggings": Item("Sturdy Leather Leggings", "legs", 12, "common", defence=3, damage_reduction=2),
        "Balanced Leather Cuisses": Item("Balanced Leather Cuisses", "legs", 12, "common", defence=3, attack=2),
        "Agile Leather Pants": Item("Agile Leather Pants", "legs", 12, "common", defence=2, evasion=3),

        # Uncommon Legs (8 points total)
        "Bronze Defender Greaves": Item("Bronze Defender Greaves", "legs", 50, "uncommon", defence=5, damage_reduction=3),
        "Bronze Warrior Cuisses": Item("Bronze Warrior Cuisses", "legs", 50, "uncommon", defence=4, attack=4),
        "Bronze Skirmisher Pants": Item("Bronze Skirmisher Pants", "legs", 50, "uncommon", defence=3, evasion=5),

        # Rare Legs (11 points total)
        "Steel Bulwark Legplates": Item("Steel Bulwark Legplates", "legs", 115, "rare", defence=7, damage_reduction=4),
        "Steel Berserker Cuisses": Item("Steel Berserker Cuisses", "legs", 115, "rare", defence=5, attack=4, crit_damage=2),
        "Steel Shadowstep Leggings": Item("Steel Shadowstep Leggings", "legs", 115, "rare", defence=4, evasion=5, crit_chance=2),

        # Epic Legs (14 points total)
        "Mithril Juggernaut Legguards": Item("Mithril Juggernaut Legguards", "legs", 340, "epic", defence=9, damage_reduction=5),
        "Mithril Warlord's Cuisses": Item("Mithril Warlord's Cuisses", "legs", 340, "epic", defence=7, attack=5, crit_damage=2),
        "Mithril Shadowdancer Leggings": Item("Mithril Shadowdancer Leggings", "legs", 340, "epic", defence=6, evasion=6, crit_chance=2),

        # Masterwork Legs (17 points total)
        "Aluthril Titan's Legplates": Item("Aluthril Titan's Legplates", "legs", 740, "masterwork", defence=11, damage_reduction=6),
        "Aluthril Conqueror's Cuisses": Item("Aluthril Conqueror's Cuisses", "legs", 740, "masterwork", defence=9, attack=5, crit_damage=3),
        "Aluthril Phantom Leggings": Item("Aluthril Phantom Leggings", "legs", 740, "masterwork", defence=8, evasion=6, crit_chance=3),

        # Legendary Legs (20 points total)
        "Adamantite Fortress Legguards": Item("Adamantite Fortress Legguards", "legs", 1300, "legendary", defence=13, damage_reduction=7),
        "Adamantite Annihilator Cuisses": Item("Adamantite Annihilator Cuisses", "legs", 1300, "legendary", defence=11, attack=6, crit_damage=3),
        "Adamantite Voidwalker Leggings": Item("Adamantite Voidwalker Leggings", "legs", 1300, "legendary", defence=10, evasion=7, crit_chance=3),

        # Mythical Legs (23 points total)
        "Legplates of Cosmic Fortitude": Item("Legplates of Cosmic Fortitude", "legs", 5400, "mythical", defence=15, damage_reduction=8),
        "Cuisses of Reality's Wrath": Item("Cuisses of Reality's Wrath", "legs", 5400, "mythical", defence=13, attack=7, crit_damage=3),
        "Leggings of Dimensional Flux": Item("Leggings of Dimensional Flux", "legs", 5400, "mythical", defence=12, evasion=8, crit_chance=3),

        # Common Boots (4 points total)
        "Sturdy Leather Boots": Item("Sturdy Leather Boots", "boots", 12, "common", defence=2, damage_reduction=2),
        "Balanced Leather Treads": Item("Balanced Leather Treads", "boots", 12, "common", defence=2, attack=2),
        "Nimble Leather Sandals": Item("Nimble Leather Sandals", "boots", 12, "common", defence=1, evasion=3),

        # Uncommon Boots (6 points total)
        "Bronze Defender Sabatons": Item("Bronze Defender Sabatons", "boots", 35, "uncommon", defence=3, damage_reduction=3),
        "Bronze Striker Boots": Item("Bronze Striker Boots", "boots", 35, "uncommon", defence=3, attack=3),
        "Bronze Quickstep Shoes": Item("Bronze Quickstep Shoes", "boots", 35, "uncommon", defence=2, evasion=4),

        # Rare Boots (8 points total)
        "Steel Bulwark Greaves": Item("Steel Bulwark Greaves", "boots", 78, "rare", defence=4, damage_reduction=4),
        "Steel Berserker Stompers": Item("Steel Berserker Stompers", "boots", 78, "rare", defence=4, attack=3, crit_chance=1),
        "Steel Shadowstep Boots": Item("Steel Shadowstep Boots", "boots", 78, "rare", defence=3, evasion=5),

        # Epic Boots (10 points total)
        "Mithril Juggernaut Sabatons": Item("Mithril Juggernaut Sabatons", "boots", 310, "epic", defence=5, damage_reduction=5),
        "Mithril Warlord's Treads": Item("Mithril Warlord's Treads", "boots", 310, "epic", defence=5, attack=4, crit_chance=1),
        "Mithril Phantom Striders": Item("Mithril Phantom Striders", "boots", 310, "epic", defence=4, evasion=6),

        # Masterwork Boots (12 points total)
        "Aluthril Titan's Stompers": Item("Aluthril Titan's Stompers", "boots", 610, "masterwork", defence=6, damage_reduction=6),
        "Aluthril Conqueror's Sabatons": Item("Aluthril Conqueror's Sabatons", "boots", 610, "masterwork", defence=6, attack=4, crit_chance=2),
        "Aluthril Ghostwalker Treads": Item("Aluthril Ghostwalker Treads", "boots", 610, "masterwork", defence=5, evasion=7),

        # Legendary Boots (14 points total)
        "Adamantite Fortress Greaves": Item("Adamantite Fortress Greaves", "boots", 1220, "legendary", defence=7, damage_reduction=7),
        "Adamantite Annihilator Boots": Item("Adamantite Annihilator Boots", "boots", 1220, "legendary", defence=7, attack=5, crit_chance=2),
        "Adamantite Voidwalker Striders": Item("Adamantite Voidwalker Striders", "boots", 1220, "legendary", defence=6, evasion=8),

        # Mythical Boots (16 points total)
        "Sabatons of Cosmic Fortitude": Item("Sabatons of Cosmic Fortitude", "boots", 5350, "mythical", defence=8, damage_reduction=8),
        "Treads of Reality's Wrath": Item("Treads of Reality's Wrath", "boots", 5350, "mythical", defence=8, attack=6, crit_chance=2),
        "Boots of Dimensional Flux": Item("Boots of Dimensional Flux", "boots", 5350, "mythical", defence=7, evasion=9),

        # Common Gloves (4 points total)
        "Sturdy Leather Bracers": Item("Sturdy Leather Bracers", "gloves", 8, "common", defence=2, damage_reduction=2),
        "Leather Fighting Gloves": Item("Leather Fighting Gloves", "gloves", 8, "common", defence=1, attack=3),
        "Nimble Leather Handwraps": Item("Nimble Leather Handwraps", "gloves", 8, "common", defence=1, crit_chance=3),

        # Uncommon Gloves (6 points total)
        "Bronze Defender Gauntlets": Item("Bronze Defender Gauntlets", "gloves", 30, "uncommon", defence=3, damage_reduction=3),
        "Bronze Striker Gloves": Item("Bronze Striker Gloves", "gloves", 30, "uncommon", defence=2, attack=4),
        "Bronze Precision Vambraces": Item("Bronze Precision Vambraces", "gloves", 30, "uncommon", defence=2, crit_chance=4),

        # Rare Gloves (8 points total)
        "Steel Bulwark Gauntlets": Item("Steel Bulwark Gauntlets", "gloves", 95, "rare", defence=4, damage_reduction=4),
        "Steel Crushing Fists": Item("Steel Crushing Fists", "gloves", 95, "rare", defence=3, attack=5),
        "Steel Duelist's Handguards": Item("Steel Duelist's Handguards", "gloves", 95, "rare", defence=3, crit_chance=3, crit_damage=2),

        # Epic Gloves (10 points total)
        "Mithril Juggernaut Gauntlets": Item("Mithril Juggernaut Gauntlets", "gloves", 280, "epic", defence=5, damage_reduction=5),
        "Mithril Warlord's Fists": Item("Mithril Warlord's Fists", "gloves", 280, "epic", defence=4, attack=6),
        "Mithril Assassin's Handwraps": Item("Mithril Assassin's Handwraps", "gloves", 280, "epic", defence=3, crit_chance=4, crit_damage=3),

        # Masterwork Gloves (12 points total)
        "Aluthril Titan's Gauntlets": Item("Aluthril Titan's Gauntlets", "gloves", 580, "masterwork", defence=6, damage_reduction=6),
        "Aluthril Conqueror's Fists": Item("Aluthril Conqueror's Fists", "gloves", 580, "masterwork", defence=5, attack=7),
        "Aluthril Shadowstrike Gloves": Item("Aluthril Shadowstrike Gloves", "gloves", 580, "masterwork", defence=4, crit_chance=4, crit_damage=4),

        # Legendary Gloves (14 points total)
        "Adamantite Fortress Gauntlets": Item("Adamantite Fortress Gauntlets", "gloves", 1180, "legendary", defence=7, damage_reduction=7),
        "Adamantite Worldbreaker Fists": Item("Adamantite Worldbreaker Fists", "gloves", 1180, "legendary", defence=6, attack=8),
        "Adamantite Deathblow Handwraps": Item("Adamantite Deathblow Handwraps", "gloves", 1180, "legendary", defence=5, crit_chance=5, crit_damage=4),

        # Mythical Gloves (16 points total)
        "Gauntlets of Cosmic Fortitude": Item("Gauntlets of Cosmic Fortitude", "gloves", 5150, "mythical", defence=8, damage_reduction=8),
        "Fists of Reality's Wrath": Item("Fists of Reality's Wrath", "gloves", 5150, "mythical", defence=7, attack=9),
        "Handwraps of Dimensional Precision": Item("Handwraps of Dimensional Precision", "gloves", 5150, "mythical", defence=6, crit_chance=5, crit_damage=5),

        # Common Shields (5 points total)
        "Sturdy Leather Shield": Item("Sturdy Leather Shield", "shield", 15, "common", defence=3, damage_reduction=2),
        "Balanced Wooden Shield": Item("Balanced Wooden Shield", "shield", 15, "common", defence=3, block_chance=2),
        "Spiked Leather Buckler": Item("Spiked Leather Buckler", "shield", 15, "common", defence=2, attack=3),

        # Uncommon Shields (7 points total)
        "Bronze Tower Shield": Item("Bronze Tower Shield", "shield", 32, "uncommon", defence=4, damage_reduction=3),
        "Bronze Kite Shield": Item("Bronze Kite Shield", "shield", 32, "uncommon", defence=4, block_chance=3),
        "Bronze Spiked Shield": Item("Bronze Spiked Shield", "shield", 32, "uncommon", defence=3, attack=4),

        # Rare Shields (9 points total)
        "Steel Bulwark": Item("Steel Bulwark", "shield", 48, "rare", defence=5, damage_reduction=4),
        "Steel Guardian Shield": Item("Steel Guardian Shield", "shield", 48, "rare", defence=5, block_chance=4),
        "Steel Retaliation Shield": Item("Steel Retaliation Shield", "shield", 48, "rare", defence=4, attack=3, crit_chance=2),

        # Epic Shields (11 points total)
        "Mithril Fortress Shield": Item("Mithril Fortress Shield", "shield", 230, "epic", defence=6, damage_reduction=5),
        "Mithril Aegis of Deflection": Item("Mithril Aegis of Deflection", "shield", 230, "epic", defence=6, block_chance=5),
        "Mithril Counterattack Shield": Item("Mithril Counterattack Shield", "shield", 230, "epic", defence=5, attack=4, crit_chance=2),

        # Masterwork Shields (13 points total)
        "Aluthril Impenetrable Bulwark": Item("Aluthril Impenetrable Bulwark", "shield", 530, "masterwork", defence=7, damage_reduction=6),
        "Aluthril Aegis of Warding": Item("Aluthril Aegis of Warding", "shield", 530, "masterwork", defence=7, block_chance=6),
        "Aluthril Shield of Retribution": Item("Aluthril Shield of Retribution", "shield", 530, "masterwork", defence=6, attack=5, crit_chance=2),

        # Legendary Shields (15 points total)
        "Adamantite Invincible Rampart": Item("Adamantite Invincible Rampart", "shield", 980, "legendary", defence=8, damage_reduction=7),
        "Adamantite Aegis of the Indomitable": Item("Adamantite Aegis of the Indomitable", "shield", 980, "legendary", defence=8, block_chance=7),
        "Adamantite Shield of Reckoning": Item("Adamantite Shield of Reckoning", "shield", 980, "legendary", defence=7, attack=6, crit_chance=2),

        # Mythical Shields (17 points total)
        "Bulwark of Cosmic Fortitude": Item("Bulwark of Cosmic Fortitude", "shield", 4900, "mythical", defence=9, damage_reduction=8),
        "Aegis of Reality's Denial": Item("Aegis of Reality's Denial", "shield", 4900, "mythical", defence=9, block_chance=8),
        "Shield of Universal Vengeance": Item("Shield of Universal Vengeance", "shield", 4900, "mythical", defence=8, attack=7, crit_chance=2),

        # Common Back Items (4 points total)
        "Sturdy Leather Poncho": Item("Sturdy Leather Poncho", "back", 14, "common", defence=2, damage_reduction=2),
        "Traveler's Cloak": Item("Traveler's Cloak", "back", 14, "common", defence=2, evasion=2),
        "Concealing Scarf": Item("Concealing Scarf", "back", 14, "common", defence=1, crit_chance=3),

        # Uncommon Back Items (6 points total)
        "Bronze-Weave Mantle": Item("Bronze-Weave Mantle", "back", 45, "uncommon", defence=3, damage_reduction=3),
        "Iron-Trimmed Cloak": Item("Iron-Trimmed Cloak", "back", 45, "uncommon", defence=3, evasion=3),
        "Shadowed Cape": Item("Shadowed Cape", "back", 45, "uncommon", defence=2, crit_chance=4),

        # Rare Back Items (8 points total)
        "Reinforced Battle Cloak": Item("Reinforced Battle Cloak", "back", 105, "rare", defence=4, damage_reduction=4),
        "Steel-Threaded Shadowcape": Item("Steel-Threaded Shadowcape", "back", 105, "rare", defence=4, evasion=4),
        "Mantle of the Unseen Strike": Item("Mantle of the Unseen Strike", "back", 105, "rare", defence=3, crit_chance=5),

        # Epic Back Items (10 points total)
        "Mithril-Woven Defender's Cape": Item("Mithril-Woven Defender's Cape", "back", 330, "epic", defence=5, damage_reduction=5),
        "Mithril Shroud of Obscurity": Item("Mithril Shroud of Obscurity", "back", 330, "epic", defence=5, evasion=5),
        "Cloak of Deadly Precision": Item("Cloak of Deadly Precision", "back", 330, "epic", defence=4, crit_chance=6),

        # Masterwork Back Items (12 points total)
        "Aluthril-Woven Bulwark Cape": Item("Aluthril-Woven Bulwark Cape", "back", 630, "masterwork", defence=6, damage_reduction=6),
        "Aluthril Shroud of the Unseen": Item("Aluthril Shroud of the Unseen", "back", 630, "masterwork", defence=6, evasion=6),
        "Mantle of Lethal Shadows": Item("Mantle of Lethal Shadows", "back", 630, "masterwork", defence=5, crit_chance=7),

        # Legendary Back Items (14 points total)
        "Adamantite Shadowcloak of Fortitude": Item("Adamantite Shadowcloak of Fortitude", "back", 1270, "legendary", defence=7, damage_reduction=7),
        "Adamantite Veil of Phantom Steps": Item("Adamantite Veil of Phantom Steps", "back", 1270, "legendary", defence=7, evasion=7),
        "Cloak of Devastating Strikes": Item("Cloak of Devastating Strikes", "back", 1270, "legendary", defence=6, crit_chance=8),

        # Mythical Back Items (16 points total)
        "Mantle of Cosmic Resilience": Item("Mantle of Cosmic Resilience", "back", 5450, "mythical", defence=8, damage_reduction=8),
        "Cloak of Celestial Shadows": Item("Cloak of Celestial Shadows", "back", 5450, "mythical", defence=8, evasion=8),
        "Shroud of Universal Precision": Item("Shroud of Universal Precision", "back", 5450, "mythical", defence=7, crit_chance=9),

        # Common Rings (4 points total)
        "Leather Armband of Might": Item("Leather Armband of Might", "ring", 20, "common", attack=2, defence=2),
        "Copper Ring of Precision": Item("Copper Ring of Precision", "ring", 20, "common", crit_chance=2, crit_damage=2),
        "Wooden Band of Resilience": Item("Wooden Band of Resilience", "ring", 20, "common", damage_reduction=2, evasion=2),

        # Uncommon Rings (6 points total)
        "Bronze Ring of Power": Item("Bronze Ring of Power", "ring", 60, "uncommon", attack=3, defence=3),
        "Silver Band of the Hawk": Item("Silver Band of the Hawk", "ring", 60, "uncommon", crit_chance=3, crit_damage=3),
        "Iron Loop of Endurance": Item("Iron Loop of Endurance", "ring", 60, "uncommon", damage_reduction=3, evasion=3),

        # Rare Rings (8 points total)
        "Steel Signet of the Warrior": Item("Steel Signet of the Warrior", "ring", 155, "rare", attack=4, defence=4),
        "Golden Ring of the Assassin": Item("Golden Ring of the Assassin", "ring", 155, "rare", crit_chance=4, crit_damage=4),
        "Reinforced Band of the Guardian": Item("Reinforced Band of the Guardian", "ring", 155, "rare", damage_reduction=4, evasion=4),

        # Epic Rings (10 points total)
        "Mithril Ring of Conquest": Item("Mithril Ring of Conquest", "ring", 350, "epic", attack=5, defence=5),
        "Opal Band of Deadly Precision": Item("Opal Band of Deadly Precision", "ring", 350, "epic", crit_chance=5, crit_damage=5),
        "Enchanted Loop of Warding": Item("Enchanted Loop of Warding", "ring", 350, "epic", damage_reduction=5, evasion=5),

        # Masterwork Rings (12 points total)
        "Aluthril Signet of Dominance": Item("Aluthril Signet of Dominance", "ring", 410, "masterwork", attack=6, defence=6),
        "Diamond Ring of Lethal Strikes": Item("Diamond Ring of Lethal Strikes", "ring", 410, "masterwork", crit_chance=6, crit_damage=6),
        "Runic Band of Invincibility": Item("Runic Band of Invincibility", "ring", 410, "masterwork", damage_reduction=6, evasion=6),

        # Legendary Rings (14 points total)
        "Adamantite Loop of Supreme Power": Item("Adamantite Loop of Supreme Power", "ring", 1550, "legendary", attack=7, defence=7),
        "Infused Ring of Deadly Mastery": Item("Infused Ring of Deadly Mastery", "ring", 1550, "legendary", crit_chance=7, crit_damage=7),
        "Celestial Band of Divine Protection": Item("Celestial Band of Divine Protection", "ring", 1550, "legendary", damage_reduction=7, evasion=7),

        # Mythical Rings (16 points total)
        "Band of Divine Providence": Item("Band of Divine Providence", "ring", 6100, "mythical", attack=8, defence=8),
        "Signet of Cosmic Devastation": Item("Signet of Cosmic Devastation", "ring", 6100, "mythical", crit_chance=8, crit_damage=8),
        "Ring of Universal Harmony": Item("Ring of Universal Harmony", "ring", 6100, "mythical", damage_reduction=8, evasion=8),

        # Consumables
        ## Healing Items
        # Common
        "Minor Health Potion": Item("Minor Health Potion", "consumable", 15, "common", effect_type="healing", effect=20, cooldown=3),
        "Quick Heal Salve": Item("Quick Heal Salve", "consumable", 10, "common", effect_type="healing", effect=12, cooldown=1),

        # Uncommon
        "Health Potion": Item("Health Potion", "consumable", 25, "uncommon", effect_type="healing", effect=40, cooldown=3),
        "Swift Healing Draught": Item("Swift Healing Draught", "consumable", 18, "uncommon", effect_type="healing", effect=24, cooldown=1),

        # Rare
        "Greater Health Potion": Item("Greater Health Potion", "consumable", 45, "rare", effect_type="healing", effect=80, cooldown=3),
        "Rapid Restoration Elixir": Item("Rapid Restoration Elixir", "consumable", 33, "rare", effect_type="healing", effect=48, cooldown=1),

        # Masterwork
        "Supreme Health Potion": Item("Supreme Health Potion", "consumable", 500, "masterwork", effect_type="healing", effect=160, cooldown=6),
        "Quicksilver Healing Tincture": Item("Quicksilver Healing Tincture", "consumable", 375, "masterwork", effect_type="healing", effect=96, cooldown=3),
        "Arcane Rejuvenation Brew": Item("Arcane Rejuvenation Brew", "consumable", 425, "masterwork", effect_type="healing", effect=128, cooldown=4),
        "Ethereal Mending Mist": Item("Ethereal Mending Mist", "consumable", 300, "masterwork", effect_type="healing", effect=80, cooldown=2),

        # Legendary
        "Godly Restoration Flask": Item("Godly Restoration Flask", "consumable", 2000, "legendary", effect_type="healing", effect=320, cooldown=12),
        "Celestial Mending Vial": Item("Celestial Mending Vial", "consumable", 1500, "legendary", effect_type="healing", effect=192, cooldown=6),
        "Phoenix Tear Elixir": Item("Phoenix Tear Elixir", "consumable", 1750, "legendary", effect_type="healing", effect=256, cooldown=8),
        "Dragon Heart Infusion": Item("Dragon Heart Infusion", "consumable", 1250, "legendary", effect_type="healing", effect=160, cooldown=4),
        "Titan's Vitality Draught": Item("Titan's Vitality Draught", "consumable", 1000, "legendary", effect_type="healing", effect=128, cooldown=3),

        # Mythical
        "Essence of Eternity": Item("Essence of Eternity", "consumable", 10000, "mythical", effect_type="healing", effect=1000, cooldown=50),
        "Divine Rejuvenation Philter": Item("Divine Rejuvenation Philter", "consumable", 7500, "mythical", effect_type="healing", effect=600, cooldown=25),
        "Ambrosia of the Gods": Item("Ambrosia of the Gods", "consumable", 8500, "mythical", effect_type="healing", effect=800, cooldown=35),
        "Cosmic Restoration Nectar": Item("Cosmic Restoration Nectar", "consumable", 6500, "mythical", effect_type="healing", effect=500, cooldown=20),
        "Starlight Healing Essence": Item("Starlight Healing Essence", "consumable", 5500, "mythical", effect_type="healing", effect=400, cooldown=15),
        "Void Mender's Elixir": Item("Void Mender's Elixir", "consumable", 4500, "mythical", effect_type="healing", effect=300, cooldown=10),
        
        # New Heal over Time Items
        "Minor Regeneration Potion": Item("Minor Regeneration Potion", "consumable", 20, "common", effect_type="hot", effect=0, cooldown=5, duration=5, tick_effect=5),
        "Regeneration Elixir": Item("Regeneration Elixir", "consumable", 40, "uncommon", effect_type="hot", effect=0, cooldown=6, duration=6, tick_effect=10),
        "Greater Regeneration Tonic": Item("Greater Regeneration Tonic", "consumable", 80, "rare", effect_type="hot", effect=0, cooldown=7, duration=8, tick_effect=15),
        "Supreme Vitality Brew": Item("Supreme Vitality Brew", "consumable", 400, "masterwork", effect_type="hot", effect=0, cooldown=8, duration=10, tick_effect=25),
        "Legendary Life Essence": Item("Legendary Life Essence", "consumable", 1600, "legendary", effect_type="hot", effect=0, cooldown=10, duration=12, tick_effect=40),
        "Mythical Fountain of Youth": Item("Mythical Fountain of Youth", "consumable", 8000, "mythical", effect_type="hot", effect=0, cooldown=15, duration=15, tick_effect=80),

        ## Damage Items
        # Common
        "Small Bomb": Item("Small Bomb", "consumable", 30, "common", effect_type="damage", effect=25, cooldown=2),
        "Throwing Knife": Item("Throwing Knife", "consumable", 20, "common", effect_type="damage", effect=15, cooldown=1),
        
        # Uncommon
        "Firebomb": Item("Firebomb", "consumable", 60, "uncommon", effect_type="damage", effect=50, cooldown=3),
        "Acid Flask": Item("Acid Flask", "consumable", 45, "uncommon", effect_type="damage", effect=30, cooldown=2),
        "Ice Shard": Item("Ice Shard", "consumable", 35, "uncommon", effect_type="damage", effect=20, cooldown=1),
        
        # Rare
        "Explosive Flask": Item("Explosive Flask", "consumable", 120, "rare", effect_type="damage", effect=100, cooldown=4),
        "Lightning Bolt": Item("Lightning Bolt", "consumable", 90, "rare", effect_type="damage", effect=60, cooldown=3),
        "Frost Spike": Item("Frost Spike", "consumable", 70, "rare", effect_type="damage", effect=40, cooldown=2),
        "Venom Dart": Item("Venom Dart", "consumable", 60, "rare", effect_type="damage", effect=25, cooldown=1),
        
        # Masterwork
        "Arcane Detonator": Item("Arcane Detonator", "consumable", 600, "masterwork", effect_type="damage", effect=200, cooldown=5),
        "Elemental Surge": Item("Elemental Surge", "consumable", 450, "masterwork", effect_type="damage", effect=120, cooldown=4),
        "Chaos Orb": Item("Chaos Orb", "consumable", 350, "masterwork", effect_type="damage", effect=80, cooldown=3),
        "Astral Shard": Item("Astral Shard", "consumable", 300, "masterwork", effect_type="damage", effect=60, cooldown=2),
        "Ethereal Dart": Item("Ethereal Dart", "consumable", 250, "masterwork", effect_type="damage", effect=40, cooldown=1),
        
        # Legendary
        "Vortex Grenade": Item("Vortex Grenade", "consumable", 2500, "legendary", effect_type="damage", effect=400, cooldown=8),
        "Phoenix Feather": Item("Phoenix Feather", "consumable", 1800, "legendary", effect_type="damage", effect=240, cooldown=6),
        "Dragon's Breath": Item("Dragon's Breath", "consumable", 1400, "legendary", effect_type="damage", effect=160, cooldown=4),
        "Titan's Fist": Item("Titan's Fist", "consumable", 1100, "legendary", effect_type="damage", effect=100, cooldown=2),
        
        # Mythical
        "Supernova Sphere": Item("Supernova Sphere", "consumable", 12000, "mythical", effect_type="damage", effect=1000, cooldown=15),
        "Cosmic Shard": Item("Cosmic Shard", "consumable", 9000, "mythical", effect_type="damage", effect=600, cooldown=10),
        "Galactic Implosion": Item("Galactic Implosion", "consumable", 7500, "mythical", effect_type="damage", effect=800, cooldown=8),
        "Nebula Burst": Item("Nebula Burst", "consumable", 6000, "mythical", effect_type="damage", effect=500, cooldown=5),
        "Quantum Flux": Item("Quantum Flux", "consumable", 4500, "mythical", effect_type="damage", effect=300, cooldown=3),
        "Star Fragment": Item("Star Fragment", "consumable", 3000, "mythical", effect_type="damage", effect=150, cooldown=1),

        ## Buff Items
        # Common
        "Minor Strength Tonic": Item("Minor Strength Tonic", "consumable", 20, "common", effect_type="buff", effect=("attack", 5), cooldown=5, combat_only=True),
        "Minor Iron Skin Elixir": Item("Minor Iron Skin Elixir", "consumable", 20, "common", effect_type="buff", effect=("defence", 5), cooldown=5, combat_only=True),
        "Minor Warrior's Brew": Item("Minor Warrior's Brew", "consumable", 25, "common", effect_type="buff", effect=("all stats", 2), cooldown=5, combat_only=True),
        "Quick Strength Drop": Item("Quick Strength Drop", "consumable", 15, "common", effect_type="buff", effect=("attack", 3), cooldown=2, combat_only=True),
        "Quick Iron Skin Drop": Item("Quick Iron Skin Drop", "consumable", 15, "common", effect_type="buff", effect=("defence", 3), cooldown=2, combat_only=True),
        "Quick Warrior's Drop": Item("Quick Warrior's Drop", "consumable", 18, "common", effect_type="buff", effect=("all stats", 1), cooldown=2, combat_only=True),

        # Uncommon
        "Strength Tonic": Item("Strength Tonic", "consumable", 40, "uncommon", effect_type="buff", effect=("attack", 10), cooldown=6, combat_only=True),
        "Iron Skin Elixir": Item("Iron Skin Elixir", "consumable", 40, "uncommon", effect_type="buff", effect=("defence", 10), cooldown=6, combat_only=True),
        "Warrior's Brew": Item("Warrior's Brew", "consumable", 50, "uncommon", effect_type="buff", effect=("all stats", 5), cooldown=6, combat_only=True),
        "Swift Strength Vial": Item("Swift Strength Vial", "consumable", 30, "uncommon", effect_type="buff", effect=("attack", 6), cooldown=3, combat_only=True),
        "Swift Iron Skin Vial": Item("Swift Iron Skin Vial", "consumable", 30, "uncommon", effect_type="buff", effect=("defence", 6), cooldown=3, combat_only=True),
        "Swift Warrior's Vial": Item("Swift Warrior's Vial", "consumable", 35, "uncommon", effect_type="buff", effect=("all stats", 3), cooldown=3, combat_only=True),

        # Rare
        "Greater Strength Tonic": Item("Greater Strength Tonic", "consumable", 80, "rare", effect_type="buff", effect=("attack", 20), cooldown=7, combat_only=True),
        "Greater Iron Skin Elixir": Item("Greater Iron Skin Elixir", "consumable", 80, "rare", effect_type="buff", effect=("defence", 20), cooldown=7, combat_only=True),
        "Greater Warrior's Brew": Item("Greater Warrior's Brew", "consumable", 100, "rare", effect_type="buff", effect=("all stats", 10), cooldown=7, combat_only=True),
        "Rapid Strength Essence": Item("Rapid Strength Essence", "consumable", 60, "rare", effect_type="buff", effect=("attack", 12), cooldown=3, combat_only=True),
        "Rapid Iron Skin Essence": Item("Rapid Iron Skin Essence", "consumable", 60, "rare", effect_type="buff", effect=("defence", 12), cooldown=3, combat_only=True),
        "Rapid Warrior's Essence": Item("Rapid Warrior's Essence", "consumable", 75, "rare", effect_type="buff", effect=("all stats", 6), cooldown=3, combat_only=True),

        # Masterwork
        "Masterwork Strength Tonic": Item("Masterwork Strength Tonic", "consumable", 400, "masterwork", effect_type="buff", effect=("attack", 40), cooldown=8, combat_only=True),
        "Masterwork Iron Skin Elixir": Item("Masterwork Iron Skin Elixir", "consumable", 400, "masterwork", effect_type="buff", effect=("defence", 40), cooldown=8, combat_only=True),
        "Masterwork Warrior's Brew": Item("Masterwork Warrior's Brew", "consumable", 500, "masterwork", effect_type="buff", effect=("all stats", 20), cooldown=8, combat_only=True),
        "Quicksilver Strength Philter": Item("Quicksilver Strength Philter", "consumable", 300, "masterwork", effect_type="buff", effect=("attack", 24), cooldown=4, combat_only=True),
        "Quicksilver Iron Skin Philter": Item("Quicksilver Iron Skin Philter", "consumable", 300, "masterwork", effect_type="buff", effect=("defence", 24), cooldown=4, combat_only=True),
        "Quicksilver Warrior's Philter": Item("Quicksilver Warrior's Philter", "consumable", 375, "masterwork", effect_type="buff", effect=("all stats", 12), cooldown=4, combat_only=True),

        # Legendary
        "Legendary Strength Tonic": Item("Legendary Strength Tonic", "consumable", 1600, "legendary", effect_type="buff", effect=("attack", 80), cooldown=10, combat_only=True),
        "Legendary Iron Skin Elixir": Item("Legendary Iron Skin Elixir", "consumable", 1600, "legendary", effect_type="buff", effect=("defence", 80), cooldown=10, combat_only=True),
        "Legendary Warrior's Brew": Item("Legendary Warrior's Brew", "consumable", 2000, "legendary", effect_type="buff", effect=("all stats", 40), cooldown=10, combat_only=True),
        "Celestial Strength Ampoule": Item("Celestial Strength Ampoule", "consumable", 1200, "legendary", effect_type="buff", effect=("attack", 48), cooldown=5, combat_only=True),
        "Celestial Iron Skin Ampoule": Item("Celestial Iron Skin Ampoule", "consumable", 1200, "legendary", effect_type="buff", effect=("defence", 48), cooldown=5, combat_only=True),
        "Celestial Warrior's Ampoule": Item("Celestial Warrior's Ampoule", "consumable", 1500, "legendary", effect_type="buff", effect=("all stats", 24), cooldown=5, combat_only=True),

        # Mythical
        "Godly Strength Tonic": Item("Godly Strength Tonic", "consumable", 8000, "mythical", effect_type="buff", effect=("attack", 160), cooldown=15, combat_only=True),
        "Godly Iron Skin Elixir": Item("Godly Iron Skin Elixir", "consumable", 8000, "mythical", effect_type="buff", effect=("defence", 160), cooldown=15, combat_only=True),
        "Godly Warrior's Brew": Item("Godly Warrior's Brew", "consumable", 10000, "mythical", effect_type="buff", effect=("all stats", 80), cooldown=15, combat_only=True),
        "Divine Strength Infusion": Item("Divine Strength Infusion", "consumable", 6000, "mythical", effect_type="buff", effect=("attack", 96), cooldown=7, combat_only=True),
        "Divine Iron Skin Infusion": Item("Divine Iron Skin Infusion", "consumable", 6000, "mythical", effect_type="buff", effect=("attack", 96), cooldown=7, combat_only=True),
        "Divine Warrior's Infusion": Item("Divine Warrior's Infusion", "consumable", 7500, "mythical", effect_type="buff", effect=("all stats", 48), cooldown=7, combat_only=True),
        
        #Sharpening Stones
        "Basic Sharpening Stone": Item("Basic Sharpening Stone", "consumable", 100, "common", effect_type="weapon_buff", effect=("attack", 5), cooldown=0, duration=20),
        "Quality Sharpening Stone": Item("Quality Sharpening Stone", "consumable", 250, "uncommon", effect_type="weapon_buff", effect=("attack", 10), cooldown=0, duration=20),
        "Superior Sharpening Stone": Item("Superior Sharpening Stone", "consumable", 500, "rare", effect_type="weapon_buff", effect=("attack", 15), cooldown=0, duration=20),
        "Master Sharpening Stone": Item("Master Sharpening Stone", "consumable", 1000, "epic", effect_type="weapon_buff", effect=("attack", 20), cooldown=0, duration=20),
        
        #Weapon Coatings
        ##Poison Coatings
        "Weak Poison Coating": Item("Weak Poison Coating", "weapon coating", 50, "common", effect_type="poison", effect=(2, 3), cooldown=5, duration=5),
        "Poison Coating": Item("Poison Coating", "weapon coating", 100, "uncommon", effect_type="poison", effect=(3, 4), cooldown=6, duration=5),
        "Potent Poison Coating": Item("Potent Poison Coating", "weapon coating", 200, "rare", effect_type="poison", effect=(4, 5), cooldown=7, duration=6),
        "Deadly Poison Coating": Item("Deadly Poison Coating", "weapon coating", 400, "epic", effect_type="poison", effect=(5, 6), cooldown=8, duration=7),
        
        # Food items
        "Bread": Item("Bread", "food", 25, "common", effect_type="stamina", stamina_restore=10),
        "Cheese": Item("Cheese", "food", 40, "common", effect_type="stamina", stamina_restore=15),
        "Apple": Item("Apple", "food", 20, "common", effect_type="stamina", stamina_restore=5),
        "Jerky": Item("Jerky", "food", 50, "common", effect_type="stamina", stamina_restore=20),
        "Meat Stew": Item("Meat Stew", "food", 80, "uncommon", effect_type="buff", effect=("attack", 2), stamina_restore=25, duration=5),
        "Fruit Salad": Item("Fruit Salad", "food", 80, "uncommon", effect_type="buff", effect=("defence", 2), stamina_restore=20, duration=5),
        "Vegetable Soup": Item("Vegetable Soup", "food", 70, "uncommon", effect_type="healing", effect=15, stamina_restore=15),
        "Fish Fillet": Item("Fish Fillet", "food", 90, "uncommon", effect_type="buff", effect=("all stats", 1), stamina_restore=30, duration=6),
        "Hearty Meal": Item("Hearty Meal", "food", 200, "rare", effect_type="buff", effect=("all stats", 3), stamina_restore=40, duration=10),
        "Elven Lembas": Item("Elven Lembas", "food", 300, "rare", effect_type="buff", effect=("all stats", 4), stamina_restore=50, duration=15),
        "Dragon Steak": Item("Dragon Steak", "food", 500, "masterwork", effect_type="buff", effect=("attack", 8), stamina_restore=70, duration=20),
        "Ambrosia": Item("Ambrosia", "food", 1000, "legendary", effect_type="buff", effect=("all stats", 10), stamina_restore=100, duration=30),

        # Drink items
        "Water": Item("Water", "drink", 15, "common", effect_type="stamina", stamina_restore=5),
        "Ale": Item("Ale", "drink", 25, "common", effect_type="stamina", stamina_restore=10),
        "Milk": Item("Milk", "drink", 20, "common", effect_type="healing", effect=5, stamina_restore=5),
        "Fruit Juice": Item("Fruit Juice", "drink", 30, "common", effect_type="stamina", stamina_restore=15),
        "Stamina Potion": Item("Stamina Potion", "drink", 120, "uncommon", effect_type="stamina", stamina_restore=50),
        "Healing Tea": Item("Healing Tea", "drink", 75, "uncommon", effect_type="healing", effect=20, stamina_restore=10),
        "Strength Brew": Item("Strength Brew", "drink", 100, "rare", effect_type="buff", effect=("attack", 5), stamina_restore=30, duration=8),
        "Fortifying Tonic": Item("Fortifying Tonic", "drink", 100, "rare", effect_type="buff", effect=("defence", 5), stamina_restore=30, duration=8),
        "Mana Elixir": Item("Mana Elixir", "drink", 175, "rare", effect_type="stamina", stamina_restore=80),
        "Giant's Strength Potion": Item("Giant's Strength Potion", "drink", 400, "masterwork", effect_type="buff", effect=("attack", 10), stamina_restore=50, duration=15),
        "Ethereal Essence": Item("Ethereal Essence", "drink", 600, "masterwork", effect_type="buff", effect=("all stats", 7), stamina_restore=70, duration=20),
        "Elixir of Immortality": Item("Elixir of Immortality", "drink", 1500, "legendary", effect_type="buff", effect=("all stats", 15), stamina_restore=150, duration=40),
        
        #Teleport Scroll
        "Scroll of Teleportation": Item("Scroll of Teleportation", "consumable", 500, "rare", effect_type="teleport", effect=0, cooldown=0),
    }