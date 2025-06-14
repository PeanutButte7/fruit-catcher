import pygame
import random

class Spritesheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet: {filename}")
            raise SystemExit(e)
    
    def get_image(self, x, y, width, height, scale=2):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        if scale != 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image
    
    def get_random_fruit(self):
        fruit_index = random.randint(0, 12)
        
        if fruit_index < 10:
            row = fruit_index // 5
            col = fruit_index % 5
        else:
            row = 2
            col = fruit_index - 10
        
        image = self.get_image(col * 16, row * 16, 16, 16, 2)
        return image, fruit_index
