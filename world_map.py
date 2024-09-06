class WorldMap:
    def __init__(self):
        self._game_map = {
            "Village": {"enemies": [], "connected_to": ["Forest", "Plains"], "level_req": 1},
            "Forest": {"enemies": ["Tree Sprite", "Snake", "Forest Hawk", "Locust", "Leprechaun"], "connected_to": ["Village", "Mountain"], "level_req": 1},
            "Plains": {"enemies": ["Rat", "Boar", "Plains Hawk", "Strider", "Bull"], "connected_to": ["Village", "Desert"], "level_req": 1},
            "Cave": {"enemies": ["Bat", "Goblin", "Spider", "Slime", "Frog"], "connected_to": ["Plains", "Temple"], "level_req": 3},
            "Deepwoods": {"enemies": ["Wood Spirit", "Deepwood Stalker", "Deep Bat", "Giant Firefly", "Treant"], "connected_to": ["Forest", "Swamp"], "level_req": 5},
            "Swamp": {"enemies": ["Alligator", "Poison Frog", "Swamp Troll", "Mosquito Swarm", "Bog Witch"], "connected_to": ["Deepwoods", "Toxic Swamp"], "level_req": 10},
            "Temple": {"enemies": ["Stone Golem", "Cultist", "Mummy", "Animated Statue", "Temple Guardian"], "connected_to": ["Cave", "Ruins"], "level_req": 12},
            "Mountain": {"enemies": ["Mountain Lion", "Rock Elemental", "Harpy", "Yeti", "Orc"], "connected_to": ["Forest", "Valley", "Mountain Peaks"], "level_req": 15},
            "Desert": {"enemies": ["Sand Wurm", "Dried Mummy", "Dust Devil", "Desert Bandit", "Leopard"], "connected_to": ["Plains", "Valley", "Scorching Plains"], "level_req": 18},
            "Valley": {"enemies": ["Canyon Cougar", "Twisted Mesquite", "Dust Devil", "Petrified Warrior", "Thunderbird"], "connected_to": ["Mountain", "Desert", "Shadowed Valley"], "level_req": 20},
            "Toxic Swamp": {"enemies": ["Venomous Hydra", "Plague Bearer", "Mire Leviathan", "Toxic Shambler", "Swamp Hag"], "connected_to": ["Swamp", "Death Caves"], "level_req": 25},
            "Ruins": {"enemies": ["Ancient Golem", "Cursed Pharaoh", "Temporal Anomaly", "Ruin Wraith", "Forgotten Titan"], "connected_to": ["Temple", "Ancient Ruins"], "level_req": 28},
            "Mountain Peaks": {"enemies": ["Frost Giant", "Storm Harpy", "Avalanche Elemental", "Mountain Wyvern", "Yeti Alpha"], "connected_to": ["Mountain", "Dragons Lair"], "level_req": 30},
            "Scorching Plains": {"enemies": ["Fire Elemental", "Sandstorm Djinn", "Mirage Assassin", "Sunburst Phoenix", "Desert Colossus"], "connected_to": ["Desert", "Death Valley"], "level_req": 33},
            "Shadowed Valley": {"enemies": ["Nightmare Stalker", "Void Weaver", "Shadow Dragon", "Ethereal Banshee", "Abyssal Behemoth"], "connected_to": ["Valley", "Volcanic Valley"], "level_req": 35},
            "Death Caves": {"enemies": ["Necropolis Guardian", "Soul Reaver", "Bone Colossus", "Spectral Devourer", "Lich King"], "connected_to": [], "level_req": 40},
            "Ancient Ruins": {"enemies": ["Timeless Sphinx", "Eternal Pharaoh", "Anubis Reborn", "Mummy Emperor", "Living Obelisk"], "connected_to": ["Desert"], "level_req": 42},
            "Death Valley": {"enemies": ["Apocalypse Horseman", "Abyssal Wyrm", "Void Titan", "Chaos Incarnate", "Eternity Warden"], "connected_to": ["Scorching Plains", "Ancient Ruins", "Volcanic Valley"], "level_req": 45},
            "Dragons Lair": {"enemies": ["Ancient Wyvern", "Elemental Drake", "Dragonlord", "Chromatic Dragon", "Elder Dragon"], "connected_to": ["Mountain Peaks", "Death Caves", "Volcanic Valley"], "level_req": 48},
            "Volcanic Valley": {"enemies": ["Magma Colossus", "Phoenix Overlord", "Volcanic Titan", "Inferno Wyrm", "Cinder Archfiend"], "connected_to": ["Shadowed Valley", "Death Valley", "Dragons Lair", "The Heavens"], "level_req": 50},
            "The Heavens": {"enemies": ["Seraphim Guardian", "Celestial Arbiter", "Astral Demiurge", "Ethereal Leviathan", "Divine Architect"], "connected_to": ["Volcanic Valley"], "level_req": 55}
        }
        
    def get_connected_locations(self, current_location, player_level):
        connected = self._game_map[current_location]["connected_to"]
        return [loc for loc in connected if player_level >= self._game_map[loc]["level_req"]]

    def get_enemies(self, location):
        return self._game_map[location]["enemies"]

    def get_all_locations(self):
        return list(self._game_map.keys())

    def get_location_level_req(self, location):
        return self._game_map[location]["level_req"]