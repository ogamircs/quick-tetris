"""Tests for the Board class."""

import pytest
from src.board import Board
from src.tetromino import Tetromino
from src.constants import HIDDEN_ROWS


class TestBoardInitialization:
    """Tests for Board initialization."""

    def test_creates_board_with_correct_width(self):
        board = Board(width=10, height=20)
        assert board.width == 10

    def test_creates_board_with_correct_height(self):
        board = Board(width=10, height=20)
        assert board.height == 20

    def test_creates_grid_with_hidden_rows(self):
        board = Board(width=10, height=20)
        # Grid should include hidden rows
        assert len(board.grid) == 20 + HIDDEN_ROWS

    def test_creates_grid_with_correct_width(self):
        board = Board(width=10, height=20)
        for row in board.grid:
            assert len(row) == 10

    def test_creates_empty_grid(self):
        board = Board(width=10, height=20)
        for row in board.grid:
            for cell in row:
                assert cell is None


class TestBoardIsValidPosition:
    """Tests for Board.is_valid_position() method."""

    def test_valid_position_in_empty_board(self):
        board = Board(width=10, height=20)
        piece = Tetromino('T', board_width=10)
        piece.y = 5  # Move down from spawn
        assert board.is_valid_position(piece) is True

    def test_invalid_position_left_wall(self):
        board = Board(width=10, height=20)
        piece = Tetromino('I', board_width=10)
        piece.x = -2  # Too far left
        assert board.is_valid_position(piece) is False

    def test_invalid_position_right_wall(self):
        board = Board(width=10, height=20)
        piece = Tetromino('I', board_width=10)
        piece.x = 10  # Too far right
        assert board.is_valid_position(piece) is False

    def test_invalid_position_below_board(self):
        board = Board(width=10, height=20)
        piece = Tetromino('O', board_width=10)
        piece.y = 25  # Below board
        assert board.is_valid_position(piece) is False

    def test_invalid_position_collision_with_locked_piece(self):
        board = Board(width=10, height=20)
        # Place a block at position (5, 10)
        board.grid[10][5] = (255, 0, 0)  # Red block
        piece = Tetromino('O', board_width=10)
        piece.x = 4  # O piece will occupy (5, y) and (6, y)
        piece.y = 9  # Will have blocks at y=9 and y=10
        assert board.is_valid_position(piece) is False

    def test_valid_position_with_custom_coordinates(self):
        board = Board(width=10, height=20)
        piece = Tetromino('T', board_width=10)
        assert board.is_valid_position(piece, x=3, y=10) is True

    def test_valid_position_with_custom_rotation(self):
        board = Board(width=10, height=20)
        piece = Tetromino('I', board_width=10)
        # I piece vertical (rotation 1) at x=0 should be valid
        assert board.is_valid_position(piece, x=0, y=5, rotation=1) is True


class TestBoardLockPiece:
    """Tests for Board.lock_piece() method."""

    def test_locks_piece_blocks_to_grid(self):
        board = Board(width=10, height=20)
        piece = Tetromino('O', board_width=10)
        piece.x = 4
        piece.y = 10
        board.lock_piece(piece)

        # O piece at x=4, y=10 occupies: (5,10), (6,10), (5,11), (6,11)
        blocks = piece.get_blocks()
        for bx, by in blocks:
            assert board.grid[by][bx] == piece.color

    def test_locked_piece_has_correct_color(self):
        board = Board(width=10, height=20)
        piece = Tetromino('I', board_width=10)
        piece.y = 5
        expected_color = piece.color
        board.lock_piece(piece)

        blocks = piece.get_blocks()
        for bx, by in blocks:
            assert board.grid[by][bx] == expected_color


class TestBoardFindCompleteLines:
    """Tests for Board.find_complete_lines() method."""

    def test_no_complete_lines_in_empty_board(self):
        board = Board(width=10, height=20)
        assert board.find_complete_lines() == []

    def test_finds_single_complete_line(self):
        board = Board(width=10, height=20)
        # Fill one row completely
        row_index = 15
        for x in range(10):
            board.grid[row_index][x] = (255, 0, 0)

        complete = board.find_complete_lines()
        assert row_index in complete

    def test_finds_multiple_complete_lines(self):
        board = Board(width=10, height=20)
        # Fill two rows
        for row_index in [15, 17]:
            for x in range(10):
                board.grid[row_index][x] = (255, 0, 0)

        complete = board.find_complete_lines()
        assert 15 in complete
        assert 17 in complete
        assert len(complete) == 2

    def test_ignores_incomplete_lines(self):
        board = Board(width=10, height=20)
        # Fill row except one cell
        row_index = 15
        for x in range(9):  # Only 9 cells
            board.grid[row_index][x] = (255, 0, 0)

        complete = board.find_complete_lines()
        assert row_index not in complete


