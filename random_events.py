from enemies import Enemy, create_enemy
from enum import Enum
import random

class EventType(Enum):
    BENEFICIAL = "beneficial"
    NEUTRAL  = "neutral"
    DANGEROUS = "dangerous"
    
class RandomEvent:
    def __init__(self, name, description, event_type, choices, conditions=None):
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
    
    def display(self):
        """Display event and choices"""
        print(f"\n=== {self.name} ===")
        print(f"\n{self.description}")
        print("\nWhat do you do?")
        for i, (choice_text, _) in enumerate(self.choices, 1):
            print(f"{i}. {choice_text}")
            
    def handle_choice(self, choice_idx, player, game):
        """Execute the chosen outcome"""
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
        
        events.append(RandomEvent(
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
                ("Make an offering (10 gold)", self._outcome_shrine_offer),
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
        
        # Dangerous events
        
        events.append(RandomEvent(
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
                "location_type": ["Cave", "Ruins", "Temple", "Deepwoods", "Ancient Ruins", "Death Caves", "Volcanic Valley", "Shadowed Valley", "Mountain", "Mountain Peaks"]
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
                "min_level": 4,
                "location_type": ["Heavens", "Death Valley", "Temple", "Ancient Ruins", "Death Caves", "Shadowed Valley", "Cave"]
            }
        ))
        
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
        event.display()
        
        while True:
            try:
                choice = int(input("\nEnter your choice (or 0 to try to leave): "))
                if choice == 0:
                    if random.random() < 0.7: # 70% chance to successfully leave
                        print("You carefully leave the area...")
                        return
                    else:
                        print("You can't avoid this situation...")
                        continue
                    
                if event.handle_choice(choice - 1, player, game):
                    break
                else:
                    print("Invalid choice. Please try again")
            except ValueError:
                print("Please enter a number!")
                
    # Event Outcomes
    # Beneficial
    
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
            (0.4, lambda: self._take_damage(player, 5, 15, "You trigger a nasty trap!"))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_traveller_accept(self, player, game):
        """Accept the travellers offer"""
        print("The traveller imparts his ancient wisdom upon you.")
        self._gain_exp(player, 10, 25)
        
    def _outcome_traveller_chat(self, player, game):
        """Have a chat with the traveller"""
        print("The traveller enjoys having a conversation with you. He generously gives you some gold as a gift!")
        self._give_gold(player, 10 * player.level, 20 * player.level)
        
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
            print("You spend time helping guard the merchant's caravan... This completely exhausts you!")
            message = "The merchant rewards you with"
            outcomes = [
                (0.4, lambda: (print(f"{message} some gold!"), self._give_gold(player, 200, 300))),
                (0.3, lambda: (print(f"{message} a number of consumables!"), self._give_multiple_consumables_random(player, game, random.randint(2, 5)))),
                (0.2, lambda: (print(f"{message} some gold and knowledge!"), self._gain_exp(player, 20, 40), self._give_gold(player, 100, 200))),
                (0.1, lambda: (print(f"{message} a special item!"), self._give_tier_equipment(player, game, random.randint(player.level + 1, player.level + 3))))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
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
            self._give_tier_equipment(player, game, player.level)
        else:
            self._give_multiple_consumables_specific(player, game, random.randint(1, 3), "consumable", "buff")
            
    def _outcome_training_rest(self, player, game):
        """Rest at the training grounds"""
        print("You rest at the ancient training grounds.")
        self._restore_and_heal(player, 0.5)
        
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
            (0.5, lambda: self._take_damage(player, 20, 30, "The god whose shrine this is smites you for your unholy act!")),
            (0.3, lambda: self._give_gold(player, 50, 100, "You find some of the gold other adventurers have left and steal it!")),
            (0.1, lambda: self._give_tier_equipment(player, game, player.level)),
            (0.1, lambda: print("Nothing happens, but you do feel guilty."))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_help_adventurer(self, player, game):
        """Help the lost adventurer"""
        if random.random() < 0.7:
            print("The grateful adventurer shares some supplies with you!")
            self._give_random_consumable(player, game, player.level)
        else:
            self._gain_exp(player, 5, 15, "The adventurer shares some valuable knowledge!")
            
    def _outcome_ask_adventurer(self, player, game):
        """Ask the adventurer for information"""
        self._discover_location(player, game, 1)
        print("The adventurer marks an interesting location on your map!")
    
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
            (0.7, lambda: self._take_damage(player, 10, 20, "The spirit of the statue doesn't take kindly to you looting it!")),
            (0.2, lambda: (print("You find a piece of equipment hidden behind the statue!"), self._give_tier_equipment(player, game, player.level))),
            (0.1, lambda: self._give_special_item(player, game, "The spirit of this statue approves of your gall! It provides an impressive piece of equipment!"))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_echo_call(self, player, game):
        """Call out into the echo chamber"""
        outcomes = [
            (0.3, lambda: (print("Your voice reutrns with an empowering presence!"), self._give_random_buff_specific(player, 5, 10, 8, 12, ["attack", "defence", "accuracy"]))),
            (0.4, lambda: self._give_random_consumable(player, game, player.level)),
            (0.15, lambda: print("Your voice echoes away unanswered!")),
            (0.15, lambda: self._hostile_response(player, game))
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
                (0.3, lambda: self._give_tier_equipment(player, game, player.level)),
                (0.1, lambda: self._gain_exp(player, 15, 25, "You hear some knowledgeable words come back to you!")),
                (0.1, lambda: (print("The confusing echoes disorient you! Acc -10 until end of next combat!"), player.apply_debuff("accuracy", 10)))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_echo_stone(self, player, game):
        """Throwing stones can be dangerous"""
        def mechanism():
            """Trigger a random mechanism effect"""
            if random.random() < 0.5:
                self._take_damage(player, 5, 15, "Your stone triggers a trap!")
            else:
                heal_amount = player.max_hp // 4
                player.heal(heal_amount)
                print(f"Your stone triggers an ancient blessing! Restores {heal_amount} HP!")

        outcomes = [
            (0.6, lambda: (print("The echoes revel a safe path forward, you regain 25% stamina!"), self._restore_stamina(player, 0.25))),
            (0.2, lambda: self._give_random_consumable(player, game, player.level)),
            (0.1, lambda: mechanism()),
            (0.1, lambda: self._take_damage(player, 5, 15, "Your stone returns unexpectedly!"))
        ]
        self._resolve_weighted_outcome(outcomes, player)
            
    def _outcome_echo_quiet(self, player, game):
        """Sneak past the chamber like a mouse"""
        outcomes = [
            (0.6, lambda: print("You pass through safely and quietly.")),
            (0.3, lambda: self._give_gold(player, 10, 30)),
            (0.1, lambda: self._permanent_stat_increase_specific(player, 1, ["accuracy"]))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
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
                (0.3, lambda: (self._give_tier_equipment(player, game, player.level), self._give_gold(player, 25, 50))),
                (0.3, lambda: self._give_multiple_consumables_random(player, game, 3)),
                (0.2, lambda: self._discover_location(player, game, 1)),
                (0.2, lambda: print("Despite your thorough search, you come up empty handed!"))
            ]
            self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_caravan_quick(self, player, game):
        """Quickly grab visible items from the caravan"""
        outcomes = [
            (0.3, lambda: self._give_random_consumable(player, game, player.level)),
            (0.3, lambda: self._give_gold(player, 20, 50)),
            (0.4, lambda: self._take_damage(player, 5, 15, "You trigger a hidden trap!"))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_caravan_survivors(self, player, game):
        """Look for survivors around the caravan"""   
        outcomes = [
            (0.4, lambda: self._gain_exp(player, 20, 40, "You help a grateful survivor who shares valuable knowledge!")),
            (0.3, lambda: (self._give_tier_equipment(player, game, player.level), self._give_gold(player, 20, 50))),
            (0.3, lambda: (print("You find clues as to what caused this."), self._discover_location(player, game, 1)))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_ritual_channel(self, player, game):
        """Attempt to channel the ritual site's energy"""
        outcomes = [
            (0.3, lambda: (print("Ancient power surges through you!"), self._give_major_buff(player, 10, 15, 15, 25), self._heal_player(player, 0.25))),
            (0.3, lambda: self._give_temporary_weapon_enchant(player, 16, 24, 15, 30)),
            (0.2, lambda: (print("You feel drained from channeling the ritual but also reinvigorated!"), self._drain_stamina(player, 0.5), self._gain_exp(player, 20, 35))),
            (0.2, lambda: (self._take_damage(player, 15, 25, "The ritual backfires!"), self._give_random_buff_specific(player, 5, 8, 10, 20, ["attack", "defence", "accuracy"])))
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
                (0.3, lambda: (self._give_gold(player, 50, 100, "You discover a hidden cache of coins!"), self._give_random_buff_specific(player, 8, 12, 10, 15, ["attack", "defence", "accuracy"])))
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
                           self._give_random_buff_specific(player, 5, 8, 5, 10, ["defence", "damage_reduction", "block_chance"]))),
            (0.3, lambda: (print("You fail to cleanse the ritual but gain insights!"), self._gain_exp(player, 25, 40, "You feel knowledgable from your failure...paradoxically!"), self._restore_stamina(player, 0.5)))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
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
                self._give_gold(player, 40, 80)
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
                    (0.2, lambda: (print("Gold starts falling all around...it's molten!"), self._take_damage(player, 5, 7, "Some gold lands on you, burning your flesh!"), self._give_gold(player, 100, 150))),
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
    
    # Dangerous Events
        
    def _outcome_unstable_careful(self, player, game):
        """Carefully handle the unstable ground"""
        if random.random() < 0.8:
            print("You carefully move to stable ground and find another way! You feel tired after this endeavour")
            player.stamina = max(0, player.stamina - 10)
        else:
            self._take_damage(player, 5, 15, "Despite your best efforts, the ground falls from beneath you!")
            
    def _outcome_unstable_quick(self, player, game):
        """Run across unstable ground"""
        if random.random() < 0.5:
            print("You sprint across safely saving alot of time and energy!")
            self._restore_stamina(player, 0.1)
        else:
            self._take_damage(player, 10, 25, "The ground collapses underneath you, you make it across but take severe damage!")
            
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
            player.stamina = max(0, player.stamina - 10)
        else:
            print("You waste a lot of time looking for a safer path, this is exhausting!")
            player.stamina = max(0, player.stamina - 20)
            
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
            self._give_random_consumable(player, game, player.level)
            player.stamina = max(0, player.stamina - 20)
        else:
            self._take_damage(player, 5, 10, "Despite your best efforts you disturb some spores and inhale them...")
            
    def _outcome_mushroom_eat(self, player, game):
        """Eat a mysterious mushroom...weirdo"""
        outcomes = [
            (0.2, lambda: (self._heal_player(player, 0.5), self._give_random_buff_specific(player, 5, 10, 8, 12, ["attack", "accuracy", "crit_damage", "crit_chance"]))),
            (0.2, lambda: (self._restore_stamina(player, 0.5)), self._give_random_buff_specific(player, 5, 10, 8, 12, ["defence", "evasion", "block_chance"])),
            (0.6, lambda: self._take_damage(player, 10, 20, "That was probably not a smart idea... "))
        ]
        self._resolve_weighted_outcome(outcomes, player)
    
    def _outcome_shrine_blood(self, player, game):
        """Make a blood sacrifice at the cursed shrine."""
        print("You approach the dark altar, knowing it demands a sacrifice of life essence...")
        
        if player.hp <= 20:
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
        required_gold = random.randint(10, 30) * player.level
        if player.gold < required_gold:
            print("You don't have enough gold to make an offering")
            if random.random() < 0.5: # 50% chance of negative outcome
                self._take_damage(player, 10, 20, "The shrine punishes you for not having anything to offer! ")
            return
        
        player.gold -= required_gold
        print("You place your gold upon the altar. It slowly disintegrates into a dark mist...")
        
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
                (0.3, lambda: (print("The tear widens dangerously!"),
                               self._take_damage(player, 15, 30, "As the tear widens, it seems to rip at your mind too! "),
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
            print(f"You acquired a {item.name}!")
            
    def _give_specific_consumable(self, player, game, level, type, effect_type):
        """Gives player a specific consumable type"""
        consumables = [item for item in game.items.values()
                       if item.type in type and item.effect_type in effect_type
                       and self._is_appropriate_tier(item, level)]
        if consumables:
            item = random.choice(consumables)
            player.add_item(item)
            print(f"You acquired a {item.name}!")
     
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
            print(*args)
            print(f"You receive something special: {item.name}!")
            
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
        print("You feel fully reinvigorated!")
        
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
        
    def _restore_and_heal(self, player, percentage):
        """Restore player health and stamina"""
        heal_amount = int(player.max_hp * percentage)
        stamina_amount = int(player.max_stamina * percentage)
        player.heal(heal_amount)
        player.restore_stamina(stamina_amount)
        print(f"You feel energised and restored! Restored {stamina_amount} stamina and healed {heal_amount} HP.")
        
    def _take_damage(self, player, min_damage, max_damage, message=""):
        """Deal damage to player"""
        damage = random.randint(min_damage, max_damage)
        player.take_damage(damage)
        print(f"{message}You take {damage} damage!")
        
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
                "base": player.base_attack + player.level_modifiers["attack"],
                "min_percent": 5,
                "max_percent": 20,
                "name": "Attack"}),
            ("defence", {
                "base": player.base_defence + player.level_modifiers["defence"],
                "min_percent": 5,
                "max_percent": 20,
                "name": "Defence"}),
            ("accuracy", {
                "base": player.base_accuracy + player.level_modifiers["accuracy"],
                "min_percent": 15,
                "max_percent": 30,
                "name": "Accuracy"}),
            ("evasion", {
                "base": player.base_evasion + player.level_modifiers["evasion"],
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
            player.weapon_buff = {
                'value': attack_boost,
                'duration': duration
            }
            print(f"Your weapon hums with energy! Attack increased by {attack_boost} for {duration} turns!")
        else:
            # Minor weapon buff
            attack_boost = random.randint(min_amnt, max_amnt) // 2
            duration = random.randint(min_dura, max_dura) // 2
            player.weapon_buff = {
                'value': attack_boost,
                'duration': duration
            }
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
            ("max_hp", 5),
            ("base_attack", 1),
            ("base_defence", 1),
            ("base_evasion", 1),
            ("base_accuracy", 2),
            ("max_stamina", 5)
        ]
        stat, amount = random.choice(stat_choices)
        setattr(player, stat, getattr(player, stat) + amount)
        print(f"You feel permanently strengthened! {stat.replace('_', ' ').title()} increased by {amount}!")
    
    def _permanent_stat_decrease(self, player):
        """Give a small permanent stat increase"""
        stat_choices = [
            ("max_hp", 5),
            ("base_attack", 1),
            ("base_defence", 1),
            ("base_evasion", 1),
            ("base_accuracy", 2),
            ("max_stamina", 5)
        ]
        stat, amount = random.choice(stat_choices)
        setattr(player, stat, getattr(player, stat) - amount)
        print(f"You feel permanently weakened! {stat.replace('_', ' ').title()} decreased by {amount}!")
    
    def _permanent_stat_increase_specific(self, player, value, stat=[]):
        """Give a small increase to chosen stat"""
        stat = random.choice(stat)
        setattr(player, stat, getattr(player, stat) + value)
        print(f"You feel permanently strengthened! {stat.replace('_', ' ').title()} increased by {value}!")
    
    def _permanent_stat_decrease_specific(self, player, stat, value):
        """Give a small decrease to chosen stat"""
        setattr(player, stat, getattr(player, stat) - value)
        print(f"You feel permanently weakened! {stat.replace('_', ' ').title()} decreased by {value}!")
        
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
    
    def _trade_hp_for_reward(self, player, game, min_percent = 10, max_percent = 75):
        """
        Trade a portion of health for a reward that scales with the sacrifice
        Default minimum 10%, maximum 75%, changeable when calling method
        """
        # Calculate the health cost (percentage of current HP)
        max_sacrifice = int(player.hp * (max_percent / 100))
        min_sacrifice = int(player.hp * (min_percent / 100))
        
        if player.hp <= min_sacrifice:
            print("You don't have enough health to sacrifice!")
            return
        
        # Let the player choose the sacrifice amount within range
        print(f"\nChoose amount of health to sacrifice ({min_sacrifice} - {max_sacrifice} HP):")
        print(f"Current HP: {player.hp}/{player.max_hp}")
        
        try:
            sacrifice = int(input(f"Enter amount to sacrifice (0 to cancel): "))
            if sacrifice == 0:
                return False
            if sacrifice < min_sacrifice or sacrifice > max_sacrifice:
                print("Invalid sacrifice amount!")
                return False
            
            # Calculate reward scaling factor (higher sacrifice = higher reward)
            scaling = sacrifice / max_sacrifice # 0.0 to 1.0
            
            # Pay the health cost
            self._take_damage(player, sacrifice, sacrifice, "The powers that be accept your sacrifice... ")
            
            # Choose reward type based on sacrifice amount
            if random.random() < 0.2 + (scaling * 0.3): # 20-50% chance for special reward
                reward_type = 'special'
            elif random.random() < 0.5 + (scaling * 0.2): # 50-70% chance for major reward
                reward_type = 'major'
            elif random.random() < 0.7 + (scaling * 0.2): # 70-90% chance for minor reward
                reward_type = 'minor'
            else:
                reward_type = 'basic'
                
            # Grant reward based on type
            if reward_type == 'special':
                # Special rewards - rare/powerful items or significant permanent bonuses
                if random.random() < 0.5:
                    self._give_special_item(player, game, "The powers that be grant you an item of great power!")
                else:
                    print("Powerful energy surges through you, permanently enhancing one of your stats!")
                    self._permanent_stat_increase_specific(player, 5, ["attack", "defence", "evasion", "accuracy", "armour_penetration"])
            elif reward_type == 'major':
                # Major rewards, significant temporary buffs or valuable items
                if random.random() < 0.5:
                    print("The nearby energy surrounds you and empowers you!") 
                    print("Gain a significant temporary bonus to all stats!")
                    print("And a small permanent increase to one stat!")
                    buff_amount = int(15 + (scaling * 10)) # 15-25 stat boost
                    duration = int(10 + (scaling * 5)) # 10-15 turns
                    self._give_major_buff(player, buff_amount, buff_amount, duration, duration)
                    self._permanent_stat_increase(player)
                else:
                    gold_amount = int(100 + (scaling * 400)) # 100-500 gold
                    self._give_gold(player, gold_amount, gold_amount, "The powerful energy provides a golden reward and a strong piece of equipment!")
                    self._give_tier_equipment(player, game, player.level * 2)
            elif reward_type == 'minor':
                # Minor rewards, small buffs or random consumables
                if random.random() < 0.5:
                    print("The swirling energy provides a small temporary buff!")
                    buff_amount = int(5 + (scaling * 10)) # 5-15 stat boost
                    duration = int(5 + (scaling * 5)) # 5-10 turns
                    self._give_random_buff_specific(player, duration, duration, buff_amount, buff_amount,
                                                    ["attack", "defence", "evasion", "accuracy"])
                else:
                    gold_amount = int(50 + (scaling * 150)) # 50-200 gold
                    self._give_gold(player, gold_amount, gold_amount, "The energy provides a small financial boon!")
                    print("It also provides a couple of consumables!")
                    self._give_multiple_consumables_random(player, game, 2)
            else:
                # Give a basic piece of equipment
                print("The energy seems to sneer at you and spits out a piece of equipment at you! Hawk Tuah!")
                self._give_tier_equipment(player, game, player.level)
            return True
    
        except ValueError:
            print("Invalid input!")
            return False
    
    def _trigger_scaled_encounter(self, player, game, enemy_type=[]):
        """Trigger an encounter with a level-scaled enemy"""
        # Randomly choose between giving enemies
        enemy_type = random.choice(enemy_type)
        enemy = create_enemy(enemy_type, player)
        
        if enemy:
            print(f"A {enemy.name} materialises before you!")
            self._pause()
            if game.battle is None:
                game.initialise_battle()
            game.battle.battle(enemy)
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
    
    def _pause(self):
        input("Press Enter to continue...")