"""Tests for monster definitions and encounter generation."""

import random

import pytest

from phantasie.encounters import (
    DEFAULT_MONSTERS,
    EncounterGenerator,
    Monster,
)


def test_default_monster_roster_is_valid() -> None:
    assert DEFAULT_MONSTERS

    for monster in DEFAULT_MONSTERS:
        assert monster.name.strip()
        assert monster.hit_points > 0
        assert monster.attack >= 0
        assert monster.defense >= 0
        assert monster.experience_reward >= 0


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"name": ""}, "name cannot be empty"),
        ({"name": "   "}, "name cannot be empty"),
        ({"hit_points": 0}, "hit points must be positive"),
        ({"hit_points": -1}, "hit points must be positive"),
        ({"attack": -1}, "attack cannot be negative"),
        ({"defense": -1}, "defense cannot be negative"),
        (
            {"experience_reward": -1},
            "Experience reward cannot be negative",
        ),
    ],
)
def test_monster_rejects_invalid_data(
    kwargs: dict[str, object],
    message: str,
) -> None:
    values: dict[str, object] = {
        "name": "Goblin",
        "hit_points": 6,
        "attack": 3,
        "defense": 1,
        "experience_reward": 10,
    }
    values.update(kwargs)

    with pytest.raises(ValueError, match=message):
        Monster(**values)  # type: ignore[arg-type]


def test_monster_definitions_are_immutable() -> None:
    monster = DEFAULT_MONSTERS[0]

    with pytest.raises(AttributeError):
        monster.hit_points = 100  # type: ignore[misc]


def test_generator_rejects_empty_roster() -> None:
    with pytest.raises(ValueError, match="At least one monster"):
        EncounterGenerator(monsters=())


@pytest.mark.parametrize("chance", [-0.1, 1.1])
def test_generator_rejects_invalid_probability(chance: float) -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        EncounterGenerator(encounter_chance=chance)


def test_zero_probability_never_generates_encounter() -> None:
    generator = EncounterGenerator(
        encounter_chance=0.0,
        rng=random.Random(42),
    )

    for _ in range(20):
        assert generator.generate() is None


def test_certain_probability_always_generates_encounter() -> None:
    generator = EncounterGenerator(
        encounter_chance=1.0,
        rng=random.Random(42),
    )

    for _ in range(20):
        assert generator.generate() in DEFAULT_MONSTERS


def test_single_monster_roster_selects_that_monster() -> None:
    goblin = Monster("Goblin", 6, 3, 1, 10)
    generator = EncounterGenerator(
        monsters=(goblin,),
        encounter_chance=1.0,
        rng=random.Random(42),
    )

    assert generator.generate() == goblin


def test_seeded_generators_produce_reproducible_encounters() -> None:
    first = EncounterGenerator(rng=random.Random(123))
    second = EncounterGenerator(rng=random.Random(123))

    assert [first.generate() for _ in range(30)] == [
        second.generate() for _ in range(30)
    ]
