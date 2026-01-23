"""Tests for the Tetromino class."""

import pytest
from src.tetromino import Tetromino
from src.constants import COLORS, TETROMINOS


class TestTetrominoInitialization:
    """Tests for Tetromino initialization."""

    def test_creates_tetromino_with_correct_type(self):
        piece = Tetromino('T', board_width=10)
        assert piece.type == 'T'

    def test_creates_tetromino_with_initial_rotation_zero(self):
        piece = Tetromino('I', board_width=10)
        assert piece.rotation == 0

    def test_creates_tetromino_with_correct_color(self):
        piece = Tetromino('T', board_width=10)
        expected_color = COLORS[TETROMINOS['T']['color']]
        assert piece.color == expected_color

    def test_centers_piece_horizontally_on_board(self):
        piece = Tetromino('O', board_width=10)
        # board_width // 2 - 2 = 10 // 2 - 2 = 3
        assert piece.x == 3

    def test_spawns_piece_at_top_of_board(self):
        piece = Tetromino('S', board_width=12)
        assert piece.y == 0

    def test_creates_all_seven_piece_types(self):
        piece_types = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        for piece_type in piece_types:
            piece = Tetromino(piece_type, board_width=10)
            assert piece.type == piece_type


class TestTetrominoGetBlocks:
    """Tests for Tetromino.get_blocks() method."""

    def test_returns_four_blocks_for_any_piece(self):
        for piece_type in TETROMINOS.keys():
            piece = Tetromino(piece_type, board_width=10)
            blocks = piece.get_blocks()
            assert len(blocks) == 4

    def test_returns_blocks_at_piece_position(self):
        piece = Tetromino('O', board_width=10)
        piece.x = 5
        piece.y = 3
        blocks = piece.get_blocks()
        # O piece shape at rotation 0: [(1, 0), (2, 0), (1, 1), (2, 1)]
        # With x=5, y=3: [(6, 3), (7, 3), (6, 4), (7, 4)]
        assert (6, 3) in blocks
        assert (7, 3) in blocks
        assert (6, 4) in blocks
        assert (7, 4) in blocks

    def test_returns_blocks_for_custom_position(self):
        piece = Tetromino('I', board_width=10)
        blocks = piece.get_blocks(x=0, y=0, rotation=0)
        # I piece at rotation 0: [(0, 1), (1, 1), (2, 1), (3, 1)]
        expected = [(0, 1), (1, 1), (2, 1), (3, 1)]
        assert sorted(blocks) == sorted(expected)

    def test_returns_blocks_for_different_rotations(self):
        piece = Tetromino('I', board_width=10)
        blocks_r0 = piece.get_blocks(x=0, y=0, rotation=0)
        blocks_r1 = piece.get_blocks(x=0, y=0, rotation=1)
        # Different rotations should give different block positions
        assert sorted(blocks_r0) != sorted(blocks_r1)


class TestTetrominoRotate:
    """Tests for Tetromino.rotate() method."""

    def test_rotates_clockwise_by_default(self):
        piece = Tetromino('T', board_width=10)
        assert piece.rotation == 0
        piece.rotate()
        assert piece.rotation == 1

    def test_rotates_counter_clockwise_with_negative_direction(self):
        piece = Tetromino('T', board_width=10)
        piece.rotation = 1
        piece.rotate(-1)
        assert piece.rotation == 0

    def test_wraps_rotation_from_3_to_0(self):
        piece = Tetromino('T', board_width=10)
        piece.rotation = 3
        piece.rotate(1)
        assert piece.rotation == 0

    def test_wraps_rotation_from_0_to_3(self):
        piece = Tetromino('T', board_width=10)
        piece.rotation = 0
        piece.rotate(-1)
        assert piece.rotation == 3

    def test_full_rotation_cycle_returns_to_start(self):
        piece = Tetromino('L', board_width=10)
        initial_rotation = piece.rotation
        for _ in range(4):
            piece.rotate()
        assert piece.rotation == initial_rotation


class TestTetrominoCopy:
    """Tests for Tetromino.copy() method."""

    def test_copy_has_same_type(self):
        original = Tetromino('J', board_width=10)
        copy = original.copy()
        assert copy.type == original.type

    def test_copy_has_same_position(self):
        original = Tetromino('Z', board_width=10)
        original.x = 5
        original.y = 10
        copy = original.copy()
        assert copy.x == original.x
        assert copy.y == original.y

    def test_copy_has_same_rotation(self):
        original = Tetromino('S', board_width=10)
        original.rotation = 2
        copy = original.copy()
        assert copy.rotation == original.rotation

    def test_copy_has_same_color(self):
        original = Tetromino('I', board_width=10)
        copy = original.copy()
        assert copy.color == original.color

    def test_copy_is_independent_of_original(self):
        original = Tetromino('T', board_width=10)
        copy = original.copy()
        copy.x = 100
        copy.y = 200
        copy.rotation = 3
        # Original should be unchanged
        assert original.x != 100
        assert original.y != 200
        assert original.rotation != 3
