"""
Tetris Game in Python with Pygame

A complete implementation featuring:
- All 7 tetromino pieces with SRS rotation
- Wall kick system
- Ghost piece preview
- Hold piece functionality
- Next piece preview
- Scoring system with levels
- Difficulty selection (Easy/Medium/Hard)
- Background music
"""

from src.game import TetrisGame

if __name__ == "__main__":
    game = TetrisGame()
    game.run()
