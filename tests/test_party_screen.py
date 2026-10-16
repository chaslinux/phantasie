"""Tests for the party screen."""

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
from phantasie.screens.party import PartyScreen


@pytest.fixture
def pygame_ready():
    """Initialize and clean up Pygame for screen tests."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def party(pygame_ready) -> Party:
    """Create a party with two characters."""
    instance = Party()

    for name in ("Arin", "Borin"):
        instance.add_member(
            Character(
                name=name,
                race=Race.HUMAN,
                profession=Profession.FIGHTER,
                attributes=Attributes(12, 10, 11, 13, 9),
            )
        )

    return instance


def press_key(screen: PartyScreen, key: int) -> None:
    """Send a keyboard event directly to the party screen."""
    screen.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key))


def test_party_screen_starts_with_first_character(party: Party) -> None:
    screen = PartyScreen(party)

    assert screen.selected_index == 0
    assert screen.selected_character == party.members[0]


def test_party_screen_moves_selection_down(party: Party) -> None:
    screen = PartyScreen(party)

    press_key(screen, pygame.K_DOWN)

    assert screen.selected_index == 1
    assert screen.selected_character == party.members[1]


def test_party_screen_moves_selection_up(party: Party) -> None:
    screen = PartyScreen(party)

    press_key(screen, pygame.K_UP)

    assert screen.selected_index == 1
    assert screen.selected_character == party.members[1]


def test_party_screen_selection_wraps(party: Party) -> None:
    screen = PartyScreen(party)

    press_key(screen, pygame.K_DOWN)
    press_key(screen, pygame.K_DOWN)

    assert screen.selected_index == 0


def test_empty_party_has_no_selected_character(pygame_ready) -> None:
    screen = PartyScreen(Party())

    assert screen.selected_character is None

    press_key(screen, pygame.K_DOWN)
    press_key(screen, pygame.K_UP)

    assert screen.selected_index == 0


def test_escape_returns_to_title(party: Party) -> None:
    screen = PartyScreen(party)

    press_key(screen, pygame.K_ESCAPE)

    assert screen.next_screen == "title"


def test_party_screen_renders(party: Party) -> None:
    screen = PartyScreen(party)
    surface = pygame.Surface((320, 200))

    screen.render(surface)

    assert surface.get_size() == (320, 200)


def test_empty_party_renders(pygame_ready) -> None:
    screen = PartyScreen(Party())
    surface = pygame.Surface((320, 200))

    screen.render(surface)

    assert surface.get_size() == (320, 200)
