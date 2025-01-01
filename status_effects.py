import random

class StatusEffect:
    def __init__(self, name, duration, is_debuff=False, stackable=False):
        self.name = name
        self.remaining_duration = duration
        self.initial_duration = duration
        self.is_debuff = is_debuff
        self.stackable = stackable
        self.strength = 1
        self.is_active = True
        self.battle_display = None
    
    def set_battle_display(self, battle_display):
        self.battle_display = battle_display
        
    def display_message(self, message):
        if self.battle_display:
            self.battle_display.draw_battle_message(message)
        else:
            print(message)
    
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
                return False, f"\n{self.name} has worn off from {character.name}."
            return True, None
        return False, None

    def reset_duration(self):
        self.remaining_duration = self.initial_duration

    def __str__(self):
        if not self.is_active:
            return ""
        if self.stackable:
            return f"\n{self.name} ({self.strength} stacks, {self.remaining_duration} turns)"
        return f"\n{self.name} ({self.remaining_duration} turns)"

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
        self.display_message(f"\n{character.name} is afflicted with {self.name}! ({self.strength} stack(s))")
        return True
    
    def on_tick(self, character):
        damage = self.calculate_damage(character)
        character.take_damage(damage)
        self.display_message(f"\n{character.name} takes {damage} {self.name.lower()} damage! ({self.strength} stack(s))")
        
    def on_remove(self, character):
        self.display_message(f"\nThe {self.name.title()} effect has worn off from {character.name}.")

class StatModifier(StatusEffect):
    def __init__(self, name, duration, stat_changes, is_debuff=False):
        super().__init__(name, duration, is_debuff)
        self.stat_changes = stat_changes
        self.total_reductions = {stat: value for stat, value in stat_changes.items()}

    def on_apply(self, character):
        #print(f"\nDEBUG: Status effects before: {character.status_effects} (Stat Modifier On_Apply)")
        #print(f"DEBUG: Current debuffs: {character.debuff_modifiers} (Stat Modifier On_apply)")
        #print(f"DEBUG: New reduction: {self.stat_changes} (Stat Modifier On_apply)")
        
        found_effect = next((effect for effect in character.status_effects 
                           if effect.name == self.name), None)
        
        if found_effect:
            for stat, value in self.stat_changes.items():
                found_effect.total_reductions[stat] += value
                if self.is_debuff:
                    character.apply_debuff(stat, value)
                print(f"DEBUG: Stacked {stat} reduction to {found_effect.total_reductions[stat]} (Stat Modifier On_apply)")
            found_effect.remaining_duration = max(found_effect.remaining_duration, self.initial_duration)
            return False

        # New effect
        for stat, value in self.stat_changes.items():
            if self.is_debuff:
                character.apply_debuff(stat, value)
        return True

    def on_remove(self, character):
        print(f"DEBUG: Removing all debuffs for {self.name}")
        for stat in self.stat_changes.keys():
            if self.is_debuff:
                character.debuff_modifiers[stat] = 0
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
            self.display_message(f"\n{character.name} resists the {self.name.lower()} effect!")
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
        messages = []
        messages.append(f"\n{character.name} enters {self.name}!")

        if self.applied_buffs:
            messages.append("\nIncreased stats:")
            for stat, value in self.applied_buffs.items():
                if value > 0:
                    stat_name = stat.replace('_', ' ').title()
                    messages.append(f"\n- {stat_name}: +{value} ({self.buff_percents[stat]}%)")

        if self.applied_debuffs:
            messages.append("\nDecreased stats:")
            for stat, value in self.applied_debuffs.items():
                if value > 0:
                    stat_name = stat.replace('_', ' ').title()
                    messages.append(f"\n- {stat_name}: -{value} ({self.debuff_percents[stat]}%)")

        # Join all messages and display as one block
        full_message = "\n".join(messages)
        self.display_message(full_message)

