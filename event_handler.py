import pygame

def handle_events(platform_manager, running):
    """
    Handle all game events like key presses and window closing.
    Students can easily add new controls here!
    
    Current controls:
    - ESC or X button: Quit game
    - TAB: Toggle difficulty between normal and hard
    - Number keys 1-5: Change platform speed
    - K: Shoot bullets (handled in player update)
    """
    # Note: This function is kept for compatibility but now just checks ESC
    keys_pressed = pygame.key.get_pressed()
    
    # Check for ESC key press to quit
    if keys_pressed[pygame.K_ESCAPE]:
        running = False
    
    return running

def handle_game_events(platform_manager, events):
    """
    Handle specific game events during gameplay
    Returns True to continue, False to quit
    """
    for event in events:
        # Check if player wants to quit
        if event.type == pygame.QUIT:
            return False
        
        # Check for key presses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            # Toggle difficulty with TAB
            elif event.key == pygame.K_TAB:
                current_difficulty = platform_manager.difficulty
                if current_difficulty == "normal":
                    platform_manager.set_difficulty("hard")
                    print("Difficulty changed to: HARD")
                else:
                    platform_manager.set_difficulty("normal")
                    print("Difficulty changed to: NORMAL")
            
            # Change platform speed with number keys
            elif event.key == pygame.K_1:
                platform_manager.set_platform_speed(1)
                print("Platform speed: 1 (Very Slow)")
            elif event.key == pygame.K_2:
                platform_manager.set_platform_speed(2)
                print("Platform speed: 2 (Slow)")
            elif event.key == pygame.K_3:
                platform_manager.set_platform_speed(3)
                print("Platform speed: 3 (Normal)")
            elif event.key == pygame.K_4:
                platform_manager.set_platform_speed(4)
                print("Platform speed: 4 (Fast)")
            elif event.key == pygame.K_5:
                platform_manager.set_platform_speed(5)
                print("Platform speed: 5 (Very Fast)")
    
    return True