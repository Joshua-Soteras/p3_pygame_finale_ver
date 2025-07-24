import pygame
from settings import *

class GameOverScreen:
    """
    A simple game over screen with restart option.
    Shows when player dies or falls off screen.
    """
    
    def __init__(self, screen_width, screen_height):
        """Create a game over screen"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Create fonts
        self.title_font = pygame.font.Font(None, 72)
        self.text_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 48)
        
        # Button dimensions
        self.button_width = 150
        self.button_height = 60
        self.button_spacing = 200
        
        # Calculate button positions
        center_x = screen_width // 2
        center_y = screen_height // 2 + 50
        
        # Yes button (restart)
        self.yes_button = pygame.Rect(
            center_x - self.button_spacing // 2 - self.button_width // 2,
            center_y,
            self.button_width,
            self.button_height
        )
        
        # No button (quit)
        self.no_button = pygame.Rect(
            center_x + self.button_spacing // 2 - self.button_width // 2,
            center_y,
            self.button_width,
            self.button_height
        )
        
        # Track mouse hover
        self.yes_hovered = False
        self.no_hovered = False
    
    def handle_events(self, events):
        """
        Handle mouse clicks and return player choice
        Returns: "restart", "quit", or None
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Check hover states
        self.yes_hovered = self.yes_button.collidepoint(mouse_pos)
        self.no_hovered = self.no_button.collidepoint(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.yes_button.collidepoint(mouse_pos):
                        return "restart"
                    elif self.no_button.collidepoint(mouse_pos):
                        return "quit"
            
            # Also allow keyboard input
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y or event.key == pygame.K_RETURN:
                    return "restart"
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    return "quit"
        
        return None
    
    def draw(self, screen, final_stats=None):
        """Draw the game over screen"""
        # Semi-transparent dark overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # Game Over title
        title_text = self.title_font.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        screen.blit(title_text, title_rect)
        
        # Show final stats if provided
        if final_stats:
            stats_y = self.screen_height // 2 - 50
            for stat in final_stats:
                stat_text = self.text_font.render(stat, True, WHITE)
                stat_rect = stat_text.get_rect(center=(self.screen_width // 2, stats_y))
                screen.blit(stat_text, stat_rect)
                stats_y += 30
        
        # Question text
        question_text = self.text_font.render("Play Again?", True, WHITE)
        question_rect = question_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 10))
        screen.blit(question_text, question_rect)
        
        # Yes button
        yes_color = GREEN if self.yes_hovered else (0, 150, 0)
        pygame.draw.rect(screen, yes_color, self.yes_button)
        pygame.draw.rect(screen, WHITE, self.yes_button, 3)
        yes_text = self.button_font.render("YES", True, WHITE)
        yes_text_rect = yes_text.get_rect(center=self.yes_button.center)
        screen.blit(yes_text, yes_text_rect)
        
        # No button
        no_color = RED if self.no_hovered else (150, 0, 0)
        pygame.draw.rect(screen, no_color, self.no_button)
        pygame.draw.rect(screen, WHITE, self.no_button, 3)
        no_text = self.button_font.render("NO", True, WHITE)
        no_text_rect = no_text.get_rect(center=self.no_button.center)
        screen.blit(no_text, no_text_rect)
        
        # Instructions
        instruction_text = self.text_font.render("Click buttons or press Y/N", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 140))
        screen.blit(instruction_text, instruction_rect)