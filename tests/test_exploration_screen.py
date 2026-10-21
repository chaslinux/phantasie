"""Tests for exploration controls, rendering, and game integration."""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest

from phantasie.characters.models import (
    Attributes,
    Character,
    Party,
    Profession,
    Race,
)
from phantasie.game import Game
from phantasie.screens.exploration import ExplorationScreen
from phantasie.world import ExplorationMap, ExplorationState


@pytest.fixture
def pygame_ready():
    """Initialize and clean up Pygame."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def party() -> Party:
    """Create a party with one character."""
    result = Party()
    result.add_member(
        Character(
            name="Arin",
            race=Race.HUMAN,
            profession=Profession.FIGHTER,
            attributes=Attributes(12, 10, 11, 13, 9),
        )
    )
    return result


@pytest.fixture
def exploration(pygame_ready, party):
    """Create an exploration screen and its state."""
    world = ExplorationMap()
    state = ExplorationState()
    screen = ExplorationScreen(world, state, lambda: party)
    return screen, world, state


def press_key(screen: ExplorationScreen, key: int) -> None:
    """Send a keyboard event to the exploration screen."""
    screen.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key))


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        (pygame.K_UP, (1, 0)),
        (pygame.K_w, (1, 0)),
        (pygame.K_DOWN, (1, 2)),
        (pygame.K_s, (1, 2)),
        (pygame.K_LEFT, (0, 1)),
        (pygame.K_a, (0, 1)),
        (pygame.K_RIGHT, (2, 1)),
        (pygame.K_d, (2, 1)),
    ],
)
def test_movement_keys(
    exploration,
    key: int,
    expected: tuple[int, int],
) -> None:
    screen, _, state = exploration

    press_key(screen, key)

    # Moving into the outer wall is blocked.
    if key in (pygame.K_UP, pygame.K_w, pygame.K_LEFT, pygame.K_a):
        assert (state.x, state.y) == (1, 1)
    else:
        assert (state.x, state.y) == expected


def test_blocked_movement_shows_message(exploration) -> None:
    screen, _, state = exploration
    state.x = 1
    state.y = 1

    press_key(screen, pygame.K_LEFT)

    assert (state.x, state.y) == (1, 1)
    assert screen.message == "YOU CANNOT GO THAT WAY."


def test_event_tile_shows_message(exploration) -> None:
    screen, _, state = exploration
    state.x = 7
    state.y = 6

    press_key(screen, pygame.K_RIGHT)

    assert (state.x, state.y) == (8, 6)
    assert state.event_seen
    assert screen.message == "YOU DISCOVER AN OLD WAYSTONE."


def test_escape_requests_title_transition(exploration) -> None:
    screen, _, _ = exploration

    press_key(screen, pygame.K_ESCAPE)

    assert screen.next_screen == "title"


def test_exploration_screen_renders(exploration) -> None:
    screen, _, _ = exploration
    surface = pygame.Surface((320, 200))

    screen.render(surface)

    assert surface.get_size() == (320, 200)


def test_screen_rejects_blocked_starting_position(party: Party) -> None:
    world = ExplorationMap()
    state = ExplorationState(x=0, y=0)

    with pytest.raises(ValueError, match="starting position"):
        ExplorationScreen(world, state, lambda: party)


def test_selected_party_enters_exploration_and_position_persists(
    pygame_ready,
) -> None:
    game = Game()

    character = Character(
        name="Arin",
        race=Race.HUMAN,
        profession=Profession.FIGHTER,
        attributes=Attributes(12, 10, 11, 13, 9),
    )
    game.party.add_member(character)

    new_game = game.screen_manager.screens["new_game"]
    new_game.selected_members.add(character)

    try:
        game.screen_manager.switch_to("new_game")
        new_game = game.screen_manager.current_screen
        new_game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f))
        game.screen_manager._process_transition()

        assert game.screen_manager.current_screen_name == "adventure"
        assert game.adventure_party.members == (character,)

        screen = game.screen_manager.current_screen
        assert isinstance(screen, ExplorationScreen)

        screen.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        assert (game.exploration_state.x, game.exploration_state.y) == (2, 1)

        game.screen_manager.switch_to("title")
        game.screen_manager.switch_to("adventure")

        assert (game.exploration_state.x, game.exploration_state.y) == (2, 1)
        assert screen.party_provider().members == (character,)
    finally:
        pygame.quit()


def test_blocked_movement_does_not_check_for_encounters(
    pygame_ready,
    party: Party,
) -> None:
    class UnexpectedEncounterGenerator:
        def generate(self):
            raise AssertionError("Blocked movement must not check encounters.")

    screen = ExplorationScreen(
        ExplorationMap(),
        ExplorationState(),
        lambda: party,
        UnexpectedEncounterGenerator(),  # type: ignore[arg-type]
    )

    press_key(screen, pygame.K_LEFT)

    assert screen.message == "YOU CANNOT GO THAT WAY."


def test_waystone_event_does_not_check_for_random_encounters(
    pygame_ready,
    party: Party,
) -> None:
    class UnexpectedEncounterGenerator:
        def generate(self):
            raise AssertionError("Waystone events must not check encounters.")

    screen = ExplorationScreen(
        ExplorationMap(),
        ExplorationState(x=7, y=6),
        lambda: party,
        UnexpectedEncounterGenerator(),  # type: ignore[arg-type]
    )

    press_key(screen, pygame.K_RIGHT)

    assert screen.message == "YOU DISCOVER AN OLD WAYSTONE."
