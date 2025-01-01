from enemies import Enemy, create_enemy, get_type_for_monster
from game_config import MONSTER_TYPES
from items import create_soulbound_item, SoulCrystal, BossResonance, VariantAffinity, SoulEcho, ElementalResonance, SoulboundItem
from display import Display, RandomEventDisplay, ComplexEventDisplay, VisualInput
from enum import Enum
import random
import pygame

class EventType(Enum):
    BENEFICIAL = "beneficial"
    NEUTRAL  = "neutral"
    DANGEROUS = "dangerous"
    
class RandomEvent:
    def __init__(self, name, description, event_type, choices, conditions=None):
        self.display = Display()
        self.clear_screen = Display.clear_screen
        self.name = name
        self.description = description
        self.event_type = event_type
        self.choices = choices # List of tuples (choice_text, outcome_func)
        self.conditions = conditions or {} # Dictionary of requirements
        self.create_enemy = create_enemy
        
    def can_occur(self, player, location):
        """Check if an event can occur based on conditions"""
        for condition, value in self.conditions.items():
            if condition == "min_level" and player.level < value:
                return False
            elif condition == "location_type" and location not in value:
                return False
            elif condition == "required_item":
                if not any(item.name == value for item in player.inventory):
                    return False
                
        return True
    
    """def display(self):
        Display event and choices
        print(f"\n=== {self.name} ===")
        print(f"\n{self.description}")
        print("\nWhat do you do?")
        for i, (choice_text, _) in enumerate(self.choices, 1):
            print(f"{i}. {choice_text}")"""
            
    def handle_choice(self, choice_idx, player, game):
        """Execute only the chosen outcome"""
        if 0 <= choice_idx < len(self.choices):
            _, outcome_func = self.choices[choice_idx]
            outcome_func(player, game)
            return True
        return False
    
