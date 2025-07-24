import pygame
import sys
from player import Player
from platform_manager import PlatformManager
from enemy_manager import EnemyManager
from powerup_manager import PowerUpManager
from game_over import GameOverScreen
from event_handler import handle_events, handle_game_events
from settings import *
from create_shapes import *

class Game:
    """
    Main game class - Students can easily customize their game here!
    """
    
    def __init__(self):
        """Set up the game"""
        pygame.init()
        # Create the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game - WASD/Arrows: Move | K: Shoot | TAB: Difficulty")
        # Game clock for smooth animation
        self.clock = pygame.time.Clock()
        # Game state
        self.game_state = "playing"  # "playing", "game_over"
        self.running = True
        
        # Create game objects
        self._create_game_objects()
        
# SECTION 1---------------------------------------------------------------
    def _create_game_objects(self):

        self.shapeOne = Shape(x = 100, y = 100 ,height= 50, width= 50, color = "red" , shape = "rectangle")
        

    def update(self):
        """Update game based on current state"""
        # Collect all events once to avoid conflicts
        events = pygame.event.get()

    def draw_playing(self):
 
        # Clear screen with black
        self.screen.fill(BLACK)
        self.shapeOne.draw(self.screen)



## SECTION 2 ---------
    def draw(self):
        """Draw everything based on current state"""
        if self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        
        while self.running:
            self.update()
            self.draw()
        
        # Clean up
        pygame.quit()
        sys.exit()

# This is what runs when students start the game
def main():
    """Start the game!"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
