import pygame
import random
import os
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((80, 40))
        self.image.fill(BLUE)  # Temporary color
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

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.game.screen.get_width():
            self.rect.right = self.game.screen.get_width()

class Fruit(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        # Load spritesheet if not already loaded
        if not hasattr(game, 'fruit_sheet'):
            try:
                game.fruit_sheet = Spritesheet(os.path.join('images', 'fruit_spritesheet.png'))
            except:
                # Fallback to colored rectangle if spritesheet fails to load
                game.fruit_sheet = None

        # Get a random fruit sprite or fallback to colored rectangle
        if game.fruit_sheet:
            self.image = game.fruit_sheet.get_random_fruit()
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(GREEN)

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
        image_path = os.path.join('images', 'bomb.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

        # self.image.fill(RED)   Temporary color
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.game.screen.get_width() - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 8)  # Same speed range as fruit

    def update(self):
        self.rect.y += self.speedy

        # If it falls off the bottom
        if self.rect.top > self.game.screen.get_height():
            self.kill()


class Explosion(pygame.sprite.Sprite):
  def __init__(self, x, y, frames, frame_rate=4):
    super().__init__()
    self.frames = frames
    self.frame_rate = frame_rate
    self.current_frame = 0
    self.image = self.frames[self.current_frame]
    self.rect = self.image.get_rect(center=(x, y))
    self.counter = 0

  def update(self):
    self.counter += 1
    if self.counter % self.frame_rate == 0:
      self.current_frame += 1
      if self.current_frame >= len(self.frames):
        self.kill()  # delete sprite after explosion
      else:
        self.image = self.frames[self.current_frame]


# Define colors here for now (will be moved to a config file later)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
