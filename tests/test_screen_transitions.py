"""Tests for transitions between game screens."""

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


def press_key(game: Game, key: int) -> None:
    """Send a keyboard event to the active screen."""
    event = pygame.event.Event(
        pygame.KEYDOWN,
        key=key,
    )
    game.screen_manager.handle_event(event)


def test_game_starts_at_title_screen(game: Game) -> None:
    assert game.screen_manager.current_screen_name == "title"


def test_new_game_opens_character_creation(game: Game) -> None:
    press_key(game, pygame.K_RETURN)

    assert game.screen_manager.current_screen_name == "new_game"


def test_options_screen_opens(game: Game) -> None:
    press_key(game, pygame.K_DOWN)
    press_key(game, pygame.K_DOWN)
    press_key(game, pygame.K_RETURN)

    assert game.screen_manager.current_screen_name == "options"


def test_escape_from_placeholder_returns_to_title(
    game: Game,
) -> None:
    press_key(game, pygame.K_RETURN)
    assert game.screen_manager.current_screen_name == "new_game"

    press_key(game, pygame.K_ESCAPE)

    assert game.screen_manager.current_screen_name == "title"


def test_quit_menu_item_requests_shutdown(game: Game) -> None:
    press_key(game, pygame.K_DOWN)
    press_key(game, pygame.K_DOWN)
    press_key(game, pygame.K_DOWN)
    press_key(game, pygame.K_RETURN)

    assert game.screen_manager.quit_requested
