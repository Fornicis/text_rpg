import random

class StatusEffect:
    def __init__(self, name, duration, effect_func, strength = 1, is_debuff = False, stackable = False):
        self.name = name
        self.remaining_duration = duration
        self.initial_duration = duration
        self.effect_func = effect_func
        self.strength = strength
        self.stackable = stackable
        self.is_debuff = is_debuff
        
    def apply(self, character):
        #print(f"Applying {self.name} effect to {character.name}")  # Debug output
        return self.effect_func(character, self.strength)
    
    def update(self, character):
        self.apply(character)
        self.remaining_duration -= 1
        #print(f"Updated {self.name} effect, {self.remaining_duration} turns remaining")  # Debug output
        return self.remaining_duration > 0
    
    def reset_duration(self):
        self.remaining_duration = self.initial_duration
        #print(f"Reset duration of {self.name} to {self.remaining_duration}") # Debug output
    
    def get_remaining_duration(self):
        return self.remaining_duration
    
    def __str__(self):
        if self.stackable:
            return f"{self.name} ({self.strength} stacks, {self.remaining_duration} turns remaining)"
        return f"{self.name} ({self.remaining_duration} turns remaining)"
    
def burn_effect(character, strength):
    burn_stack = strength
    character.burn_stack += burn_stack
    damage = max(1, int(character.max_hp * 0.02 * character.burn_stack))
    character.take_damage(damage)
    print(f"{character.name} takes {damage} burn damage!")

def poison_effect(character, strength):
    poison_stack = strength
    character.poison_stack += poison_stack  # Use the highest poison stack
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
        
def self_damage_effect(character, strength):
    damage = int(strength * 0.2) # Deals 20% of original damage to user
    character.take_damage(damage)
    print(f"{character.name} takes {damage} self-damage from their reckless attack!")
    
def stamina_drain_effect(character, strength):
    if hasattr(character, 'stamina'):
        max_drain = int(strength * 0.2)  # 20% of the damage dealt
        stamina_loss = max(10, min(max_drain, character.stamina))  # Minimum 10, maximum 20% of damage, capped at current stamina
        character.use_stamina(stamina_loss)
        print(f"{character.name} lost {stamina_loss} stamina from the draining attack!")
    else:
        print(f"The draining attack has no effect on {character.name}!")
        
def damage_reflect(character, strength, damage_dealt):
    if damage_dealt > 0:
        reflected_damage = int(damage_dealt * 0.5 * strength)
        print(f"{character.name} reflects {reflected_damage} damage!")
        return reflected_damage
    else:
        print(f"{character.name} has a reflective barrier active!")
        return 0

# Define StatusEffect instances for common effects
BURN = lambda duration, strength=1: StatusEffect("Burn", duration, burn_effect, strength, is_debuff=True, stackable=True)
POISON = lambda duration, strength=1: StatusEffect("Poison", duration, poison_effect, strength, is_debuff=True, stackable=True)
FREEZE = lambda duration, strength=1: StatusEffect("Freeze", duration, freeze_effect, strength, is_debuff=True)
STUN = lambda duration, strength=1: StatusEffect("Stun", duration, stun_effect, strength, is_debuff=True)
SELF_DAMAGE = lambda strength: StatusEffect("Self Damage", 1, self_damage_effect, strength, is_debuff=True)
STAMINA_DRAIN = lambda strength: StatusEffect("Stamina Drain", 1, stamina_drain_effect, strength, is_debuff=True)
DAMAGE_REFLECT = lambda duration, strength=1: StatusEffect("Damage Reflect", duration, damage_reflect, strength, is_debuff=False)