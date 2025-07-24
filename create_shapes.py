import pygame

class Shape:
    def __init__(self, x, y, width, height, color, shape_type):
        """
        Create a new shape!
        
        x: how far right on the screen (number)
        y: how far down on the screen (number)  
        width: how wide the shape is (number)
        height: how tall the shape is (number)
        color: what color the shape is (like "red" or (255, 0, 0))
        shape_type: "circle" or "rectangle"
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shape_type = shape_type
        
        # Handle color names or RGB tuples
        if isinstance(color, str):
            self.color = self._get_color_from_name(color)
        else:
            self.color = color
    
    def _get_color_from_name(self, color_name):
        """Convert color names to RGB values"""
        colors = {
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "green": (0, 255, 0),
            "yellow": (255, 255, 0),
            "purple": (128, 0, 128),
            "orange": (255, 165, 0),
            "pink": (255, 192, 203),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "gray": (128, 128, 128)
        }
        return colors.get(color_name.lower(), (0, 0, 0))  # Default to black
    
    def draw(self, screen):
        """Draw the shape on the screen"""
        if self.shape_type == "circle":
            # For circles, we use width as the diameter
            radius = self.width // 2
            center_x = self.x + radius
            center_y = self.y + radius
            pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
        
        elif self.shape_type == "rectangle":
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def move(self, new_x, new_y):
        """Move the shape to a new position"""
        self.x = new_x
        self.y = new_y
    
    def change_color(self, new_color):
        """Change the shape's color"""
        if isinstance(new_color, str):
            self.color = self._get_color_from_name(new_color)
        else:
            self.color = new_color




# More examples of how students can create shapes:

# Example 1: Making different colored circles
def make_rainbow_circles():
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    circles = []
    
    for i, color in enumerate(colors):
        x = 50 + (i * 100)  # Space them out
        y = 250
        circle = Shape(x, y, 60, 60, color, "circle")
        circles.append(circle)
    
    return circles

# Example 2: Making a simple house with rectangles
def make_house():
    house_parts = []
    
    # House base
    base = Shape(200, 300, 200, 150, "brown", "rectangle")
    house_parts.append(base)
    
    # Roof
    roof = Shape(180, 250, 240, 60, "red", "rectangle")
    house_parts.append(roof)
    
    # Door
    door = Shape(280, 380, 40, 70, "black", "rectangle")
    house_parts.append(door)
    
    # Windows
    window1 = Shape(220, 330, 30, 30, "blue", "rectangle")
    window2 = Shape(350, 330, 30, 30, "blue", "rectangle")
    house_parts.extend([window1, window2])
    
    return house_parts