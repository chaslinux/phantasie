"""Core application loop for Phantasie III."""

import pygame


class Game:
    """Manage the main game window and application loop."""

    WIDTH = 960
    HEIGHT = 640
    FPS = 60

    BACKGROUND_COLOR = (20, 24, 36)
    TEXT_COLOR = (230, 220, 190)

    def __init__(self) -> None:
        """Initialize the game."""
        pygame.init()

        pygame.display.set_caption("Phantasie III")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)

        self.running = True

    def handle_events(self) -> None:
        """Process keyboard, mouse, and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, dt: float) -> None:
        """Update game state.

        Args:
            dt: Time elapsed since the previous frame, in seconds.
        """
        # Game mechanics will be updated here.
        # For example: movement, combat, and animations.
        _ = dt

    def render(self) -> None:
        """Draw the current frame."""
        self.screen.fill(self.BACKGROUND_COLOR)

        title = self.font.render(
            "PHANTASIE III",
            True,
            self.TEXT_COLOR,
        )

        title_rect = title.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        self.screen.blit(title, title_rect)

        pygame.display.flip()

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
