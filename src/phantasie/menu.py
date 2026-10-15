"""Title menu for Phantasie III."""

import pygame

from phantasie import palette


class TitleMenu:
    """Display and manage the title screen menu."""

    ITEMS = (
        "New Game",
        "Load Game",
        "Options",
        "Quit",
    )

    def __init__(self) -> None:
        """Initialize the title menu."""
        self.selected = 0
        self.status_message = ""

        self.title_font = pygame.font.Font(None, 32)
        self.menu_font = pygame.font.Font(None, 20)
        self.status_font = pygame.font.Font(None, 12)

    def move_selection(self, direction: int) -> None:
        """Move the selection through the menu."""
        self.selected = (self.selected + direction) % len(self.ITEMS)

        self.status_message = ""

    def activate(self) -> str:
        """Activate the selected menu item."""
        item = self.ITEMS[self.selected]

        if item == "Quit":
            return "quit"

        # These features will be implemented in later stages.
        self.status_message = f"{item} is not implemented yet."

        return item.lower().replace(" ", "_")

    def render(self, surface: pygame.Surface) -> None:
        """Draw the title menu."""
        surface.fill(palette.BACKGROUND)

        width, height = surface.get_size()

        # Decorative border.
        pygame.draw.rect(
            surface,
            palette.BORDER,
            (4, 4, width - 8, height - 8),
            width=1,
        )

        pygame.draw.rect(
            surface,
            palette.PURPLE,
            (8, 8, width - 16, height - 16),
            width=1,
        )

        # Game title.
        title = self.title_font.render(
            "PHANTASIE III",
            True,
            palette.HIGHLIGHT,
        )

        title_rect = title.get_rect(
            center=(width // 2, 45),
        )

        surface.blit(title, title_rect)

        subtitle = self.menu_font.render(
            "THE WRATH OF NIKADEMUS",
            True,
            palette.TEXT_MUTED,
        )

        subtitle_rect = subtitle.get_rect(
            center=(width // 2, 65),
        )

        surface.blit(subtitle, subtitle_rect)

        # Menu options.
        menu_y = 100
        line_height = 20

        for index, item in enumerate(self.ITEMS):
            is_selected = index == self.selected

            color = palette.HIGHLIGHT if is_selected else palette.TEXT

            prefix = ">" if is_selected else " "

            label = self.menu_font.render(
                f"{prefix} {item}",
                True,
                color,
            )

            label_rect = label.get_rect(
                center=(width // 2, menu_y + index * line_height),
            )

            surface.blit(label, label_rect)

        # Status or instructions.
        message = self.status_message or "UP/DOWN: SELECT    ENTER: CONFIRM"

        status = self.status_font.render(
            message,
            True,
            palette.TEXT_MUTED,
        )

        status_rect = status.get_rect(
            center=(width // 2, height - 22),
        )

        surface.blit(status, status_rect)
