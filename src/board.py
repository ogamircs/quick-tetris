"""Game board management."""

from .constants import HIDDEN_ROWS


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
