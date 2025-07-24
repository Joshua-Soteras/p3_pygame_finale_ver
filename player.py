import pygame
import os
from bullet import Bullet
from settings import *

class Player(pygame.sprite.Sprite):
    """
    A simple player class for young coders!
    Students only need to set basic values like color, speed, and jump power.
    """
    
    def __init__(self, width=30, height=30, color=(255, 0, 0), 
                 movement_speed=6, jump_strength=18, gravity_strength=0.8, 
                 lives=DEFAULT_PLAYER_LIVES, image_path=None):
        """
        Create a player character!
        
        Parameters students can easily change:
        - width, height: Size of the player
        - color: Color of the player (red, blue, etc.)
        - movement_speed: How fast the player moves left/right
        - jump_strength: How high the player can jump
        - gravity_strength: How fast the player falls
        - lives: Number of lives the player starts with
        - image_path: Path to an image file (optional)
        """
        super(Player, self).__init__()
        
        # Store student-friendly settings
        self.movement_speed = movement_speed
        self.original_movement_speed = movement_speed
        self.jump_strength = jump_strength
        self.original_jump_strength = jump_strength
        self.gravity_strength = gravity_strength
        self.original_gravity_strength = gravity_strength
        
        # Player lives system
        self.lives = lives
        self.max_lives = 10
        
        # Physics properties
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = 2  # Allow double jump
        
        # Create player appearance
        self.original_width = width
        self.original_height = height
        self.original_color = color
        self._create_appearance(width, height, color, image_path)
        
        # Screen boundaries
        self.screen_width = 800
        self.screen_height = 600
        
        # Stats tracking
        self.distance_traveled = 0
        
        # Shooting system
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.shot_cooldown = 300  # milliseconds
        self.bullet_speed = DEFAULT_BULLET_SPEED
        self.bullet_range = DEFAULT_BULLET_RANGE
        
        # Power-up effects
        self.active_powerups = {}
        self.powerup_end_times = {}
        self.is_invincible = False
        self.is_flying = False
        self.has_shield = False
        self.is_shrunk = False
        
        # Double jump fix - track key states
        self.w_key_was_pressed = False
        self.up_key_was_pressed = False
        self.space_key_was_pressed = False
    
    def _create_appearance(self, width, height, color, image_path):
        """Create the player's visual appearance"""
        if image_path:
            try:
                if not os.path.isfile(image_path):
                    raise FileNotFoundError(f"File not found: {image_path}")
                self.surf = pygame.image.load(image_path).convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (width, height))
                self.rect = self.surf.get_rect()
            except Exception as e:
                print(f"[Warning] Could not load image: {e}")
                print("Using colored rectangle instead.")
                self.surf = pygame.Surface((width, height))
                self.surf.fill(color)
                self.rect = self.surf.get_rect()
        else:
            self.surf = pygame.Surface((width, height))
            self.surf.fill(color)
            self.rect = self.surf.get_rect()
    
    # Simple methods students can understand and use
    def jump(self):
        """Make the player jump! (Works with double jump)"""
        if self.is_flying:
            # In fly mode, move up
            self.vel_y = -self.movement_speed
        elif self.jump_count < self.max_jumps:
            if self.on_ground:
                self.jump_count = 0
            self.vel_y = -self.jump_strength
            self.jump_count += 1
            self.on_ground = False
    
    def move_left(self):
        """Move the player left"""
        self.vel_x = -self.movement_speed
    
    def move_right(self):
        """Move the player right"""
        self.vel_x = self.movement_speed
    
    def move_down(self):
        """Move the player down (only works in fly mode)"""
        if self.is_flying:
            self.vel_y = self.movement_speed
    
    def stop_moving(self):
        """Stop horizontal movement"""
        self.vel_x = 0
    
    def shoot(self):
        """Make the player shoot a bullet"""
        current_time = pygame.time.get_ticks()
        
        # Check shooting cooldown
        cooldown = self.shot_cooldown
        if "double_shot" in self.active_powerups:
            cooldown = self.shot_cooldown // 2
        
        if current_time - self.last_shot_time >= cooldown:
            bullet = Bullet(
                x=self.rect.right,
                y=self.rect.centery - 2,
                speed=self.bullet_speed,
                bullet_range=self.bullet_range
            )
            self.bullets.add(bullet)
            self.last_shot_time = current_time
    
    def get_bullets(self):
        """Get all player bullets for collision detection"""
        return self.bullets
    
    def is_on_ground(self):
        """Check if player is touching the ground"""
        return self.on_ground
    
    def get_position(self):
        """Get player's current position (x, y)"""
        return (self.rect.x, self.rect.y)
    
    def get_distance_traveled(self):
        """Get how far the player has traveled"""
        return self.distance_traveled
    
    def get_lives(self):
        """Get number of lives remaining"""
        return self.lives
    
    def add_life(self):
        """Add a life (from power-up)"""
        if self.lives < self.max_lives:
            self.lives += 1
    
    def lose_life(self):
        """Lose a life (from enemy collision)"""
        if self.has_shield:
            # Shield protects from damage
            self.has_shield = False
            self._remove_powerup("shield")
            print("Shield protected you!")
            return False
        elif not self.is_invincible:
            self.lives -= 1
            print(f"Life lost! Lives remaining: {self.lives}")
            return True
        else:
            print("Invincible - no damage!")
            return False
    
    def is_dead(self):
        """Check if player has no lives left"""
        return self.lives <= 0
    
    def is_falling_off_screen(self):
        """Check if player has fallen off the bottom of screen"""
        return self.rect.top > self.screen_height
    
    def apply_powerup(self, powerup_type, duration):
        """Apply a power-up effect to the player"""
        current_time = pygame.time.get_ticks()
        end_time = current_time + (duration * 1000)
        
        self.active_powerups[powerup_type] = True
        self.powerup_end_times[powerup_type] = end_time
        
        # Apply power-up effects
        if powerup_type == "speed":
            self.movement_speed = self.original_movement_speed * 2
        elif powerup_type == "jump":
            self.jump_strength = self.original_jump_strength * 1.5
        elif powerup_type == "fly":
            self.is_flying = True
        elif powerup_type == "invincible":
            self.is_invincible = True
        elif powerup_type == "shrink":
            self._shrink_player()
        elif powerup_type == "shield":
            self.has_shield = True
        elif powerup_type == "extra_life":
            self.add_life()
        elif powerup_type == "long_range":
            self.bullet_range = DEFAULT_BULLET_RANGE * 2
        
        print(f"Power-up activated: {powerup_type.upper()}")
    
    def get_active_powerups(self):
        """Get list of currently active power-ups"""
        return list(self.active_powerups.keys())
    
    def reset_for_new_game(self):
        """Reset player for a new game"""
        self.lives = DEFAULT_PLAYER_LIVES
        self.distance_traveled = 0
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.jump_count = 0
        self.bullets.empty()
        
        # Clear all power-ups
        self.active_powerups.clear()
        self.powerup_end_times.clear()
        self.is_invincible = False
        self.is_flying = False
        self.has_shield = False
        
        # Restore original stats
        self.movement_speed = self.original_movement_speed
        self.jump_strength = self.original_jump_strength
        self.gravity_strength = self.original_gravity_strength
        self.bullet_range = DEFAULT_BULLET_RANGE
        
        # Restore size if shrunk
        if self.is_shrunk:
            self._restore_normal_size()
    
    def land_on_platform(self, platform_top):
        """Called when player lands on a platform"""
        if not self.is_flying and self.vel_y > 0:
            self.rect.bottom = platform_top
            self.vel_y = 0
            self.on_ground = True
            self.jump_count = 0
    
    def set_screen_bounds(self, width, height):
        """Set screen boundaries"""
        self.screen_width = width
        self.screen_height = height
    
    def get_max_jump_distance(self):
        """Calculate maximum jump distance for platform generation"""
        time_to_peak = self.jump_strength / self.gravity_strength
        total_air_time = 2 * time_to_peak
        max_horizontal_distance = self.movement_speed * total_air_time
        return int(max_horizontal_distance * 0.8)
    
    # Hidden methods (students don't need to worry about these)
    def _shrink_player(self):
        """Shrink the player size"""
        if not self.is_shrunk:
            new_width = self.original_width // 2
            new_height = self.original_height // 2
            old_center = self.rect.center
            
            self.surf = pygame.transform.scale(self.surf, (new_width, new_height))
            self.rect = self.surf.get_rect()
            self.rect.center = old_center
            self.is_shrunk = True
    
    def _restore_normal_size(self):
        """Restore player to normal size"""
        if self.is_shrunk:
            old_center = self.rect.center
            self.surf = pygame.Surface((self.original_width, self.original_height))
            self.surf.fill(self.original_color)
            self.rect = self.surf.get_rect()
            self.rect.center = old_center
            self.is_shrunk = False
    
    def _remove_powerup(self, powerup_type):
        """Remove a power-up effect"""
        if powerup_type in self.active_powerups:
            del self.active_powerups[powerup_type]
            del self.powerup_end_times[powerup_type]
            
            # Remove effects
            if powerup_type == "speed":
                self.movement_speed = self.original_movement_speed
            elif powerup_type == "jump":
                self.jump_strength = self.original_jump_strength
            elif powerup_type == "fly":
                self.is_flying = False
            elif powerup_type == "invincible":
                self.is_invincible = False
            elif powerup_type == "shrink":
                self._restore_normal_size()
            elif powerup_type == "shield":
                self.has_shield = False
            elif powerup_type == "long_range":
                self.bullet_range = DEFAULT_BULLET_RANGE
    
    def _update_powerups(self):
        """Update active power-ups and remove expired ones"""
        current_time = pygame.time.get_ticks()
        expired_powerups = []
        
        for powerup_type, end_time in self.powerup_end_times.items():
            if current_time >= end_time:
                expired_powerups.append(powerup_type)
        
        for powerup_type in expired_powerups:
            self._remove_powerup(powerup_type)
    
    def _apply_physics(self, dt):
        """Apply gravity and movement physics"""
        # Apply gravity (unless flying)
        if not self.is_flying:
            self.vel_y += self.gravity_strength * dt
            if self.vel_y > 15:  # Terminal velocity
                self.vel_y = 15
        else:
            self.vel_y *= 0.9  # Gradual slowdown in fly mode
        
        # Update position
        old_x = self.rect.x
        self.rect.x += self.vel_x * dt
        self.rect.y += self.vel_y * dt
        
        # Track distance traveled
        if self.vel_x > 0:
            self.distance_traveled += abs(self.rect.x - old_x)
    
    def _handle_input(self, keys_pressed):
        """Handle keyboard input with fixed double jump"""
        # Reset horizontal velocity
        self.vel_x = 0
        
        # Movement controls
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.move_left()
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.move_right()
        
        # Jump controls - Fixed double jump detection
        w_pressed = keys_pressed[pygame.K_w]
        up_pressed = keys_pressed[pygame.K_UP]
        space_pressed = keys_pressed[pygame.K_SPACE]
        
        # Jump on key press (not hold)
        if (w_pressed and not self.w_key_was_pressed) or \
           (up_pressed and not self.up_key_was_pressed) or \
           (space_pressed and not self.space_key_was_pressed):
            self.jump()
        
        # Update key states
        self.w_key_was_pressed = w_pressed
        self.up_key_was_pressed = up_pressed
        self.space_key_was_pressed = space_pressed
        
        # Fly mode down movement
        if self.is_flying and (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]):
            self.move_down()
        
        # Shooting
        if keys_pressed[pygame.K_k]:
            self.shoot()
    
    def _constrain_to_screen(self):
        """Keep player within screen boundaries"""
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        
        if self.rect.top < 0:
            self.rect.top = 0
            if not self.is_flying:
                self.vel_y = 0
    
    def update(self, keys_pressed, dt=1):
        """Main update method called each frame"""
        self._handle_input(keys_pressed)
        self._apply_physics(dt)
        self._constrain_to_screen()
        self._update_powerups()
        
        # Update bullets
        self.bullets.update()
        
        # Remove off-screen bullets
        for bullet in self.bullets.copy():
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # Reset on_ground flag (collision detection will set it)
        if not self.is_flying:
            self.on_ground = False
    
    def draw(self, screen):
        """Draw the player and bullets on screen"""
        # Draw player with invincibility flash effect
        if self.is_invincible:
            if (pygame.time.get_ticks() // 100) % 2:  # Flash every 100ms
                screen.blit(self.surf, self.rect)
        else:
            screen.blit(self.surf, self.rect)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)