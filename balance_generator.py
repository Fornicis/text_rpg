# balance_generator.py
from enemies import TIER_RANGES, get_stat_range, generate_balanced_stats

def generate_random_ranges(tier):
   stats = {}
   for stat in ["hp_percent", "attack_percent", "defence_percent", 
                "accuracy_percent", "evasion_percent", "crit_chance_percent",
                "crit_damage_percent", "armour_penetration_percent", 
                "damage_reduction_percent", "block_chance_percent"]:
       min_val, max_val = get_stat_range(tier, stat)
       base = (min_val + max_val) // 2  # Get middle value
       stats[stat] = f"random.randint({base-2}, {base+3})"  # ±5% variation
   return stats

tier = "boss"  # Change as needed
stats = generate_random_ranges(tier)
for stat, value in stats.items():
   print(f'"{stat}": {value},')