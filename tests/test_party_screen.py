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


def test_large_party_scrolls_to_keep_selection_visible(
    pygame_ready,
    monkeypatch,
) -> None:
    party = Party()

    for index in range(12):
        party.add_member(
            Character(
                name=f"Member {index:02}",
                race=Race.HUMAN,
                profession=Profession.FIGHTER,
                attributes=Attributes(12, 10, 11, 13, 9),
            )
        )

    screen = PartyScreen(party)
    screen.selected_index = 9

    drawn_text: list[tuple[str, tuple[int, int]]] = []
    original_draw_text = screen._draw_text

    def capture_text(
        surface: pygame.Surface,
        text: str,
        position: tuple[int, int],
        color: tuple[int, int, int],
        font: pygame.font.Font | None = None,
    ) -> None:
        drawn_text.append((text, position))
        original_draw_text(surface, text, position, color, font)

    monkeypatch.setattr(screen, "_draw_text", capture_text)
    screen.render(pygame.Surface((320, 200)))

    roster = [text for text, (x, y) in drawn_text if x == 12 and 38 <= y < 38 + 8 * 13]

    assert len(roster) == 8
    assert any(text == "> Member 09" for text in roster)
    assert any(text.endswith("Member 11") for text in roster)
