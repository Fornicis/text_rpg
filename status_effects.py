import random

class StatusEffect:
    def __init__(self, name, duration, effect_func, strength = 1, is_debuff = False):
        self.name = name
        self.duration = duration
        self.effect_func = effect_func
        self.strength = strength
        self.is_debuff = is_debuff
        
    def apply(self, character):
        self.effect_func(character, self.strength)
    
    def update(self, character):
        self.apply(character)
        self.duration -= 1
        return self.duration > 0
    
    def get_remaining_duration(self):
        return self.duration
    
    def __str__(self):
        return f"{self.name} ({self.duration} turns remaining)"
    
def burn_effect(character, strength):
    damage = max(1, int(character.max_hp * 0.05 * strength))
    character.take_damage(damage)
    print(f"{character.name} takes {damage} burn damage!")

def poison_effect(character, strength):
    character.poison_stack = max(character.poison_stack, strength)  # Use the highest poison stack
    damage = character.poison_stack
    character.take_damage(damage)
    print(f"{character.name} takes {damage} poison damage!")

def freeze_effect(character, strength):
    if random.random() < 0.5 * strength:
        character.frozen = True
        print(f"{character.name} is frozen and loses their next turn!")
    else:
        print(f"{character.name} resists the freeze effect!")

def stun_effect(character, strength):
    if random.random() < 0.3 * strength:
        character.stunned = True
        print(f"{character.name} is stunned and loses their next turn!")
    else:
        print(f"{character.name} resists the stun effect!")

# Define StatusEffect instances for common effects
BURN = lambda duration, strength=1: StatusEffect("Burn", duration, burn_effect, strength, is_debuff=True)
POISON = lambda duration, strength=1: StatusEffect("Poison", duration, poison_effect, strength, is_debuff=True)
FREEZE = lambda duration, strength=1: StatusEffect("Freeze", duration, freeze_effect, strength, is_debuff=True)
STUN = lambda duration, strength=1: StatusEffect("Stun", duration, stun_effect, strength, is_debuff=True)