class RandomEventSystem:
    def __init__(self):
        self.events = self._initialise_events()
        
    def _initialise_events(self):
        """Initialise all possible random events."""
        events = []
        
        # Beneficial events
        
        """events.append(RandomEvent(
            "Hidden Cache",
            "You notice something glinting behind some rocks...",
            EventType.BENEFICIAL,
            [
                ("Investigate carefully", self._outcome_hidden_cache_careful),
                ("Quickly grab it", self._outcome_hidden_cache_quick),
                ("Leave it alone", self._outcome_ignore)
            ],
            {"min_level": 1}
        ))
        
        events.append(RandomEvent(
            "Mysterious Traveller",
            "A hooded figure approaches, offering to share their knowledge...",
            EventType.BENEFICIAL,
            [
                ("Accept their offer", self._outcome_traveller_accept),
                ("Politely decline", self._outcome_ignore),
                ("Ask about their journey", self._outcome_traveller_chat)
            ],
            {"min_level": 2}
        ))
        
        events.append(RandomEvent(
            "Wandering Merchant",
            "You encounter a travelling merchant with unusual wares...",
            EventType.BENEFICIAL,
            [
                ("Trade with merchant (Costs half of current gold)", self._outcome_merchant_trade),
                ("Barter items (Trade a random item)", self._outcome_merchant_barter),
                ("Help guard their caravan (Requires 80% stamina)", self._outcome_merchant_guard),
                ("Continue on your way.", self._outcome_ignore)
            ],
            {"min_level": 3}
        ))
        
        events.append(RandomEvent(
            "Ancient Training Grounds",
            "You come across a seemingly ancient and weathered training ground. Some of the equipment nearby looks usable...",
            EventType.BENEFICIAL,
            [
                ("Practice combat techniques (Uses 50% stamina)", self._outcome_training_combat),
                ("Study ancient techniques (Uses 25% stamina)", self._outcome_training_study),
                ("Search for left behind equipment", self._outcome_training_search),
                ("Rest here", self._outcome_training_rest)
            ],
            {"min_level": 2}
        ))
        
        events.append(RandomEvent(
            "Magical Spring",
            "You come across a spring emanating mysterious energy...",
            EventType.BENEFICIAL,
            [
                ("Drink from the spring", self._outcome_spring_drink),
                ("Meditate beside it", self._outcome_spring_meditate),
                ("Fill empty containers", self._outcome_spring_fill),
                ("Wade in the water", self._outcome_spring_wade)
            ],
            {
                "min_level": 4,
                "location_type": ["Forest", "Deepwoods", "Plains", "Mountain", "Swamp", "Desert", "Toxic Swamp", "Valley", "Mountain Peaks", "Scorching Valley", "Death Caves", "Death Valley", "Volcanic Valley"]
            }
        ))
        
        # Neutral Events
        
        events.append(RandomEvent(
            "Ancient Shrine",
            "You come across a weather shrine with a small offering bowl...",
            EventType.NEUTRAL,
            [
                ("Make an offering (Costs 10 gold)", self._outcome_shrine_offer),
                ("Pray respectfully", self._outcome_shrine_pray),
                ("Desecrate altar", self._outcome_shrine_desecrate),
                ("Continue on your way", self._outcome_ignore)
            ],
            {"min_level": 1}
        ))
        
        events.append(RandomEvent(
            "Lost Adventurer",
            "You encounter a confused adventurer studying their map...",
            EventType.NEUTRAL,
            [
                ("Offer to help", self._outcome_help_adventurer),
                ("Ask for information", self._outcome_ask_adventurer),
                ("Continue on your way", self._outcome_ignore)
            ],
            {"min_level": 1}
        ))
        
        events.append(RandomEvent(
            "Weather-worn Statue",
            "An old statue weathered by time and the elements, you see some writing at the base...",
            EventType.NEUTRAL,
            [
                ("Clean the statue, this will take some effort! (Uses 20% stamina)", self._outcome_statue_clean),
                ("Read inscription", self._outcome_statue_read),
                ("Search the area", self._outcome_statue_search),
                ("Carry on your way", self._outcome_ignore)
            ],
            {"min_level": 1}
        ))
        
        events.append(RandomEvent(
            "Echo Chamber",
            "You enter a strange space where even your smallest sounds carry strangely. The acoustics seem almost magical...",
            EventType.NEUTRAL,
            [
                ("Call out!", self._outcome_echo_call),
                ("Listen carefully", self._outcome_echo_listen),
                ("Throw a stone", self._outcome_echo_stone),
                ("Pass by quietly", self._outcome_echo_quiet)
            ],
            {"location_type": ["Cave", "Temple", "Ruins", "Ancient Ruins", "Death Caves"]}
        ))
        
        events.append(RandomEvent(
            "Abandoned Caravan",
            "You discover a merchant's caravan, seemingly abandoned in haste...",
            EventType.NEUTRAL,
            [
                ("Search thoroughly (Takes time, 25% stamina)", self._outcome_caravan_search),
                ("Quickly grab what you can see", self._outcome_caravan_quick),
                ("Look for survivors", self._outcome_caravan_survivors),
                ("Leave it be", self._outcome_ignore)
            ],
            {
                "min_level": 5,
                "location_type": ["Desert", "Plains", "Mountain", "Valley", "Death Valley", "Shadowed Valley", "Scorching Plains"]
            }
        ))
        
        events.append(RandomEvent(
            "Ancient Ritual Site",
            "You stumble upon a circle of standing stones humming with residual magic...",
            EventType.NEUTRAL,
            [
                ("Attempt to channel the energy", self._outcome_ritual_channel),
                ("Study the runes (Takes time, costs 33% stamina)", self._outcome_ritual_study),
                ("Perform a cleansing ritual (Costs 25 gold)", self._outcome_ritual_cleanse),
                ("Leave the site undisturbed", self._outcome_ignore)
            ],
            {
                "min level": 8,
                "location_type": ["Ruins", "Temple", "Ancient Ruins", "Death Caves", "Heavens"]
            }
        ))
        
        events.append(RandomEvent(
            "Mysterious Campfire",
            "You spot a recently abandoned campfire with strange coloured flames...",
            EventType.NEUTRAL,
            [
                ("Rest by the fire", self._outcome_campfire_rest),
                ("Study the unusual flames (Uses 25% stamina)", self._outcome_campfire_study),
                ("Add fuel to the fire", self._outcome_campfire_fuel),
                ("Continue your journey...", self._outcome_ignore)
            ],
            {
                "min_level": 4,
                "location_type": ["Forest", "Deepwoods", "Mountain", "Cave", "Ruins", "Ancient Ruins", "Mountain Peaks", "Death Caves", "Dragons Lair"]
            }
        ))
        
        events.append(RandomEvent(
            "Soul Collector",
            "A ghostly figure emerges from the shadows, surrounded by writhing souls. It gestures to your collection of defeated foes, offering power in exchange for their essence...",
            EventType.NEUTRAL,
            [
                ("Trade monster souls", self._outcome_soul_trade),
                ("Sacrifice boss souls", self._outcome_soul_boss),
                ("Offer your own essence", self._outcome_soul_sacrifice),
                ("Reject the offer", self._outcome_soul_reject)
            ],
            {
                "min_level": 8,
                "location_type": ["Cave", "Death Valley", "Death Caves", "Temple", "Ancient Ruins", "Shadowed Valley"]
            }
        ))"""
        
        events.append(RandomEvent(
                "Soul Forge",
                "You discover an ancient forge burning with ethereal flames. The souls of your defeated enemies seem drawn to its power...",
                EventType.NEUTRAL,
                [
                    ("Forge equipment", self._outcome_forge_equipment),
                    ("Create soul crystal", self._outcome_forge_crystal),
                    ("Enhance abilities", self._outcome_forge_enhance),
                    ("Challenge the forge", self._outcome_forge_challenge)
                ],
                {
                    "min_level": 1,
                }
            ))
       
        # Dangerous events
        
        """events.append(RandomEvent(
            "Unstable Ground",
            "The ground beneath your feet feels unnaturally soft...",
            EventType.DANGEROUS,
            [
                ("Carefully backtrack", self._outcome_unstable_careful),
                ("Quickly run across", self._outcome_unstable_quick),
                ("Slowly pick your way across", self._outcome_unstable_slow),
                ("Try to find another path", self._outcome_unstable_avoid)
            ],
            {"location_type": ["Swamp", "Cave", "Mountain", "Desert", "Toxic Swamp", "Mountain Peaks", "Death Caves", "Death Valley", "Volcanic Valley"]}
        ))
        
        events.append(RandomEvent(
            "Stange Mushrooms",
            "You spot some strange looking mushrooms, they give of a faint aura...",
            EventType.DANGEROUS,
            [
                ("Pick the mushrooms", self._outcome_mushroom_pick),
                ("Cautiously harvest", self._outcome_mushroom_harvest),
                ("Have a snack, mushrooms are delicious!", self._outcome_mushroom_eat),
                ("Something seems off, leave them alone", self._outcome_ignore)
            ],
            {"location_type": ["Forest", "Swamp", "Cave", "Deepwoods", "Toxic Swamp", "Valley", "Ruins", "Death Caves", "Death Valley", "Ancient Ruins"]}
        ))
        
        events.append(RandomEvent(
            "Cursed Shrine",
            "You come across a dark altar radiating malevolent power. Ancient runes pulse with an ominous blood red glow...",
            EventType.DANGEROUS,
            [
                ("Make a blood sacrifice...", self._outcome_shrine_blood),
                ("Offer gold (Unknown amount!)", self._outcome_shrine_gold),
                ("Attempt to destroy the shrine...", self._outcome_shrine_destroy),
                ("Leave it alone and attempt to leave...", self._outcome_shrine_ignore)
            ],
            {
                "min_level": 5,
                #"location_type": ["Cave", "Ruins", "Temple", "Deepwoods", "Ancient Ruins", "Death Caves", "Volcanic Valley", "Shadowed Valley", "Mountain", "Mountain Peaks"]
            }
        ))
        
        events.append(RandomEvent(
            "Unstable Crystal",
            "A large crystal pulses with chaotic energy. The air around it crackles and warps...",
            EventType.DANGEROUS,
            [
                ("Try to harness it's power", self._outcome_crystal_harness),
                ("Carefully extract it", self._outcome_crystal_extract),
                ("Shatter it", self._outcome_crystal_shatter),
                ("Back away", self._outcome_crystal_retreat)
            ],
            {
                "min_level": 8,
                "location_type": ["Cave", "Ruins", "Ancient Ruins", "Temple", "Mountain", "Mountain Peaks", "Death Caves", "Dragons Lair"]
            }
        ))
        
        events.append(RandomEvent(
            "Void Tear",
            "A tear in reality floats before you, whispering promises of power. The air around it warps and twists unnaturally...",
            EventType.DANGEROUS,
            [
                ("Sacrifice essence to the void", self._outcome_void_sacrifice),
                ("Reach through the tear", self._outcome_void_reach),
                ("Try to seal the tear", self._outcome_void_seal),
                ("Back away carefully", self._outcome_void_retreat)
            ],
            {
                "min_level": 12,
                "location_type": ["Heavens", "Death Valley", "Temple", "Ancient Ruins", "Death Caves", "Shadowed Valley", "Cave"]
            }
        ))
        
        events.append(RandomEvent(
        "Storm Nexus",
        "Lightning converges into a swirling vortex of pure energy. Each bolt that strikes the ground leaves crystallized power in its wake...",
        EventType.DANGEROUS,
        [
            ("Channel the storm", self._outcome_storm_channel),
            ("Collect storm crystals", self._outcome_storm_collect),
            ("Embrace the lightning", self._outcome_storm_embrace),
            ("Seek shelter", self._outcome_storm_shelter)
        ],
        {
            "min_level": 10,
            "location_type": ["Mountain Peaks", "Heavens", "Mountain", "Temple", "Dragons Lair"]
        }
    ))"""
        
        return events

    def trigger_random_event(self, player, game):
        """Attempt to trigger an event"""
        # 15% chance for a random event
        if random.random() < 0.15:
            # Filter eligible events
            eligible_events = [
                event for event in self.events
                if event.can_occur(player, game.current_location)
            ]
            
            if eligible_events:
                event = random.choice(eligible_events)
                self._run_event(event, player, game)
                return True
        
        return False
    
    def _run_event(self, event, player, game):
        """Run a random event"""
        event_display = RandomEventDisplay(game.display)
        choice = event_display.show_event(event)
        
        if choice is not None:
            choice_text = event.choices[choice][0]
            
            # Create display wrapper
            def display_message(*args):
                message = ' '.join(str(arg) for arg in args)
                event_display.display_event_message(message)
                
            # Store and replace print
            import builtins
            original_print = builtins.print
            builtins.print = display_message
            
            # Handle choice
            event.handle_choice(choice, player, game)
            
            # Restore print
            builtins.print = original_print
        
        game.display.text_buffer.clear()
                
    # Event Outcomes
    # Beneficial
    
    # Hidden Cache Outcomes
    
    def _outcome_hidden_cache_careful(self, player, game):
        """Carefully investigate the hidden cache"""
        message = "Inside the cache you find"
        outcomes = [
            (0.4, lambda: (print(f"{message} a consumable!"), self._give_random_consumable(player, game, player.level))),
            (0.3, lambda: (print(f"{message} some gold"), self._give_gold(player, 20, 50))),
            (0.2, lambda: (print(f"{message} a piece of equipment!"), self._give_tier_equipment(player, game, player.level))),
            (0.1, lambda: print("Unfortunately, you find nothing of value."))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_hidden_cache_quick(self, player, game):
        """Quickly grab from the hidden cache"""
        message = "After making it to safety you look at what you found in the cache. It was"
        outcomes = [
            (0.3, lambda: (print(f"{message} a piece of equipment!"), self._give_tier_equipment(player, game, player.level))),
            (0.3, lambda: (print(f"{message} some gold!"), self._give_gold(player, 50, 100))),
            (0.4, lambda: self._take_damage(player, 5, 15, "You trigger a nasty trap! "))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    # Mysterious Traveler Outcomes
        
    def _outcome_traveller_accept(self, player, game):
        """Accept the travellers offer"""
        print("The traveller imparts his ancient wisdom upon you.")
        self._gain_exp(player, 10, 25)
        
    def _outcome_traveller_chat(self, player, game):
        """Have a chat with the traveller"""
        print("The traveller enjoys having a conversation with you. He generously gives you some gold as a gift!")
        self._give_gold(player, 10 * player.level, 20 * player.level)
    
    # Wandering Merchant Outcomes
        
    def _outcome_merchant_trade(self, player, game):
        """Trade gold for potentially valuable items"""
        trade_cost = player.gold // 2
        if trade_cost < 10:
            print("The merchant doesn't think you can afford their wares...Peasunt")
            return
        
        outcomes = [
            (0.4, lambda: (print("The merchant gives you some consumables!"), self._give_multiple_consumables_random(player, game, 2))),
            (0.3, lambda: (print("The merchant gives you a piece of equipment!"), self._give_tier_equipment(player, game, player.level))),
            (0.2, lambda: (print("The merchant doesn't have anything of value to give you, he returns your gold and then some as compensation!"), self._give_gold(player, trade_cost * 2, trade_cost * 3))),
            (0.1, lambda: self._give_special_item(player, game, "The merchant is impressed by your task and gives you a special item!"))
        ]
        
        player.gold -= trade_cost
        print(f"You spend {trade_cost} gold.")
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_merchant_barter(self, player, game):
        """Trade a random item for potentially better ones"""
        if not player.inventory:
            print("You have nothing to trade")
            return
        
        # Remove random item
        traded_item = random.choice(player.inventory)
        player.inventory.remove(traded_item)
        print(f"You trade your {traded_item.name}...")
        
        # Higher chance of good outcome if traded item was valuable
        if traded_item.value >= 100:
            outcomes = [
                (0.6, lambda: (print("The merchant gives you an item!"), self._give_tier_equipment(player, game, player.level * 2))),
                (0.4, lambda: (print("The merchant gives you some consumables!"), self._give_multiple_consumables_random(player, game, 3)))
            ]
        else:
            outcomes = [
                (0.4, lambda: (print("The merchant gives you a consumable!"), self._give_random_consumable(player, game, player.level))),
                (0.4, lambda: (print("The merchant gives you a piece of equipment!"), self._give_tier_equipment(player, game, player.level))),
                (0.2, lambda: (print("The merchant gives you some gold!"), self._give_gold(player, traded_item.value * 2, traded_item.value * 3)))
            ]
            
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_merchant_guard(self, player, game):
        """Help guard the merchant's caravan"""
        if player.stamina < (player.max_stamina * 0.8):
            print("You're too tired to help guard the caravan.")
            return
        else:
            self._drain_stamina(player, 1.0)
            gold_reward = random.randint(player.max_stamina * 2, player.max_stamina * 3)
            print("You spend time helping guard the merchant's caravan... This completely exhausts you!")
            message = "The merchant rewards you with"
            outcomes = [
                (0.4, lambda: (print(f"{message} some gold!"), self._give_gold(player, gold_reward, gold_reward))),
                (0.3, lambda: (print(f"{message} a number of consumables!"), self._give_multiple_consumables_random(player, game, random.randint(2, 5)))),
                (0.2, lambda: (print(f"{message} some gold and knowledge!"), self._gain_exp(player, 20, 40), self._give_gold(player, gold_reward // 2, gold_reward // 2))),
                (0.1, lambda: (print(f"{message} a special item!"), self._give_tier_equipment(player, game, random.randint(player.level + 1, player.level + 3))))
            ]
            self._resolve_weighted_outcome(outcomes, player)
    
    # Ancient Training Grounds Outcomes
        
    def _outcome_training_combat(self, player, game):
        """Practice combat at the ancient training grounds"""
        stamina_cost = player.max_stamina // 2
        if player.stamina < stamina_cost:
            print("You're too tired to study effectively")
            return
        else:
            self._drain_stamina(player, 0.5)
            for _ in range(2):
                self._give_random_buff_specific(player, 5, 10, 5, 15, ["attack", "accuracy", "crit_chance", "armour_penetration"])
            self._gain_exp(player, 15, 30, "You learn valuable offensive techniques!")
        
    def _outcome_training_study(self, player, game):
        """Study ancient combat techniques"""
        stamina_cost = player.max_stamina // 4
        if player.stamina < stamina_cost:
            print("You're too tired to study effectively")
            return
        else:
            self._drain_stamina(player, 0.25)
            for _ in range(2):
                self._give_random_buff_specific(player, 5, 10, 5, 15, ["defence", "evasion", "block_chance", "damage_reduction"])
            self._gain_exp(player, 15, 30, "You learn valuable defensive techniques!")
        
    def _outcome_training_search(self, player, game):
        """Search the training grounds for equipment"""
        if random.random() < 0.6:
            print("After searching around for a while you find a piece of equipment!")
            self._give_tier_equipment(player, game, player.level)
        else:
            print("After searching for a while you find a chest containing some consumables!")
            self._give_multiple_consumables_specific(player, game, random.randint(2, 3), "consumable", "buff")
            
    def _outcome_training_rest(self, player, game):
        """Rest at the training grounds"""
        print("You rest at the ancient training grounds.")
        self._restore_and_heal(player, 0.5)
    
    # Magical Spring Outcomes
        
    def _outcome_spring_drink(self, player, game):
        """Drink from the magical spring"""
        outcomes = [
            (0.3, lambda: self._full_heal_player(player)),
            (0.3, lambda: self._give_major_buff(player, 5, 10, 10, 15)),
            (0.2, lambda: self._permanent_stat_increase(player)),
            (0.2, lambda: self._temporary_max_increase(player))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_spring_meditate(self, player, game):
        """Meditate besides the spring"""
        # Restore resources
        self._restore_and_heal(player, 1.0)
        
        # Give exp bonus
        self._gain_exp(player, 25, 50, "Your meditation leaves you fully restored and enlightened!")
        
    def _outcome_spring_fill(self, player, game):
        """Fill containers with spring water"""
        # Give healing potions
        print("You manage to fill a number of containers with magical water!")
        self._give_multiple_consumables_specific(player, game, random.randint(2, 4), "consumable", ["healing", "hot"])
            
    def _outcome_spring_wade(self, player, game):
        """Wade in the magical spring"""
        # Remove all negative effects
        player.status_effects = [effect for effect in player.status_effects
                                 if not effect.is_debuff]
        
        # Give temporary bonus
        print("The magical water cleanses and empowers you!")
        self._give_major_buff(player, 10, 20, 5, 10)
        
    # Neutral Events
    
    # Ancient Shrine Outcomes
    
    def _outcome_shrine_offer(self, player, game):
        """Make an offering to the shrine"""
        if player.gold >= 10:
            player.gold -= 10
            outcomes = [
                (0.4, lambda: self._give_random_buff_percentile(player)),
                (0.3, lambda: self._heal_player(player, 0.3)),
                (0.2, lambda: self._restore_stamina(player, 0.3)),
                (0.1, lambda: self._give_gold(player, 20, 40))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        else:
            print("You don't have enough gold to make an offering...peasunt!")
            
    def _outcome_shrine_pray(self, player, game):
        """Pray at the shrine"""
        print("A golden beam shines down and revitalises you!")
        outcomes = [
            (0.4, lambda: self._heal_player(player, 0.15)),
            (0.4, lambda: self._restore_stamina(player, 0.15)),
            (0.2, lambda: self._restore_and_heal(player, 0.15))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_shrine_desecrate(self, player, game):
        """Desecrate the shrine"""
        outcomes = [
            (0.5, lambda: self._take_damage(player, 20, 30, "The god whose shrine this is smites you for your unholy act! ")),
            (0.3, lambda: self._give_gold(player, 50, 100, "You find some of the gold other adventurers have left and steal it!")),
            (0.1, lambda: (print("After destryoing the altar you find a piece of equipment hidden beneath it!"),self._give_tier_equipment(player, game, player.level))),
            (0.1, lambda: print("Nothing happens, but you do feel guilty."))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    # Lost Adventurer Outcomes
        
    def _outcome_help_adventurer(self, player, game):
        """Help the lost adventurer"""
        if random.random() < 0.7:
            print("The grateful adventurer shares some supplies with you!")
            self._give_random_consumable(player, game, player.level)
        else:
            self._gain_exp(player, 5, 15, "The adventurer shares some valuable knowledge!")
            
    def _outcome_ask_adventurer(self, player, game):
        """Ask the adventurer for information"""
        locations = game.world_map.get_all_locations()
        undiscovered = [loc for loc in locations if loc not in player.visited_locations]
        self._discover_location(player, game, 1)
        if undiscovered:
            print("The adventurer marks an interesting location on your map!")
    
    # Weather-Worn Statue Outcomes
    
    def _outcome_statue_clean(self, player, game):
        """Clean the old weathered statue"""
        stamina_cost = player.max_stamina // 5
        if player.stamina < stamina_cost:
            print("You don't have the energy for this!")
            return
        else:
            player.stamina -= stamina_cost
            outcomes = [
                (0.5, lambda: (print("The spirit of the statue thanks you with a buff!"), self._give_random_buff_percentile(player))),
                (0.3, lambda: self._give_gold(player, 30, 60, "While cleaning the status you notice some coins in the crook of its arm.")),
                (0.2, lambda: (print("While cleaning the statue you spot a piece of equipment!"), self._give_tier_equipment(player, game, player.level)))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_statue_read(self, player, game):
        """Read the inscription on the statue"""
        if random.random() < 0.7:
            self._gain_exp(player, 15, 30, "The inscription contains some words of wisdom.")
        else:
            self._gain_exp(player, 30, 60, "The inscription seems to draw you in, you feel like you hear the statue whispering to you!")
            
    def _outcome_statue_search(self, player, game):
        """Search the statue for loot"""
        outcomes = [
            (0.7, lambda: self._take_damage(player, 10, 20, "The spirit of the statue doesn't take kindly to you looting it! ")),
            (0.2, lambda: (print("You find a piece of equipment hidden behind the statue!"), self._give_tier_equipment(player, game, player.level))),
            (0.1, lambda: self._give_special_item(player, game, "The spirit of this statue approves of your gall! It provides an impressive piece of equipment!"))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    # Echo Chamber Outcomes
        
    def _outcome_echo_call(self, player, game):
        """Call out into the echo chamber"""
        outcomes = [
            (0.3, lambda: (print("Your voice reutrns with an empowering presence!"), self._give_random_buff_specific(player, 5, 10, 8, 12, ["attack", "defence", "accuracy"]))),
            (0.4, lambda: (print("After calling out you hear something clink to the ground and roll towards you!"), self._give_random_consumable(player, game, player.level))),
            (0.15, lambda: print("Your voice echoes away unanswered!")),
            (0.15, lambda: self._trigger_scaled_encounter(player, game, ["Echo Wraith"]))
        ]
        self._resolve_weighted_outcome(outcomes, player)
            
    def _outcome_echo_listen(self, player, game):
        """Listen carefully to the echoes"""
        if player.stamina < 20:
            print("You're too tired to focus on the echoes.")
            return
        else:
            player.stamina -= 20  # Cost to listen carefully
        
            outcomes = [
                (0.5, lambda: (print("You hear distant dangers and prepare accordingly!"), self._give_random_buff_specific(player, 5, 10, 8, 12, ["evasion", "defence", "block_chance"]))),
                (0.3, lambda: (print("You hear a soft thrumming coming from just inside the chamber!"),self._give_tier_equipment(player, game, player.level))),
                (0.1, lambda: self._gain_exp(player, 15, 25, "You hear some knowledgeable words come back to you!")),
                (0.1, lambda: (print("The confusing echoes disorient you! Accuracy -10 until end of next combat!"), player.apply_debuff("accuracy", 10)))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_echo_stone(self, player, game):
        """Throwing stones can be dangerous"""
        def mechanism():
            """Trigger a random mechanism effect"""
            if random.random() < 0.5:
                self._take_damage(player, 5, 15, "Your stone triggers a trap! ")
            else:
                heal_amount = player.max_hp // 4
                player.heal(heal_amount)
                print(f"Your stone triggers an ancient blessing! Restores {heal_amount} HP!")

        outcomes = [
            (0.6, lambda: (print("The echoes revel a safe path forward, you regain 25% stamina!"), self._restore_stamina(player, 0.25))),
            (0.2, lambda: (print("The stone knocks something off a hidden shelf! It falls to the ground and rolls towards you!"),self._give_random_consumable(player, game, player.level))),
            (0.1, lambda: mechanism()),
            (0.1, lambda: self._take_damage(player, 5, 15, "Your stone returns unexpectedly! "))
        ]
        self._resolve_weighted_outcome(outcomes, player)
            
    def _outcome_echo_quiet(self, player, game):
        """Sneak past the chamber like a mouse"""
        outcomes = [
            (0.6, lambda: print("You pass through safely and quietly.")),
            (0.3, lambda: self._give_gold(player, player.level * 2 + 10, player.level * 4 + 30)),
            (0.1, lambda: self._permanent_stat_increase_specific(player, 1, ["accuracy"]))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    # Abandoned Caravan Outcomes
    
    def _outcome_caravan_search(self, player, game):
        """Thoroughly search the abandoned caravan"""
        # Costs stamina for a thorough search
        stamina_cost = player.max_stamina // 4
        if player.stamina <= stamina_cost:
            print("You're too tired to conduct a thorough search")
            return
        else:
            player.stamina -= stamina_cost
            
            outcomes = [
                (0.3, lambda: (print("You find a hidden cache of some equipment! Underneath you notice some gold glinting, lucky you!"), self._give_tier_equipment(player, game, player.level), self._give_gold(player, player.level * 4 + 20, player.level * 8 + 35))),
                (0.3, lambda: (print("You find a hidden cache of consumables!"), self._give_multiple_consumables_random(player, game, 3))),
                (0.2, lambda: (print("You find a map detailing the location of another area!"), self._discover_location(player, game, 1))),
                (0.2, lambda: print("Despite your thorough search, you come up empty handed!"))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_caravan_quick(self, player, game):
        """Quickly grab visible items from the caravan"""
        outcomes = [
            (0.3, lambda: (print("You notice a small bag which you quickly grab and retreat with!"), print("After getting to safety you check the contents, it's a consumable item!"), self._give_random_consumable(player, game, player.level))),
            (0.3, lambda: (print("You notice a small bag which you quickly grab and retreat with!"), print("After getting to safety you check the contents, it's some gold!"),self._give_gold(player, player.level * 2 + 10, player.level * 4 + 20))),
            (0.4, lambda: self._take_damage(player, 5, 15, "You trigger a hidden trap! "))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_caravan_survivors(self, player, game):
        """Look for survivors around the caravan"""   
        outcomes = [
            (0.4, lambda: self._gain_exp(player, 20, 40, "You help a grateful survivor who shares valuable knowledge!")),
            (0.3, lambda: (print("You don't find anyone alive, but you find some gold and equipment!"), print("You don't feel great about taking from the dead, but they don't need it, you do!"), self._give_tier_equipment(player, game, player.level), self._give_gold(player, 20, 50))),
            (0.3, lambda: (print("You find clues as to what caused this."), print("It's a map indicating the area the monsters which did this came from!"), self._discover_location(player, game, 1)))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    # Ancient Ritual Site Outcomes
        
    def _outcome_ritual_channel(self, player, game):
        """Attempt to channel the ritual site's energy"""
        outcomes = [
            (0.3, lambda: (print("Ancient power surges through you!"), self._give_major_buff(player, 10, 15, 15, 25), self._heal_player(player, 0.25))),
            (0.3, lambda: self._give_temporary_weapon_enchant(player, 16, 24, 15, 30)),
            (0.2, lambda: (print("You feel drained from channeling the ritual but also gain knowledge about ancient rituals!"), self._drain_stamina(player, 0.5), self._gain_exp(player, 20, 35))),
            (0.2, lambda: (self._take_damage(player, 15, 25, "The ritual backfires! "), print("But you still manage to gain a temporary buff!"), self._give_random_buff_specific(player, 5, 8, 10, 20, ["attack", "defence", "accuracy"])))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    def _outcome_ritual_study(self, player, game):
        """Study the ritual sites runes"""
        stamina_cost = player.max_stamina // 3
        if player.stamina < stamina_cost:
            print("You're too tired to focuse on the complex runes.")
            return
        else:
            player.stamina -= stamina_cost
            
            outcomes = [
                (0.4, lambda: (self._gain_exp(player, 20, 40, "Ancient knowledge flows into your mind!"), self._permanent_stat_increase(player))),
                (0.3, lambda: (print("You decipher the magical crafting patterns!"), self._give_multiple_consumables_random(player, game, random.randint(2, 4)), self._gain_exp(player, 20, 30, "The knowledge grants you experience!"))),
                (0.3, lambda: (self._give_gold(player, 50, 100, "You discover a hidden cache of coins!"), print("You also gain a temporary buff due to the runes!"), self._give_random_buff_specific(player, 8, 12, 10, 15, ["attack", "defence", "accuracy"])))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_ritual_cleanse(self, player, game):
        """Attempt to cleanse the ritual"""
        outcomes = [
            (0.4, lambda: (print("By cleansing the ritual you feel restored and protected!"),
                            self._full_heal_player(player),
                            self._give_random_buff_specific(player, 10, 10, 10, 15, ["defence"]),
                            self._give_random_buff_specific(player, 10, 10, 10, 15, ["damage_reduction"]))),
            (0.3, lambda: (print("You partially cleanse the ritual and feel somewhat restored and protected!"),
                           self._restore_and_heal(player, 0.25),
                           self._give_random_buff_specific(player, 5, 8, 5, 10, ["defence", "damage_reduction", "block_chance"]))),
            (0.3, lambda: (print("You fail to cleanse the ritual but gain insights!"), self._gain_exp(player, 10, 20, "You feel knowledgable from your failure...paradoxically!"), self._restore_stamina(player, 0.5)))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    # Mysterious Campfire Outcomes
    
    def _outcome_campfire_rest(self, player, game):
        def strange_effect():
            # Provides a random effect 
            if random.random() < 0.3:
                """Temporary transformation boosting all stats"""
                print("The flames temporarily transform you into a stronger being!")
                self._give_major_buff(player, 8, 12, 10, 10)
            elif random.random() < 0.6:
                """Elemental energy surge boosting weapons strength"""
                print("Elemental energy surges through your weapon empowering it!")
                self._give_temporary_weapon_enchant(player, 5, 10, 15, 25)
            else:
                """Transport to another dimension temporarily"""
                print("You find yourself in a different place after watching the flames flicker!")
                print("You see some gold and equipment laying on the ground!!")
                self._give_gold(player, player.level * 2 + 20, player.level * 4 + 40)
                self._give_tier_equipment(player, game, player.level)
            
        outcomes = [
            (0.4, lambda: (print("The mystical flames provide a deep, restorative rest."), self._restore_and_heal(player, 0.6), print("You feel protected by the flames!"), self._give_random_buff_specific(player, 5, 8, 8, 12, ["defence", "evasion"]))),
            (0.3, lambda: (print("You dream of ancient battles and mystical techniques! You gain some knowledge and feel strengthened!"), self._gain_exp(player, 20, 30), self._give_random_buff_specific(player, 6, 9, 8, 15, ["attack", "accuracy", "crit_chance"]))),
            (0.3, lambda: (print("As you stare at the flames you feel something strange building up..."), strange_effect()))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    def _outcome_campfire_study(self, player, game):
        """Study the unusual flames"""
        # Check to see if the player has enough stamina
        stamina_cost = player.max_stamina // 4
        if player.stamina < stamina_cost:
            print("You're too tired to focus on the mystical flames.")
            return
        else:
            self._drain_stamina(player, 0.25)
            outcomes = [
                (0.3, lambda: (print("You learn some magical knowledge from studying the flames!"), self._gain_exp(player, 30, 40), self._permanent_stat_increase(player))),
                (0.3, lambda: (print("From studying the flames you feel rejuvenated and temporarily tougher!"), self._heal_player(player, 0.25), self._give_multiple_random_buffs(player, 8, 15, 8, 15, 2, ["defence", "damage_reduction", "block_chance", "evasion"]))),
                (0.4, lambda: (print("You get mesmerised by studying the flames! You feel drained but benefit from what you saw!"), self._drain_stamina(player, 0.33), self._gain_exp(player, 25, 40)))
            ]
            self._resolve_weighted_outcome(outcomes, player)
    
    def _outcome_campfire_fuel(self, player, game):
        """Feed the flames there chosen fuel...Gold!"""
        # Check if the player has enough gold for offering
        def summon_spirit():
            # Summons a friendly spirit who provides boons
            outcomes = [
                (0.25, lambda: (print("You summon a warrior spirit who trains you in ancient techniques!"), self._give_multiple_random_buffs(player, 8, 12, 10, 20, 2, ["attack", "accuracy", "armour_penetration", "crit_chance", "crit_damage"]))),
                (0.25, lambda: (print("You summon a guardian spirit who defends you temporarily!"), self._give_multiple_random_buffs(player, 8, 12, 10, 15, 2, ["defence", "evasion", "block_chance", "damage_reduction"]))),
                (0.25, lambda: (print("You summon a generous spirit who gives you some gold and items!"), self._give_gold(player, 50, 100), self._give_tier_equipment(player, game, player.level))),
                (0.25, lambda: (print("You summon a wise spirit who grants you untold knowledge!"), self._gain_exp(player, 50, 100)))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
        def wild_magic():
            # The mystical flames go wild spewing forth magic!
            def chaos():
                outcomes = [
                    # Positive chaos
                    (0.2, lambda: (print("The flames cauterise your wounds!"), self._take_damage(player, 5, 5, "Healing can sometimes be painful..."), self._heal_player(player, 0.5))),
                    (0.2, lambda: (print("Gold starts falling all around...it's molten!"), self._take_damage(player, 5, 7, "Some gold lands on you, burning your flesh! "), self._give_gold(player, 100, 150))),
                    # Mixed chaos
                    (0.2, lambda: (print("The flames empower you!"), self._give_multiple_random_buffs(player, 5, 10, 5, 10, random.randint(1, 3), ["attack", "accuracy", "armour_penetration"]))),
                    (0.2, lambda: (print("The flames devour you! Att and Def -10 until end of next combat!"), player.apply_debuff("defence", 10), player.apply_debuff("attack", 10), self._take_damage(player, 10, 20, "The flames eat away at your body and soul! "))),
                    # Negative chaos
                    (0.2, lambda: (print("The flames start scorching you severely!"), self._take_damage(player, 30, 50, "You're severely burned by the flames! "), self._drain_stamina(player, 0.33))),
                    (0.2, lambda: (print("The flames drain something from you!"), self._permanent_stat_decrease(player), self._drain_stamina(player, 0.25)))
                ]
                self._resolve_weighted_outcome(outcomes, player)
            outcomes = [
                (0.4, lambda: (print("The magic surges around you both healing and damaging you, but making you stronger in the process...temporarily!"), self._heal_player(player, 0.33), self._take_damage(player, 15, 20), self._give_major_buff(player, 8, 12, 10, 15))),
                (0.3, lambda: (print("The wild magic temporarily enhances you in multiple ways!"), self._give_multiple_random_buffs(player, 8, 12, 8, 12, random.randint(2, 4), ["attack", "defence", "evasion", "accuracy", "damage_reduction", "armour_penetration", "crit_chance", "crit_damage", "block_chance"]))),
                (0.3, lambda: (print("The flames go absolutely chaotic! You try to back away but it's too late!"), chaos()))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        if player.gold < 15:
            print("You have nothing worthy to offer the flames!")
            return
        else:
            player.gold -= 15
            outcomes = [
                (0.3, lambda: (print("The flames grow stronger! Their magic flows into you!"), self._restore_and_heal(player, 0.33), self._give_major_buff(player, 12, 15, 10, 15))),
                (0.3, lambda: (print("You summon a spirit who helps you!"), summon_spirit())),
                (0.4, lambda: (print("The flames react unexpectedly to your offering! The magic goes wild!"), wild_magic()))
            ]
            self._resolve_weighted_outcome(outcomes, player)
    
    # Soul Collector Outcomes and Helper methods
    
    def use_boss_souls(self, player, total_souls):
        """Helper function to handle boss soul trading"""
        if not hasattr(player, 'boss_kill_tracker'):
            return total_souls, False
                
        boss_souls = sum(player.boss_kill_tracker.values()) * 10
        if boss_souls <= 0:
            return total_souls, False
                
        while True:
            choice = input(f"\nWould you like to use your {boss_souls} boss souls? (y/n): ").lower()
            if choice == "y":
                print("You foolishly use your boss souls on these minor rewards...Muahahahahhaha!")
                return total_souls + boss_souls, True
            elif choice == "n":
                return total_souls, False
            else:
                print("Invalid choice! Please enter 'y' for yes or 'n' for no.")
                
            while True:
                choice = input(f"\nWould you like to use your {boss_souls} boss souls? (y/n): ").lower()
                if choice == "y":
                    print("You foolishly use your boss souls on these minor rewards...Muahahahahhaha!")
                    player.used_boss_kill_tracker = player.boss_kill_tracker.copy()
                    player.boss_kill_tracker.clear()
                    return total_souls + boss_souls
                elif choice == "n":
                    return total_souls
                else:
                    print("Invalid choice! Please enter 'y' for yes or 'n' for no.")
    
    def _outcome_soul_trade(self, player, game):
        """Trade accumulated monster souls for power"""
        event_display = ComplexEventDisplay(game.display)
        
        if not player.kill_tracker and not player.variant_kill_tracker and not player.boss_kill_tracker:
            event_display.display_text("You have no souls to trade... The collector seems disappointed.")
            return
        
        # Display available souls
        self._display_available_souls(player)
        
        # Calculate total souls
        total_souls = sum(player.kill_tracker.values()) + (sum(player.variant_kill_tracker.values()) * 5) + (sum(player.boss_kill_tracker.values()) * 10)
        
        # Trade options with complex display
        trade_choices = [
            "Convert souls to permanent stat increase (500 souls max)",
            "Transform souls into equipment (500 souls max)",
            "Exchange souls for consumable items (250 souls max)",
            "Return souls for gold and experience"
        ]
        
        choice = event_display.show_choice(
            "Soul Collector Trades",
            trade_choices,
            f"Total Souls: {total_souls}\nChoose your trade wisely..."
        )
        
        if choice is None:
            return
        
        # Determine reward scaling based on total souls
        reward_scale = min(1, max(1, total_souls // 100))
        
        # Process trade based on selected choice
        trade_methods = [
            self._trade_souls_for_stat_increase,
            self._trade_souls_for_equipment,
            self._trade_souls_for_consumables,
            self._trade_souls_for_gold_and_exp
        ]
        
        trade_methods[choice](player, game, total_souls, reward_scale, game.display)

    def _trade_souls_for_stat_increase(self, player, game, total_souls, reward_scale, game_display):
        """Trade souls for permanent stat increase"""
        event_display = ComplexEventDisplay(game_display)
        if total_souls < 100:
            event_display.show_outcome("The collector scoffs at your meagre offering...")
            return
        
        selected_souls = self._select_souls(player, total_souls, game_display, 'stats', game)
    
        if not selected_souls:
            return
        
        # Calculate actual souls used
        used_souls = selected_souls['total_value']
        
        if used_souls < 100:
            event_display.show_outcome("You need at least 100 souls for a permanent enhancement.")
            return
        
        stat_choices = ["attack", "crit_chance", "crit_damage", "defence", "accuracy", "evasion", "max_hp"]
        
        stat_choice = event_display.show_choice(
            "Soul Enhancement", 
            [stat.replace('_', ' ').title() for stat in stat_choices],
            f"Select a stat to enhance.\nSouls Used: {used_souls}"
        )
        
        if stat_choice is not None:
            chosen_stat = stat_choices[stat_choice]
            
            # Calculate increase amount based on actual souls used
            increase_amount = min(5, max(1, used_souls // 100))
            
            self._consume_selected_souls(player, selected_souls)
            self._permanent_stat_increase_specific(player, increase_amount, [chosen_stat])
            event_display.show_outcome(f"{chosen_stat.replace('_', ' ').title()} permanently increased by {increase_amount}!")
                
    def _trade_souls_for_equipment(self, player, game, total_souls, reward_scale, game_display):
        """Trade souls for equipment"""
        event_display = ComplexEventDisplay(game_display)
        if total_souls < 75:
            event_display.show_outcome("The collector scoffs at your meagre offering...")
            return
        
        selected_souls = self._select_souls(player, total_souls, game_display, 'equipment', game)
    
        if not selected_souls:
            return
        
        used_souls = selected_souls['total_value']
        
        if used_souls < 75:
            event_display.show_outcome("You need at least 75 souls to forge equipment.")
            return
        
        # Determine equipment tier based on actual souls used
        equipment_tiers = [
            (500, "legendary"),
            (300, "masterwork"),
            (200, "epic"),
            (75, "rare")
        ]
        
        selected_tier = next(
            tier for souls_threshold, tier in equipment_tiers 
            if used_souls >= souls_threshold
        )
        
        self._consume_selected_souls(player, selected_souls)
        
        # Get equipment of appropriate tier
        equipment = [
            item for item in game.items.values()
            if item.type in ["weapon", "helm", "chest", "legs", "boots", "gloves", "shield", "ring"]
            and item.tier == selected_tier
        ]
        
        if equipment:
            item = random.choice(equipment)
            player.add_item(item)
            event_display.show_outcome(f"Souls forged into a {item.name} ({item.tier.title()})!")
                
    def _trade_souls_for_consumables(self, player, game, total_souls, reward_scale, game_display):
        """Trade souls for consumable items"""
        event_display = ComplexEventDisplay(game_display)
        if total_souls < 50:
            event_display.show_outcome("The collector scoffs at your meagre offering...")
            return
        
        selected_souls = self._select_souls(player, total_souls, game_display, 'consumables', game)
    
        if not selected_souls:
            return
        
        used_souls = selected_souls['total_value']
        
        if used_souls < 50:
            event_display.show_outcome("You need at least 50 souls to create consumables.")
            return
        
        # Determine number of items based on actual souls used
        num_items = min(5, max(1, used_souls // 50))
        
        self._consume_selected_souls(player, selected_souls)
        
        event_display.show_outcome(f"Creating {num_items} consumable items...")
        
        for _ in range(num_items):
            self._give_random_consumable(player, game, player.level + (used_souls // 100))
                
    def _trade_souls_for_gold_and_exp(self, player, game, total_souls, reward_scale, game_display):
        """Trade souls for gold and experience"""
        event_display = ComplexEventDisplay(game_display)
        selected_souls = self._select_souls(player, total_souls, game_display, 'gold_exp', game)
    
        if not selected_souls:
            return
        
        used_souls = selected_souls['total_value']
        
        self._consume_selected_souls(player, selected_souls)
        
        # Calculate rewards based on actual souls used
        gold_reward = used_souls * 10
        exp_reward = used_souls * 5
        
        player.gold += gold_reward
        player.gain_exp(exp_reward, player.level)
        
        event_display.show_outcome(f"Received {gold_reward} gold and {exp_reward} experience!")
            
    def _outcome_soul_boss(self, player, game):
        """Sacrifice specifically boss souls for greater rewards, up to 50 souls"""
        event_display = ComplexEventDisplay(game.display)
        
        if not player.boss_kill_tracker:
            event_display.show_outcome("You haven't defeated any worthy bosses yet...")
            return
            
        # Calculate total available boss souls
        total_boss_souls = sum(player.boss_kill_tracker.values())
        if total_boss_souls == 0:
            event_display.show_outcome("No boss souls available!")
            return
            
        # Use select_souls with boss-specific parameters
        selected_souls = self._select_souls(player, 50, game.display, 'boss', game)
        
        if not selected_souls or selected_souls["total_value"] == 0:
            return
            
        # Get actual boss kills used
        boss_kills = sum(selected_souls["boss"].values())
        
        # Consume the selected souls
        self._consume_selected_souls(player, selected_souls)
        
        event_display.show_outcome(f"Using {boss_kills} boss souls...")
        
        def give_special_items():
            num_items = min(4, max(1, boss_kills // 10))
            for _ in range(num_items):
                self._give_special_item(player, game)
            
            if boss_kills >= 30:
                self._permanent_stat_increase_specific(player, boss_kills / 15, ["attack", "accuracy", "crit_chance", "crit_damage"])
                self._permanent_stat_increase_specific(player, boss_kills / 15, ["defence", "evasion", "damage_reduction"])
                #self._gain_exp(player, boss_kills * 20, boss_kills * 30, "The Soul Collector grants you an immense amount of experience for your boss souls!")
                self._give_gold(player, boss_kills * 20, boss_kills * 30, "He also showers you in Gold!")
                self._take_damage(player, 10, 20, "It turns out that much Gold isn't good for your health when it all pours on you at once! ")
        
        outcomes = [
            (0.3, lambda: (
                print("The boss souls grant you immense power!"),
                self._permanent_stat_increase_specific(player, boss_kills, 
                    ["attack", "defence", "accuracy", "evasion"]),
                self._give_major_buff(player, 10, 15, 15 + boss_kills, 25 + boss_kills)
            )),
            (10.3, lambda: (
                print("The boss souls transform into legendary equipment!"),
                give_special_items()
            )),
            (0.2, lambda: (
                print("The boss souls imbue you with their knowledge!"),
                self._gain_exp(player, 100 * boss_kills, 150 * boss_kills),
                self._give_gold(player, 200 * boss_kills, 300 * boss_kills)
            )),
            (0.2, lambda: (
                print("The souls overwhelm you with their power!"),
                self._take_damage(player, 30, 50, "The souls tear at your essence! "),
                self._permanent_stat_increase_specific(player, boss_kills,
                    ["attack", "accuracy", "crit_chance", "crit_damage", "armour_penetration"]),
                self._permanent_stat_increase_specific(player, boss_kills, ["defence", "evasion", "damage_reduction", "block_chance"]),
                self._give_major_buff(player, 15, 20, 30, 40)
            ))
        ]
        
        self._resolve_weighted_outcome(outcomes, player)

    def _outcome_soul_sacrifice(self, player, game):
        """Offer your own essence for power"""
        print("The collector eyes you hungrily...")
        return self._trade_hp_for_reward(player, game, min_percent=20, max_percent=50)

    def _outcome_soul_reject(self, player, game):
        """Attempt to reject the soul collector's offer"""
        if random.random() < 0.7:  # 70% chance to leave safely
            print("The collector fades away, disappointed but accepting.")
            return
        else:
            print("The collector doesn't take kindly to rejection!")
            if random.random() < 0.5:
                self._take_damage(player, 20, 30, "Soul energy tears at your essence! ")
            else:
                print("The collector attacks!")
                enemy = create_enemy("Void Walker", player)  # Use void walker as collector's servant
                if enemy:
                    game.battle.battle(enemy)
    
    # Soul Forge Outcomes and Helper Methods
    
    def _outcome_forge_equipment(self, player, game):
        """Forge new equipment using accumulated souls"""
        event_display = ComplexEventDisplay(game.display)
        
        if not player.kill_tracker and not player.variant_kill_tracker and not player.boss_kill_tracker:
            event_display.display_text("You have no souls to trade... The collector seems disappointed.")
            return
        
        # Calculate total souls
        total_souls = sum(player.kill_tracker.values()) + (sum(player.variant_kill_tracker.values()) * 5) + (sum(player.boss_kill_tracker.values()) * 10)
        
        forge_options = [
            (100, "Basic Forge (100 souls) - Regular equipment piece", "basic"),
            (300, "Greater Forge (300 souls) - Enhanced equipment piece", "greater_forge"),
            (500, "Soul-Bound Forge (500 souls) - Equipment that grows with you", "soulbound")
        ]
        
        available_choices = [option[1] for option in forge_options if option[0] <= total_souls]
        
        if not available_choices:
            event_display.show_outcome("You don't have enough souls for any forging!")
            return
            
        available_choices.append("Cancel")
        
        choice = event_display.show_choice(
            "Soul Forge",
            available_choices,
            f"Total Souls: {total_souls}\nChoose your forge wisely..."
        )
        
        if choice is None or choice == len(available_choices) - 1:
            return
            
        required_souls = forge_options[choice][0]
        forge_type = forge_options[choice][2]
        
        selected_souls = self._select_souls(player, required_souls, game.display, forge_type, game)
        
        if not selected_souls:
            return
        
        self._forge_equipment_with_souls(player, game, forge_type, selected_souls)
        self.display.pause()

    def _outcome_forge_crystal(self, player, game):
        """Create a soul crystal to store power"""
        event_display = ComplexEventDisplay(game.display)
        
        # Calculate total available souls
        total_souls = self._calculate_total_souls(player)
        
        # Crystal options with requirements
        crystal_options = [
            (50, "Lesser Crystal (50 each) - Small buff storage", "lesser"),
            (150, "Greater Crystal (150 each) - Medium buff storage", "greater"),
            (250, "Perfect Crystal (250 each) - Large buff storage", "perfect")
        ]
        
        # Filter available options based on souls
        available_choices = [option[1] for option in crystal_options if option[0] <= total_souls]
        
        if not available_choices:
            event_display.show_outcome("You don't have enough souls to forge any crystals!")
            return
            
        available_choices.append("Cancel")
        
        # Display available choices
        choice = event_display.show_choice(
            "Soul Crystal Creation",
            available_choices,
            f"Total Souls: {total_souls}\nChoose your crystal wisely..."
        )
        
        # Cancel if no choice or cancel selected
        if choice is None or choice == len(available_choices) - 1:
            return
        
        # Get selected crystal requirements
        required_souls = crystal_options[choice][0]
        crystal_type = crystal_options[choice][2]
        
        selected_souls = self._select_souls(player, required_souls, game.display, crystal_type, game)
        
        if not selected_souls:
            return
        
        crystal = self._create_soul_crystal(player, game, crystal_type, selected_souls)
        event_display.show_crystal_description(crystal)

    def _outcome_forge_enhance(self, player, game):
        """Use the forge to enhance abilities"""
        event_display = ComplexEventDisplay(game.display)
        
        total_souls = self._calculate_total_souls(player)
        
        enhance_options = [
            (25, "Combat Training (25 souls) - Combat stat bonuses", "combat"),
            (75, "Soul Attunement (75 souls) - Permanent improvements", "attunement"),
            (150, "Spirit Bond (150 souls) - Major enhancements", "spirit")
        ]
        
        available_choices = [option[1] for option in enhance_options if option[0] <= total_souls]
        
        if not available_choices:
            event_display.show_outcome("You don't have enough souls for any enhancements!")
            return
            
        available_choices.append("Cancel")
        
        choice = event_display.show_choice(
            "Soul Enhancement",
            available_choices,
            f"Total Souls: {total_souls}\nChoose your enhancement wisely..."
        )
        
        if choice is None or choice == len(available_choices) - 1:
            return
        
        required_souls = enhance_options[choice][0]
        enhance_type = enhance_options[choice][2]
        
        selected_souls = self._select_souls(player, required_souls, game.display, enhance_type, game)
        
        if not selected_souls:
            return
        
        self._enhance_with_souls(player, game, enhance_type, selected_souls)
        self.display.pause()

    def _outcome_forge_challenge(self, player, game):
        """Challenge the forge's guardian for greater rewards"""
        event_display = ComplexEventDisplay(game.display)
        self.display = Display()
        
        if player.stamina < (player.max_stamina * 0.5):
            event_display.show_outcome("You're too exhausted to face this challenge!")
            return
            
        choice = event_display.show_choice(
            "Soul Forgemaster Challenge",
            ["Accept the challenge", "Decline"],
            "A mighty presence materializes from the forge...\n"
            "The Soul Forgemaster appears, offering to test your worth!"
        )
        
        if choice is None or choice == 1:
            return
            
        event_display.show_outcome(
            "The forge erupts with ethereal flames as the Forgemaster readies for battle!",
            2000
        )
        
        # Create and fight the Soul Forgemaster
        enemy = create_enemy("Soul Forgemaster", player)
        if enemy:
            if game.battle is None:
                game.initialise_battle()
            game.battle.battle(enemy)
            
            # Clear battle log and show outcome after battle
            game.display.text_buffer.clear()
            
            if not enemy.is_alive():
                event_display.show_outcome("The forge acknowledges your victory!", 2000)
                
                pygame.time.wait(2000)
                
                outcomes = [
                    (0.3, lambda: self._forge_victory_power(player, game, event_display)),
                    (0.3, lambda: self._forge_victory_essence(player, game, event_display)),
                    (0.2, lambda: self._forge_victory_mastery(player, game, event_display)),
                    (10.2, lambda: self._forge_victory_secrets(player, game, event_display))
                ]
                
                self._resolve_weighted_outcome(outcomes, player)
            else:
                event_display.show_outcome(
                    "The Soul Forgemaster was too powerful..."
                    "Perhaps you should return when you're stronger.",
                    2000
                )

    def _forge_victory_power(self, player, game, event_display):
        """Handle power victory outcome"""
        event_display.show_outcome("You receive a mighty reward!", 2000)
        event_display.show_progress(
            "Forge Power",
            1, 3,
            "The forge's power flows into you..."
        )
        self._give_special_item(player, game)
        
        event_display.show_progress(
            "Forge Power",
            2, 3,
            "Ancient techniques manifest in your mind..."
        )
        self._permanent_stat_increase_specific(player, 3, 
            ["attack", "defence", "accuracy", "crit_chance"])
        
        event_display.show_progress(
            "Forge Power",
            3, 3,
            "Victory complete!"
        )
        self.display.pause()

    def _forge_victory_essence(self, player, game, event_display):
        """Handle essence victory outcome"""
        event_display.show_progress(
            "Forge Essence",
            1, 3,
            "The forge's essence infuses your being..."
        )
        self._give_major_buff(player, 15, 20, 20, 25)
        
        event_display.show_progress(
            "Forge Essence",
            2, 3,
            "Crystallizing rewards..."
        )
        self._give_multiple_consumables_random(player, game, 4)
        
        event_display.show_progress(
            "Forge Essence",
            3, 3,
            "Victory complete!"
        )
        self.display.pause()
        
    def _forge_victory_mastery(self, player, game, event_display):
        """Handle mastery victory outcome"""
        event_display.show_progress(
            "Forge Mastery",
            1, 4,
            "You gain mastery over soul energy..."
        )
        self._restore_and_heal(player, 1.0)
        self._give_special_item(player, game)
        self.display.pause()
        
        event_display.show_progress(
            "Forge Mastery",
            2, 4,
            "The forge offers additional power..."
        )
        
        # Offer bonus forging attempt
        souls = self._select_souls(player, 300, game.display, "greater_forge", game)
        if souls:
            event_display.show_progress(
                "Forge Mastery",
                3, 4,
                "Forging with newfound mastery..."
            )
            self._forge_equipment_with_souls(player, game, "greater_forge", souls)
        else:
            event_display.show_outcome("Insufficient souls for bonus forging.")
        self.display.pause()
            
        event_display.show_progress(
            "Forge Mastery",
            4, 4,
            "Victory complete!"
        )
        self.display.pause()

    def _forge_victory_secrets(self, player, game, event_display):
        """Handle secrets victory outcome"""
        
        
        event_display.show_progress(
            "Forge Secrets",
            1, 4,
            "The forge reveals its ancient secrets..."
        )
        self._give_multiple_consumables_random(player, game, 4)
        self.display.pause()
        
        event_display.show_progress(
            "Forge Secrets",
            2, 4,
            "Creating soul crystal..."
        )
        
        available_souls = self._calculate_total_souls(player)
        if available_souls < 50:
            event_display.show_outcome("Insufficient souls for crystal creation.")
            return
        elif available_souls >= 50 and available_souls < 150:
            souls = self._select_souls(player, 50, game.display, "lesser", game)
            soul_crystal = "lesser"
        elif available_souls >= 150 and available_souls < 250:
            souls = self._select_souls(player, 150, game.display, "greater", game)
            soul_crystal = "greater"
        elif available_souls >= 250:
            souls = self._select_souls(player, 250, game.display, "perfect", game)
            soul_crystal = "perfect"
        if souls:
            event_display.show_progress(
                "Forge Secrets",
                3, 4,
                "Crystallizing ancient knowledge..."
            )
            crystal = self._create_soul_crystal(player, game, soul_crystal, souls)
            event_display.show_crystal_description(crystal)
        self.display.pause()
        
        event_display.show_progress(
            "Forge Secrets",
            4, 4,
            "Victory complete!"
        )
        self.display.pause()
            
    def _display_available_souls(self, player):
        """Display all available soul types and counts"""
        print("\nAvailable Souls:")
        
        # Standard souls
        if hasattr(player.kill_tracker, 'items'):
            print("\nStandard Monster Souls:")
            for enemy, count in sorted(player.kill_tracker.items()):
                monster_type = get_type_for_monster(enemy)
                type_str = f" ({monster_type.title()})" if monster_type != "unknown" else ""
                print(f"{count:3d}x {enemy}{type_str} (1 soul each)")
                
        # Variant souls
        if hasattr(player.variant_kill_tracker, 'items'):
            print("\nVariant Souls:")
            for variant, count in sorted(player.variant_kill_tracker.items()):
                print(f"{count:3d}x {variant} (5 souls each)")
                
        # Boss souls
        if hasattr(player.boss_kill_tracker, 'items'):
            print("\nBoss Souls:")
            for boss, count in sorted(player.boss_kill_tracker.items()):
                monster_type = get_type_for_monster(boss)
                type_str = f" ({monster_type.title()})" if monster_type != "unknown" else ""
                print(f"{count:3d}x {boss}{type_str} (10 souls each)")

    def _calculate_total_souls(self, player):
        """Calculate the total number of souls the player has"""
        total_souls = 0
        for count in player.kill_tracker.values():
            total_souls += count
        for count in player.variant_kill_tracker.values():
            total_souls += count * 5
        for count in player.boss_kill_tracker.values():
            total_souls += count * 10
        return total_souls
    
    def _select_souls(self, player, required_souls, game_display, trade_type, game):
        """Select souls for trading using VisualInput for quantity"""
        event_display = ComplexEventDisplay(game_display)
        visual_input = VisualInput(game_display)
        self.display = Display()
        
        max_souls_limits = {
            'stats': 500,
            'equipment': 500,
            'consumables': 250,
            'gold_exp': 500,
            'boss': 50,
            'basic': 100,
            'greater_forge': 300,
            'soulbound': 500,
            'lesser': 50,
            'greater': 150,
            'perfect': 250,
            'combat': 25,
            'attunement': 75,
            'spirit': 150
        }
        
        if trade_type not in max_souls_limits:
            event_display.show_outcome("Invalid trade type!")
            return None
        
        max_souls = max_souls_limits[trade_type]
        
        selected_souls = {
            "standard": {},
            "variant": {},
            "boss": {},
            "total_value": 0
        }
        
        if trade_type == 'boss':
            soul_categories = [("boss", player.boss_kill_tracker, "Boss Souls")]
        else:
            soul_categories = [
                ("standard", player.kill_tracker, "Standard Souls (1 soul each)"),
                ("variant", player.variant_kill_tracker, "Variant Souls (5 souls each)"),
                ("boss", player.boss_kill_tracker, "Boss Souls (10 souls each)")
            ]
        
        while selected_souls["total_value"] < min(required_souls, max_souls):
            remaining = min(required_souls, max_souls) - selected_souls["total_value"]
            
            available_categories = []
            for category_info in soul_categories:
                category_name, category_tracker, category_label = category_info
                if category_tracker and any(count > selected_souls[category_name].get(soul_name, 0) 
                                         for soul_name, count in category_tracker.items()):
                    available_categories.append(category_info)
            
            if not available_categories:
                event_display.show_outcome("No souls available! Press ESC to return to Soul Type selection.")
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (
                            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                        ):
                            return None
                    pygame.display.flip()
                    game_display.clock.tick(game_display.config.FPS)
            
            category_choices = [category_info[2] for category_info in available_categories]
            category_choices.extend(["Clear Selections", "Finish Selection"])
            
            category_choice = event_display.show_choice(
                "Soul Selection",
                category_choices,
                f"Total Souls Selected: {selected_souls['total_value']}/{min(required_souls, max_souls)}\n"
                f"Remaining Souls Needed: {remaining}"
            )
            
            if category_choice is None:
                return None
            
            if category_choice >= len(available_categories):
                if category_choice == len(available_categories):
                    selected_souls = {
                        "standard": {},
                        "variant": {},
                        "boss": {},
                        "total_value": 0
                    }
                    continue
                elif category_choice == len(available_categories) + 1:
                    if selected_souls["total_value"] > 0:
                        return selected_souls
                    event_display.show_outcome("Select at least some souls!")
                    continue
            
            category_name, category_tracker, category_label = available_categories[category_choice]
            
            if trade_type == 'boss':
                soul_values = {"boss": 1}
                soul_value_multiplier = 1
            else:
                soul_values = {"standard": 1, "variant": 5, "boss": 10}
                soul_value_multiplier = soul_values[category_name]
            
            soul_names = []
            available_souls = {}
            for soul_name, count in sorted(category_tracker.items(), key=lambda x: x[1], reverse=True):
                available = count - selected_souls[category_name].get(soul_name, 0)
                if available > 0:
                    monster_type = get_type_for_monster(soul_name)
                    type_str = f" ({monster_type.title()})" if monster_type != "unknown" else ""
                    soul_names.append(f"{soul_name}{type_str} (Available: {available})")
                    available_souls[soul_name] = available
            
            soul_choice = event_display.show_choice(
                f"Select {category_name.capitalize()} Soul",
                soul_names,
                f"Each {category_name} soul is worth {soul_value_multiplier} souls.\n"
                f"Max Souls: {max_souls}"
            )
            
            if soul_choice is not None:
                selected_soul_name = list(available_souls.keys())[soul_choice]
                max_available = available_souls[selected_soul_name]
                
                visual_input.text = ""
                # Draw the game screen first
                self.display.draw_game_screen(player, game.current_location)
                
                # Get layout and main panel dimensions
                layout = self.display.calculate_layout()
                main_panel = layout['main_panel']
                
                # Create semi-transparent overlay for entire screen
                overlay = pygame.Surface((main_panel[0], main_panel[1]))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(128)  # 50% transparency
                self.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
                
                # Draw title
                self.display.draw_text(f"Select quantity of {selected_soul_name} ({remaining // soul_value_multiplier} max)",
                            (self.display.config.SCREEN_WIDTH // 2, self.display.config.SCREEN_HEIGHT // 2 - 50),
                            'large', center=True)
                
                pygame.display.flip()
                
                while True:
                    # Draw input box centered
                    input_x = (self.display.config.SCREEN_WIDTH - visual_input.width) // 2
                    input_y = self.display.config.SCREEN_HEIGHT // 2
                    visual_input.draw(input_x, input_y)
                    
                    pygame.display.flip()
                    self.display.clock.tick(self.display.config.FPS)
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (
                            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                        ):
                            return None
                        
                        if visual_input.handle_event(event):
                            try:
                                quantity = int(visual_input.text)
                                
                                if quantity <= 0:
                                    event_display.show_outcome("Quantity must be positive!")
                                    visual_input.text = ""
                                    break
                                
                                if quantity > max_available:
                                    event_display.show_outcome(f"Only {max_available} souls available!")
                                    visual_input.text = ""
                                    break
                                
                                total_souls_value = quantity * soul_value_multiplier
                                
                                if selected_souls["total_value"] + total_souls_value > min(required_souls, max_souls):
                                    event_display.show_outcome("Would exceed maximum souls!")
                                    visual_input.text = ""
                                    break
                                
                                selected_souls[category_name][selected_soul_name] = selected_souls[category_name].get(selected_soul_name, 0) + quantity
                                selected_souls["total_value"] += total_souls_value
                                break
                            
                            except ValueError:
                                event_display.show_outcome("Please enter a valid number!")
                                visual_input.text = ""
                    else:
                        continue
                    break
        
        return selected_souls

    def _consume_selected_souls(self, player, selected_souls):
        """Consume only the selected souls and track them"""
        # Consume standard souls
        for enemy, count in selected_souls["standard"].items():
            if enemy in player.kill_tracker:
                if not hasattr(player, 'used_kill_tracker'):
                    player.used_kill_tracker = {}
                player.used_kill_tracker[enemy] = player.used_kill_tracker.get(enemy, 0) + count
                player.kill_tracker[enemy] -= count
                if player.kill_tracker[enemy] <= 0:
                    del player.kill_tracker[enemy]
                    
        # Consume variant souls
        for variant, count in selected_souls["variant"].items():
            if variant in player.variant_kill_tracker:
                if not hasattr(player, 'used_variant_tracker'):
                    player.used_variant_tracker = {}
                player.used_variant_tracker[variant] = player.used_variant_tracker.get(variant, 0) + count
                player.variant_kill_tracker[variant] -= count
                if player.variant_kill_tracker[variant] <= 0:
                    del player.variant_kill_tracker[variant]
                    
        # Consume boss souls
        for boss, count in selected_souls["boss"].items():
            if boss in player.boss_kill_tracker:
                if not hasattr(player, 'used_boss_kill_tracker'):
                    player.used_boss_kill_tracker = {}
                player.used_boss_kill_tracker[boss] = player.used_boss_kill_tracker.get(boss, 0) + count
                player.boss_kill_tracker[boss] -= count
                if player.boss_kill_tracker[boss] <= 0:
                    del player.boss_kill_tracker[boss]
                    
    def _forge_equipment_with_souls(self, player, game, forge_type, selected_souls):
        """Create equipment based on selected souls"""
        event_display = ComplexEventDisplay(game.display)
        
        # Determine equipment preferences based on souls
        equipment_affinities = self._get_equipment_affinities(selected_souls)
        preferred_stats = self._get_stat_preferences(selected_souls)
        
        if forge_type == "basic":
            def create_basic():
                event_display.show_forge_message("The forge accepts your offering...", game)
                self._create_themed_equipment(player, game, "basic", selected_souls,
                    equipment_affinities, preferred_stats)
                    
            def create_enhanced():
                event_display.show_forge_message("The souls enhance your crafting!", game)
                self._create_themed_equipment(player, game, "enhanced", selected_souls,
                    equipment_affinities, preferred_stats)
                    
            def forge_fail():
                event_display.show_forge_message("The forging process goes wrong!", game)
                self._take_damage(player, 10, 20, "Soul energy burns you! ")
                self._give_random_consumable(player, game, player.level)
                
            outcomes = [
                (0.4, create_basic),
                (0.3, create_enhanced),
                (0.3, forge_fail)
            ]
            self._resolve_weighted_outcome(outcomes, player)
            
        elif forge_type == "greater_forge":
            def create_greater():
                event_display.show_forge_message("The souls create something powerful!", game)
                self._create_themed_equipment(player, game, "greater", selected_souls,
                    equipment_affinities, preferred_stats)
                    
            def create_blessed():
                event_display.show_forge_message("The forge blesses your creation!", game)
                self._create_themed_equipment(player, game, "blessed", selected_souls,
                    equipment_affinities, preferred_stats)
                self._permanent_stat_increase(player)
                    
            def forge_rebel():
                event_display.show_forge_message("The souls rebel against your crafting!", game)
                self._take_damage(player, 20, 30, "Wild soul energy tears at you! ")
                self._create_themed_equipment(player, game, "basic", selected_souls,
                    equipment_affinities, preferred_stats)
                
            outcomes = [
                (0.4, create_greater),
                (0.3, create_blessed),
                (0.3, forge_rebel)
            ]
            self._resolve_weighted_outcome(outcomes, player)
            
        else:  # soulbound
            if random.random() < 0.7:
                event_display.show_forge_message("The forge resonates with your soul...", game)
                self._create_themed_equipment(player, game, "soulbound", selected_souls,
                    equipment_affinities, preferred_stats)
            else:
                event_display.show_forge_message("The soulbinding process fails catastrophically!", game)
                self._take_damage(player, 30, 50, "The souls tear at your essence! ")
                self._create_themed_equipment(player, game, "greater", selected_souls,
                    equipment_affinities, preferred_stats)
                
        """if forge_type != "soulbound":
            self._resolve_weighted_outcome(outcomes, player)"""

    def _create_themed_equipment(self, player, game, quality, souls_used, 
                            equipment_affinities, preferred_stats):
        """Create equipment with theme based on souls used"""
        item_display = ComplexEventDisplay(player.display)
        # Select equipment type from affinities
        equipment_type = random.choice(equipment_affinities) if equipment_affinities else \
            random.choice(["weapon", "shield", "helm", "chest", "boots", "gloves", "ring"])
        
        # Map quality to item tier
        tier_mapping = {
            "basic": "rare",
            "enhanced": "epic",
            "greater": "masterwork",
            "blessed": "legendary",
            "soulbound": "mythical"
        }
        target_tier = tier_mapping.get(quality, "rare")
        
        # Find valid base items
        valid_items = [item for item in game.items.values()
                    if item.type == equipment_type
                    and item.tier == target_tier]
        
        if not valid_items:
            print("No suitable equipment found!")
            return
            
        # Select and modify base item
        base_item = random.choice(valid_items)
        #print(f"Base item chosen is {base_item.name}") Debug print
        modified_item = self._modify_equipment_with_souls(base_item, souls_used, 
            quality, preferred_stats)
        
        player.add_item(modified_item)
        
        item_display.show_forged_item_description(modified_item, game, souls_used, preferred_stats)

    def _calculate_item_value(self, item):
        """Calculate item value based on stats and tier
        
        Each stat contributes to the final value with different weights.
        Tier multipliers are applied at the end.
        Soulbound items get a 50% bonus to final value.
        """
        base_value = 100  # Starting base value
        
        # Stat value multipliers
        if item.type == "weapon":
            stat_multipliers = {
                'attack': 5,
                'defence': 5,
                'accuracy': 5,
                'evasion': 10,
                'crit_chance': 10,
                'crit_damage': 3,
                'armour_penetration': 10,
                'damage_reduction': 10,
                'block_chance': 8
            }
        else:
            stat_multipliers = {
                'attack': 15,
                'defence': 15,
                'accuracy': 10,
                'evasion': 20,
                'crit_chance': 30,
                'crit_damage': 20,
                'armour_penetration': 20,
                'damage_reduction': 20,
                'block_chance': 15
            }
        
        # Calculate value from stats
        value = base_value
        for stat, multiplier in stat_multipliers.items():
            stat_value = getattr(item, stat, 0)
            if stat_value > 0:
                value += stat_value * multiplier
                
        # Tier multipliers
        tier_multipliers = {
            'common': 1,
            'uncommon': 2,
            'rare': 4,
            'epic': 7,
            'masterwork': 11,
            'legendary': 16,
            'mythical': 22
        }
        
        # Apply tier multiplier
        value *= tier_multipliers.get(item.tier, 1)
        
        # Apply Soulbound multiplier to all Soulbound items
        if isinstance(item, SoulboundItem):
            value *= 1.5  # 50% bonus for all soulbound items
            
        return int(value)
    
    def _modify_equipment_with_souls(self, base_item, souls_used, quality, preferred_stats):
        """Apply soul-based modifications to equipment"""
        # Generate themed name
        new_name = self._generate_themed_name(base_item, souls_used)
        
        # Create modified item
        if quality == "soulbound":
            modified_item = create_soulbound_item(
                base_item,
                growth_stats=preferred_stats,
                soul_source=souls_used
            )
            modified_item.name = new_name  # Apply themed name
        else:
            modified_item = type(base_item)(
                new_name,
                base_item.type,
                base_item.value,  # Initial value will be recalculated
                base_item.tier
            )
        
        # For weapons, set special weapon type
        if modified_item.type == "weapon":
            modified_item.weapon_type = "soulbound"
        
        # Quality multipliers for stats
        quality_multipliers = {
            "basic": 1.3,
            "enhanced": 1.6,
            "greater": 1.9,
            "blessed": 2.2,
            "soulbound": 2.5
        }
        multiplier = quality_multipliers.get(quality, 1.0)
        
        # Apply stat bonuses
        stats_to_modify = [
            "attack", "defence", "accuracy", "evasion", "crit_chance",
            "crit_damage", "armour_penetration", "damage_reduction", "block_chance"
        ]
        
        for stat in stats_to_modify:
            base_value = getattr(base_item, stat, 0)
            if base_value > 0:
                # Extra bonus for preferred stats
                bonus_multiplier = 1.2 if stat in preferred_stats else 1.0
                new_value = int(base_value * multiplier * bonus_multiplier)
                setattr(modified_item, stat, new_value)
        
        # Calculate and set new value based on stats
        modified_item.value = self._calculate_item_value(modified_item)
        
        return modified_item

    def _generate_themed_name(self, base_item, souls_used):
        """Generate a themed name based on souls used"""
        # Get most common monster type from souls
        monster_counts = {}
        for monster in souls_used.get("standard", {}):
            monster_type = get_type_for_monster(monster)
            monster_counts[monster_type] = monster_counts.get(monster_type, 0) + 1
            
        primary_type = max(monster_counts.items(), key=lambda x: x[1])[0] \
            if monster_counts else "unknown"
        
        prefixes = {
            "earth": ["Feral", "Bestial", "Savage", "Wild"],
            "wind": ["Tempest", "Gale", "Zephyr", "Windswept"],
            "water": ["Tidal", "Aqua", "Ocean", "Torrent"],
            "grass": ["Verdant", "Wild", "Primal", "Natural"],
            "dragon": ["Draconic", "Wyrm", "Dragon-Forged", "Scaled"],
            "undead": ["Deathbound", "Grave-Touched", "Ghostly", "Spectral"],
            "spirit": ["Ethereal", "Phantom", "Spirit-Touched", "Wraithbound"],
            "fire": ["Blazing", "Infernal", "Flame-Forged", "Molten"],
            "ice": ["Frozen", "Frost-Touched", "Glacial", "Rimefrost"],
            "lightning": ["Thunder", "Lightning", "Storm-Forged", "Tempest"],
            "arcane": ["Mystic", "Spellbound", "Arcane", "Enchanted"],
            "void": ["Void-Touched", "Null", "Cosmic", "Astral"],
            "warrior": ["Battle", "War-Forged", "Champion's", "Warrior"],
        }
        
        suffixes = {
            "weapon": ["Slayer", "Blade", "Reaver", "Edge"],
            "shield": ["Bulwark", "Aegis", "Guard", "Ward"],
            "helm": ["Crown", "Helm", "Visage", "Gaze"],
            "chest": ["Plate", "Armour", "Mail", "Guard"],
            "boots": ["Striders", "Treads", "Greaves", "Steps"],
            "gloves": ["Grips", "Touch", "Grasp", "Hold"],
            "ring": ["Circle", "Loop", "Band", "Seal"],
            "back": ["Cloak", "Mantle", "Shroud", "Cape"]
        }
        
        prefix = random.choice(prefixes.get(primary_type, ["Mysterious"]))
        suffix = random.choice(suffixes.get(base_item.type, ["Artifact"]))
        
        return f"{prefix} {suffix}"

    def _get_stat_preferences(self, souls_used):
        """Determine preferred stats based on souls used"""
        stat_votes = {}
        
        # Process standard souls and their types
        for monster, count in souls_used.get("standard", {}).items():
            monster_type = get_type_for_monster(monster)
            if monster_type in MONSTER_TYPES:
                for stat in MONSTER_TYPES[monster_type]["stat_preferences"]:
                    stat_votes[stat] = stat_votes.get(stat, 0) + count
                    
        # Process variant souls - add their preferences with higher weight
        if souls_used.get("variant"):
            variant_stats = ["accuracy", "crit_chance", "crit_damage", "armour_penetration", "attack", "evasion"]
            for stat in variant_stats:
                stat_votes[stat] = stat_votes.get(stat, 0) + sum(souls_used["variant"].values()) * 3
                
        # Process boss souls - add all high-tier stats
        if souls_used.get("boss"):
            boss_stats = [
                "attack", "defence", "accuracy", "crit_chance", "crit_damage",
                "armour_penetration", "damage_reduction", "block_chance"
            ]
            for stat in boss_stats:
                stat_votes[stat] = stat_votes.get(stat, 0) + sum(souls_used["boss"].values()) * 6
                
        # Return top stats
        sorted_stats = sorted(stat_votes.items(), key=lambda x: x[1], reverse=True)
        return [stat for stat, _ in sorted_stats[:4]]  # Return top 4 stats

    def _get_equipment_affinities(self, souls_used):
        """Determine equipment affinities based on souls used"""
        affinities = {}
        
        # Process standard souls
        for monster, count in souls_used.get("standard", {}).items():
            monster_type = get_type_for_monster(monster)
            if monster_type in MONSTER_TYPES:
                for equip_type in MONSTER_TYPES[monster_type]["equipment_affinities"]:
                    affinities[equip_type] = affinities.get(equip_type, 0) + count
                    
        # Return top equipment types
        sorted_affinities = sorted(affinities.items(), key=lambda x: x[1], reverse=True)
        return [equip for equip, _ in sorted_affinities[:3]]  # Return top 3 equipment types
    
    def _calculate_crystal_value(self, stored_buffs, special_effects):
        """Calculate soul crystal value based on stored buffs and special effects
        
        Args:
            stored_buffs: Dict of stat: (value, duration) pairs
            special_effects: List of CrystalEffect objects
        
        Returns:
            int: Calculated value of the crystal
        """
        value = 0
        
        # Value from stored buffs
        buff_multipliers = {
            'attack': 15,
            'defence': 15,
            'accuracy': 10,
            'evasion': 20,
            'crit_chance': 30,
            'crit_damage': 20,
            'armour_penetration': 20,
            'damage_reduction': 20,
            'block_chance': 15
        }
        
        # Calculate value from stored buffs
        for stat, (amount, duration) in stored_buffs.items():
            multiplier = buff_multipliers.get(stat, 50)  # Default 50 for unknown stats
            value += amount * multiplier * (duration / 10)  # Duration factor
            
        # Value from special effects
        for effect in special_effects:
            if isinstance(effect, BossResonance):
                # Value based on kill count and bonus values
                value += (effect.bonus * 150) * (effect.duration / 5)
                
            elif isinstance(effect, VariantAffinity):
                # Value based on kill count and bonus values
                value += (effect.bonus * 100) * (effect.duration / 5)
                
            elif isinstance(effect, SoulEcho):
                # Value based on kill count and percentage bonus
                value += (effect.bonus * 50) * (effect.duration / 5)
                
            elif isinstance(effect, ElementalResonance):
                # Fixed value for elemental effects
                value += 2500  # Base value for elemental effects
                
        # Apply minimum value
        value = max(100, value)
        
        return int(value)
    
    def _create_soul_crystal(self, player, game, crystal_type, selected_souls):
        """Create a soul crystal with the selected souls"""
        # Define base parameters for crystal types
        total_souls = sum(selected_souls["standard"].values()) + (sum(selected_souls["variant"].values()) * 5) + (sum(selected_souls["boss"].values()) * 10)
        crystal_params = {
            "lesser": {
                "buff_count": random.randint(1, 2),
                "min_value": random.randint(total_souls // 25, total_souls // 20),
                "max_value": random.randint(total_souls // 15, total_souls // 10),
                "min_duration": random.randint(total_souls // 20, total_souls // 15),
                "max_duration": random.randint(total_souls // 12, total_souls // 8),
                "tier": "uncommon"
            },
            "greater": {
                "buff_count": random.randint(2, 3),
                "min_value": random.randint(total_souls // 25, total_souls // 20),
                "max_value": random.randint(total_souls // 15, total_souls // 10),
                "min_duration": random.randint(total_souls // 20, total_souls // 15),
                "max_duration": random.randint(total_souls // 12, total_souls // 8),
                "tier": "rare"
            },
            "perfect": {
                "buff_count": random.randint(3, 4),
                "min_value": random.randint(total_souls // 25, total_souls // 20),
                "max_value": random.randint(total_souls // 15, total_souls // 10),
                "min_duration": random.randint(total_souls // 20, total_souls // 15),
                "max_duration": random.randint(total_souls // 12, total_souls // 8),
                "tier": "epic"
            }
        }
        
        params = crystal_params[crystal_type]
        preferred_stats = self._get_stat_preferences(selected_souls)
        
        # Create stored buffs
        stored_buffs = {}
        for _ in range(params["buff_count"]):
            if not preferred_stats:  # Guard against empty preferred_stats
                continue
                
            stat = random.choice(preferred_stats)
            value = random.randint(params["min_value"], params["max_value"])
            duration = random.randint(params["min_duration"], params["max_duration"])
            
            # Adjust values for certain stats
            if stat in ["accuracy", "crit_damage"]:
                value *= 2
            elif stat in ["armour_penetration", "damage_reduction", "block_chance"]:
                value = value // 2
            
            if stat in stored_buffs:
                old_value, old_duration = stored_buffs[stat]
                stored_buffs[stat] = (old_value + value, old_duration + duration)
            else:
                stored_buffs[stat] = (value, duration)
        
        # Create special effects
        special_effects = []
        
        # Add boss resonance if boss souls used
        if selected_souls.get("boss"):
            # Sum up total boss souls
            total_boss_souls = sum(selected_souls["boss"].values())
            # Get most common boss monster soul used
            special_effects.append(BossResonance("Boss Monsters", total_boss_souls))
            
        # Add variant affinity if variant souls used
        if selected_souls.get("variant"):
            # Sum up total variant souls
            total_variant_souls = sum(selected_souls["variant"].values())
            most_common_variant = max(selected_souls["variant"].items(), key=lambda x: x[1])
            special_effects.append(VariantAffinity(most_common_variant[0], total_variant_souls))
            
        # Add soul echo for most common standard soul
        if selected_souls.get("standard"):
            total_monster_souls = sum(selected_souls["standard"].values())
            most_common_monster = max(selected_souls["standard"].items(), key=lambda x: x[1])
            monster_type = get_type_for_monster(most_common_monster[0])
            special_effects.append(SoulEcho(monster_type, total_monster_souls))
        
         # Calculate crystal value using new method
        crystal_value = self._calculate_crystal_value(stored_buffs, special_effects)
        
        # Apply tier multiplier to final value
        tier_multipliers = {
            "uncommon": 1,
            "rare": 1.5,
            "epic": 2
        }
        crystal_value = int(crystal_value * tier_multipliers.get(params["tier"], 1))
        
        # Create crystal
        crystal = SoulCrystal(
            f"{crystal_type.capitalize()} Soul Crystal",
            crystal_value,
            params["tier"],
            stored_buffs,
            special_effects,
            selected_souls
        )
        
        self._consume_selected_souls(player, selected_souls)
        player.add_item(crystal)
        
        #print(f"\nCreated {crystal.name}!")
        #print(crystal.get_description())
        
        return crystal

    def _enhance_with_souls(self, player, game, enhancement_type, selected_souls):
        """Apply ability enhancements based on selected souls"""
        self._consume_selected_souls(player, selected_souls)
        preferred_stats = self._get_stat_preferences(selected_souls)
        
        if enhancement_type == "combat":
            def enhance_combat():
                print("The souls enhance your combat abilities!")
                for stat in random.sample(preferred_stats, min(2, len(preferred_stats))):
                    value = random.randint(8, 12)
                    if stat in ["accuracy", "crit_chance"]:
                        value *= 2
                    elif stat in ["armour_penetration", "damage_reduction", "block_chance"]:
                        value = value // 2
                    duration = random.randint(10, 15)
                    player.apply_buff(stat, value, duration, combat_only=False)
                    print(f"Gained +{value} {stat.replace('_', ' ').title()} for {duration} turns!")
                
            def absorb_experience():
                print("You absorb the combat experience of your fallen foes!")
                exp_gain = 30 * player.level
                bonus = sum(count for count in selected_souls["standard"].values())
                exp_gain += bonus * 5
                player.gain_exp(exp_gain, player.level)
                
            def enhance_strain():
                print("The enhancement strains your body!")
                self._take_damage(player, 10, 20, "Soul energy burns you! ")
                # But gives better buffs as compensation
                for stat in random.sample(preferred_stats, min(3, len(preferred_stats))):
                    value = random.randint(10, 15)
                    if stat in ["accuracy", "crit_chance"]:
                        value *= 2
                    elif stat in ["armour_penetration", "damage_reduction", "block_chance"]:
                        value = value // 2
                    duration = random.randint(12, 18)
                    player.apply_buff(stat, value, duration, combat_only=False)
                    print(f"Gained +{value} {stat.replace('_', ' ').title()} for {duration} turns!")
                
            outcomes = [
                (0.4, enhance_combat),
                (0.3, absorb_experience),
                (0.3, enhance_strain)
            ]
            
        elif enhancement_type == "attunement":
            def attune_souls():
                print("You attune with the collected souls!")
                self._give_major_buff(player, 10, 15, 15, 20)
                self._restore_and_heal(player, 0.5)
                
            def grant_power():
                print("The attunement grants lasting power!")
                self._permanent_stat_increase_specific(player, 2, random.sample(preferred_stats, 2))
                
            def painful_attunement():
                print("The attunement process is painful!")
                self._take_damage(player, 20, 30, "Soul energy tears at you! ")
                self._permanent_stat_increase_specific(player, 3, random.sample(preferred_stats, 2))
                
            outcomes = [
                (0.4, attune_souls),
                (0.3, grant_power),
                (0.3, painful_attunement)
            ]
            
        else:  # spirit
            if random.random() < 0.7:
                print("You form a powerful spirit bond!")
                # Multiple random buffs
                self._give_multiple_random_buffs(player, 10, 15, 15, 20, 3, preferred_stats)
                # And a permanent increase
                self._permanent_stat_increase_specific(player, 2, 
                    random.sample(preferred_stats, min(2, len(preferred_stats))))
            else:
                print("The spirit bond backfires!")
                self._take_damage(player, 30, 40, "Spirit energy overwhelms you! ")
                # But gives a powerful single buff as compensation
                stat = random.choice(preferred_stats)
                value = random.randint(12, 18)
                if stat in ["accuracy", "crit_chance"]:
                        value *= 2
                elif stat in ["armour_penetration", "damage_reduction", "block_chance"]:
                    value = value // 2
                duration = random.randint(15, 22)
                player.apply_buff(stat, value, duration, combat_only=False)
                print(f"Gained +{value} {stat.replace('_', ' ').title()} for {duration} turns!")
        
        if enhancement_type != "spirit":
            self._resolve_weighted_outcome(outcomes, player)
    
    # Dangerous Events
    
    # Unstable Ground Outcomes
        
    def _outcome_unstable_careful(self, player, game):
        """Carefully handle the unstable ground"""
        if random.random() < 0.8:
            print("You carefully move to stable ground and find another way! You feel tired after this endeavour")
            self._use_stamina(player, 0.1)
        else:
            self._take_damage(player, 5, 15, "Despite your best efforts, the ground falls from beneath you! ")
            
    def _outcome_unstable_quick(self, player, game):
        """Run across unstable ground"""
        if random.random() < 0.5:
            print("You sprint across safely saving alot of time and energy!")
            self._restore_stamina(player, 0.1)
        else:
            self._take_damage(player, 10, 25, "The ground collapses underneath you, you make it across but take severe damage! ")
            
    def _outcome_unstable_slow(self, player, game):
        """Slowly make your across the unstable ground"""
        if random.random() < 0.65:
            print("You carefully make your across the unstable ground!")
        else:
            self._take_damage(player, 5, 15, "Despite your best efforts, the ground falls from beneath you!")
            
    def _outcome_unstable_avoid(self, player, game):
        """Try to find another path"""
        if random.random() < 0.6:
            print("You find a safer path around the unstable ground!")
            self._use_stamina(player, 0.05)
        else:
            print("You waste a lot of time looking for a safer path, this is exhausting!")
            self._use_stamina(player, 0.15)
    
    # Strange Mushrooms Outcomes
            
    def _outcome_mushroom_pick(self, player, game):
        """Greedily pick the mushrooms"""
        if random.random() < 0.4:
            print("You manage to pick some useful reagents!")
            self._give_random_consumable(player, game, player.level)
        else:
            self._take_damage(player, 5, 15, "In your haste you disturb some spores and inhale them...")
            
    def _outcome_mushroom_harvest(self, player, game):
        """Slowly and carefully harvest the mushrooms"""
        if random.random() < 0.8:
            print("You take your time and manage to harvest some useful reagents, this has been tiring work!")
            print("Your stamina is reduced by 20 points!")
            self._give_random_consumable(player, game, player.level)
            player.stamina = max(0, player.stamina - 20)
        else:
            self._take_damage(player, 5, 10, "Despite your best efforts you disturb some spores and inhale them...")
            
    def _outcome_mushroom_eat(self, player, game):
        """Eat a mysterious mushroom...weirdo"""
        outcomes = [
            (0.2, lambda: (self._heal_player(player, 0.5), self._give_random_buff_specific(player, 5, 10, 8, 12, ["attack", "accuracy", "crit_damage", "crit_chance"]))),
            (0.2, lambda: (self._restore_stamina(player, 0.5), self._give_random_buff_specific(player, 5, 10, 8, 12, ["defence", "evasion", "block_chance"]))),
            (0.6, lambda: self._take_damage(player, 10, 20, "That was probably not a smart idea... "))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    # Cursed Shrine Outcomes
    
    def _outcome_shrine_blood(self, player, game):
        """Make a blood sacrifice at the cursed shrine."""
        print("You approach the dark altar, knowing it demands a sacrifice of life essence...")
        
        if player.hp <= 200:
            print("You're too weak to safely make a blood sacrifice!")
            self._take_damage(player, 5, 10, "The shrine doesn't care about that, dark energies reach out and drain some of your vitality! ")
            return
        
        # Use the health trading helper method
        success = self._trade_hp_for_reward(player, game, min_percent=15, max_percent=60)
        
        if not success:
            # Handle failed or cancelled sacrifice
            if random.random() < 0.5: # 50% chance of shrine being angry!
                print("The shrine pulses angrily at your hesitation!")
                self._take_damage(player, 5, 15, "Dark energy lashes out at you! It takes some of your life as recompense!")
                
    def _outcome_shrine_gold(self, player, game):
        """Offer gold to the cursed shrine, great risk, great reward"""
        event_display = ComplexEventDisplay(game.display)
        required_gold = random.randint(10, 30) * player.level
        if player.gold < required_gold:
            print("You don't have enough gold to make an offering")
            if random.random() < 0.5: # 50% chance of negative outcome
                self._take_damage(player, 10, 20, "The shrine punishes you for not having anything to offer! ")
            return
        
        choice = event_display.show_choice(
            "You approach the dark altar, knowing it demands a sacrifice of wealth...",
            ["Offer Gold!", "Ignore the Shrine"],
            "Would you like to sacrfice your gold to the shrine?"
        )
        
        if choice is None or choice == 1:
            self._outcome_shrine_ignore(player, game)
            return
        
        event_display.show_outcome(f"The shrine accepts your offering of {required_gold} gold...")
        
        player.gold -= required_gold
        #print("You place your gold upon the altar. It slowly disintegrates into a dark mist...")
        
        outcomes = [
            (0.3, lambda: (print("The shrine accepts your offering..."),
                           self._give_random_buff_specific(player, 8, 12, 10, 15,
                            ["attack", "defence", "evasion", "accuracy", "crit_chance"]),
                           self._give_gold(player, required_gold * 2, required_gold * 3))),
            (0.3, lambda: (print("Dark energy surges through you!"),
                           self._give_major_buff(player, 5, 10, 15, 20),
                           self._take_damage(player, 5, 10, "The power overwhelms you briefly! "))),
            (0.2, lambda: (print("The shrine's power infuses your very being!"),
                           self._permanent_stat_increase_specific(player, 3,
                            ["attack", "defence", "accuracy", "armour_penetration"]))),
            (0.2, lambda:(print("The shrine rejects your offering violently!"),
                          self._take_damage(player, 20, 30, "Dark energy explodes outward! ")))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_shrine_destroy(self, player, game):
        """Attempt to destroy the cursed shrine"""
        print("You attempt to destroy the dark altar...")
        
        # Check if player is strong enough based on level
        if player.level < 1:
            print("The shrine's power is too great for your current abilities!")
            self._take_damage(player, 25, 35, "Dark energy overwhelms you! ")
            return
        
        # Higher level = better chance of success
        success_chance = max(1.0, 0.3 + (player.level -10) * 0.05) # Caps at 70%
        
        if random.random() < success_chance:
            # Successful destruction...
            outcomes = [
                (0.4, lambda: (print("You destroy the shrine and absorb it's power!"),
                               self._give_major_buff(player, 10, 15, 10, 15),
                               self._gain_exp(player, 50, 100, "Dark knowledge floods your mind!"),
                               self._trigger_scaled_encounter(player, game, ["Shrine Guardian"]))),
                (0.3, lambda: (print("The shrine shatters revealing hidden treasures!"),
                               self._give_gold(player, 200, 400),
                               self._give_tier_equipment(player, game, player.level + 2),
                               self._trigger_scaled_encounter(player, game, ["Shrine Guardian"]))),
                (0.3, lambda: (print("As the shrine crumbles, its power permanently enhances you!"),
                               self._permanent_stat_increase_specific(player, 4,
                                ["attack", "defence", "evasion", "accuracy"]),
                               self._trigger_scaled_encounter(player, game, ["Shrine Guardian"])))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        else:
            # Failed destruction attempt
            print("Your attempt to destroy the shrine backfires horribly!")
            
            # Multiple negative effects
            self._take_damage(player, 30, 50, "Dark energy tears through you! ")
            outcomes = [
                (0.5, lambda: (print("The shrine's curse weakens you! Att and Def -10 until end of next combat!"),
                               player.apply_debuff("attack", 10),
                               player.apply_debuff("defence", 10))),
                (0.3, lambda: (print("The shrine drains your vitality!"),
                               self._drain_stamina(player, 0.5),
                               self._permanent_stat_decrease_specific(player, "max_hp", 10))),
                (0.2, lambda: (print("The shrine's guardian appears!"),
                               self._trigger_scaled_encounter(player, game, ["Shrine Guardian"])))
            ]
            self._resolve_weighted_outcome(outcomes, player)
    
    def _outcome_shrine_ignore(self, player, game):
        """Attempt to ignore the shrine"""
        if random.random() < 0.5:
            print("The shrine won't allow you to go that easily!")
            self._take_damage(player, 10, 20, "The shrine rips some health away from you before you escape! ")
        else:
            print("You hear something behind you as you attempt to leave, you turn around...")
            self._trigger_scaled_encounter(player, game, ["Shrine Guardian"])
    
    # Unstable Crystal Outcomes
            
    def _outcome_crystal_harness(self, player, game):
        """Attempt to harness the crystal's unstable power"""
        stamina_cost = player.max_stamina // 4
        if player.stamina < stamina_cost:
            print("You're too exhausted to focus on the crystal's energy!")
            return
        
        print("You reach out to channel the crystal's power...")
        self._drain_stamina(player, 0.25)
        
        outcomes = [
            (0.3, lambda: (print("The crystal's energy surges through you!"),
                           self._give_major_buff(player, 10, 15, 12, 18),
                           self._take_damage(player, 10, 20, "The power overwhelms you briefly! "))),
            (0.3, lambda: (print("You successfully harness the crystal's essence"),
                          self._give_random_buff_specific(player, 8, 12, 15, 20,
                               ["attack", "defence", "accuracy", "crit_chance"]),
                          self._restore_stamina(player, 0.5))),
            (0.2, lambda: (print("The crystal's power permanently alters you!"),
                          self._permanent_stat_increase(player),
                          self._take_damage(player, 5, 15, "The transformation is painful! "))),
            (0.2, lambda: (print("The crystal's energy violently rejects you!"),
                           self._take_damage(player, 25, 40, "Crystal energy tears through your body! "),
                           print("Def -10 until end of next combat!"),
                           player.apply_debuff("defence", 10)))
        ]
        self._resolve_weighted_outcome(outcomes, player)
      
    def _outcome_crystal_extract(self, player, game):
        """Attempt to extract the crystal"""
        print("You carefully attempt to extract the crystal...")
        
        if random.random() < 0.6: # 60% chance of success
            outcomes = [
                (0.4, lambda: (print("You successfully extract a shard of the crystal! It morphs in your hands becoming a piece of equipment!"),
                               self._give_tier_equipment(player, game, player.level + 2))),
                (0.3, lambda: (print("The crystal fractures, releasing stored energy!"),
                               self._give_multiple_consumables_random(player, game, 3))),
                (0.3, lambda: (print("You extract the crystal and gain its knowledge!"),
                               self._gain_exp(player, 40, 60)))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        else:
            print("As you attempt to pull the crystal free, you slip and lose your grip!")
            self._take_damage(player, 10, 25, "You slice your hands on the sharp crystal! ")
            print("Acc -10 until end of next combat!")
            player.apply_debuff("accuracy", 20)
            
    def _outcome_crystal_shatter(self, player, game):
        """Deliberately shatter the crystal"""
        print("You strike the crystal with force")
        
        if player.attack < 50: # Require 50 attack to break
            print("You're not strong enough to break the crystal... The crystal rings like a bell...")
            self._take_damage(player, 5, 10, "The vibrations travel through your weapon and hurt you! ")
            print("It turns out it didn't just sound like a bell, it acted as one!")
            self._trigger_scaled_encounter(player, game, ["Crystal Guardian"])
        else:
            outcomes = [
                (0.3, lambda: (print("The crystal explodes in a surge of power!"),
                               self._give_multiple_random_buffs(player, 5, 10, 8, 12, 3,
                               ["attack", "defence", "accuracy", "crit_chance", "crit_damage", "evasion"]),
                               self._take_damage(player, 20, 35, "Crystal shards lacerate you! "))),
                (0.3, lambda: (print("The crystals destruction releases trapped energy!"),
                               self._give_gold(player, 100, 200, "The rampant energy turns some of the surrounding rock to gold!"),
                               self._gain_exp(player, 30, 50, "The energy rushes into you, it increases your intellect!"))),
                (0.2, lambda: (print("The crystals destruction summons its Guardian!"),
                               self._trigger_scaled_encounter(player, game, ["Crystal Guardian"]))),
                (0.2, lambda: (print("The crystal violently explodes!"),
                               self._take_damage(player, 40, 60, "The explosion sends crystal shards through you! You are grievously wounded! "),
                               self._drain_stamina(player, 0.5)))
            ]
            self._resolve_weighted_outcome(outcomes, player)
            
    def _outcome_crystal_retreat(self, player, game):
        """Attempt to back away from the crystal"""
        print("You attempt to back away from the crystal...")
        
        if random.random() < 0.8: # 80% chance of success
            print("You successfully make it away!")
        else:
            print("As you think you're safely away...")
            self._take_damage(player, 10, 20, "A wave of energy strikes you! ")
    
    # Void Tear Outcomes
            
    def _outcome_void_sacrifice(self, player, game):
        """Sacrfice HP to the void for unique rewards"""
        print("The void's whispers grow stronger as you approach...")
        
        if player.hp <= 30:
            print("You're too weak to safely offer your essence to the void!")
            self._take_damage(player, 15, 20, "The void rips away some of your vitality anyway... ")
            return
        
        # Use health trading with higher percentages
        success = self._trade_hp_for_reward(player, game, min_percent=20, max_percent=80)
        
        if not success:
            # The void doesn't take kindly to hesitation, severe punishment
            if random.random() < 0.7:
                print("The void does not tolerate hesitation!")
                outcomes = [
                    (0.4, lambda: self._take_damage(player, 15, 25, "Void energy tears at your very essence! ")),
                    (0.3, lambda: (print("The void marks you as unworthy! Acc and Eva -15 until end of next combat!"),
                                   player.apply_debuff("accuracy", 15),
                                   player.apply_debuff("evasion", 15))),
                    (0.3, lambda: (print("The void starts to swell...something appears to be emerging!"),
                                   self._trigger_scaled_encounter(player, game, ["Void Walker"])))
                ]
                self._resolve_weighted_outcome(outcomes, player)
            else:
                print("The void swells to massive sizes! You can vaguely make out a shape moving...")
                self._trigger_scaled_encounter(player, game, ["Empowered Void Walker"])
                
    def _outcome_void_reach(self, player, game):
        """Reach through the void tear"""
        print("You reach into the swirling void...")
        
        def reach_out():
            outcomes = [
                (0.5, lambda: self._trigger_scaled_encounter(player, game, ["Void Walker"])),
                (0.5, lambda: self._trigger_scaled_encounter(player, game, ["Empowered Void Walker"]))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
        outcomes = [
            (0.25, lambda: (print("Your hand grasps something from beyond..."),
                            self._give_tier_equipment(player, game, player.level + 3),
                            self._give_random_buff_specific(player, 8, 12, 10, 15,
                                ["accuracy", "evasion", "crit_chance"]),
                            self._take_damage(player, 20, 30, "The void doesn't just give... "))),
            (0.25, lambda: (print("The void grants you insight into its nature!"),
                            self._gain_exp(player, 40, 60, "The knowledge is astounding... You gain alot of experience!"),
                            self._permanent_stat_increase_specific(player, 2,
                                ["accuracy", "evasion", "crit_chance"]),
                            self._take_damage(player, 15, 45, "The information you gain drives you slightly mad... You come too with wounds all over you! "))),
            (0.25, lambda: (print("The voids touch empowers you..."),
                            self._give_major_buff(player, 8, 12, 20, 25),
                            self._take_damage(player, 15, 25, "The voids touch burns at you! "))),
            (0.25, lambda: (print("The void reaches back!"),
                            self._take_damage(player, 20, 30, "The voids tendrils wrap around you arm! "),
                            print("You see something start to force it's way out!"), reach_out()))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_void_seal(self, player, game):
        """Attempt to seal the void tear"""
        print("You attempt to close the tear in reality...")
        
        # Check if player has enough stamina
        if player.stamina < (player.max_stamina * 0.6):
            print("You're too exhausted to focus on sealing the void!")
            self._take_damage(player, 15, 25, "Void energy lashes out at your weakness! ")
            return
        
        # Drain stamina for the attempt
        self._drain_stamina(player, 0.6)
        
        # Success chance based on level
        success_chance = min(0.7, 0.3 + (player.level - 6) * 0.05) # Caps at 70%
        
        if random.random() < success_chance:
            # Successful sealing
            outcomes = [
                (0.4, lambda: (print("You successfully seal the void tear!"),
                               self._give_major_buff(player, 10, 15, 15, 20),
                               self._gain_exp(player, 50, 75, "The knowledge of sealing the void strengthens you!"))),
                (0.3, lambda: (print("The void acknowledges your power!"),
                               self._give_gold(player, 200, 400),
                               self._give_multiple_consumables_random(player, game, 3))),
                (0.3, lambda: (print("As the tear closes, its power infuses you!"),
                               self._permanent_stat_increase_specific(player, 3, 
                                ["accuracy", "evasion", "crit_chance", "crit_damage"])))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
        else:
            # Failed sealing attempt
            print("Your attempt to seal the void tear fails catastrophically!")
            
            outcomes = [
                (0.4, lambda: (print("The void tears at your mind! Acc and Eva -20 until end of next combat!"),
                               self._take_damage(player, 35, 50, "Reality warps around you! "),
                               player.apply_debuff("accuracy", 20),
                               player.apply_debuff("evasion", 20))),
                (10.3, lambda: (print("The tear widens dangerously!"),
                               self._take_damage(player, 15, 30, "As the tear widens, it seems to rip at your mind too! "),
                               pygame.time.wait(2000),
                               self._trigger_scaled_encounter(player, game, ["Void Walker"]))),
                (0.3, lambda: (print("The void marks you for your failure"),
                               self._permanent_stat_decrease_specific(player, "max_hp", 10),
                               self._take_damage(player, 20, 30, "Void energy consumes your vitality! ")))
            ]
            self._resolve_weighted_outcome(outcomes, player)
            
    def _outcome_void_retreat(self, player, game):
        """Try to back away from the void tear"""
        
        if random.random() < 0.6: # 60% escape chance
            print("You manage to safely retreat from the void tear...")
            return
        else:
            print("The void will not let you leave so easily...")
            if random.random() < 0.5: # 50% chance for each back outcome
                self._take_damage(player, 15, 25, "Void tendrils lash out at you! ")
                print("Eva -10 until end of next combat!")
                player.apply_debuff("evasion", 10)
            else:
                print("A void entity follows you through the tear!")
                if random.random() < 0.8:
                    self._trigger_scaled_encounter(player, game, ["Void Walker"])
                else:
                    self._trigger_scaled_encounter(player, game, ["Empowered Void Walker"])
    
    # Storm Nexus Outcomes
    
    def _outcome_storm_channel(self, player, game):
        """Channel the storm's power with increasing risk/reward"""
        if player.stamina < (player.max_stamina * 0.3):
            print("You're too exhausted to channel such power!")
            return
            
        chain_count = 0
        max_chains = random.randint(3, 5)
        event_display = ComplexEventDisplay(game.display)
        
        while chain_count < max_chains:
            # Increase risk and reward with each chain
            stamina_cost = int(player.max_stamina * (0.15 + (chain_count * 0.1)))
            damage_range = (15 + (chain_count * 10), 25 + (chain_count * 15))
            buff_amount = random.randint(8 + (chain_count * 4), 12 + (chain_count * 6))
            buff_duration = random.randint(3 + (chain_count * 2), 5 + (chain_count * 3))
            
            event_display.show_progress(
                "Storm Channeling",
                chain_count + 1,
                max_chains,
                f"Chain Power: {buff_amount} | Risk: {damage_range[0]}-{damage_range[1]} | Stamina Cost: {stamina_cost}"
            )
            
            if player.stamina < stamina_cost:
                event_display.show_outcome("You're too exhausted to continue!")
                # Give buff equal to current chain
                self._give_random_buff_specific(player, buff_duration, buff_duration, 
                    buff_amount, buff_amount, ["attack", "accuracy", "crit_chance", "crit_damage"])
                break
                
            # Continue channeling prompt
            choice = event_display.show_choice(
                "Continue channeling the storm's power?",
                ["Continue", "Stop"],
                f"Current chain: {chain_count + 1}/{max_chains}"
            )
            
            if choice != 0: # If not continuing
                event_display.show_outcome("You safely absorb the current power!")
                self._give_random_buff_specific(player, buff_duration, buff_duration,
                    buff_amount, buff_amount, ["attack", "accuracy", "crit_chance", "crit_damage"])
                break
                
            self._use_stamina(player, stamina_cost)
            
            # Higher chain = lower success chance
            success_chance = 0.7 - (chain_count * 0.1)
            
            if random.random() < success_chance:
                event_display.show_outcome("You successfully channel the storm's power!")
                # Give potion based on chain count
                rarity_tiers = ["uncommon", "rare", "epic", "masterwork", "legendary"]
                if chain_count < len(rarity_tiers):
                    consumables = [item for item in game.items.values()
                                    if item.type == "consumable" and item.tier == rarity_tiers[chain_count]]
                    if consumables:
                        item = random.choice(consumables)
                        player.add_item(item)
                        event_display.show_outcome(f"The storms power crystalizes into {item.name}!",
                                                   2000)
                chain_count += 1
            else:
                event_display.show_outcome("The storm's power overwhelms you!", 2000)
                self._take_damage(player, damage_range[0], damage_range[1], "Lightning tears through your body! ")
                break
                
        if chain_count == max_chains:
            event_display.show_outcome(
                f"The storm's power resonates within you! Your base attack permanently increases by {chain_count}!",
                2000
            )
            # Give permanent attack increase equal to chain count
            player.base_attack += chain_count

    def _outcome_storm_collect(self, player, game):
        """Collect crystallized lightning for temporary power"""
        crystal_count = 0
        max_crystals = random.randint(3, 5)
        event_display = ComplexEventDisplay(game.display)
        
        while crystal_count < max_crystals:
            event_display.show_progress(
                "Crystal Collection",
                crystal_count + 1,
                max_crystals,
                "Gathering storm crystals..."
            )
            
            # Each crystal increases risk
            base_damage = 10 + (crystal_count * 5)
            if random.random() < (0.8 - (crystal_count * 0.1)):
                event_display.show_outcome("You successfully collect a crystal!")
                
                outcomes = [
                    (0.2, lambda: self._give_random_buff_specific(player, 6, 10, 8, 12,
                        ["attack", "accuracy", "crit_chance"])),
                    (0.15, lambda: self._restore_stamina(player, 0.25)),
                    (0.15, lambda: self._give_random_consumable(player, game, player.level)),
                    (0.15, lambda: self._give_tier_equipment(player, game, player.level)),
                    (0.1, lambda: self._give_multiple_random_buffs(player, random.randint(8, 12), random.randint(14, 18), random.randint(10, 14), random.randint(18, 22), random.randint(1, 3),
                         ["attack", "accuracy", "crit_chance", "crit_damage", "evasion", "armour_penetration"])),
                    (0.1, lambda: self._give_multiple_consumables_random(player, game, random.randint(2, 5))),
                    (0.1, lambda: self._give_major_buff(player, 8, 12, 15, 20)),
                    (0.05, lambda: self._give_special_item(player, game, "The crystal suddenly bursts into a kaleidoscope of colours!"))
                ]
                self._resolve_weighted_outcome(outcomes, player)
                crystal_count += 1
                
                if crystal_count < max_crystals:
                    choice = event_display.show_choice(
                        "Continue Collecting?",
                        ["Yes", "No"],
                        f"Current Crystals: {crystal_count}/{max_crystals}"
                    )
                    if choice != 0:
                        break
            else:
                event_display.show_outcome("The crystal shatters violently!")
                self._take_damage(player, base_damage, base_damage + 10,
                    "Crystal shards tear through you! ")
                break
                
        if crystal_count == max_crystals:
            event_display.show_outcome(
                "The crystals start to resonate together! Major buff granted!",
                2000
            )
            self._give_major_buff(player, 10, 15, 15, 20)

    def _outcome_storm_embrace(self, player, game):
        """Embrace the storm's power for permanent changes"""
        event_display = ComplexEventDisplay(game.display)
        event_display.show_outcome("You reach out to embrace the storm's power...")
        
        if player.hp < (player.max_hp * 0.5):
            event_display.show_outcome("You're too weak to embrace the storm's power!")
            self._take_damage(player, 20, 30, "The storm's energy tears through you! ")
            return
            
        outcomes = [
            (0.3, lambda: self._permanent_stat_increase_specific(player, 2, 
                ["accuracy", "crit_chance"])),
            (0.3, lambda: self._give_temporary_weapon_enchant(player, 15, 20, 20, 30)),
            (0.2, lambda: (self._permanent_stat_increase(player),
                self._give_major_buff(player, 8, 12, 15, 20))),
            (0.2, lambda: self._take_damage(player, 40, 50))
        ]
        
        event_display.show_outcome("The storm's power courses through you!")
        self._resolve_weighted_outcome(outcomes, player)

    def _outcome_storm_shelter(self, player, game):
        """Attempt to find shelter from the storm"""
        event_display = ComplexEventDisplay(game.display)
        if random.random() < 0.7:
            event_display.show_outcome("You find a small cave to shelter in...")
            
            # Small chance for hidden benefit
            if random.random() < 0.3:
                event_display.show_outcome("While waiting, you notice something...")
                self._give_random_consumable(player, game, player.level)
        else:
            event_display.show_outcome("You can't escape the storm's fury!")
            self._take_damage(player, 15, 25, "Lightning strikes nearby! ")
    
    def _outcome_ignore(self, player, game):
        """Ignore the event"""
        print("You decide to move on...")
        
    # Helper methods
    
    def _resolve_weighted_outcome(self, outcomes, player):
        """Resolve a weighted random outcome"""
        total = sum(weight for weight, _ in outcomes)
        r = random.random() * total
        
        current = 0
        for weight, outcome in outcomes:
            current += weight
            if r <= current:
                outcome()
                break
    
    def _gain_exp(self, player, min_exp, max_exp, message=""):
        """Player gains exp based on level"""
        exp_gain = random.randint(min_exp, max_exp) * player.level
        print(f"{message}")
        player.gain_exp(exp_gain, player.level)
        
    def _give_random_consumable(self, player, game, level):
        """Gives player a random consumable"""
        consumables = [item for item in game.items.values()
                       if item.type in ["consumable", "food", "drink"]
                       and self._is_appropriate_tier(item, level)]
        if consumables:
            item = random.choice(consumables)
            player.add_item(item)
            print(f"You acquired a {item.name} ({item.tier.title()})!")
            
    def _give_specific_consumable(self, player, game, level, type, effect_type):
        """Gives player a specific consumable type"""
        consumables = [item for item in game.items.values()
                       if item.type in type and item.effect_type in effect_type
                       and self._is_appropriate_tier(item, level)]
        if consumables:
            item = random.choice(consumables)
            player.add_item(item)
            print(f"You acquired a {item.name} ({item.tier.title()})!")
     
    def _give_multiple_consumables_random(self, player, game, count):
        """Give multiple random consumables"""
        for _ in range(count):
            self._give_random_consumable(player, game, player.level)
            
    def _give_multiple_consumables_specific(self, player, game, count, type, effect_type):
        for _ in range(count):
            self._give_specific_consumable(player, game, player.level, type, effect_type)
            
    def _give_tier_equipment(self, player, game, level):
        """Gives player a random piece of equipment appropriate to level"""
        equipment = [item for item in game.items.values()
                     if item.type in ["weapon", "helm", "chest", "legs", "boots", "gloves", "shield", "ring"]
                     and self._is_appropriate_tier(item, level)]
        if equipment:
            item = random.choice(equipment)
            player.add_item(item)
            print(f"You gained a {item.name}")
    
    def _give_special_item(self, player, game, *args):
        """Gives a special rare item"""
        special_items = [item for item in game.items.values()
                         if item.tier in ["masterwork", "legendary"]]
        
        if special_items:
            item = random.choice(special_items)
            player.add_item(item)
            if args:
                print(*args)
            print(f"You receive something special: {item.name} ({item.tier.title()})!")
            
    def _give_merchant_favour(self, player):
        """Give gold and exp for helping merchant"""
        gold = random.randint(150, 300)
        exp = random.randint(30, 60) * player.level
        player.gold += gold
        player.gain_exp(exp, player.level)
        print(f"The merchant rewards you with {gold} gold and valuable knowledge! (No lamborghini though)")
            
    def _give_gold(self, player, min_amount, max_amount, *args):
        """Give player some gold"""
        amount = random.randint(min_amount, max_amount)
        player.gold += amount
        if args:
            print(*args)
        print(f"You found {amount} gold!")
        
    def _heal_player(self, player, percentage):
        """Heal player by percentage of max HP"""
        heal_amount = int(player.max_hp * percentage)
        player.heal(heal_amount)
        print(f"You feel refreshed! Healed for {heal_amount} HP.")
        
    def _full_heal_player(self, player):
        """Fully heal player and restore stamina"""
        heal_amount = player.max_hp - player.hp
        stamina_amount = player.max_stamina - player.stamina
        player.heal(heal_amount)
        player.restore_stamina(stamina_amount)
        print("You feel completely reinvigorated! HP and Stamina fully restored!")
        
    def _restore_stamina(self, player, percentage):
        """Restore player stamina by percentage"""
        stamina_amount = int(player.max_stamina * percentage)
        player.restore_stamina(stamina_amount)
        print(f"You feel energised! Restored {stamina_amount} stamina.")
        
    def _drain_stamina(self, player, percentage):
        """Drain player stamina by percentage"""
        stamina_amount = int(player.max_stamina * percentage)
        player.stamina = max(0, player.stamina - stamina_amount)
        print(f"Your stamina is drained by {stamina_amount}!")
        
    def _use_stamina(self, player, amount):
        """Lose a set amount of stamina"""
        player.stamina = max(0, player.stamina - amount)
        print(f"You use {amount} of stamina!")
        
    def _restore_and_heal(self, player, percentage):
        """Restore player health and stamina"""
        heal_amount = int(player.max_hp * percentage)
        stamina_amount = int(player.max_stamina * percentage)
        player.heal(heal_amount)
        player.restore_stamina(stamina_amount)
        print(f"You feel energised and restored! Restored {stamina_amount} stamina and healed {heal_amount} HP.")
        
    def _take_damage(self, player, min_damage, max_damage, message=""):
        """Deal damage to player"""
        damage = random.randint(min_damage, max_damage) * 10
        player.take_damage(damage)
        if message:
            print(f"{message}You take {damage} damage!")
        else:
            print(f"You take {damage} damage!")
            
    def _sacrifice_health(self, player, amount, message=""):
        """Sacrifice health to for rewards"""
        player.take_damage(amount)
        if message:
            print(f"{message}You sacrifice {amount} health for power!")
        else:
            print(f"You sacrifice {amount} health for power!")
        
    def _hostile_response(self, player, game):
        """Trigger an immediate hostile encounter"""
        print("\nYou feel you've made a mistake... Something approaches!")
        # Force an encounter by setting random chance to 1
        old_random = random.random
        random.random = lambda: 0.5 # Ensures the encounter trigger succeeds
        game.encounter() # Handles enemy selection and battle
        random.random = old_random # Restore normal behaviour
    
    def _give_random_buff_percentile(self, player):
        """Gives player a random temporary buff"""
        buff_types = [
            ("attack", {
                "base": player.base_attack + player.level_modifiers["attack"] + player.equipment_modifiers.get("attack", 0),
                "min_percent": 5,
                "max_percent": 20,
                "name": "Attack"}),
            ("defence", {
                "base": player.base_defence + player.level_modifiers["defence"] + player.equipment_modifiers.get("defence", 0),
                "min_percent": 5,
                "max_percent": 20,
                "name": "Defence"}),
            ("accuracy", {
                "base": player.base_accuracy + player.level_modifiers["accuracy"] + player.equipment_modifiers.get("accuracy", 0),
                "min_percent": 15,
                "max_percent": 30,
                "name": "Accuracy"}),
            ("evasion", {
                "base": player.base_evasion + player.level_modifiers["evasion"] + player.equipment_modifiers.get("evasion", 0),
                "min_percent": 5,
                "max_percent": 20,
                "name": "Evasion"
            })
        ]
        # Select random buff type
        stat, buff_info = random.choice(buff_types)
        # Calculate percentage increase
        percent = random.randint(buff_info["min_percent"], buff_info["max_percent"])
        # Calculate actual value based on percentage of base stat
        value = int((buff_info["base"] * percent) / 100)
        # Ensure minimum of 1
        value = max(1, value)
        # Random duration between 5 and 10
        duration = random.randint(5, 10)
        # Apply the buff
        player.apply_buff(stat, value, duration, combat_only=False)
        print(f"You feel blessed! Gained +{value} {buff_info['name']} ({percent}% increase) for {duration} turns.")
    
    def _give_major_buff(self, player, min_dura, max_dura, min_amnt, max_amnt):
        """Give a significant temporary buff"""
        buff_duration = random.randint(min_dura, max_dura)
        buff_amount = random.randint(min_amnt, max_amnt)
        player.apply_buff("all stats", buff_amount, buff_duration, combat_only=False)
        print(f"You feel incredibly empowered! All stats increased by {buff_amount} for {buff_duration} turns!")
    
    def _give_random_buff_specific(self, player, min_dura, max_dura, min_amnt, max_amnt, stat=[]):
        """Give a random buff to a random stat in a list of stats"""
        stat = random.choice(stat)
        buff_duration = random.randint(min_dura, max_dura)
        buff_amount = random.randint(min_amnt, max_amnt)
        if stat in ["accuracy", "crit_chance"]:
            buff_amount *= 2
            player.apply_buff(stat, buff_amount, buff_duration, combat_only=False)
        elif stat in ["armour_penetration", "damage_reduction"]:
            buff_amount //= 2
            player.apply_buff(stat, buff_amount, buff_duration, combat_only=False)
        else:
            player.apply_buff(stat, buff_amount, buff_duration, combat_only=False)
        print(f"You feel empowered and gain {buff_amount} in {stat.replace('_', ' ').title()} for {buff_duration} turns.")
    
    def _give_multiple_random_buffs(self, player, min_dura, max_dura, min_amnt, max_amnt, count, stat=[]):
        """Gives multiple buffs selected randomly from a given list"""
        for _ in range(count):
            self._give_random_buff_specific(player, min_dura, max_dura, min_amnt, max_amnt, stat)
    
    def _give_temporary_weapon_enchant(self, player, min_dura, max_dura, min_amnt, max_amnt):
        """Gives a temporary weapon enchantment"""
        if random.random() < 0.3:
            # Significant weapon buff
            attack_boost = random.randint(min_amnt, max_amnt)
            duration = random.randint(min_dura, max_dura)
            player.apply_weapon_buff(attack_boost, duration, 'attack')
            print(f"Your weapon hums with energy! Attack increased by {attack_boost} for {duration} turns!")
        else:
            # Minor weapon buff
            attack_boost = random.randint(min_amnt, max_amnt) // 2
            duration = random.randint(min_dura, max_dura) // 2
            player.apply_weapon_buff(attack_boost, duration, 'attack')
            print(f"Your weapon buzzes with energy! Attack increased by {attack_boost} for {duration} turns!")
    
    def _temporary_max_increase(self, player):
        """Temporarily increase max HP and/or stamina"""
        # Random choice of which stat(s) to boost
        boost_type = random.choice([
            "hp",
            "stamina",
            "both"
        ])
        
        # Calculate boost amounts (15-25% increase)
        hp_boost = int(player.max_hp * random.randint(15, 25) / 100)
        stamina_boost = int(player.max_stamina * random.randint(15, 25) / 100)
        
        # Duration between 10-20 turns
        duration = random.randint(10, 20)
        
        message_parts = []
        
        if boost_type in ["hp", "both"]:
            player.max_hp += hp_boost
            player.hp = player.max_hp  # Fill to new maximum
            message_parts.append(f"maximum HP by {hp_boost}")
            
            # Create a delayed effect to remove the HP boost
            def remove_hp_boost():
                player.max_hp -= hp_boost
                player.hp = min(player.hp, player.max_hp)  # Ensure HP doesn't exceed new maximum
                
            # Store the removal function with the player's buffs
            player.active_buffs["temp_max_hp"] = {
                'value': hp_boost,
                'duration': duration,
                'remove_func': remove_hp_boost
            }
        
        if boost_type in ["stamina", "both"]:
            player.max_stamina += stamina_boost
            player.stamina = player.max_stamina  # Fill to new maximum
            message_parts.append(f"maximum stamina by {stamina_boost}")
            
            # Create a delayed effect to remove the stamina boost
            def remove_stamina_boost():
                player.max_stamina -= stamina_boost
                player.stamina = min(player.stamina, player.max_stamina)  # Ensure stamina doesn't exceed new maximum
                
            # Store the removal function with the player's buffs
            player.active_buffs["temp_max_stamina"] = {
                'value': stamina_boost,
                'duration': duration,
                'remove_func': remove_stamina_boost
            }
        
        message = f"The magical water surges through you, increasing your {' and '.join(message_parts)} for {duration} turns!"
        print(message)
        
    def _permanent_stat_increase(self, player):
        """Give a small permanent stat increase"""
        stat_choices = [
            ("max_hp", player.max_hp // 10),
            ("base_attack", 1),
            ("base_defence", 1),
            ("base_evasion", 1),
            ("base_accuracy", 2),
            ("max_stamina", player.max_stamina // 10)
        ]
        stat, amount = random.choice(stat_choices)
        setattr(player, stat, getattr(player, stat) + amount)
        print(f"You feel permanently strengthened! {stat.replace('_', ' ').title()} increased by {amount}!")
    
    def _permanent_stat_decrease(self, player):
        """Give a small permanent stat decrease"""
        stat_choices = [
            ("max_hp", player.max_hp // 10),
            ("base_attack", 1),
            ("base_defence", 1),
            ("base_evasion", 1),
            ("base_accuracy", 2),
            ("max_stamina", player.max_stamina // 10)
        ]
        stat, amount = random.choice(stat_choices)
        setattr(player, stat, getattr(player, stat) - amount)
        print(f"You feel permanently weakened! {stat.replace('_', ' ').title()} decreased by {amount}!")
    
    def _permanent_stat_increase_specific(self, player, value, stat=[]):
        """Give a small increase to chosen stat"""
        stat = random.choice(stat)
        if stat in ["accuracy", "crit_damage"]:
            value = value * 3
        elif stat in ["max_hp", "max_stamina"]:
            value = value * 10
        setattr(player, stat, getattr(player, stat) + int(value))
        print(f"You feel permanently strengthened! {stat.replace('_', ' ').title()} increased by {int(value)}!")
    
    def _permanent_stat_decrease_specific(self, player, stat, value):
        """Give a small decrease to chosen stat"""
        setattr(player, stat, getattr(player, stat) - int(value))
        print(f"You feel permanently weakened! {stat.replace('_', ' ').title()} decreased by {int(value)}!")
        
    def _discover_location(self, player, game, number):
        """Discover a number of unvisited locations"""
        locations = game.world_map.get_all_locations()
        undiscovered = [loc for loc in locations if loc not in player.visited_locations]
        if undiscovered:
            for _ in range(min(number, len(undiscovered))):
                loc = random.choice(undiscovered)
                player.add_visited_location(loc)
            print("You gain information about a new area of the map (Allows teleportation to location)")
        else:
            self._give_gold(player, 50, 100, "You already know of all locations, the Deities provide a monetary gain instead!")
    
    def _trade_hp_for_reward(self, player, game, min_percent=10, max_percent=75):
        """
        Trade a portion of health for a reward that scales with the sacrifice
        Default minimum 10%, maximum 75%, changeable when calling method
        """
        # Calculate health cost (percentage of current HP)
        max_sacrifice = int(player.hp * (max_percent / 100))
        min_sacrifice = int(player.hp * (min_percent / 100))
        
        if player.hp <= min_sacrifice:
            print("You don't have enough health to sacrifice!")
            return False
        
        event_display = ComplexEventDisplay(game.display)
        visual_input = VisualInput(game.display)
        visual_input.text = ""
        
        while True:
            # Draw the game screen first
            game.display.draw_game_screen(game.player, game.current_location)
            
            # Get main panel dimensions
            layout = game.display.calculate_layout()
            main_panel = layout['main_panel']
            
            # Draw semi-transparent overlay just for main panel
            overlay = pygame.Surface((main_panel[0], main_panel[1]))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(200)  # More opaque for better readability
            game.display.screen.blit(overlay, (main_panel[2], main_panel[3]))
            
            # Calculate positions relative to main panel
            panel_center_x = main_panel[2] + (main_panel[0] // 2)
            base_y = main_panel[3] + 50  # Start 50 pixels from top of panel
            
            # Draw title
            game.display.draw_text("=== BLOOD SACRIFICE ===",
                                (panel_center_x, base_y),
                                'title', 'red', center=True)
            
            # Draw HP info
            game.display.draw_text(f"Current HP: {player.hp}/{player.max_hp}",
                                (panel_center_x, base_y + 100),
                                'large', center=True)
            
            # Draw sacrifice info
            game.display.draw_text(f"Choose sacrifice amount ({min_sacrifice}-{max_sacrifice} HP)",
                                (panel_center_x, base_y + 150),
                                'large', center=True)
            
            # Draw input box
            input_x = panel_center_x - (visual_input.width // 2)
            input_y = base_y + 200
            visual_input.draw(input_x, input_y)
            
            # Draw instructions
            game.display.draw_text("Press ENTER to confirm sacrifice, ESC to cancel",
                                (panel_center_x, base_y + 300),
                                'medium', center=True)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    return False
                    
                if visual_input.handle_event(event):
                    try:
                        sacrifice = int(visual_input.text)
                        if min_sacrifice <= sacrifice <= max_sacrifice:
                            # Valid sacrifice amount, continue with rewards
                            break
                        event_display.show_outcome("Invalid sacrifice amount!")
                        visual_input.text = ""
                        continue
                    except ValueError:
                        event_display.show_outcome("Please enter a valid number!")
                        visual_input.text = ""
                        continue
            else:
                continue
            break
        
        # Calculate reward scaling factor (higher sacrifice = higher reward)
        scaling = sacrifice / max_sacrifice  # 0.0 to 1.0
        
        # Pay the health cost
        self._sacrifice_health(player, sacrifice, "The powers that be accept your sacrifice... ")
        
        # Choose reward type based on sacrifice amount
        if random.random() < 0.2 + (scaling * 0.3):  # 20-50% chance for special reward
            reward_type = 'special'
        elif random.random() < 0.5 + (scaling * 0.2):  # 50-70% chance for major reward
            reward_type = 'major'
        elif random.random() < 0.7 + (scaling * 0.2):  # 70-90% chance for minor reward
            reward_type = 'minor'
        else:
            reward_type = 'basic'
        
        # Grant reward based on type
        if reward_type == 'special':
            # Special rewards - rare/powerful items or significant permanent bonuses
            if random.random() < 0.5:
                self._give_special_item(player, game, "The powers that be grant you an item of great power!")
            else:
                print("Powerful energy surges through you, permanently enhancing your stats!")
                self._permanent_stat_increase_specific(player, 5, ["attack", "defence", "evasion", "accuracy", "armour_penetration"])
        
        elif reward_type == 'major':
            # Major rewards - significant temporary buffs or valuable items
            if random.random() < 0.5:
                print("The nearby energy surrounds you and empowers you!")
                print("Gain a significant temporary bonus to all stats!")
                print("And a small permanent increase to one stat!")
                buff_amount = int(15 + (scaling * 10))  # 15-25 stat boost
                duration = int(10 + (scaling * 5))  # 10-15 turns
                self._give_major_buff(player, buff_amount, buff_amount, duration, duration)
                self._permanent_stat_increase(player)
            else:
                gold_amount = int(100 + (scaling * 400))  # 100-500 gold
                self._give_gold(player, gold_amount, gold_amount, "The powerful energy provides a golden reward and a strong piece of equipment!")
                self._give_tier_equipment(player, game, player.level * 2)
        
        elif reward_type == 'minor':
            # Minor rewards - small buffs or random consumables
            if random.random() < 0.5:
                print("The swirling energy provides a small temporary buff!")
                buff_amount = int(5 + (scaling * 10))  # 5-15 stat boost
                duration = int(5 + (scaling * 5))  # 5-10 turns
                self._give_random_buff_specific(player, duration, duration, buff_amount, buff_amount,
                                            ["attack", "defence", "evasion", "accuracy"])
            else:
                gold_amount = int(50 + (scaling * 150))  # 50-200 gold
                self._give_gold(player, gold_amount, gold_amount, "The energy provides a small financial boon!")
                print("It also provides a couple of consumables!")
                self._give_multiple_consumables_random(player, game, 2)
        
        else:  # basic reward
            print("The energy seems to sneer at you and spits out a piece of equipment at you! Hawk Tuah!")
            self._give_tier_equipment(player, game, player.level)
        
        return True
    
    def _trigger_scaled_encounter(self, player, game, enemy_type=[]):
        """Trigger an encounter with a level-scaled enemy"""
        # Randomly choose between giving enemies
        event_display = ComplexEventDisplay(game.display)
        game.display.pause()
        
        enemy_type = random.choice(enemy_type)
        enemy = create_enemy(enemy_type, player)
        
        event_display.show_outcome(
            f"Something approaches! Prepare yourself for a fight against a {enemy.name}!",
            2000
        )
        
        if enemy:
            if game.battle is None:
                game.initialise_battle()
            game.battle.battle(enemy)
            game.display.text_buffer.clear()
        else:
            # Fallback to normal encounter
            print("\nSomething approaches! Prepare yourself!")
            game.encounter()
                            
    def _is_appropriate_tier(self, item, level):
        """Check if item tier is appropriate for level"""
        tier_levels = {
            "common": 1,
            "uncommon": 3,
            "rare": 6,
            "epic": 10,
            "masterwork": 15,
            "legendary": 20,
            "mythical": 25
        }
        # Find the highest tier available at player's level
        highest_available_tier = None
        for tier, req_level in tier_levels.items():
            if level >= req_level:
                highest_available_tier = tier
                
        # Return true only if item is of the highest available tier
        return item.tier == highest_available_tier
    
    """def _pause(self):
        input("Press Enter to continue...")"""