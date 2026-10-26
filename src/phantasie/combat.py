"""Turn-based combat model."""

from dataclasses import dataclass
from enum import Enum

from phantasie.characters.models import Character, Party
from phantasie.encounters import Monster


class CombatStatus(str, Enum):
    """Possible outcomes of a combat encounter."""

    ACTIVE = "active"
    VICTORY = "victory"
    DEFEAT = "defeat"


@dataclass(slots=True)
class Combatant:
    """A participant with independent combat statistics."""

    name: str
    hit_points: int
    attack: int
    defense: int
    max_hit_points: int | None = None

    def __post_init__(self) -> None:
        """Validate combatant statistics."""
        if not self.name.strip():
            raise ValueError("Combatant name cannot be empty.")

        if self.hit_points < 0:
            raise ValueError("Hit points cannot be negative.")

        if self.attack < 0:
            raise ValueError("Attack cannot be negative.")

        if self.defense < 0:
            raise ValueError("Defense cannot be negative.")

        if self.max_hit_points is None:
            self.max_hit_points = self.hit_points

        if self.max_hit_points < 0:
            raise ValueError("Maximum hit points cannot be negative.")

        if self.hit_points > self.max_hit_points:
            raise ValueError("Hit points cannot exceed maximum hit points.")

    @property
    def is_alive(self) -> bool:
        """Return whether the combatant has hit points remaining."""
        return self.hit_points > 0

    def take_damage(self, damage: int) -> None:
        """Apply damage without allowing negative hit points."""
        if damage < 0:
            raise ValueError("Damage cannot be negative.")

        self.hit_points = max(0, self.hit_points - damage)

class Combat:
    """Manage a party fighting a group of monsters."""

    def __init__(
        self,
        party: Party,
        monsters: tuple[Monster, ...],
    ) -> None:
        """Initialize combat from a party and monster definitions."""
        if party.member_count == 0:
            raise ValueError("Combat requires at least one party member.")

        if not monsters:
            raise ValueError("Combat requires at least one monster.")

        self.party = [
            self._character_to_combatant(character)
            for character in party.members
        ]
        self.monsters = [
            Combatant(
                name=monster.name,
                hit_points=monster.hit_points,
                attack=monster.attack,
                defense=monster.defense,
            )
            for monster in monsters
        ]
        self.status = CombatStatus.ACTIVE
        self.acted_members: set[int] = set()
        self.defending: set[int] = set()
        self.round_number = 1
        self._update_status()

    @staticmethod
    def _character_to_combatant(character: Character) -> Combatant:
        """Create combat statistics from a character."""
        return Combatant(
            name=character.name,
            hit_points=max(1, character.attributes.constitution),
            attack=max(1, character.attributes.strength // 2),
            defense=max(0, character.attributes.dexterity // 4),
        )

    @staticmethod
    def calculate_damage(
        attacker: Combatant,
        defender: Combatant,
    ) -> int:
        """Calculate attack damage after defense."""
        return max(1, attacker.attack - defender.defense)

    def attack(
        self,
        attacker: Combatant,
        defender: Combatant,
        *,
        damage_reduction: int = 0,
    ) -> int:
        """Resolve an attack and update combat status."""
        if self.status is not CombatStatus.ACTIVE:
            raise RuntimeError("Combat has already ended.")

        if not attacker.is_alive:
            raise ValueError("A defeated combatant cannot attack.")

        if not defender.is_alive:
            raise ValueError("A defeated combatant cannot be attacked.")

        if damage_reduction < 0:
            raise ValueError("Damage reduction cannot be negative.")

        damage = max(
            1,
            self.calculate_damage(attacker, defender) - damage_reduction,
        )
        defender.take_damage(damage)
        self._update_status()
        return damage

    @property
    def party_phase_complete(self) -> bool:
        """Return whether every living party member has acted."""
        return all(
            not member.is_alive or index in self.acted_members
            for index, member in enumerate(self.party)
        )

    def member_attack(
        self,
        member_index: int,
        monster_index: int,
    ) -> int:
        """Let a party member attack a monster."""
        if self.status is not CombatStatus.ACTIVE:
            raise RuntimeError("Combat has already ended.")

        if not 0 <= member_index < len(self.party):
            raise IndexError("Invalid party member index.")

        if not 0 <= monster_index < len(self.monsters):
            raise IndexError("Invalid monster index.")

        if member_index in self.acted_members:
            raise ValueError("This party member has already acted.")

        damage = self.attack(
            self.party[member_index],
            self.monsters[monster_index],
        )
        self.acted_members.add(member_index)
        return damage

    def member_defend(self, member_index: int) -> None:
        """Let a party member defend for the current round."""
        if self.status is not CombatStatus.ACTIVE:
            raise RuntimeError("Combat has already ended.")

        if not 0 <= member_index < len(self.party):
            raise IndexError("Invalid party member index.")

        if not self.party[member_index].is_alive:
            raise ValueError("A defeated member cannot defend.")

        if member_index in self.acted_members:
            raise ValueError("This party member has already acted.")

        self.acted_members.add(member_index)
        self.defending.add(member_index)

    def resolve_monster_phase(self) -> None:
        """Let surviving monsters attack before starting the next round."""
        if self.status is not CombatStatus.ACTIVE:
            return

        if not self.party_phase_complete:
            return

        for monster in self.monsters:
            if not monster.is_alive:
                continue

            living_members = [
                index
                for index, member in enumerate(self.party)
                if member.is_alive
            ]

            if not living_members:
                break

            # Target the first living party member.
            target_index = living_members[0]
            damage_reduction = (
                1 if target_index in self.defending else 0
            )

            self.attack(
                monster,
                self.party[target_index],
                damage_reduction=damage_reduction,
            )

            if self.status is not CombatStatus.ACTIVE:
                break

        # Temporary defensive stances expire after monster retaliation.
        self.defending.clear()
        self.acted_members.clear()

        if self.status is CombatStatus.ACTIVE:
            self.round_number += 1
    def _update_status(self) -> None:
        """Determine whether either side has been defeated."""
        if not any(monster.is_alive for monster in self.monsters):
            self.status = CombatStatus.VICTORY
        elif not any(member.is_alive for member in self.party):
            self.status = CombatStatus.DEFEAT
        else:
            self.status = CombatStatus.ACTIVE
