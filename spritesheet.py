import pygame
import pygame
import random


class Spritesheet:
    def __init__(self, filename):
        """Load the spritesheet."""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet: {filename}")
            raise SystemExit(e)

    def get_image(self, x, y, width, height, scale=2):
        """Extract a single image from the spritesheet."""
        # Create a new surface
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Copy the sprite from the sheet to the new surface
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        # Scale the image if needed
        if scale != 1:
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def get_random_fruit(self):
        """Get a random fruit sprite from the spritesheet."""
        # The spritesheet is 80x48 with 16x16 tiles (5 columns, 3 rows)
        # The last two columns in the last row are empty, so we skip them

        # Total fruits available: (5 columns * 2 rows) + 3 fruits in last row = 13 fruits
        fruit_index = random.randint(0, 12)

        # Calculate row and column
        if fruit_index < 10:  # First two full rows (10 fruits)
            row = fruit_index // 5
            col = fruit_index % 5
        else:  # First three fruits in last row
            row = 2
            col = fruit_index - 10

        # Get the fruit sprite (16x16)
        return self.get_image(col * 16, row * 16, 16, 16, 2)  # Scale 2x for better visibility


def load_explosion_frames(sprite_sheet_path, frame_width, frame_height):
  sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
  sheet_width, sheet_height = sprite_sheet.get_size()

  num_frames = sheet_width // frame_width
  print(f"Auto-detected {num_frames} frames.")

  frames = []
  for i in range(num_frames):
    x = i * frame_width
    frame = sprite_sheet.subsurface(pygame.Rect(x, 0, frame_width, frame_height))
    frames.append(frame)
  return frames
