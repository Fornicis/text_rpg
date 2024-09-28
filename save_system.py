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

def save_game(player, current_location, days, filename):
    ensure_save_directory()
    save_data = {
        "player": {
            "name": player.name,
            "level": player.level,
            "exp": player.exp,
            "hp": player.hp,
            "days": player.days,
            "respawn_counter": player.respawn_counter,
            "max_hp": player.max_hp,
            "stamina": player.stamina,
            "max_stamina": player.max_stamina,
            "weapon_stamina_cost": player.weapon_stamina_cost,
            "attack": player.attack,
            "defence": player.defence,
            "gold": player.gold,
            "inventory": [item.name for item in player.inventory],
            "equipped": {slot: (item.name if item else None) for slot, item in player.equipped.items()},
            "cooldowns": player.cooldowns,
            "active_buffs": player.active_buffs,
            "combat_buffs": player.combat_buffs,  # New: Save combat buffs
            "active_hots": player.active_hots,  # New: Save active HoTs
            "visited_locations": list(player.visited_locations)  # New: Save visited locations
        },
        "current_location": current_location,
        #"days": days  # New: Save the current day count
    }
    
    filepath = os.path.join(SAVE_DIRECTORY, filename)
    with open(filepath, 'w') as f:
        json.dump(save_data, f)
    print(f"Game saved successfully to {filepath}")

def load_game(filename):
    filepath = os.path.join(SAVE_DIRECTORY, filename)
    if not os.path.exists(filepath):
        print(f"Save file {filename} not found.")
        return None, None, None  # Return None for player, location, and days

    with open(filepath, 'r') as f:
        save_data = json.load(f)

    player_data = save_data["player"]
    player = Player(player_data["name"])
    player.level = player_data["level"]
    player.exp = player_data["exp"]
    player.days = player_data["days"]
    player.hp = player_data["hp"]
    player.max_hp = player_data["max_hp"]
    player.respawn_counter = player_data["respawn_counter"]
    player.stamina = player_data["stamina"]
    player.max_stamina = player_data["max_stamina"]
    player.weapon_stamina_cost = player_data.get("weapon_stamina_cost", {"light": 3, "medium": 5, "heavy": 7})
    player.attack = player_data["attack"]
    player.defence = player_data["defence"]
    player.gold = player_data["gold"]
    
    all_items = initialise_items()
    player.inventory = [all_items[item_name] for item_name in player_data["inventory"] if item_name in all_items]
    player.equipped = {slot: (all_items[item_name] if item_name else None) for slot, item_name in player_data["equipped"].items()}
    player.cooldowns = player_data["cooldowns"]
    player.active_buffs = player_data["active_buffs"]
    player.combat_buffs = player_data["combat_buffs"]  # New: Load combat buffs
    player.active_hots = player_data["active_hots"]  # New: Load active HoTs
    player.visited_locations = set(player_data["visited_locations"])  # New: Load visited locations

    current_location = save_data["current_location"]
    #days = save_data["days"]  # New: Load the current day count
    
    print(f"Game loaded successfully from {filepath}")
    return player, current_location  # Return player, location, and days