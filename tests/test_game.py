"""Tests for the main game application."""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest

from phantasie.game import Game


@pytest.fixture
def game() -> Game:
    """Create a game instance for testing."""
    instance = Game()
    yield instance
    pygame.quit()


def test_game_initializes(game: Game) -> None:
    """The game should initialize its display and state."""
    assert game.running is True
    assert game.screen.get_size() == (Game.WIDTH, Game.HEIGHT)


def test_escape_key_stops_game(game: Game) -> None:
    """Pressing Escape should stop the application."""
    pygame.event.post(
        pygame.event.Event(
            pygame.KEYDOWN,
            key=pygame.K_ESCAPE,
        )
    )

    game.handle_events()

    assert game.running is False


def test_quit_event_stops_game(game: Game) -> None:
    """A window-close event should stop the application."""
    pygame.event.post(pygame.event.Event(pygame.QUIT))

    game.handle_events()

    assert game.running is False


def test_render_draws_a_frame(game: Game) -> None:
    """Rendering should complete without raising an exception."""
    game.render()
