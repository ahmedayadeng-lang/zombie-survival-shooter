# main.py
import pygame
import sys
from settings import *
from player import Survivor
from skeleton import Skeleton
from game_map import GameMap
from audio_manager import AudioManager
import random

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Skeleton Survival")
        clock = pygame.time.Clock()
        
        # Initialize audio
        audio_manager = AudioManager()
        audio_manager.play_music()  # Start background music
        
        player = Survivor()
        game_map = GameMap()
        skeletons = []
        last_spawn = pygame.time.get_ticks()
        
        running = True
        while running:
            dt = clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # M key toggles music
                        if pygame.mixer.music.get_busy():
                            audio_manager.stop_background_music()
                        else:
                            audio_manager.play_music()
            
            # Spawn skeletons
            current_time = pygame.time.get_ticks()
            if current_time - last_spawn > 1000:
                last_spawn = current_time
                skeletons.append(Skeleton(random.choice([True, False])))
            
            # Update game objects (pass audio_manager)
            player.update()  # Pass to player
            skeletons = [sk for sk in skeletons if sk.update(player.position, player.bullets, dt, audio_manager)]
            
            # Draw
            screen.fill(BACKGROUND_COLOR)
            game_map.draw(screen)
            player.draw(screen)
            for skeleton in skeletons:
                skeleton.draw(screen)
            
            pygame.display.flip()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()
        
if __name__ == "__main__":
    main()  # This line MUST be at the bottom of main.py
