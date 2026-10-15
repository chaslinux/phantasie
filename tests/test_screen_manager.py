"""Tests for the screen manager."""

import pygame
import pytest

from phantasie.screen_manager import ScreenManager
from phantasie.screens.base import BaseScreen


class FakeScreen(BaseScreen):
    """Minimal screen for testing."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Ignore events."""

    def update(self, dt: float) -> None:
        """Request a transition if configured."""

    def render(self, surface: pygame.Surface) -> None:
        """Do nothing."""


def test_manager_registers_screen() -> None:
    manager = ScreenManager()
    screen = FakeScreen()

    manager.register("title", screen)

    assert manager.screens["title"] is screen


def test_manager_switches_screen() -> None:
    manager = ScreenManager()
    manager.register("title", FakeScreen())
    manager.register("options", FakeScreen())

    manager.switch_to("title")
    manager.switch_to("options")

    assert manager.current_screen_name == "options"


def test_manager_rejects_unknown_screen() -> None:
    manager = ScreenManager()

    with pytest.raises(KeyError):
        manager.switch_to("missing")


def test_manager_rejects_duplicate_screen() -> None:
    manager = ScreenManager()
    manager.register("title", FakeScreen())

    with pytest.raises(ValueError):
        manager.register("title", FakeScreen())


def test_current_screen_requires_active_screen() -> None:
    manager = ScreenManager()

    with pytest.raises(RuntimeError):
        _ = manager.current_screen
