"""Tests for the turn-based combat model."""

import pytest

from phantasie.characters.models import (
    Attributes,
    Character,
    Party,
    Profession,
    Race,
)
from phantasie.combat import Combat, CombatStatus, Combatant
from phantasie.encounters import Monster


@pytest.fixture
def character() -> Character:
    """Create a test character."""
    return Character(
        name="Arin",
        race=Race.HUMAN,
        profession=Profession.FIGHTER,
        attributes=Attributes(12, 10, 11, 13, 9),
    )


@pytest.fixture
def party(character: Character) -> Party:
    """Create a party with one character."""
    result = Party()
    result.add_member(character)
    return result


@pytest.fixture
def monster() -> Monster:
    """Create a test monster."""
    return Monster(
        name="Goblin",
        hit_points=6,
        attack=3,
        defense=1,
        experience_reward=10,
    )


@pytest.fixture
def combat(party: Party, monster: Monster) -> Combat:
    """Create a combat encounter."""
    return Combat(party, (monster,))


def test_combat_initializes_combatants(combat: Combat) -> None:
    """Combat should create independent combat state."""
    assert combat.status is CombatStatus.ACTIVE
    assert len(combat.party) == 1
    assert len(combat.monsters) == 1
    assert combat.party[0].name == "Arin"
    assert combat.monsters[0].name == "Goblin"
    assert combat.monsters[0].hit_points == 6


def test_monster_definition_is_not_modified(
    combat: Combat,
    monster: Monster,
) -> None:
    """Damage should not change the original monster definition."""
    original = monster.hit_points

    combat.attack(combat.party[0], combat.monsters[0])

    assert monster.hit_points == original
    assert combat.monsters[0].hit_points < original


def test_attack_applies_damage(combat: Combat) -> None:
    """Attacks should reduce the defender's hit points."""
    attacker = Combatant("Attacker", 10, 5, 0, 10)
    defender = Combatant("Defender", 10, 1, 2, 10)

    damage = combat.calculate_damage(attacker, defender)

    assert damage == 3
    defender.take_damage(damage)
    assert defender.hit_points == 7


def test_damage_cannot_reduce_hit_points_below_zero() -> None:
    """Excess damage should leave the defender at zero hit points."""
    combatant = Combatant("Goblin", 6, 3, 1, 6)

    combatant.take_damage(20)

    assert combatant.hit_points == 0
    assert not combatant.is_alive


def test_negative_damage_is_rejected() -> None:
    """Damage must not be negative."""
    combatant = Combatant("Goblin", 6, 3, 1, 6)

    with pytest.raises(ValueError, match="Damage cannot be negative"):
        combatant.take_damage(-1)


def test_defeated_combatant_cannot_attack(combat: Combat) -> None:
    """A combatant with no hit points cannot attack."""
    combat.party[0].take_damage(combat.party[0].hit_points)

    with pytest.raises(ValueError, match="cannot attack"):
        combat.attack(combat.party[0], combat.monsters[0])


def test_defeated_monster_cannot_be_attacked(combat: Combat) -> None:
    """A defeated monster cannot be attacked again."""
    monster = combat.monsters[0]
    monster.take_damage(monster.hit_points)

    with pytest.raises(ValueError, match="cannot be attacked"):
        combat.attack(combat.party[0], monster)


def test_defeating_all_monsters_wins_combat(combat: Combat) -> None:
    """Defeating the last monster should produce victory."""
    monster = combat.monsters[0]
    monster.take_damage(monster.hit_points)

    combat._update_status()

    assert combat.status is CombatStatus.VICTORY


def test_defeating_the_entire_party_loses_combat(combat: Combat) -> None:
    """Defeating the last party member should produce defeat."""
    member = combat.party[0]
    member.take_damage(member.hit_points)

    combat._update_status()

    assert combat.status is CombatStatus.DEFEAT


def test_actions_are_rejected_after_victory(combat: Combat) -> None:
    """Combat actions should not be allowed after victory."""
    monster = combat.monsters[0]
    monster.take_damage(monster.hit_points)
    combat._update_status()

    with pytest.raises(RuntimeError, match="already ended"):
        combat.attack(combat.party[0], monster)


def test_empty_party_is_rejected(monster: Monster) -> None:
    """Combat requires a party member."""
    with pytest.raises(ValueError, match="at least one party member"):
        Combat(Party(), (monster,))


def test_empty_monster_group_is_rejected(party: Party) -> None:
    """Combat requires at least one monster."""
    with pytest.raises(ValueError, match="at least one monster"):
        Combat(party, ())
