"""Tests for the Sweetie 16 palette."""

from phantasie import palette


def test_palette_contains_16_colors() -> None:
    assert len(palette.COLORS) == 16


def test_palette_colors_are_rgb_tuples() -> None:
    for color in palette.COLORS.values():
        assert len(color) == 3
        assert all(0 <= channel <= 255 for channel in color)


def test_palette_background_matches_sweetie_16() -> None:
    assert palette.BACKGROUND == (26, 28, 44)


def test_palette_white_matches_sweetie_16() -> None:
    assert palette.COLORS["WHITE"] == (244, 244, 244)
