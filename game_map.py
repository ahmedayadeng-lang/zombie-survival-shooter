# map.py
import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BASE_PATH
from pathlib import Path

class GameMap:
    def __init__(self):
        # Tile configuration
        self.tile_size = 64  # Standard tile size (adjust if needed)
        self.tile_path = BASE_PATH / "map" / "Tile"
        
        # Selected tile numbers (1,2,15,27,28,29,41,42)
        self.valid_tiles = [1, 2, 15, 27, 28, 29, 41, 42]
        self.tile_probabilities = {
            1: 0.4,   # Ground - common
            2: 0.3,   # Ground variant
            15: 0.05, # Special tile - rare
            27: 0.05, # Decoration
            28: 0.05, # Decoration
            29: 0.05, # Decoration
            41: 0.05, # Wall
            42: 0.05  # Wall variant
        }
        
        # Calculate map dimensions
        self.map_width = (SCREEN_WIDTH // self.tile_size) + 2
        self.map_height = (SCREEN_HEIGHT // self.tile_size) + 2
        
        # Load textures
        self.tile_textures = self.load_tile_textures()
        self.generate_map()
    
    def load_tile_textures(self):
        """Load all specified tile textures"""
        textures = {}
        for tile_num in self.valid_tiles:
            try:
                # Pad numbers to two digits (01, 02, etc.)
                padded_num = f"{tile_num:02d}"
                path = self.tile_path / f"scifiTile_{padded_num}.png"
                texture = pygame.image.load(str(path)).convert_alpha()
                # Scale to our tile size if needed
                if texture.get_size() != (self.tile_size, self.tile_size):
                    texture = pygame.transform.scale(texture, (self.tile_size, self.tile_size))
                textures[tile_num] = texture
            except Exception as e:
                print(f"Error loading tile {tile_num}: {e}")
                # Create placeholder
                placeholder = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
                color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
                pygame.draw.rect(placeholder, color, (0, 0, self.tile_size, self.tile_size))
                pygame.draw.line(placeholder, (255, 255, 255), (0, 0), (self.tile_size, self.tile_size))
                pygame.draw.line(placeholder, (255, 255, 255), (self.tile_size, 0), (0, self.tile_size))
                textures[tile_num] = placeholder
        return textures
    
    def generate_map(self):
        """Generate a random map using selected tiles"""
        self.tiles = []
        
        # Create border walls (using tile 41)
        for x in range(self.map_width):
            row = []
            for y in range(self.map_height):
                if x == 0 or x == self.map_width-1 or y == 0 or y == self.map_height-1:
                    row.append(41)  # Border walls
                else:
                    # Randomly select tile based on probabilities
                    rand = random.random()
                    cumulative_prob = 0
                    for tile_num, prob in self.tile_probabilities.items():
                        cumulative_prob += prob
                        if rand < cumulative_prob:
                            row.append(tile_num)
                            break
                    else:
                        row.append(1)  # Default to tile 1 if no selection
            self.tiles.append(row)
        
        # Ensure walkable path (optional)
        self.ensure_walkability()
    
    def ensure_walkability(self):
        """Ensure there's a basic walkable path through the map"""
        # Make center tiles walkable (tile 1 or 2)
        center_x = self.map_width // 2
        center_y = self.map_height // 2
        radius = 5
        
        for x in range(center_x - radius, center_x + radius):
            for y in range(center_y - radius, center_y + radius):
                if 0 <= x < self.map_width and 0 <= y < self.map_height:
                    if random.random() < 0.8:  # 80% chance for walkable tile
                        self.tiles[x][y] = random.choice([1, 2])
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Draw the map with optional camera offset"""
        start_x = max(0, int(camera_offset[0] / self.tile_size))
        start_y = max(0, int(camera_offset[1] / self.tile_size))
        end_x = min(self.map_width, int((camera_offset[0] + SCREEN_WIDTH) / self.tile_size) + 1)
        end_y = min(self.map_height, int((camera_offset[1] + SCREEN_HEIGHT) / self.tile_size) + 1)
        
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile_num = self.tiles[x][y]
                if tile_num in self.tile_textures:
                    surface.blit(
                        self.tile_textures[tile_num],
                        (x * self.tile_size - camera_offset[0],
                         y * self.tile_size - camera_offset[1])
                    )