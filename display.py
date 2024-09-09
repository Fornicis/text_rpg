import os
import platform

def clear_screen():
    #Clears the console screen based on the operating system.
    os.system('cls' if platform.system() in ['Win64', 'Windows'] else 'clear')

def pause():
    #Pauses the game until the user presses Enter.
    input("\nPress Enter to continue...")
    
def display_title():
    clear_screen()
    print("""
    ╔═══════════════════════════════════════════╗
    ║             TEXT RPG ADVENTURE            ║
    ║                                           ║
    ║              © Fornicis, 2024             ║
    ╚═══════════════════════════════════════════╝
    """)

def display_help():
    clear_screen()
    print("""
    === HELP ===
    
    Welcome to Text RPG Adventure!
    
    BASIC GAMEPLAY:
    - You start in the Village, which serves as your home base.
    - Explore different areas, battle monsters, and collect loot to level up.
    - Your goal is to become strong enough to face the ultimate challenges.

    NAVIGATION:
    - Use the [m]ove command to travel between connected areas.
    - Some areas have level requirements to enter.
    - Use numbers, name, or first few characters of area to move to it.
    - Use the [v]iew map command to see the world layout.

    COMBAT:
    - Battles are turn-based. You can:
      [a]ttack: Deal damage to the enemy
      [u]se item: Use a consumable from your inventory
      [r]un: Attempt to flee (not always successful)
    - Defeating enemies grants EXP and sometimes loot.

    INVENTORY AND EQUIPMENT:
    - Access your [i]nventory to see your items.
    - Use the [e]quip command to manage your gear.
    - [c]onsumables can be viewed separately for quick access.

    SHOP:
    - Visit the shop in the Village to buy and sell items.
    - To sell items just enter the number associated with the item.
    - Multiple items can be bought/sold at once, simple enter the numbers seperated by a space.
    - The shop's inventory changes periodically.

    SAVING AND LOADING:
    - Use the [sa]ve game command to save your progress.
    - You can load your game from the main menu.

    OTHER COMMANDS:
    - [r]est: Restore some HP (only in the Village)
    - [u]se item: Use a consumable item
    - [l]ocation actions: Perform actions specific to your current location

    TIPS:
    - Pay attention to your HP, EXP, and gold.
    - Upgrade your equipment regularly.
    - Save your game often to avoid losing progress.
    - Explore new areas as you level up, but be cautious of tough enemies.

    Remember, most actions can be performed by typing the letter in brackets, 
    e.g., 'm' for move, 'i' for inventory, etc.

    Good luck on your adventure!
    """)
    input("Press Enter to return to the main menu...")
    
def title_screen():
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