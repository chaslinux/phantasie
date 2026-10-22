"""Adventure party selection screen."""

from collections.abc import Callable

import pygame

from phantasie import palette
from phantasie.characters.models import Character, Party
from phantasie.screens.base import BaseScreen


class NewGameScreen(BaseScreen):
    """Let the player assemble a party before starting an adventure."""

    def __init__(
        self,
        roster: Party,
        on_start: Callable[[tuple[Character, ...]], None],
    ) -> None:
        """Initialize adventure setup."""
        super().__init__()
        self.roster = roster
        self.on_start = on_start
        self.selected_index = 0
        self.selected_members: set[Character] = set()
        self.message = ""

        self.title_font = pygame.font.Font(None, 24)
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle party selection and adventure setup."""
        if event.type != pygame.KEYDOWN:
            return

        members = self.roster.members

        if event.key == pygame.K_ESCAPE:
            self.next_screen = "title"
        elif event.key in (pygame.K_UP, pygame.K_w):
            if members:
                self.selected_index = (self.selected_index - 1) % len(members)
            self.message = ""
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            if members:
                self.selected_index = (self.selected_index + 1) % len(members)
            self.message = ""
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if not members:
                self.message = "CREATE A CHARACTER FIRST."
                return

            character = members[self.selected_index]

            if character in self.selected_members:
                self.selected_members.remove(character)
            else:
                self.selected_members.add(character)

            self.message = ""
        elif event.key == pygame.K_c:
            self.next_screen = "new_game_character_creation"
        elif event.key == pygame.K_f:
            self._start_adventure()

    def _start_adventure(self) -> None:
        """Start the adventure if at least one character is selected."""
        if not self.selected_members:
            self.message = "SELECT AT LEAST ONE CHARACTER."
            return

        ordered_members = tuple(
            character
            for character in self.roster.members
            if character in self.selected_members
        )
        self.on_start(ordered_members)
        self.next_screen = "adventure"

    def update(self, dt: float) -> None:
        """Update adventure setup."""
        _ = dt

    def render(self, surface: pygame.Surface) -> None:
        """Render the character roster and current selection."""
        surface.fill(palette.BACKGROUND)
        width, height = surface.get_size()

        pygame.draw.rect(
            surface,
            palette.BORDER,
            (4, 4, width - 8, height - 8),
            width=1,
        )

        title = self.title_font.render(
            "NEW ADVENTURE",
            True,
            palette.HIGHLIGHT,
        )
        surface.blit(title, (12, 10))

        members = self.roster.members

        if not members:
            text = self.font.render(
                "NO CHARACTERS AVAILABLE",
                True,
                palette.TEXT,
            )
            surface.blit(text, (12, 48))
            hint = "PRESS C TO CREATE A CHARACTER"
        else:
            visible_count = 7
            max_start = max(0, len(members) - visible_count)
            start_index = min(
                max(0, self.selected_index - visible_count // 2),
                max_start,
            )
            visible_members = members[start_index : start_index + visible_count]

            for offset, character in enumerate(visible_members):
                index = start_index + offset
                highlighted = index == self.selected_index
                chosen = character in self.selected_members

                prefix = ">" if highlighted else " "
                marker = "[X]" if chosen else "[ ]"
                color = palette.HIGHLIGHT if highlighted else palette.TEXT
                text = self.small_font.render(
                    f"{prefix} {marker} {character.name[:18]}",
                    True,
                    color,
                )
                surface.blit(text, (12, 39 + offset * 15))

            hint = "UP/DOWN: SELECT  ENTER: ADD/REMOVE"

        footer = self.small_font.render(
            hint,
            True,
            palette.TEXT_MUTED,
        )
        surface.blit(footer, (12, height - 33))

        controls = self.small_font.render(
            "C: CREATE CHARACTER  F: START  ESC: BACK",
            True,
            palette.TEXT_MUTED,
        )
        surface.blit(controls, (12, height - 20))

        if self.message:
            message = self.small_font.render(
                self.message,
                True,
                palette.HIGHLIGHT,
            )
            surface.blit(message, (12, height - 48))
