# skeleton.py
import pygame
import random
import math
from settings import *
from pathlib import Path
from audio_manager import AudioManager

class Skeleton:
    def __init__(self, spawn_left=True):
        # Spawn positions for new screen size
        if spawn_left:
            self.x = random.randint(50, SCREEN_WIDTH//4)
        else:
            self.x = random.randint(SCREEN_WIDTH*3//4, SCREEN_WIDTH-50)
        self.y = random.randint(50, SCREEN_HEIGHT-50)
        
        # Stats (keep same)
        self.speed = 2.5
        self.health = 2
        self.attack_range = 70
        self.state = SkeletonState.MOVE
        self.facing_right = True
        
        # Load animations with 20% smaller size
        self.animations = {
            SkeletonState.MOVE: self.load_animation("skeleton move", "skeleton-move", 16),
            SkeletonState.ATTACK: self.load_animation("skeleton attack", "skeleton-attack", 8)
        }
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 0.1
        
        # Initial image
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def load_animation(self, folder, prefix, frame_count):
        frames = []
        for i in range(frame_count):
            try:
                path = BASE_PATH / folder / f"{prefix}_{i}.png"
                frame = pygame.image.load(str(path)).convert_alpha()
                # 40% smaller (scale factor 0.6)
                frame = pygame.transform.scale(
                    frame, 
                    (int(frame.get_width() * 0.40), 
                    int(frame.get_height() * 0.40))
                )
                frames.append(frame)
            except Exception as e:
                print(f"Error loading skeleton frame: {path} - {e}")
                placeholder = pygame.Surface((30, 30), pygame.SRCALPHA)  # Smaller placeholder
                pygame.draw.rect(placeholder, (255, 165, 0, 128), (0, 0, 30, 30))
                frames.append(placeholder)
        return frames
    
    def update(self, player_pos, bullets, dt, audio_manager=None):
        if self.state == SkeletonState.DEAD:
            return False

        # Update facing direction first
        px, py = player_pos
        self.facing_right = px > self.x
        
        # Animation update
        self.last_update += dt
        if self.last_update >= self.animation_speed * 1000:
            self.last_update = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]
        
        # Check bullet collisions
        for bullet in bullets[:]:
            if self.rect.colliderect(bullet.rect):
                self.health -= 1
                bullets.remove(bullet)
                if audio_manager:
                    audio_manager.play_sound("HIT")  # Play when hit
                    if self.health <= 0:
                        audio_manager.play_sound("ZOMBIE_DEATH")  # Play when dead
                if self.health <= 0:
                    return False
        
        # Movement and attack logic
        dx = px - self.x
        dy = py - self.y
        distance = math.hypot(dx, dy)
        
        if distance <= self.attack_range:
            self.state = SkeletonState.ATTACK
        else:
            self.state = SkeletonState.MOVE
            if distance > 0:
                self.x += dx/distance * self.speed
                self.y += dy/distance * self.speed
        
        self.rect.center = (self.x, self.y)
        return True
    
    def draw(self, surface):
        if self.state != SkeletonState.DEAD:
            # Flip image if facing left
            image = pygame.transform.flip(self.image, not self.facing_right, False)
            surface.blit(image, self.rect)