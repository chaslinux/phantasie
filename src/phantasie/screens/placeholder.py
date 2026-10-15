"""Temporary screens for unfinished game features."""

import pygame

from phantasie import palette
from phantasie.screens.base import BaseScreen


class PlaceholderScreen(BaseScreen):
    """Display a message for a feature that is not implemented yet."""

    def __init__(
        self,
        title: str,
        message: str,
        return_screen: str = "title",
    ) -> None:
        """Initialize a placeholder screen."""
        super().__init__()

        self.title = title
        self.message = message
        self.return_screen = return_screen

        self.title_font = pygame.font.Font(None, 28)
        self.message_font = pygame.font.Font(None, 18)
        self.instruction_font = pygame.font.Font(None, 14)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Return to the previous screen when requested."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (
            pygame.K_ESCAPE,
            pygame.K_RETURN,
            pygame.K_SPACE,
        ):
            self.next_screen = self.return_screen

    def update(self, dt: float) -> None:
        """Update the placeholder screen."""
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        """Render the placeholder screen."""
        surface.fill(palette.BACKGROUND)

        width, height = surface.get_size()

        pygame.draw.rect(
            surface,
            palette.BORDER,
            (4, 4, width - 8, height - 8),
            width=1,
        )

        title_surface = self.title_font.render(
            self.title,
            True,
            palette.HIGHLIGHT,
        )

        title_rect = title_surface.get_rect(
            center=(width // 2, height // 2 - 24),
        )

        surface.blit(title_surface, title_rect)

        message_surface = self.message_font.render(
            self.message,
            True,
            palette.TEXT,
        )

        message_rect = message_surface.get_rect(
            center=(width // 2, height // 2 + 4),
        )

        surface.blit(message_surface, message_rect)

        instruction_surface = self.instruction_font.render(
            "ENTER OR ESCAPE TO RETURN",
            True,
            palette.TEXT_MUTED,
        )

        instruction_rect = instruction_surface.get_rect(
            center=(width // 2, height - 24),
        )

        surface.blit(instruction_surface, instruction_rect)
