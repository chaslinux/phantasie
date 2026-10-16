"""Character creation screen."""

import random
from collections.abc import Callable

import pygame

from phantasie import palette
from phantasie.characters.models import Attributes, Character, Profession, Race
from phantasie.characters.rules import generate_attributes
from phantasie.screens.base import BaseScreen


class CharacterCreationScreen(BaseScreen):
    """Allow the player to create a character."""

    FIELDS = ("Name", "Race", "Profession")

    def __init__(
        self,
        on_confirm: Callable[[Character], None],
        rng: random.Random | None = None,
    ) -> None:
        """Initialize character creation."""
        super().__init__()

        self.on_confirm = on_confirm
        self.rng = rng if rng is not None else random.Random()

        self.races = list(Race)
        self.professions = list(Profession)

        self.name = ""
        self.race_index = 0
        self.profession_index = 0
        self.field_index = 0

        self.attributes = self._generate_attributes()

        self.title_font = pygame.font.Font(None, 24)
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)

        self.message = ""

    @property
    def selected_race(self) -> Race:
        """Return the selected race."""
        return self.races[self.race_index]

    @property
    def selected_profession(self) -> Profession:
        """Return the selected profession."""
        return self.professions[self.profession_index]

    def _generate_attributes(self) -> Attributes:
        """Generate attributes for the current race and profession."""
        return generate_attributes(
            self.selected_race,
            self.selected_profession,
            self.rng,
        )

    def _cycle_field(self, direction: int) -> None:
        """Move focus between the editable fields."""
        self.field_index = (self.field_index + direction) % len(self.FIELDS)

    def _change_selection(self, direction: int) -> None:
        """Change the selected race or profession."""
        if self.field_index == 1:
            self.race_index = (self.race_index + direction) % len(self.races)
        elif self.field_index == 2:
            self.profession_index = (self.profession_index + direction) % len(
                self.professions
            )
        else:
            return

        self.attributes = self._generate_attributes()
        self.message = ""

    def _confirm(self) -> None:
        """Create and retain the character if the name is valid."""
        name = self.name.strip()

        if not name:
            self.message = "ENTER A CHARACTER NAME"
            self.field_index = 0
            return

        character = Character(
            name=name,
            race=self.selected_race,
            profession=self.selected_profession,
            attributes=self.attributes,
        )

        self.on_confirm(character)
        self.next_screen = "title"

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle keyboard input."""
        if event.type == pygame.TEXTINPUT:
            if self.field_index == 0 and len(self.name) < 16:
                self.name += event.text
                self.message = ""
            return

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.next_screen = "title"
            return

        if event.key == pygame.K_TAB:
            self._cycle_field(1)
            return

        if event.key == pygame.K_UP:
            self._cycle_field(-1)
            return

        if event.key == pygame.K_DOWN:
            self._cycle_field(1)
            return

        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            direction = -1 if event.key == pygame.K_LEFT else 1
            self._change_selection(direction)
            return

        if self.field_index == 0:
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
                self.message = ""
            elif event.key == pygame.K_r:
                self.attributes = self._generate_attributes()
                self.message = ""
            elif event.key == pygame.K_RETURN:
                self._confirm()
            return

        if event.key == pygame.K_r:
            self.attributes = self._generate_attributes()
            self.message = ""
        elif event.key == pygame.K_RETURN:
            self._confirm()

    def update(self, dt: float) -> None:
        """Update character creation."""
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
        """Render the character creation interface."""
        surface.fill(palette.BACKGROUND)

        width, height = surface.get_size()
        pygame.draw.rect(
            surface,
            palette.BORDER,
            (4, 4, width - 8, height - 8),
            width=1,
        )

        self._draw_text(
            surface,
            "CREATE CHARACTER",
            (12, 10),
            palette.HIGHLIGHT,
            self.title_font,
        )

        fields = (
            f"Name: {self.name or '_'}",
            f"Race: {self.selected_race.value}",
            f"Profession: {self.selected_profession.value}",
        )

        for index, text in enumerate(fields):
            prefix = ">" if index == self.field_index else " "
            color = palette.HIGHLIGHT if index == self.field_index else palette.TEXT
            self._draw_text(
                surface,
                f"{prefix} {text}",
                (12, 42 + index * 18),
                color,
            )

        self._draw_text(
            surface,
            "ATTRIBUTES",
            (176, 42),
            palette.HIGHLIGHT,
        )

        attribute_lines = (
            ("STR", self.attributes.strength),
            ("INT", self.attributes.intelligence),
            ("DEX", self.attributes.dexterity),
            ("CON", self.attributes.constitution),
            ("CHA", self.attributes.charisma),
        )

        for index, (label, value) in enumerate(attribute_lines):
            self._draw_text(
                surface,
                f"{label}  {value:2}",
                (184, 59 + index * 15),
                palette.TEXT,
            )

        if self.message:
            self._draw_text(
                surface,
                self.message,
                (12, 112),
                palette.HIGHLIGHT,
                self.small_font,
            )

        self._draw_text(
            surface,
            "TAB/ARROWS: SELECT FIELD",
            (12, height - 39),
            palette.TEXT_MUTED,
            self.small_font,
        )
        self._draw_text(
            surface,
            "LEFT/RIGHT: CHANGE  R: REROLL",
            (12, height - 27),
            palette.TEXT_MUTED,
            self.small_font,
        )
        self._draw_text(
            surface,
            "ENTER: ACCEPT  ESC: CANCEL",
            (12, height - 15),
            palette.TEXT_MUTED,
            self.small_font,
        )
