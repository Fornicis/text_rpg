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
            (0.4, lambda: self._give_random_consumable(player, game)),
            (0.3, lambda: self._give_gold(player, 20, 50)),
            (0.2, lambda: self._give_random_equipment(player, game)),
            (0.1, lambda: print("Unfortunately, you find nothing of value."))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_hidden_cache_quick(self, player, game):
        """Quickly grab from the hidden cache"""
        outcomes = [
            (0.3, lambda: self._give_random_equipment(player, game)),
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
            (0.1, lambda: self._give_random_equipment(player, game)),
            (0.1, lambda: print("Nothing happens, but you do feel guilty."))
        ]
        self._resolve_weighted_outcome(outcomes, player)
        
    def _outcome_help_adventurer(self, player, game):
        """Help the lost adventurer"""
        if random.random() < 0.7:
            print("The grateful adventurer shares some supplies with you!")
            self._give_random_consumable(player, game)
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
            self._give_random_consumable(player, game)
        else:
            self._take_damage(player, 5, 15, "In your haste you disturb some spores and inhale them...")
            
    def _outcome_mushroom_harvest(self, player, game):
        """Slowly and carefully harvest the mushrooms"""
        if random.random() < 0.8:
            print("You take your time and manage to harvest some useful reagents, this has been tiring work!")
            self._give_random_consumable(player, game)
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
            
    def _give_random_consumable(self, player, game):
        """Gives player a random consumable"""
        consumables = [item for item in game.items.values()
                       if item.type in ["consumable", "food", "drink"]]
        if consumables:
            item = random.choice(consumables)
            player.add_item(item)
            print(f"You found a {item.name}")
            
    def _give_random_equipment(self, player, game):
        """Gives player a random piece of equipment"""
        equipment = [item for item in game.items.values()
                     if item.type in ["weapon", "helm", "chest", "legs", "boots", "gloves", "shield", "ring"]]
        if equipment:
            item = random.choice(equipment)
            player.add_item(item)
            print(f"You found a {item.name}")
            
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