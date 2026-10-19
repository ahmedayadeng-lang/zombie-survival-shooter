# player.py
import pygame
import math
from pathlib import Path
from enum import Enum, auto
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BASE_PATH, BACKGROUND_COLOR, WHITE
from audio_manager import AudioManager

# Enums for state management
class WeaponType(Enum):
    RIFLE = auto()
    SHOTGUN = auto()
    HANDGUN = auto()
    KNIFE = auto()

class ActionState(Enum):
    IDLE = auto()
    MOVE = auto()
    MELEE = auto()
    RELOAD = auto()
    SHOOT = auto()

class Bullet:
    def __init__(self, x, y, facing_right, speed=25):
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.speed = speed if facing_right else -speed
        self.distance_traveled = 0
        self.max_distance = 750
        self.image = pygame.image.load(str(BASE_PATH / "bullet.png")).convert_alpha()
        
        # Scale down the bullet (adjust these values as needed)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        
        if not facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.x += self.speed
        self.distance_traveled += abs(self.speed)
        self.rect.center = (self.x+46, self.y+43)
        return self.distance_traveled >= self.max_distance
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Survivor:
    def __init__(self):
        # Define weapon-specific frame counts
        self.weapon_frame_counts = {
            WeaponType.RIFLE: {
                ActionState.IDLE: 20,
                ActionState.MOVE: 20,
                ActionState.MELEE: 15,
                ActionState.RELOAD: 20,
                ActionState.SHOOT: 3
                },
            WeaponType.SHOTGUN: {
                ActionState.IDLE: 20,
                ActionState.MOVE: 20,
                ActionState.MELEE: 15,
                ActionState.RELOAD: 20,
                ActionState.SHOOT: 3
                },
            WeaponType.HANDGUN: {
                ActionState.IDLE: 20,
                ActionState.MOVE: 20,
                ActionState.MELEE: 15,
                ActionState.RELOAD: 15,
                ActionState.SHOOT: 3
                },
            WeaponType.KNIFE: {
                ActionState.IDLE: 20,
                ActionState.MOVE: 20,
                ActionState.MELEE: 15,
                ActionState.RELOAD: 0,
                ActionState.SHOOT: 0
            }
            }
    
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.weapon = WeaponType.RIFLE
        self.action = ActionState.IDLE
        self.animations = {}
        self.current_frame = 0
        self.last_update = 0
        self.last_shot_time = 0
        self.shoot_cooldown = 100
        self.movement_speed = 5
        self.facing_right = True
        self.scale_factor = 0.45
        self.bullets = []

        self.load_all_animations()
        
    def load_all_animations(self):
        """Load animations with exact frame counts per weapon/action"""
        weapon_folders = {
            WeaponType.RIFLE: "rifle",
            WeaponType.SHOTGUN: "shotgun",
            WeaponType.HANDGUN: "handgun",
            WeaponType.KNIFE: "knife"
        }
    
        
        action_folders = {
            ActionState.IDLE: "idle",
            ActionState.MOVE: "move",
            ActionState.MELEE: "meleeattack",
            ActionState.RELOAD: "reload",
            ActionState.SHOOT: "shoot"
        }

        for weapon, weapon_folder in weapon_folders.items():
            self.animations[weapon] = {}
            for action, action_folder in action_folders.items():
                frames = []
                frame_count = self.weapon_frame_counts[weapon][action]
                
                # Skip actions with 0 frames
                if frame_count <= 0:
                    self.animations[weapon][action] = {'frames': [], 'speed': 0.1}
                    continue
                
                # Load each frame
                for i in range(frame_count):
                    try:
                        path = (
                            BASE_PATH / "Top_Down_Survivor" / weapon_folder / action_folder /
                            f"survivor-{action_folder}_{weapon_folder}_{i}.png"
                        )
                        frame = pygame.image.load(str(path)).convert_alpha()
                        # Scale down the player sprite
                        frame = pygame.transform.scale(
                            frame, 
                            (int(frame.get_width() * self.scale_factor), 
                             int(frame.get_height() * self.scale_factor))
                        )
                        frames.append(frame)
                    except pygame.error:
                        if i == 0:
                            print(f"Missing all frames for {weapon.name} {action.name}")
                            placeholder = pygame.Surface((100, 100), pygame.SRCALPHA)
                            pygame.draw.rect(placeholder, (255, 0, 255, 128), (0, 0, 100, 100))
                            frames.append(placeholder)
                            break
                        break
                
                self.animations[weapon][action] = {
                    'frames': frames,
                    'speed': self.get_animation_speed(action)
                }

    def get_animation_speed(self, action):
        """Return animation speed based on action type"""
        speeds = {
            ActionState.IDLE: 0.15,    # seconds per frame
            ActionState.MOVE: 0.1,
            ActionState.MELEE: 0.08,
            ActionState.RELOAD: 0.12,
            ActionState.SHOOT: 0.01
        }
        return speeds.get(action, 0.1)  # default speed if action not found                          
    

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_cooldown and self.weapon != WeaponType.KNIFE:
            self.last_shot_time = current_time
            self.action = ActionState.SHOOT
            self.current_frame = 0
            
            # Calculate bullet spawn position
            offset_x = 50 if self.facing_right else -50
            offset_y = -10
            spawn_x = self.position[0] + offset_x
            spawn_y = self.position[1] + offset_y
            
            self.bullets.append(Bullet(spawn_x, spawn_y, self.facing_right))
    
    def update(self):
        """Update animation, position, and bullets"""
        now = pygame.time.get_ticks()
        anim_data = self.animations[self.weapon][self.action]
        
        # Update animation frames
        if anim_data['frames']:
            if now - self.last_update > anim_data['speed'] * 1000:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(anim_data['frames'])
                
                if (self.action in [ActionState.MELEE, ActionState.SHOOT, ActionState.RELOAD] and 
                    self.current_frame == 0):
                    self.action = ActionState.IDLE
        
        # Handle movement
        keys = pygame.key.get_pressed()
        move_vector = [0, 0]
        
        if keys[pygame.K_w]: move_vector[1] -= 1
        if keys[pygame.K_s]: move_vector[1] += 1
        if keys[pygame.K_a]: 
            move_vector[0] -= 1
            self.facing_right = False
        if keys[pygame.K_d]: 
            move_vector[0] += 1
            self.facing_right = True
            
        if move_vector != [0, 0]:
            if self.action not in [ActionState.MELEE, ActionState.SHOOT, ActionState.RELOAD]:
                self.action = ActionState.MOVE
            if move_vector[0] != 0 and move_vector[1] != 0:
                move_vector[0] *= 0.7071
                move_vector[1] *= 0.7071
            self.position[0] += move_vector[0] * self.movement_speed
            self.position[1] += move_vector[1] * self.movement_speed
        elif self.action == ActionState.MOVE:
            self.action = ActionState.IDLE
        
        # Weapon switching
        if self.action == ActionState.IDLE:
            if keys[pygame.K_1]: self.weapon = WeaponType.RIFLE
            if keys[pygame.K_2]: self.weapon = WeaponType.SHOTGUN
            if keys[pygame.K_3]: self.weapon = WeaponType.HANDGUN
            if keys[pygame.K_4]: self.weapon = WeaponType.KNIFE
        
        # Shooting (space key)
        if keys[pygame.K_SPACE] and self.action == ActionState.IDLE:
            self.shoot()  # Pass the audio_manager

        # Other actions
        if keys[pygame.K_r] and self.action == ActionState.IDLE and self.weapon != WeaponType.KNIFE:
            self.action = ActionState.RELOAD
            self.current_frame = 0
        if keys[pygame.K_f] and self.action == ActionState.IDLE:
            self.action = ActionState.MELEE
            self.current_frame = 0
        
        # Update bullets
        self.bullets = [bullet for bullet in self.bullets if not bullet.update()]
    
    def draw(self, surface):
        """Draw player and bullets"""
        # Draw bullets first (so player appears on top)
        for bullet in self.bullets:
            bullet.draw(surface)
        
        # Draw player
        anim_data = self.animations[self.weapon][self.action]
        if anim_data['frames']:
            frame = anim_data['frames'][self.current_frame]
            if not self.facing_right:
                frame = pygame.transform.flip(frame, True, False)
            rect = frame.get_rect(center=self.position)
            surface.blit(frame, rect)
        
        # Debug info
        font = pygame.font.SysFont('Arial', 24)
        debug_text = [
            f"Weapon: {self.weapon.name}",
            f"Action: {self.action.name}",
            f"Bullets: {len(self.bullets)}",
            "Controls: WASD=Move, 1-4=Weapons, SPACE=Shoot, R=Reload, F=Melee"
        ]
        
        for i, text in enumerate(debug_text):
            text_surface = font.render(text, True, WHITE)
            surface.blit(text_surface, (10, 10 + i * 30))

