
# Phantasie III for Linux — Next Steps and Development Handoff

## 1. Project Overview

We are developing a playable Linux implementation of Phantasie III: The Wrath of Nikademus, inspired by the original Commodore 64 release.

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

The objective is to build a playable retro RPG with recognizable Phantasie III mechanics, not necessarily an exact reproduction of every original game feature.

Research original mechanics when practical, but prioritize a coherent, enjoyable, playable game. Document assumptions when original rules are unknown or when we deliberately simplify them.

## 2. Development Workflow

The developer prefers incremental development, with working features tested before proceeding to the next milestone.

Before making changes:

1. Inspect the current repository state.
2. Review relevant source files, tests, and documentation.
3. Identify what has already been implemented.
4. Propose the next small, useful change.
5. Avoid rewriting working code unnecessarily.

After making changes, run the relevant tests and quality checks.

Activate the virtual environment from the repository root:

```bash
source .venv/bin/activate
```

Run the game:

```bash
python -m phantasie
```

Run the full test suite:

```bash
python -m pytest -v
```

Run Ruff:

```bash
ruff check .
ruff format --check .
```

Format Python files when needed:

```bash
ruff format .
```

Run mypy:

```bash
mypy src/phantasie
```

Before committing:

```bash
git status
git diff --check
git diff
```

Stage only the intended files, commit, and push when requested.

## 3. Current Implementation

The repository already contains the following functionality.

### Application Foundation

- Pygame application loop.
- 320 × 200 logical rendering canvas.
- 3× scaled display.
- Sweetie 16 palette.
- Keyboard-controlled title menu.
- Screen manager with lifecycle hooks and transitions.
- Placeholder options screen.
- Quit handling.

### Character Data Model

The package `src/phantasie/characters/` contains:

- `models.py`
- `rules.py`
- `__init__.py`

The current model includes:

- `Race`
- `Profession`
- `Attributes`
- `Character`

The documented character races and professions are represented by enums.

Attributes are represented by a frozen dataclass containing:

- Strength
- Intelligence
- Dexterity
- Constitution
- Charisma

The rules module defines racial attribute maximums, profession modifiers, attribute validation, and attribute generation.

The initial attribute-generation implementation is a project design choice, not a verified reproduction of the original Commodore 64 algorithm.

### Character Creation Screen

Implemented in:

`src/phantasie/screens/character_creation.py`

The character creation screen is integrated into the existing screen manager.

Implemented functionality includes:

- Entering a character name.
- Selecting a race.
- Selecting a profession.
- Generating attributes.
- Displaying character attributes.
- Rejecting confirmation when the name is blank.
- Confirming a character.
- Storing the confirmed character in the game state.
- Cancelling character creation with Escape.

The developer has manually verified that the behavior and usability work correctly.

Automated tests are in:

`tests/test_character_creation.py`

### Existing Architecture

Important files include:

```text
src/phantasie/
├── game.py
├── menu.py
├── palette.py
├── screen_manager.py
├── characters/
│   ├── __init__.py
│   ├── models.py
│   └── rules.py
└── screens/
    ├── __init__.py
    ├── base.py
    ├── title.py
    ├── placeholder.py
    └── character_creation.py

tests/
├── test_game.py
├── test_menu.py
├── test_palette.py
├── test_screen_manager.py
├── test_screen_transitions.py
├── test_characters.py
└── test_character_creation.py

docs/
├── ASSETS.md
└── CHARACTER_GENERATION.md
```

Always inspect the actual repository before relying on this list. It may have changed since this document was written.

## 4. Recent Git History

The following commits were confirmed in the development session:

- `40b9677` — Implement character creation screen
- `f833a56` — Update CHARACTER_GENERATION.md
- `9eebf84` — Update CHARACTER_GENERATION.md
- `ceff4c8` — Add initial docs/CHARACTER_GENERATION.md document
- `9cf431b` — Add initial character models and documented rules
- `175c199` — Integrate screen manager and screen transitions

Commit `40b9677` was created successfully.

