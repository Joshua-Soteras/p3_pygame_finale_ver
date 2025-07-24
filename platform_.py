import pygame

class Platform(pygame.sprite.Sprite):
    """
    A simple platform class for the game.
    Students can easily understand what each platform does.
    """
    
    def __init__(self, x, y, width, height, color=(139, 69, 19), 
                 platform_type="ground", speed=3, can_collide=True):
        """
        Create a platform!
        
        Parameters students can change:
        - x, y: Position of the platform
        - width, height: Size of the platform
        - color: Color of the platform
        - platform_type: "ground" or "elevated"
        - speed: How fast the platform moves left
        - can_collide: Whether the player can land on this platform
        """
        super(Platform, self).__init__()
        
        # Store student-friendly settings
        self.platform_type = platform_type
        self.speed = speed
        self.can_collide = can_collide
        self.original_speed = speed  # Remember original speed for difficulty scaling
        
        # Create platform appearance
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def move_left(self):
        """Move the platform to the left"""
        self.rect.x -= self.speed
    
    def set_speed(self, new_speed):
        """Change the platform's movement speed"""
        self.speed = new_speed
    
    def is_off_screen(self):
        """Check if platform has moved off the left side of screen"""
        return self.rect.right < 0
    
    def can_player_collide(self):
        """Check if player can collide with this platform"""
        return self.can_collide
    
    def set_collision(self, can_collide):
        """Enable or disable collision for this platform"""
        self.can_collide = can_collide
    
    def get_position(self):
        """Get platform position (x, y)"""
        return (self.rect.x, self.rect.y)
    
    def get_size(self):
        """Get platform size (width, height)"""
        return (self.rect.width, self.rect.height)
    
    def update(self):
        """Update the platform (move it left)"""
        self.move_left()
    
    def draw(self, screen):
        """Draw the platform on screen"""
        screen.blit(self.surf, self.rect)