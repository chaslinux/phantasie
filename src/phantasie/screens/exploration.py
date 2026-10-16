"""Exploration screen for the active adventure party."""

from collections.abc import Callable

import pygame

from phantasie import palette
from phantasie.characters.models import Party
from phantasie.screens.base import BaseScreen
from phantasie.world import ExplorationMap, ExplorationState, MoveResult


class ExplorationScreen(BaseScreen):
    """Render the exploration map and handle party movement."""

    TILE_SIZE = 16
    MAP_X = 8
    MAP_Y = 32

    def __init__(
        self,
        world: ExplorationMap,
        state: ExplorationState,
        party_provider: Callable[[], Party],
    ) -> None:
        """Initialize exploration with persistent world state."""
        super().__init__()
        self.world = world
        self.state = state
        self.party_provider = party_provider
        if not self.world.is_walkable(self.state.x, self.state.y):
            raise ValueError("The exploration starting position must be walkable.")
        self.message = "EXPLORE THE AREA."
        self.title_font = pygame.font.Font(None, 24)
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)

        if not self.world.is_walkable(self.state.x, self.state.y):
            raise ValueError("The starting position must be walkable.")

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle movement and navigation."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.next_screen = "title"
            return

        movement = {
            pygame.K_UP: (0, -1),
            pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_s: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_d: (1, 0),
        }

        direction = movement.get(event.key)

        if direction is None:
            return

        result = self.state.move(self.world, *direction)

        if result is MoveResult.BLOCKED:
            self.message = "YOU CANNOT GO THAT WAY."
        elif result is MoveResult.EVENT:
            self.message = "YOU DISCOVER AN OLD WAYSTONE."
        else:
            self.message = ""

    def update(self, dt: float) -> None:
        """Update exploration state."""
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
        surface.blit(active_font.render(text, True, color), position)

    def render(self, surface: pygame.Surface) -> None:
        """Render the map, party marker, and status information."""
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
            "EXPLORATION",
            (12, 10),
            palette.HIGHLIGHT,
            self.title_font,
        )

        for y, row in enumerate(self.world.rows):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    self.MAP_X + x * self.TILE_SIZE,
                    self.MAP_Y + y * self.TILE_SIZE,
                    self.TILE_SIZE,
                    self.TILE_SIZE,
                )

                if tile == "#":
                    color = palette.BORDER
                elif tile == "E":
                    color = palette.HIGHLIGHT
                else:
                    color = palette.BACKGROUND

                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(
                    surface,
                    palette.BORDER,
                    rect,
                    width=1,
                )

        player_rect = pygame.Rect(
            self.MAP_X + self.state.x * self.TILE_SIZE + 3,
            self.MAP_Y + self.state.y * self.TILE_SIZE + 3,
            self.TILE_SIZE - 6,
            self.TILE_SIZE - 6,
        )
        pygame.draw.rect(surface, palette.TEXT, player_rect)

        panel_x = self.MAP_X + self.world.width * self.TILE_SIZE + 8

        self._draw_text(
            surface,
            "PARTY",
            (panel_x, self.MAP_Y),
            palette.HIGHLIGHT,
            self.small_font,
        )

        party = self.party_provider()
        self._draw_text(
            surface,
            f"MEMBERS: {party.member_count}",
            (panel_x, self.MAP_Y + 16),
            palette.TEXT,
            self.small_font,
        )

        self._draw_text(
            surface,
            f"X: {self.state.x}",
            (panel_x, self.MAP_Y + 36),
            palette.TEXT_MUTED,
            self.small_font,
        )
        self._draw_text(
            surface,
            f"Y: {self.state.y}",
            (panel_x, self.MAP_Y + 50),
            palette.TEXT_MUTED,
            self.small_font,
        )

        self._draw_text(
            surface,
            self.message[:44],
            (12, height - 34),
            palette.HIGHLIGHT if self.message else palette.TEXT_MUTED,
            self.small_font,
        )
        self._draw_text(
            surface,
            "ARROWS/WASD: MOVE   ESC: EXIT",
            (12, height - 20),
            palette.TEXT_MUTED,
            self.small_font,
        )
