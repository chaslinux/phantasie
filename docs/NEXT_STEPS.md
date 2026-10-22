# Phantasie III - Next Steps

## Current Status

Phantasie III has a working foundation for an RPG inspired by the
classic Phantasie series.

The game currently supports character creation, party selection,
exploration, random encounters, encounter fleeing, and resetting
adventure state when starting a new game.

The next major gameplay milestone is implementing turn-based combat.

## Implemented Features

### Application and Navigation

- Pygame application initialization and main loop.
- Title screen and menu navigation.
- Screen manager for switching between screens.
- Rendering through a logical game canvas.
- Keyboard-driven navigation between screens.

### Characters and Parties

- Character creation.
- Character names, races, professions, and attributes.
- Character attribute validation and generation.
- Character roster management.
- Party management with support for multiple characters.
- Party screen with character selection and scrolling.
- New-adventure party selection from the existing character roster.
- Replacement of the active adventure party when a new party is selected.

### Exploration

- Exploration map with walls, open tiles, and a waystone event tile.
- Cardinal movement using arrow keys or WASD.
- Collision detection preventing movement through walls.
- Map boundary validation.
- Persistent exploration coordinates during an adventure.
- Separate party state for the active adventure.
- Exploration screen integrated with the screen manager.
- Exploration messages and event handling.
- Waystone discovery.
- Preservation of exploration position when returning to the title
  screen during the current application session.

### Random Encounters

- Monster data models with validated combat statistics and experience
  rewards.
- A small default monster roster.
- Random encounter generation with configurable encounter probability.
- Injectable random-number generator for reproducible tests.
- Random encounter checks after successful ordinary exploration
  movement.
- Encounter messages displayed during exploration.
- Blocked movement does not trigger random encounters.
- Waystone events do not trigger random encounters on the same move.
- Active encounter tracking in the exploration screen.
- Ordinary exploration movement is restricted while an encounter is
  active.
- Pressing F flees from an active encounter.
- Fleeing clears the active encounter.
- Fleeing preserves exploration coordinates.
- Exploration can resume after fleeing.
- Fleeing does not consume an additional movement action.
- Encounter generation and monster definitions are separate from
  Pygame rendering.

### New-Adventure Initialization

- Starting a new game resets exploration coordinates.
- Exploration event state is reset for the new adventure.
- Active encounter state is cleared.
- Exploration messages are reset.
- Previous party selections are cleared.
- Party selection starts at the first roster entry.
- The active adventure party is reset before a new adventure begins.
- The existing character roster is preserved.
- Returning to the title screen does not automatically reset the
  current adventure.
- Regression tests cover new-adventure state reset and party replacement.

## Current Verification

The latest complete verification run reported:

- 115 automated tests passed.
- Ruff linting passed.
- Ruff formatting checks passed.
- Mypy reported no issues in 19 source files.
- git diff --check passed.
- The relevant encounter, exploration, and game tests passed.

The game has previously launched successfully using:

    python3 -m phantasie

The test run produces a Pygame warning that the installed Pygame build
does not support AVX2 optimizations on the current system. This is a
performance warning, not a test failure.

Repeat the complete verification commands after future changes.

## Current Limitations

The game is not yet a complete RPG.

### Combat

- Encounters can occur during exploration, but combat is not implemented.
- Monsters cannot yet be defeated through player actions.
- Party members cannot yet attack monsters.
- Monsters do not take combat turns.
- Combat victory and defeat conditions are not implemented.
- Experience rewards are defined but are not awarded.
- Fleeing currently exits an encounter without combat consequences.

### Character Progression

- Experience is not tracked or distributed.
- Character advancement is not implemented.
- Character statistics do not increase through progression.

### Inventory and Equipment

- Inventory management is not implemented.
- Weapons and armor are not implemented as usable equipment.
- Equipment bonuses do not affect combat.

### Persistence

- Saving and loading are not implemented.
- The Continue menu option is not implemented.
- Adventure state is retained only during the current application
  session.

### World and Gameplay

- Exploration currently uses a small map.
- Only a small default monster roster exists.
- There are no additional maps, towns, shops, or quests.
- Combat, treasure, and progression rewards are not implemented.
- Spells and status effects are not implemented.

## Development Approach

Continue building the game in small, testable increments.

Guidelines:

