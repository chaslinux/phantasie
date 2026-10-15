"""Base interface for game screens."""

from abc import ABC, abstractmethod

import pygame


class BaseScreen(ABC):
    """Common interface for all game screens."""

    def __init__(self) -> None:
        """Initialize the screen."""
        self.next_screen: str | None = None

    def on_enter(self) -> None:  # noqa: B027
        """Called when this screen becomes active."""

    def on_exit(self) -> None:  # noqa: B027
        """Called when this screen stops being active."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a Pygame event."""

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the screen state.

        Args:
            dt: Time elapsed since the previous frame, in seconds.
        """

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render the screen."""
