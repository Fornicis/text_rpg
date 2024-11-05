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
        outcomes = [
            (0.4, lambda: self._give_random_consumable(player, game, player.level)),
            (0.3, lambda: self._give_gold(player, 20, 50)),
            (0.2, lambda: self._give_tier_equipment(player, game)),
            (0.1, lambda: print("Unfortunately, you find nothing of value."))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_hidden_cache_quick(self, player, game):
        """Quickly grab from the hidden cache"""
        outcomes = [
            (0.3, lambda: self._give_tier_equipment(player, game)),
            (0.3, lambda: self._give_gold(player, 50, 100)),
            (0.4, lambda: self._take_damage(player, 5, 15, "You trigger a nasty trap!"))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_traveller_accept(self, player, game):
        """Accept the travellers offer"""
        exp_gain = random.randint(10, 25) * player.level
        print(f"The traveller imparts his ancient wisdom upon you. You gain {exp_gain} experience!")
        player.gain_exp(exp_gain, player.level)
        
    def _outcome_traveller_chat(self, player, game):
        """Have a chat with the traveller"""
        gold_gain = random.randint(10, 20) * player.level
        player.gold += gold_gain
        print(f"The traveller enjoys having a conversation with you. He generously gives you {gold_gain} gold as a gift!")
        
    def _outcome_merchant_trade(self, player, game):
        """Trade gold for potentially valuable items"""
        trade_cost = player.gold // 2
        if trade_cost < 10:
            print("The merchant doesn't think you can afford their wares...Peasunt")
            return
        
        outcomes = [
            (0.3, lambda: self._give_multiple_consumables(player, game, 2)),
            (0.3, lambda: self._give_tier_equipment(player, game, player.level)),
            (0.2, lambda: self._give_gold(player, trade_cost * 2, trade_cost * 3)),
            (0.2, lambda: self._give_special_item(player, game))
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
                (0.6, lambda: self._give_tier_equipment(player, game, player.level + 1)),
                (0.4, lambda: self._give_multiple_consumables(player, game, 3))
            ]
        else:
            outcomes = [
                (0.4, lambda: self._give_random_consumable(player, game, player.level)),
                (0.4, lambda: self._give_tier_equipment(player, game, player.level)),
                (0.2, lambda: self._give_gold(player, traded_item.value * 2, traded_item.value * 3))
            ]
            
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_merchant_guard(self, player, game):
        """Help guard the merchant's caravan"""
        if player.stamina < (player.max_stamina * 0.8):
            print("You're too tired to help guard the caravan.")
            return
    
        player.stamina = 0 # Exhaust stamina
        
        outcomes = [
            (0.4, lambda: self._give_gold(player, 100, 200)),
            (0.3, lambda: self._give_multiple_consumables(player, game, 2)),
            (0.2, lambda: self._give_merchant_favour(player)),
            (0.1, lambda: self._give_tier_equipment(player, game, player.level + 1))
        ]
        
        print("You spend time helping guard the merchant's caravan...")
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_training_combat(self, player, game):
        """Practice combat at the ancient training grounds"""
        stamina_cost = player.max_stamina // 2
        if player.stamina < stamina_cost:
            print("You are too tired to train effectively")
            return
        
        player.stamina -= stamina_cost
        
        # Give combat focused buffs
        buff_choices = [
            ("attack", 15),
            ("accuracy", 30),
            ("crit_chance", 10),
            ("crit_damage", 20),
        ]
        
        # Apply 2 random buffs
        for _ in range(2):
            stat, value = random.choice(buff_choices)
            duration = random.randint(5, 10)
            player.apply_buff(stat, value, duration, combat_only=False)
            
        exp_gain = random.randint(20, 40) * player.level
        player.gain_exp(exp_gain, player.level)
        print(f"Your combat training yields great results! Gained {exp_gain} experience!")
        
    def _outcome_training_study(self, player, game):
        """Study ancient combat techniques"""
        stamina_cost = player.max_stamina // 4
        if player.stamina < stamina_cost:
            print("You're too tired to study effectively")
            return
        
        # Give defensive buffs
        buff_choices = [
            ("defence", 15),
            ("evasion", 15),
            ("block_chance", 10),
            ("damage_reduction", 10)
        ]
        
        # Apply 2 random buffs
        for _ in range(2):
            stat, value = random.choice(buff_choices)
            duration = random.randint(5, 10)
            player.apply_buff(stat, value, duration, combat_only=False)
            
        exp_gain = random.randint(15, 30) * player.level
        player.gain_exp(exp_gain, player.level)
        print(f"You learn valuable defensive techniques! Gained {exp_gain} experience!")
        
    def _outcome_training_search(self, player, game):
        """Search the training grounds for equipment"""
        if random.random() < 0.6:
            self._give_tier_equipment(player, game, player.level)
        else:
            self._give_multiple_consumables(player, game, 2)
            
    def _outcome_training_rest(self, player, game):
        """Rest at the training grounds"""
        heal_amount = player.max_hp // 2
        stamina_amount = player.max_stamina // 2
        player.heal(heal_amount)
        player.restore_stamina(stamina_amount)
        print(f"You rest at the ancient training grounds. Restored {heal_amount} HP and {stamina_amount} stamina!")
        
    def _outcome_spring_drink(self, player, game):
        """Drink from the magical spring"""
        outcomes = [
            (0.3, lambda: self._full_heal_player(player)),
            (0.3, lambda: self._give_major_buff(player)),
            (0.2, lambda: self._permanent_stat_increase(player)),
            (0.2, lambda: self._temporary_max_increase(player))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_spring_meditate(self, player, game):
        """Meditate besides the spring"""
        # Restore resources
        player.hp = player.max_hp
        player.stamina = player.max_stamina
        
        # Give exp bonus
        exp_gain = random.randint(25, 50) * player.level
        player.gain_exp(exp_gain, player.level)
        print(f"Your meditation leaves you fully restored and enlightened! Gained {exp_gain} experience!")
        
    def _outcome_spring_fill(self, player, game):
        """Fill containers with spring water"""
        # Give healing potions
        potions = [item for item in game.items.values()
                   if item.type == "consumable" and item.effect_type == "healing"
                   and self._is_appropriate_tier(item, player.level)]
        
        if potions:
            num_potions = random.randint(2, 4)
            for _ in range(num_potions):
                potion = random.choice(potions)
                player.add_item(potion)
                print(f"You acquire {potion.name}.")
            print(f"You manage to fill {num_potions} containers with magical water!")
            
    def _outcome_spring_wade(self, player, game):
        """Wade in the magical spring"""
        # Remove all negative effects
        player.status_effects = [effect for effect in player.status_effects
                                 if not effect.is_debuff]
        
        # Give temporary bonus
        buff_duration = random.randint(10, 20)
        player.apply_buff("all stats", 5, buff_duration, combat_only=False)
        print("The magical water cleanses and empowers you!")
        
    # Neutral Events
    
    def _outcome_shrine_offer(self, player, game):
        """Make an offering to the shrine"""
        if player.gold >= 10:
            player.gold -= 10
            outcomes = [
                (0.4, lambda: self._give_random_buff(player)),
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
            (0.1, lambda: self._give_tier_equipment(player, game)),
            (0.1, lambda: print("Nothing happens, but you do feel guilty."))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_help_adventurer(self, player, game):
        """Help the lost adventurer"""
        if random.random() < 0.7:
            print("The grateful adventurer shares some supplies with you!")
            self._give_random_consumable(player, game, player.level)
        else:
            exp_gain = random.randint(5, 15) * player.level
            print(f"The adventurer shares some valuable knowledge. You gain {exp_gain} experience!")
            player.gain_exp(exp_gain, player.level)
            
    def _outcome_ask_adventurer(self, player, game):
        """Ask the adventurer for information"""
        player.add_visited_location(random.choice(game.world_map.get_all_locations()))
        print("The adventurer marks an interesting location on your map!")
        
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
            self._restore_stamina(10)
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
            player.stamina = max(0, player.stamina - 10)
        else:
            self._take_damage(player, 5, 10, "Despite your best efforts you disturb some spores and inhale them...")
            
    def _outcome_mushroom_eat(self, player, game):
        """Eat a mysterious mushroom...weirdo"""
        outcomes = [
            (0.3, lambda: self._heal_player(player, 0.5)),
            (0.3, lambda: self._restore_stamina(player, 0.5)),
            (0.4, lambda: self._take_damage(player, 10, 20, "That was probably not a smart idea..."))
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
            
    def _give_random_consumable(self, player, game, level):
        """Gives player a random consumable"""
        consumables = [item for item in game.items.values()
                       if item.type in ["consumable", "food", "drink"]
                       and self._is_appropriate_tier(item, level)]
        if consumables:
            item = random.choice(consumables)
            player.add_item(item)
            print(f"You acquired a {item.name}")
     
    def _give_multiple_consumables(self, player, game, count):
        """Give multiple random consumables"""
        for _ in range(count):
            self._give_random_consumable(player, game, player.level)
            
    def _give_tier_equipment(self, player, game, level):
        """Gives player a random piece of equipment appropriate to level"""
        equipment = [item for item in game.items.values()
                     if item.type in ["weapon", "helm", "chest", "legs", "boots", "gloves", "shield", "ring"]
                     and self._is_appropriate_tier(item, level)]
        if equipment:
            item = random.choice(equipment)
            player.add_item(item)
            print(f"You gained a {item.name}")
    
    def _give_special_item(self, player, game):
        """Gives a special rare item"""
        special_items = [item for item in game.items.values()
                         if item.tier in ["masterwork", "legendary"]]
        
        if special_items:
            item = random.choice(special_items)
            player.add_item(item)
            print(f"The merchant gives you something special: {item.name}!")
            
    def _give_merchant_favour(self, player):
        """Give gold and exp for helping merchant"""
        gold = random.randint(150, 300)
        exp = random.randint(30, 60) * player.level
        player.gold += gold
        player.gain_exp(exp, player.level)
        print(f"The merchant rewards you with {gold} gold and valuable knowledge! (No lamborghini though)")
            
    def _give_gold(self, player, min_amount, max_amount):
        """Give player some gold"""
        amount = random.randint(min_amount, max_amount)
        player.gold += amount
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
        
    def _take_damage(self, player, min_damage, max_damage, message):
        """Deal damage to player"""
        damage = random.randint(min_damage, max_damage)
        player.take_damage(damage)
        print(f"{message} You take {damage} damage!")
        
    def _give_random_buff(self, player):
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
    
    def _give_major_buff(self, player):
        """Give a significant temporary buff"""
        buff_duration = random.randint(15, 30)
        buff_amount = random.randint(20, 40)
        player.apply_buff("all stats", buff_amount, buff_duration, combat_only=False)
        print(f"You feel incredibly empowered! All stats increased by {buff_amount} for {buff_duration} turns!")
    
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
            ("max_hp", 10),
            ("base_attack", 2),
            ("base_defence", 2),
            ("base_evasion", 1),
            ("base_accuracy", 4),
            ("max_stamina", 5)
        ]
        stat, amount = random.choice(stat_choices)
        setattr(player, stat, getattr(player, stat) + amount)
        print(f"You feel permanently strengthened! {stat.replace('_', ' ').title()} increased by {amount}!")
        
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
        return tier_levels.get(item.tier, 0) <= level