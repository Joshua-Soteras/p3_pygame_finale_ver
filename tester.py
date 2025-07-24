import pygame
import sys
from player import Player
from platform_manager import PlatformManager
from enemy_manager import EnemyManager
from powerup_manager import PowerUpManager
from game_over import GameOverScreen
from event_handler import handle_events, handle_game_events
from settings import *

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
        
        # Create fonts for displaying text
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.game_state = "playing"  # "playing", "game_over"
        self.running = True
        
        # Create game objects
        self._create_game_objects()
        
        # Create game over screen
        self.game_over_screen = GameOverScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Slow motion effect
        self.slow_motion_active = False
        self.time_multiplier = 1.0
    
    def _create_game_objects(self):
        """Create the player and managers"""
        # Create player - Students can easily modify these values!
        self.player = Player(
            width=30,           # Size of player
            height=30,
            color=RED,          # Player color
            movement_speed=6,   # How fast player moves
            jump_strength=18,   # How high player jumps
            gravity_strength=.9,  # How fast player falls
            lives=3,
            image_path= "pixil-frame-0.png"           # Starting lives
        )
        
        # Set player starting position
        self.player.set_screen_bounds(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player.rect.x = 150  # Keep player on left side
        self.player.rect.y = SCREEN_HEIGHT - 150
        
        # Create platform manager - Students can modify these settings!
        self.platform_manager = PlatformManager(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
            player=self.player,
            platform_speed=3,           # Base platform speed
            difficulty="normal",        # Starting difficulty
            difficulty_increase_rate=1.5,  # How much harder it gets
            difficulty_increase_time=10     # Seconds before getting harder
        )
        
        # Create enemy manager - Students can customize enemies!
        self.enemy_manager = EnemyManager(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
            enemy_speed=10,              # Enemy movement speed
            spawn_rate=10,               # Seconds between enemy spawns
            spawn_increase_time=15,     # Seconds before spawn rate increases
            enemy_image_path=None       # Path to enemy image (optional)
        )
        
        # Create power-up manager - Students can customize power-ups!
        enabled_powerups = [
            "speed", "jump", "fly", "double_shot", "invincible", 
            "shrink", "slow_motion", "shield", "extra_life", "long_range"
        ]
        

        
        self.powerup_manager = PowerUpManager(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
            spawn_rate=8,               # Seconds between power-up spawns
            enabled_powerups=enabled_powerups,  # Which power-ups can spawn
            powerup_images={}           # Custom images for power-ups
        )
    
    def reset_game(self):
        """Reset the game for a new playthrough"""
        print("Game Reset! Starting new game...")
        
        # Change game state first
        self.game_state = "playing"
        
        # Clear any pending timers
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        
        # Reset time effects
        self.slow_motion_active = False
        self.time_multiplier = 1.0
        
        # Clear all game objects
        if hasattr(self, 'enemy_manager'):
            self.enemy_manager.clear_all_enemies()
        if hasattr(self, 'powerup_manager'):
            self.powerup_manager.clear_all_powerups()
        
        # Create fresh game objects
        self._create_game_objects()
        
        # Reset player position
        self.player.rect.x = 150
        self.player.rect.y = SCREEN_HEIGHT - 150
    
    def check_platform_collisions(self):
        """Check if player collides with platforms"""
        collisionable_platforms = self.platform_manager.get_collisionable_platforms()
        
        for platform in collisionable_platforms:
            if self.player.rect.colliderect(platform.rect):
                # Check if player is landing on top of platform
                if (self.player.vel_y > 0 and 
                    self.player.rect.bottom - self.player.vel_y <= platform.rect.top + 10):
                    self.player.land_on_platform(platform.rect.top)
                    return True
        return False
    
    def check_enemy_collisions(self):
        """Check if player collides with enemies"""
        for enemy in self.enemy_manager.get_enemies():
            if self.player.rect.colliderect(enemy.rect):
                # Player hit by enemy
                if self.player.lose_life():
                    print(f"Player hit! Lives remaining: {self.player.get_lives()}")
                
                # Remove the enemy
                self.enemy_manager.remove_enemy(enemy)
                
                # Check if player is dead
                if self.player.is_dead():
                    print("Game Over: Player has no lives left!")
                    self.game_state = "game_over"
                
                return True
        return False
    
    def check_bullet_enemy_collisions(self):
        """Check if bullets hit enemies"""
        for bullet in self.player.get_bullets():
            for enemy in self.enemy_manager.get_enemies():
                if bullet.rect.colliderect(enemy.rect):
                    # Bullet hit enemy
                    self.player.bullets.remove(bullet)
                    self.enemy_manager.remove_enemy(enemy)
                    return True
        return False
    
    def check_powerup_collisions(self):
        """Check if player collides with power-ups"""
        for powerup in self.powerup_manager.get_powerups():
            if self.player.rect.colliderect(powerup.rect):
                # Player collected power-up
                powerup_type = powerup.get_type()
                duration = powerup.get_duration()
                
                # Apply power-up effect
                if powerup_type == "slow_motion":
                    self.slow_motion_active = True
                    self.time_multiplier = 0.5
                    # Set timer to end slow motion
                    pygame.time.set_timer(pygame.USEREVENT + 1, duration * 1000)
                else:
                    self.player.apply_powerup(powerup_type, duration)
                
                # Remove power-up
                self.powerup_manager.remove_powerup(powerup)
                return True
        return False
    
    def check_player_fall(self):
        """Check if player has fallen off the screen"""
        if self.player.is_falling_off_screen():
            print("Game Over: Player fell off screen!")
            self.game_state = "game_over"
            return True
        return False
    
    def draw_game_info(self):
        """Draw game information on screen"""
        # Get game stats
        time_elapsed = self.platform_manager.get_time_elapsed()
        distance = self.player.get_distance_traveled()
        current_speed = self.platform_manager.get_current_speed()
        difficulty_level = self.platform_manager.get_difficulty_level()
        lives = self.player.get_lives()
        
        # Draw background for text
        info_bg = pygame.Surface((320, 160))
        info_bg.fill((0, 0, 0))
        info_bg.set_alpha(128)  # Semi-transparent
        self.screen.blit(info_bg, (10, 10))
        
        # Draw game stats
        time_text = self.small_font.render(f"Time: {time_elapsed:.1f}s", True, WHITE)
        distance_text = self.small_font.render(f"Distance: {distance:.0f}", True, WHITE)
        speed_text = self.small_font.render(f"Speed: {current_speed:.1f}x", True, WHITE)
        difficulty_text = self.small_font.render(f"Difficulty: {difficulty_level:.1f}x", True, WHITE)
        lives_text = self.small_font.render(f"Lives: {lives}", True, RED if lives <= 1 else WHITE)
        
        self.screen.blit(time_text, (15, 15))
        self.screen.blit(distance_text, (15, 35))
        self.screen.blit(speed_text, (15, 55))
        self.screen.blit(difficulty_text, (15, 75))
        self.screen.blit(lives_text, (15, 95))
        
        # Draw difficulty mode
        difficulty_mode = self.platform_manager.difficulty.upper()
        mode_color = (255, 100, 100) if difficulty_mode == "HARD" else (100, 255, 100)
        mode_text = self.small_font.render(f"Mode: {difficulty_mode}", True, mode_color)
        self.screen.blit(mode_text, (15, 115))
        
        # Draw active power-ups
        active_powerups = self.player.get_active_powerups()
        if active_powerups:
            powerup_text = self.small_font.render(f"Powers: {', '.join(active_powerups)}", True, YELLOW)
            self.screen.blit(powerup_text, (15, 135))
        
        # Draw slow motion indicator
        if self.slow_motion_active:
            slow_text = self.small_font.render("SLOW MOTION", True, CYAN)
            self.screen.blit(slow_text, (15, 155))
    
    def draw_controls(self):
        """Draw control instructions"""
        controls = [
            "WASD/Arrows: Move & Jump",
            "K: Shoot",
            "TAB: Toggle Difficulty",  
            "1-5: Change Speed",
            "ESC: Quit"
        ]
        
        y_start = SCREEN_HEIGHT - 120
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            self.screen.blit(text, (10, y_start + i * 20))
    
    def update_playing(self, events):
        """Update game when in playing state"""
        # Get time step for smooth animation (affected by slow motion)
        dt = self.clock.tick(FPS) / 10.0 * self.time_multiplier
        
        # Handle game events (keyboard input, etc.)
        self.running = handle_game_events(self.platform_manager, events)
        
        # Handle slow motion timer
        for event in events:
            if event.type == pygame.USEREVENT + 1:
                # End slow motion
                self.slow_motion_active = False
                self.time_multiplier = 1.0
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
        
        # Get currently pressed keys
        keys_pressed = pygame.key.get_pressed()
        
        # Update player
        self.player.update(keys_pressed, dt)
        
        # Update platforms
        self.platform_manager.update()
        
        # Update enemies
        self.enemy_manager.update()
        
        # Update power-ups
        self.powerup_manager.update(self.platform_manager)
        
        # Check all collisions
        self.check_platform_collisions()
        self.check_enemy_collisions()
        self.check_bullet_enemy_collisions()
        self.check_powerup_collisions()
        self.check_player_fall()
    
    def update_game_over(self, events):
        """Update game when in game over state"""
        choice = self.game_over_screen.handle_events(events)
        
        if choice == "restart":
            print("Restarting game from game over screen...")
            self.reset_game()
        elif choice == "quit":
            print("Quitting game from game over screen...")
            self.running = False
        
    def update(self):
        """Update game based on current state"""
        # Collect all events once to avoid conflicts
        events = pygame.event.get()
        
        if self.game_state == "playing":
            self.update_playing(events)
        elif self.game_state == "game_over":
            self.update_game_over(events)
    
    def draw_playing(self):
        """Draw game when in playing state"""
        # Clear screen with black
        self.screen.fill(BLACK)
        
        # Draw platforms
        self.platform_manager.draw(self.screen)
        
        # Draw enemies
        self.enemy_manager.draw(self.screen)
        
        # Draw power-ups
        self.powerup_manager.draw(self.screen)
        
        # Draw player (includes bullets)
        self.player.draw(self.screen)
        
        # Draw game information
        self.draw_game_info()
        
        # Draw controls
        self.draw_controls()
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Draw final game state first
        self.draw_playing()
        
        # Create final stats
        final_stats = [
            f"Final Time: {self.platform_manager.get_time_elapsed():.1f} seconds",
            f"Distance Traveled: {self.player.get_distance_traveled():.0f}",
            f"Final Speed: {self.platform_manager.get_current_speed():.1f}x"
        ]
        
        # Draw game over screen on top
        self.game_over_screen.draw(self.screen, final_stats)
    
    def draw(self):
        """Draw everything based on current state"""
        if self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting Enhanced Platformer Game!")
        print("Controls:")
        print("- WASD or Arrow Keys: Move and jump")
        print("- K: Shoot bullets")
        print("- TAB: Toggle difficulty")
        print("- 1-5: Change platform speed")
        print("- ESC: Quit")
        print("\nFeatures:")
        print("- Enemies that fly across screen")
        print("- Power-ups with special abilities")
        print("- Lives system")
        print("- Progressive difficulty")
        
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
