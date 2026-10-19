# audio_manager.py
import pygame
from settings import AUDIO_PATH, SOUND_FILES

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        
        # MP3 files need higher frequency for better quality
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        """Load all MP3 sound effects"""
        try:
            # Convert MP3s to Sound objects
            self.sounds["SHOOT"] = self._load_mp3(SOUND_FILES["SHOOT"], volume=0.5)
            self.sounds["HIT"] = self._load_mp3(SOUND_FILES["HIT"], volume=0.7)
            self.sounds["ZOMBIE_DEATH"] = self._load_mp3(SOUND_FILES["ZOMBIE_DEATH"], volume=0.6)
        except Exception as e:
            print(f"Error loading sounds: {e}")

    def _load_mp3(self, filename, volume=1.0):
        """Helper method to load MP3 files as Sound objects"""
        sound = pygame.mixer.Sound(str(AUDIO_PATH / filename))
        sound.set_volume(volume)
        return sound

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_music(self):
        try:
            pygame.mixer.music.load(str(AUDIO_PATH / SOUND_FILES["BACKGROUND"]))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print(f"Couldn't load background music: {e}")

    def stop_background_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False        

    def play_sound(self, sound_name):
        try:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
        except:
            pass  # Silently fail if sound can't be played    