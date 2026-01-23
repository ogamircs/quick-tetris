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

import pygame
import random
import sys
import math
import array

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# ============== CONSTANTS ==============

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

# ============== TETROMINO DEFINITIONS ==============

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


# ============== MUSIC GENERATOR ==============

def generate_tetris_music():
    """Generate a simple Tetris-like melody procedurally."""
    sample_rate = 44100

    # Tetris theme notes (simplified Korobeiniki melody)
    # Format: (frequency, duration_in_beats)
    melody = [
        # First phrase
        (659, 1), (494, 0.5), (523, 0.5), (587, 1), (523, 0.5), (494, 0.5),
        (440, 1), (440, 0.5), (523, 0.5), (659, 1), (587, 0.5), (523, 0.5),
        (494, 1.5), (523, 0.5), (587, 1), (659, 1),
        (523, 1), (440, 1), (440, 1), (0, 1),
        # Second phrase
        (587, 1), (698, 0.5), (880, 1), (784, 0.5), (698, 0.5),
        (659, 1.5), (523, 0.5), (659, 1), (587, 0.5), (523, 0.5),
        (494, 1), (494, 0.5), (523, 0.5), (587, 1), (659, 1),
        (523, 1), (440, 1), (440, 1), (0, 1),
    ]

    tempo = 140  # BPM
    beat_duration = 60.0 / tempo

    samples = []

    for freq, beats in melody:
        duration = beat_duration * beats
        num_samples = int(sample_rate * duration)

        for i in range(num_samples):
            t = i / sample_rate
            # Envelope for smoother sound
            envelope = min(1.0, min(t * 20, (duration - t) * 20))

            if freq > 0:
                # Square wave with slight smoothing
                value = envelope * 0.3 * (1 if math.sin(2 * math.pi * freq * t) > 0 else -1)
                # Add a softer harmonic
                value += envelope * 0.1 * math.sin(2 * math.pi * freq * 2 * t)
            else:
                value = 0

            # Convert to 16-bit integer
            sample = int(value * 32767)
            samples.append(sample)

    # Create stereo sound
    stereo_samples = []
    for s in samples:
        stereo_samples.append(s)  # Left
        stereo_samples.append(s)  # Right

    # Create pygame sound from samples
    sound_array = array.array('h', stereo_samples)
    sound = pygame.mixer.Sound(buffer=sound_array)

    return sound


# ============== TETROMINO CLASS ==============

class Tetromino:
    """Represents a falling tetromino piece."""

    def __init__(self, piece_type, board_width):
        self.type = piece_type
        self.rotation = 0
        self.color = COLORS[TETROMINOS[piece_type]['color']]
        self.x = board_width // 2 - 2
        self.y = 0

    def get_blocks(self, rotation=None, x=None, y=None):
        """Get absolute positions of all blocks in the tetromino."""
        if rotation is None:
            rotation = self.rotation
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        shape = TETROMINOS[self.type]['shapes'][rotation]
        return [(x + dx, y + dy) for dx, dy in shape]

    def rotate(self, direction=1):
        """Rotate piece. direction: 1=clockwise, -1=counter-clockwise."""
        self.rotation = (self.rotation + direction) % 4

    def copy(self):
        """Create a copy of this tetromino."""
        new_piece = Tetromino.__new__(Tetromino)
        new_piece.type = self.type
        new_piece.rotation = self.rotation
        new_piece.color = self.color
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece


# ============== BOARD CLASS ==============

