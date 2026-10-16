
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
git status --short
git diff --check
git diff
```

Stage only the intended files, commit, and push when requested.

Do not claim that a commit has been pushed unless the remote repository confirms it.

## 3. Current Implementation

### Application Foundation

Implemented functionality includes:

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

The character model includes:

- `Race`
- `Profession`
- `Attributes`
- `Character`

The documented races and professions are represented by enums.

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

Features include:

- Entering a character name.
- Selecting a race.
- Selecting a profession.
- Generating and displaying attributes.
- Rejecting confirmation when the name is blank.
- Confirming a character.
- Adding the confirmed character to the party.
- Cancelling character creation with Escape.
- Returning to the title screen after confirmation or cancellation.

The developer has manually verified that the behavior and usability work correctly.

Automated tests are in:

`tests/test_character_creation.py`

### Party Model

The party model has been implemented in the character models module.

Current functionality includes:

- Creating an empty party.
- Adding characters to a party.
- Preserving member order.
- Reporting the number of party members.
- Exposing party members through an immutable collection.
- Keeping different party instances independent.

The party model is independent of Pygame.

Automated tests are in:

`tests/test_party.py`

No maximum party size has been imposed. Research or an explicit design decision should precede adding a party limit.

### Game Integration

The main application is implemented in:

`src/phantasie/game.py`

The game maintains party state and integrates character recruitment with the character creation screen.

Multiple characters can be recruited sequentially. The character creation screen resets the name field appropriately when preparing for another character, preventing text from a previously created character from being retained.

The next development step should build on this existing implementation rather than recreate character creation or the party model.

## 4. Current Architecture

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
├── test_character_creation.py
└── test_party.py

docs/
├── ASSETS.md
├── CHARACTER_GENERATION.md
└── NEXT_STEPS.md
```

Always inspect the actual repository before relying on this list. The project may have changed since this document was written.

## 5. Recent Git History

The latest confirmed local Git history is:

- `1e84ea0` — Add party model and character recruitment
- `a23fd4d` — Add development roadmap and handoff
- `40b9677` — Implement character creation screen
- `f833a56` — Update CHARACTER_GENERATION.md
- `9eebf84` — Update CHARACTER_GENERATION.md

At the last reported Git check:

- `1e84ea0` was the local HEAD.
- `a23fd4d` was `origin/main`.
- The new party and recruitment commit had not yet been confirmed on the remote.

The development roadmap was previously committed, but the most recent party and recruitment commit still needs to be pushed if it has not already been pushed.

Check the current state before acting:

```bash
git status --short
git log -5 --oneline
git remote -v
```

If the local branch is ahead of the remote and the working tree is ready, push when requested:

```bash
git push
```

Do not amend or recreate existing commits unnecessarily.

## 6. Latest Confirmed Quality Checks

After implementing the party model and correcting the character-name reset behavior, the developer reported the following results:

- Ruff checks passed.
- Ruff formatting checks passed.
- All 52 tests passed.
- Mypy reported no issues in 14 source files.
- `git diff --check` passed.

These results apply to the reported working tree at that time. Re-run the checks before making further changes or committing new work.

## 7. Immediate Next Step: Party Management Interface

The party model and recruitment functionality are implemented. The next useful milestone is to make the party visible and accessible through the game interface.

Start by inspecting:

- `src/phantasie/game.py`
- `src/phantasie/characters/models.py`
- `src/phantasie/screens/character_creation.py`
- `src/phantasie/screens/title.py`
- `src/phantasie/screen_manager.py`
- `tests/test_party.py`
- `tests/test_character_creation.py`
- `tests/test_screen_transitions.py`

Determine how the existing menu actions and screen transitions are structured before changing navigation.

### Proposed Party Screen

Implement a party screen that can:

- Display the current party roster.
- Show each character's name, race, and profession.
- Display relevant attributes for the selected character.
- Handle an empty party gracefully.
- Return to the title screen or previous screen using a consistent navigation convention.
- Provide a foundation for future character inspection and party management.

Keep the visual design consistent with the title and character creation screens.

Use the existing screen manager rather than introducing another navigation system.

Add automated tests for the party screen and its transitions.

### Navigation

Inspect how the title menu currently handles selection and actions.

Choose a simple, consistent way to access the party screen. Avoid adding unnecessary menu complexity.

If a party menu option is added, ensure it behaves sensibly when the party is empty.

Do not implement party rearrangement, dismissal, formation, or a party-size restriction until those features are needed.

## 8. Next Major Milestone: A Playable Exploration Loop

After the party screen, prioritize a small but playable game loop.

A suggested initial loop is:

1. Create one or more characters.
2. View the party roster.
3. Enter a simple exploration area.
4. Move through a small map.
5. Encounter an enemy or event.
6. Resolve a basic encounter.
7. Return to exploration.
8. Retain party and character state between screens.

The first playable version does not need the complete original world, every monster, all spells, or a complete item system.

It should demonstrate that the player can recruit characters, explore, encounter danger, and make meaningful progress.

### Exploration Architecture

Consider introducing separate modules for:

- World and map data.
- Player position and movement rules.
- Exploration state.
- Encounter initiation.

Keep movement and encounter rules independent of Pygame where practical.

The screen should handle input and rendering. Game rules should determine what happens when the player moves or encounters an event.

Use small maps and simple interactions initially.

## 9. Combat

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

## 10. Character and RPG Progression

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

## 11. Save and Load

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

## 12. Graphics and Audio

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

## 13. Packaging and Distribution

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

## 14. Development Principles

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
- When asked for Markdown documents, provide plain Markdown source using standard Markdown syntax that can be copied directly into a text editor.

## 15. Instructions for the Next ChatGPT Session

Start by checking the current Git state and reading the existing documentation.

```bash
git status --short
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
git diff --check
```

Review:

- `docs/CHARACTER_GENERATION.md`
- `docs/ASSETS.md`
- `docs/NEXT_STEPS.md`
- `src/phantasie/characters/models.py`
- `src/phantasie/characters/rules.py`
- `src/phantasie/screens/character_creation.py`
- `src/phantasie/game.py`
- `tests/test_party.py`
- `tests/test_character_creation.py`

Verify the latest commits and whether the party and recruitment commit has reached GitHub.

Then proceed with the party-management interface.

Do not recreate character creation, rebuild the party model, repeat the original setup milestones, or replace the existing screen architecture unnecessarily.

## 16. Overall Goal

Build a maintainable, playable Linux RPG inspired by the Commodore 64 version of Phantasie III.

The current foundation includes a working title menu, screen transitions, character data models, attribute-generation rules, a tested character creation interface, a party model, and sequential character recruitment.

The next priority is to make the party accessible through the interface and then build a small exploration-and-combat loop.

Focus on delivering a playable game incrementally, expanding mechanics as needed, and maintaining automated tests throughout development.

