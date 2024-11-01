import os
import json
from datetime import datetime
from save_system import save_game, SAVE_DIRECTORY
from display import pause

class AutosaveManager:
    def __init__(self, game, autosave_frequency = 10):
        """Initialise the autosave manager.
        
        Args:
            game: Reference to the main game instance
            auto_save frequency: Number of turns between autosaves
        """
        self.game = game
        self.autosave_frequency = autosave_frequency
        self.turns_since_autosave = 0
        self.autosave_enabled = True
        self.autosaves_to_keep = 3
        
    def toggle_autosave(self):
        """Toggles autosave on/off."""
        self.autosave_enabled = not self.autosave_enabled
        status = "enabled" if self.autosave_enabled else "disabled"
        print(f"\nAutosave {status}.")
        pause()
        
    def increment_turn(self):
        """Increment turn counter and performs autosave if needed."""
        if not self.autosave_enabled:
            return
        
        self.turns_since_autosave += 1
        if self.turns_since_autosave >= self.autosave_frequency:
            self.perform_autosave()
            
    def perform_autosave(self):
        """Perform the autosave operation."""
        try:
            # Create autosave filename with player name
            autosave_name = f"autosave_{self.game.player.name}.json"
            
            # Create rotating backup of previous autosave
            self._rotate_autosaves(autosave_name)
            
            # Perform the save
            save_game(self.game.player, self.game.current_location, autosave_name)
            self.turns_since_autosave = 0
            print("\nGame autosaved.")
            
        except Exception as e:
            print(f"\nAutosave failed: {str(e)}")
            
    def _rotate_autosaves(self, current_save):
        """Maintain a rotating list of autosaves."""
        try:
            base_name = os.path.splitext(current_save)[0]
            
            # Get list of existing autosaves for this player
            existing_saves = [
                f for f in os.listdir(SAVE_DIRECTORY)
                if f.startswith(base_name) and f.endswith('.json')
            ]
            
            # Sort by creation time
            existing_saves.sort(
                key=lambda x: os.path.getctime(os.path.join(SAVE_DIRECTORY, x)),
                reverse=True
            )
            
            # Remove oldest saves if we have too many
            for old_save in existing_saves[self.autosaves_to_keep - 1:]:
                try:
                    os.remove(os.path.join(SAVE_DIRECTORY, old_save))
                except OSError:
                    continue
                    
            # Rename existing autosaves to make room for new one
            for i in range(min(len(existing_saves), self.autosaves_to_keep - 1)):
                old_path = os.path.join(SAVE_DIRECTORY, existing_saves[i])
                new_name = f"{base_name}_{i+1}.json"
                new_path = os.path.join(SAVE_DIRECTORY, new_name)
                try:
                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)
                except OSError:
                    continue
                    
        except Exception as e:
            print(f"\nError rotating autosaves: {str(e)}")