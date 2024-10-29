import random

class StatusEffect:
    def __init__(self, name, duration, apply_func, remove_func=None, strength=1, is_debuff=False, stackable=False):
        self.name = name
        self.remaining_duration = duration
        self.initial_duration = duration
        self.apply_func = apply_func
        self.remove_func = remove_func
        self.strength = strength
        self.stackable = stackable
        self.is_debuff = is_debuff
        self.applied_this_turn = False
        self.is_active = False

    def apply(self, character, *args):
        if not self.is_active:
            result = self.apply_func(character, self.strength, *args)
            self.is_active = result
            return result
        return False

    def remove(self, character):
        if self.remove_func:
            self.remove_func(character, self.strength)
        self.is_active = False
        return None

    def update(self, character):
        if self.is_active:
            self.remaining_duration -= 1
            if self.remaining_duration <= 0:
                remove_message = self.remove(character)
                self.is_active = False
                return False, remove_message
            return True, None
        return False, None

    def reset_duration(self):
        self.remaining_duration = self.initial_duration

    def __str__(self):
        if not self.is_active:
            return ""
        if self.stackable:
            return f"{self.name} ({self.strength} stacks, {self.remaining_duration} turns)"
        return f"{self.name} ({self.remaining_duration} turns)"

def create_dot_effect(name, damage_func):
    def apply(character, strength):
        damage = damage_func(character, strength)
        character.take_damage(damage)
        effect = next((e for e in character.status_effects if e.name == name), None)
        duration = effect.remaining_duration if effect else 0
        print(f"{character.name} takes {damage} {name.lower()} damage! (Current stacks: {strength}, Duration: {duration} turns)")
        return True
    return apply

def create_chance_effect(name, chance_func, effect_func):
    def apply(character, strength):
        if random.random() < chance_func(strength):
            effect_func(character, True)
            return True
        else:
            effect_func(character, False)
            print(f"{character.name} resists the {name} effect!")
            return False
    
    def remove(character, strength):
        effect_func(character, False)
    
    return apply, remove

# Define status effects
BURN = lambda duration, strength=1: StatusEffect("Burn", duration, 
    create_dot_effect("Burn", lambda char, str: max(1, int(char.max_hp * 0.02 * str))),
    strength=strength, is_debuff=True, stackable=True)

POISON = lambda duration, strength=1: StatusEffect("Poison", duration, 
    create_dot_effect("Poison", lambda char, str: str),
    strength=strength, is_debuff=True, stackable=True)

freeze_apply, freeze_remove = create_chance_effect("Freeze", lambda str: 0.3 * str, lambda char, frozen: setattr(char, 'frozen', frozen))
FREEZE = lambda duration, strength=1: StatusEffect("Freeze", duration, freeze_apply, freeze_remove, strength=strength, is_debuff=True)

stun_apply, stun_remove = create_chance_effect("Stun", lambda str: 0.8 * str, lambda char, stunned: setattr(char, 'stunned', stunned))
STUN = lambda duration, strength=1: StatusEffect("Stun", duration, stun_apply, stun_remove, strength=strength, is_debuff=True)

def confusion_apply(character, strength):
    if random.random() < 0.5:  # 50% chance to apply confusion
        character.confused = True
        print(f"{character.name} is confused!")
        return True
    else:
        print(f"{character.name} resists the confusion!")
        return False

def confusion_remove(character, strength):
    character.confused = False
    print(f"{character.name} is no longer confused.")

CONFUSION = lambda duration, strength=1: StatusEffect("Confusion", duration, confusion_apply, confusion_remove, strength=strength, is_debuff=True)

def self_damage_apply(character, strength, attack_type="reckless"):
    damage = int(strength * 0.2)
    character.take_damage(damage)
    print(f"{character.name} takes {damage} self-damage from their {attack_type} attack!")

SELF_DAMAGE = lambda strength, attack_type="reckless": StatusEffect("Self Damage", 1, 
    lambda char, str: self_damage_apply(char, str, attack_type),
    strength=strength, is_debuff=True)

