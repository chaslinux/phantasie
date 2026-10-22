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


def test_reset_adventure_clears_progress_and_preserves_roster(
    game: Game,
) -> None:
    from phantasie.characters.models import (
        Attributes,
        Character,
        Profession,
        Race,
    )
    from phantasie.encounters import DEFAULT_MONSTERS
    from phantasie.screens.exploration import ExplorationScreen
    from phantasie.screens.new_game import NewGameScreen

    character = Character(
        name="Arin",
        race=Race.HUMAN,
        profession=Profession.FIGHTER,
        attributes=Attributes(12, 10, 11, 13, 9),
    )
    game.party.add_member(character)
    game.adventure_party.add_member(character)

    game.exploration_state.x = 8
    game.exploration_state.y = 6
    game.exploration_state.event_seen = True

    adventure = game.screen_manager.screens["adventure"]
    new_game = game.screen_manager.screens["new_game"]

    assert isinstance(adventure, ExplorationScreen)
    assert isinstance(new_game, NewGameScreen)

    adventure.active_encounter = DEFAULT_MONSTERS[0]
    adventure.message = "A WILD GOBLIN APPEARS!"
    new_game.selected_members.add(character)
    new_game.selected_index = 1
    new_game.message = "STALE MESSAGE"

    game._reset_adventure()

    assert (game.exploration_state.x, game.exploration_state.y) == (1, 1)
    assert game.exploration_state.event_seen is False
    assert game.adventure_party.members == ()
    assert adventure.active_encounter is None
    assert adventure.message == "EXPLORE THE AREA."
    assert new_game.selected_members == set()
    assert new_game.selected_index == 0
    assert new_game.message == ""
    assert game.party.members == (character,)


def test_selecting_new_game_resets_previous_adventure(game: Game) -> None:
    from phantasie.characters.models import (
        Attributes,
        Character,
        Profession,
        Race,
    )

    character = Character(
        name="Arin",
        race=Race.HUMAN,
        profession=Profession.FIGHTER,
        attributes=Attributes(12, 10, 11, 13, 9),
    )
    game.party.add_member(character)
    game.adventure_party.add_member(character)

    game.exploration_state.x = 4
    game.exploration_state.y = 3
    game.exploration_state.event_seen = True

    title = game.screen_manager.current_screen
    title.menu.selected_index = 0

    game.screen_manager.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert game.screen_manager.current_screen_name == "new_game"
    assert (game.exploration_state.x, game.exploration_state.y) == (1, 1)
    assert game.exploration_state.event_seen is False
    assert game.adventure_party.members == ()
    assert game.party.members == (character,)


def test_returning_to_title_does_not_reset_adventure(game: Game) -> None:
    game.exploration_state.x = 4
    game.exploration_state.y = 3
    game.exploration_state.event_seen = True

    game.screen_manager.switch_to("adventure")
    game.screen_manager.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    )

    assert game.screen_manager.current_screen_name == "title"
    assert (game.exploration_state.x, game.exploration_state.y) == (4, 3)
    assert game.exploration_state.event_seen is True


def test_starting_new_adventure_replaces_previous_party(game: Game) -> None:
    from phantasie.characters.models import (
        Attributes,
        Character,
        Profession,
        Race,
    )

    first = Character(
        name="Arin",
        race=Race.HUMAN,
        profession=Profession.FIGHTER,
        attributes=Attributes(12, 10, 11, 13, 9),
    )
    second = Character(
        name="Borin",
        race=Race.HUMAN,
        profession=Profession.FIGHTER,
        attributes=Attributes(11, 12, 10, 13, 9),
    )

    game.party.add_member(first)
    game.party.add_member(second)

    game._start_adventure((first,))
    assert game.adventure_party.members == (first,)

    game._reset_adventure()
    game._start_adventure((second,))

    assert game.adventure_party.members == (second,)
    assert game.party.members == (first, second)
