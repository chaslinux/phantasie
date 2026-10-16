"""Documented race limits and profession modifiers."""

from phantasie.characters.models import Attributes, Profession, Race

# Maximum attributes by race, in STR, INT, DEX, CON, CHA order.
# Source: Phantasie III rulebook, Maximum Attributes by Race.
RACIAL_MAXIMUMS: dict[Race, Attributes] = {
    Race.HUMAN: Attributes(18, 18, 18, 18, 18),
    Race.DWARF: Attributes(20, 17, 17, 19, 17),
    Race.ELF: Attributes(17, 19, 19, 17, 18),
    Race.GNOME: Attributes(19, 17, 18, 19, 17),
    Race.HALFLING: Attributes(16, 18, 20, 18, 17),
    Race.GNOLL: Attributes(20, 13, 17, 21, 11),
    Race.GOBLIN: Attributes(17, 14, 18, 17, 11),
    Race.KOBOLD: Attributes(17, 15, 19, 19, 13),
    Race.LIZARD_MAN: Attributes(19, 14, 17, 18, 13),
    Race.MINOTAUR: Attributes(20, 14, 16, 19, 12),
    Race.OGRE: Attributes(21, 14, 16, 19, 13),
    Race.ORC: Attributes(19, 16, 17, 18, 14),
    Race.PIXIE: Attributes(16, 18, 21, 16, 17),
    Race.SPRITE: Attributes(16, 18, 22, 16, 17),
    Race.TROLL: Attributes(22, 13, 15, 20, 12),
}

# Profession modifiers in STR, INT, DEX, CON, CHA order.
# Source: Phantasie III rulebook, Attribute Modifiers by Class.
PROFESSION_MODIFIERS: dict[Profession, Attributes] = {
    Profession.FIGHTER: Attributes(2, -2, 1, 0, -1),
    Profession.MONK: Attributes(0, 0, 1, 0, 0),
    Profession.PRIEST: Attributes(0, 2, 0, 0, 0),
    Profession.RANGER: Attributes(0, 1, 0, 0, 1),
    Profession.THIEF: Attributes(-2, 0, 2, 0, -1),
    Profession.WIZARD: Attributes(-4, 3, -2, 0, 1),
}


def attributes_within_racial_maximums(
    race: Race,
    attributes: Attributes,
) -> bool:
    """Return whether attributes do not exceed their racial maximums."""
    maximums = RACIAL_MAXIMUMS[race]
    return all(
        value <= maximum
        for value, maximum in zip(attributes.values(), maximums.values(), strict=True)
    )