The next action after creating this document is to verify whether that commit has been pushed. Do not assume that a commit was pushed merely because it was created.

Use:

```bash
git status
git log -5 --oneline
git push
```

If the commit is already on the remote, there may be nothing to push.

## 5. Latest Confirmed Quality Checks

After character creation was implemented, the reported results were:

- 46 tests passed.
- Ruff formatting check passed.
- Mypy reported no issues in 14 source files.
- One Ruff import-order issue remained in `src/phantasie/game.py` at the time of the report.

The import-order issue should be checked against the current repository rather than assumed to remain unresolved.

The developer subsequently confirmed that character creation behavior and usability work correctly.

Run the quality checks again before making larger changes.

## 6. Immediate Next Step: Party Management

The next milestone should turn character creation into the beginning of a playable RPG session.

At present, a character can be created and stored, but there is not yet a complete party-management or exploration loop.

Start by inspecting:

- `src/phantasie/game.py`
- `src/phantasie/characters/models.py`
- `src/phantasie/characters/rules.py`
- `src/phantasie/screens/character_creation.py`
- `tests/test_character_creation.py`
- `docs/CHARACTER_GENERATION.md`

Determine exactly how the confirmed character is stored and how character creation currently exits.

Do not assume a party model already exists.

### Proposed first party-management milestone

Implement a minimal party model that can hold one or more characters.

Potential responsibilities:

- Store party members in a defined order.
- Add a newly created character to the party.
- Expose party members for display and inspection.
- Prevent accidental loss of characters during screen transitions.
- Provide a foundation for future party limits and management rules.

Keep the party model independent of Pygame.

Add automated tests for the party model before integrating it into the interface.

Do not impose a maximum party size or other original-game restriction until it has been researched or explicitly chosen as a project simplification.

### Party screen

Once the data model is tested, implement a party screen that can:

- Display the party roster.
- Show each character's name, race, and profession.
- Show relevant attributes for the selected character.
- Return to the previous screen.
- Allow the player to continue toward exploration when appropriate.

Keep the visual design consistent with the title and character creation screens.

Use the existing screen manager rather than introducing another navigation system.

## 7. Next Major Milestone: A Playable Exploration Loop

After party management, prioritize a small but playable game loop.

A suggested initial loop is:

1. Create a character.
2. Add the character to the party.
3. Enter a simple exploration area.
4. Move through a small map.
5. Encounter an enemy or event.
6. Resolve a basic encounter.
7. Return to exploration.
8. Retain party state between screens.

The first playable version does not need the complete original world, every monster, all spells, or a complete item system.

It should demonstrate that the player can create a character, move around, encounter danger, and make meaningful progress.

### Exploration architecture

Consider introducing separate modules for:

- World and map data.
- Player position and movement rules.
- Exploration state.
- Encounter initiation.

Keep movement and encounter rules independent of Pygame where practical.

The screen should handle input and rendering. Game rules should determine what happens when the player moves or encounters an event.

Use small maps and simple interactions initially.

## 8. Combat

Implement a minimal turn-based combat system after the party and exploration foundations exist.

Potential initial features:

- One enemy type.
- Character attacks.
- Enemy attacks.
- Hit points.
- Damage calculations.
- Victory and defeat.
- A way to return to exploration after an encounter.
- Tests for combat outcomes.

Research the original game's mechanics where useful, but use clearly documented simplifications when necessary to get a playable version working.

Avoid implementing a large combat subsystem before the basic exploration loop works.

Keep combat rules independent of rendering and input.

## 9. Character and RPG Progression

Once basic combat is playable, consider:

- Character hit points.
- Experience points.
- Level progression.
- Equipment.
- Inventory.
- Spells and abilities.
- Status effects.
- Healing and recovery.
- Gold and rewards.

Review the existing character model before adding fields.

Avoid adding statistics merely because generic RPGs commonly have them. Each addition should serve the intended gameplay.

If a feature requires a substantial change to the character model, update the tests and documentation alongside the implementation.

## 10. Save and Load

Implement persistence after party, character, and exploration state have stabilized.

