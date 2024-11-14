import random
from display import pause

class StatusEffect:
    def __init__(self, name, duration, is_debuff=False, stackable=False):
        self.name = name
        self.remaining_duration = duration
        self.initial_duration = duration
        self.is_debuff = is_debuff
        self.stackable = stackable
        self.strength = 1
        self.is_active = True
    
    def on_apply(self, character):
        """Override this method to implement effect application logic"""
        pass

    def on_remove(self, character):
        """Override this method to implement effect removal logic"""
        pass

    def on_tick(self, character):
        """Override this method to implement per-turn effect logic"""
        pass

    def update(self, character):
        if self.is_active:
            self.on_tick(character)
            self.remaining_duration -= 1
            
            if self.remaining_duration <= 0:
                self.on_remove(character)
                self.is_active = False
                return False, f"{self.name} has worn off from {character.name}."
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

class DotEffect(StatusEffect):
    def __init__(self, name, duration, base_damage, is_percent=False, stackable=True):
        super().__init__(name, duration, is_debuff=True, stackable=stackable)
        self.base_damage = base_damage
        self.is_percent = is_percent

    def calculate_damage(self, character):
        if self.is_percent:
            return max(1, int(character.max_hp * self.base_damage * self.strength))
        return self.base_damage * self.strength

    def on_apply(self, character):
        print(f"{character.name} is afflicted with {self.name}! ({self.strength} stack(s), {self.strength * 2} damage per turn)")
        return True
    
    def on_tick(self, character):
        damage = self.calculate_damage(character)
        character.take_damage(damage)
        print(f"{character.name} takes {damage} {self.name.lower()} damage! ({self.strength} stack(s))")

class StatModifier(StatusEffect):
    def __init__(self, name, duration, stat_changes, is_debuff=False):
        super().__init__(name, duration, is_debuff)
        self.stat_changes = stat_changes
        
    def on_apply(self, character):
        for stat, value in self.stat_changes.items():
            if self.is_debuff:
                character.apply_debuff(stat, value)
            else:
                current = character.combat_buff_modifiers.get(stat, 0)
                character.combat_buff_modifiers[stat] = current + value
        character.recalculate_stats()
        return True

    def on_remove(self, character):
        for stat, value in self.stat_changes.items():
            if self.is_debuff:
                character.remove_debuff(stat, value)
            else:
                current = character.combat_buff_modifiers.get(stat, 0)
                character.combat_buff_modifiers[stat] = max(0, current - value)
        character.recalculate_stats()

class ControlEffect(StatusEffect):
    def __init__(self, name, duration, control_type, chance=0.8):
        super().__init__(name, duration, is_debuff=True)
        self.control_type = control_type
        self.chance = chance

    def on_apply(self, character):
        if random.random() < self.chance:
            setattr(character, self.control_type, True)
            return True
        else:
            print(f"{character.name} resists the {self.name.lower()} effect!")
            return False

    def on_remove(self, character):
        setattr(character, self.control_type, False)

class StanceEffect(StatusEffect):
    def __init__(self, name, duration, buff_percents, debuff_percents):
        super().__init__(name, duration)
        self.buff_percents = buff_percents
        self.debuff_percents = debuff_percents
        self.applied_buffs = {}
        self.applied_debuffs = {}

    def calculate_stat_change(self, character, stat, percent):
        base = getattr(character, f"base_{stat}", 0)
        level_mod = character.level_modifiers.get(stat, 0)
        equip_mod = character.equipment_modifiers.get(stat, 0)
        weapon_mod = character.weapon_buff_modifiers.get(stat, 0)
        
        total_stat = base + level_mod + equip_mod + weapon_mod
        return int(total_stat * percent / 100)

    def on_apply(self, character):
        # Calculate and apply buffs
        for stat, percent in self.buff_percents.items():
            value = self.calculate_stat_change(character, stat, percent)
            current = character.combat_buff_modifiers.get(stat, 0)
            character.combat_buff_modifiers[stat] = current + value
            self.applied_buffs[stat] = value
            
        # Calculate and apply debuffs
        for stat, percent in self.debuff_percents.items():
            value = self.calculate_stat_change(character, stat, percent)
            current = character.combat_buff_modifiers.get(stat, 0)
            character.combat_buff_modifiers[stat] = current - value
            self.applied_debuffs[stat] = value
            
        character.recalculate_stats()
        self._display_changes(character)
        return True

    def on_remove(self, character):
        # Remove buffs
        for stat, value in self.applied_buffs.items():
            current = character.combat_buff_modifiers.get(stat, 0)
            character.combat_buff_modifiers[stat] = max(0, current - value)
            
        # Remove debuffs
        for stat, value in self.applied_debuffs.items():
            current = character.combat_buff_modifiers.get(stat, 0)
            character.combat_buff_modifiers[stat] = max(0, current + value)
            
        character.recalculate_stats()

    def _display_changes(self, character):
        print(f"\n{character.name} enters {self.name}!")
        if self.applied_buffs:
            print("Increased stats:")
            for stat, value in self.applied_buffs.items():
                if value > 0:
                    print(f"- {stat.replace('_', ' ').title()}: +{value} ({self.buff_percents[stat]}%)")
        if self.applied_debuffs:
            print("Decreased stats:")
            for stat, value in self.applied_debuffs.items():
                if value > 0:
                    print(f"- {stat.replace('_', ' ').title()}: -{value} ({self.debuff_percents[stat]}%)")

