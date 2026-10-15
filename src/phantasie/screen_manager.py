"""Manage game screens and transitions."""

import pygame

from phantasie.screens.base import BaseScreen


class ScreenManager:
    """Register, activate, and update game screens."""

    def __init__(self) -> None:
        """Initialize the screen manager."""
        self.screens: dict[str, BaseScreen] = {}
        self.current_screen_name: str | None = None
        self.quit_requested = False

    @property
    def current_screen(self) -> BaseScreen:
        """Return the active screen."""
        if self.current_screen_name is None:
            raise RuntimeError("No screen is currently active.")

        return self.screens[self.current_screen_name]

    def register(self, name: str, screen: BaseScreen) -> None:
        """Register a screen under a unique name."""
        if name in self.screens:
            raise ValueError(f"Screen '{name}' is already registered.")

        self.screens[name] = screen

    def switch_to(self, name: str) -> None:
        """Deactivate the current screen and activate another."""
        if name not in self.screens:
            raise KeyError(f"Screen '{name}' is not registered.")

        if name == self.current_screen_name:
            return

        if self.current_screen_name is not None:
            self.current_screen.on_exit()

        self.current_screen_name = name
        self.current_screen.next_screen = None
        self.current_screen.on_enter()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Send an event to the active screen."""
        self.current_screen.handle_event(event)
        self._process_transition()

    def update(self, dt: float) -> None:
        """Update the active screen and process transitions."""
        self.current_screen.update(dt)
        self._process_transition()

    def _process_transition(self) -> None:
        """Process a screen transition requested by the active screen."""
        next_screen = self.current_screen.next_screen

        if next_screen is None:
            return

        if next_screen == "quit":
            self.current_screen.next_screen = None
            self.quit_requested = True
            return

        self.switch_to(next_screen)

    def render(self, surface: pygame.Surface) -> None:
        """Render the active screen."""
        self.current_screen.render(surface)
