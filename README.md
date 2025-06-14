# Fruit Catcher Game

A simple arcade-style game built with Python and Pygame where you catch falling fruits while avoiding bombs.

## Features

- Catch fruits to score points
- **Combo Bonus System**: Catch the same fruit type 3 times in a row for bonus points!
- Avoid bombs that reduce your lives
- Catch heart to increase your lives score
- Increasing difficulty as you play
- High score tracking
- Simple and intuitive controls
- Instant restart functionality

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clone the repository or download the source code
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:

   ```
   python fruit_catcher.py
   ```

2. Use the LEFT and RIGHT arrow keys to move the basket
3. Catch as many fruits as you can to score points
4. Avoid the bombs - they'll cost you a life!
5. The game ends when you run out of lives

## Controls

- LEFT ARROW: Move basket left
- RIGHT ARROW: Move basket right
- R: Restart game instantly (during gameplay)
- ESC: Return to main menu (during game)
- ENTER: Start game or return to menu (from game over)
- SPACE: Restart game directly (from game over screen)
- ESC: Quit game (from main menu)

## Game Elements

- 🧺 Basket: Your character at the bottom of the screen (blue rectangle)
- 🍎 Fruits: Various fruit sprites (13 different types) - catch these for points (10 points each)
- 💣 Bombs: Red rectangles - avoid these or lose a life
- ❤️ Healing: Heart sprite 
  - Cath these to heal a life (+1 life)
  - Maximum number of lives is limited to 3
- 🔥 **Combo System**:
  - Catch the same fruit type consecutively to build combos
  - 3+ consecutive same fruits = bonus points (20, 40, 60+ bonus)
  - Combo counter shows in top-left when active (yellow when 3+)
  - Hitting a bomb resets your combo

## Future Improvements

- ✅ ~~Add actual fruit and bomb sprites~~ (Implemented with spritesheet)
- ✅ ~~Add different types of fruits with different point values~~ (Implemented with combo system)
- Include sound effects and background music
- Implement power-ups and special abilities
- Add particle effects for catching fruits and explosions
- Create different levels with increasing difficulty
- Add visual effects for combo achievements
- Implement high score persistence

## Credits

Created with Python and Pygame
