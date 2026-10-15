"""Core application loop for Phantasie III."""

import pygame

from phantasie import palette
from phantasie.menu import TitleMenu


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

        # Draw at the logical resolution.
        self.canvas = pygame.Surface((self.LOGICAL_WIDTH, self.LOGICAL_HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.menu = TitleMenu()
        self.current_screen = "title"

        self._render()

    def handle_events(self) -> None:
        """Process keyboard and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif self.current_screen == "title":
                    if event.key in (
                        pygame.K_UP,
                        pygame.K_w,
                    ):
                        self.menu.move_selection(-1)

                    elif event.key in (
                        pygame.K_DOWN,
                        pygame.K_s,
                    ):
                        self.menu.move_selection(1)

                    elif event.key in (
                        pygame.K_RETURN,
                        pygame.K_SPACE,
                    ):
                        action = self.menu.activate()

                        if action == "quit":
                            self.running = False

    def update(self, dt: float) -> None:
        """Update game state.

        Args:
            dt: Time elapsed since the previous frame, in seconds.
        """
        # Future gameplay systems will update here.
        _ = dt

    def _render(self) -> None:
        """Render the current screen to the logical canvas."""
        if self.current_screen == "title":
            self.menu.render(self.canvas)
        else:
            self.canvas.fill(palette.BACKGROUND)

        # Scale without smoothing to preserve crisp pixel edges.
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
