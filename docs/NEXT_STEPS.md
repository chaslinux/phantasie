
# Phantasie III - Next Steps

## Current Status

The project has a working foundation for an RPG inspired by Phantasie III.

Implemented features:

- Pygame application initialization and main loop.
- Title screen and menu navigation.
- Screen manager for switching between screens.
- Character creation.
- Character names, races, professions, and attributes.
- Character attribute validation and generation.
- Party management with support for multiple characters.
- Party screen with character selection and scrolling.
- Exploration map with walls, open tiles, and an event tile.
- Cardinal movement using the arrow keys or WASD.
- Collision detection preventing movement through walls.
- Map boundary validation.
- Persistent exploration position.
- Separate party state for the active adventure.
- Exploration screen integrated with the screen manager.
- Basic exploration messages and event handling.
- Monster data models with validated combat statistics and experience rewards.
- A small default monster roster.
- Random encounter generation with configurable encounter probability.
- Injectable random-number generator for reproducible tests.
- Random encounter checks after successful ordinary exploration movement.
- Encounter messages displayed during exploration.
- Blocked movement does not trigger random encounters.
- Waystone events do not trigger random encounters.
- Encounter generation and monster data are separate from Pygame rendering.

The latest reported test run has 106 automated tests passing.

Code quality checks:

- Ruff linting passes.
- Mypy type checking passes.
- Ruff formatting and Git whitespace checks require final verification after the latest changes.

The game has previously launched successfully. Pygame may display an AVX2 performance warning, but it does not prevent the game from running.

## Development Approach

Continue building the game in small, testable increments.

Guidelines:

- Keep game logic separate from Pygame rendering and input handling.
- Write automated tests for new functionality.
- Run the complete test suite after integrating each feature.
- Run Ruff, formatting checks, and Mypy before committing.
- Run `git diff --check` before committing.
- Keep changes focused on one feature at a time.
- Commit working features to Git before beginning the next major feature.
- Push completed commits to GitHub.
- Update this document as the project evolves.

## Immediate Priority: Finish Random Encounters

The initial random encounter implementation is in place. Finish verification and commit the feature before starting combat.

### Step 1: Final Code Quality Checks

Run:

- `pytest -q`
- `ruff check .`
- `ruff format --check .`
- `mypy src`
- `git diff --check`

Resolve all failures before proceeding.

### Step 2: Review the Changes

Inspect the working tree and diff.

Confirm that:

- Monster definitions are in `src/phantasie/encounters.py`.
- Monster data is validated.
- Encounter probability is configurable.
- Randomness can be controlled in tests.
- Successful ordinary movement triggers one encounter check.
- Blocked movement does not trigger an encounter.
- Waystone events retain their existing behavior.
- Encounter messages display correctly.
- Exploration position remains consistent.

### Step 3: Manual Gameplay Verification

Launch the game and verify:

- The application starts successfully.
- Character creation and party selection still work.
- The party enters exploration at the expected position.
- Arrow keys and WASD move the party correctly.
- Walls prevent movement.
- The waystone event still works.
- Random encounters can appear during exploration.
- Encounter messages are readable.
- The game remains responsive after an encounter message.

Investigate any issues before committing.

### Step 4: Commit and Push

Once all checks pass and manual verification is complete:

- Review `git status` and `git diff`.
- Commit the random encounter feature.
- Push the commit to GitHub.
- Confirm that the local branch is synchronized with `origin/main`.

## Next Feature: Turn-Based Combat

Once random encounters are committed and verified, implement a basic combat system.

### Step 1: Combat Data and Rules

Introduce combat logic independently of Pygame rendering.

Initial goals:

- Represent an active combat encounter.
- Track the party and opposing monsters.
- Track current hit points during combat.
- Determine whether combatants are alive or defeated.
- Calculate basic attack damage.
- Prevent defeated combatants from taking turns.

Keep the initial rules straightforward and testable.

### Step 2: Combat State and Screen

Introduce a combat state and a combat screen.

Requirements:

- Transition from exploration to combat when an encounter occurs.
- Preserve the party's exploration position during combat.
- Display party members and opposing monsters.
- Display current hit points.
- Show combat messages.
- Provide a clear way to select or execute party actions.

Avoid triggering additional exploration encounters while combat is active.

### Step 3: Turn Order and Attacks

Implement a simple turn-based combat loop.

Initial goals:

- Allow party members to attack.
- Allow living monsters to attack.
- Apply damage and update hit points.
- Skip defeated combatants.
- Detect victory and defeat.
- Prevent actions after combat has ended.

Defer spells, status effects, advanced monster behavior, and complicated combat formulas.

### Step 4: Combat Tests

Add automated tests covering:

- Combat initialization.
- Attack and damage calculations.
- Hit-point changes.
- Defeated combatants.
- Turn handling.
- Victory and defeat conditions.
- Exploration-to-combat transitions.
- Prevention of duplicate encounters during combat.
- Return to exploration after victory.
- Correct preservation of exploration state.

Use deterministic tests wherever randomness is involved.

### Step 5: Integration and Verification

Before considering combat complete:

- Run the complete pytest suite.
- Run Ruff linting and formatting checks.
- Run Mypy.
- Run `git diff --check`.
- Launch the game and test combat manually.
- Commit and push the completed feature.

## Following Feature: Experience and Character Progression

After basic combat is functional:

- Award experience for defeating monsters.
- Track experience for individual characters.
- Introduce character advancement.
- Increase character statistics or hit points when appropriate.
- Display victory and advancement messages.
- Define how experience rewards are distributed among party members.

Keep progression rules consistent with the existing character model.

## Following Feature: Inventory and Equipment

Introduce basic inventory and equipment management.

Initial goals:

- Represent items in the game.
- Track items owned by party members.
- Add weapons and armor.
- Introduce equipment slots.
- Apply equipment bonuses to combat.
- Support acquiring items through exploration or combat rewards.

Keep the initial item system small and extensible.

## Following Feature: Saving and Loading

Implement persistent game saves after the core gameplay loop is established.

Save data should eventually include:

- Character names, races, and professions.
- Character attributes and progression.
- Current hit points and other relevant character state.
- Party membership and order.
- Inventory and equipment.
- Exploration position.
- World and event state.

Use a versioned save format where practical so future changes can be handled safely.

Add tests for saving, loading, invalid data, and incompatible save formats.

## Longer-Term Ideas

Potential future features include:

- Multiple exploration maps.
- Additional monsters and encounter types.
- Monster groups.
- More sophisticated combat mechanics.
- Spells and magic.
- Status effects.
- Shops and equipment purchases.
- Treasure and rewards.
- Quests and scripted events.
- Towns and other locations.
- More sophisticated character progression.
- Improved graphics, animation, and sound.
- Additional game settings.

Prioritize these features after the core exploration, combat, progression, and saving systems are working.

## Current Priority

The immediate development priorities are:

1. Finish verification and commit random encounters.
2. Implement basic turn-based combat.
3. Implement experience and character progression.
4. Add inventory and equipment.
5. Implement saving and loading.

Complete and test each feature before moving to the next.

