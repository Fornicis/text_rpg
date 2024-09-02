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
            #Starter items
            "Peasants Top": Item("Peasants Top", "chest", 0, "starter", defence=1),
            "Peasants Bottoms": Item("Peasants Bottoms", "legs", 0, "starter", defence=1),
            "Wooden Sword": Item("Wooden Sword", "weapon", 0, "starter", attack=2),
            #Low tier weapons
            "Rusty Sword": Item("Rusty Sword", "weapon", 20, "common", attack=5),
            "Wooden Club": Item("Wooden Club", "weapon", 15, "common", attack=4),
            "Farmer's Pitchfork": Item("Farmer's Pitchfork", "weapon", 18, "common", attack=6),
            "Sling": Item("Sling", "weapon", 22, "common", attack=3),
            "Rusty Dagger": Item("Rusty Dagger", "weapon", 16, "common", attack=4),

            #Low tier armour
            "Wooden Shield": Item("Wooden Shield", "shield", 15, "common", defence=2),
            "Leather Helm": Item("Leather Helm", "helm", 10, "common", defence=1),
            "Padded Vest": Item("Padded Vest", "chest", 25, "common", defence=3),
            "Leather Boots": Item("Leather Boots", "boots", 12, "common", defence=1),
            "Cloth Gloves": Item("Cloth Gloves", "gloves", 8, "common", defence=1),
            "Tattered Cloak": Item("Tattered Cloak", "back", 14, "common", defence=1),
            "Leather Leggins": Item("Leather Leggings", "legs", 12, "common", defence=2),
            #Low tier consumables
            "Basic Health Potion": Item("Basic Health Potion", "consumable", 15, "common", effect_type="healing", effect=20, cooldown=3),
            "Fire Bomb": Item("Fire Bomb", "consumable", 30, "common",effect_type="damage", effect=20, cooldown=2),
            "Stone of Courage": Item("Stone of Courage", "consumable", 35, "common", effect_type="buff", effect=("attack", 5), cooldown=6),
            #Medium tier items
            "Steel Sword": Item("Steel Sword", "weapon", 100, "uncommon", attack=15),
            "Kite Shield": Item("Kite Shield", "shield", 80, "uncommon", defence=8),
            #High tier
            "Enchanted Blade": Item("Enchanted Blade", "weapon", 300, "rare", attack=25),
            "Dragon Shield": Item("Dragon Shield", "shield", 250, "rare", defence=15),
            "Elixir of Life": Item("Elixir of Life", "consumable", 120, "rare", effect_type="healing", effect=100, cooldown=3),
        }