"""Exploration map and party movement state."""

from dataclasses import dataclass
from enum import Enum


class MoveResult(Enum):
    """Result of an attempted movement."""

    BLOCKED = "blocked"
    MOVED = "moved"
    EVENT = "event"


@dataclass(frozen=True, slots=True)
class ExplorationMap:
    """A rectangular, tile-based exploration map."""

    rows: tuple[str, ...] = (
        "###############",
        "#.............#",
        "#..###........#",
        "#.............#",
        "#.....###.....#",
        "#.............#",
        "#.......E.....#",
        "###############",
    )

    def __post_init__(self) -> None:
        """Validate the map layout."""
        if not self.rows:
            raise ValueError("The map must contain at least one row.")

        width = len(self.rows[0])

        if width == 0:
            raise ValueError("Map rows cannot be empty.")

        for row in self.rows:
            if len(row) != width:
                raise ValueError("All map rows must have equal width.")

            if any(tile not in "#.E" for tile in row):
                raise ValueError("Map contains an unsupported tile.")

    @property
    def width(self) -> int:
        """Return the map width in tiles."""
        return len(self.rows[0])

    @property
    def height(self) -> int:
        """Return the map height in tiles."""
        return len(self.rows)

    def tile_at(self, x: int, y: int) -> str:
        """Return the tile at the specified coordinates."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Coordinates are outside the map.")

        return self.rows[y][x]

    def is_walkable(self, x: int, y: int) -> bool:
        """Return whether a tile can be entered."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        return self.tile_at(x, y) != "#"


@dataclass(slots=True)
class ExplorationState:
    """Mutable state for a party exploring the map."""

    x: int = 1
    y: int = 1
    event_seen: bool = False

    def move(
        self,
        world: ExplorationMap,
        dx: int,
        dy: int,
    ) -> MoveResult:
        """Move one tile and report whether an event was encountered."""
        if abs(dx) + abs(dy) != 1:
            raise ValueError("Movement must be one tile in a cardinal direction.")

        target_x = self.x + dx
        target_y = self.y + dy

        if not world.is_walkable(target_x, target_y):
            return MoveResult.BLOCKED

        self.x = target_x
        self.y = target_y

        if world.tile_at(self.x, self.y) == "E" and not self.event_seen:
            self.event_seen = True
            return MoveResult.EVENT

        return MoveResult.MOVED