- Keep game rules separate from Pygame rendering and input handling.
- Write automated tests for new functionality.
- Prefer deterministic tests when randomness is involved.
- Run the complete test suite after integrating each feature.
- Run Ruff, formatting checks, and Mypy before committing.
- Run git diff --check before committing.
- Keep changes focused on one feature at a time.
- Commit working features before beginning the next major feature.
- Push completed commits to GitHub.
- Update this document as the project evolves.
- Avoid introducing a complicated architecture before gameplay
  requirements justify it.
- Do not mark planned functionality as implemented until it exists
  and has been tested.

## Immediate Priority: Review Repository and Encounter Integration

Encounter generation, fleeing, and new-adventure initialization now
have regression tests.

Before beginning combat, perform a final review of the surrounding
implementation and repository contents.

### Step 1: Review Backup Files

The repository currently contains backup files alongside source files:

- src/phantasie/game.py.bak
- src/phantasie/screens/exploration.py.bak
- src/phantasie/screens/new_game.py.bak
- src/phantasie/screens/title.py.bak

Determine whether these files are intentional project assets or
temporary development backups.

If they are unnecessary backups, remove them in a separate, reviewed
change. Confirm that no project tooling or documentation depends on
them.

Avoid mixing unrelated cleanup with the combat implementation.

### Step 2: Review Encounter Behavior

Confirm that the current implementation continues to satisfy these
requirements:

- Successful ordinary movement checks for random encounters.
- Blocked movement does not trigger encounters.
- Waystone events do not trigger random encounters on the same move.
- Encounter messages are displayed correctly.
- Movement is restricted while an encounter is active.
- Fleeing clears the active encounter.
- Fleeing preserves exploration coordinates.
- The player can continue exploring after fleeing.
- Encounter probability remains configurable.
- Seeded random-number generators produce reproducible results.

Do not disable random encounters globally to make exploration easier.

### Step 3: Review New-Adventure Initialization

Confirm that:

- Starting a new game resets exploration coordinates.
- Waystone discovery can occur again in a new adventure.
- Active encounter state is cleared.
- The previous active adventure party is discarded.
- The existing character roster is preserved.
- Previous party selections do not carry over.
- Returning to the title screen does not unexpectedly reset progress.
- The selected party becomes the active adventure party.

Keep adventure reset logic centralized and testable.

### Step 4: Verify Code Quality

Run:

    pytest -q
    ruff check .
    ruff format --check .
    mypy src
    git diff --check

Resolve failures before proceeding.

Review the final Git diff before committing any cleanup or code changes.

## Next Priority: Turn-Based Combat

Once the final encounter and new-adventure review is complete,
implement a basic turn-based combat system.

Keep combat rules independent of Pygame rendering so they can be
tested without simulating the entire game interface.

### Step 1: Define Combat State

Introduce a combat model representing an active encounter.

The model should track:

- The party participating in combat.
- The opposing monsters.
- Current hit points for each combatant.
- Whether each combatant is alive or defeated.
- The current turn or active combatant.
- Whether combat is active, won, or lost.
- Combat messages or other information needed by the interface.

Do not modify immutable monster definitions to represent changing
combat hit points.

Use separate combat state for each monster instance.

Define clearly how party members' current hit points will be stored.
Avoid unexpectedly resetting character health when creating a combat
encounter.

Keep the initial implementation small and testable.

### Step 2: Implement Basic Combat Rules

Implement the minimum rules needed for a complete combat encounter.

Initial goals:

- Initialize combat from an exploration encounter.
- Allow living party members to attack.
- Allow living monsters to attack.
- Calculate and apply attack damage.
- Update hit points after damage.
- Prevent defeated combatants from taking turns.
- Determine when all monsters have been defeated.
- Determine when the party has been defeated.
- Prevent actions after combat has ended.
- Handle an empty or unavailable combat party safely.

Keep attack and damage calculations in the combat model rather than
the rendering code.

Start with straightforward, deterministic rules. More elaborate
formulas can be added later.

### Step 3: Implement Turn Order

Introduce a simple turn-based action sequence.

Initial goals:

- Determine which combatant acts next.
- Allow party members to perform their actions.
- Allow surviving monsters to respond.
- Skip defeated combatants.
- Prevent a combatant from acting more than once per turn.
- Detect victory and defeat immediately when their conditions occur.
- Prevent additional actions after victory or defeat.

