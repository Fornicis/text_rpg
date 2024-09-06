class WorldMap:
    def __init__(self):
        self._game_map = {
            #Home
            "Village": {"enemies": [], "connected_to": ["Forest", "Plains"]},
            #Easy Monster Areas
            "Deepwoods": {"enemies": ["Wood Spirit", "Deepwood Stalker", "Deep Bat", "Giant Firefly", "Treant"], "connected_to": ["Forest", "Swamp"]},
            "Cave": {"enemies": ["Bat", "Goblin", "Spider", "Slime", "Frog"], "connected_to": ["Plains", "Temple"]},
            "Forest": {"enemies": ["Tree Sprite", "Snake", "Forest Hawk", "Locust", "Leprechaun"], "connected_to": ["Village", "Mountain"]},
            "Plains": {"enemies": ["Rat", "Boar", "Plains Hawk", "Strider", "Bull"], "connected_to": ["Village", "Desert"]},
            #Medium Monster Areas
            "Swamp": {"enemies": ["Alligator", "Poison Frog", "Swamp Troll", "Mosquito Swarm", "Bog Witch"], "connected_to": ["Deepwoods", "Toxic Swamp"]},
            "Temple": {"enemies": ["Stone Golem", "Cultist", "Mummy", "Animated Statue", "Temple Guardian"], "connected_to": ["Cave", "Ruins"]},
            "Mountain": {"enemies": ["Mountain Lion", "Rock Elemental", "Harpy", "Yeti", "Orc"], "connected_to": ["Forest", "Valley", "Mountain Peaks"]},
            "Desert": {"enemies": ["Sand Wurm", "Dried Mummy", "Dust Devil", "Desert Bandit", "Leopard"], "connected_to": ["Plains", "Valley", "Scorching Plains"]},
            #Medium-Hard Monster Areas
            "Valley": {"enemies": ["Canyon Cougar", "Twisted Mesquite", "Dust Devil", "Petrified Warrior", "Thunderbird"], "connected_to": ["Mountain", "Desert", "Shadowed Valley"]},
            #Hard Monster Areas
            "Toxic Swamp": {"enemies": ["Venomous Hydra", "Plague Bearer", "Mire Leviathan", "Toxic Shambler", "Swamp Hag"], "connected_to": ["Swamp", "Death Caves"]},
            "Ruins": {"enemies": ["Ancient Golem", "Cursed Pharaoh", "Temporal Anomaly", "Ruin Wraith", "Forgotten Titan"], "connected_to": ["Temple", "Ancient Ruins"]},
            "Mountain Peaks": {"enemies": ["Frost Giant", "Storm Harpy", "Avalanche Elemental", "Mountain Wyvern", "Yeti Alpha"], "connected_to": ["Mountain", "Dragons Lair"]},
            "Scorching Plains": {"enemies": ["Fire Elemental", "Sandstorm Djinn", "Mirage Assassin", "Sunburst Phoenix", "Desert Colossus"], "connected_to": ["Desert", "Death Valley"]},
            "Shadowed Valley": {"enemies": ["Nightmare Stalker", "Void Weaver", "Shadow Dragon", "Ethereal Banshee", "Abyssal Behemoth"], "connected_to": ["Valley", "Volcanic Valley"]},
            #Very Hard Monster Areas
            "Death Caves": {"enemies": ["Necropolis Guardian", "Soul Reaver", "Bone Colossus", "Spectral Devourer", "Lich King"], "connected_to": []},
            "Ancient Ruins": {"enemies": ["Timeless Sphinx", "Eternal Pharaoh", "Anubis Reborn", "Mummy Emperor", "Living Obelisk"], "connected_to": ["Desert"]},
            "Death Valley": {"enemies": ["Apocalypse Horseman", "Abyssal Wyrm", "Void Titan", "Chaos Incarnate", "Eternity Warden"], "connected_to": ["Scorching Plains", "Ancient Ruins", "Volcanic Valley"]},
            "Dragons Lair": {"enemies": ["Ancient Wyvern", "Elemental Drake", "Dragonlord", "Chromatic Dragon", "Elder Dragon"], "connected_to": ["Mountain Peaks", "Death Caves", "Volcanic Valley"]},
            #Extreme Monster Areas
            "Volcanic Valley": {"enemies": ["Magma Colossus", "Phoenix Overlord", "Volcanic Titan", "Inferno Wyrm", "Cinder Archfiend"], "connected_to": ["Shadowed Valley", "Death Valley", "Dragons Lair", "The Heavens"]},
            #Boss Monster Area
            "The Heavens": {"enemies": ["Seraphim Guardian", "Celestial Arbiter", "Astral Demiurge", "Ethereal Leviathan", "Divine Architect"], "connected_to": ["Volcanic Valley"]}
        }
        
    def get_connected_locations(self, current_location):
        #Returns connected locations of the current area
        return self._game_map[current_location]["connected_to"]

    def get_enemies(self, location):
        #Returns which enemies are in each area
        return self._game_map[location]["enemies"]

    def get_all_locations(self):
        #Returns of a list of all the locations in the map
        return list(self._game_map.keys())