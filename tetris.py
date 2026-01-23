"""
Tetris Game in Python with Pygame
A complete implementation featuring:
- All 7 tetromino pieces with SRS rotation
- Wall kick system
- Ghost piece preview
- Hold piece functionality
- Next piece preview
- Scoring system with levels
- Increasing difficulty
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# ============== CONSTANTS ==============

# Board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
HIDDEN_ROWS = 2  # Hidden rows above visible area for spawning

# Cell and screen dimensions
CELL_SIZE = 30
BOARD_PIXEL_WIDTH = BOARD_WIDTH * CELL_SIZE
BOARD_PIXEL_HEIGHT = BOARD_HEIGHT * CELL_SIZE

# UI panel dimensions
SIDE_PANEL_WIDTH = 200
SCREEN_WIDTH = BOARD_PIXEL_WIDTH + SIDE_PANEL_WIDTH
SCREEN_HEIGHT = BOARD_PIXEL_HEIGHT

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
}

# Timing (milliseconds)
INITIAL_FALL_SPEED = 1000  # 1 second per drop
SOFT_DROP_SPEED = 50       # Fast drop speed
LOCK_DELAY = 500           # Time before piece locks after landing
DAS_DELAY = 170            # Delayed Auto Shift initial delay
DAS_REPEAT = 50            # DAS repeat rate
HARD_DROP_ANIM_SPEED = 15  # Milliseconds per row during hard drop animation

# Scoring
SCORE_SINGLE = 100
SCORE_DOUBLE = 300
SCORE_TRIPLE = 500
SCORE_TETRIS = 800
SOFT_DROP_SCORE = 1
HARD_DROP_SCORE = 2

# ============== TETROMINO DEFINITIONS ==============

# Each tetromino defined with 4 rotation states
# Coordinates are relative to piece center
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
# Format: (dx, dy) offsets to try when rotation fails
WALL_KICKS = {
    # For J, L, S, T, Z pieces
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
    # For I piece
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


# ============== TETROMINO CLASS ==============

class Tetromino:
    """Represents a falling tetromino piece."""

    def __init__(self, piece_type):
        self.type = piece_type
        self.rotation = 0
        self.color = COLORS[TETROMINOS[piece_type]['color']]
        # Spawn position (centered at top)
        self.x = BOARD_WIDTH // 2 - 2
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
        new_piece = Tetromino(self.type)
        new_piece.rotation = self.rotation
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece


# ============== BOARD CLASS ==============

class Board:
    """Manages the game board/grid."""

    def __init__(self):
        # Grid: None = empty, color tuple = filled
        self.grid = [[None for _ in range(BOARD_WIDTH)]
                     for _ in range(BOARD_HEIGHT + HIDDEN_ROWS)]

    def is_valid_position(self, piece, x=None, y=None, rotation=None):
        """Check if piece position is valid (no collisions, within bounds)."""
        blocks = piece.get_blocks(rotation, x, y)

        for bx, by in blocks:
            # Check horizontal bounds
            if bx < 0 or bx >= BOARD_WIDTH:
                return False
            # Check vertical bounds (allow above board for spawning)
            if by >= BOARD_HEIGHT + HIDDEN_ROWS:
                return False
            # Check collision with placed blocks
            if by >= 0 and self.grid[by][bx] is not None:
                return False

        return True

    def lock_piece(self, piece):
        """Lock a piece into the grid."""
        blocks = piece.get_blocks()
        for bx, by in blocks:
            if 0 <= by < BOARD_HEIGHT + HIDDEN_ROWS:
                self.grid[by][bx] = piece.color

    def clear_lines(self):
        """Clear completed lines and return number cleared."""
        lines_cleared = 0
        y = BOARD_HEIGHT + HIDDEN_ROWS - 1

        while y >= 0:
            if all(cell is not None for cell in self.grid[y]):
                # Remove the line
                del self.grid[y]
                # Add empty line at top
                self.grid.insert(0, [None for _ in range(BOARD_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1

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
        # Display setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Game state
        self.reset_game()

    def reset_game(self):
        """Reset/initialize game state."""
        self.board = Board()
        self.bag = []  # For 7-bag randomizer
        self.current_piece = self.get_next_piece()
        self.next_piece = self.get_next_piece()
        self.held_piece = None
        self.can_hold = True

        # Scoring
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.combo = 0

        # Timing
        self.fall_time = 0
        self.lock_time = 0
        self.is_locking = False
        self.lock_moves = 0  # Track moves during lock delay

        # Input handling
        self.das_time = 0
        self.das_direction = 0
        self.das_charged = False

        # Game state
        self.game_over = False
        self.paused = False

        # Hard drop animation
        self.hard_drop_animating = False
        self.hard_drop_target_y = 0
        self.hard_drop_anim_time = 0
        self.hard_drop_score_pending = 0

    def get_next_piece(self):
        """Get next piece using 7-bag randomizer."""
        if not self.bag:
            self.bag = list(TETROMINOS.keys())
            random.shuffle(self.bag)
        return Tetromino(self.bag.pop())

    def get_fall_speed(self):
        """Calculate fall speed based on level."""
        # Speed increases with level
        return max(100, INITIAL_FALL_SPEED - (self.level - 1) * 80)

    def try_wall_kick(self, piece, old_rotation, new_rotation):
        """Try wall kicks for rotation. Returns True if successful."""
        kick_type = 'I' if piece.type == 'I' else 'normal'
        kick_key = (old_rotation, new_rotation)

        if kick_key not in WALL_KICKS[kick_type]:
            return False

        kicks = WALL_KICKS[kick_type][kick_key]

        for dx, dy in kicks:
            new_x = piece.x + dx
            new_y = piece.y - dy  # Note: Tetris uses inverted y for kicks

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

        # Try basic rotation first
        if self.board.is_valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece.rotation = new_rotation
            self.on_piece_moved()
            return True

        # Try wall kicks
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

        # Calculate target position and score
        target_y = self.board.get_ghost_position(self.current_piece)
        drop_distance = target_y - self.current_piece.y

        if drop_distance > 0:
            # Start animation
            self.hard_drop_animating = True
            self.hard_drop_target_y = target_y
            self.hard_drop_anim_time = 0
            self.hard_drop_score_pending = drop_distance * HARD_DROP_SCORE
        else:
            # Already at bottom, just lock
            self.lock_piece()

    def hold_piece(self):
        """Hold current piece."""
        if not self.can_hold or self.current_piece is None:
            return

        self.can_hold = False

        if self.held_piece is None:
            self.held_piece = Tetromino(self.current_piece.type)
            self.current_piece = self.next_piece
            self.next_piece = self.get_next_piece()
        else:
            # Swap current and held
            held_type = self.held_piece.type
            self.held_piece = Tetromino(self.current_piece.type)
            self.current_piece = Tetromino(held_type)

        # Reset piece position
        self.current_piece.x = BOARD_WIDTH // 2 - 2
        self.current_piece.y = 0
        self.is_locking = False

    def on_piece_moved(self):
        """Called when piece is moved/rotated during lock delay."""
        if self.is_locking:
            self.lock_time = 0
            self.lock_moves += 1
            # Limit lock delay resets
            if self.lock_moves >= 15:
                self.lock_piece()

    def lock_piece(self):
        """Lock current piece and spawn next."""
        if self.current_piece is None:
            return

        self.board.lock_piece(self.current_piece)

        # Clear lines
        lines = self.board.clear_lines()
        if lines > 0:
            self.lines_cleared += lines
            self.combo += 1
            # Scoring
            base_scores = {1: SCORE_SINGLE, 2: SCORE_DOUBLE,
                         3: SCORE_TRIPLE, 4: SCORE_TETRIS}
            self.score += base_scores.get(lines, 0) * self.level
            # Combo bonus
            if self.combo > 1:
                self.score += 50 * self.combo * self.level
            # Level up every 10 lines
            self.level = self.lines_cleared // 10 + 1
        else:
            self.combo = 0

        # Check game over
        if self.board.is_game_over():
            self.game_over = True
            return

        # Spawn next piece
        self.current_piece = self.next_piece
        self.next_piece = self.get_next_piece()
        self.can_hold = True
        self.is_locking = False
        self.lock_moves = 0

        # Check if new piece can spawn
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True

    def update(self, dt):
        """Update game state."""
        if self.game_over or self.paused or self.current_piece is None:
            return

        # Hard drop animation
        if self.hard_drop_animating:
            self.hard_drop_anim_time += dt
            # Move piece down one row per HARD_DROP_ANIM_SPEED ms
            while self.hard_drop_anim_time >= HARD_DROP_ANIM_SPEED:
                self.hard_drop_anim_time -= HARD_DROP_ANIM_SPEED
                if self.current_piece.y < self.hard_drop_target_y:
                    self.current_piece.y += 1
                else:
                    # Animation complete
                    self.hard_drop_animating = False
                    self.score += self.hard_drop_score_pending
                    self.hard_drop_score_pending = 0
                    self.lock_piece()
                    break
            return  # Don't process normal gravity during animation

        # Gravity
        self.fall_time += dt
        fall_speed = self.get_fall_speed()

        if self.fall_time >= fall_speed:
            self.fall_time = 0
            if not self.soft_drop():
                # Piece can't move down, start/continue lock delay
                self.is_locking = True

        # Lock delay
        if self.is_locking:
            self.lock_time += dt
            if self.lock_time >= LOCK_DELAY:
                self.lock_piece()

    def handle_input(self, dt):
        """Handle keyboard input."""
        # Block input during hard drop animation
        if self.hard_drop_animating:
            return

        keys = pygame.key.get_pressed()

        # DAS (Delayed Auto Shift) for horizontal movement
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

        # Soft drop (continuous)
        if keys[pygame.K_DOWN]:
            self.fall_time += SOFT_DROP_SPEED

    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused

            if self.game_over:
                if event.key == pygame.K_r:
                    self.reset_game()
                return

            if self.paused or self.hard_drop_animating:
                return

            if event.key == pygame.K_UP or event.key == pygame.K_x:
                self.rotate_piece(1)  # Clockwise
            elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                self.rotate_piece(-1)  # Counter-clockwise
            elif event.key == pygame.K_SPACE:
                self.hard_drop()
            elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
                self.hold_piece()
            elif event.key == pygame.K_r:
                self.reset_game()

    def draw_block(self, x, y, color, surface=None, offset_x=0, offset_y=0):
        """Draw a single block with 3D effect."""
        if surface is None:
            surface = self.screen

        px = offset_x + x * CELL_SIZE
        py = offset_y + y * CELL_SIZE

        # Main block
        pygame.draw.rect(surface, color,
                        (px + 1, py + 1, CELL_SIZE - 2, CELL_SIZE - 2))

        # Highlight (top-left)
        highlight = tuple(min(255, c + 50) for c in color)
        pygame.draw.line(surface, highlight, (px + 1, py + 1),
                        (px + CELL_SIZE - 2, py + 1), 2)
        pygame.draw.line(surface, highlight, (px + 1, py + 1),
                        (px + 1, py + CELL_SIZE - 2), 2)

        # Shadow (bottom-right)
        shadow = tuple(max(0, c - 50) for c in color)
        pygame.draw.line(surface, shadow,
                        (px + CELL_SIZE - 2, py + 2),
                        (px + CELL_SIZE - 2, py + CELL_SIZE - 2), 2)
        pygame.draw.line(surface, shadow,
                        (px + 2, py + CELL_SIZE - 2),
                        (px + CELL_SIZE - 2, py + CELL_SIZE - 2), 2)

    def draw_board(self):
        """Draw the game board."""
        # Board background
        pygame.draw.rect(self.screen, COLORS['black'],
                        (0, 0, BOARD_PIXEL_WIDTH, BOARD_PIXEL_HEIGHT))

        # Grid lines
        for x in range(BOARD_WIDTH + 1):
            pygame.draw.line(self.screen, COLORS['grid_line'],
                           (x * CELL_SIZE, 0),
                           (x * CELL_SIZE, BOARD_PIXEL_HEIGHT))
        for y in range(BOARD_HEIGHT + 1):
            pygame.draw.line(self.screen, COLORS['grid_line'],
                           (0, y * CELL_SIZE),
                           (BOARD_PIXEL_WIDTH, y * CELL_SIZE))

        # Placed blocks
        for y in range(HIDDEN_ROWS, BOARD_HEIGHT + HIDDEN_ROWS):
            for x in range(BOARD_WIDTH):
                if self.board.grid[y][x] is not None:
                    self.draw_block(x, y - HIDDEN_ROWS, self.board.grid[y][x])

        # Ghost piece
        if self.current_piece and not self.game_over:
            ghost_y = self.board.get_ghost_position(self.current_piece)
            ghost_color = tuple(c // 4 for c in self.current_piece.color)
            for bx, by in self.current_piece.get_blocks(y=ghost_y):
                if by >= HIDDEN_ROWS:
                    self.draw_block(bx, by - HIDDEN_ROWS, ghost_color)

        # Current piece
        if self.current_piece and not self.game_over:
            for bx, by in self.current_piece.get_blocks():
                if by >= HIDDEN_ROWS:
                    self.draw_block(bx, by - HIDDEN_ROWS, self.current_piece.color)

        # Board border
        pygame.draw.rect(self.screen, COLORS['white'],
                        (0, 0, BOARD_PIXEL_WIDTH, BOARD_PIXEL_HEIGHT), 2)

    def draw_piece_preview(self, piece, x, y, label):
        """Draw a piece in the side panel."""
        # Label
        text = self.small_font.render(label, True, COLORS['white'])
        self.screen.blit(text, (x, y))

        # Preview box
        box_size = 4 * CELL_SIZE // 2
        box_y = y + 25
        pygame.draw.rect(self.screen, COLORS['dark_gray'],
                        (x, box_y, box_size + 10, box_size + 10))
        pygame.draw.rect(self.screen, COLORS['gray'],
                        (x, box_y, box_size + 10, box_size + 10), 1)

        if piece:
            # Draw piece centered in box
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
        panel_x = BOARD_PIXEL_WIDTH + 10

        # Background
        pygame.draw.rect(self.screen, COLORS['dark_gray'],
                        (BOARD_PIXEL_WIDTH, 0, SIDE_PANEL_WIDTH, SCREEN_HEIGHT))

        # Next piece
        self.draw_piece_preview(self.next_piece, panel_x, 10, "NEXT")

        # Hold piece
        self.draw_piece_preview(self.held_piece, panel_x, 120, "HOLD")

        # Score
        y = 240
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

        # Controls help
        y = SCREEN_HEIGHT - 170
        controls = [
            "CONTROLS:",
            "Arrow keys: Move",
            "Up/X: Rotate CW",
            "Z/Ctrl: Rotate CCW",
            "Space: Hard drop",
            "C/Shift: Hold",
            "Esc: Pause",
            "R: Restart",
        ]
        for line in controls:
            text = self.small_font.render(line, True, COLORS['gray'])
            self.screen.blit(text, (panel_x, y))
            y += 20

    def draw_overlay(self, text, subtext=""):
        """Draw an overlay with text (for pause/game over)."""
        # Dim background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(COLORS['black'])
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # Main text
        text_surface = self.font.render(text, True, COLORS['white'])
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2,
                                                   SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(text_surface, text_rect)

        # Subtext
        if subtext:
            sub_surface = self.small_font.render(subtext, True, COLORS['light_gray'])
            sub_rect = sub_surface.get_rect(center=(SCREEN_WIDTH // 2,
                                                    SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(sub_surface, sub_rect)

    def draw(self):
        """Draw everything."""
        self.screen.fill(COLORS['black'])
        self.draw_board()
        self.draw_ui()

        if self.paused:
            self.draw_overlay("PAUSED", "Press ESC to resume")
        elif self.game_over:
            self.draw_overlay("GAME OVER", f"Score: {self.score} - Press R to restart")

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        running = True

        while running:
            dt = self.clock.tick(60)  # 60 FPS, dt in milliseconds

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)

            # Input and update
            if not self.game_over and not self.paused:
                self.handle_input(dt)
                self.update(dt)

            # Draw
            self.draw()

        pygame.quit()
        sys.exit()


# ============== MAIN ==============

if __name__ == "__main__":
    game = TetrisGame()
    game.run()
