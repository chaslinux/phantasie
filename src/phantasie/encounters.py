"""Monster definitions and random encounter generation."""

import random
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Monster:
    """Immutable definition of a monster."""

    name: str
    hit_points: int
    attack: int
    defense: int
    experience_reward: int

    def __post_init__(self) -> None:
        """Validate monster data."""
        if not self.name.strip():
            raise ValueError("Monster name cannot be empty.")

        if self.hit_points <= 0:
            raise ValueError("Monster hit points must be positive.")

        if self.attack < 0:
            raise ValueError("Monster attack cannot be negative.")

        if self.defense < 0:
            raise ValueError("Monster defense cannot be negative.")

        if self.experience_reward < 0:
            raise ValueError("Experience reward cannot be negative.")


DEFAULT_MONSTERS: tuple[Monster, ...] = (
    Monster(
        name="Goblin",
        hit_points=6,
        attack=3,
        defense=1,
        experience_reward=10,
    ),
    Monster(
        name="Orc",
        hit_points=12,
        attack=5,
        defense=2,
        experience_reward=20,
    ),
    Monster(
        name="Skeleton",
        hit_points=8,
        attack=4,
        defense=2,
        experience_reward=15,
    ),
)


class EncounterGenerator:
    """Determine whether an encounter occurs and select a monster."""

    def __init__(
        self,
        monsters: Sequence[Monster] = DEFAULT_MONSTERS,
        encounter_chance: float = 0.10,
        rng: random.Random | None = None,
    ) -> None:
        """Initialize encounter rules and their random-number generator."""
        if not monsters:
            raise ValueError("At least one monster is required.")

        if not 0.0 <= encounter_chance <= 1.0:
            raise ValueError("Encounter chance must be between 0 and 1.")

        self.monsters = tuple(monsters)
        self.encounter_chance = encounter_chance
        self.rng = rng if rng is not None else random.Random()

    def generate(self) -> Monster | None:
        """Return an encountered monster, or None if no encounter occurs."""
        if self.rng.random() >= self.encounter_chance:
            return None

        return self.rng.choice(self.monsters)
