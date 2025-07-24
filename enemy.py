import pygame
import os
from settings import *

class Enemy(pygame.sprite.Sprite):
    """
    A simple enemy class for the game!
    Students can customize enemy speed, size, color, and appearance.
    """
    
    def __init__(self, x, y, speed=DEFAULT_ENEMY_SPEED, 
                 width=40, height=40, color=RED, image_path=None):
        """
        Create an enemy!
        
        Parameters students can change:
        - x, y: Starting position
        - speed: How fast the enemy moves left
        - width, height: Size of the enemy
        - color: Color of the enemy (if no image)
        - image_path: Path to enemy image file (optional)
        """
        super(Enemy, self).__init__()
        
        # Store student-friendly settings
        self.speed = speed
        self.original_speed = speed
        
        # Create enemy appearance
        self._create_appearance(width, height, color, image_path)
        
        # Set position after creating the surface
        self.rect.x = x
        self.rect.y = y
    
    def _create_appearance(self, width, height, color, image_path):
        """Create the enemy's visual appearance"""
        if image_path:
            try:
                if not os.path.isfile(image_path):
                    raise FileNotFoundError(f"File not found: {image_path}")
                self.surf = pygame.image.load(image_path).convert_alpha()
                # Scale image to desired size
                self.surf = pygame.transform.scale(self.surf, (width, height))
                self.rect = self.surf.get_rect()
            except Exception as e:
                print(f"[Warning] Could not load enemy image: {e}")
                print("Using colored rectangle instead.")
                self.surf = pygame.Surface((width, height))
                self.surf.fill(color)
                self.rect = self.surf.get_rect()
        else:
            self.surf = pygame.Surface((width, height))
            self.surf.fill(color)
            self.rect = self.surf.get_rect()
    
    def move_left(self):
        """Move the enemy to the left"""
        self.rect.x -= self.speed
    
    def set_speed(self, speed):
        """Change the enemy's movement speed"""
        self.speed = speed
    
    def is_off_screen(self):
        """Check if enemy has moved off the left side of screen"""
        return self.rect.right < 0
    
    def get_position(self):
        """Get enemy position (x, y)"""
        return (self.rect.x, self.rect.y)
    
    def get_size(self):
        """Get enemy size (width, height)"""
        return (self.rect.width, self.rect.height)
    
    def update(self):
        """Update the enemy (move it left)"""
        self.move_left()
    
    def draw(self, screen):
        """Draw the enemy on screen"""
        screen.blit(self.surf, self.rect)