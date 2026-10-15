# Phantasie III Asset Guide

## Art direction

- Visual inspiration: Commodore 64 version of Phantasie III.
- Working palette: Sweetie 16.
- Palette reference: https://lospec.com/palette-list/sweetie-16
- Logical display resolution: 320 x 200.
- Display scaling: 3x nearest-neighbor.
- Preferred image format: PNG.
- Transparency: Use alpha transparency for sprites and UI elements.

## Images

### Title screen

| Filename | Purpose |
|---|---|
| title_background.png | Optional title screen background |
| title_logo.png | Optional title logo |

### User interface: assets/images/ui/

| Filename | Purpose |
|---|---|
| panel_border.png | Reusable panel border |
| cursor.png | Menu selection cursor |
| button_normal.png | Normal button |
| button_selected.png | Selected button |
| divider.png | Horizontal divider |

### Characters: assets/images/characters/

| Filename | Purpose |
|---|---|
| warrior.png | Warrior sprite |
| mage.png | Mage sprite |
| cleric.png | Cleric sprite |
| thief.png | Thief sprite |

### Portraits: assets/images/portraits/

| Filename | Purpose |
|---|---|
| warrior_portrait.png | Warrior portrait |
| mage_portrait.png | Mage portrait |
| cleric_portrait.png | Cleric portrait |
| thief_portrait.png | Thief portrait |

### World: assets/images/world/

| Filename | Purpose |
|---|---|
| grass_tile.png | Grass terrain |
| forest_tile.png | Forest terrain |
| mountain_tile.png | Mountain terrain |
| water_tile.png | Water terrain |
| dungeon_floor.png | Dungeon floor |
| dungeon_wall.png | Dungeon wall |
| town_building.png | Town building |

### Enemies: assets/images/enemies/

| Filename | Purpose |
|---|---|
| goblin.png | Goblin |
| skeleton.png | Skeleton |
| orc.png | Orc |
| dragon.png | Dragon |

### Items: assets/images/items/

| Filename | Purpose |
|---|---|
| sword.png | Sword icon |
| shield.png | Shield icon |
| potion.png | Potion icon |
| gold.png | Gold icon |

### Effects: assets/images/effects/

| Filename | Purpose |
|---|---|
| sword_slash.png | Melee attack effect |
| magic_bolt.png | Magical projectile |
| healing_effect.png | Healing effect |

## Fonts: assets/fonts/

| Filename | Purpose |
|---|---|
| fantasy_pixel.ttf | Main interface font |
| fantasy_pixel_bold.ttf | Headings and emphasis |

## Music: assets/audio/music/

| Filename | Purpose |
|---|---|
| title_theme.ogg | Title screen music |
| exploration.ogg | Exploration music |
| combat.ogg | Combat music |

## Sound effects: assets/audio/sfx/

| Filename | Purpose |
|---|---|
| menu_move.wav | Menu navigation |
| menu_select.wav | Menu confirmation |
| sword_hit.wav | Weapon impact |
| spell_cast.wav | Spell casting |

## Notes

- These filenames describe planned assets, not existing files.
- Artwork is created separately from the game code.
- Asset dimensions will be documented as the relevant systems are implemented.
- Missing optional assets should not prevent the game from starting.

