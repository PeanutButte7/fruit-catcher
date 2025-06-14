import pygame
import sys
import random
import numpy as np
from enum import Enum
from sprites import Player, Fruit, Bomb, WHITE, BLACK, RED, GREEN, BLUE, Explosion, Heart
from spritesheet import load_explosion_frames

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Fruit Catcher"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.score = 0
        self.lives = 3

        self.all_sprites = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.combo_count = 0
        self.last_fruit_type = None
        self.combo_bonus = 0

        self.explosion_frames = load_explosion_frames("images/explosion.png", 64, 32)
        self.load_assets()

    def load_assets(self):
        self.font = pygame.font.Font(None, 36)
        try:
            self.background = pygame.image.load("images/background.png").convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            print("Background error")
            self.background = self.create_background()

        self.last_fruit = 0
        self.fruit_delay = 1000
        self.last_bomb = 0
        self.bomb_delay = 2000
        self.spawn_delay = 2000
        self.last_spawn = pygame.time.get_ticks()

    def create_background(self):
        tile_size = 50
        rows = SCREEN_HEIGHT // tile_size + 1
        cols = SCREEN_WIDTH // tile_size + 1
        grid = np.zeros((rows, cols, 3), dtype=np.uint8)
        for i in range(rows):
            for j in range(cols):
                grid[i, j] = [30, 30, 40] if (i + j) % 2 == 0 else [20, 20, 30]
        background = pygame.surfarray.make_surface(grid)
        return pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def new_game(self):
        self.score = 0
        self.lives = 3
        self.combo_count = 0
        self.last_fruit_type = None
        self.combo_bonus = 0

        self.all_sprites.empty()
        self.fruits.empty()
        self.bombs.empty()
        self.hearts.empty()
        self.explosions.empty()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.last_fruit = pygame.time.get_ticks()
        self.last_bomb = pygame.time.get_ticks()
        self.last_spawn = pygame.time.get_ticks()
        self.spawn_delay = 2000

        self.state = GameState.PLAYING

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == GameState.MENU:
                self.events_menu(event)
            elif self.state == GameState.PLAYING:
                self.events_playing(event)
            elif self.state == GameState.GAME_OVER:
                self.events_game_over(event)

    def events_menu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.new_game()
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    def events_playing(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
            elif event.key == pygame.K_r:
                self.new_game()

    def events_game_over(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = GameState.MENU
            elif event.key == pygame.K_SPACE:
                self.new_game()
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        if self.state == GameState.PLAYING:
            now = pygame.time.get_ticks()
            if now - self.last_spawn > self.spawn_delay:
                self.last_spawn = now
                self.spawn_delay = max(500, self.spawn_delay - 20)
                if random.random() < 0.40:
                    self.spawn_bomb()
                elif self.lives == 3:
                    self.spawn_fruit()
                else:
                    if random.random() < 0.9:
                        self.spawn_fruit()
                    else:
                        self.spawn_heart()

            self.all_sprites.update()
            self.explosions.update()
            self.check_collisions()
            if self.lives <= 0:
                self.state = GameState.GAME_OVER

    def spawn_fruit(self):
        fruit = Fruit(self)
        self.all_sprites.add(fruit)
        self.fruits.add(fruit)

    def spawn_heart(self):
        heart = Heart(self)
        self.all_sprites.add(heart)
        self.hearts.add(heart)

    def spawn_bomb(self):
        bomb = Bomb(self)
        self.all_sprites.add(bomb)
        self.bombs.add(bomb)

    def check_collisions(self):
        hits = pygame.sprite.spritecollide(self.player, self.fruits, True)
        for hit in hits:
            points = 10
            if self.last_fruit_type == hit.fruit_type:
                self.combo_count += 1
            else:
                self.combo_count = 1
                self.last_fruit_type = hit.fruit_type
            if self.combo_count >= 3:
                bonus = (self.combo_count - 2) * 20
                points += bonus
                self.combo_bonus = bonus
            else:
                self.combo_bonus = 0
            self.score += points

        hits = pygame.sprite.spritecollide(self.player, self.bombs, True)
        for hit in hits:
            explosion = Explosion(hit.rect.centerx, hit.rect.centery, self.explosion_frames)
            self.explosions.add(explosion)
            self.all_sprites.add(explosion)
            self.combo_count = 0
            self.last_fruit_type = None
            self.combo_bonus = 0
            self.lives -= 1

        hits = pygame.sprite.spritecollide(self.player, self.hearts, True)
        for hit in hits:
            if self.lives < 5:
                self.lives += 1
            self.combo_count = 0

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.explosions.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        restart_text = self.font.render("Press R to restart", True, WHITE)

        score_bg_height = 100 if self.combo_count >= 2 else 70
        score_bg = pygame.Surface((220, score_bg_height), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 128))
        self.screen.blit(score_bg, (0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(restart_text, (10, 40))

        if self.combo_count >= 2:
            combo_text = self.font.render(f"Combo: {self.combo_count}x", True, YELLOW)
            self.screen.blit(combo_text, (10, 70))

        if self.combo_bonus > 0:
            bonus_text = self.font.render(f"+{self.combo_bonus} COMBO BONUS!", True, YELLOW)
            bonus_x = SCREEN_WIDTH//2 - bonus_text.get_width()//2
            bonus_y = SCREEN_HEIGHT//2 - 100
            bonus_bg = pygame.Surface((bonus_text.get_width() + 20, 40), pygame.SRCALPHA)
            bonus_bg.fill((0, 0, 0, 160))
            self.screen.blit(bonus_bg, (bonus_x - 10, bonus_y - 5))
            self.screen.blit(bonus_text, (bonus_x, bonus_y))

        lives_bg = pygame.Surface((150, 40), pygame.SRCALPHA)
        lives_bg.fill((0, 0, 0, 128))
        self.screen.blit(lives_bg, (SCREEN_WIDTH - 150, 0))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 140, 10))
        pygame.display.flip()

    def draw_menu(self):
        title = self.font.render("FRUIT CATCHER", True, WHITE)
        start = self.font.render("Press ENTER to Start", True, WHITE)
        quit_text = self.font.render("Press ESC to Quit", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
        self.screen.blit(start, (SCREEN_WIDTH//2 - start.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 50))

    def draw_game_over(self):
        game_over = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_direct = self.font.render("Press SPACE to restart", True, YELLOW)
        restart_menu = self.font.render("Press ENTER to return to menu", True, WHITE)
        self.screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, SCREEN_HEIGHT//3))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(restart_direct, (SCREEN_WIDTH//2 - restart_direct.get_width()//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_menu, (SCREEN_WIDTH//2 - restart_menu.get_width()//2, SCREEN_HEIGHT//2 + 90))

g = Game()
g.run()
