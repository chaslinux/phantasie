"""Tests for the exploration map and movement."""

import pytest

from phantasie.world import ExplorationMap, ExplorationState, MoveResult


def test_default_map_has_expected_dimensions() -> None:
    world = ExplorationMap()

    assert world.width == 15
    assert world.height == 8


def test_map_rejects_inconsistent_row_widths() -> None:
    with pytest.raises(ValueError, match="equal width"):
        ExplorationMap(rows=("###", "#..#"))


def test_map_rejects_unsupported_tiles() -> None:
    with pytest.raises(ValueError, match="unsupported tile"):
        ExplorationMap(rows=("###", "#X#"))


def test_map_boundaries_are_not_walkable() -> None:
    world = ExplorationMap()

    assert not world.is_walkable(-1, 0)
    assert not world.is_walkable(world.width, 0)
    assert not world.is_walkable(0, -1)
    assert not world.is_walkable(0, world.height)


def test_map_rejects_out_of_bounds_tile_lookup() -> None:
    world = ExplorationMap()

    with pytest.raises(IndexError):
        world.tile_at(-1, 0)


def test_party_can_move_across_open_tiles() -> None:
    world = ExplorationMap()
    state = ExplorationState()

    result = state.move(world, 1, 0)

    assert result is MoveResult.MOVED
    assert (state.x, state.y) == (2, 1)


def test_party_cannot_walk_through_walls() -> None:
    world = ExplorationMap()
    state = ExplorationState(x=3, y=1)

    result = state.move(world, 0, 1)

    assert result is MoveResult.BLOCKED
    assert (state.x, state.y) == (3, 1)


def test_party_cannot_walk_outside_map() -> None:
    world = ExplorationMap()
    state = ExplorationState(x=1, y=1)

    result = state.move(world, -1, 0)

    assert result is MoveResult.BLOCKED
    assert (state.x, state.y) == (1, 1)


def test_movement_requires_one_cardinal_step() -> None:
    world = ExplorationMap()
    state = ExplorationState()

    with pytest.raises(ValueError, match="cardinal direction"):
        state.move(world, 1, 1)


def test_entering_event_tile_triggers_event_once() -> None:
    world = ExplorationMap()
    state = ExplorationState(x=7, y=6)

    result = state.move(world, 1, 0)

    assert result is MoveResult.EVENT
    assert (state.x, state.y) == (8, 6)
    assert state.event_seen

    state.move(world, -1, 0)
    result = state.move(world, 1, 0)

    assert result is MoveResult.MOVED
