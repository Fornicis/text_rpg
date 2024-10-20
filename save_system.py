import json
import os
from player import Player
from items import Item, initialise_items
from status_effects import StatusEffect, BURN, POISON, FREEZE, STUN, SELF_DAMAGE, VAMPIRIC, STAMINA_DRAIN, DAMAGE_REFLECT, DEFENCE_BREAK, DEFENSIVE_STANCE

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
            "stamina": player.stamina,
            "max_stamina": player.max_stamina,
            "attack": player.attack,
            "defence": player.defence,
            "accuracy": player.accuracy,
            "evasion": player.evasion,
            "crit_chance": player.crit_chance,
            "crit_damage": player.crit_damage,
            "armour_penetration": player.armour_penetration,
            "damage_reduction": player.damage_reduction,
            "block_chance": player.block_chance,
            "gold": player.gold,
            "base_attack": player.base_attack,
            "base_defence": player.base_defence,
            "respawn_counter": player.respawn_counter,
            "days": player.days,
            "inventory": [item.name for item in player.inventory],
            "equipped": {slot: (item.name if item else None) for slot, item in player.equipped.items()},
            "cooldowns": player.cooldowns,
            "active_buffs": player.active_buffs,
            "combat_buffs": player.combat_buffs,
            "weapon_buff": player.weapon_buff,
            "weapon_coating": player.weapon_coating,
            "active_hots": player.active_hots,
            "visited_locations": list(player.visited_locations),
            "kill_tracker": player.kill_tracker,
            "weapon_stamina_cost": player.weapon_stamina_cost,
            "level_modifiers": player.level_modifiers,
            "equipment_modifiers": player.equipment_modifiers,
            "buff_modifiers": player.buff_modifiers,
            "combat_buff_modifiers": player.combat_buff_modifiers,
            "weapon_buff_modifiers": player.weapon_buff_modifiers,
            "debuff_modifiers": player.debuff_modifiers,
            "status_effects": [(effect.name, effect.remaining_duration, effect.strength, effect.stackable) for effect in player.status_effects]
        },
        "current_location": current_location,
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
    
    # Load basic attributes
    for attr in ["level", "exp", "hp", "max_hp", "stamina", "max_stamina", "attack", "defence", "accuracy", "evasion", "crit_chance", "crit_damage", "armour_penetration", "damage_reduction", "block_chance", "gold", 
                 "base_attack", "base_defence", "respawn_counter", "days"]:
        setattr(player, attr, player_data[attr])
    
    # Load inventory and equipped items
    all_items = initialise_items()
    player.inventory = [all_items[item_name] for item_name in player_data["inventory"] if item_name in all_items]
    player.equipped = {slot: (all_items[item_name] if item_name else None) for slot, item_name in player_data["equipped"].items()}
    
    # Load other attributes
    player.cooldowns = player_data["cooldowns"]
    player.active_buffs = player_data["active_buffs"]
    player.combat_buffs = player_data["combat_buffs"]
    player.weapon_buff = player_data["weapon_buff"]
    player.weapon_coating = player_data["weapon_coating"]
    player.active_hots = player_data["active_hots"]
    player.visited_locations = set(player_data["visited_locations"])
    player.kill_tracker = player_data["kill_tracker"]
    player.weapon_stamina_cost = player_data["weapon_stamina_cost"]
    
    # Load new modifier dictionaries
    player.level_modifiers = player_data["level_modifiers"]
    player.equipment_modifiers = player_data["equipment_modifiers"]
    player.buff_modifiers = player_data["buff_modifiers"]
    player.combat_buff_modifiers = player_data["combat_buff_modifiers"]
    player.weapon_buff_modifiers = player_data["weapon_buff_modifiers"]
    player.debuff_modifiers = player_data["debuff_modifiers"]
    
    # Load status effects
    effect_map = {
        "Burn": BURN,
        "Poison": POISON,
        "Freeze": FREEZE,
        "Stun": STUN,
        "Self Damage": SELF_DAMAGE,
        "Vampiric": VAMPIRIC,
        "Stamina Drain": STAMINA_DRAIN,
        "Damage Reflect": DAMAGE_REFLECT,
        "Defence Break": DEFENCE_BREAK,
        "Defensive Stance": DEFENSIVE_STANCE
    }
    player.status_effects = []
    for name, duration, strength, stackable in player_data["status_effects"]:
        if name in effect_map:
            effect = effect_map[name](duration, strength)
            effect.stackable = stackable
            player.status_effects.append(effect)

    current_location = save_data["current_location"]
    
    print(f"Game loaded successfully from {filepath}")
    return player, current_location