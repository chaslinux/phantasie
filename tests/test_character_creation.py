"""Tests for the character creation screen."""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest

from phantasie.characters.models import Character, Profession, Race
from phantasie.game import Game
from phantasie.screens.character_creation import CharacterCreationScreen


@pytest.fixture
def game() -> Game:
    """Create a game instance for testing."""
    instance = Game()
    yield instance
    pygame.quit()


def press_key(game: Game, key: int, unicode: str | None = None) -> None:
    """Send a keyboard event to the active screen."""
    if unicode is None:
        unicode = chr(key) if pygame.K_a <= key <= pygame.K_z else ""

    event = pygame.event.Event(
        pygame.KEYDOWN,
        key=key,
        unicode=unicode,
    )
    game.screen_manager.handle_event(event)


def press_text(game: Game, text: str) -> None:
    """Send a text-input event to the active screen."""
    event = pygame.event.Event(
        pygame.TEXTINPUT,
        text=text,
    )
    game.screen_manager.handle_event(event)


def open_character_creation(game: Game) -> None:
    """Open character creation from the party-selection screen."""
    if game.screen_manager.current_screen_name == "title":
        press_key(game, pygame.K_RETURN)

    press_key(game, pygame.K_c)


def test_new_game_uses_character_creation_screen(game: Game) -> None:
    open_character_creation(game)

    assert isinstance(
        game.screen_manager.current_screen,
        CharacterCreationScreen,
    )


def test_character_creation_has_default_choices(game: Game) -> None:
    open_character_creation(game)

    screen = game.screen_manager.current_screen
    assert isinstance(screen, CharacterCreationScreen)
    assert screen.selected_race is Race.HUMAN
    assert screen.selected_profession is Profession.FIGHTER


def test_player_can_enter_character_name(game: Game) -> None:
    open_character_creation(game)
    press_text(game, "A")
    press_text(game, "d")
    press_text(game, "a")

    screen = game.screen_manager.current_screen
    assert isinstance(screen, CharacterCreationScreen)
    assert screen.name == "Ada"


def test_player_can_change_race(game: Game) -> None:
    open_character_creation(game)
    press_key(game, pygame.K_TAB)
    press_key(game, pygame.K_RIGHT)

    screen = game.screen_manager.current_screen
    assert isinstance(screen, CharacterCreationScreen)
    assert screen.selected_race is Race.DWARF


def test_player_can_change_profession(game: Game) -> None:
    open_character_creation(game)
    press_key(game, pygame.K_TAB)
    press_key(game, pygame.K_TAB)
    press_key(game, pygame.K_RIGHT)

    screen = game.screen_manager.current_screen
    assert isinstance(screen, CharacterCreationScreen)
    assert screen.selected_profession is Profession.MONK


def test_blank_name_cannot_be_confirmed(game: Game) -> None:
    open_character_creation(game)
    press_key(game, pygame.K_RETURN)

    assert (
        game.screen_manager.current_screen_name
        == "new_game_character_creation"
    )
    assert game.character is None


def test_confirmed_character_is_stored(game: Game) -> None:
    open_character_creation(game)
    press_text(game, "A")
    press_text(game, "d")
    press_text(game, "a")
    press_key(game, pygame.K_RETURN)

    assert game.screen_manager.current_screen_name == "new_game"
    assert isinstance(game.character, Character)
    assert game.character.name == "Ada"
    assert game.character.race is Race.HUMAN
    assert game.character.profession is Profession.FIGHTER
    assert game.party.member_count == 1
    assert game.party.members == (game.character,)


def test_escape_cancels_character_creation(game: Game) -> None:
    open_character_creation(game)
    press_key(game, pygame.K_ESCAPE)

    assert game.screen_manager.current_screen_name == "new_game"
    assert game.character is None
    assert game.party.member_count == 0


def test_multiple_characters_can_be_added_to_party(game: Game) -> None:
    press_key(game, pygame.K_RETURN)
    for name in ("Ada", "Borin"):
        press_key(game, pygame.K_c)

        screen = game.screen_manager.current_screen
        assert isinstance(screen, CharacterCreationScreen)

        # Clear any name retained from the previous character.
        for _ in range(len(screen.name)):
            press_key(game, pygame.K_BACKSPACE)

        for character in name:
            event = pygame.event.Event(
                pygame.TEXTINPUT,
                text=character,
            )
            game.screen_manager.handle_event(event)

        press_key(game, pygame.K_RETURN)

    assert game.party.member_count == 2
    assert [character.name for character in game.party.members] == [
        "Ada",
        "Borin",
    ]
    assert game.character is game.party.members[-1]
