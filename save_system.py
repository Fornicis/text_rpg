import json
import os
from player import Player
from items import Item, initialise_items

SAVE_DIRECTORY = "saves"

def ensure_save_directory():
    #Makes a folder called saves if one does not exist in the path
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

def get_save_files():
    #Shows a list of save_files in the saves folder as long as they end with .json
    ensure_save_directory()
    return [f for f in os.listdir(SAVE_DIRECTORY) if f.endswith('.json')]

def save_game(player, current_location, filename):
    #Saves all stats, items, equipment and location of the player to chosen save file, makes a new save if requested to do so
    ensure_save_directory()
    save_data = {
        "player": {
            "name": player.name,
            "level": player.level,
            "exp": player.exp,
            "hp": player.hp,
            "max_hp": player.max_hp,
            "attack": player.attack,
            "defence": player.defence,
            "gold": player.gold,
            "inventory": [item.name for item in player.inventory],
            "equipped": {slot: (item.name if item else None) for slot, item in player.equipped.items()},
            "cooldowns": player.cooldowns,
            "active_buffs": player.active_buffs
        },
        "current_location": current_location
    }
    
    filepath = os.path.join(SAVE_DIRECTORY, filename)
    with open(filepath, 'w') as f:
        json.dump(save_data, f)
    print(f"Game saved successfully to {filepath}")

def load_game(filename):
    #Pulls data from specified save file and loads that into the game parsing information to relevant sections
    filepath = os.path.join(SAVE_DIRECTORY, filename)
    if not os.path.exists(filepath):
        print(f"Save file {filename} not found.")
        return None, None

    with open(filepath, 'r') as f:
        save_data = json.load(f)

    player_data = save_data["player"]
    player = Player(player_data["name"])
    player.level = player_data["level"]
    player.exp = player_data["exp"]
    player.hp = player_data["hp"]
    player.max_hp = player_data["max_hp"]
    player.attack = player_data["attack"]
    player.defence = player_data["defence"]
    player.gold = player_data["gold"]
    
    all_items = initialise_items()
    player.inventory = [all_items[item_name] for item_name in player_data["inventory"] if item_name in all_items]
    player.equipped = {slot: (all_items[item_name] if item_name else None) for slot, item_name in player_data["equipped"].items()}
    player.cooldowns = player_data["cooldowns"]
    player.active_buffs = player_data["active_buffs"]

    current_location = save_data["current_location"]
    
    print(f"Game loaded successfully from {filepath}")
    return player, current_location