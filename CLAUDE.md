# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```bash
# Activate virtual environment first
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

# Run the game
python tetris.py
```

## Dependencies

The only external dependency is `pygame`. Install with:
```bash
pip install pygame
# or with uv
uv pip install pygame
```

## Project Structure

```
tetris_game/
├── tetris.py           # Entry point (imports and runs TetrisGame)
├── src/
│   ├── __init__.py     # Package init, exports TetrisGame
│   ├── constants.py    # All constants, colors, tetromino shapes, wall kicks
│   ├── music.py        # Procedural music generation
│   ├── tetromino.py    # Tetromino class
│   ├── board.py        # Board class (grid management)
│   └── game.py         # TetrisGame class (main game logic)
├── tests/
│   ├── test_tetromino.py   # Tetromino class tests
│   ├── test_board.py       # Board class tests
│   ├── test_constants.py   # Constants validation tests
│   └── test_music.py       # Music generation tests
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_board.py -v

# Run single test
python -m pytest tests/test_board.py::TestBoardClearLines::test_shifts_blocks_down_after_clear -v
```

## Architecture

### Module Responsibilities

- **`constants.py`**: All game constants including `DIFFICULTY_SETTINGS`, `COLORS`, `TETROMINOS` (shape definitions), `WALL_KICKS` (SRS rotation data), timing values, and scoring values.

- **`music.py`**: Contains `generate_tetris_music()` which procedurally generates a Tetris-like melody using square waves.

- **`tetromino.py`**: `Tetromino` class representing a falling piece with position, rotation state, and methods to get block coordinates.

- **`board.py`**: `Board` class managing the game grid, collision detection (`is_valid_position`), line clearing, and ghost piece positioning. The grid includes 2 hidden rows (`HIDDEN_ROWS`) above the visible area for piece spawning.

- **`game.py`**: `TetrisGame` class orchestrating the game loop, state management (menu/playing/paused/game_over), input handling with DAS (Delayed Auto Shift), animations, and rendering.

### Key Concepts

**Hidden Rows**: The board is 2 rows taller than visible. Pieces spawn in hidden rows (y=0, y=1). Game over occurs when locked blocks exist in hidden rows.

**7-Bag Randomizer**: Pieces are drawn from shuffled bags of all 7 pieces via `get_next_piece()`, ensuring fair distribution.

**DAS Input System**: Horizontal movement uses Delayed Auto Shift - 170ms initial delay before 50ms auto-repeat intervals.

**Animations**: Hard drop (15ms per row) and line clear (300ms total with flash/shrink phases) pause normal gameplay during execution.
