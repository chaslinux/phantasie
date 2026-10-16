"""Data models for Phantasie III characters."""

from dataclasses import dataclass
from enum import Enum


class Race(str, Enum):
    """Character races documented in the Phantasie III rulebook."""

    HUMAN = "Human"
    DWARF = "Dwarf"
    ELF = "Elf"
    GNOME = "Gnome"
    HALFLING = "Halfling"
    GNOLL = "Gnoll"
    GOBLIN = "Goblin"
    KOBOLD = "Kobold"
    LIZARD_MAN = "Lizard Man"
    MINOTAUR = "Minotaur"
    OGRE = "Ogre"
    ORC = "Orc"
    PIXIE = "Pixie"
    SPRITE = "Sprite"
    TROLL = "Troll"


class Profession(str, Enum):
    """Character professions documented in the rulebook."""

    FIGHTER = "Fighter"
    MONK = "Monk"
    PRIEST = "Priest"
    RANGER = "Ranger"
    THIEF = "Thief"
    WIZARD = "Wizard"


@dataclass(frozen=True, slots=True)
class Attributes:
    """The five primary character attributes."""

    strength: int
    intelligence: int
    dexterity: int
    constitution: int
    charisma: int

    def values(self) -> tuple[int, int, int, int, int]:
        """Return attributes in the documented table order."""
        return (
            self.strength,
            self.intelligence,
            self.dexterity,
            self.constitution,
            self.charisma,
        )


@dataclass(frozen=True, slots=True)
class Character:
    """Core identity and attributes for a character."""

    name: str
    race: Race
    profession: Profession
    attributes: Attributes
