
"""Tests for the combat screen."""

import pygame
import pytest

from phantasie.characters.models import (
    Attributes,
    Character,
    Party,
    Profession,
    Race,
)
from phantasie.combat import Combat, CombatStatus
from phantasie.encounters import Monster
from phantasie.screens.combat import CombatScreen


@pytest.fixture(autouse=True)
def pygame_init():
    """Initialize Pygame with a headless video driver."""
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()


def make_character(name: str) -> Character:
    """Create a test character."""
    return Character(
        name=name,
        race=Race.HUMAN,
        profession=Profession.FIGHTER,
        attributes=Attributes(12, 10, 11, 13, 9),
    )


@pytest.fixture
def party() -> Party:
    """Create a party with one character."""
    result = Party()
    result.add_member(make_character("Arin"))
    return result


@pytest.fixture
def two_member_party() -> Party:
    """Create a party with two characters."""
    result = Party()
    result.add_member(make_character("Arin"))
    result.add_member(make_character("Bryn"))
    return result


@pytest.fixture
def monster() -> Monster:
    """Create a monster for combat."""
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


@pytest.fixture
def screen(combat: Combat) -> CombatScreen:
    """Create a combat screen with an active encounter."""
    result = CombatScreen()
    result.start_combat(combat)
    return result


def make_two_member_screen(monster: Monster) -> CombatScreen:
    """Create a screen with two party members and one monster."""
    combat = Combat(
        two_member_party_for_test(),
        (monster,),
    )
    result = CombatScreen()
    result.start_combat(combat)
    return result


def two_member_party_for_test() -> Party:
    """Build a two-member party for focused screen tests."""
    result = Party()
    result.add_member(make_character("Arin"))
    result.add_member(make_character("Bryn"))
    return result


def test_screen_starts_without_combat() -> None:
    """The screen should initially have no active encounter."""
    screen = CombatScreen()

    assert screen.combat is None
    assert screen.selected_member == 0
    assert screen.selected_monster == 0


def test_start_combat_resets_selection_and_message(combat: Combat) -> None:
    """Starting combat should initialize the encounter state."""
    screen = CombatScreen()
    screen.selected_member = 5
    screen.selected_monster = 3

    screen.start_combat(combat)

    assert screen.combat is combat
    assert screen.selected_member == 0
    assert screen.selected_monster == 0
    assert screen.message == "CHOOSE YOUR ACTION."
    assert screen.next_screen is None


def test_render_without_combat() -> None:
    """The screen should render safely without an encounter."""
    screen = CombatScreen()
    surface = pygame.Surface((320, 200))

    screen.render(surface)


def test_render_active_combat(screen: CombatScreen) -> None:
    """The screen should render an active encounter."""
    surface = pygame.Surface((320, 200))

    screen.render(surface)

    assert screen.combat is not None
    assert screen.combat.status is CombatStatus.ACTIVE


def test_enter_attacks_selected_monster(screen: CombatScreen) -> None:
    """Pressing Enter should attack the selected monster."""
    assert screen.combat is not None
    monster = screen.combat.monsters[0]
    original_hp = monster.hit_points

    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert monster.hit_points < original_hp


def test_space_marks_member_as_defending(monster: Monster) -> None:
    """Defending should consume an action and select the next member."""
    screen = make_two_member_screen(monster)

    assert screen.combat is not None
    screen.combat.monsters[0].hit_points = 20
    screen.combat.monsters[0].max_hit_points = 20

    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    )

    assert screen.combat is not None
    assert 0 in screen.combat.acted_members
    assert 0 in screen.defending
    assert screen.selected_member == 1
    assert "DEFENSIVE STANCE" in screen.message


def test_flee_returns_to_adventure(screen: CombatScreen) -> None:
    """Pressing F should request a return to exploration."""
    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f)
    )

    assert screen.next_screen == "adventure"
    assert "FLEE" in screen.message


def test_escape_returns_to_adventure(screen: CombatScreen) -> None:
    """Escape should request a return to exploration."""
    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    )

    assert screen.next_screen == "adventure"


def test_victory_returns_to_adventure_on_enter(
    screen: CombatScreen,
) -> None:
    """Enter after victory should return to exploration."""
    assert screen.combat is not None

    for monster in screen.combat.monsters:
        monster.take_damage(monster.hit_points)

    screen.combat._update_status()

    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert screen.combat.status is CombatStatus.VICTORY
    assert screen.next_screen == "adventure"


def test_defeat_returns_to_title_on_enter(
    screen: CombatScreen,
) -> None:
    """Enter after defeat should return to the title screen."""
    assert screen.combat is not None

    for member in screen.combat.party:
        member.take_damage(member.hit_points)

    screen.combat._update_status()

    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert screen.combat.status is CombatStatus.DEFEAT
    assert screen.next_screen == "title"


def test_non_key_events_are_ignored(screen: CombatScreen) -> None:
    """Non-keyboard events should not affect combat."""
    original_message = screen.message

    screen.handle_event(pygame.event.Event(pygame.MOUSEMOTION))

    assert screen.message == original_message
    assert screen.next_screen is None

def test_defending_reduces_incoming_damage(
    monster: Monster,
) -> None:
    """Defending reduces damage from a sufficiently strong monster."""
    stronger_monster = Monster(
        name="Ogre",
        hit_points=20,
        attack=6,
        defense=1,
        experience_reward=25,
    )
    screen = make_two_member_screen(stronger_monster)

    assert screen.combat is not None
    defender = screen.combat.party[0]
    original_hp = defender.hit_points

    # Arin defends; Bryn attacks, completing the party phase.
    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    )
    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    damage_taken = original_hp - defender.hit_points

    # The stronger monster should hit, but defense should reduce damage.
    assert damage_taken > 0
    assert damage_taken < screen.combat.monsters[0].attack
    assert screen.combat.round_number == 2
    assert screen.combat.defending == set()

def test_not_defending_takes_normal_incoming_damage(
    screen: CombatScreen,
) -> None:
    """Without defending, the member should take normal incoming damage."""
    assert screen.combat is not None

    member = screen.combat.party[0]
    original_hp = member.hit_points

    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert member.hit_points < original_hp

def test_party_members_act_before_monster_phase(
    monster: Monster,
) -> None:
    """The monster should wait until every living party member has acted."""
    screen = make_two_member_screen(monster)

    assert screen.combat is not None

    # Keep the monster alive through both party attacks.
    target = screen.combat.monsters[0]
    target.hit_points = 30
    target.max_hit_points = 30

    first_member = screen.combat.party[0]
    original_hp = first_member.hit_points

    # Arin attacks. The monster must not retaliate yet.
    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert first_member.hit_points == original_hp
    assert screen.combat.round_number == 1
    assert screen.selected_member == 1
    assert target.hit_points < 30

    # Bryn attacks. Now the monster phase should run.
    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert screen.combat.round_number == 2
    assert first_member.hit_points < original_hp

def test_defeated_monster_does_not_retaliate(
    monster: Monster,
) -> None:
    """Victory should prevent a defeated monster from retaliating."""
    screen = make_two_member_screen(monster)

    assert screen.combat is not None
    monster_combatant = screen.combat.monsters[0]

    # Make the monster weak enough for the first attack to defeat it.
    monster_combatant.hit_points = 1
    first_member = screen.combat.party[0]
    original_hp = first_member.hit_points

    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert screen.combat.status is CombatStatus.VICTORY
    assert first_member.hit_points == original_hp

