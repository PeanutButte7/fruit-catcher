import pygame
import sys
import random
import numpy as np
from enum import Enum
from sprites import Player, Fruit, Bomb, WHITE, BLACK, RED, GREEN, BLUE

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Fruit Catcher"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game states
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
        
        # Initialize game assets
        self.load_assets()
        
    def load_assets(self):
        self.font = pygame.font.Font(None, 36)
        # Generate a simple tilemap background
        self.background = self.create_background()
        self.last_fruit = 0
        self.fruit_delay = 1000  # milliseconds
        self.last_bomb = 0
        self.bomb_delay = 2000  # milliseconds
        self.spawn_delay = 2000  # Initial spawn delay (decreases over time)
        self.last_spawn = pygame.time.get_ticks()
        
    def create_background(self):
        # Create a simple tiled background using NumPy
        tile_size = 50
        rows = SCREEN_HEIGHT // tile_size + 1
        cols = SCREEN_WIDTH // tile_size + 1
        
        # Create a grid with alternating colors
        grid = np.zeros((rows, cols, 3), dtype=np.uint8)
        for i in range(rows):
            for j in range(cols):
                if (i + j) % 2 == 0:
                    grid[i, j] = [30, 30, 40]  # Dark gray
                else:
                    grid[i, j] = [20, 20, 30]   # Even darker gray
        
        # Convert to a surface
        background = pygame.surfarray.make_surface(grid)
        return pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def new_game(self):
        # Reset game state
        self.score = 0
        self.lives = 3
        self.all_sprites.empty()
        self.fruits.empty()
        self.bombs.empty()
        
        # Create player
        self.player = Player(self)
        self.all_sprites.add(self.player)
        
        # Reset timers
        self.last_fruit = pygame.time.get_ticks()
        self.last_bomb = pygame.time.get_ticks()
        self.last_spawn = pygame.time.get_ticks()
        self.spawn_delay = 2000
        
        self.state = GameState.PLAYING
    
    def run(self):
        # Game loop
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
            
            # Spawn fruits and bombs
            if now - self.last_spawn > self.spawn_delay:
                self.last_spawn = now
                # Gradually increase spawn rate
                self.spawn_delay = max(500, self.spawn_delay - 20)
                
                # Randomly decide to spawn fruit or bomb
                if random.random() < 0.60:  # 60% chance for fruit
                    self.spawn_fruit()
                else:  # 40% chance for bomb
                    self.spawn_bomb()
            
            # Update all sprites
            self.all_sprites.update()
            
            # Check for collisions
            self.check_collisions()
            
            # Check game over condition
            if self.lives <= 0:
                self.state = GameState.GAME_OVER
    
    def spawn_fruit(self):
        fruit = Fruit(self)
        self.all_sprites.add(fruit)
        self.fruits.add(fruit)
    
    def spawn_bomb(self):
        bomb = Bomb(self)
        self.all_sprites.add(bomb)
        self.bombs.add(bomb)
    
    def check_collisions(self):
        # Check fruit catches
        hits = pygame.sprite.spritecollide(self.player, self.fruits, True)
        for hit in hits:
            self.score += 10
            # Play sound here if we had one
        
        # Check bomb hits
        hits = pygame.sprite.spritecollide(self.player, self.bombs, True)
        for hit in hits:
            self.lives -= 1
            if self.lives <= 0:
                self.state = GameState.GAME_OVER
                return
            # Play explosion sound here if we had one
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_playing()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        title = self.font.render("FRUIT CATCHER", True, WHITE)
        start = self.font.render("Press ENTER to Start", True, WHITE)
        quit_text = self.font.render("Press ESC to Quit", True, WHITE)
        
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
        self.screen.blit(start, (SCREEN_WIDTH//2 - start.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
    
    def draw_playing(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        restart_text = self.font.render("Press R to restart", True, WHITE)
        
        # Add semi-transparent background for better text visibility
        score_bg = pygame.Surface((200, 70), pygame.SRCALPHA)  # Increased height for restart text
        score_bg.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(score_bg, (0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(restart_text, (10, 40))  # Position under the score
        
        lives_bg = pygame.Surface((150, 40), pygame.SRCALPHA)
        lives_bg.fill((0, 0, 0, 128))
        self.screen.blit(lives_bg, (SCREEN_WIDTH - 150, 0))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 140, 10))
    
    def draw_game_over(self):
        game_over = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_direct = self.font.render("Press SPACE to restart", True, YELLOW)
        restart_menu = self.font.render("Press ENTER to return to menu", True, WHITE)
        
        self.screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, SCREEN_HEIGHT//3))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(restart_direct, (SCREEN_WIDTH//2 - restart_direct.get_width()//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_menu, (SCREEN_WIDTH//2 - restart_menu.get_width()//2, SCREEN_HEIGHT//2 + 90))

# Create the game object
g = Game()
g.run()
