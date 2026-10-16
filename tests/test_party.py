"""Tests for party management."""

from phantasie.characters.models import (
    Attributes,
    Character,
    Party,
    Profession,
    Race,
)


def make_character(name: str) -> Character:
    """Create a character for testing."""
    return Character(
        name=name,
        race=Race.HUMAN,
        profession=Profession.FIGHTER,
        attributes=Attributes(
            strength=12,
            intelligence=10,
            dexterity=11,
            constitution=13,
            charisma=9,
        ),
    )


def test_new_party_is_empty() -> None:
    party = Party()

    assert party.member_count == 0
    assert party.members == ()


def test_adding_character_increases_member_count() -> None:
    party = Party()
    character = make_character("Arin")

    party.add_member(character)

    assert party.member_count == 1


def test_party_preserves_member_order() -> None:
    party = Party()
    first = make_character("Arin")
    second = make_character("Borin")

    party.add_member(first)
    party.add_member(second)

    assert party.members == (first, second)


def test_party_returns_immutable_member_collection() -> None:
    party = Party()
    party.add_member(make_character("Arin"))

    members = party.members

    assert isinstance(members, tuple)
    assert len(members) == 1


def test_parties_keep_their_members_separate() -> None:
    first_party = Party()
    second_party = Party()
    character = make_character("Arin")

    first_party.add_member(character)

    assert first_party.member_count == 1
    assert second_party.member_count == 0
