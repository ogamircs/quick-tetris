"""Tests for the music module."""

import pytest
import pygame
from src.music import generate_tetris_music


@pytest.fixture(scope="module", autouse=True)
def init_pygame_mixer():
    """Initialize pygame mixer for music tests."""
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    yield
    pygame.mixer.quit()
    pygame.quit()


class TestGenerateTetrisMusic:
    """Tests for generate_tetris_music() function."""

    def test_returns_pygame_sound_object(self):
        sound = generate_tetris_music()
        assert isinstance(sound, pygame.mixer.Sound)

    def test_sound_has_positive_length(self):
        sound = generate_tetris_music()
        # Sound length should be greater than 0
        assert sound.get_length() > 0

    def test_sound_is_longer_than_one_second(self):
        sound = generate_tetris_music()
        # The melody should be at least a few seconds long
        assert sound.get_length() > 1.0

    def test_can_generate_multiple_times(self):
        # Should be able to call multiple times without error
        sound1 = generate_tetris_music()
        sound2 = generate_tetris_music()
        assert sound1 is not None
        assert sound2 is not None

    def test_sound_can_be_played(self):
        sound = generate_tetris_music()
        # Should not raise an exception when attempting to play
        channel = sound.play()
        if channel:
            channel.stop()
