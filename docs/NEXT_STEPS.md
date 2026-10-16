# Phantasie III for Linux — Next Steps

## 1. Project Overview

We are developing a playable Linux implementation of *Phantasie III: The Wrath of Nikademus*, inspired by the original Commodore 64 release.

- Repository: https://github.com/chaslinux/phantasie
- Language: Python 3.10+
- Graphics and input: Pygame
- Target platform: Debian and Ubuntu Linux
- Logical resolution: 320 × 200
- Display scaling: 3× (960 × 600)
- Graphics palette: Sweetie 16
- Testing: pytest
- Linting and formatting: Ruff
- Static type checking: mypy

Prioritize a coherent, playable RPG that preserves recognizable Phantasie III mechanics. Historical accuracy is desirable where practical, but deliberate simplifications are acceptable when documented.

## 2. Current Implementation

### Application and Interface

- Pygame application loop and scaled rendering.
- Sweetie 16 palette.
- Keyboard-controlled title menu.
- Screen manager and screen transitions.
- Placeholder options screen.
- Title, character creation, and party screens.
- Keyboard navigation and screen instructions.

### Characters and Party

- Character data models for races, professions, attributes, and characters.
- Attribute generation and validation.
- Character creation with name, race, profession, and generated attributes.
- Character recruitment into the party.
- Sequential creation of multiple characters.
- Party model that preserves member order.
- Party roster display and member selection.
- Roster navigation for larger parties.

### Tests and Documentation

- Automated tests for the game, characters, character creation, party model, party screen, menus, screen management, and transitions.
- `docs/CHARACTER_GENERATION.md` documents character generation.
- `docs/ASSETS.md` documents asset conventions.

## 3. Immediate Next Milestone: Exploration

The basic character and party foundation is in place. The next priority is to let the player take the party into a simple game world.

- [ ] Add an exploration screen.
- [ ] Create a small test map using placeholder graphics.
- [ ] Implement player movement and map boundaries.
- [ ] Track the party's position in the exploration area.
- [ ] Add at least one encounter or interactive event.
- [ ] Preserve party and character state across screen transitions.
- [ ] Add automated tests for movement, boundaries, and exploration state.

### Initial Gameplay Loop

1. Create one or more characters.
2. View the party.
3. Enter an exploration area.
4. Move around the map.
5. Trigger an encounter or event.
6. Resolve the encounter.
7. Return to exploration with party state intact.

Keep the first map small. Focus on a working gameplay loop rather than a complete world or finished artwork.

## 4. Combat

After exploration works, implement a minimal turn-based combat system.

- [ ] Define combat state and combatants.
- [ ] Introduce one enemy type.
- [ ] Implement character and enemy attacks.
- [ ] Add hit points and damage calculations.
- [ ] Handle victory and defeat.
- [ ] Return to exploration after combat.
- [ ] Test combat outcomes and edge cases.

Keep combat rules independent of rendering and input. Research the original mechanics where useful and document deliberate simplifications.

## 5. Character Progression

After basic exploration and combat are playable:

- [ ] Character hit points and recovery.
- [ ] Experience and level progression.
- [ ] Equipment and inventory.
- [ ] Spells and special abilities.
- [ ] Status effects.
- [ ] Gold, rewards, and purchases.

Extend the existing character model carefully. Add mechanics incrementally with tests and documentation.

## 6. Save and Load

Implement persistence after party, character, and exploration state have stabilized.

- [ ] Save and load party data.
- [ ] Preserve character attributes and progression.
- [ ] Preserve relevant exploration state.
- [ ] Use a versioned save format.
- [ ] Validate loaded data.
- [ ] Handle missing, malformed, and corrupted saves.
- [ ] Add automated persistence tests.

Use appropriate Linux user-data directories. Do not deserialize untrusted save files using unsafe serialization mechanisms.

## 7. Graphics and Audio

Artwork is created offline. Do not generate artwork automatically unless explicitly requested.

Maintain `docs/ASSETS.md` as the reference for asset names, dimensions, formats, and intended usage.

Planned asset categories:

- Character portraits and sprites.
- Map tiles and environmental elements.
- Monsters.
- Interface elements.
- Combat effects.
- Music and sound effects.
- Fonts.

Use the Sweetie 16 palette consistently. Placeholder assets should not block gameplay development.

## 8. Packaging and Distribution

Prioritize distribution once the game has a useful playable loop.

- [ ] Verify installation on supported Debian and Ubuntu systems.
- [ ] Maintain Python packaging and dependency configuration.
- [ ] Document installation and launch instructions.
- [ ] Determine configuration and save-data locations.
- [ ] Add useful error reporting.
- [ ] Prepare versioned releases.
- [ ] Test on supported Linux distributions.

## 9. Development Workflow

Activate the virtual environment:

```bash
source .venv/bin/activate
