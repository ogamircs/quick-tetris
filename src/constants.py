"""Game constants, colors, and tetromino definitions."""

# Board dimensions
HIDDEN_ROWS = 2  # Hidden rows above visible area for spawning
CELL_SIZE = 30
SIDE_PANEL_WIDTH = 200

# Difficulty settings: (board_width, board_height, start_level, fall_speed_multiplier)
DIFFICULTY_SETTINGS = {
    'easy': {'width': 10, 'height': 16, 'start_level': 1, 'speed_mult': 1.2},
    'medium': {'width': 12, 'height': 20, 'start_level': 1, 'speed_mult': 1.0},
    'hard': {'width': 14, 'height': 24, 'start_level': 2, 'speed_mult': 0.8},
}

# Colors (RGB)
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'dark_gray': (40, 40, 40),
    'light_gray': (200, 200, 200),
    'grid_line': (50, 50, 50),
    # Tetromino colors
    'cyan': (0, 255, 255),      # I piece
    'yellow': (255, 255, 0),    # O piece
    'purple': (128, 0, 128),    # T piece
    'green': (0, 255, 0),       # S piece
    'red': (255, 0, 0),         # Z piece
    'blue': (0, 0, 255),        # J piece
    'orange': (255, 165, 0),    # L piece
    # Menu colors
    'menu_bg': (20, 20, 40),
    'menu_highlight': (80, 80, 120),
    'title_color': (0, 200, 255),
}

# Timing (milliseconds)
INITIAL_FALL_SPEED = 1000  # 1 second per drop
SOFT_DROP_SPEED = 50       # Fast drop speed
LOCK_DELAY = 500           # Time before piece locks after landing
DAS_DELAY = 170            # Delayed Auto Shift initial delay
DAS_REPEAT = 50            # DAS repeat rate
HARD_DROP_ANIM_SPEED = 15  # Milliseconds per row during hard drop animation
LINE_CLEAR_ANIM_DURATION = 300  # Total duration of line clear animation in ms

# Scoring
SCORE_SINGLE = 100
SCORE_DOUBLE = 300
SCORE_TRIPLE = 500
SCORE_TETRIS = 800
SOFT_DROP_SCORE = 1
HARD_DROP_SCORE = 2

# Game states
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_PAUSED = 'paused'
STATE_GAME_OVER = 'game_over'

# Tetromino definitions
TETROMINOS = {
    'I': {
        'color': 'cyan',
        'shapes': [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
        ]
    },
    'O': {
        'color': 'yellow',
        'shapes': [
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
        ]
    },
    'T': {
        'color': 'purple',
        'shapes': [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
        ]
    },
    'S': {
        'color': 'green',
        'shapes': [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
            [(1, 1), (2, 1), (0, 2), (1, 2)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
        ]
    },
    'Z': {
        'color': 'red',
        'shapes': [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
        ]
    },
    'J': {
        'color': 'blue',
        'shapes': [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ]
    },
    'L': {
        'color': 'orange',
        'shapes': [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ]
    },
}

# SRS Wall Kick Data
WALL_KICKS = {
    'normal': {
        (0, 1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (1, 0): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
        (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (2, 3): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        (3, 2): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    },
    'I': {
        (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
        (1, 0): [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
        (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
        (2, 1): [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
        (2, 3): [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
        (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
        (3, 0): [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
        (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
    },
}
