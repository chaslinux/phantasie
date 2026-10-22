"""Turn-based combat screen."""

import pygame

from phantasie import palette
from phantasie.combat import Combat, CombatStatus, Combatant
from phantasie.screens.base import BaseScreen


class CombatScreen(BaseScreen):
    """Display and manage a turn-based combat encounter."""

    def __init__(self) -> None:
        """Initialize the screen without an active encounter."""
        super().__init__()

        self.combat: Combat | None = None
        self.selected_member = 0
        self.selected_monster = 0
        self.message = "A BATTLE BEGINS!"
        self.defending: set[int] = set()

        self.title_font = pygame.font.Font(None, 24)
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)

    def start_combat(self, combat: Combat) -> None:
        """Start a new encounter."""
        self.combat = combat
        self.selected_member = 0
        self.selected_monster = 0
        self.defending.clear()
        self.message = "CHOOSE YOUR ACTION."
        self.next_screen = None

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle combat menu input."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.next_screen = "adventure"
            return

        if self.combat is None:
            return

        if self.combat.status is not CombatStatus.ACTIVE:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.next_screen = (
                    "adventure"
                    if self.combat.status is CombatStatus.VICTORY
                    else "title"
                )
            return

        if event.key in (pygame.K_UP, pygame.K_w):
            self._select_member(-1)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self._select_member(1)
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self._select_monster(-1)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self._select_monster(1)
        elif event.key == pygame.K_f:
            self.message = "YOU FLEE FROM THE ENCOUNTER."
            self.next_screen = "adventure"
        elif event.key == pygame.K_RETURN:
            self._attack()
        elif event.key == pygame.K_SPACE:
            self._defend()

    def _select_member(self, direction: int) -> None:
        """Select a living party member."""
        assert self.combat is not None

        members = self.combat.party
        for offset in range(1, len(members) + 1):
            index = (self.selected_member + direction * offset) % len(members)
            if members[index].is_alive:
                self.selected_member = index
                self.message = f"{members[index].name}'S TURN."
                return

    def _select_monster(self, direction: int) -> None:
        """Select a living monster."""
        assert self.combat is not None

        monsters = self.combat.monsters
        for offset in range(1, len(monsters) + 1):
            index = (self.selected_monster + direction * offset) % len(monsters)
            if monsters[index].is_alive:
                self.selected_monster = index
                self.message = f"TARGET: {monsters[index].name.upper()}."
                return

    def _attack(self) -> None:
        """Attack the selected monster and resolve enemy turns."""
        assert self.combat is not None

        members = self.combat.party
        monsters = self.combat.monsters

        if not members[self.selected_member].is_alive:
            self.message = "SELECT A LIVING PARTY MEMBER."
            return

        living_monsters = [
            index for index, monster in enumerate(monsters)
            if monster.is_alive
        ]
        if not living_monsters:
            return

        if not monsters[self.selected_monster].is_alive:
            self.selected_monster = living_monsters[0]

        attacker = members[self.selected_member]
        target = monsters[self.selected_monster]

        damage = self.combat.attack(attacker, target)
        self.message = (
            f"{attacker.name.upper()} DEALS {damage} DAMAGE!"
        )

        if self.combat.status is not CombatStatus.ACTIVE:
            return

        for index, monster in enumerate(monsters):
            if not monster.is_alive:
                continue

            defender_index = self.selected_member
            defender = members[defender_index]

            if not defender.is_alive:
                living_member_indices = [
                    member_index
                    for member_index, member in enumerate(members)
                    if member.is_alive
                ]
                if not living_member_indices:
                    self.combat._update_status()
                    return

                defender_index = living_member_indices[0]
                defender = members[defender_index]

            damage_reduction = (
                2 if defender_index in self.defending else 0
            )
            self.combat.attack(
                monster,
                defender,
                damage_reduction=damage_reduction,
            )

            self.message = (
                f"{monster.name.upper()} ATTACKS "
                f"{defender.name.upper()}!"
            )

            if self.combat.status is not CombatStatus.ACTIVE:
                return

        self.defending.clear()

    def _defend(self) -> None:
        """Mark the selected member as defending."""
        assert self.combat is not None

        if not self.combat.party[self.selected_member].is_alive:
            self.message = "SELECT A LIVING PARTY MEMBER."
            return

        self.defending.add(self.selected_member)
        self.message = (
            f"{self.combat.party[self.selected_member].name.upper()} "
            "TAKES A DEFENSIVE STANCE."
        )

    def update(self, dt: float) -> None:
        """Update combat."""
        _ = dt

    def _draw_text(
        self,
        surface: pygame.Surface,
        text: str,
        position: tuple[int, int],
        color: tuple[int, int, int],
        font: pygame.font.Font | None = None,
    ) -> None:
        """Draw text."""
        active_font = font or self.font
        surface.blit(active_font.render(text, True, color), position)

    def render(self, surface: pygame.Surface) -> None:
        """Render combatants and available actions."""
        surface.fill(palette.BACKGROUND)

        self._draw_text(
            surface, "COMBAT", (12, 10), palette.HIGHLIGHT,
            self.title_font,
        )

        if self.combat is None:
            self._draw_text(
                surface, "NO ACTIVE ENCOUNTER.", (12, 40), palette.TEXT,
            )
            return

        self._draw_text(
            surface, "PARTY", (12, 38), palette.HIGHLIGHT,
        )

        for index, member in enumerate(self.combat.party):
            marker = ">" if index == self.selected_member else " "
            color = palette.TEXT if member.is_alive else palette.TEXT_MUTED
            self._draw_text(
                surface,
                f"{marker}{member.name} HP:{member.hit_points}",
                (12, 54 + index * 16),
                color,
                self.small_font,
            )

        self._draw_text(
            surface, "MONSTERS", (170, 38), palette.HIGHLIGHT,
        )

        for index, monster in enumerate(self.combat.monsters):
            marker = ">" if index == self.selected_monster else " "
            color = palette.TEXT if monster.is_alive else palette.TEXT_MUTED
            self._draw_text(
                surface,
                f"{marker}{monster.name} HP:{monster.hit_points}",
                (170, 54 + index * 16),
                color,
                self.small_font,
            )

        if self.combat.status is CombatStatus.VICTORY:
            self.message = "VICTORY! PRESS ENTER."
        elif self.combat.status is CombatStatus.DEFEAT:
            self.message = "DEFEAT! PRESS ENTER."

        self._draw_text(
            surface, self.message[:44], (12, 150), palette.HIGHLIGHT,
            self.small_font,
        )
        self._draw_text(
            surface,
            "ENTER: ATTACK  SPACE: DEFEND  F: FLEE",
            (12, 172),
            palette.TEXT_MUTED,
            self.small_font,
        )

