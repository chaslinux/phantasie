"""Party roster and character inspection screen."""

import pygame

from phantasie import palette
from phantasie.characters.models import Character, Party
from phantasie.screens.base import BaseScreen


class PartyScreen(BaseScreen):
    """Display the party roster and inspect individual characters."""

    def __init__(self, party: Party) -> None:
        """Initialize the party screen."""
        super().__init__()
        self.party = party
        self.selected_index = 0
        self.show_details = False

        self.title_font = pygame.font.Font(None, 24)
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)

    @property
    def selected_character(self) -> Character | None:
        """Return the selected character, or None for an empty party."""
        members = self.party.members

        if not members:
            return None

        # Keep the selection valid if the roster changes.
        self.selected_index = min(
            self.selected_index,
            len(members) - 1,
        )
        return members[self.selected_index]

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle party navigation."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            if self.show_details:
                self.show_details = False
            else:
                self.next_screen = "title"
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.selected_character is not None:
                self.show_details = True
        elif event.key in (pygame.K_UP, pygame.K_w):
            if self.party.member_count:
                self.selected_index = (
                    self.selected_index - 1
                ) % self.party.member_count
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            if self.party.member_count:
                self.selected_index = (
                    self.selected_index + 1
                ) % self.party.member_count

    def update(self, dt: float) -> None:
        """Update party screen state."""
        _ = dt

    def _draw_text(
        self,
        surface: pygame.Surface,
        text: str,
        position: tuple[int, int],
        color: tuple[int, int, int],
        font: pygame.font.Font | None = None,
    ) -> None:
        """Draw text at a logical canvas position."""
        active_font = font if font is not None else self.font
        rendered = active_font.render(text, True, color)
        surface.blit(rendered, position)

    def render(self, surface: pygame.Surface) -> None:
        """Render the party roster and selected character."""
        surface.fill(palette.BACKGROUND)

        width, height = surface.get_size()
        pygame.draw.rect(
            surface,
            palette.BORDER,
            (4, 4, width - 8, height - 8),
            width=1,
        )

        if self.show_details:
            character = self.selected_character

            if character is not None:
                self._draw_text(
                    surface,
                    "CHARACTER DETAILS",
                    (12, 10),
                    palette.HIGHLIGHT,
                    self.title_font,
                )
                self._draw_text(
                    surface,
                    character.name,
                    (12, 40),
                    palette.HIGHLIGHT,
                )
                self._draw_text(
                    surface,
                    f"Race: {character.race.value}",
                    (12, 62),
                    palette.TEXT,
                )
                self._draw_text(
                    surface,
                    f"Class: {character.profession.value}",
                    (12, 80),
                    palette.TEXT,
                )

                attributes = (
                    ("Strength", character.attributes.strength),
                    ("Intelligence", character.attributes.intelligence),
                    ("Dexterity", character.attributes.dexterity),
                    ("Constitution", character.attributes.constitution),
                    ("Charisma", character.attributes.charisma),
                )

                for row, (label, value) in enumerate(attributes):
                    self._draw_text(
                        surface,
                        f"{label}: {value}",
                        (12, 103 + row * 13),
                        palette.TEXT,
                        self.small_font,
                    )

                self._draw_text(
                    surface,
                    "ESC: BACK TO PARTY",
                    (12, height - 20),
                    palette.TEXT_MUTED,
                    self.small_font,
                )
                return

            self.show_details = False

        self._draw_text(
            surface,
            "PARTY",
            (12, 10),
            palette.HIGHLIGHT,
            self.title_font,
        )

        members = self.party.members

        if not members:
            self._draw_text(
                surface,
                "YOUR PARTY IS EMPTY",
                (12, 48),
                palette.TEXT,
            )
            self._draw_text(
                surface,
                "CREATE A CHARACTER FROM THE TITLE MENU.",
                (12, 68),
                palette.TEXT_MUTED,
                self.small_font,
            )
        else:
            character = self.selected_character

            # Keep the selected member visible as the roster grows.
            visible_count = 8
            # Keep the selected member near the middle of the visible
            # roster, while keeping the first and last members in view
            # when navigating near either end of the party.
            max_start = max(0, len(members) - visible_count)
            start_index = min(
                max(0, self.selected_index - visible_count // 2),
                max_start,
            )
            visible_members = members[start_index : start_index + visible_count]

            for row, member in enumerate(visible_members):
                selected = start_index + row == self.selected_index
                prefix = ">" if selected else " "
                color = palette.HIGHLIGHT if selected else palette.TEXT

                self._draw_text(
                    surface,
                    f"{prefix} {member.name[:15]}",
                    (12, 38 + row * 13),
                    color,
                    self.small_font,
                )

            if character is not None:
                self._draw_text(
                    surface,
                    character.name[:18],
                    (158, 38),
                    palette.HIGHLIGHT,
                )
                self._draw_text(
                    surface,
                    f"Race: {character.race.value}",
                    (158, 56),
                    palette.TEXT,
                    self.small_font,
                )
                self._draw_text(
                    surface,
                    f"Class: {character.profession.value}",
                    (158, 70),
                    palette.TEXT,
                    self.small_font,
                )

                self._draw_text(
                    surface,
                    "ATTRIBUTES",
                    (158, 91),
                    palette.HIGHLIGHT,
                    self.small_font,
                )

                attributes = (
                    ("STR", character.attributes.strength),
                    ("INT", character.attributes.intelligence),
                    ("DEX", character.attributes.dexterity),
                    ("CON", character.attributes.constitution),
                    ("CHA", character.attributes.charisma),
                )

                for row, (label, value) in enumerate(attributes):
                    self._draw_text(
                        surface,
                        f"{label} {value:2}",
                        (166, 104 + row * 12),
                        palette.TEXT,
                        self.small_font,
                    )

        self._draw_text(
            surface,
            "UP/DOWN: SELECT   ESC: RETURN",
            (12, height - 20),
            palette.TEXT_MUTED,
            self.small_font,
        )
