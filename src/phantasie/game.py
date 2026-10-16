"""Core application loop for Phantasie III."""

import pygame

from phantasie.characters.models import Character
from phantasie.screen_manager import ScreenManager
from phantasie.screens.character_creation import CharacterCreationScreen
from phantasie.screens.placeholder import PlaceholderScreen
from phantasie.screens.title import TitleScreen


class Game:
    """Manage the game window and application loop."""

    LOGICAL_WIDTH = 320
    LOGICAL_HEIGHT = 200
    SCALE = 3

    WIDTH = LOGICAL_WIDTH * SCALE
    HEIGHT = LOGICAL_HEIGHT * SCALE

    FPS = 60

    def __init__(self) -> None:
        """Initialize the game."""
        pygame.init()

        pygame.display.set_caption("Phantasie III")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.canvas = pygame.Surface((self.LOGICAL_WIDTH, self.LOGICAL_HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True
        self.character: Character | None = None

        # Register the available screens.
        self.screen_manager = ScreenManager()

        self.title_screen = TitleScreen()

        self.screen_manager.register(
            "title",
            self.title_screen,
        )

        self.screen_manager.register(
            "new_game",
            CharacterCreationScreen(
                on_confirm=self._accept_character,
            ),
        )

        self.screen_manager.register(
            "options",
            PlaceholderScreen(
                title="OPTIONS",
                message="Options are coming soon.",
            ),
        )

        # Start at the title screen.
        self.screen_manager.switch_to("title")

        # Render the initial frame.
        self._render()

    def handle_events(self) -> None:
        """Process Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.screen_manager.handle_event(event)

            if self.screen_manager.quit_requested:
                self.running = False

    def update(self, dt: float) -> None:
        """Update the active screen.

        Args:
            dt: Time elapsed since the previous frame, in seconds.
        """
        self.screen_manager.update(dt)

        if self.screen_manager.quit_requested:
            self.running = False

    def _render(self) -> None:
        """Render the active screen to the logical canvas."""
        self.screen_manager.render(self.canvas)

        pygame.transform.scale(
            self.canvas,
            self.screen.get_size(),
            self.screen,
        )

        pygame.display.flip()

    def render(self) -> None:
        """Draw the current frame."""
        self._render()

    def run(self) -> None:
        """Run the main game loop."""
        try:
            while self.running:
                dt = self.clock.tick(self.FPS) / 1000.0

                self.handle_events()
                self.update(dt)
                self.render()
        finally:
            pygame.quit()

    def _accept_character(self, character: Character) -> None:
        """Store a confirmed character and report success on the title screen."""
        self.character = character
        self.title_screen.menu.status_message = f"Created {character.name}!"
