import os
import platform

def clear_screen():
    #Clears the console screen based on the operating system.
    os.system('cls' if platform.system() in ['Win64', 'Windows'] else 'clear')

def pause():
    #Pauses the game until the user presses Enter.
    input("\nPress Enter to continue...")
    
def display_title():
    #Displays the games title screen
    clear_screen()
    print("""
    ╔═══════════════════════════════════════════╗
    ║             TEXT RPG ADVENTURE            ║
    ║                                           ║
    ║              © Fornicis, 2024             ║
    ╚═══════════════════════════════════════════╝
    """)

def display_help():
    #Displays the help menu with game instructions
    clear_screen()
    print("""
    === TEXT RPG ADVENTURE HELP ===
    
    Welcome, brave adventurer! This guide will help you navigate your journey.
    
    GAME BASICS:
    - Your adventure begins in the Village, your home base.
    - Explore various locations, battle monsters, and collect loot to level up.
    - Your goal is to become strong enough to face the ultimate challenges in the Heavens.
    - You have 5 respawns granted by the deities in the Heavens, after your fifth one, it's game over.

    NAVIGATION:
    - Use the [m]ove command to travel between connected areas.
    - Some areas have level requirements to enter.
    - Use the [v]iew map command to see the world layout and available paths.

    COMBAT:
    - Battles are turn-based. Your options are:
      [a]ttack: Deal damage to the enemy (costs stamina based on weapon type)
      [u]se item: Use a consumable from your inventory
      [r]un: Attempt to flee (not always successful)
    - Defeating enemies grants EXP, gold, and sometimes loot.
    - Your stamina replenishes on level up and resting, it is used for attacks.

    INVENTORY AND EQUIPMENT:
    - Access your [i]nventory to see all your items.
    - Use the [e]quip command to manage your gear.
    - [c]onsumables can be viewed separately for quick access.
    - Equip better gear to increase your attack and defense stats.

    SHOPS:
    - Visit shops in the Village to buy and sell items:
      - [ar]mourer: Buy and sell weapons and armor
      - [a]lchemist: Buy and sell potions and consumables
      - [in]n: Rest to restore HP and stamina, buy food and drinks
    - Shop inventories change periodically, so check back often.

    CHARACTER PROGRESSION:
    - Gain EXP by defeating enemies. Level up to increase your stats.
    - Higher levels unlock access to new areas with stronger enemies and better loot.

    CONSUMABLES AND BUFFS:
    - Use healing potions to restore HP during and outside of combat.
    - Buff items can temporarily increase your stats.
    - Food and drinks can restore stamina and provide various effects.

    SAVING AND LOADING:
    - Use the [sa]ve game command to save your progress.
    - Load your game from the main menu when starting the game.

    TIPS:
    - Rest at the Inn or use the [r]est command anywhere (reduced effectiveness) to restore HP and stamina.
    - Upgrade your equipment regularly to stay competitive.
    - Use the right weapon type for your playstyle (light, medium, or heavy).
    - Always carry healing items for tough battles.
    - Explore new areas as you level up, but be cautious of tough enemies.

    Remember, most actions can be performed by typing the letter in brackets, 
    e.g., 'm' for move, 'i' for inventory, etc.

    Good luck on your adventure!
    """)
    input("Press Enter to return to the main menu...")
    
def title_screen():
    #Displays the title screen and handles main menu options
    while True:
        display_title()
        print("\n    1. Play")
        print("    2. Load Game")
        print("    3. Help")
        print("    4. Quit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            return "new_game"
        elif choice == '2':
            return "load_game"
        elif choice == '3':
            display_help()
        elif choice == '4':
            print("Thanks for playing! Goodbye.")
            exit()
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")
            
