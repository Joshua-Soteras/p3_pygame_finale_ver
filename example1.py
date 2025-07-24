import pygame
import sys
from create_Shape import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Project")

# Clock to control frame rate
clock = pygame.time.Clock()

blockOne = shapeOne = Shape(x = 100, y = 100 , height= 50, width= 50, color = "red" , shape_type = "rectangle")

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state here

    # Draw everything
    screen.fill((0, 0, 0))  # Fill the screen with black
    blockOne.draw(screen)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
