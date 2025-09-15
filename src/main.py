"""
Classroom Chaos - Desktop Game
Main entry point and game state management
"""
import pygame
import sys
from enum import Enum
from src.ui.main_menu import MainMenu
from src.ui.settings_menu import SettingsMenu
from src.game.game_screen import GameScreen
from src.game.game_over_screen import GameOverScreen

class GameState(Enum):
    MENU = "menu"
    SETTINGS = "settings"
    GAME = "game"
    GAME_OVER = "game_over"

class Game:
    def __init__(self):
        pygame.init()
        
        # Constants
        self.WINDOW_WIDTH = 450
        self.WINDOW_HEIGHT = 800
        self.FPS = 60
        self.PRIMARY_COLOR = (238, 108, 43)  # #ee6c2b
        self.TEXT_COLOR = (24, 19, 17)  # #181311
        self.GRAY_COLOR = (107, 114, 128)  # gray-500
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Classroom Chaos")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.MENU
        self.running = True
        self.settings = {
            'difficulty': 'Normal',
            'sound_enabled': True
        }
        self.game_score = 0
        
        # Initialize screens
        self.main_menu = MainMenu(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.settings_menu = SettingsMenu(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.game_screen = GameScreen(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.game_over_screen = GameOverScreen(self.screen, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        
    def handle_events(self):
        """Handle pygame events and delegate to current screen"""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            # Handle state transitions based on current screen
            if self.state == GameState.MENU:
                result = self.main_menu.handle_event(event)
                if result == "play":
                    self.state = GameState.GAME
                    self.game_screen.reset()
                elif result == "settings":
                    self.state = GameState.SETTINGS
                    
            elif self.state == GameState.SETTINGS:
                result = self.settings_menu.handle_event(event)
                if result == "back":
                    self.state = GameState.MENU
                elif result == "settings_changed":
                    # Update game settings
                    self.settings.update(self.settings_menu.get_settings())
                    self.game_screen.update_settings(self.settings)
                    
            elif self.state == GameState.GAME:
                result = self.game_screen.handle_event(event)
                if result == "game_over":
                    self.game_score = self.game_screen.get_score()
                    self.state = GameState.GAME_OVER
                    self.game_over_screen.set_score(self.game_score)
                elif result == "back_to_menu":
                    self.state = GameState.MENU
                    
            elif self.state == GameState.GAME_OVER:
                result = self.game_over_screen.handle_event(event)
                if result == "play_again":
                    self.state = GameState.GAME
                    self.game_screen.reset()
                elif result == "main_menu":
                    self.state = GameState.MENU
    
    def update(self):
        """Update current screen"""
        if self.state == GameState.MENU:
            self.main_menu.update()
        elif self.state == GameState.SETTINGS:
            self.settings_menu.update()
        elif self.state == GameState.GAME:
            self.game_screen.update()
        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.update()
    
    def draw(self):
        """Draw current screen"""
        self.screen.fill((255, 255, 255))  # White background
        
        if self.state == GameState.MENU:
            self.main_menu.draw()
        elif self.state == GameState.SETTINGS:
            self.settings_menu.draw()
        elif self.state == GameState.GAME:
            self.game_screen.draw()
        elif self.state == GameState.GAME_OVER:
            self.game_over_screen.draw()
            
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()