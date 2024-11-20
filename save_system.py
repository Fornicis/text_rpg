import json
import os
from player import Player
from items import Item, initialise_items, SoulboundItem, SoulCrystal, BossResonance, VariantAffinity, ElementalResonance, SoulEcho
from status_effects import StatusEffect, BURN, POISON, FREEZE, STUN, SELF_DAMAGE, VAMPIRIC, STAMINA_DRAIN, DAMAGE_REFLECT, DEFENCE_BREAK, DEFENSIVE_STANCE, POWER_STANCE, BERSERKER_STANCE, EVASION_STANCE, ACCURACY_STANCE

SAVE_DIRECTORY = "saves"

def ensure_save_directory():
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)

def get_save_files():
    ensure_save_directory()
    return [f for f in os.listdir(SAVE_DIRECTORY) if f.endswith('.json')]

def save_game(player, current_location, filename):
    ensure_save_directory()
    
    # Initialize item data lists/dicts
    inventory_data = []
    equipped_data = {}
    
    # Process inventory items
    for item in player.inventory:
        item_data = {
            "name": item.name,
            "type": item.type,
            "value": item.value,
            "tier": item.tier,
            "stats": {
                "attack": getattr(item, 'attack', 0),
                "defence": getattr(item, 'defence', 0),
                "accuracy": getattr(item, 'accuracy', 0),
                "evasion": getattr(item, 'evasion', 0),
                "crit_chance": getattr(item, 'crit_chance', 0),
                "crit_damage": getattr(item, 'crit_damage', 0),
                "armour_penetration": getattr(item, 'armour_penetration', 0),
                "damage_reduction": getattr(item, 'damage_reduction', 0),
                "block_chance": getattr(item, 'block_chance', 0),
                "weapon_type": getattr(item, 'weapon_type', None)
            }
        }
        
        # Add soul crystal properties if present
        if isinstance(item, SoulCrystal):
            item_data["is_soul_crystal"] = True
            item_data["stored_buffs"] = item.stored_buffs
            item_data["used"] = item.used
            item_data["soul_source"] = item.soul_source
            
            # Save special effects data
            special_effects_data = []
            for effect in item.special_effects:
                effect_data = {
                    "type": effect.__class__.__name__,  # Store the class name
                    "description": effect.description,
                    "effect_details": effect.effect_details
                }
                # Store additional attributes based on effect type
                if hasattr(effect, 'boss_type'):
                    effect_data["boss_type"] = effect.boss_type
                if hasattr(effect, 'variant_type'):
                    effect_data["variant_type"] = effect.variant_type
                if hasattr(effect, 'element'):
                    effect_data["element"] = effect.element
                if hasattr(effect, 'enemy_type'):
                    effect_data["enemy_type"] = effect.enemy_type
                    effect_data["kill_count"] = effect.kill_count
                special_effects_data.append(effect_data)
            item_data["special_effects"] = special_effects_data
        
        # Add soulbound properties if present
        if hasattr(item, 'soulbound') and item.soulbound:
            item_data["soulbound"] = True
            item_data["growth_stats"] = getattr(item, 'growth_stats', [])
            item_data["soul_source"] = getattr(item, 'soul_source', {})
            item_data["birth_level"] = getattr(item, 'birth_level', 1)
            item_data["current_level"] = getattr(item, 'current_level', 1)
            item_data["growth_rate"] = getattr(item, 'growth_rate', 0.1)
            
        inventory_data.append(item_data)
    
    # Process equipped items
    for slot, item in player.equipped.items():
        if item:
            item_data = {
                "name": item.name,
                "type": item.type,
                "value": item.value,
                "tier": item.tier,
                "stats": {
                    "attack": getattr(item, 'attack', 0),
                    "defence": getattr(item, 'defence', 0),
                    "accuracy": getattr(item, 'accuracy', 0),
                    "evasion": getattr(item, 'evasion', 0),
                    "crit_chance": getattr(item, 'crit_chance', 0),
                    "crit_damage": getattr(item, 'crit_damage', 0),
                    "armour_penetration": getattr(item, 'armour_penetration', 0),
                    "damage_reduction": getattr(item, 'damage_reduction', 0),
                    "block_chance": getattr(item, 'block_chance', 0),
                    "weapon_type": getattr(item, 'weapon_type', None)
                }
            }
            
            # Add soulbound properties if present
            if hasattr(item, 'soulbound') and item.soulbound:
                item_data["soulbound"] = True
                item_data["growth_stats"] = getattr(item, 'growth_stats', [])
                item_data["soul_source"] = getattr(item, 'soul_source', {})
                item_data["birth_level"] = getattr(item, 'birth_level', 1)
                item_data["current_level"] = getattr(item, 'current_level', 1)
                item_data["growth_rate"] = getattr(item, 'growth_rate', 0.1)
                
            equipped_data[slot] = item_data
        else:
            equipped_data[slot] = None
            
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
            "inventory": inventory_data,
            "equipped": equipped_data,
            "cooldowns": player.cooldowns,
            "active_buffs": player.active_buffs,
            "combat_buffs": player.combat_buffs,
            "weapon_buff": player.weapon_buff,
            "weapon_coating": player.weapon_coating,
            "active_hots": player.active_hots,
            "visited_locations": list(player.visited_locations),
            "kill_tracker": player.kill_tracker,
            "used_kill_tracker": player.used_kill_tracker,
            "variant_kill_tracker": player.variant_kill_tracker,
            "used_variant_tracker": player.used_variant_tracker,
            "boss_kill_tracker": player.boss_kill_tracker,
            "used_boss_kill_tracker": player.used_boss_kill_tracker,
            "weapon_stamina_cost": player.weapon_stamina_cost,
            "level_modifiers": player.level_modifiers,
            "equipment_modifiers": player.equipment_modifiers,
            "buff_modifiers": player.buff_modifiers,
            "combat_buff_modifiers": player.combat_buff_modifiers,
            "weapon_buff_modifiers": player.weapon_buff_modifiers,
            "debuff_modifiers": player.debuff_modifiers,
            "status_effects": [(effect.name, effect.remaining_duration, effect.strength, effect.stackable) 
                             for effect in player.status_effects]
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
    for attr in ["level", "exp", "hp", "max_hp", "stamina", "max_stamina", "attack", 
                "defence", "accuracy", "evasion", "crit_chance", "crit_damage", 
                "armour_penetration", "damage_reduction", "block_chance", "gold", 
                "base_attack", "base_defence", "respawn_counter", "days"]:
        setattr(player, attr, player_data[attr])
    
    # Load inventory items
    player.inventory = []
    all_items = initialise_items()
    
    for item_data in player_data["inventory"]:
        if isinstance(item_data, str):  # Handle old save format
            if item_data in all_items:
                player.inventory.append(all_items[item_data])
        else:  # New save format
            if "is_soul_crystal" in item_data:
                # Recreate special effects
                special_effects = []
                for effect_data in item_data["special_effects"]:
                    effect_class = globals()[effect_data["type"]]  # Get effect class by name
                    if effect_data["type"] == "BossResonance":
                        effect = BossResonance(effect_data["boss_type"])
                    elif effect_data["type"] == "VariantAffinity":
                        effect = VariantAffinity(effect_data["variant_type"])
                    elif effect_data["type"] == "ElementalResonance":
                        effect = ElementalResonance(effect_data["element"])
                    elif effect_data["type"] == "SoulEcho":
                        effect = SoulEcho(effect_data["enemy_type"], effect_data["kill_count"])
                    special_effects.append(effect)
                
                # Create soul crystal
                item = SoulCrystal(
                    item_data["name"],
                    item_data["value"],
                    item_data["tier"],
                    item_data["stored_buffs"],
                    special_effects,
                    item_data["soul_source"]
                )
                item.used = item_data["used"]
                
            elif "soulbound" in item_data and item_data["soulbound"]:
                # Get weapon_type from stats if it exists
                weapon_type = item_data["stats"].pop("weapon_type", None)
                # Create soulbound item
                item = SoulboundItem(
                    item_data["name"],
                    item_data["type"],
                    item_data["value"],
                    item_data["tier"],
                    growth_stats=item_data["growth_stats"],
                    soul_source=item_data["soul_source"],
                    weapon_type=weapon_type,
                    **item_data["stats"]
                )
                item.birth_level = item_data["birth_level"]
                item.current_level = item_data["current_level"]
                item.growth_rate = item_data["growth_rate"]
            else:
                # Try to get from all_items first
                if item_data["name"] in all_items:
                    item = all_items[item_data["name"]]
                else:
                    # Get the weapon_type from stats if it exists
                    weapon_type = item_data["stats"].pop("weapon_type", None)
                    # Create regular item
                    item = Item(
                        item_data["name"],
                        item_data["type"],
                        item_data["value"],
                        item_data["tier"],
                        weapon_type=weapon_type,
                        **item_data["stats"]
                    )
            player.inventory.append(item)
    
    # Load equipped items
    player.equipped = {}
    for slot, item_data in player_data["equipped"].items():
        if isinstance(item_data, str):  # Handle old save format
            if item_data in all_items:
                player.equipped[slot] = all_items[item_data]
            else:
                player.equipped[slot] = None
        else:  # New save format
            if item_data:
                if "soulbound" in item_data and item_data["soulbound"]:
                    # Get the weapon_type from stats if it exists
                    weapon_type = item_data["stats"].pop("weapon_type", None)
                    # Create soulbound equipped item
                    item = SoulboundItem(
                        item_data["name"],
                        item_data["type"],
                        item_data["value"],
                        item_data["tier"],
                        growth_stats=item_data["growth_stats"],
                        soul_source=item_data["soul_source"],
                        weapon_type=weapon_type,
                        **item_data["stats"]
                    )
                    item.birth_level = item_data["birth_level"]
                    item.current_level = item_data["current_level"]
                    item.growth_rate = item_data["growth_rate"]
                else:
                    # Try to get from all_items first
                    if item_data["name"] in all_items:
                        item = all_items[item_data["name"]]
                    else:
                        # Get the weapon_type from stats if it exists
                        weapon_type = item_data["stats"].pop("weapon_type", None)
                        # Create regular item
                        item = Item(
                            item_data["name"],
                            item_data["type"],
                            item_data["value"],
                            item_data["tier"],
                            weapon_type=weapon_type,
                            **item_data["stats"]
                        )
                player.equipped[slot] = item
            else:
                player.equipped[slot] = None

    # Load other attributes
    player.cooldowns = player_data["cooldowns"]
    player.active_buffs = player_data["active_buffs"]
    player.combat_buffs = player_data["combat_buffs"]
    player.weapon_buff = player_data["weapon_buff"]
    player.weapon_coating = player_data["weapon_coating"]
    player.active_hots = player_data["active_hots"]
    player.visited_locations = set(player_data["visited_locations"])
    player.kill_tracker = player_data["kill_tracker"]
    player.used_kill_tracker = player_data["used_kill_tracker"]
    player.variant_kill_tracker = player_data["variant_kill_tracker"]
    player.used_variant_tracker = player_data["used_variant_tracker"]
    player.boss_kill_tracker = player_data["boss_kill_tracker"]
    player.used_boss_kill_tracker = player_data["used_boss_kill_tracker"]
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
        "Defensive Stance": DEFENSIVE_STANCE,
        "Power Stance": POWER_STANCE,
        "Berserker Stance": BERSERKER_STANCE,
        "Evasion Stance": EVASION_STANCE,
        "Accuracy Stance": ACCURACY_STANCE
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