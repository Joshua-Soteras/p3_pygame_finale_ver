import pygame
import os
import math
from settings import *

class PowerUp(pygame.sprite.Sprite):
    """
    A power-up class that gives players special abilities!
    Students can customize power-up types, colors, and effects.
    """
    
    def __init__(self, x, y, powerup_type="speed", 
                 duration=DEFAULT_POWERUP_DURATION, 
                 size=30, color=None, image_path=None, speed=3):
        """
        Create a power-up!
        
        Parameters students can change:
        - x, y: Position of the power-up
        - powerup_type: Type of power-up ("speed", "jump", "fly", "double_shot", 
                       "invincible", "shrink", "slow_motion", "shield", "extra_life", "long_range")
        - duration: How long the effect lasts (seconds)
        - size: Size of the power-up
        - color: Color of the power-up (if no image)
        - image_path: Path to power-up image
        - speed: How fast power-up moves left
        """
        super(PowerUp, self).__init__()
        
        # Store power-up properties
        self.powerup_type = powerup_type
        self.duration = duration
        self.speed = speed
        self.size = size
        
        # Default colors for different power-up types
        self.default_colors = {
            "speed": GREEN,
            "jump": BLUE,
            "fly": CYAN,
            "double_shot": YELLOW,
            "invincible": PURPLE,
            "shrink": PINK,
            "slow_motion": ORANGE,
            "shield": WHITE,
            "extra_life": RED,
            "long_range": (0, 255, 128)
        }
        
        # Set color
        if color is None:
            color = self.default_colors.get(powerup_type, GREEN)
        
        # Create appearance
        self._create_appearance(size, color, image_path)
        
        # Position
        self.rect.x = x
        self.rect.y = y
        
        # Animation properties
        self.spawn_time = pygame.time.get_ticks()
        self.animation_offset = 0
        self.blink_start_time = None
        self.is_blinking = False
        self.visible = True
    
    def _create_appearance(self, size, color, image_path):
        """Create the power-up's visual appearance"""
        if image_path:
            try:
                if not os.path.isfile(image_path):
                    raise FileNotFoundError(f"File not found: {image_path}")
                self.surf = pygame.image.load(image_path).convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (size, size))
                self.rect = self.surf.get_rect()
            except Exception as e:
                print(f"[Warning] Could not load power-up image: {e}")
                print("Using colored circle instead.")
                self._create_default_appearance(size, color)
        else:
            self._create_default_appearance(size, color)
    
    def _create_default_appearance(self, size, color):
        """Create default circular power-up appearance"""
        self.surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, color, (size//2, size//2), size//2)
        # Add white border
        pygame.draw.circle(self.surf, WHITE, (size//2, size//2), size//2, 2)
        self.rect = self.surf.get_rect()
    
    def move_left(self):
        """Move the power-up to the left"""
        self.rect.x -= self.speed
    
    def is_off_screen(self):
        """Check if power-up has moved off screen"""
        return self.rect.right < 0
    
    def should_start_blinking(self):
        """Check if power-up should start blinking (about to disappear)"""
        current_time = pygame.time.get_ticks()
        time_on_screen = (current_time - self.spawn_time) / 1000.0
        disappear_time = 15  # Power-ups disappear after 15 seconds if not collected
        
        return time_on_screen >= (disappear_time - POWERUP_BLINK_WARNING)
    
    def should_disappear(self):
        """Check if power-up should disappear"""
        current_time = pygame.time.get_ticks()
        time_on_screen = (current_time - self.spawn_time) / 1000.0
        return time_on_screen >= 15  # Disappear after 15 seconds
    
    def start_blinking(self):
        """Start the blinking animation"""
        if not self.is_blinking:
            self.is_blinking = True
            self.blink_start_time = pygame.time.get_ticks()
    
    def update_animation(self):
        """Update power-up animation (floating and blinking)"""
        # Floating animation
        current_time = pygame.time.get_ticks()
        self.animation_offset = math.sin((current_time - self.spawn_time) * 0.005) * 3
        
        # Check if should start blinking
        if self.should_start_blinking():
            self.start_blinking()
        
        # Blinking animation
        if self.is_blinking:
            blink_time = (current_time - self.blink_start_time) / 200.0  # Blink every 200ms
            self.visible = int(blink_time) % 2 == 0
    
    def get_type(self):
        """Get the power-up type"""
        return self.powerup_type
    
    def get_duration(self):
        """Get the power-up duration"""
        return self.duration
    
    def get_position(self):
        """Get power-up position"""
        return (self.rect.x, self.rect.y + self.animation_offset)
    
    def set_speed(self, speed):
        """Change power-up movement speed"""
        self.speed = speed
    
    def update(self):
        """Update the power-up"""
        self.move_left()
        self.update_animation()
    
    def draw(self, screen):
        """Draw the power-up on screen"""
        if self.visible:  # Only draw if not blinking (invisible phase)
            # Draw with floating animation offset
            draw_rect = self.rect.copy()
            draw_rect.y += int(self.animation_offset)
            screen.blit(self.surf, draw_rect)