# Specific Effect Implementations
class Burn(DotEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Burn", duration, 0.03, is_percent=True)
        self.strength = strength

class Poison(DotEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Poison", duration, 2, is_percent=False)
        self.strength = strength

class Stun(ControlEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Stun", duration, "stunned")
        self.strength = strength
        
    def on_apply(self, character):
        if random.random() < self.chance:
            setattr(character, self.control_type, True)
            print(f"{character.name} is stunned!")
            pause()
            return True
        else:
            print(f"{character.name} resists the stun effect!")
            return False
        
    def on_remove(self, character):
        setattr(character, self.control_type, False)

class Freeze(ControlEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Freeze", duration, "frozen", chance=0.5)
        self.strength = strength
        
    def on_apply(self, character):
        success = super().on_apply(character)
        if success:
            print(f"{character.name} is frozen solid! (Block disabled, +25% chance to be critically hit!)")
        return success

class Confusion(ControlEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Confusion", duration, "confused", chance=0.5)
        self.strength = strength

class DefensiveStance(StanceEffect):
    def __init__(self, duration, strength=33):
        buff_percents = {
            "defence": strength,
            "block_chance": strength,
            "damage_reduction": strength
        }
        debuff_percents = {
            "attack": strength // 2,
            "crit_chance": strength // 2
        }
        super().__init__("Defensive Stance", duration, buff_percents, debuff_percents)

class PowerStance(StanceEffect):
    def __init__(self, duration, strength=33):
        buff_percents = {
            "attack": strength,
            "armour_penetration": strength,
            "crit_damage": strength
        }
        debuff_percents = {
            "defence": strength // 2,
            "evasion": strength // 2
        }
        super().__init__("Power Stance", duration, buff_percents, debuff_percents)

class BerserkerStance(StanceEffect):
    def __init__(self, duration, strength=50):
        buff_percents = {
            "attack": strength * 2,
            "armour_penetration": strength,
            "crit_chance": strength,
            "crit_damage": strength * 2
        }
        debuff_percents = {
            "defence": strength,
            "evasion": strength,
            "block_chance": strength,
            "damage_reduction": strength
        }
        super().__init__("Berserker Stance", duration, buff_percents, debuff_percents)

class AccuracyStance(StanceEffect):
    def __init__(self, duration, strength=33):
        buff_percents = {
            "accuracy": strength * 2,
            "crit_chance": strength
        }
        debuff_percents = {
            "block_chance": strength // 2,
            "evasion": strength // 2
        }
        super().__init__("Accuracy Stance", duration, buff_percents, debuff_percents)

class EvasionStance(StanceEffect):
    def __init__(self, duration, strength=33):
        buff_percents = {
            "evasion": strength * 2,
            "crit_chance": strength,
            "crit_damage": strength
        }
        debuff_percents = {
            "defence": strength,
            "block_chance": strength,
            "damage_reduction": strength
        }
        super().__init__("Evasion Stance", duration, buff_percents, debuff_percents)

# Special Effects
class Vampiric(StatusEffect):
    def __init__(self, strength):
        super().__init__("Vampiric", 0, is_debuff=False)
        self.strength = strength

    def on_apply(self, character):
        heal_amount = int(self.strength * 0.33)
        character.heal(heal_amount)
        print(f"{character.name} healed {heal_amount} damage from their vampiric attack!")
        return True

class StaminaDrain(StatusEffect):
    def __init__(self, strength):
        super().__init__("Stamina Drain", 1, is_debuff=True)
        self.strength = strength

    def on_apply(self, character):
        if hasattr(character, 'stamina'):
            max_drain = int(self.strength * 0.33)
            stamina_loss = max(10, min(max_drain, character.stamina))
            character.use_stamina(stamina_loss)
            print(f"{character.name} lost {stamina_loss} stamina from the draining attack!")
        return True

class DamageReflect(StatusEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Damage Reflect", duration, is_debuff=False)
        self.strength = strength

    def on_apply(self, character):
        return True

    def apply_func(self, character, strength, damage_dealt=0):
        if damage_dealt > 0:
            reflected_damage = int(damage_dealt * 0.5)
            return reflected_damage, True
        return 0, True

class SelfDamage(StatusEffect):
    def __init__(self, strength, attack_type="reckless"):
        super().__init__("Self Damage", 1, is_debuff=True)
        self.strength = strength
        self.attack_type = attack_type

    def on_apply(self, character):
        damage = int(self.strength * 0.2)  # 20% of the damage dealt
        character.take_damage(damage)
        print(f"{character.name} takes {damage} self-damage from their {self.attack_type} attack!")
        return True

class DefenceBreak(StatModifier):
    def __init__(self, duration, strength, damage_dealt=0):
        # Calculate defense reduction based on damage and strength multiplier
        reduction = int((damage_dealt * 0.33) * strength)  # 33% of damage * strength multiplier
        super().__init__("Defence Break", duration, {"defence": reduction}, is_debuff=True)
        self.strength = strength

    def on_apply(self, character):
        print(f"{character.name}'s defence is reduced by {self.stat_changes['defence']}!")
        return super().on_apply(character)

    def on_remove(self, character):
        print(f"{character.name}'s Defence Break effect has worn off.")
        super().on_remove(character)

class AttackWeaken(StatModifier):
    def __init__(self, duration, strength, damage_dealt=0):
        # Calculate attack reduction based on damage and strength multiplier
        reduction = int((damage_dealt * 0.33) * strength)  # 33% of damage * strength multiplier
        super().__init__("Attack Weaken", duration, {"attack": reduction}, is_debuff=True)
        self.strength = strength

    def on_apply(self, character):
        print(f"{character.name}'s attack is reduced by {self.stat_changes['attack']}!")
        return super().on_apply(character)

    def on_remove(self, character):
        print(f"{character.name}'s Attack Weaken effect has worn off.")
        super().on_remove(character)

# Factory functions to maintain compatibility with existing code
def BURN(duration, strength=1): return Burn(duration, strength)
def POISON(duration, strength=1): return Poison(duration, strength)
def STUN(duration, strength=1): return Stun(duration, strength)
def FREEZE(duration, strength=1): return Freeze(duration, strength)
def CONFUSION(duration, strength=1): return Confusion(duration, strength)
def VAMPIRIC(strength): return Vampiric(strength)
def STAMINA_DRAIN(strength): return StaminaDrain(strength)
def DAMAGE_REFLECT(duration, strength=1): return DamageReflect(duration, strength)
def DEFENCE_BREAK(duration, strength, damage_dealt=0): return DefenceBreak(duration, strength, damage_dealt)
def ATTACK_WEAKEN(duration, strength, damage_dealt=0): return AttackWeaken(duration, strength, damage_dealt)
def DEFENSIVE_STANCE(duration, strength=33): return DefensiveStance(duration, strength)
def POWER_STANCE(duration, strength=33): return PowerStance(duration, strength)
def BERSERKER_STANCE(duration, strength=50): return BerserkerStance(duration, strength)
def ACCURACY_STANCE(duration, strength=33): return AccuracyStance(duration, strength)
def EVASION_STANCE(duration, strength=33): return EvasionStance(duration, strength)
def SELF_DAMAGE(strength, attack_type="reckless"): return SelfDamage(strength, attack_type)
