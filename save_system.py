import json
import os
from player import Player
from items import Item, initialise_items

SAVE_DIRECTORY = "saves"

def ensure_save_directory():
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

def get_save_files():
    ensure_save_directory()
    return [f for f in os.listdir(SAVE_DIRECTORY) if f.endswith('.json')]

def save_game(player, current_location, filename):
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