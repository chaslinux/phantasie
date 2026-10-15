"""Sweetie 16 colour palette.

Palette source: https://lospec.com/palette-list/sweetie-16
"""

from typing import Final

Color = tuple[int, int, int]

# Palette entries are indexed from 0 to 15.
COLORS: Final[dict[str, Color]] = {
    "BLACK": (26, 28, 44),  # #1A1C2C
    "PURPLE": (93, 39, 93),  # #5D275D
    "RED": (177, 62, 83),  # #B13E53
    "ORANGE": (239, 125, 87),  # #EF7D57
    "YELLOW": (255, 205, 117),  # #FFCD75
    "LIGHT_GREEN": (167, 240, 112),  # #A7F070
    "GREEN": (56, 183, 100),  # #38B764
    "TEAL": (37, 113, 121),  # #257179
    "DARK_BLUE": (41, 54, 111),  # #29366F
    "BLUE": (59, 93, 201),  # #3B5DC9
    "LIGHT_BLUE": (65, 166, 246),  # #41A6F6
    "CYAN": (115, 239, 247),  # #73EFF7
    "WHITE": (244, 244, 244),  # #F4F4F4
    "LIGHT_GRAY": (148, 176, 194),  # #94B0C2
    "GRAY": (86, 108, 134),  # #566C86
    "DARK_GRAY": (51, 60, 87),  # #333C57
}

# Semantic aliases keep the interface consistent.
BACKGROUND = COLORS["BLACK"]
PANEL = COLORS["DARK_GRAY"]
BORDER = COLORS["GRAY"]
TEXT = COLORS["WHITE"]
TEXT_MUTED = COLORS["LIGHT_GRAY"]
HIGHLIGHT = COLORS["YELLOW"]
ACCENT = COLORS["ORANGE"]
SUCCESS = COLORS["LIGHT_GREEN"]
DANGER = COLORS["RED"]

# Named colors used directly by interface components.
PURPLE = COLORS["PURPLE"]
