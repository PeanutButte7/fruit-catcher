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
        """
        Get a random fruit sprite from the spritesheet.
        The spritesheet is 80x48 with 16x16 tiles (5 columns, 3 rows).
        Last row has only 3 usable tiles (total 13 fruits).
        """
        fruit_index = random.randint(0, 12)

        if fruit_index < 10:
            row = fruit_index // 5
            col = fruit_index % 5
        else:
            row = 2
            col = fruit_index - 10

        image = self.get_image(col * 16, row * 16, 16, 16, 2)
        return image, fruit_index


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
