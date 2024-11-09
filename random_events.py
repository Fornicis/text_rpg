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
        ))"""
        
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
        
        """events.append(RandomEvent(
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
            {"min_level": 4, "location_type": ["Forest", "Deepwoods", "Plains", "Mountain", "Swamp", "Desert", "Toxic Swamp", "Valley", "Mountain Peaks", "Scorching Valley", "Death Caves", "Death Valley", "Volcanic Valley"]}
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
            {"min_level": 5, "location_type": ["Desert", "Plains", "Mountain", "Valley", "Death Valley", "Shadowed Valley", "Scorching Plains"]}
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
                "min level": 8, "location_type": ["Ruins", "Temple", "Ancient Ruins", "Death Caves", "Heavens"]
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
        ))"""
        
        return events

    def trigger_random_event(self, player, game):
        """Attempt to trigger an event"""
        # 15% chance for a random event
        if random.random() < 1.0:
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
        outcomes = [
            (0.5, lambda: self._heal_player(player, 0.15)),
            (0.5, lambda: self._restore_stamina(player, 0.15))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_shrine_desecrate(self, player, game):
        """Desecrate the shrine"""
        outcomes = [
            (0.5, lambda: self._take_damage(player, 30, "The god whose shrine this is smites you for your unholy act!")),
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
                (0.1, lambda: (print("The confusing echoes disorient you! Accuracy -10 until end of next combat!"), player.apply_debuff("accuracy", 10)))
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
            (0.1, lambda: self._permanent_stat_increase_specific(player, "accuracy", 1))
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
            (0.6, lambda: self._take_damage(player, 10, 20, "That was probably not a smart idea..."))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
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
        print(f"{message} You take {damage} damage!")
        
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
    
    def _permanent_stat_increase_specific(self, player, stat, value):
        """Give a small increase to chosen stat"""
        setattr(player, stat, getattr(player, stat) + value)
        print(f"You feel permanently strengthened! {stat.title()} increased by {value}!")
        
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