class TestBoardClearLines:
    """Tests for Board.clear_lines() method."""

    def test_clears_specified_lines(self):
        board = Board(width=10, height=20)
        # Fill one row
        row_index = 15
        for x in range(10):
            board.grid[row_index][x] = (255, 0, 0)

        cleared = board.clear_lines([row_index])
        assert cleared == 1
        # Row should now be empty (shifted from above)
        assert all(cell is None for cell in board.grid[row_index])

    def test_shifts_blocks_down_after_clear(self):
        board = Board(width=10, height=20)
        # Place a block above the line to clear
        board.grid[14][5] = (0, 255, 0)  # Green block at row 14
        # Fill row 15 completely
        for x in range(10):
            board.grid[15][x] = (255, 0, 0)

        board.clear_lines([15])
        # Green block should have shifted down from 14 to 15
        assert board.grid[15][5] == (0, 255, 0)

    def test_returns_number_of_cleared_lines(self):
        board = Board(width=10, height=20)
        # Fill two rows
        for row_index in [15, 16]:
            for x in range(10):
                board.grid[row_index][x] = (255, 0, 0)

        cleared = board.clear_lines([15, 16])
        assert cleared == 2

    def test_auto_finds_lines_when_none_specified(self):
        board = Board(width=10, height=20)
        # Fill one row
        row_index = 15
        for x in range(10):
            board.grid[row_index][x] = (255, 0, 0)

        cleared = board.clear_lines()  # No lines specified
        assert cleared == 1


class TestBoardIsGameOver:
    """Tests for Board.is_game_over() method."""

    def test_not_game_over_with_empty_board(self):
        board = Board(width=10, height=20)
        assert board.is_game_over() is False

    def test_not_game_over_with_blocks_in_visible_area(self):
        board = Board(width=10, height=20)
        # Place block in visible area (below hidden rows)
        board.grid[HIDDEN_ROWS + 5][5] = (255, 0, 0)
        assert board.is_game_over() is False

    def test_game_over_with_block_in_hidden_row(self):
        board = Board(width=10, height=20)
        # Place block in hidden row
        board.grid[0][5] = (255, 0, 0)
        assert board.is_game_over() is True

    def test_game_over_with_block_in_second_hidden_row(self):
        board = Board(width=10, height=20)
        # Place block in second hidden row
        board.grid[1][5] = (255, 0, 0)
        assert board.is_game_over() is True


class TestBoardGetGhostPosition:
    """Tests for Board.get_ghost_position() method."""

    def test_ghost_at_bottom_of_empty_board(self):
        board = Board(width=10, height=20)
        piece = Tetromino('O', board_width=10)
        piece.y = 0

        ghost_y = board.get_ghost_position(piece)
        # O piece is 2 tall, so ghost should be at height + hidden - 2
        # For O piece shape, blocks are at y and y+1
        # Maximum valid y is when y+1 = height + hidden - 1
        expected_y = board.height + HIDDEN_ROWS - 2
        assert ghost_y == expected_y

    def test_ghost_stops_at_locked_blocks(self):
        board = Board(width=10, height=20)
        # Place blocks to stop the piece
        for x in range(10):
            board.grid[15][x] = (255, 0, 0)

        piece = Tetromino('O', board_width=10)
        piece.x = 4
        piece.y = 0

        ghost_y = board.get_ghost_position(piece)
        # O piece should stop with its bottom row at y=14 (just above row 15)
        # O piece blocks at y=ghost_y would be at ghost_y and ghost_y+1
        # So ghost_y+1 must be < 15, meaning ghost_y = 13
        assert ghost_y == 13

    def test_ghost_position_same_as_current_when_landed(self):
        board = Board(width=10, height=20)
        piece = Tetromino('O', board_width=10)
        # Place piece at bottom
        piece.y = board.height + HIDDEN_ROWS - 2

        ghost_y = board.get_ghost_position(piece)
        assert ghost_y == piece.y