def vampiric_apply(character, strength):
    heal_amount = int(strength * 0.33)
    character.heal(heal_amount)
    print(f"{character.name} healed {heal_amount} damage from their vampiric attack!")

VAMPIRIC = lambda strength: StatusEffect("Vampiric", 1, vampiric_apply, strength=strength, is_debuff=False)

def stamina_drain_apply(character, strength):
    if hasattr(character, 'stamina'):
        max_drain = int(strength * 0.2)
        stamina_loss = max(10, min(max_drain, character.stamina))
        character.use_stamina(stamina_loss)
        print(f"{character.name} lost {stamina_loss} stamina from the draining attack!")
    else:
        print(f"The draining attack has no effect on {character.name}!")

STAMINA_DRAIN = lambda strength: StatusEffect("Stamina Drain", 1, stamina_drain_apply, strength=strength, is_debuff=True)

def damage_reflect_apply(character, strength, damage_dealt=0):
    if damage_dealt > 0:
        reflected_damage = int(damage_dealt * 0.5 * strength)
        print(f"{character.name} reflects {reflected_damage} damage!")
        return reflected_damage
    else:
        print(f"{character.name} has a reflective barrier active!")
        return 0

DAMAGE_REFLECT = lambda duration, strength=1: StatusEffect("Damage Reflect", duration, damage_reflect_apply, strength=strength, is_debuff=False)

def defence_break_apply(character, strength):
    character.apply_debuff("defence", strength)
    print(f"{character.name}'s defence is reduced by {strength}!")
    return True

def defence_break_remove(character, strength):
    character.remove_debuff("defence", strength)
    print(f"{character.name}'s Defence Break effect has worn off.")

DEFENCE_BREAK = lambda duration, strength: StatusEffect("Defence Break", duration, defence_break_apply, defence_break_remove, strength=strength, is_debuff=True)

def create_stance_message(character_name, stat_changes):
    """
    Creates a formatted message for stance changes.
    
    Args:
        character_name: Name of the character
        stat_changes: Dictionary of stat changes in the format:
            {
                "increases": {"category_name": [(stat_name, value), ...]},
                "decreases": {"category_name": [(stat_name, value), ...]}
            }
    """
    message = []
    
    # Handle increases
    for category, changes in stat_changes["increases"].items():
        # Filter out zero changes
        valid_changes = [(stat, val) for stat, val in changes if val > 0]
        if valid_changes:
            message.append(f"{character_name}'s {category} increased:")
            message.extend(f"{stat}: +{val}" for stat, val in valid_changes)
    
    # Handle decreases
    for category, changes in stat_changes["decreases"].items():
        # Filter out zero changes
        valid_changes = [(stat, val) for stat, val in changes if val > 0]
        if valid_changes:
            message.append(f"{character_name}'s {category} reduced:")
            message.extend(f"{stat}: -{val}" for stat, val in valid_changes)
    
    if message:
        print("\n".join(message))

