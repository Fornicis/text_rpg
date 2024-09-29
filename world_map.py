import os

class WorldMap:
    def __init__(self):
        self._game_map = {
            #Home
            "Village": {"enemies": [], "connected_to": ["Forest", "Plains"], "min_level": 1},
            #Easy Monster Areas (levels 1-4)
            "Deepwoods": {"enemies": ["Wood Spirit", "Deepwood Stalker", "Deep Bat", "Giant Firefly", "Treant"], "connected_to": ["Forest", "Swamp"], "min_level": 2},
            "Cave": {"enemies": ["Bat", "Goblin", "Spider", "Slime", "Frog"], "connected_to": ["Plains", "Temple"], "min_level": 2},
            "Forest": {"enemies": ["Tree Sprite", "Snake", "Forest Hawk", "Locust", "Leprechaun"], "connected_to": ["Village", "Deepwoods", "Mountain"], "min_level": 1},
            "Plains": {"enemies": ["Rat", "Boar", "Plains Hawk", "Strider", "Bull"], "connected_to": ["Village", "Cave", "Desert"], "min_level": 1},
            
            #Medium Monster Areas (levels 5-9)
            "Swamp": {"enemies": ["Alligator", "Poison Frog", "Swamp Troll", "Mosquito Swarm", "Bog Witch"], "connected_to": ["Deepwoods", "Toxic Swamp"], "min_level": 5},
            "Temple": {"enemies": ["Stone Golem", "Cultist", "Mummy", "Animated Statue", "Temple Guardian"], "connected_to": ["Cave", "Ruins"], "min_level": 5},
            "Mountain": {"enemies": ["Mountain Lion", "Rock Elemental", "Harpy", "Yeti", "Orc"], "connected_to": ["Forest", "Valley", "Mountain Peaks"], "min_level": 3},
            "Desert": {"enemies": ["Sand Wurm", "Dried Mummy", "Dust Devil", "Desert Bandit", "Leopard"], "connected_to": ["Plains", "Valley", "Scorching Plains"], "min_level": 3},
            
            #Medium-Hard Monster Areas (levels 10-14)
            "Valley": {"enemies": ["Canyon Cougar", "Twisted Mesquite", "Dustier Devil", "Petrified Warrior", "Thunderbird"], "connected_to": ["Mountain", "Desert", "Shadowed Valley"], "min_level": 7},
            
            #Hard Monster Areas (levels 15-19)
            "Toxic Swamp": {"enemies": ["Venomous Hydra", "Plague Bearer", "Mire Leviathan", "Toxic Shambler", "Swamp Hag"], "connected_to": ["Swamp", "Death Caves"], "min_level": 13},
            "Ruins": {"enemies": ["Ancient Golem", "Cursed Pharaoh", "Temporal Anomaly", "Ruin Wraith", "Forgotten Titan"], "connected_to": ["Temple", "Ancient Ruins"], "min_level": 13},
            "Mountain Peaks": {"enemies": ["Frost Giant", "Storm Harpy", "Avalanche Elemental", "Mountain Wyvern", "Yeti Alpha"], "connected_to": ["Mountain", "Dragons Lair"], "min_level": 11},
            "Scorching Plains": {"enemies": ["Fire Elemental", "Sandstorm Djinn", "Mirage Assassin", "Sunburst Phoenix", "Desert Colossus"], "connected_to": ["Desert", "Death Valley"], "min_level": 11},
            "Shadowed Valley": {"enemies": ["Nightmare Stalker", "Void Weaver", "Shadow Dragon", "Ethereal Banshee", "Abyssal Behemoth"], "connected_to": ["Valley", "Volcanic Valley"], "min_level": 11},
            
            #Very Hard Monster Areas (levels 20-24)
            "Death Caves": {"enemies": ["Necropolis Guardian", "Soul Reaver", "Bone Colossus", "Spectral Devourer", "Lich King"], "connected_to": ["Toxic Swamp", "Dragons Lair"], "min_level": 15},
            "Ancient Ruins": {"enemies": ["Timeless Sphinx", "Eternal Pharaoh", "Anubis Reborn", "Mummy Emperor", "Living Obelisk"], "connected_to": ["Ruins", "Death Valley"], "min_level": 15},
            "Death Valley": {"enemies": ["Apocalypse Horseman", "Abyssal Wyrm", "Void Titan", "Chaos Incarnate", "Eternity Warden"], "connected_to": ["Scorching Plains", "Ancient Ruins", "Volcanic Valley"], "min_level": 13},
            "Dragons Lair": {"enemies": ["Ancient Wyvern", "Elemental Drake", "Dragonlord", "Chromatic Dragon", "Elder Dragon"], "connected_to": ["Mountain Peaks", "Death Caves", "Volcanic Valley"], "min_level": 13},
            
            #Extreme Monster Areas (levels 25+)
            "Volcanic Valley": {"enemies": ["Magma Colossus", "Phoenix Overlord", "Volcanic Titan", "Inferno Wyrm", "Cinder Archfiend"], "connected_to": ["Shadowed Valley", "Death Valley", "Dragons Lair", "Heavens"], "min_level": 17},
            
            #Boss Monster Area
            "Heavens": {"enemies": ["Seraphim Guardian", "Celestial Arbiter", "Astral Demiurge", "Ethereal Leviathan", "Divine Architect"], "connected_to": ["Volcanic Valley"], "min_level": 21}
        }
        
    def get_connected_locations(self, current_location):
        #Returns connected locations of the current area
        return self._game_map[current_location]["connected_to"]

    def get_enemies(self, location):
        #Returns which enemies are in each area
        return self._game_map[location]["enemies"]

    def get_all_locations(self):
        #Returns a list of all the locations in the map
        return list(self._game_map.keys())
    
    def get_min_level(self, location):
        #Returns minimum level required to enter area
        return self._game_map[location]["min_level"]
    
    def display_map(self, current_location, player_level):
        #Displays an ASCII representation of the world map, highlighting the current location
        #and showing available paths based on the player's level.
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== World Map ===\n")
        
        map_art = """
                                               [HEAVENS]
                                                  |
    [ANCIENT]------[DEATH_V]---------[VOLCANIC]------[DRAGONS]-----[DEATH_C]
          |                |                      |                   |                |
          |                |                      |                   |                |            
        [RUINS]        [SCORCHING]       [SHADOWED]     [MOUNTAIN_P]    [TOXIC]
          |                |                      |                   |                |
          |                |                      |                   |                |
        [TEMPLE]----------[DESERT]-----------------[VALLEY]-------------[MOUNTAIN]-----------[SWAMP]
          |                |                                          |                |
          |                |                                          |                |
        [CAVE]------------[PLAINS]----------------[VILLAGE]------------[FOREST]----------[DEEPWOODS]
        """
        
        # Define a dictionary to map markers to actual location names
        location_markers = {
            "[HEAVENS]": "Heavens",
            "[ANCIENT]": "Ancient Ruins",
            "[DEATH_V]": "Death Valley",
            "[VOLCANIC]": "Volcanic Valley",
            "[DRAGONS]": "Dragons Lair",
            "[DEATH_C]": "Death Caves",
            "[RUINS]": "Ruins",
            "[SCORCHING]": "Scorching Plains",
            "[SHADOWED]": "Shadowed Valley",
            "[MOUNTAIN_P]": "Mountain Peaks",
            "[TOXIC]": "Toxic Swamp",
            "[TEMPLE]": "Temple",
            "[DESERT]": "Desert",
            "[VALLEY]": "Valley",
            "[MOUNTAIN]": "Mountain",
            "[SWAMP]": "Swamp",
            "[CAVE]": "Cave",
            "[PLAINS]": "Plains",
            "[VILLAGE]": "Village",
            "[FOREST]": "Forest",
            "[DEEPWOODS]": "Deepwoods"
        }
        
        # Highlight current location
        for marker, location in location_markers.items():
            if location == current_location:
                map_art = map_art.replace(marker, f"*{location}*")
            else:
                map_art = map_art.replace(marker, location)
        
        # Add zero-width spaces to the beginning of each line
        map_art = "\u200B" + map_art.replace("\n", "\n\u200B")
        
        print(map_art)
        
        print("\nLegend:")
        print("* Your current location *")
        print("------ Direct connection")
        print()
        
        # Display available directions
        connected_locations = self.get_connected_locations(current_location)
        if connected_locations:
            print("You can go to:")
            for loc in connected_locations:
                min_level = self.get_min_level(loc)
                if player_level >= min_level:
                    print(f"  - {loc}")
                else:
                    print(f"  - {loc} (Locked - Required Level: {min_level})")
        else:
            print("There are no connected locations from here.")

        input("\nPress Enter to continue...")