import pygame
import random
from enemy import Enemy
from settings import *

class EnemyManager:
    """
    Manages all enemies in the game.
    Students can easily control enemy spawning and difficulty.
    """
    
    def __init__(self, screen_width, screen_height, 
                 enemy_speed=DEFAULT_ENEMY_SPEED, 
                 spawn_rate=DEFAULT_ENEMY_SPAWN_RATE,
                 spawn_increase_time=ENEMY_SPAWN_INCREASE_TIME,
                 enemy_image_path=None):
        """
        Create an enemy manager!
        
        Parameters students can change:
        - enemy_speed: How fast enemies move (1=slow, 8=fast)
        - spawn_rate: Seconds between enemy spawns
        - spawn_increase_time: Seconds before spawn rate increases
        - enemy_image_path: Path to enemy image file
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemy_speed = enemy_speed
        self.spawn_rate = spawn_rate  # seconds
        self.spawn_increase_time = spawn_increase_time
        self.enemy_image_path = enemy_image_path
        
        # Enemy group
        self.enemies = pygame.sprite.Group()
        
        # Spawning control
        self.last_spawn_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        
        # Ground level for spawning (above base platforms)
        self.ground_level = screen_height - 80  # Just above ground platforms
        self.spawn_height_range = 200  # How high above ground enemies can spawn
        
        # Enemy colors (if no image provided)
        self.enemy_colors = [RED, PURPLE, ORANGE, (150, 0, 0), (180, 0, 180)]
    
    def should_spawn_enemy(self):
        """Check if it's time to spawn a new enemy"""
        current_time = pygame.time.get_ticks()
        time_since_last_spawn = (current_time - self.last_spawn_time) / 1000.0
        
        # Calculate current spawn rate (gets faster over time)
        time_elapsed = (current_time - self.start_time) / 1000.0
        spawn_multiplier = 1 + (time_elapsed / self.spawn_increase_time) * 0.5
        current_spawn_rate = self.spawn_rate / spawn_multiplier
        
        # Minimum spawn rate (don't spawn too fast)
        current_spawn_rate = max(current_spawn_rate, 1.0)
        
        return time_since_last_spawn >= current_spawn_rate
    
    def spawn_enemy(self):
        """Spawn a new enemy"""
        # Spawn position (right side of screen, random height)
        spawn_x = self.screen_width + 50
        spawn_y = random.randint(
            self.ground_level - self.spawn_height_range,
            self.ground_level - 40
        )
        
        # Make sure enemy doesn't spawn too high
        spawn_y = max(spawn_y, 50)
        
        # Choose random color if no image
        color = random.choice(self.enemy_colors)
        
        # Create enemy
        enemy = Enemy(
            x=spawn_x,
            y=spawn_y,
            speed=self.enemy_speed,
            color=color,
            image_path=self.enemy_image_path
        )
        
        self.enemies.add(enemy)
        self.last_spawn_time = pygame.time.get_ticks()
    
    def set_enemy_speed(self, speed):
        """Change speed for all enemies"""
        self.enemy_speed = speed
        for enemy in self.enemies:
            enemy.set_speed(speed)
    
    def set_spawn_rate(self, spawn_rate):
        """Change how often enemies spawn"""
        self.spawn_rate = spawn_rate
    
    def set_enemy_image(self, image_path):
        """Change the enemy image path"""
        self.enemy_image_path = image_path
    
    def get_enemies(self):
        """Get all enemies for collision detection"""
        return self.enemies
    
    def remove_enemy(self, enemy):
        """Remove a specific enemy (when shot or off-screen)"""
        if enemy in self.enemies:
            self.enemies.remove(enemy)
    
    def clear_all_enemies(self):
        """Remove all enemies (for game reset)"""
        self.enemies.empty()
    
    def get_enemy_count(self):
        """Get number of active enemies"""
        return len(self.enemies)
    
    def update(self):
        """Update all enemies and spawn new ones"""
        # Update all enemies
        self.enemies.update()
        
        # Remove off-screen enemies
        for enemy in self.enemies.copy():
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
        
        # Spawn new enemies
        if self.should_spawn_enemy():
            self.spawn_enemy()
    
    def draw(self, screen):
        """Draw all enemies"""
        for enemy in self.enemies:
            enemy.draw(screen)