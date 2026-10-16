"""Tests for Phantasie III character definitions."""

from phantasie.characters.models import Attributes, Profession, Race
from phantasie.characters.rules import (
    PROFESSION_MODIFIERS,
    RACIAL_MAXIMUMS,
    attributes_within_racial_maximums,
)


def test_all_documented_races_have_maximums() -> None:
    assert len(Race) == 15
    assert set(RACIAL_MAXIMUMS) == set(Race)


def test_all_documented_professions_have_modifiers() -> None:
    assert len(Profession) == 6
    assert set(PROFESSION_MODIFIERS) == set(Profession)


def test_human_maximums() -> None:
    assert RACIAL_MAXIMUMS[Race.HUMAN] == Attributes(18, 18, 18, 18, 18)


def test_sprite_dexterity_maximum() -> None:
    assert RACIAL_MAXIMUMS[Race.SPRITE].dexterity == 22


def test_wizard_profession_modifiers() -> None:
    assert PROFESSION_MODIFIERS[Profession.WIZARD] == Attributes(-4, 3, -2, 0, 1)


def test_attributes_at_racial_maximums_are_valid() -> None:
    assert attributes_within_racial_maximums(
        Race.HUMAN,
        Attributes(18, 18, 18, 18, 18),
    )


def test_attributes_above_racial_maximums_are_invalid() -> None:
    assert not attributes_within_racial_maximums(
        Race.HUMAN,
        Attributes(19, 18, 18, 18, 18),
    )
