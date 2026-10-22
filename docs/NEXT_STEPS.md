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
- Exploration map with walls, open tiles, and a waystone event tile.
- Cardinal movement using the arrow keys or WASD.
- Collision detection preventing movement through walls.
- Map boundary validation.
- Persistent exploration position during the current game session.
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
- Active encounter tracking in the exploration screen.
- Basic encounter fleeing.
- Exploration movement is restricted while an encounter is active.
- Encounter generation and monster data are separate from Pygame rendering.

### Current Limitations

The encounter system is not yet a complete combat system.

- Encounters can occur before the player reaches the waystone.
- Active encounters can be fled, but there is no turn-based combat yet.
- Defeating monsters, victory rewards, and experience distribution are not implemented.
- Selecting New Game can reuse existing characters and adventure state instead of starting a completely fresh game.
- Exploration position persists when returning to the title screen and re-entering exploration.
- Saving and loading are not implemented.
- The Continue menu option is not implemented.

### Latest Verification

The latest reported complete test run passed:

- 108 automated tests passed.
- Ruff linting passed.
- Ruff formatting checks passed.
- Mypy reported no issues in 19 source files.
- git diff --check passed.

The game has launched successfully using:

    python3 -m phantasie

The working tree contains uncommitted changes related to encounter handling and its tests. Review the current Git status before committing.

## Development Approach

Continue building the game in small, testable increments.

Guidelines:

- Keep game logic separate from Pygame rendering and input handling.
- Write automated tests for new functionality.
- Run the complete test suite after integrating each feature.
- Run Ruff, formatting checks, and Mypy before committing.
- Run git diff --check before committing.
- Keep changes focused on one feature at a time.
- Commit working features to Git before beginning the next major feature.
- Push completed commits to GitHub.
- Update this document as the project evolves.
- Avoid introducing a complicated architecture before the gameplay requirements justify it.

## Immediate Priority: Stabilize Encounter Handling

Before beginning the full combat system, finish and commit the existing encounter work.

### Step 1: Verify Encounter Behavior

Confirm that:

- Successful ordinary movement checks for random encounters.
- Blocked movement does not trigger encounters.
- Waystone events do not trigger random encounters.
- Encounter messages display correctly.
- An active encounter prevents ordinary exploration movement.
- Pressing the flee key exits the encounter.
- Fleeing clears the active encounter.
- Fleeing does not unintentionally reset the exploration position.
- The player can continue exploring after fleeing.

Investigate the interaction between encounter probability and waystone placement. The player should have a reasonable opportunity to discover the waystone without being trapped in a sequence of encounters.

Do not disable random encounters globally just to make the waystone easier to reach. Prefer a small, testable adjustment to encounter probability or encounter eligibility if necessary.

### Step 2: Add or Update Tests

Add automated tests for:

- Encounter activation.
- Movement restrictions during an encounter.
- Fleeing an encounter.
- Clearing encounter state after fleeing.
- Resuming exploration after fleeing.
- Waystone discovery without a random encounter on the same move.
- Preservation of exploration coordinates.
- Reproducible encounter behavior using a seeded random-number generator.

Use deterministic tests rather than relying on the probability of a random outcome.

### Step 3: Verify Code Quality

Run:

    pytest -q
    ruff check .
    ruff format --check .
    mypy src
    git diff --check

Resolve all failures before proceeding.

### Step 4: Review, Commit, and Push

Inspect the changes:

    git status --short --branch
    git diff --stat
    git diff

Confirm that the changes are limited to the intended encounter behavior and tests.

Commit the completed work and push it to GitHub. Verify that the local branch is synchronized with origin/main.

## Next Priority: New Game State Reset

Fix the behavior where selecting New Game can reuse existing game data.

### Step 1: Define New Game Behavior

Starting a new game should create a fresh adventure rather than silently resuming the previous one.

Clarify the distinction between:

- The character roster available for party selection.
- The active adventure party.
- The current exploration position.
- The world event state, including whether the waystone has been discovered.
- Any future combat, inventory, and progression state.

Decide which information should persist between adventures and which should be reset.

For the initial implementation:

- Reset the active adventure party.
- Reset the exploration position to the starting coordinates.
- Reset exploration event state.
- Clear any active encounter.
- Clear stale party selections and setup messages.
- Ensure the previous adventure cannot continue accidentally after starting a new one.

Character roster persistence can remain a separate decision. If the roster is intended to persist, document that behavior clearly. Do not confuse roster persistence with continuing an old adventure.

### Step 2: Implement a Focused Reset

Introduce a small, explicit new-adventure initialization path.

Prefer a single, testable method responsible for resetting adventure state over scattered assignments throughout screen handlers.

Avoid recreating the entire application or screen manager just to reset the adventure.

### Step 3: Add Regression Tests

Test that:

- Starting a new adventure resets exploration coordinates.
- The waystone can be discovered again in the new adventure.
- Active encounter state is cleared.
- The new adventure party contains only the newly selected members.
- Stale party selections do not carry over unintentionally.
- Existing character creation and roster behavior remain correct.
- Returning to the title screen does not reset state unexpectedly unless that is the intended behavior.

Run the full test suite and code quality checks.

## Following Priority: Turn-Based Combat

Once encounter handling and new-game initialization are stable and committed, implement basic turn-based combat.

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
- Prevent additional exploration encounters while combat is active.

Keep combat state separate from the exploration screen wherever practical.

### Step 3: Turn Order and Attacks

Implement a simple turn-based combat loop.

Initial goals:

- Allow party members to attack.
- Allow living monsters to attack.
- Apply damage and update hit points.
- Skip defeated combatants.
- Detect victory and defeat.
- Prevent actions after combat has ended.
- Provide a clear way to return to exploration after combat.

Fleeing from an encounter should remain supported, with its behavior integrated consistently into the combat system.

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
- Fleeing from combat.
- Correct preservation of exploration state.

Use deterministic tests wherever randomness is involved.

### Step 5: Integration and Verification

Before considering combat complete:

- Run the complete pytest suite.
- Run Ruff linting and formatting checks.
- Run Mypy.
- Run git diff --check.
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
- Any additional state required to resume an adventure accurately.

Use a versioned save format where practical so future changes can be handled safely.

Add tests for saving, loading, invalid data, and incompatible save formats.

The Continue menu option should be implemented alongside or after the save system.

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

## Current Priority Order

1. Stabilize random encounter handling and fleeing.
2. Commit and push the encounter work.
3. Fix new-game initialization and state reset behavior.
4. Commit and push the new-game fix.
5. Implement basic turn-based combat.
6. Implement experience and character progression.
7. Add inventory and equipment.
8. Implement saving and loading.

Complete and test each feature before moving to the next.
