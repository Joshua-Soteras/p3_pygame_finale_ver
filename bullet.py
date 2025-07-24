import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    """
    A simple bullet class for the player to shoot enemies!
    Students can customize bullet speed, size, and color.
    """
    
    def __init__(self, x, y, speed=DEFAULT_BULLET_SPEED, 
                 bullet_range=DEFAULT_BULLET_RANGE, 
                 width=8, height=4, color=YELLOW):
        """
        Create a bullet!
        
        Parameters students can change:
        - x, y: Starting position
        - speed: How fast the bullet travels
        - bullet_range: How far the bullet can travel
        - width, height: Size of the bullet
        - color: Color of the bullet
        """
        super(Bullet, self).__init__()
        
        # Store student-friendly settings
        self.speed = speed
        self.bullet_range = bullet_range
        self.start_x = x
        
        # Create bullet appearance
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def move(self):
        """Move the bullet to the right"""
        self.rect.x += self.speed
    
    def is_off_screen(self):
        """Check if bullet has moved off screen or reached max range"""
        return (self.rect.left > SCREEN_WIDTH or 
                self.rect.x - self.start_x > self.bullet_range)
    
    def get_position(self):
        """Get bullet position (x, y)"""
        return (self.rect.x, self.rect.y)
    
    def set_speed(self, speed):
        """Change bullet speed"""
        self.speed = speed
    
    def update(self):
        """Update the bullet (move it)"""
        self.move()
    
    def draw(self, screen):
        """Draw the bullet on screen"""
        screen.blit(self.surf, self.rect)