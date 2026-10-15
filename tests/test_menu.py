"""Tests for the title menu."""

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import pytest

from phantasie.menu import TitleMenu


@pytest.fixture
def menu() -> TitleMenu:
    """Create a title menu for testing."""
    pygame.init()
    instance = TitleMenu()

    yield instance

    pygame.quit()


def test_menu_starts_with_first_item_selected(
    menu: TitleMenu,
) -> None:
    assert menu.selected == 0
    assert menu.ITEMS[menu.selected] == "New Game"


def test_menu_moves_down(menu: TitleMenu) -> None:
    menu.move_selection(1)

    assert menu.selected == 1
    assert menu.ITEMS[menu.selected] == "Load Game"


def test_menu_moves_up(menu: TitleMenu) -> None:
    menu.move_selection(-1)

    assert menu.selected == len(menu.ITEMS) - 1
    assert menu.ITEMS[menu.selected] == "Quit"


def test_menu_selection_wraps(menu: TitleMenu) -> None:
    menu.move_selection(-1)
    menu.move_selection(1)

    assert menu.selected == 0


def test_new_game_returns_action(menu: TitleMenu) -> None:
    assert menu.activate() == "new_game"


def test_quit_returns_quit_action(menu: TitleMenu) -> None:
    menu.selected = len(menu.ITEMS) - 1

    assert menu.activate() == "quit"


def test_menu_renders(menu: TitleMenu) -> None:
    surface = pygame.Surface((320, 200))

    menu.render(surface)

    assert surface.get_size() == (320, 200)
