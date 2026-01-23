# Quick Tetris

A complete Tetris game built in Python with Pygame, featuring modern gameplay mechanics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)

## Features

- **All 7 Tetromino Pieces** - I, O, T, S, Z, J, L with authentic colors
- **SRS Rotation System** - Super Rotation System with wall kicks
- **Ghost Piece** - See where your piece will land
- **Hold Piece** - Store a piece for later use
- **Next Piece Preview** - Plan your moves ahead
- **Hard Drop Animation** - Smooth visual feedback when dropping
- **Scoring System** - Points for lines, combos, and levels
- **Increasing Difficulty** - Speed increases as you level up
- **7-Bag Randomizer** - Fair piece distribution

## Installation

### Prerequisites
- Python 3.8 or higher
- pip or uv package manager

### Setup with uv (Recommended)
```bash
# Clone the repository
git clone https://github.com/ogamircs/quick-tetris.git
cd quick-tetris

# Create virtual environment and install dependencies
uv venv .venv --python 3.12
uv pip install pygame
```

### Setup with pip
```bash
# Clone the repository
git clone https://github.com/ogamircs/quick-tetris.git
cd quick-tetris

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install pygame
```

## Running the Game

```bash
# With virtual environment activated:
python tetris.py

# Or directly with the venv Python:
.venv/Scripts/python tetris.py      # Windows
.venv/bin/python tetris.py          # macOS/Linux
```

## Controls

| Key | Action |
|-----|--------|
| Left/Right Arrow | Move piece horizontally |
| Down Arrow | Soft drop (faster fall) |
| Space | Hard drop (instant drop with animation) |
| Up Arrow / X | Rotate clockwise |
| Z / Ctrl | Rotate counter-clockwise |
| C / Shift | Hold piece |
| Esc | Pause game |
| R | Restart game |

## Scoring

| Action | Points |
|--------|--------|
| Single (1 line) | 100 x Level |
| Double (2 lines) | 300 x Level |
| Triple (3 lines) | 500 x Level |
| Tetris (4 lines) | 800 x Level |
| Soft drop | 1 per row |
| Hard drop | 2 per row |
| Combo bonus | 50 x Combo x Level |

## Game Mechanics

### SRS Wall Kicks
When a rotation would cause a collision, the game tries alternative positions (wall kicks) to allow the rotation. This enables advanced techniques like T-spins.

### Lock Delay
Pieces don't lock immediately upon landing. You have 500ms to make adjustments, with up to 15 move/rotate resets.

### 7-Bag Randomizer
Pieces are drawn from shuffled bags of all 7 pieces, ensuring you never go too long without seeing a specific piece.

### DAS (Delayed Auto Shift)
Holding left/right has an initial delay (170ms) before auto-repeat kicks in (50ms intervals), allowing precise single-tap movements.

## Project Structure

```
quick-tetris/
├── tetris.py      # Main game file (all code in one file)
├── README.md      # This file
└── .gitignore     # Git ignore rules
```

## License

MIT License - feel free to use, modify, and distribute.

## Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Tetris game design by Alexey Pajitnov
- SRS rotation system based on Tetris Guideline