# Specific Effect Implementations
class Burn(DotEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Burn", duration, 0.01, is_percent=True)
        self.strength = strength
        
    def on_apply(self, character):
        self.display_message(f"\n{character.name} is afflicted with {self.name}! ({self.strength} stack(s), {int(self.strength * (character.max_hp * 0.01))} damage per turn)")
        return True

class Poison(DotEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Poison", duration, 5, is_percent=False)
        self.strength = strength
        
    def on_apply(self, character):
        self.display_message(f"\n{character.name} is afflicted with {self.name}! ({self.strength} stack(s), {self.strength * 5} damage per turn)")
        return True

class Stun(ControlEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Stun", duration, "stunned")
        self.strength = strength
        
    def on_apply(self, character):
        if random.random() < self.chance:
            setattr(character, self.control_type, True)
            self.display_message(f"\n{character.name} is stunned!")
            return True
        else:
            self.display_message(f"\n{character.name} resists the stun effect!")
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
            self.display_message(f"\n{character.name} is frozen solid! (Block disabled, +25% chance to be critically hit!)")
        return success
    
    def on_remove(self, character):
        super().on_remove(character)
        self.display_message(f"\n{character.name} is no longer frozen.")
        character.frozen = False

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
        self.display_message(f"\n{character.name} healed {heal_amount} damage from their vampiric attack!")
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
            self.display_message(f"\n{character.name} lost {stamina_loss} stamina from the draining attack!")
        return True

class DamageReflect(StatusEffect):
    def __init__(self, duration, strength=1):
        super().__init__("Damage Reflect", duration, is_debuff=False)
        self.strength = strength

    def on_apply(self, character):
        self.display_message(f"\n{character.name} is surrounded by a reflective shield!")
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
        if self.battle_display:
            self.display_message(f"\n{character.name} takes {damage} recoil damage from their {self.attack_type} attack!")
        return False
    
class DefenceBreak(StatModifier):
   def __init__(self, duration, strength, damage_dealt=0):
       reduction = int((damage_dealt * 0.33) * strength)
       super().__init__("Defence Break", duration, {"defence": reduction}, is_debuff=True)
       self.reduction = reduction

   def on_apply(self, character):
       #print(f"\nDEBUG: Status effects before: {character.status_effects} (Defence Break On_Apply)")
       #print(f"DEBUG: Current debuffs: {character.debuff_modifiers} (Defence Break On_apply)")
       #print(f"DEBUG: New reduction: {self.reduction} (Defence Break On_apply)")
       #print("DEBUG: Creating new effect (Defence Break On_apply)")
       if "defence" not in character.debuff_modifiers:
            character.debuff_modifiers["defence"] = 0
       character.debuff_modifiers["defence"] += self.reduction
       self.display_message(f"\n{character.name} is affected by Defence Break! {self.reduction} Defence reduction!")
       character.recalculate_stats()
       return True

   def on_remove(self, character):
       #print(f"DEBUG: Removing reduction: {self.reduction}")
       super().on_remove(character)
       
class AttackWeaken(StatModifier):
    def __init__(self, duration, strength, damage_dealt=0):
        reduction = int((damage_dealt * 0.33) * strength)
        super().__init__("Attack Weaken", duration, {"attack": reduction}, is_debuff=True)
        self.reduction = reduction

    def on_apply(self, character):
        #print(f"\nDEBUG: Status effects before: {character.status_effects} (Attack Weaken On_Apply)")
        #print(f"DEBUG: Current debuffs: {character.debuff_modifiers} (Attack Weaken On_apply)")
        #print(f"DEBUG: New reduction: {self.reduction}(Attack Weaken On_apply)")
        #print("DEBUG: Creating new effect (Attack Weaken On_apply)")
        if "attack" not in character.debuff_modifiers:
            character.debuff_modifiers["attack"] = 0
        character.debuff_modifiers["attack"] += self.reduction
        self.display_message(f"\n{character.name} is affected by Attack Weaken! {self.reduction} Attack reduction!")
        character.recalculate_stats()
        return True

    def on_remove(self, character):
        #print(f"DEBUG: Removing reduction: {self.reduction}")
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
