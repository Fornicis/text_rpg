class Item:
    def __init__(self, name, item_type, value, tier, attack=0, defence=0, effect_type=None, effect=0, cooldown=0, duration=0, tick_effect=0, weapon_type=None):
        self.name = name
        self.type = item_type
        self.value = value
        self.tier = tier
        self.attack = attack
        self.defence = defence
        self.effect_type = effect_type
        self.effect = effect
        self.cooldown = cooldown
        self.duration = duration
        self.tick_effect = tick_effect
        self.weapon_type = weapon_type
        
def initialise_items():
    return {
        # Starter items
        "Peasants Top": Item("Peasants Top", "chest", 0, "starter", defence=1),
        "Peasants Bottoms": Item("Peasants Bottoms", "legs", 0, "starter", defence=1),
        "Wooden Sword": Item("Wooden Sword", "weapon", 0, "starter", attack=2),

        # Weapons
        # Common
        "Leather Garrote": Item("Leather Garrote", "weapon", 14, "common", attack=3),
        "Leather Knuckles": Item("Leather Knuckles", "weapon", 13, "common", attack=3),
        "Leather Sling": Item("Leather Sling", "weapon", 15, "common", attack=4),
        "Leather Sap": Item("Leather Sap", "weapon", 16, "common", attack=4),
        "Wooden Blowgun": Item("Wooden Blowgun", "weapon", 18, "common", attack=4),
        "Wooden Boomerang": Item("Wooden Boomerang", "weapon", 17, "common", attack=4),
        "Leather Strap Mace": Item("Leather Strap Mace", "weapon", 19, "common", attack=5),
        "Leather Whip": Item("Leather Whip", "weapon", 20, "common", attack=5),
        "Leather Bound Axe": Item("Leather Bound Axe", "weapon", 21, "common", attack=5),
        "Leather Bound Club": Item("Leather Bound Club", "weapon", 18, "common", attack=6),
        "Wooden Javelin": Item("Wooden Javelin", "weapon", 24, "common", attack=6),
        "Wooden Quarterstaff": Item("Wooden Quarterstaff", "weapon", 23, "common", attack=6),
        "Wooden Spear": Item("Wooden Spear", "weapon", 22, "common", attack=6),
        "Leather Flail": Item("Leather Flail", "weapon", 26, "common", attack=7),
        "Wooden Bow": Item("Wooden Bow", "weapon", 25, "common", attack=7),

        # Uncommon
        "Bronze Falchion": Item("Bronze Falchion", "weapon", 34, "uncommon", attack=9),
        "Bronze Shortsword": Item("Bronze Shortsword", "weapon", 33, "uncommon", attack=9),
        "Bronze Kopis": Item("Bronze Kopis", "weapon", 35, "uncommon", attack=10),
        "Bronze Scimitar": Item("Bronze Scimitar", "weapon", 36, "uncommon", attack=10),
        "Bronze Sword": Item("Bronze Sword", "weapon", 35, "uncommon", attack=10),
        "Bronze Xiphos": Item("Bronze Xiphos", "weapon", 36, "uncommon", attack=10),
        "Bronze Rapier": Item("Bronze Rapier", "weapon", 37, "uncommon", attack=11),
        "Iron Flail": Item("Iron Flail", "weapon", 39, "uncommon", attack=11),
        "Iron Mace": Item("Iron Mace", "weapon", 40, "uncommon", attack=11),
        "Bronze Khopesh": Item("Bronze Khopesh", "weapon", 39, "uncommon", attack=11),
        "Bronze Halberd": Item("Bronze Halberd", "weapon", 41, "uncommon", attack=12),
        "Bronze Spear": Item("Bronze Spear", "weapon", 38, "uncommon", attack=12),
        "Iron Pike": Item("Iron Pike", "weapon", 40, "uncommon", attack=12),
        "Iron Battleaxe": Item("Iron Battleaxe", "weapon", 42, "uncommon", attack=13),
        "Iron Glaive": Item("Iron Glaive", "weapon", 43, "uncommon", attack=13),
        "Iron Maul": Item("Iron Maul", "weapon", 44, "uncommon", attack=14),
        "Iron Warhammer": Item("Iron Warhammer", "weapon", 45, "uncommon", attack=14),
        "Iron War Scythe": Item("Iron War Scythe", "weapon", 45, "uncommon", attack=14),
        "Iron Bardiche": Item("Iron Bardiche", "weapon", 46, "uncommon", attack=15),
        "Iron Lucerne Hammer": Item("Iron Lucerne Hammer", "weapon", 47, "uncommon", attack=15),

        # Rare
        "Steel Chakram": Item("Steel Chakram", "weapon", 63, "rare", attack=15),
        "Steel Longsword": Item("Steel Longsword", "weapon", 60, "rare", attack=15),
        "Steel Battleaxe": Item("Steel Battleaxe", "weapon", 65, "rare", attack=16),
        "Steel Katana": Item("Steel Katana", "weapon", 67, "rare", attack=16),
        "Steel Bow": Item("Steel Bow", "weapon", 70, "rare", attack=17),
        "Steel Halberd": Item("Steel Halberd", "weapon", 72, "rare", attack=17),
        "Steel Warhammer": Item("Steel Warhammer", "weapon", 68, "rare", attack=18),
        "Steel Crossbow": Item("Steel Crossbow", "weapon", 75, "rare", attack=18),
        "Steel Claymore": Item("Steel Claymore", "weapon", 71, "rare", attack=19),

        # Epic
        "Mithril Chakram Pair": Item("Mithril Chakram Pair", "weapon", 258, "epic", attack=25),
        "Mithril Greatsword": Item("Mithril Greatsword", "weapon", 250, "epic", attack=25),
        "Mithril Trident": Item("Mithril Trident", "weapon", 255, "epic", attack=26),
        "Mithril Warhammer": Item("Mithril Warhammer", "weapon", 260, "epic", attack=26),
        "Mithril Longbow": Item("Mithril Longbow", "weapon", 270, "epic", attack=27),
        "Mithril Nodachi": Item("Mithril Nodachi", "weapon", 268, "epic", attack=27),
        "Mithril Dualblade": Item("Mithril Dualblade", "weapon", 265, "epic", attack=28),
        "Mithril War Scythe": Item("Mithril War Scythe", "weapon", 272, "epic", attack=28),
        "Mithril Repeating Crossbow": Item("Mithril Repeating Crossbow", "weapon", 275, "epic", attack=29),

        # Legendary
        "Adamantite Runeblade": Item("Adamantite Runeblade", "weapon", 1000, "legendary", attack=40),
        "Adamantite Storm Glaive": Item("Adamantite Storm Glaive", "weapon", 1030, "legendary", attack=41),
        "Adamantite Whisperwind": Item("Adamantite Whisperwind", "weapon", 1040, "legendary", attack=41),
        "Adamantite Void Blade": Item("Adamantite Void Blade", "weapon", 1070, "legendary", attack=42),
        "Adamantite Worldbreaker": Item("Adamantite Worldbreaker", "weapon", 1050, "legendary", attack=42),
        "Adamantite Soul Reaver": Item("Adamantite Soul Reaver", "weapon", 1080, "legendary", attack=43),
        "Adamantite Titan's Fist": Item("Adamantite Titan's Fist", "weapon", 1090, "legendary", attack=44),
        "Adamantite Skypierce": Item("Adamantite Skypierce", "weapon", 1100, "legendary", attack=44),
        "Adamantite Ethereal Bow": Item("Adamantite Ethereal Bow", "weapon", 1120, "legendary", attack=45),

        # Mythical
        "Worldsplitter": Item("Worldsplitter", "weapon", 5000, "mythical", attack=100),
        "Whisper of the Void": Item("Whisper of the Void", "weapon", 5100, "mythical", attack=103),
        "Destiny's Call": Item("Destiny's Call", "weapon", 5200, "mythical", attack=105),
        "Fang of the Cosmos": Item("Fang of the Cosmos", "weapon", 5250, "mythical", attack=106),
        "Oblivion's Embrace": Item("Oblivion's Embrace", "weapon", 5300, "mythical", attack=107),
        "Harmony's Discord": Item("Harmony's Discord", "weapon", 5350, "mythical", attack=108),
        "Eternity's Edge": Item("Eternity's Edge", "weapon", 5400, "mythical", attack=110),
        "Apocalypse Incarnate": Item("Apocalypse Incarnate", "weapon", 5450, "mythical", attack=111),
        "Starforged Annihilator": Item("Starforged Annihilator", "weapon", 5500, "mythical", attack=112),
        
        # Helm
        "Leather Cap": Item("Leather Cap", "helm", 9, "common", defence=1),
        "Leather Helm": Item("Leather Helm", "helm", 10, "common", defence=1),
        "Bronze Coif": Item("Bronze Coif", "helm", 38, "uncommon", defence=2),
        "Iron Helm": Item("Iron Helm", "helm", 40, "uncommon", defence=3),
        "Steel Helm": Item("Steel Helm", "helm", 80, "rare", defence=6),
        "Steel Great Helm": Item("Steel Great Helm", "helm", 85, "rare", defence=7),
        "Mithril Full Helm": Item("Mithril Full Helm", "helm", 280, "epic", defence=9),
        "Mithril Crown": Item("Mithril Crown", "helm", 290, "epic", defence=10),
        "Adamantite Crown": Item("Adamantite Crown", "helm", 1100, "legendary", defence=15),
        "Adamantite Diadem": Item("Adamantite Diadem", "helm", 1150, "legendary", defence=17),
        "Crown of Infinite Wisdom": Item("Crown of Infinite Wisdom", "helm", 5200, "mythical", defence=30),
        "Diadem of Omniscient Thought": Item("Diadem of Omniscient Thought", "helm", 5250, "mythical", defence=32),

        # Chest
        "Leather Vest": Item("Leather Vest", "chest", 22, "common", defence=2),
        "Leather Chest": Item("Leather Chest", "chest", 25, "common", defence=3),
        "Bronze Chestplate": Item("Bronze Chestplate", "chest", 55, "uncommon", defence=6),
        "Iron Cuirass": Item("Iron Cuirass", "chest", 58, "uncommon", defence=5),
        "Steel Breastplate": Item("Steel Breastplate", "chest", 120, "rare", defence=10),
        "Steel Hauberk": Item("Steel Hauberk", "chest", 125, "rare", defence=11),
        "Mithril Plate Armour": Item("Mithril Plate Armour", "chest", 350, "epic", defence=18),
        "Mithril Cuirass": Item("Mithril Cuirass", "chest", 360, "epic", defence=19),
        "Adamantite Godplate": Item("Adamantite Godplate", "chest", 1300, "legendary", defence=30),
        "Adamantite Vanguard": Item("Adamantite Vanguard", "chest", 1350, "legendary", defence=32),
        "Vestment of Universal Constants": Item("Vestment of Universal Constants", "chest", 5500, "mythical", defence=60),
        "Cuirass of the Unbreakable Will": Item("Cuirass of the Unbreakable Will", "chest", 5600, "mythical", defence=65),

        # Belt
        "Leather Belt": Item("Leather Belt", "belt", 10, "common", defence=1),
        "Bronze Girdle": Item("Bronze Girdle", "belt", 33, "uncommon", defence=2),
        "Iron Belt": Item("Iron Belt", "belt", 35, "uncommon", defence=2),
        "Steel Girdle": Item("Steel Girdle", "belt", 85, "rare", defence=3),
        "Steel Fauld": Item("Steel Fauld", "belt", 88, "rare", defence=4),
        "Mithril Waistguard": Item("Mithril Waistguard", "belt", 290, "epic", defence=5),
        "Mithril Tasset": Item("Mithril Tasset", "belt", 300, "epic", defence=6),
        "Adamantite Cinch": Item("Adamantite Cinch", "belt", 1180, "legendary", defence=8),
        "Adamantite Girdle": Item("Adamantite Girdle", "belt", 1200, "legendary", defence=9),
        "Girdle of Worldly Axis": Item("Girdle of Worldly Axis", "belt", 5250, "mythical", defence=15),
        "Cincture of Dimensional Stability": Item("Cincture of Dimensional Stability", "belt", 5300, "mythical", defence=17),

        # Legs
        "Leather Skirt": Item("Leather Skirt", "legs", 11, "common", defence=1),
        "Leather Leggings": Item("Leather Leggings", "legs", 12, "common", defence=2),
        "Bronze Greaves": Item("Bronze Greaves", "legs", 50, "uncommon", defence=4),
        "Iron Cuisses": Item("Iron Cuisses", "legs", 48, "uncommon", defence=3),
        "Steel Cuisses": Item("Steel Cuisses", "legs", 110, "rare", defence=8),
        "Steel Tassets": Item("Steel Tassets", "legs", 115, "rare", defence=9),
        "Mithril Leggings": Item("Mithril Leggings", "legs", 330, "epic", defence=14),
        "Mithril Cuisses": Item("Mithril Cuisses", "legs", 340, "epic", defence=15),
        "Adamantite Legguards": Item("Adamantite Legguards", "legs", 1280, "legendary", defence=25),
        "Adamantite Cuisses": Item("Adamantite Cuisses", "legs", 1300, "legendary", defence=27),
        "Leggings of Cosmic Balance": Item("Leggings of Cosmic Balance", "legs", 5350, "mythical", defence=45),
        "Tassets of Reality's Anchor": Item("Tassets of Reality's Anchor", "legs", 5400, "mythical", defence=48),

        # Boots
        "Leather Sandals": Item("Leather Sandals", "boots", 11, "common", defence=1),
        "Leather Boots": Item("Leather Boots", "boots", 12, "common", defence=1),
        "Bronze Sabatons": Item("Bronze Sabatons", "boots", 33, "uncommon", defence=2),
        "Iron Boots": Item("Iron Boots", "boots", 35, "uncommon", defence=3),
        "Steel Sabatons": Item("Steel Sabatons", "boots", 75, "rare", defence=5),
        "Steel Greaves": Item("Steel Greaves", "boots", 78, "rare", defence=6),
        "Mithril Greaves": Item("Mithril Greaves", "boots", 300, "epic", defence=7),
        "Mithril Sabatons": Item("Mithril Sabatons", "boots", 310, "epic", defence=8),
        "Adamantite Striders": Item("Adamantite Striders", "boots", 1200, "legendary", defence=12),
        "Adamantite Treads": Item("Adamantite Treads", "boots", 1220, "legendary", defence=13),
        "Boots of Boundless Journey": Item("Boots of Boundless Journey", "boots", 5300, "mythical", defence=25),
        "Sabatons of the Astral Strider": Item("Sabatons of the Astral Strider", "boots", 5350, "mythical", defence=27),

        # Gloves
        "Leather Bracers": Item("Leather Bracers", "gloves", 7, "common", defence=1),
        "Leather Gloves": Item("Leather Gloves", "gloves", 8, "common", defence=1),
        "Bronze Gauntlets": Item("Bronze Gauntlets", "gloves", 30, "uncommon", defence=2),
        "Iron Vambraces": Item("Iron Vambraces", "gloves", 28, "uncommon", defence=2),
        "Steel Gauntlets": Item("Steel Gauntlets", "gloves", 90, "rare", defence=4),
        "Steel Fists": Item("Steel Fists", "gloves", 95, "rare", defence=5),
        "Mithril Gauntlets": Item("Mithril Gauntlets", "gloves", 270, "epic", defence=6),
        "Mithril Vambraces": Item("Mithril Vambraces", "gloves", 280, "epic", defence=7),
        "Adamantite Fists": Item("Adamantite Fists", "gloves", 1150, "legendary", defence=10),
        "Adamantite Crushers": Item("Adamantite Crushers", "gloves", 1180, "legendary", defence=11),
        "Gauntlets of Primordial Might": Item("Gauntlets of Primordial Might", "gloves", 5100, "mythical", defence=20),
        "Vambraces of Cosmic Manipulation": Item("Vambraces of Cosmic Manipulation", "gloves", 5150, "mythical", defence=22),

        # Shield
        "Leather Shield": Item("Leather Shield", "shield", 15, "common", defence=2),
        "Bronze Shield": Item("Bronze Shield", "shield", 30, "uncommon", defence=4),
        "Iron Buckler": Item("Iron Buckler", "shield", 32, "uncommon", defence=3),
        "Steel Kite Shield": Item("Steel Kite Shield", "shield", 45, "rare", defence=7),
        "Steel Tower Shield": Item("Steel Tower Shield", "shield", 48, "rare", defence=8),
        "Mithril Tower Shield": Item("Mithril Tower Shield", "shield", 220, "epic", defence=12),
        "Mithril Aegis": Item("Mithril Aegis", "shield", 230, "epic", defence=13),
        "Adamantite Bulwark": Item("Adamantite Bulwark", "shield", 950, "legendary", defence=20),
        "Adamantite Aegis": Item("Adamantite Aegis", "shield", 980, "legendary", defence=22),
        "Aegis of the Cosmos": Item("Aegis of the Cosmos", "shield", 4800, "mythical", defence=50),
        "Bulwark of Eternal Defiance": Item("Bulwark of Eternal Defiance", "shield", 4900, "mythical", defence=55),

        # Back
        "Leather Poncho": Item("Leather Poncho", "back", 13, "common", defence=1),
        "Leather Cloak": Item("Leather Cloak", "back", 14, "common", defence=1),
        "Bronze-Weave Mantle": Item("Bronze-Weave Mantle", "back", 43, "uncommon", defence=2),
        "Iron-Trimmed Cloak": Item("Iron-Trimmed Cloak", "back", 45, "uncommon", defence=3),
        "Reinforced Cloak": Item("Reinforced Cloak", "back", 100, "rare", defence=5),
        "Steel-Threaded Cape": Item("Steel-Threaded Cape", "back", 105, "rare", defence=6),
        "Mithril-Woven Cape": Item("Mithril-Woven Cape", "back", 320, "epic", defence=8),
        "Mithril Shroud": Item("Mithril Shroud", "back", 330, "epic", defence=9),
        "Adamantite Shadowcloak": Item("Adamantite Shadowcloak", "back", 1250, "legendary", defence=14),
        "Adamantite Veil": Item("Adamantite Veil", "back", 1270, "legendary", defence=15),
        "Cloak of Celestial Shadows": Item("Cloak of Celestial Shadows", "back", 5400, "mythical", defence=28),
        "Mantle of Ethereal Whispers": Item("Mantle of Ethereal Whispers", "back", 5450, "mythical", defence=30),

        # Ring
        "Leather Armband": Item("Leather Armband", "ring", 18, "common", attack=1, defence=1),
        "Leather Wristband": Item("Leather Wristband", "ring", 20, "common", attack=1, defence=1),
        "Bronze Ring": Item("Bronze Ring", "ring", 60, "uncommon", attack=2, defence=1),
        "Iron Band": Item("Iron Band", "ring", 58, "uncommon", attack=1, defence=2),
        "Steel Signet": Item("Steel Signet", "ring", 150, "rare", attack=3, defence=2),
        "Steel Circlet": Item("Steel Circlet", "ring", 155, "rare", attack=4, defence=3),
        "Mithril Band": Item("Mithril Band", "ring", 400, "epic", attack=5, defence=3),
        "Mithril Signet": Item("Mithril Signet", "ring", 410, "epic", attack=6, defence=4),
        "Adamantite Loop": Item("Adamantite Loop", "ring", 1500, "legendary", attack=8, defence=5),
        "Adamantite Seal": Item("Adamantite Seal", "ring", 1550, "legendary", attack=9, defence=6),
        "Band of Divine Providence": Item("Band of Divine Providence", "ring", 6000, "mythical", attack=15, defence=10),
        "Signet of Cosmic Influence": Item("Signet of Cosmic Influence", "ring", 6100, "mythical", attack=17, defence=12),

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

        # Epic
        "Supreme Health Potion": Item("Supreme Health Potion", "consumable", 500, "epic", effect_type="healing", effect=160, cooldown=6),
        "Quicksilver Healing Tincture": Item("Quicksilver Healing Tincture", "consumable", 375, "epic", effect_type="healing", effect=96, cooldown=3),
        "Arcane Rejuvenation Brew": Item("Arcane Rejuvenation Brew", "consumable", 425, "epic", effect_type="healing", effect=128, cooldown=4),
        "Ethereal Mending Mist": Item("Ethereal Mending Mist", "consumable", 300, "epic", effect_type="healing", effect=80, cooldown=2),

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
        "Supreme Vitality Brew": Item("Supreme Vitality Brew", "consumable", 400, "epic", effect_type="hot", effect=0, cooldown=8, duration=10, tick_effect=25),
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
        
        # Epic
        "Arcane Detonator": Item("Arcane Detonator", "consumable", 600, "epic", effect_type="damage", effect=200, cooldown=5),
        "Elemental Surge": Item("Elemental Surge", "consumable", 450, "epic", effect_type="damage", effect=120, cooldown=4),
        "Chaos Orb": Item("Chaos Orb", "consumable", 350, "epic", effect_type="damage", effect=80, cooldown=3),
        "Astral Shard": Item("Astral Shard", "consumable", 300, "epic", effect_type="damage", effect=60, cooldown=2),
        "Ethereal Dart": Item("Ethereal Dart", "consumable", 250, "epic", effect_type="damage", effect=40, cooldown=1),
        
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
        "Minor Strength Tonic": Item("Minor Strength Tonic", "consumable", 20, "common", effect_type="buff", effect=("attack", 5), cooldown=5),
        "Minor Iron Skin Elixir": Item("Minor Iron Skin Elixir", "consumable", 20, "common", effect_type="buff", effect=("defence", 5), cooldown=5),
        "Minor Warrior's Brew": Item("Minor Warrior's Brew", "consumable", 25, "common", effect_type="buff", effect=("all stats", 2), cooldown=5),
        "Quick Strength Drop": Item("Quick Strength Drop", "consumable", 15, "common", effect_type="buff", effect=("attack", 3), cooldown=2),
        "Quick Iron Skin Drop": Item("Quick Iron Skin Drop", "consumable", 15, "common", effect_type="buff", effect=("defence", 3), cooldown=2),
        "Quick Warrior's Drop": Item("Quick Warrior's Drop", "consumable", 18, "common", effect_type="buff", effect=("all stats", 1), cooldown=2),

        # Uncommon
        "Strength Tonic": Item("Strength Tonic", "consumable", 40, "uncommon", effect_type="buff", effect=("attack", 10), cooldown=6),
        "Iron Skin Elixir": Item("Iron Skin Elixir", "consumable", 40, "uncommon", effect_type="buff", effect=("defence", 10), cooldown=6),
        "Warrior's Brew": Item("Warrior's Brew", "consumable", 50, "uncommon", effect_type="buff", effect=("all stats", 5), cooldown=6),
        "Swift Strength Vial": Item("Swift Strength Vial", "consumable", 30, "uncommon", effect_type="buff", effect=("attack", 6), cooldown=3),
        "Swift Iron Skin Vial": Item("Swift Iron Skin Vial", "consumable", 30, "uncommon", effect_type="buff", effect=("defence", 6), cooldown=3),
        "Swift Warrior's Vial": Item("Swift Warrior's Vial", "consumable", 35, "uncommon", effect_type="buff", effect=("all stats", 3), cooldown=3),

        # Rare
        "Greater Strength Tonic": Item("Greater Strength Tonic", "consumable", 80, "rare", effect_type="buff", effect=("attack", 20), cooldown=7),
        "Greater Iron Skin Elixir": Item("Greater Iron Skin Elixir", "consumable", 80, "rare", effect_type="buff", effect=("defence", 20), cooldown=7),
        "Greater Warrior's Brew": Item("Greater Warrior's Brew", "consumable", 100, "rare", effect_type="buff", effect=("all stats", 10), cooldown=7),
        "Rapid Strength Essence": Item("Rapid Strength Essence", "consumable", 60, "rare", effect_type="buff", effect=("attack", 12), cooldown=3),
        "Rapid Iron Skin Essence": Item("Rapid Iron Skin Essence", "consumable", 60, "rare", effect_type="buff", effect=("defence", 12), cooldown=3),
        "Rapid Warrior's Essence": Item("Rapid Warrior's Essence", "consumable", 75, "rare", effect_type="buff", effect=("all stats", 6), cooldown=3),

        # Epic
        "Epic Strength Tonic": Item("Epic Strength Tonic", "consumable", 400, "epic", effect_type="buff", effect=("attack", 40), cooldown=8),
        "Epic Iron Skin Elixir": Item("Epic Iron Skin Elixir", "consumable", 400, "epic", effect_type="buff", effect=("defence", 40), cooldown=8),
        "Epic Warrior's Brew": Item("Epic Warrior's Brew", "consumable", 500, "epic", effect_type="buff", effect=("all stats", 20), cooldown=8),
        "Quicksilver Strength Philter": Item("Quicksilver Strength Philter", "consumable", 300, "epic", effect_type="buff", effect=("attack", 24), cooldown=4),
        "Quicksilver Iron Skin Philter": Item("Quicksilver Iron Skin Philter", "consumable", 300, "epic", effect_type="buff", effect=("defence", 24), cooldown=4),
        "Quicksilver Warrior's Philter": Item("Quicksilver Warrior's Philter", "consumable", 375, "epic", effect_type="buff", effect=("all stats", 12), cooldown=4),

        # Legendary
        "Legendary Strength Tonic": Item("Legendary Strength Tonic", "consumable", 1600, "legendary", effect_type="buff", effect=("attack", 80), cooldown=10),
        "Legendary Iron Skin Elixir": Item("Legendary Iron Skin Elixir", "consumable", 1600, "legendary", effect_type="buff", effect=("defence", 80), cooldown=10),
        "Legendary Warrior's Brew": Item("Legendary Warrior's Brew", "consumable", 2000, "legendary", effect_type="buff", effect=("all stats", 40), cooldown=10),
        "Celestial Strength Ampoule": Item("Celestial Strength Ampoule", "consumable", 1200, "legendary", effect_type="buff", effect=("attack", 48), cooldown=5),
        "Celestial Iron Skin Ampoule": Item("Celestial Iron Skin Ampoule", "consumable", 1200, "legendary", effect_type="buff", effect=("defence", 48), cooldown=5),
        "Celestial Warrior's Ampoule": Item("Celestial Warrior's Ampoule", "consumable", 1500, "legendary", effect_type="buff", effect=("all stats", 24), cooldown=5),

        # Mythical
        "Godly Strength Tonic": Item("Godly Strength Tonic", "consumable", 8000, "mythical", effect_type="buff", effect=("attack", 160), cooldown=15),
        "Godly Iron Skin Elixir": Item("Godly Iron Skin Elixir", "consumable", 8000, "mythical", effect_type="buff", effect=("defence", 160), cooldown=15),
        "Godly Warrior's Brew": Item("Godly Warrior's Brew", "consumable", 10000, "mythical", effect_type="buff", effect=("all stats", 80), cooldown=15),
        "Divine Strength Infusion": Item("Divine Strength Infusion", "consumable", 6000, "mythical", effect_type="buff", effect=("attack", 96), cooldown=7),
        "Divine Iron Skin Infusion": Item("Divine Iron Skin Infusion", "consumable", 6000, "mythical", effect_type="buff", effect=("attack", 96), cooldown=7),
        "Divine Warrior's Infusion": Item("Divine Warrior's Infusion", "consumable", 7500, "mythical", effect_type="buff", effect=("all stats", 48), cooldown=7),
    }