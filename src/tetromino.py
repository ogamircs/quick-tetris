"""Tetromino piece representation."""

from .constants import COLORS, TETROMINOS


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
