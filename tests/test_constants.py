"""Tests for the constants module."""

import pytest
from src.constants import (
    TETROMINOS, WALL_KICKS, DIFFICULTY_SETTINGS, COLORS,
    HIDDEN_ROWS, CELL_SIZE, SIDE_PANEL_WIDTH,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER,
)


class TestTetrominos:
    """Tests for TETROMINOS definitions."""

    def test_all_seven_pieces_defined(self):
        expected_pieces = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        for piece in expected_pieces:
            assert piece in TETROMINOS

    def test_each_piece_has_color(self):
        for piece_type, data in TETROMINOS.items():
            assert 'color' in data
            assert data['color'] in COLORS

    def test_each_piece_has_four_rotations(self):
        for piece_type, data in TETROMINOS.items():
            assert 'shapes' in data
            assert len(data['shapes']) == 4, f"{piece_type} should have 4 rotations"

    def test_each_rotation_has_four_blocks(self):
        for piece_type, data in TETROMINOS.items():
            for rotation_idx, shape in enumerate(data['shapes']):
                assert len(shape) == 4, f"{piece_type} rotation {rotation_idx} should have 4 blocks"

    def test_blocks_are_coordinate_tuples(self):
        for piece_type, data in TETROMINOS.items():
            for shape in data['shapes']:
                for block in shape:
                    assert isinstance(block, tuple)
                    assert len(block) == 2
                    assert isinstance(block[0], int)
                    assert isinstance(block[1], int)

    def test_o_piece_has_identical_rotations(self):
        # O piece should look the same in all rotations
        o_shapes = TETROMINOS['O']['shapes']
        for i in range(1, 4):
            assert sorted(o_shapes[0]) == sorted(o_shapes[i])


class TestWallKicks:
    """Tests for WALL_KICKS definitions."""

    def test_has_normal_and_i_piece_kicks(self):
        assert 'normal' in WALL_KICKS
        assert 'I' in WALL_KICKS

    def test_all_rotation_transitions_defined(self):
        # All possible rotation transitions: 0->1, 1->0, 1->2, 2->1, 2->3, 3->2, 3->0, 0->3
        expected_transitions = [
            (0, 1), (1, 0), (1, 2), (2, 1),
            (2, 3), (3, 2), (3, 0), (0, 3)
        ]
        for kick_type in ['normal', 'I']:
            for transition in expected_transitions:
                assert transition in WALL_KICKS[kick_type], \
                    f"Missing {transition} in {kick_type} wall kicks"

    def test_each_kick_has_five_attempts(self):
        for kick_type in ['normal', 'I']:
            for transition, kicks in WALL_KICKS[kick_type].items():
                assert len(kicks) == 5, f"{kick_type} {transition} should have 5 kick attempts"

    def test_first_kick_is_no_offset(self):
        # First kick attempt should always be (0, 0)
        for kick_type in ['normal', 'I']:
            for transition, kicks in WALL_KICKS[kick_type].items():
                assert kicks[0] == (0, 0), f"{kick_type} {transition} first kick should be (0,0)"


class TestDifficultySettings:
    """Tests for DIFFICULTY_SETTINGS definitions."""

    def test_all_difficulties_defined(self):
        expected = ['easy', 'medium', 'hard']
        for difficulty in expected:
            assert difficulty in DIFFICULTY_SETTINGS

    def test_each_difficulty_has_required_keys(self):
        required_keys = ['width', 'height', 'start_level', 'speed_mult']
        for difficulty, settings in DIFFICULTY_SETTINGS.items():
            for key in required_keys:
                assert key in settings, f"{difficulty} missing {key}"

    def test_easy_has_smaller_board(self):
        assert DIFFICULTY_SETTINGS['easy']['width'] < DIFFICULTY_SETTINGS['hard']['width']
        assert DIFFICULTY_SETTINGS['easy']['height'] < DIFFICULTY_SETTINGS['hard']['height']

    def test_hard_has_faster_speed(self):
        # Lower speed_mult = faster
        assert DIFFICULTY_SETTINGS['hard']['speed_mult'] < DIFFICULTY_SETTINGS['easy']['speed_mult']

    def test_board_dimensions_are_positive(self):
        for difficulty, settings in DIFFICULTY_SETTINGS.items():
            assert settings['width'] > 0
            assert settings['height'] > 0


class TestColors:
    """Tests for COLORS definitions."""

    def test_basic_colors_defined(self):
        basic_colors = ['black', 'white', 'gray', 'red', 'green', 'blue']
        for color in basic_colors:
            assert color in COLORS

    def test_tetromino_colors_defined(self):
        tetromino_colors = ['cyan', 'yellow', 'purple', 'orange']
        for color in tetromino_colors:
            assert color in COLORS

    def test_colors_are_rgb_tuples(self):
        for color_name, rgb in COLORS.items():
            assert isinstance(rgb, tuple), f"{color_name} should be tuple"
            assert len(rgb) == 3, f"{color_name} should have 3 components"
            for component in rgb:
                assert 0 <= component <= 255, f"{color_name} component out of range"


class TestGameStates:
    """Tests for game state constants."""

    def test_all_states_are_unique(self):
        states = [STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER]
        assert len(states) == len(set(states))

    def test_states_are_strings(self):
        for state in [STATE_MENU, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER]:
            assert isinstance(state, str)


class TestLayoutConstants:
    """Tests for layout constants."""

    def test_hidden_rows_is_positive(self):
        assert HIDDEN_ROWS > 0

    def test_cell_size_is_positive(self):
        assert CELL_SIZE > 0

    def test_side_panel_width_is_positive(self):
        assert SIDE_PANEL_WIDTH > 0