class Board:
    """Manages the game board/grid."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)]
                     for _ in range(height + HIDDEN_ROWS)]

    def is_valid_position(self, piece, x=None, y=None, rotation=None):
        """Check if piece position is valid (no collisions, within bounds)."""
        blocks = piece.get_blocks(rotation, x, y)

        for bx, by in blocks:
            if bx < 0 or bx >= self.width:
                return False
            if by >= self.height + HIDDEN_ROWS:
                return False
            if by >= 0 and self.grid[by][bx] is not None:
                return False

        return True

    def lock_piece(self, piece):
        """Lock a piece into the grid."""
        blocks = piece.get_blocks()
        for bx, by in blocks:
            if 0 <= by < self.height + HIDDEN_ROWS:
                self.grid[by][bx] = piece.color

    def find_complete_lines(self):
        """Find all completed lines and return their y positions."""
        complete = []
        for y in range(self.height + HIDDEN_ROWS):
            if all(cell is not None for cell in self.grid[y]):
                complete.append(y)
        return complete

    def clear_lines(self, lines_to_clear=None):
        """Clear completed lines and return number cleared."""
        if lines_to_clear is None:
            lines_to_clear = self.find_complete_lines()

        lines_cleared = len(lines_to_clear)

        for y in sorted(lines_to_clear, reverse=True):
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(self.width)])

        return lines_cleared

    def is_game_over(self):
        """Check if any blocks in hidden rows (game over condition)."""
        for y in range(HIDDEN_ROWS):
            if any(cell is not None for cell in self.grid[y]):
                return True
        return False

    def get_ghost_position(self, piece):
        """Get the y position where the piece would land."""
        ghost_y = piece.y
        while self.is_valid_position(piece, piece.x, ghost_y + 1):
            ghost_y += 1
        return ghost_y


# ============== GAME CLASS ==============

class TetrisGame:
    """Main game class handling game logic and rendering."""

    def __init__(self):
        # Start with medium difficulty dimensions for initial window
        self.difficulty = 'medium'
        self.board_width = DIFFICULTY_SETTINGS['medium']['width']
        self.board_height = DIFFICULTY_SETTINGS['medium']['height']

        # Calculate screen dimensions
        self.update_screen_dimensions()

        # Display setup
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 72)

        # Menu state
        self.state = STATE_MENU
        self.menu_selection = 1  # 0=Easy, 1=Medium, 2=Hard
        self.pause_selection = 0  # 0=Resume, 1=Main Menu

        # Music
        self.music = None
        self.music_playing = False
        self.init_music()

        # Game state (will be initialized when starting game)
        self.board = None
        self.current_piece = None
        self.next_piece = None

    def update_screen_dimensions(self):
        """Update screen dimensions based on board size."""
        self.board_pixel_width = self.board_width * CELL_SIZE
        self.board_pixel_height = self.board_height * CELL_SIZE
        self.screen_width = self.board_pixel_width + SIDE_PANEL_WIDTH
        self.screen_height = self.board_pixel_height

    def init_music(self):
        """Initialize background music."""
        try:
            self.music = generate_tetris_music()
        except Exception as e:
            print(f"Could not generate music: {e}")
            self.music = None

    def start_music(self):
        """Start playing background music."""
        if self.music and not self.music_playing:
            self.music.play(loops=-1)
            self.music_playing = True

    def stop_music(self):
        """Stop background music."""
        if self.music and self.music_playing:
            self.music.stop()
            self.music_playing = False

    def start_game(self, difficulty):
        """Start a new game with selected difficulty."""
        self.difficulty = difficulty
        settings = DIFFICULTY_SETTINGS[difficulty]

        self.board_width = settings['width']
        self.board_height = settings['height']
        self.speed_multiplier = settings['speed_mult']
        self.start_level = settings['start_level']

        # Update screen size
        self.update_screen_dimensions()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Initialize game
        self.reset_game()
        self.state = STATE_PLAYING
        self.start_music()

    def reset_game(self):
        """Reset/initialize game state."""
        self.board = Board(self.board_width, self.board_height)
        self.bag = []
        self.current_piece = self.get_next_piece()
        self.next_piece = self.get_next_piece()
        self.held_piece = None
        self.can_hold = True

        # Scoring
        self.score = 0
        self.lines_cleared = 0
        self.level = getattr(self, 'start_level', 1)
        self.combo = 0

        # Timing
        self.fall_time = 0
        self.lock_time = 0
        self.is_locking = False
        self.lock_moves = 0

        # Input handling
        self.das_time = 0
        self.das_direction = 0
        self.das_charged = False

        # Animations
        self.hard_drop_animating = False
        self.hard_drop_target_y = 0
        self.hard_drop_anim_time = 0
        self.hard_drop_score_pending = 0

        self.line_clear_animating = False
        self.clearing_lines = []
        self.line_clear_anim_time = 0

    def return_to_menu(self):
        """Return to main menu."""
        self.state = STATE_MENU
        self.stop_music()

        # Reset to medium size for menu
        self.board_width = DIFFICULTY_SETTINGS['medium']['width']
        self.board_height = DIFFICULTY_SETTINGS['medium']['height']
        self.update_screen_dimensions()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def get_next_piece(self):
        """Get next piece using 7-bag randomizer."""
        if not self.bag:
            self.bag = list(TETROMINOS.keys())
            random.shuffle(self.bag)
        return Tetromino(self.bag.pop(), self.board_width)

    def get_fall_speed(self):
        """Calculate fall speed based on level and difficulty."""
        base_speed = max(100, INITIAL_FALL_SPEED - (self.level - 1) * 80)
        return int(base_speed * getattr(self, 'speed_multiplier', 1.0))

    def try_wall_kick(self, piece, old_rotation, new_rotation):
        """Try wall kicks for rotation."""
        kick_type = 'I' if piece.type == 'I' else 'normal'
        kick_key = (old_rotation, new_rotation)

        if kick_key not in WALL_KICKS[kick_type]:
            return False

        kicks = WALL_KICKS[kick_type][kick_key]

        for dx, dy in kicks:
            new_x = piece.x + dx
            new_y = piece.y - dy

            if self.board.is_valid_position(piece, new_x, new_y, new_rotation):
                piece.x = new_x
                piece.y = new_y
                piece.rotation = new_rotation
                return True

        return False

    def rotate_piece(self, direction=1):
        """Attempt to rotate the current piece."""
        if self.current_piece is None:
            return False

        old_rotation = self.current_piece.rotation
        new_rotation = (old_rotation + direction) % 4

        if self.board.is_valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece.rotation = new_rotation
            self.on_piece_moved()
            return True

        if self.try_wall_kick(self.current_piece, old_rotation, new_rotation):
            self.on_piece_moved()
            return True

        return False

    def move_piece(self, dx):
        """Move piece horizontally."""
        if self.current_piece is None:
            return False

        new_x = self.current_piece.x + dx
        if self.board.is_valid_position(self.current_piece, x=new_x):
            self.current_piece.x = new_x
            self.on_piece_moved()
            return True
        return False

    def soft_drop(self):
        """Move piece down one cell."""
        if self.current_piece is None:
            return False

        new_y = self.current_piece.y + 1
        if self.board.is_valid_position(self.current_piece, y=new_y):
            self.current_piece.y = new_y
            self.score += SOFT_DROP_SCORE
            return True
        return False

    def hard_drop(self):
        """Start hard drop animation."""
        if self.current_piece is None or self.hard_drop_animating:
            return

        target_y = self.board.get_ghost_position(self.current_piece)
        drop_distance = target_y - self.current_piece.y

        if drop_distance > 0:
            self.hard_drop_animating = True
            self.hard_drop_target_y = target_y
            self.hard_drop_anim_time = 0
            self.hard_drop_score_pending = drop_distance * HARD_DROP_SCORE
        else:
            self.lock_piece()

    def hold_piece(self):
        """Hold current piece."""
        if not self.can_hold or self.current_piece is None:
            return

        self.can_hold = False

        if self.held_piece is None:
            self.held_piece = Tetromino(self.current_piece.type, self.board_width)
            self.current_piece = self.next_piece
            self.next_piece = self.get_next_piece()
        else:
            held_type = self.held_piece.type
            self.held_piece = Tetromino(self.current_piece.type, self.board_width)
            self.current_piece = Tetromino(held_type, self.board_width)

        self.current_piece.x = self.board_width // 2 - 2
        self.current_piece.y = 0
        self.is_locking = False

    def on_piece_moved(self):
        """Called when piece is moved/rotated during lock delay."""
        if self.is_locking:
            self.lock_time = 0
            self.lock_moves += 1
            if self.lock_moves >= 15:
                self.lock_piece()

    def lock_piece(self):
        """Lock current piece and spawn next."""
        if self.current_piece is None:
            return

        self.board.lock_piece(self.current_piece)

        complete_lines = self.board.find_complete_lines()
        if complete_lines:
            self.line_clear_animating = True
            self.clearing_lines = complete_lines
            self.line_clear_anim_time = 0
            self.current_piece = None
            return

        self.finish_lock_piece(0)

    def finish_lock_piece(self, lines_cleared):
        """Complete the lock piece process after line clear animation."""
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.combo += 1
            base_scores = {1: SCORE_SINGLE, 2: SCORE_DOUBLE,
                         3: SCORE_TRIPLE, 4: SCORE_TETRIS}
            self.score += base_scores.get(lines_cleared, 0) * self.level
            if self.combo > 1:
                self.score += 50 * self.combo * self.level
            self.level = max(getattr(self, 'start_level', 1),
                           self.lines_cleared // 10 + 1)
        else:
            self.combo = 0

        if self.board.is_game_over():
            self.state = STATE_GAME_OVER
            return

        self.current_piece = self.next_piece
        self.next_piece = self.get_next_piece()
        self.can_hold = True
        self.is_locking = False
        self.lock_moves = 0

        if not self.board.is_valid_position(self.current_piece):
            self.state = STATE_GAME_OVER

    def update(self, dt):
        """Update game state."""
        if self.state != STATE_PLAYING:
            return

        # Line clear animation
        if self.line_clear_animating:
            self.line_clear_anim_time += dt
            if self.line_clear_anim_time >= LINE_CLEAR_ANIM_DURATION:
                lines_count = len(self.clearing_lines)
                self.board.clear_lines(self.clearing_lines)
                self.line_clear_animating = False
                self.clearing_lines = []
                self.finish_lock_piece(lines_count)
            return

        if self.current_piece is None:
            return

        # Hard drop animation
        if self.hard_drop_animating:
            self.hard_drop_anim_time += dt
            while self.hard_drop_anim_time >= HARD_DROP_ANIM_SPEED:
                self.hard_drop_anim_time -= HARD_DROP_ANIM_SPEED
                if self.current_piece.y < self.hard_drop_target_y:
                    self.current_piece.y += 1
                else:
                    self.hard_drop_animating = False
                    self.score += self.hard_drop_score_pending
                    self.hard_drop_score_pending = 0
                    self.lock_piece()
                    break
            return

        # Gravity
        self.fall_time += dt
        fall_speed = self.get_fall_speed()

        if self.fall_time >= fall_speed:
            self.fall_time = 0
            if not self.soft_drop():
                self.is_locking = True

        # Lock delay
        if self.is_locking:
            self.lock_time += dt
            if self.lock_time >= LOCK_DELAY:
                self.lock_piece()

    def handle_input(self, dt):
        """Handle keyboard input during gameplay."""
        if self.state != STATE_PLAYING:
            return
        if self.hard_drop_animating or self.line_clear_animating:
            return

        keys = pygame.key.get_pressed()

        # DAS for horizontal movement
        if keys[pygame.K_LEFT]:
            if self.das_direction != -1:
                self.das_direction = -1
                self.das_time = 0
                self.das_charged = False
                self.move_piece(-1)
            else:
                self.das_time += dt
                if not self.das_charged:
                    if self.das_time >= DAS_DELAY:
                        self.das_charged = True
                        self.das_time = 0
                        self.move_piece(-1)
                else:
                    if self.das_time >= DAS_REPEAT:
                        self.das_time = 0
                        self.move_piece(-1)
        elif keys[pygame.K_RIGHT]:
            if self.das_direction != 1:
                self.das_direction = 1
                self.das_time = 0
                self.das_charged = False
                self.move_piece(1)
            else:
                self.das_time += dt
                if not self.das_charged:
                    if self.das_time >= DAS_DELAY:
                        self.das_charged = True
                        self.das_time = 0
                        self.move_piece(1)
                else:
                    if self.das_time >= DAS_REPEAT:
                        self.das_time = 0
                        self.move_piece(1)
        else:
            self.das_direction = 0
            self.das_charged = False

        if keys[pygame.K_DOWN]:
            self.fall_time += SOFT_DROP_SPEED

    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.KEYDOWN:
            if self.state == STATE_MENU:
                self.handle_menu_event(event)
            elif self.state == STATE_PLAYING:
                self.handle_game_event(event)
            elif self.state == STATE_PAUSED:
                self.handle_pause_event(event)
            elif self.state == STATE_GAME_OVER:
                self.handle_game_over_event(event)

    def handle_menu_event(self, event):
        """Handle menu input."""
        if event.key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % 3
        elif event.key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % 3
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            difficulties = ['easy', 'medium', 'hard']
            self.start_game(difficulties[self.menu_selection])

    def handle_game_event(self, event):
        """Handle game input."""
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_PAUSED
            self.pause_selection = 0
            return

        if self.hard_drop_animating or self.line_clear_animating:
            return

        if event.key == pygame.K_UP or event.key == pygame.K_x:
            self.rotate_piece(1)
        elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
            self.rotate_piece(-1)
        elif event.key == pygame.K_SPACE:
            self.hard_drop()
        elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
            self.hold_piece()

    def handle_pause_event(self, event):
        """Handle pause menu input."""
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_PLAYING
        elif event.key == pygame.K_UP:
            self.pause_selection = (self.pause_selection - 1) % 2
        elif event.key == pygame.K_DOWN:
            self.pause_selection = (self.pause_selection + 1) % 2
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.pause_selection == 0:
                self.state = STATE_PLAYING
            else:
                self.return_to_menu()

    def handle_game_over_event(self, event):
        """Handle game over input."""
        if event.key == pygame.K_r:
            self.reset_game()
            self.state = STATE_PLAYING
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
            self.return_to_menu()

    def draw_block(self, x, y, color, surface=None, offset_x=0, offset_y=0):
        """Draw a single block with 3D effect."""
        if surface is None:
            surface = self.screen

        px = offset_x + x * CELL_SIZE
        py = offset_y + y * CELL_SIZE

        pygame.draw.rect(surface, color,
                        (px + 1, py + 1, CELL_SIZE - 2, CELL_SIZE - 2))

        highlight = tuple(min(255, c + 50) for c in color)
        pygame.draw.line(surface, highlight, (px + 1, py + 1),
                        (px + CELL_SIZE - 2, py + 1), 2)
        pygame.draw.line(surface, highlight, (px + 1, py + 1),
                        (px + 1, py + CELL_SIZE - 2), 2)

        shadow = tuple(max(0, c - 50) for c in color)
        pygame.draw.line(surface, shadow,
                        (px + CELL_SIZE - 2, py + 2),
                        (px + CELL_SIZE - 2, py + CELL_SIZE - 2), 2)
        pygame.draw.line(surface, shadow,
                        (px + 2, py + CELL_SIZE - 2),
                        (px + CELL_SIZE - 2, py + CELL_SIZE - 2), 2)

    def draw_block_animated(self, x, y, color, scale=1.0, flash=0.0):
        """Draw a block with animation effects."""
        px = x * CELL_SIZE
        py = y * CELL_SIZE

        scaled_size = int(CELL_SIZE * scale)
        offset = (CELL_SIZE - scaled_size) // 2

        if scaled_size <= 0:
            return

        if flash > 0:
            color = tuple(int(c + (255 - c) * flash) for c in color)

        pygame.draw.rect(self.screen, color,
                        (px + offset + 1, py + offset + 1,
                         scaled_size - 2, scaled_size - 2))

        if scale > 0.5:
            highlight = tuple(min(255, c + 50) for c in color)
            pygame.draw.line(self.screen, highlight,
                           (px + offset + 1, py + offset + 1),
                           (px + offset + scaled_size - 2, py + offset + 1), 2)
            pygame.draw.line(self.screen, highlight,
                           (px + offset + 1, py + offset + 1),
                           (px + offset + 1, py + offset + scaled_size - 2), 2)

            shadow = tuple(max(0, c - 50) for c in color)
            pygame.draw.line(self.screen, shadow,
                           (px + offset + scaled_size - 2, py + offset + 2),
                           (px + offset + scaled_size - 2, py + offset + scaled_size - 2), 2)
            pygame.draw.line(self.screen, shadow,
                           (px + offset + 2, py + offset + scaled_size - 2),
                           (px + offset + scaled_size - 2, py + offset + scaled_size - 2), 2)

    def draw_menu(self):
        """Draw the main menu."""
        self.screen.fill(COLORS['menu_bg'])

        # Title
        title = self.title_font.render("TETRIS", True, COLORS['title_color'])
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.small_font.render("Select Difficulty", True, COLORS['white'])
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 160))
        self.screen.blit(subtitle, subtitle_rect)

        # Difficulty options
        difficulties = [
            ("EASY", "10x16 board, slower speed"),
            ("MEDIUM", "12x20 board, normal speed"),
            ("HARD", "14x24 board, faster speed"),
        ]

        start_y = 220
        for i, (name, desc) in enumerate(difficulties):
            y = start_y + i * 80

            # Highlight selected option
            if i == self.menu_selection:
                pygame.draw.rect(self.screen, COLORS['menu_highlight'],
                               (self.screen_width // 2 - 150, y - 10, 300, 60),
                               border_radius=10)
                color = COLORS['title_color']
            else:
                color = COLORS['white']

            # Option name
            text = self.font.render(name, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, y + 10))
            self.screen.blit(text, text_rect)

            # Description
            desc_text = self.small_font.render(desc, True, COLORS['gray'])
            desc_rect = desc_text.get_rect(center=(self.screen_width // 2, y + 35))
            self.screen.blit(desc_text, desc_rect)

        # Instructions
        instructions = self.small_font.render("Use UP/DOWN to select, ENTER to start",
                                              True, COLORS['gray'])
        inst_rect = instructions.get_rect(center=(self.screen_width // 2,
                                                  self.screen_height - 40))
        self.screen.blit(instructions, inst_rect)

    def draw_board(self):
        """Draw the game board."""
        pygame.draw.rect(self.screen, COLORS['black'],
                        (0, 0, self.board_pixel_width, self.board_pixel_height))

        # Grid lines
        for x in range(self.board_width + 1):
            pygame.draw.line(self.screen, COLORS['grid_line'],
                           (x * CELL_SIZE, 0),
                           (x * CELL_SIZE, self.board_pixel_height))
        for y in range(self.board_height + 1):
            pygame.draw.line(self.screen, COLORS['grid_line'],
                           (0, y * CELL_SIZE),
                           (self.board_pixel_width, y * CELL_SIZE))

        # Animation parameters
        clear_scale = 1.0
        clear_flash = 0.0
        if self.line_clear_animating:
            progress = self.line_clear_anim_time / LINE_CLEAR_ANIM_DURATION
            if progress < 0.3:
                clear_flash = progress / 0.3
            elif progress < 0.5:
                clear_flash = 1.0
            else:
                shrink_progress = (progress - 0.5) / 0.5
                clear_scale = 1.0 - shrink_progress
                clear_flash = 1.0 - shrink_progress

        # Placed blocks
        for y in range(HIDDEN_ROWS, self.board_height + HIDDEN_ROWS):
            for x in range(self.board_width):
                if self.board.grid[y][x] is not None:
                    if y in self.clearing_lines:
                        self.draw_block_animated(x, y - HIDDEN_ROWS,
                                                self.board.grid[y][x],
                                                scale=clear_scale,
                                                flash=clear_flash)
                    else:
                        self.draw_block(x, y - HIDDEN_ROWS, self.board.grid[y][x])

        # Ghost piece
        if self.current_piece and self.state == STATE_PLAYING:
            ghost_y = self.board.get_ghost_position(self.current_piece)
            ghost_color = tuple(c // 4 for c in self.current_piece.color)
            for bx, by in self.current_piece.get_blocks(y=ghost_y):
                if by >= HIDDEN_ROWS:
                    self.draw_block(bx, by - HIDDEN_ROWS, ghost_color)

        # Current piece
        if self.current_piece and self.state == STATE_PLAYING:
            for bx, by in self.current_piece.get_blocks():
                if by >= HIDDEN_ROWS:
                    self.draw_block(bx, by - HIDDEN_ROWS, self.current_piece.color)

        # Board border
        pygame.draw.rect(self.screen, COLORS['white'],
                        (0, 0, self.board_pixel_width, self.board_pixel_height), 2)

    def draw_piece_preview(self, piece, x, y, label):
        """Draw a piece in the side panel."""
        text = self.small_font.render(label, True, COLORS['white'])
        self.screen.blit(text, (x, y))

        box_size = 4 * CELL_SIZE // 2
        box_y = y + 25
        pygame.draw.rect(self.screen, COLORS['dark_gray'],
                        (x, box_y, box_size + 10, box_size + 10))
        pygame.draw.rect(self.screen, COLORS['gray'],
                        (x, box_y, box_size + 10, box_size + 10), 1)

        if piece:
            blocks = piece.get_blocks(0, 0, 0)
            min_x = min(b[0] for b in blocks)
            max_x = max(b[0] for b in blocks)
            min_y = min(b[1] for b in blocks)
            max_y = max(b[1] for b in blocks)

            width = max_x - min_x + 1
            height = max_y - min_y + 1

            offset_x = x + 5 + (box_size - width * CELL_SIZE // 2) // 2
            offset_y = box_y + 5 + (box_size - height * CELL_SIZE // 2) // 2

            for bx, by in blocks:
                px = offset_x + (bx - min_x) * CELL_SIZE // 2
                py = offset_y + (by - min_y) * CELL_SIZE // 2
                color = COLORS[TETROMINOS[piece.type]['color']]
                pygame.draw.rect(self.screen, color,
                               (px, py, CELL_SIZE // 2 - 1, CELL_SIZE // 2 - 1))

    def draw_ui(self):
        """Draw the side panel UI."""
        panel_x = self.board_pixel_width + 10

        pygame.draw.rect(self.screen, COLORS['dark_gray'],
                        (self.board_pixel_width, 0, SIDE_PANEL_WIDTH, self.screen_height))

        self.draw_piece_preview(self.next_piece, panel_x, 10, "NEXT")
        self.draw_piece_preview(self.held_piece, panel_x, 120, "HOLD")

        # Difficulty indicator
        diff_text = self.small_font.render(f"Mode: {self.difficulty.upper()}",
                                           True, COLORS['title_color'])
        self.screen.blit(diff_text, (panel_x, 220))

        # Score
        y = 250
        labels = [
            ("SCORE", str(self.score)),
            ("LEVEL", str(self.level)),
            ("LINES", str(self.lines_cleared)),
        ]

        for label, value in labels:
            text = self.small_font.render(label, True, COLORS['gray'])
            self.screen.blit(text, (panel_x, y))
            text = self.font.render(value, True, COLORS['white'])
            self.screen.blit(text, (panel_x, y + 18))
            y += 55

        # Controls
        y = self.screen_height - 150
        controls = [
            "CONTROLS:",
            "Arrows: Move",
            "Up/X: Rotate CW",
            "Z: Rotate CCW",
            "Space: Hard drop",
            "C: Hold",
            "Esc: Menu",
        ]
        for line in controls:
            text = self.small_font.render(line, True, COLORS['gray'])
            self.screen.blit(text, (panel_x, y))
            y += 18

    def draw_pause_menu(self):
        """Draw pause menu overlay."""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill(COLORS['black'])
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("PAUSED", True, COLORS['white'])
        title_rect = title.get_rect(center=(self.screen_width // 2,
                                            self.screen_height // 2 - 60))
        self.screen.blit(title, title_rect)

        options = ["Resume", "Main Menu"]
        for i, opt in enumerate(options):
            y = self.screen_height // 2 + i * 50

            if i == self.pause_selection:
                color = COLORS['title_color']
                pygame.draw.rect(self.screen, COLORS['menu_highlight'],
                               (self.screen_width // 2 - 80, y - 15, 160, 40),
                               border_radius=5)
            else:
                color = COLORS['white']

            text = self.font.render(opt, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, y))
            self.screen.blit(text, text_rect)

    def draw_game_over(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill(COLORS['black'])
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("GAME OVER", True, COLORS['red'])
        title_rect = title.get_rect(center=(self.screen_width // 2,
                                            self.screen_height // 2 - 40))
        self.screen.blit(title, title_rect)

        score_text = self.font.render(f"Score: {self.score}", True, COLORS['white'])
        score_rect = score_text.get_rect(center=(self.screen_width // 2,
                                                  self.screen_height // 2))
        self.screen.blit(score_text, score_rect)

        hint = self.small_font.render("Press R to restart, ESC for menu",
                                      True, COLORS['gray'])
        hint_rect = hint.get_rect(center=(self.screen_width // 2,
                                          self.screen_height // 2 + 40))
        self.screen.blit(hint, hint_rect)

    def draw(self):
        """Draw everything based on current state."""
        if self.state == STATE_MENU:
            self.draw_menu()
        else:
            self.screen.fill(COLORS['black'])
            self.draw_board()
            self.draw_ui()

            if self.state == STATE_PAUSED:
                self.draw_pause_menu()
            elif self.state == STATE_GAME_OVER:
                self.draw_game_over()

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True

        while running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)

            if self.state == STATE_PLAYING:
                self.handle_input(dt)
                self.update(dt)

            self.draw()

        self.stop_music()
        pygame.quit()
        sys.exit()


# ============== MAIN ==============

if __name__ == "__main__":
    game = TetrisGame()
    game.run()
