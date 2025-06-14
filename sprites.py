import pygame
import random
import os
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((80, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.screen.get_rect().centerx
        self.rect.bottom = self.game.screen.get_rect().bottom - 20
        self.speed = 8
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.game.screen.get_width():
            self.rect.right = self.game.screen.get_width()

class Fruit(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        if not hasattr(game, 'fruit_sheet'):
            try:
                game.fruit_sheet = Spritesheet(os.path.join('images', 'fruit_spritesheet.png'))
            except:
                game.fruit_sheet = None

        if game.fruit_sheet:
            self.image, self.fruit_type = game.fruit_sheet.get_random_fruit()
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(GREEN)
            self.fruit_type = 0 
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.game.screen.get_width() - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 8)
        
    def update(self):
        self.rect.y += self.speedy
        # If it falls off the bottom
        if self.rect.top > self.game.screen.get_height():
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((30, 30))  # Same size as fruit
        self.image.fill(RED)  # Temporary color
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.game.screen.get_width() - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 8)  # Same speed range as fruit
        
    def update(self):
        self.rect.y += self.speedy
        
        # If it falls off the bottom
        if self.rect.top > self.game.screen.get_height():
            self.kill()


class Heart(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        if not hasattr(game, 'heart'):
            try:
                game.heart = Spritesheet(os.path.join('images', 'heart.png'))
            except:
                game.heart = None

        if game.heart:
            self.image = game.heart.get_image(0, 0, 16, 16, 2)
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(GREEN)
            self.fruit_type = 0

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.game.screen.get_width() - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 8) # Make the heart a bit faster

    def update(self):
        self.rect.y += self.speedy
        # If it falls off the bottom
        if self.rect.top > self.game.screen.get_height():
            self.kill()

# Define colors here for now (will be moved to a config file later)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