Document the initial turn-order rules so the behavior is predictable
and easy to test.

### Step 4: Add a Combat Screen

Introduce a combat screen that displays:

- Party members.
- Opposing monsters.
- Current hit points.
- The active combatant or current turn.
- Combat messages.
- Available player actions.
- Victory or defeat messages.

Provide a clear way for the player to select or execute party actions.

Keep the screen focused on displaying state and translating input
into combat actions. The combat model should remain responsible for
the game rules.

### Step 5: Integrate Combat with Exploration

Connect encounter generation to the combat system.

Requirements:

- A random encounter transitions from exploration into combat.
- The current exploration coordinates are preserved.
- The active encounter cannot trigger duplicate combat.
- Exploration movement is unavailable while combat is active.
- Combat victory returns the player to exploration.
- Combat defeat produces a clear and consistent outcome.
- Fleeing remains available and has a clearly defined result.
- Combat state is cleared when combat ends.
- Starting a new adventure clears any remaining combat state.

Prefer explicit screen transitions and state ownership over scattered
assignments in event handlers.

Do not allow the exploration screen and combat screen to maintain
conflicting versions of the same active encounter.

### Step 6: Add Combat Tests

Add automated tests covering:

- Combat initialization.
- Combatant hit points.
- Attack and damage calculations.
- Damage application.
- Defeated combatants.
- Turn order.
- Skipping defeated combatants.
- Victory conditions.
- Defeat conditions.
- Prevention of actions after combat ends.
- Exploration-to-combat transitions.
- Prevention of duplicate encounters during combat.
- Return to exploration after victory.
- Fleeing from combat.
- Preservation of exploration coordinates.
- Clearing combat state after a new adventure begins.

Use deterministic tests for combat rules.

Test the combat model independently of the Pygame screen before
testing integration.

### Step 7: Verify and Commit

Before considering basic combat complete:

- Run the complete pytest suite.
- Run Ruff linting.
- Run Ruff formatting checks.
- Run Mypy.
- Run git diff --check.
- Launch the game and test combat manually.
- Review the Git diff.
- Commit the completed feature.
- Push the commit to GitHub.
- Update this document to reflect the verified implementation.

Do not begin advanced combat mechanics until the basic combat loop
works reliably.

## Following Priority: Experience and Character Progression

After basic combat is functional, implement experience and character
advancement.

Initial goals:

- Award experience for defeating monsters.
- Track experience for individual characters.
- Define how experience is distributed among party members.
- Introduce character advancement.
- Increase character statistics or hit points when appropriate.
- Display victory and advancement messages.
- Prevent duplicate rewards for the same encounter.

Keep progression rules consistent with the existing character model.

Add tests for experience awards, distribution, advancement thresholds,
and changes to character statistics.

## Following Priority: Inventory and Equipment

Introduce basic inventory and equipment management.

Initial goals:

- Represent items in the game.
- Track items owned by party members.
- Add weapons and armor.
- Introduce equipment slots.
- Apply equipment bonuses to combat.
- Support acquiring items through exploration or combat rewards.

Keep the initial item system small and extensible.

Add tests for item ownership, equipment changes, and the effects of
equipment on combat.

## Following Priority: Saving and Loading

Implement persistent game saves after the core gameplay loop is
established.

Save data should eventually include:

- Character names, races, and professions.
- Character attributes and progression.
- Current hit points and other relevant character state.
- Party membership and order.
- Inventory and equipment.
- Exploration position.
- World and event state.
- Any additional state required to resume an adventure accurately.

Use a versioned save format where practical so future changes can be
handled safely.

Add tests for:

- Saving a game.
- Loading a saved game.
- Restoring party membership and order.
- Restoring exploration position.
- Restoring character progression and inventory.
- Invalid or incomplete save data.
- Incompatible save formats.
- Missing save files.

Implement the Continue menu option alongside or after the save system.

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

Prioritize these features after exploration, combat, progression,
inventory, and saving are working reliably.

## Current Priority Order

1. Review encounter integration and new-adventure initialization.
2. Review and resolve the tracked backup files.
3. Implement the combat model and basic combat rules.
4. Implement turn order and combat actions.
5. Integrate combat with exploration and screen transitions.
6. Add combat regression tests and complete verification.
7. Implement experience and character progression.
8. Add inventory and equipment.
9. Implement saving and loading.
10. Expand the world and add further gameplay features.
