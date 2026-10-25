"""Core application loop for Phantasie III."""

import pygame

from phantasie.characters.models import Character, Party
from phantasie.screen_manager import ScreenManager
from phantasie.screens.character_creation import CharacterCreationScreen
from phantasie.screens.exploration import ExplorationScreen
from phantasie.screens.new_game import NewGameScreen
from phantasie.screens.party import PartyScreen
from phantasie.screens.placeholder import PlaceholderScreen
from phantasie.screens.title import TitleScreen
from phantasie.world import ExplorationMap, ExplorationState
from phantasie.combat import Combat
from phantasie.screens.combat import CombatScreen


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
        pygame.key.start_text_input()

        pygame.display.set_caption("Phantasie III")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.canvas = pygame.Surface((self.LOGICAL_WIDTH, self.LOGICAL_HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True
        self.character: Character | None = None
        self.party = Party()
        self.adventure_party = Party()
        self.exploration_map = ExplorationMap()
        self.exploration_state = ExplorationState()

        if not self.exploration_map.is_walkable(
            self.exploration_state.x,
            self.exploration_state.y,
        ):
            raise ValueError("The exploration starting position must be walkable.")

        # Register the available screens.
        self.screen_manager = ScreenManager()

        self.title_screen = TitleScreen(on_new_game=self._reset_adventure)

        self.screen_manager.register(
            "title",
            self.title_screen,
        )

        self.screen_manager.register(
            "new_game",
            NewGameScreen(
                roster=self.party,
                on_start=self._start_adventure,
            ),
        )

        self.screen_manager.register(
            "character_creation",
            CharacterCreationScreen(
                on_confirm=self._accept_character,
            ),
        )

        self.screen_manager.register(
            "new_game_character_creation",
            CharacterCreationScreen(
                on_confirm=self._accept_character,
                return_screen="new_game",
            ),
        )

        self.screen_manager.register(
            "party",
            PartyScreen(self.party),
        )

        self.combat_screen = CombatScreen()
        self.screen_manager.register("combat", self.combat_screen)

        self.exploration_screen = ExplorationScreen(
            world=self.exploration_map,
            state=self.exploration_state,
            party_provider=lambda: self.adventure_party,
            on_encounter=self._start_combat,
        )

        self.screen_manager.register(
            "adventure",
            self.exploration_screen,
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
        events = pygame.event.get()
        ignore_textinput: str | None = None

        for event in events:
            if event.type == pygame.TEXTINPUT and ignore_textinput is not None:
                if event.text.casefold() == ignore_textinput.casefold():
                    ignore_textinput = None
                    continue

                ignore_textinput = None

            if event.type == pygame.QUIT:
                self.running = False
            else:
                previous_screen = self.screen_manager.current_screen_name
                self.screen_manager.handle_event(event)
                current_screen = self.screen_manager.current_screen_name

                if (
                    event.type == pygame.KEYDOWN
                    and previous_screen != current_screen
                ):
                    typed_character = getattr(event, "unicode", "")
                    if typed_character and typed_character.isprintable():
                        ignore_textinput = typed_character

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

    def _reset_adventure(self) -> None:
        """Reset adventure progress before starting a new game."""
        self.exploration_state.x = 1
        self.exploration_state.y = 1
        self.exploration_state.event_seen = False
        self.adventure_party = Party()
        adventure = self.screen_manager.screens["adventure"]
        if isinstance(adventure, ExplorationScreen):
            adventure.active_encounter = None
            adventure.message = "EXPLORE THE AREA."
        new_game = self.screen_manager.screens["new_game"]
        if isinstance(new_game, NewGameScreen):
            new_game.reset_selection()

    def _accept_character(self, character: Character) -> None:
        """Add a confirmed character to the roster."""
        self.character = character
        self.party.add_member(character)
        self.title_screen.menu.status_message = f"Created {character.name}!"

    def _start_combat(self, monster: object) -> None:
        """Start combat when exploration triggers a monster encounter."""
        if self.adventure_party.member_count == 0:
            self.exploration_screen.message = "YOU NEED A PARTY TO FIGHT!"
            self.exploration_screen.active_encounter = None
            return

        combat = Combat(self.adventure_party, (monster,))
        self.combat_screen.start_combat(combat)

        self.exploration_screen.active_encounter = None
        self.exploration_screen.message = "A BATTLE BEGINS!"
        self.exploration_screen.next_screen = "combat"

    def _start_adventure(
        self,
        members: tuple[Character, ...],
    ) -> None:
        """Store the selected characters as the adventure party."""
        self.adventure_party = Party()

        for character in members:
            self.adventure_party.add_member(character)
