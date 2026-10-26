"""Turn-based combat screen."""

import pygame

from phantasie import palette
from phantasie.combat import (
    Combat,
    CombatStatus,
    MonsterAttackResult,
)
from phantasie.screens.base import BaseScreen


class CombatScreen(BaseScreen):
    """Display combat and manage party actions and monster turns."""

    def __init__(self) -> None:
        """Initialize the screen without an active encounter."""
        super().__init__()

        self.combat: Combat | None = None
        self.selected_member = 0
        self.selected_monster = 0
        self.message = "A BATTLE BEGINS!"

        # Keep a reference to the model's defensive-state set.
        self.defending: set[int] = set()

        self.title_font = pygame.font.Font(None, 24)
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)

    def start_combat(self, combat: Combat) -> None:
        """Start a new encounter and reset screen selections."""
        self.combat = combat
        self.selected_member = 0
        self.selected_monster = 0
        self.defending = combat.defending
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

    # ------------------------------------------------------------------
    # Party and monster selection.
    # ------------------------------------------------------------------

    def _select_member(self, direction: int) -> None:
        """Select a living party member who has not acted this round."""
        assert self.combat is not None

        members = self.combat.party

        for offset in range(1, len(members) + 1):
            index = (
                self.selected_member + direction * offset
            ) % len(members)

            if (
                members[index].is_alive
                and index not in self.combat.acted_members
            ):
                self.selected_member = index
                self.message = f"{members[index].name.upper()}'S TURN."
                return

        self.message = "NO OTHER PARTY MEMBERS READY."

    def _select_monster(self, direction: int) -> None:
        """Select a living monster."""
        assert self.combat is not None

        monsters = self.combat.monsters

        for offset in range(1, len(monsters) + 1):
            index = (
                self.selected_monster + direction * offset
            ) % len(monsters)

            if monsters[index].is_alive:
                self.selected_monster = index
                self.message = (
                    f"TARGET: {monsters[index].name.upper()}."
                )
                return

    # ------------------------------------------------------------------
    # Party actions.
    # ------------------------------------------------------------------

    def _attack(self) -> None:
        """Attack the selected monster and advance the party turn."""
        assert self.combat is not None

        members = self.combat.party
        monsters = self.combat.monsters

        if not members[self.selected_member].is_alive:
            self.message = "SELECT A LIVING PARTY MEMBER."
            return

        if self.selected_member in self.combat.acted_members:
            self.message = "THIS MEMBER HAS ALREADY ACTED."
            return

        living_monsters = [
            index
            for index, monster in enumerate(monsters)
            if monster.is_alive
        ]

        if not living_monsters:
            return

        if not monsters[self.selected_monster].is_alive:
            self.selected_monster = living_monsters[0]

        attacker = members[self.selected_member]
        target = monsters[self.selected_monster]

        damage = self.combat.member_attack(
            self.selected_member,
            self.selected_monster,
        )

        if not target.is_alive:
            self.message = (
                f"{target.name.upper()} FALLS! "
                f"{attacker.name.upper()} DEALT {damage}."
            )
        else:
            self.message = (
                f"{attacker.name.upper()} HITS "
                f"{target.name.upper()} FOR {damage}!"
            )

        # Preserve the outcome message and skip monster retaliation.
        if self.combat.status is CombatStatus.VICTORY:
            self.message = "VICTORY! PRESS ENTER."
            return

        if self.combat.status is not CombatStatus.ACTIVE:
            return

        self._finish_party_action()

    def _defend(self) -> None:
        """Defend with the selected member and advance the party turn."""
        assert self.combat is not None

        if not self.combat.party[self.selected_member].is_alive:
            self.message = "SELECT A LIVING PARTY MEMBER."
            return

        if self.selected_member in self.combat.acted_members:
            self.message = "THIS MEMBER HAS ALREADY ACTED."
            return

        member = self.combat.party[self.selected_member]

        self.combat.member_defend(self.selected_member)

        self.message = (
            f"{member.name.upper()} TAKES A DEFENSIVE STANCE."
        )

        self._finish_party_action()

    def _finish_party_action(self) -> None:
        """Advance to the next member or resolve the monster phase."""
        assert self.combat is not None

        if self.combat.status is not CombatStatus.ACTIVE:
            return

        if not self.combat.party_phase_complete:
            # Automatically select the next living member who is ready.
            for index, member in enumerate(self.combat.party):
                if (
                    member.is_alive
                    and index not in self.combat.acted_members
                ):
                    self.selected_member = index
                    return

        # Every living party member has acted. Monsters now retaliate.
        attacks: list[MonsterAttackResult] = (
            self.combat.resolve_monster_phase()
        )

        if self.combat.status is CombatStatus.DEFEAT:
            final_attack = attacks[-1] if attacks else None

            if final_attack is not None and final_attack.target_defeated:
                self.message = (
                    f"{final_attack.target_name.upper()} FALLS! "
                    "PARTY DEFEATED."
                )
            else:
                self.message = "THE PARTY HAS BEEN DEFEATED!"
            return

        if self.combat.status is CombatStatus.VICTORY:
            self.message = "VICTORY! PRESS ENTER."
            return

        if attacks:
            # Display the final monster attack of this phase.
            attack = attacks[-1]

            if attack.target_defeated:
                self.message = (
                    f"{attack.monster_name.upper()} HITS "
                    f"{attack.target_name.upper()} FOR "
                    f"{attack.damage}! {attack.target_name.upper()} FALLS!"
                )
            else:
                self.message = (
                    f"{attack.monster_name.upper()} HITS "
                    f"{attack.target_name.upper()} FOR {attack.damage}!"
                )
        else:
            self.message = (
                f"ROUND {self.combat.round_number}: CHOOSE ACTION."
            )

        # The model has started the next round and cleared temporary states.
        self.selected_member = next(
            index
            for index, member in enumerate(self.combat.party)
            if member.is_alive
        )

    # ------------------------------------------------------------------
    # Rendering.
    # ------------------------------------------------------------------

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
        surface.blit(
            active_font.render(text, True, color),
            position,
        )

    def render(self, surface: pygame.Surface) -> None:
        """Render combatants, round information, and available actions."""
        surface.fill(palette.BACKGROUND)

        self._draw_text(
            surface,
            "COMBAT",
            (12, 10),
            palette.HIGHLIGHT,
            self.title_font,
        )

        if self.combat is None:
            self._draw_text(
                surface,
                "NO ACTIVE ENCOUNTER.",
                (12, 40),
                palette.TEXT,
            )
            return

        self._draw_text(
            surface,
            f"ROUND {self.combat.round_number}",
            (230, 12),
            palette.TEXT,
            self.small_font,
        )

        self._draw_text(
            surface,
            "PARTY",
            (12, 38),
            palette.HIGHLIGHT,
        )

        for index, member in enumerate(self.combat.party):
            if not member.is_alive:
                marker = "X"
                color = palette.TEXT_MUTED
            elif index == self.selected_member:
                marker = ">"
                color = palette.TEXT
            elif index in self.combat.acted_members:
                marker = "*"
                color = palette.TEXT_MUTED
            else:
                marker = " "
                color = palette.TEXT

            defense_marker = " D" if index in self.defending else ""

            self._draw_text(
                surface,
                (
                    f"{marker}{member.name} "
                    f"HP:{member.hit_points}{defense_marker}"
                ),
                (12, 54 + index * 16),
                color,
                self.small_font,
            )

        self._draw_text(
            surface,
            "MONSTERS",
            (170, 38),
            palette.HIGHLIGHT,
        )

        for index, monster in enumerate(self.combat.monsters):
            if not monster.is_alive:
                marker = "X"
                color = palette.TEXT_MUTED
            else:
                marker = ">" if index == self.selected_monster else " "
                color = palette.TEXT

            self._draw_text(
                surface,
                f"{marker}{monster.name} HP:{monster.hit_points}",
                (170, 54 + index * 16),
                color,
                self.small_font,
            )

        # Terminal messages are set by combat actions, not by rendering.
        self._draw_text(
            surface,
            self.message[:44],
            (12, 150),
            palette.HIGHLIGHT,
            self.small_font,
        )

        self._draw_text(
            surface,
            "ENTER: ATTACK  SPACE: DEFEND  F: FLEE",
            (12, 172),
            palette.TEXT_MUTED,
            self.small_font,
        )
