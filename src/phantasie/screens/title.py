"""Title screen for Phantasie III."""

import pygame

from phantasie.menu import TitleMenu
from phantasie.screens.base import BaseScreen


class TitleScreen(BaseScreen):
    """Handle title screen input, updates, and rendering."""

    def __init__(self, on_new_game=None) -> None:
        """Initialize the title screen."""
        super().__init__()
        self.menu = TitleMenu()
        self.on_new_game = on_new_game

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle title screen input."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.next_screen = "quit"

        elif event.key in (pygame.K_UP, pygame.K_w):
            self.menu.move_selection(-1)

        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.menu.move_selection(1)

        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            action = self.menu.activate()

            if action in (
                "new_game",
                "party",
                "options",
                "character_creation",
            ):
                self.menu.status_message = ""
                if action == "new_game" and self.on_new_game is not None:
                    self.on_new_game()
                self.next_screen = action

            elif action == "continue":
                self.menu.status_message = "Continue is not implemented yet."

            elif action == "quit":
                self.next_screen = "quit"

    def update(self, dt: float) -> None:
        """Update title screen state."""
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        """Render the title screen."""
        self.menu.render(surface)