Potential requirements:

- Save and load the party.
- Preserve character attributes and progression.
- Preserve relevant exploration state.
- Use a versioned save format.
- Validate data when loading.
- Handle missing, malformed, or corrupted files.
- Avoid overwriting a valid save unexpectedly.
- Add automated persistence tests.

Use appropriate Linux user-data directories when preparing the game for distribution.

Do not treat Python object serialization as automatically safe for untrusted save files.

## 11. Graphics and Audio

Artwork is created offline by the developer.

Do not generate artwork automatically unless explicitly requested.

Maintain `docs/ASSETS.md` as the reference for asset filenames, dimensions, formats, and intended usage.

Use the Sweetie 16 palette consistently.

Potential asset categories include:

- Character portraits or sprites.
- Tiles and map elements.
- Monsters.
- Interface elements.
- Combat effects.
- Music and sound effects.
- Fonts.

Continue using placeholder graphics where necessary so gameplay development is not blocked by missing artwork.

## 12. Packaging and Distribution

Once the game has a useful playable loop, consider:

- Installation instructions for Debian and Ubuntu.
- Dependency management.
- Launch scripts or console entry points.
- Configuration files.
- Save-data locations.
- Error reporting.
- Versioned releases.
- Testing on multiple supported Linux distributions.

Keep the project installable through its existing Python packaging configuration.

Do not prioritize packaging work over the core playable loop unless installation problems prevent development or testing.

## 13. Development Principles

Follow these principles throughout development.

### Gameplay

- Prioritize a playable game over exhaustive historical accuracy.
- Preserve recognizable Phantasie III concepts and mechanics.
- Research original mechanics when doing so is practical.
- Clearly document deliberate simplifications.
- Avoid building a generic fantasy RPG unrelated to the project's goals.

### Architecture

- Keep `game.py` focused on application coordination and the main loop.
- Use `ScreenManager` for screen transitions.
- Keep game rules separate from Pygame.
- Prefer small modules with focused responsibilities.
- Avoid unnecessary dependencies and architectural complexity.

### Testing

- Add tests for new game rules.
- Test data models without initializing a graphical display.
- Use Pygame's dummy video driver for headless UI tests where appropriate.
- Run the full suite after integration changes.
- Fix linting, formatting, and type-checking errors rather than ignoring them.

### Git

- Inspect the working tree before changes.
- Review diffs before committing.
- Stage only intended files.
- Never assume local commits have been pushed.
- Avoid overwriting unrelated local work.

### Collaboration

- Work in small, verifiable steps.
- Explain the purpose of each change.
- Give precise filenames and complete code when code changes are needed.
- Avoid asking for information already available in the repository or this handoff.
- Ask the developer to provide local files when the repository or tool access does not expose the required information.
- Preserve working behavior unless a change has a clear benefit.

## 14. Instructions for the Next ChatGPT Session

Start by checking the current Git state and reading the existing documentation.

```bash
git status
git log -5 --oneline
git remote -v
find src tests docs -maxdepth 4 -type f | sort
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the quality checks:

```bash
ruff check .
ruff format --check .
python -m pytest -v
mypy src/phantasie
```

Review:

- `docs/CHARACTER_GENERATION.md`
- `docs/ASSETS.md`
- `src/phantasie/characters/models.py`
- `src/phantasie/characters/rules.py`
- `src/phantasie/screens/character_creation.py`
- `src/phantasie/game.py`

Verify the latest commits and whether the character creation commit has reached GitHub.

Then begin the party-management milestone.

Do not recreate character creation, repeat the original setup milestones, or replace the existing screen architecture unnecessarily.

## 15. Overall Goal

Build a maintainable, playable Linux RPG inspired by the Commodore 64 version of Phantasie III.

The current foundation includes a working title menu, screen transitions, character data models, attribute-generation rules, and a tested character creation interface.

The next priority is to turn those foundations into a persistent party and a small exploration-and-combat loop.

Focus on delivering a playable game incrementally, expanding mechanics as needed, and maintaining automated tests throughout development.

