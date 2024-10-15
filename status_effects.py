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
        if not self.applied_this_turn:
            result = self.apply_func(character, self.strength, *args)
            self.applied_this_turn = True
            self.is_active = result
            return result
        return False

    def remove(self, character):
        if self.remove_func:
            self.remove_func(character, self.strength)
        self.is_active = False

    def update(self, character):
        self.applied_this_turn = False
        if self.is_active:
            self.remaining_duration -= 1
            if self.remaining_duration <= 0:
                self.remove(character)
                return False
            return True
        return False

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
            #print(f"{character.name} is affected by {name}!\n")
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

freeze_apply, freeze_remove = create_chance_effect("Freeze", lambda str: 0.5 * str, lambda char, frozen: setattr(char, 'frozen', frozen))
FREEZE = lambda duration, strength=1: StatusEffect("Freeze", duration, freeze_apply, freeze_remove, strength=strength, is_debuff=True)

stun_apply, stun_remove = create_chance_effect("Stun", lambda str: 0.3 * str, lambda char, stunned: setattr(char, 'stunned', stunned))
STUN = lambda duration, strength=1: StatusEffect("Stun", duration, stun_apply, stun_remove, strength=strength, is_debuff=True)

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

# New effect: Defence Break
def defence_break_apply(character, strength):
    if not hasattr(character, 'original_defence'):
        character.original_defence = character.defence
    defence_reduction = strength
    character.defence = max(0, character.defence - defence_reduction)
    print(f"{character.name}'s defence is reduced by {defence_reduction}!")

def defence_break_remove(character, strength):
    if hasattr(character, 'original_defence'):
        character.defence = character.original_defence
        del character.original_defence
        print(f"{character.name}'s defence has been restored.")

DEFENCE_BREAK = lambda duration, strength: StatusEffect("Defence Break", duration, defence_break_apply, defence_break_remove, strength=strength, is_debuff=True)

def defensive_stance_apply(character, strength):
    if not hasattr(character, 'defensive_stance_boost'):
        defence_boost = int(character.defence * strength / 100)
        character.defensive_stance_boost = defence_boost
        character.defence += defence_boost
        print(f"{character.name}'s defence increased by {defence_boost} due to Defensive Stance.")
    return True

def defensive_stance_remove(character, strength):
    if hasattr(character, 'defensive_stance_boost'):
        character.defence -= character.defensive_stance_boost
        del character.defensive_stance_boost
        print(f"{character.name}'s Defensive Stance has worn off. Defence decreased to {character.defence}.")

DEFENSIVE_STANCE = lambda duration, strength=25: StatusEffect("Defensive Stance", duration, defensive_stance_apply, defensive_stance_remove, strength=strength, is_debuff=False)