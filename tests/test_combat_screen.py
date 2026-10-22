"""Tests for the combat screen."""

import pygame
import pytest

from phantasie.characters.models import Attributes, Character, Party, Profession, Race
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


@pytest.fixture
def party() -> Party:
    """Create a party with one character."""
    result = Party()
    result.add_member(
        Character(
            name="Arin",
            race=Race.HUMAN,
            profession=Profession.FIGHTER,
            attributes=Attributes(12, 10, 11, 13, 9),
        )
    )
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


def test_space_marks_member_as_defending(screen: CombatScreen) -> None:
    """Pressing Space should select the defensive action."""
    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    )

    assert 0 in screen.defending
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


def test_victory_returns_to_adventure_on_enter(screen: CombatScreen) -> None:
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


def test_defeat_returns_to_title_on_enter(screen: CombatScreen) -> None:
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
    screen: CombatScreen,
) -> None:
    """Defending should prevent damage when reduction covers the attack."""
    assert screen.combat is not None

    member = screen.combat.party[0]
    original_hp = member.hit_points

    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    )
    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert member.hit_points == original_hp


def test_not_defending_takes_normal_incoming_damage(
    screen: CombatScreen,
) -> None:
    """Without defending, the member should take normal attack damage."""
    assert screen.combat is not None

    member = screen.combat.party[0]
    original_hp = member.hit_points

    screen.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    )

    assert member.hit_points < original_hp

