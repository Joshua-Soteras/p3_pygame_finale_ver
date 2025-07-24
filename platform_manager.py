import pygame
import random
from platform_ import Platform
from settings import *

class PlatformManager:
    """
    Manages all platforms in the game.
    Students can easily control difficulty and platform generation.
    """
    
    def __init__(self, screen_width, screen_height, player, 
                 platform_speed=3, difficulty="normal", 
                 difficulty_increase_rate=1.5, difficulty_increase_time=10):
        """
        Create a platform manager!
        
        Parameters students can change:
        - platform_speed: How fast platforms move (1=slow, 5=fast)
        - difficulty: "easy", "normal", or "hard"
        - difficulty_increase_rate: How much harder it gets (1.5 = 50% harder)
        - difficulty_increase_time: Seconds before difficulty increases
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        
        # Student-friendly settings
        self.base_platform_speed = platform_speed
        self.current_platform_speed = platform_speed
        self.difficulty = difficulty
        self.difficulty_increase_rate = difficulty_increase_rate
        self.difficulty_increase_time = difficulty_increase_time
        
        # Platform group
        self.platforms = pygame.sprite.Group()
        
        # Ground settings
        self.ground_height = 80
        self.ground_y = screen_height - self.ground_height
        
        # Platform size ranges
        self.min_ground_length = 100
        self.max_ground_length = 300
        self.min_elevated_length = 80
        self.max_elevated_length = 200
        
        # Gap settings (based on player jump ability)
        max_jump_distance = player.get_max_jump_distance()
        self.min_gap = int(max_jump_distance * 0.3)
        self.max_gap = int(max_jump_distance * 0.9)
        
        # Elevated platform heights
        self.elevated_heights = [
            screen_height - 200,  # Low
            screen_height - 300,  # Medium  
            screen_height - 400,  # High
        ]
        
        # Difficulty tracking
        self.consecutive_elevated = 0
        self.max_consecutive_elevated = self._get_max_consecutive()
        
        # Time tracking for difficulty progression
        self.start_time = pygame.time.get_ticks()
        self.last_difficulty_increase = self.start_time
        self.difficulty_level = 1.0
        
        # Colors
        self.ground_colors = [(139, 69, 19), (101, 67, 33), (160, 82, 45)]
        self.elevated_colors = [(70, 130, 180), (100, 149, 237), (135, 206, 250)]
        
        # Generate initial platforms
        self._generate_initial_platforms()
    
    def _get_max_consecutive(self):
        """Get max consecutive elevated platforms based on difficulty"""
        if self.difficulty == "easy":
            return 2
        elif self.difficulty == "normal":
            return 3
        else:  # hard
            return 5
    
    def _generate_initial_platforms(self):
        """Generate starting platforms with baseline platform"""
        current_x = -100
        
        # Create baseline starting platform (2 screen widths)
        baseline_platform = Platform(
            x=current_x,
            y=self.ground_y,
            width=BASELINE_PLATFORM_LENGTH,
            height=self.ground_height,
            color=self.ground_colors[0],
            platform_type="ground",
            speed=self.current_platform_speed
        )
        self.platforms.add(baseline_platform)
        current_x += BASELINE_PLATFORM_LENGTH
        
        # Generate additional platforms to fill screen
        while current_x < self.screen_width + 600:
            platform_type, width, height, y, color = self._get_next_platform_properties()
            
            # Add gap before platform
            gap = random.randint(self.min_gap, self.max_gap)
            current_x += gap
            
            # Create platform
            platform = Platform(current_x, y, width, height, color, 
                               platform_type, self.current_platform_speed)
            self.platforms.add(platform)
            
            current_x += width
    
    def _get_next_platform_properties(self):
        """Determine properties for next platform"""
        should_be_elevated = self._should_generate_elevated()
        
        if should_be_elevated and self.consecutive_elevated < self.max_consecutive_elevated:
            # Generate elevated platform
            platform_type = "elevated"
            width = random.randint(self.min_elevated_length, self.max_elevated_length)
            height = 30
            y = random.choice(self.elevated_heights)
            color = random.choice(self.elevated_colors)
            self.consecutive_elevated += 1
        else:
            # Generate ground platform
            platform_type = "ground"
            width = random.randint(self.min_ground_length, self.max_ground_length)
            height = self.ground_height
            y = self.ground_y
            color = random.choice(self.ground_colors)
            self.consecutive_elevated = 0
        
        return platform_type, width, height, y, color
    
    def _should_generate_elevated(self):
        """Determine if next platform should be elevated"""
        if self.difficulty == "easy":
            return random.random() < 0.2  # 20% chance
        elif self.difficulty == "normal":
            return random.random() < 0.3  # 30% chance
        else:  # hard
            return random.random() < 0.5  # 50% chance
    
    def _update_difficulty(self):
        """Increase difficulty over time"""
        current_time = pygame.time.get_ticks()
        time_since_start = (current_time - self.start_time) / 1000.0  # Convert to seconds
        
        # Check if it's time to increase difficulty
        expected_increases = int(time_since_start / self.difficulty_increase_time)
        
        if expected_increases > (self.difficulty_level - 1):
            self.difficulty_level = 1.0 + (expected_increases * (self.difficulty_increase_rate - 1.0))
            self.current_platform_speed = self.base_platform_speed * self.difficulty_level
            
            # Update speed for all existing platforms
            for platform in self.platforms:
                platform.set_speed(self.current_platform_speed)
    
    def set_difficulty(self, difficulty):
        """Change the difficulty setting"""
        self.difficulty = difficulty
        self.max_consecutive_elevated = self._get_max_consecutive()
    
    def set_platform_speed(self, speed):
        """Change the base platform speed"""
        self.base_platform_speed = speed
        self.current_platform_speed = speed * self.difficulty_level
        
        # Update all existing platforms
        for platform in self.platforms:
            platform.set_speed(self.current_platform_speed)
    
    def get_platforms(self):
        """Get all platforms for collision detection"""
        return self.platforms
    
    def get_collisionable_platforms(self):
        """Get only platforms that can collide with player"""
        return [platform for platform in self.platforms if platform.can_player_collide()]
    
    def get_time_elapsed(self):
        """Get time elapsed since game start (in seconds)"""
        return (pygame.time.get_ticks() - self.start_time) / 1000.0
    
    def get_current_speed(self):
        """Get current platform speed"""
        return self.current_platform_speed
    
    def get_difficulty_level(self):
        """Get current difficulty multiplier"""
        return self.difficulty_level
    
    def update(self):
        """Update all platforms and generate new ones"""
        # Update difficulty progression
        self._update_difficulty()
        
        # Update all platforms
        self.platforms.update()
        
        # Remove off-screen platforms
        for platform in self.platforms.copy():
            if platform.is_off_screen():
                self.platforms.remove(platform)
        
        # Generate new platforms
        self._generate_new_platforms()
    
    def _generate_new_platforms(self):
        """Generate new platforms on the right side"""
        # Find rightmost platform
        rightmost_x = self.screen_width
        for platform in self.platforms:
            if platform.rect.right > rightmost_x:
                rightmost_x = platform.rect.right
        
        # Generate platforms until screen is filled
        while rightmost_x < self.screen_width + 600:
            platform_type, width, height, y, color = self._get_next_platform_properties()
            
            # Add gap before new platform
            gap = random.randint(self.min_gap, self.max_gap)
            x = rightmost_x + gap
            
            # Create platform
            platform = Platform(x, y, width, height, color, 
                               platform_type, self.current_platform_speed)
            self.platforms.add(platform)
            
            # Update rightmost position
            rightmost_x = x + width
    
    def draw(self, screen):
        """Draw all platforms"""
        for platform in self.platforms:
            platform.draw(screen)