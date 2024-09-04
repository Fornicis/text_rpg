class Item:
    def __init__(self, name, item_type, value, tier, attack=0, defence=0, effect_type=None, effect=0, cooldown=0):
        self.name = name
        self.type = item_type
        self.value = value
        self.tier = tier
        self.attack = attack
        self.defence = defence
        self.effect_type = effect_type
        self.effect = effect
        self.cooldown = cooldown
        
def initialise_items():
    return {
        # Starter items
        "Peasants Top": Item("Peasants Top", "chest", 0, "starter", defence=1),
        "Peasants Bottoms": Item("Peasants Bottoms", "legs", 0, "starter", defence=1),
        "Wooden Sword": Item("Wooden Sword", "weapon", 0, "starter", attack=2),

        # Common tier (Leather)
        ## Weapons
        "Leather Whip": Item("Leather Whip", "weapon", 20, "common", attack=5),
        "Leather Sling": Item("Leather Sling", "weapon", 15, "common", attack=4),
        "Leather Bound Club": Item("Leather Bound Club", "weapon", 18, "common", attack=6),

        ## Armor
        "Leather Shield": Item("Leather Shield", "shield", 15, "common", defence=2),
        "Leather Helm": Item("Leather Helm", "helm", 10, "common", defence=1),
        "Leather Chest": Item("Leather Chest", "chest", 25, "common", defence=3),
        "Leather Boots": Item("Leather Boots", "boots", 12, "common", defence=1),
        "Leather Gloves": Item("Leather Gloves", "gloves", 8, "common", defence=1),
        "Leather Cloak": Item("Leather Cloak", "back", 14, "common", defence=1),
        "Leather Leggings": Item("Leather Leggings", "legs", 12, "common", defence=2),
        "Leather Belt": Item("Leather Belt", "waist", 10, "common", defence=1),
        "Leather Wristband": Item("Leather Wristband", "ring", 20, "common", attack=1, defence=1),
        "Leather Cap": Item("Leather Cap", "helm", 9, "common", defence=1),
        "Leather Vest": Item("Leather Vest", "chest", 22, "common", defence=2),
        "Leather Sandals": Item("Leather Sandals", "boots", 11, "common", defence=1),
        "Leather Bracers": Item("Leather Bracers", "gloves", 7, "common", defence=1),
        "Leather Poncho": Item("Leather Poncho", "back", 13, "common", defence=1),
        "Leather Skirt": Item("Leather Skirt", "legs", 11, "common", defence=1),
        "Leather Armband": Item("Leather Armband", "ring", 18, "common", attack=1, defence=1),

        ## Consumables
        "Minor Health Potion": Item("Minor Health Potion", "consumable", 15, "common", effect_type="healing", effect=20, cooldown=3),
        "Small Bomb": Item("Small Bomb", "consumable", 30, "common", effect_type="damage", effect=20, cooldown=2),
        "Courage Charm": Item("Courage Charm", "consumable", 35, "common", effect_type="buff", effect=("attack", 5), cooldown=6),

        # Uncommon tier (Bronze and Iron)
        ## Weapons
        "Bronze Sword": Item("Bronze Sword", "weapon", 35, "uncommon", attack=10),
        "Iron Mace": Item("Iron Mace", "weapon", 40, "uncommon", attack=11),
        "Bronze Spear": Item("Bronze Spear", "weapon", 38, "uncommon", attack=12),

        ## Armor
        "Bronze Shield": Item("Bronze Shield", "shield", 30, "uncommon", defence=4),
        "Iron Helm": Item("Iron Helm", "helm", 40, "uncommon", defence=3),
        "Bronze Chestplate": Item("Bronze Chestplate", "chest", 55, "uncommon", defence=6),
        "Iron Boots": Item("Iron Boots", "boots", 35, "uncommon", defence=3),
        "Bronze Gauntlets": Item("Bronze Gauntlets", "gloves", 30, "uncommon", defence=2),
        "Iron-Trimmed Cloak": Item("Iron-Trimmed Cloak", "back", 45, "uncommon", defence=3),
        "Bronze Greaves": Item("Bronze Greaves", "legs", 50, "uncommon", defence=4),
        "Iron Belt": Item("Iron Belt", "waist", 35, "uncommon", defence=2),
        "Bronze Ring": Item("Bronze Ring", "ring", 60, "uncommon", attack=2, defence=1),
        "Iron Buckler": Item("Iron Buckler", "shield", 32, "uncommon", defence=3),
        "Bronze Coif": Item("Bronze Coif", "helm", 38, "uncommon", defence=2),
        "Iron Cuirass": Item("Iron Cuirass", "chest", 58, "uncommon", defence=5),
        "Bronze Sabatons": Item("Bronze Sabatons", "boots", 33, "uncommon", defence=2),
        "Iron Vambraces": Item("Iron Vambraces", "gloves", 28, "uncommon", defence=2),
        "Bronze-Weave Mantle": Item("Bronze-Weave Mantle", "back", 43, "uncommon", defence=2),
        "Iron Cuisses": Item("Iron Cuisses", "legs", 48, "uncommon", defence=3),
        "Bronze Girdle": Item("Bronze Girdle", "waist", 33, "uncommon", defence=2),
        "Iron Band": Item("Iron Band", "ring", 58, "uncommon", attack=1, defence=2),

        ## Consumables
        "Health Potion": Item("Health Potion", "consumable", 25, "uncommon", effect_type="healing", effect=30, cooldown=3),
        "Strength Elixir": Item("Strength Elixir", "consumable", 55, "uncommon", effect_type="buff", effect=("attack", 10), cooldown=4),

        # Rare tier (Steel)
        ## Weapons
        "Steel Longsword": Item("Steel Longsword", "weapon", 60, "rare", attack=15),
        "Steel Battleaxe": Item("Steel Battleaxe", "weapon", 65, "rare", attack=16),
        "Steel Bow": Item("Steel Bow", "weapon", 70, "rare", attack=17),
        "Steel Warhammer": Item("Steel Warhammer", "weapon", 68, "rare", attack=18),
        "Steel Halberd": Item("Steel Halberd", "weapon", 72, "rare", attack=17),
        "Steel Crossbow": Item("Steel Crossbow", "weapon", 75, "rare", attack=18),
        "Steel Katana": Item("Steel Katana", "weapon", 67, "rare", attack=16),
        "Steel Claymore": Item("Steel Claymore", "weapon", 71, "rare", attack=19),
        "Steel Chakram": Item("Steel Chakram", "weapon", 63, "rare", attack=15),

        ## Armor
        "Steel Kite Shield": Item("Steel Kite Shield", "shield", 45, "rare", defence=7),
        "Steel Helm": Item("Steel Helm", "helm", 80, "rare", defence=6),
        "Steel Breastplate": Item("Steel Breastplate", "chest", 120, "rare", defence=10),
        "Steel Sabatons": Item("Steel Sabatons", "boots", 75, "rare", defence=5),
        "Steel Gauntlets": Item("Steel Gauntlets", "gloves", 90, "rare", defence=4),
        "Reinforced Cloak": Item("Reinforced Cloak", "back", 100, "rare", defence=5),
        "Steel Cuisses": Item("Steel Cuisses", "legs", 110, "rare", defence=8),
        "Steel Girdle": Item("Steel Girdle", "waist", 85, "rare", defence=3),
        "Steel Signet": Item("Steel Signet", "ring", 150, "rare", attack=3, defence=2),
        "Steel Tower Shield": Item("Steel Tower Shield", "shield", 48, "rare", defence=8),
        "Steel Great Helm": Item("Steel Great Helm", "helm", 85, "rare", defence=7),
        "Steel Hauberk": Item("Steel Hauberk", "chest", 125, "rare", defence=11),
        "Steel Greaves": Item("Steel Greaves", "boots", 78, "rare", defence=6),
        "Steel Fists": Item("Steel Fists", "gloves", 95, "rare", defence=5),
        "Steel-Threaded Cape": Item("Steel-Threaded Cape", "back", 105, "rare", defence=6),
        "Steel Tassets": Item("Steel Tassets", "legs", 115, "rare", defence=9),
        "Steel Fauld": Item("Steel Fauld", "waist", 88, "rare", defence=4),
        "Steel Circlet": Item("Steel Circlet", "ring", 155, "rare", attack=4, defence=3),

        ## Consumables
        "Greater Health Potion": Item("Greater Health Potion", "consumable", 45, "rare", effect_type="healing", effect=45, cooldown=3),
        "Elixir of Protection": Item("Elixir of Protection", "consumable", 100, "rare", effect_type="buff", effect=("defence", 15), cooldown=5),

        # Epic tier (Mithril)
        ## Weapons
        "Mithril Greatsword": Item("Mithril Greatsword", "weapon", 250, "epic", attack=25),
        "Mithril Warhammer": Item("Mithril Warhammer", "weapon", 260, "epic", attack=26),
        "Mithril Longbow": Item("Mithril Longbow", "weapon", 270, "epic", attack=27),
        "Mithril Dualblade": Item("Mithril Dualblade", "weapon", 265, "epic", attack=28),
        "Mithril Trident": Item("Mithril Trident", "weapon", 255, "epic", attack=26),
        "Mithril Repeating Crossbow": Item("Mithril Repeating Crossbow", "weapon", 275, "epic", attack=29),
        "Mithril Nodachi": Item("Mithril Nodachi", "weapon", 268, "epic", attack=27),
        "Mithril War Scythe": Item("Mithril War Scythe", "weapon", 272, "epic", attack=28),
        "Mithril Chakram Pair": Item("Mithril Chakram Pair", "weapon", 258, "epic", attack=25),


        ## Armor
        "Mithril Tower Shield": Item("Mithril Tower Shield", "shield", 220, "epic", defence=12),
        "Mithril Full Helm": Item("Mithril Full Helm", "helm", 280, "epic", defence=9),
        "Mithril Plate Armor": Item("Mithril Plate Armor", "chest", 350, "epic", defence=18),
        "Mithril Greaves": Item("Mithril Greaves", "boots", 300, "epic", defence=7),
        "Mithril Gauntlets": Item("Mithril Gauntlets", "gloves", 270, "epic", defence=6),
        "Mithril-Woven Cape": Item("Mithril-Woven Cape", "back", 320, "epic", defence=8),
        "Mithril Leggings": Item("Mithril Leggings", "legs", 330, "epic", defence=14),
        "Mithril Waistguard": Item("Mithril Waistguard", "waist", 290, "epic", defence=5),
        "Mithril Band": Item("Mithril Band", "ring", 400, "epic", attack=5, defence=3),
        "Mithril Aegis": Item("Mithril Aegis", "shield", 230, "epic", defence=13),
        "Mithril Crown": Item("Mithril Crown", "helm", 290, "epic", defence=10),
        "Mithril Cuirass": Item("Mithril Cuirass", "chest", 360, "epic", defence=19),
        "Mithril Sabatons": Item("Mithril Sabatons", "boots", 310, "epic", defence=8),
        "Mithril Vambraces": Item("Mithril Vambraces", "gloves", 280, "epic", defence=7),
        "Mithril Shroud": Item("Mithril Shroud", "back", 330, "epic", defence=9),
        "Mithril Cuisses": Item("Mithril Cuisses", "legs", 340, "epic", defence=15),
        "Mithril Tasset": Item("Mithril Tasset", "waist", 300, "epic", defence=6),
        "Mithril Signet": Item("Mithril Signet", "ring", 410, "epic", attack=6, defence=4),

        ## Consumables
        "Supreme Health Potion": Item("Supreme Health Potion", "consumable", 500, "epic", effect_type="healing", effect=100, cooldown=6),
        "Elixir of Heroes": Item("Elixir of Heroes", "consumable", 600, "epic", effect_type="buff", effect=("all_stats", 20), cooldown=10),

        # Legendary tier (Adamantite)
        ## Weapons
        "Adamantite Runeblade": Item("Adamantite Runeblade", "weapon", 1000, "legendary", attack=40),
        "Adamantite Worldbreaker": Item("Adamantite Worldbreaker", "weapon", 1050, "legendary", attack=42),
        "Adamantite Skypierce": Item("Adamantite Skypierce", "weapon", 1100, "legendary", attack=44),
        "Adamantite Soul Reaver": Item("Adamantite Soul Reaver", "weapon", 1080, "legendary", attack=43),
        "Adamantite Storm Glaive": Item("Adamantite Storm Glaive", "weapon", 1030, "legendary", attack=41),
        "Adamantite Ethereal Bow": Item("Adamantite Ethereal Bow", "weapon", 1120, "legendary", attack=45),
        "Adamantite Void Blade": Item("Adamantite Void Blade", "weapon", 1070, "legendary", attack=42),
        "Adamantite Titan's Fist": Item("Adamantite Titan's Fist", "weapon", 1090, "legendary", attack=44),
        "Adamantite Whisperwind": Item("Adamantite Whisperwind", "weapon", 1040, "legendary", attack=41),

        ## Armor
        "Adamantite Bulwark": Item("Adamantite Bulwark", "shield", 950, "legendary", defence=20),
        "Adamantite Crown": Item("Adamantite Crown", "helm", 1100, "legendary", defence=15),
        "Adamantite Godplate": Item("Adamantite Godplate", "chest", 1300, "legendary", defence=30),
        "Adamantite Striders": Item("Adamantite Striders", "boots", 1200, "legendary", defence=12),
        "Adamantite Fists": Item("Adamantite Fists", "gloves", 1150, "legendary", defence=10),
        "Adamantite Shadowcloak": Item("Adamantite Shadowcloak", "back", 1250, "legendary", defence=14),
        "Adamantite Legguards": Item("Adamantite Legguards", "legs", 1280, "legendary", defence=25),
        "Adamantite Cinch": Item("Adamantite Cinch", "waist", 1180, "legendary", defence=8),
        "Adamantite Loop": Item("Adamantite Loop", "ring", 1500, "legendary", attack=8, defence=5),
        "Adamantite Aegis": Item("Adamantite Aegis", "shield", 980, "legendary", defence=22),
        "Adamantite Diadem": Item("Adamantite Diadem", "helm", 1150, "legendary", defence=17),
        "Adamantite Vanguard": Item("Adamantite Vanguard", "chest", 1350, "legendary", defence=32),
        "Adamantite Treads": Item("Adamantite Treads", "boots", 1220, "legendary", defence=13),
        "Adamantite Crushers": Item("Adamantite Crushers", "gloves", 1180, "legendary", defence=11),
        "Adamantite Veil": Item("Adamantite Veil", "back", 1270, "legendary", defence=15),
        "Adamantite Cuisses": Item("Adamantite Cuisses", "legs", 1300, "legendary", defence=27),
        "Adamantite Girdle": Item("Adamantite Girdle", "waist", 1200, "legendary", defence=9),
        "Adamantite Seal": Item("Adamantite Seal", "ring", 1550, "legendary", attack=9, defence=6),

        ## Consumables
        "Godly Restoration Flask": Item("Godly Restoration Flask", "consumable", 2000, "legendary", effect_type="healing", effect=250, cooldown=12),
        "Elixir of Transcendence": Item("Elixir of Transcendence", "consumable", 2500, "legendary", effect_type="buff", effect=("all_stats", 50), cooldown=20),

        # Mythical tier (Unique names)
        ## Weapons
        "Worldsplitter": Item("Worldsplitter", "weapon", 5000, "mythical", attack=100),
        "Destiny's Call": Item("Destiny's Call", "weapon", 5200, "mythical", attack=105),
        "Eternity's Edge": Item("Eternity's Edge", "weapon", 5400, "mythical", attack=110),
        "Oblivion's Embrace": Item("Oblivion's Embrace", "weapon", 5300, "mythical", attack=107),
        "Starforged Annihilator": Item("Starforged Annihilator", "weapon", 5500, "mythical", attack=112),
        "Whisper of the Void": Item("Whisper of the Void", "weapon", 5100, "mythical", attack=103),
        "Fang of the Cosmos": Item("Fang of the Cosmos", "weapon", 5250, "mythical", attack=106),
        "Harmony's Discord": Item("Harmony's Discord", "weapon", 5350, "mythical", attack=108),
        "Apocalypse Incarnate": Item("Apocalypse Incarnate", "weapon", 5450, "mythical", attack=111),

        ## Armor
        "Aegis of the Cosmos": Item("Aegis of the Cosmos", "shield", 4800, "mythical", defence=50),
        "Crown of Infinite Wisdom": Item("Crown of Infinite Wisdom", "helm", 5200, "mythical", defence=30),
        "Vestment of Universal Constants": Item("Vestment of Universal Constants", "chest", 5500, "mythical", defence=60),
        "Boots of Boundless Journey": Item("Boots of Boundless Journey", "boots", 5300, "mythical", defence=25),
        "Gauntlets of Primordial Might": Item("Gauntlets of Primordial Might", "gloves", 5100, "mythical", defence=20),
        "Cloak of Celestial Shadows": Item("Cloak of Celestial Shadows", "back", 5400, "mythical", defence=28),
        "Leggings of Cosmic Balance": Item("Leggings of Cosmic Balance", "legs", 5350, "mythical", defence=45),
        "Girdle of Worldly Axis": Item("Girdle of Worldly Axis", "waist", 5250, "mythical", defence=15),
        "Band of Divine Providence": Item("Band of Divine Providence", "ring", 6000, "mythical", attack=15, defence=10),
        "Bulwark of Eternal Defiance": Item("Bulwark of Eternal Defiance", "shield", 4900, "mythical", defence=55),
        "Diadem of Omniscient Thought": Item("Diadem of Omniscient Thought", "helm", 5250, "mythical", defence=32),
        "Cuirass of the Unbreakable Will": Item("Cuirass of the Unbreakable Will", "chest", 5600, "mythical", defence=65),
        "Sabatons of the Astral Strider": Item("Sabatons of the Astral Strider", "boots", 5350, "mythical", defence=27),
        "Vambraces of Cosmic Manipulation": Item("Vambraces of Cosmic Manipulation", "gloves", 5150, "mythical", defence=22),
        "Mantle of Ethereal Whispers": Item("Mantle of Ethereal Whispers", "back", 5450, "mythical", defence=30),
        "Tassets of Reality's Anchor": Item("Tassets of Reality's Anchor", "legs", 5400, "mythical", defence=48),
        "Cincture of Dimensional Stability": Item("Cincture of Dimensional Stability", "waist", 5300, "mythical", defence=17),
        "Signet of Cosmic Influence": Item("Signet of Cosmic Influence", "ring", 6100, "mythical", attack=17, defence=12),

        ## Consumables
        "Essence of Eternity": Item("Essence of Eternity", "consumable", 10000, "mythical", effect_type="healing", effect=1000, cooldown=50),
        "Elixir of Omnipotence": Item("Elixir of Omnipotence", "consumable", 15000, "mythical", effect_type="buff", effect=("all_stats", 100), cooldown=100),
    }