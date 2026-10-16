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

The project currently has 88 automated tests passing.

Code quality checks:

- Ruff linting passes.
- Ruff formatting checks pass.
- Mypy type checking passes.
- Git whitespace checks pass.

The game launches successfully. Pygame may display an AVX2 performance warning, but it does not prevent the game from running.

## Development Approach

Continue building the game in small, testable increments.

Guidelines:

- Keep game logic separate from Pygame rendering and input handling.
- Write automated tests for new functionality.
- Run the complete test suite after integrating each feature.
- Run Ruff, formatting checks, and Mypy before committing.
- Keep changes focused on one feature at a time.
- Commit working features to Git before beginning the next major feature.
- Push completed commits to GitHub.
- Update this document as the project evolves.

## Next Feature: Random Encounters

### Goal

Introduce monsters and random encounters during exploration.

The first implementation should establish the encounter system without implementing full combat.

### Step 1: Monster Data Models

Create the data structures needed to represent monsters.

Initially, monsters should have:

- A name.
- Hit points.
- Basic combat statistics, as needed for future combat.
- Experience rewards, for future character progression.

Keep the initial monster roster small.

Monster data and game rules should not depend on Pygame rendering.

### Step 2: Encounter Generation

Implement an encounter system that can determine whether an encounter occurs and select a monster or group of monsters.

Requirements:

- Use a controllable random-number generator or equivalent mechanism.
- Make encounter generation testable without relying on unpredictable test results.
- Keep encounter rules separate from screen rendering.
- Allow the encounter probability and monster selection rules to evolve later.

Start with a simple encounter probability and a small monster roster.

### Step 3: Integrate Encounters with Exploration

Connect encounter generation to successful exploration movement.

Requirements:

- Check for encounters after successful movement.
- Do not generate encounters when movement is blocked.
- Keep the party's exploration position consistent.
- Display an appropriate message when an encounter occurs.
- Avoid triggering multiple encounters from a single movement action.

The initial implementation may announce the encounter without starting combat.

### Step 4: Tests

Add automated tests covering:

- Monster data validation.
- Encounter generation.
- Encounter probability behavior.
- Monster selection.
- Successful movement triggering an encounter check.
- Blocked movement not triggering an encounter.
- Encounter messages.
- Correct handling of the party's exploration state.

Use deterministic tests wherever randomness is involved.

### Step 5: Integration and Verification

Before considering the feature complete:

- Run the full pytest suite.
- Run Ruff linting.
- Run Ruff formatting checks.
- Run Mypy.
- Run git diff --check.
- Launch the game and verify exploration behavior manually.

Commit and push the completed feature to GitHub.

## Following Feature: Turn-Based Combat

Once random encounters are working, implement a basic combat system.

Initial goals:

- Introduce a combat state.
- Display a combat screen.
- Show the party and opposing monsters.
- Allow party members to attack.
- Allow monsters to attack.
- Track hit points and damage.
- Detect victory and defeat.
- Return to exploration after combat ends.

Keep combat rules separate from Pygame rendering.

The first version should prioritize a working combat loop over complex mechanics.

Defer spells, status effects, advanced monster behavior, and complicated combat formulas until the basic system works.

## Following Feature: Experience and Character Progression

After combat is functional:

- Award experience for defeating monsters.
- Track experience for individual characters.
- Introduce character advancement.
- Increase character statistics or hit points when appropriate.
- Display victory and advancement messages.

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

Add tests for saving, loading, and invalid or incompatible save data.

## Longer-Term Ideas

Potential future features include:

- Multiple exploration maps.
- Additional monsters and encounters.
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

These features should be prioritized after the core exploration, combat, progression, and saving systems are working.

## Current Priority

The immediate development priority is:

1. Random encounters.
2. Basic turn-based combat.
3. Experience and character progression.
4. Inventory and equipment.
5. Saving and loading.

Complete and test each feature before moving to the next.

