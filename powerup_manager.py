import pygame
import random
from powerup import PowerUp
from settings import *

class PowerUpManager:
    """
    Manages all power-ups in the game.
    Students can easily control which power-ups spawn and how often.
    """
    
    def __init__(self, screen_width, screen_height, 
                 spawn_rate=DEFAULT_POWERUP_SPAWN_RATE,
                 enabled_powerups=None, powerup_images=None):
        """
        Create a power-up manager!
        
        Parameters students can change:
        - spawn_rate: Seconds between power-up spawns
        - enabled_powerups: List of power-up types to enable
        - powerup_images: Dictionary of power-up type -> image path
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.spawn_rate = spawn_rate
        
        # Power-up group (only one active at a time)
        self.powerups = pygame.sprite.Group()
        self.active_powerup = None
        
        # Spawning control
        self.last_spawn_time = pygame.time.get_ticks()
        
        # Available power-up types
        self.all_powerup_types = [
            "speed",        # 2x movement speed
            "jump",         # 1.5x jump power
            "fly",          # Remove gravity, move up/down
            "double_shot",  # Twice as fast shooting
            "invincible",   # Can't be hurt by enemies
            "shrink",       # Smaller player hitbox
            "slow_motion",  # Everything moves slower
            "shield",       # Protects from one enemy hit
            "extra_life",   # Gives an extra life
            "long_range"    # Bullets travel farther
        ]
        
        # Set enabled power-ups
        if enabled_powerups is None:
            self.enabled_powerups = self.all_powerup_types.copy()
        else:
            self.enabled_powerups = enabled_powerups
        
        # Power-up images
        self.powerup_images = powerup_images if powerup_images else {}
        
        # Ground level for spawning (on platforms)
        self.ground_level = screen_height - 80
    
    def set_enabled_powerups(self, powerup_list):
        """Set which power-ups can spawn"""
        self.enabled_powerups = powerup_list
    
    def enable_powerup(self, powerup_type):
        """Enable a specific power-up type"""
        if powerup_type in self.all_powerup_types and powerup_type not in self.enabled_powerups:
            self.enabled_powerups.append(powerup_type)
    
    def disable_powerup(self, powerup_type):
        """Disable a specific power-up type"""
        if powerup_type in self.enabled_powerups:
            self.enabled_powerups.remove(powerup_type)
    
    def set_spawn_rate(self, spawn_rate):
        """Change how often power-ups spawn"""
        self.spawn_rate = spawn_rate
    
    def set_powerup_image(self, powerup_type, image_path):
        """Set custom image for a power-up type"""
        self.powerup_images[powerup_type] = image_path
    
    def should_spawn_powerup(self):
        """Check if it's time to spawn a new power-up"""
        # Only spawn if no power-up is currently active
        if len(self.powerups) > 0:
            return False
        
        current_time = pygame.time.get_ticks()
        time_since_last_spawn = (current_time - self.last_spawn_time) / 1000.0
        
        return time_since_last_spawn >= self.spawn_rate
    
    def spawn_powerup(self, platform_manager):
        """Spawn a new power-up on a ground platform"""
        if not self.enabled_powerups:
            return  # No power-ups enabled
        
        # Find ground platforms to spawn on
        ground_platforms = []
        for platform in platform_manager.get_platforms():
            if (platform.platform_type == "ground" and 
                platform.rect.x > 0 and 
                platform.rect.x < self.screen_width + 200):
                ground_platforms.append(platform)
        
        if not ground_platforms:
            return  # No suitable platforms
        
        # Choose random platform and power-up type
        platform = random.choice(ground_platforms)
        powerup_type = random.choice(self.enabled_powerups)
        
        # Spawn position (on top of platform)
        spawn_x = platform.rect.x + random.randint(20, platform.rect.width - 50)
        spawn_y = platform.rect.top - 35  # Just above platform
        
        # Get image path if available
        image_path = self.powerup_images.get(powerup_type, None)
        
        # Create power-up
        powerup = PowerUp(
            x=spawn_x,
            y=spawn_y,
            powerup_type=powerup_type,
            image_path=image_path,
            speed=platform_manager.current_platform_speed  # Match platform speed
        )
        
        self.powerups.add(powerup)
        self.last_spawn_time = pygame.time.get_ticks()
    
    def get_powerups(self):
        """Get all power-ups for collision detection"""
        return self.powerups
    
    def remove_powerup(self, powerup):
        """Remove a specific power-up (when collected)"""
        if powerup in self.powerups:
            self.powerups.remove(powerup)
    
    def clear_all_powerups(self):
        """Remove all power-ups (for game reset)"""
        self.powerups.empty()
    
    def get_powerup_count(self):
        """Get number of active power-ups"""
        return len(self.powerups)
    
    def update(self, platform_manager):
        """Update all power-ups and spawn new ones"""
        # Update all power-ups
        self.powerups.update()
        
        # Remove off-screen or expired power-ups
        for powerup in self.powerups.copy():
            if powerup.is_off_screen() or powerup.should_disappear():
                self.powerups.remove(powerup)
        
        # Spawn new power-ups
        if self.should_spawn_powerup():
            self.spawn_powerup(platform_manager)
    
    def draw(self, screen):
        """Draw all power-ups"""
        for powerup in self.powerups:
            powerup.draw(screen)