def defensive_stance_apply(character, strength):
    # Calculate boosts and negatives
    defence_boost = int((character.base_defence + character.level_modifiers["defence"] + character.equipment_modifiers["defence"]) * strength / 75)
    block_boost = int((character.base_block_chance + character.level_modifiers.get("block_chance", 0) + character.equipment_modifiers.get("block_chance", 0)) * strength / 75)
    dr_boost = int((character.base_block_chance + character.level_modifiers.get("damage_reduction", 0) + character.equipment_modifiers.get("damage_reduction", 0)) * strength / 75)
    atk_reduce = int((character.base_attack + character.level_modifiers["attack"] + character.equipment_modifiers["attack"]) * strength / 100)
    crit_chance_reduce = int((character.base_crit_chance + character.level_modifiers["crit_chance"] + character.weapon_buff_modifiers.get("crit_chance", 0) + character.equipment_modifiers.get("crit_chance", 0) * strength / 100))
    
    # Update combat buff modifiers using the get() method with default value
    current_defence = character.combat_buff_modifiers.get("defence", 0)
    current_block = character.combat_buff_modifiers.get("block_chance", 0)
    current_dr = character.combat_buff_modifiers.get("damage_reduction", 0)
    current_atk = character.combat_buff_modifiers.get("attack", 0)
    current_crit_chance = character.combat_buff_modifiers.get("crit_chance", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["defence"] = current_defence + defence_boost
    character.combat_buff_modifiers["block_chance"] = current_block + block_boost
    character.combat_buff_modifiers["damage_reduction"] = current_dr + dr_boost
    character.combat_buff_modifiers["attack"] = current_atk - atk_reduce
    character.combat_buff_modifiers["crit_chance"] = current_crit_chance - crit_chance_reduce
    
    character.recalculate_stats()
    # Create stat changes dictionary
    stat_changes = {
        "increases": {
            "defensive stats": [
                ("Defence", defence_boost),
                ("Damage Reduction", dr_boost),
                ("Block Chance", block_boost)
            ]
        },
        "decreases": {
            "offensive stats": [
                ("Attack", atk_reduce),
                ("Crit %", crit_chance_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)
    return True

def defensive_stance_remove(character, strength):
    # Calculate the boosts and negatives
    defence_boost = int((character.base_defence + character.level_modifiers["defence"] + character.equipment_modifiers["defence"]) * strength / 75)
    block_boost = int((character.base_block_chance + character.level_modifiers.get("block_chance", 0) + character.equipment_modifiers.get("block_chance", 0)) * strength / 75)
    dr_boost = int((character.base_block_chance + character.level_modifiers.get("damage_reduction", 0) + character.equipment_modifiers.get("damage_reduction", 0)) * strength / 75)
    atk_reduce = int((character.base_attack + character.level_modifiers["attack"] + character.equipment_modifiers["attack"]) * strength / 100)
    crit_chance_reduce = int((character.base_crit_chance + character.level_modifiers["crit_chance"] + character.weapon_buff_modifiers.get("crit_chance", 0) + character.equipment_modifiers.get("crit_chance", 0) * strength / 100))
    
    # Update combat buff modifiers using the get() method with default value
    current_defence = character.combat_buff_modifiers.get("defence", 0)
    current_block = character.combat_buff_modifiers.get("block_chance", 0)
    current_dr = character.combat_buff_modifiers.get("damage_reduction", 0)
    current_atk = character.combat_buff_modifiers.get("attack", 0)
    current_crit_chance = character.combat_buff_modifiers.get("crit_chance", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["defence"] = max(0, current_defence - defence_boost)
    character.combat_buff_modifiers["block_chance"] = max(0, current_block - block_boost)
    character.combat_buff_modifiers["damage_reduction"] = max(0, current_dr - dr_boost)
    character.combat_buff_modifiers["attack"] = max(0, current_atk + atk_reduce)
    character.combat_buff_modifiers["crit_chance"] = max(0, current_crit_chance + crit_chance_reduce)
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "decreases": {
            "defensive stats": [
                ("Defence", defence_boost),
                ("Damage Reduction", dr_boost),
                ("Block Chance", block_boost)
            ]
        },
        "increases": {
            "offensive stats": [
                ("Attack", atk_reduce),
                ("Crit %", crit_chance_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)


DEFENSIVE_STANCE = lambda duration, strength=25: StatusEffect("Defensive Stance", duration, defensive_stance_apply, defensive_stance_remove, strength=strength, is_debuff=False)

def power_stance_apply(character, strength):
    # Calculate the boosts and negatives
    att_boost = int((character.base_attack + character.level_modifiers["attack"] + character.weapon_buff_modifiers["attack"] + character.equipment_modifiers["attack"]) * strength / 100)
    armour_pen_boost = int((character.base_armour_penetration + character.level_modifiers.get("armour_penetration", 0) + character.equipment_modifiers.get("armour_penetration", 0)) * strength / 100)
    crit_damage_boost = int((character.base_crit_damage + character.level_modifiers.get("crit_damage", 0) + character.equipment_modifiers.get("crit_damage", 0)) * strength / 100)
    def_reduce = int((character.base_defence + character.level_modifiers.get("defence", 0) + character.equipment_modifiers.get("defence", 0)) * strength / 100)
    eva_reduce = int((character.base_evasion + character.level_modifiers.get("evasion", 0) + character.equipment_modifiers.get("evasion", 0)) * strength / 100)
    
    # Update the combat_buff_modifiers with current value
    current_att = character.combat_buff_modifiers.get("attack", 0)
    current_armour_pen = character.combat_buff_modifiers.get("armour_penetration", 0)
    current_crit_damage = character.combat_buff_modifiers.get("crit_damage", 0)
    current_def = character.combat_buff_modifiers.get("defence", 0)
    current_eva = character.combat_buff_modifiers.get("evasion", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["attack"] = current_att + att_boost
    character.combat_buff_modifiers["armour_penetration"] = current_armour_pen + armour_pen_boost
    character.combat_buff_modifiers["crit_damage"] = current_crit_damage + crit_damage_boost
    character.combat_buff_modifiers["defence"] = current_def - def_reduce
    character.combat_buff_modifiers["evasion"] = current_eva - eva_reduce
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "increases": {
            "offensive stats": [
                ("Attack", att_boost),
                ("Armour Penetration", armour_pen_boost),
                ("Crit Dmg", crit_damage_boost)
            ]
        },
        "decreases": {
            "defensive stats": [
                ("Defence", def_reduce),
                ("Evasion", eva_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)
    return True
    
def power_stance_remove(character, strength):
    # Calculate the boosts and negatives
    att_boost = int((character.base_attack + character.level_modifiers["attack"] + character.weapon_buff_modifiers["attack"] + character.equipment_modifiers["attack"]) * strength / 100)
    armour_pen_boost = int((character.base_armour_penetration + character.level_modifiers.get("armour_penetration", 0) + character.equipment_modifiers.get("armour_penetration", 0)) * strength / 100)
    crit_damage_boost = int((character.base_crit_damage + character.level_modifiers.get("crit_damage", 0) + character.equipment_modifiers.get("crit_damage", 0)) * strength / 100)
    def_reduce = int((character.base_defence + character.level_modifiers.get("defence", 0) + character.equipment_modifiers.get("defence", 0)) * strength / 100)
    eva_reduce = int((character.base_evasion + character.level_modifiers.get("evasion", 0) + character.equipment_modifiers.get("evasion", 0)) * strength / 100)
    
    # Update the combat_buff_modifiers with current value
    current_att = character.combat_buff_modifiers.get("attack", 0)
    current_armour_pen = character.combat_buff_modifiers.get("armour_penetration", 0)
    current_crit_damage = character.combat_buff_modifiers.get("crit_damage", 0)
    current_def = character.combat_buff_modifiers.get("defence", 0)
    current_eva = character.combat_buff_modifiers.get("evasion", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["attack"] = max(0, current_att - att_boost)
    character.combat_buff_modifiers["armour_penetration"] = max(0, current_armour_pen - armour_pen_boost)
    character.combat_buff_modifiers["crit_damage"] = max(0, current_crit_damage - crit_damage_boost)
    character.combat_buff_modifiers["defence"] = max(0, current_def + def_reduce)
    character.combat_buff_modifiers["evasion"] = max(0, current_eva + eva_reduce)
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "decreases": {
            "offensive stats": [
                ("Attack", att_boost),
                ("Armour Penetration", armour_pen_boost),
                ("Crit Dmg", crit_damage_boost)
            ]
        },
        "increases": {
            "defensive stats": [
                ("Defence", def_reduce),
                ("Evasion", eva_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)

    
POWER_STANCE = lambda duration, strength=25: StatusEffect("Power Stance", duration, power_stance_apply, power_stance_remove, strength=strength, is_debuff=False)

def berserker_stance_apply(character, strength):
    # Calculate the boosts and negatives
    att_boost = int((character.base_attack + character.level_modifiers["attack"] + character.weapon_buff_modifiers["attack"] + character.equipment_modifiers["attack"]))
    armour_pen_boost = int((character.base_armour_penetration + character.level_modifiers.get("armour_penetration", 0) + character.equipment_modifiers.get("armour_penetration", 0)))
    crit_damage_boost = int((character.base_crit_damage + character.level_modifiers.get("crit_damage", 0) + character.equipment_modifiers.get("crit_damage", 0)))
    crit_chance_boost = int((character.base_crit_chance + character.level_modifiers.get("crit_chance", 0) + character.equipment_modifiers.get("crit_chance", 0)))
    def_reduce = int((character.base_defence + character.level_modifiers.get("defence", 0) + character.equipment_modifiers.get("defence", 0)))
    eva_reduce = int((character.base_evasion + character.level_modifiers.get("evasion", 0) + character.equipment_modifiers.get("evasion", 0)))
    bc_reduce = int((character.base_block_chance + character.level_modifiers.get("block_chance", 0) + character.equipment_modifiers.get("block_chance", 0)))
    dr_reduce = int((character.base_damage_reduction + character.level_modifiers.get("damage_reduction", 0) + character.equipment_modifiers.get("damage_reduction", 0)))
    
    # Update the combat_buff_modifiers with current value
    current_att = character.combat_buff_modifiers.get("attack", 0)
    current_armour_pen = character.combat_buff_modifiers.get("armour_penetration", 0)
    current_crit_damage = character.combat_buff_modifiers.get("crit_damage", 0)
    current_crit_chance = character.combat_buff_modifiers.get("crit_chance", 0)
    current_def = character.combat_buff_modifiers.get("defence", 0)
    current_eva = character.combat_buff_modifiers.get("evasion", 0)
    current_bc = character.combat_buff_modifiers.get("block_chance", 0)
    current_dr = character.combat_buff_modifiers.get("damage_reduction", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["attack"] = current_att + att_boost
    character.combat_buff_modifiers["armour_penetration"] = current_armour_pen + armour_pen_boost
    character.combat_buff_modifiers["crit_damage"] = current_crit_damage + crit_damage_boost
    character.combat_buff_modifiers["crit_chance"] = current_crit_chance + crit_chance_boost
    character.combat_buff_modifiers["defence"] = current_def - def_reduce
    character.combat_buff_modifiers["evasion"] = current_eva - eva_reduce
    character.combat_buff_modifiers["block_chance"] = current_bc - bc_reduce
    character.combat_buff_modifiers["damage_reduction"] = current_dr - dr_reduce
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "increases": {
            "offensive stats": [
                ("Attack", att_boost),
                ("Armour Penetration", armour_pen_boost),
                ("Crit Dmg", crit_damage_boost),
                ("Crit %", crit_chance_boost)
            ]
        },
        "decreases": {
            "defensive stats": [
                ("Defence", def_reduce),
                ("Evasion", eva_reduce),
                ("Block Chance", bc_reduce),
                ("Damage Reduction", dr_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)
    return True
    
def berserker_stance_remove(character, strength):
    # Calculate the boosts and negatives
    att_boost = int((character.base_attack + character.level_modifiers["attack"] + character.weapon_buff_modifiers["attack"] + character.equipment_modifiers["attack"]))
    armour_pen_boost = int((character.base_armour_penetration + character.level_modifiers.get("armour_penetration", 0) + character.equipment_modifiers.get("armour_penetration", 0)))
    crit_damage_boost = int((character.base_crit_damage + character.level_modifiers.get("crit_damage", 0) + character.equipment_modifiers.get("crit_damage", 0)))
    crit_chance_boost = int((character.base_crit_chance + character.level_modifiers.get("crit_chance", 0) + character.equipment_modifiers.get("crit_chance", 0)))
    def_reduce = int((character.base_defence + character.level_modifiers.get("defence", 0) + character.equipment_modifiers.get("defence", 0)))
    eva_reduce = int((character.base_evasion + character.level_modifiers.get("evasion", 0) + character.equipment_modifiers.get("evasion", 0)))
    bc_reduce = int((character.base_block_chance + character.level_modifiers.get("block_chance", 0) + character.equipment_modifiers.get("block_chance", 0)))
    dr_reduce = int((character.base_damage_reduction + character.level_modifiers.get("damage_reduction", 0) + character.equipment_modifiers.get("damage_reduction", 0)))
    
    # Update the combat_buff_modifiers with current value
    current_att = character.combat_buff_modifiers.get("attack", 0)
    current_armour_pen = character.combat_buff_modifiers.get("armour_penetration", 0)
    current_crit_damage = character.combat_buff_modifiers.get("crit_damage", 0)
    current_crit_chance = character.combat_buff_modifiers.get("crit_chance", 0)
    current_def = character.combat_buff_modifiers.get("defence", 0)
    current_eva = character.combat_buff_modifiers.get("evasion", 0)
    current_bc = character.combat_buff_modifiers.get("block_chance", 0)
    current_dr = character.combat_buff_modifiers.get("damage_reduction", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["attack"] = max(0, current_att - att_boost)
    character.combat_buff_modifiers["armour_penetration"] = max(0, current_armour_pen - armour_pen_boost)
    character.combat_buff_modifiers["crit_damage"] = max(0, current_crit_damage - crit_damage_boost)
    character.combat_buff_modifiers["crit_chance"] = max(0, current_crit_chance - crit_chance_boost)
    character.combat_buff_modifiers["defence"] = max(0, current_def + def_reduce)
    character.combat_buff_modifiers["evasion"] = max(0, current_eva + eva_reduce)
    character.combat_buff_modifiers["block_chance"] = max(0, current_bc + bc_reduce)
    character.combat_buff_modifiers["damage_reduction"] = max(0, current_dr + dr_reduce)
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "decreases": {
            "offensive stats": [
                ("Attack", att_boost),
                ("Armour Penetration", armour_pen_boost),
                ("Crit Dmg", crit_damage_boost),
                ("Crit %", crit_chance_boost)
            ]
        },
        "increases": {
            "defensive stats": [
                ("Defence", def_reduce),
                ("Evasion", eva_reduce),
                ("Block Chance", bc_reduce),
                ("Damage Reduction", dr_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)

    
BERSERKER_STANCE = lambda duration, strength=25: StatusEffect("Berserker Stance", duration, berserker_stance_apply, berserker_stance_remove, strength=strength, is_debuff=False)

def accuracy_stance_apply(character, strength):
    # Calculate the boosts and negatives
    acc_boost = int((character.base_accuracy + character.level_modifiers["accuracy"] + character.weapon_buff_modifiers["accuracy"] + character.equipment_modifiers["accuracy"]) * strength / 50)
    crit_chance_boost = int((character.base_crit_chance + character.level_modifiers["crit_chance"] + character.weapon_buff_modifiers.get("crit_chance", 0) + character.equipment_modifiers.get("crit_chance", 0) * strength / 75))
    block_reduce = int((character.base_block_chance + character.level_modifiers.get("block_chance", 0) + character.equipment_modifiers.get("block_chance", 0)) * strength / 50)
    eva_reduce = int((character.base_evasion + character.level_modifiers.get("evasion", 0) + character.equipment_modifiers.get("evasion", 0)) * strength / 50)
    
    # Update the combat_buff_modifiers with the current boost
    current_acc = character.combat_buff_modifiers.get("accuracy", 0)
    current_crit_chance = character.combat_buff_modifiers.get("crit_chance", 0)
    current_eva = character.combat_buff_modifiers.get("evasion", 0)
    current_block = character.combat_buff_modifiers.get("block_chance", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["accuracy"] = current_acc + acc_boost
    character.combat_buff_modifiers["crit_chance"] = current_crit_chance + crit_chance_boost
    character.combat_buff_modifiers["evasion"] = current_eva - eva_reduce
    character.combat_buff_modifiers["block_chance"] = current_block - block_reduce
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "increases": {
            "offensive stats": [
                ("Accuracy", acc_boost),
                ("Crit %", crit_chance_boost)
            ]
        },
        "decreases": {
            "defensive stats": [
                ("Evasion", eva_reduce),
                ("Block Chance", block_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)
    return True
    
def accuracy_stance_remove(character, strength):
    # Calculate the boosts and negatives
    acc_boost = int((character.base_accuracy + character.level_modifiers["accuracy"] + character.weapon_buff_modifiers["accuracy"] + character.equipment_modifiers["accuracy"]) * strength / 50)
    crit_chance_boost = int((character.base_crit_chance + character.level_modifiers["crit_chance"] + character.weapon_buff_modifiers.get("crit_chance", 0) + character.equipment_modifiers.get("crit_chance", 0) * strength / 75))
    block_reduce = int((character.base_block_chance + character.level_modifiers.get("block_chance", 0) + character.equipment_modifiers.get("block_chance", 0)) * strength / 50)
    eva_reduce = int((character.base_evasion + character.level_modifiers.get("evasion", 0) + character.equipment_modifiers.get("evasion", 0)) * strength / 50)
    
    # Update the combat_buff_modifiers with the current boost
    current_acc = character.combat_buff_modifiers.get("accuracy", 0)
    current_crit_chance = character.combat_buff_modifiers.get("crit_chance", 0)
    current_eva = character.combat_buff_modifiers.get("evasion", 0)
    current_block = character.combat_buff_modifiers.get("block_chance", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["accuracy"] = max(0, current_acc - acc_boost)
    character.combat_buff_modifiers["crit_chance"] = max(0, current_crit_chance - crit_chance_boost)
    character.combat_buff_modifiers["evasion"] = max(0, current_eva - eva_reduce)
    character.combat_buff_modifiers["block_chance"] = max(0, current_block - block_reduce)
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "decreases": {
            "offensive stats": [
                ("Accuracy", acc_boost),
                ("Crit %", crit_chance_boost)
            ]
        },
        "increases": {
            "defensive stats": [
                ("Evasion", eva_reduce),
                ("Block Chance", block_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)

    
ACCURACY_STANCE = lambda duration, strength=25: StatusEffect("Accuracy Stance", duration, accuracy_stance_apply, accuracy_stance_remove, strength=strength, is_debuff=False)

def evasion_stance_apply(character, strength):
    # Calculate boosts and negatives
    eva_boost = int((character.base_evasion + character.level_modifiers.get("evasion", 0) + character.equipment_modifiers.get("evasion", 0)) * strength / 50)
    crit_chance_boost = int((character.base_crit_chance + character.level_modifiers.get("crit_chance", 0) + character.equipment_modifiers.get("crit_chance", 0)) * strength / 75)
    crit_damage_boost = int((character.base_crit_damage + character.level_modifiers.get("crit_damage", 0) + character.equipment_modifiers.get("crit_damage", 0)) * strength / 75)
    def_reduce = int((character.base_defence + character.level_modifiers.get("defence", 0) + character.equipment_modifiers.get("defence", 0)) * strength / 50)
    bc_reduce = int((character.base_block_chance + character.level_modifiers.get("block_chance", 0) + character.equipment_modifiers.get("block_chance", 0)) * strength / 50)
    dr_reduce = int((character.base_damage_reduction + character.level_modifiers.get("damage_reduction", 0) + character.equipment_modifiers.get("damage_reduction", 0)) * strength / 50)

    # Update the combat_buff_modifiers with the current boost
    current_eva = character.combat_buff_modifiers.get("evasion", 0)
    current_crit_chance = character.combat_buff_modifiers.get("crit_chance", 0)
    current_crit_damage = character.combat_buff_modifiers.get("crit_damage", 0)
    current_def = character.combat_buff_modifiers.get("defence", 0)
    current_bc = character.combat_buff_modifiers.get("block_chance", 0)
    current_dr = character.combat_buff_modifiers.get("damage_reduction", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["evasion"] = current_eva + eva_boost
    character.combat_buff_modifiers["crit_chance"] = current_crit_chance + crit_chance_boost
    character.combat_buff_modifiers["crit_damage"] = current_crit_damage + crit_damage_boost
    character.combat_buff_modifiers["defence"] = current_def - def_reduce
    character.combat_buff_modifiers["block_chance"] = current_bc - bc_reduce
    character.combat_buff_modifiers["damage_reduction"] = current_dr - dr_reduce
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "increases": {
            "offensive stats": [
                ("Evasion", eva_boost),
                ("Crit %", crit_chance_boost),
                ("Crit Dmg", crit_damage_boost)
            ]
        },
        "decreases": {
            "defensive stats": [
                ("Defence", def_reduce),
                ("Block Chance", bc_reduce),
                ("Damage Reduction", dr_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)
    return True

def evasion_stance_remove(character, strength):
    # Calculate boosts and negatives
    eva_boost = int((character.base_evasion + character.level_modifiers.get("evasion", 0) + character.equipment_modifiers.get("evasion", 0)) * strength / 50)
    crit_chance_boost = int((character.base_crit_chance + character.level_modifiers.get("crit_chance", 0) + character.equipment_modifiers.get("crit_chance", 0)) * strength / 75)
    crit_damage_boost = int((character.base_crit_damage + character.level_modifiers.get("crit_damage", 0) + character.equipment_modifiers.get("crit_damage", 0)) * strength / 75)
    def_reduce = int((character.base_defence + character.level_modifiers.get("defence", 0) + character.equipment_modifiers.get("defence", 0)) * strength / 50)
    bc_reduce = int((character.base_block_chance + character.level_modifiers.get("block_chance", 0) + character.equipment_modifiers.get("block_chance", 0)) * strength / 50)
    dr_reduce = int((character.base_damage_reduction + character.level_modifiers.get("damage_reduction", 0) + character.equipment_modifiers.get("damage_reduction", 0)) * strength / 50)

    # Update the combat_buff_modifiers with the current boost
    current_eva = character.combat_buff_modifiers.get("evasion", 0)
    current_crit_chance = character.combat_buff_modifiers.get("crit_chance", 0)
    current_crit_damage = character.combat_buff_modifiers.get("crit_damage", 0)
    current_def = character.combat_buff_modifiers.get("defence", 0)
    current_bc = character.combat_buff_modifiers.get("block_chance", 0)
    current_dr = character.combat_buff_modifiers.get("damage_reduction", 0)
    
    # Add on the boost or reduction to the combat_buff_modifiers
    character.combat_buff_modifiers["evasion"] = max(0, current_eva - eva_boost)
    character.combat_buff_modifiers["crit_chance"] = max(0, current_crit_chance - crit_chance_boost)
    character.combat_buff_modifiers["crit_damage"] = max(0, current_crit_damage - crit_damage_boost)
    character.combat_buff_modifiers["defence"] = max(0, current_def + def_reduce)
    character.combat_buff_modifiers["block_chance"] = max(0, current_bc + bc_reduce)
    character.combat_buff_modifiers["damage_reduction"] = max(0, current_dr + dr_reduce)
    
    character.recalculate_stats()
    
    # Create stat changes dictionary
    stat_changes = {
        "decreases": {
            "offensive stats": [
                ("Evasion", eva_boost),
                ("Crit %", crit_chance_boost),
                ("Crit Dmg", crit_damage_boost)
            ]
        },
        "increases": {
            "defensive stats": [
                ("Defence", def_reduce),
                ("Block Chance", bc_reduce),
                ("Damage Reduction", dr_reduce)
            ]
        }
    }
    create_stance_message(character.name, stat_changes)

EVASION_STANCE = lambda duration, strength=25: StatusEffect("Evasion Stance", duration, evasion_stance_apply, evasion_stance_remove, strength=strength, is_debuff=False)

def weaken_apply(character, strength):
    character.apply_debuff("attack", strength)
    print(f"{character.name}'s attack is reduced by {strength}!")
    return True

def weaken_remove(character, strength):
    character.remove_debuff("attack", strength)
    print(f"{character.name}'s Attack weaken has worn off.")
    
ATTACK_WEAKEN = lambda duration, strength: StatusEffect("Attack Weaken", duration, weaken_apply, weaken_remove, strength=strength, is_debuff=True)
