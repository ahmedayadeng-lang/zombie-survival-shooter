# settings.py
import pygame
from pathlib import Path
from enum import Enum, auto

# Base directory for all assets
BASE_PATH = Path(__file__).resolve().parent / "assets"

# Audio files (inside assets/audio)
SOUND_FILES = {
    "SHOOT": "shoot.mp3",
    "HIT": "hit.mp3",
    "ZOMBIE_DEATH": "zombie_death.mp3",
    "BACKGROUND": "background.mp3"  # or .ogg
}

# Screen settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1030
BACKGROUND_COLOR = (30, 30, 40)
WHITE = (255, 255, 255)
AUDIO_PATH = BASE_PATH / "audio" 

# Enums
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

class SkeletonState(Enum):
    MOVE = auto()
    ATTACK = auto()
    DEAD = auto()    

class SoundFiles:
    BACKGROUND = "background.mp3"
    SHOOT = "shoot.mp3"
    HIT = "hit.mp3"
    ZOMBIE_DEATH = "zombie_death.mp3"    

