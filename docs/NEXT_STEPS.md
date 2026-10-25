# Phantasie III — Development Roadmap

## Current Status

The project has a working foundation for a retro-style RPG inspired by
the Commodore 64 version of Phantasie III.

Development is being carried out across Ubuntu and Linux Mint systems.
The source code is synchronized through Git, but local environments
and uncommitted changes may differ between machines.

### Implemented Features

- [x] Pygame application loop and screen management.
- [x] Title screen and navigation.
- [x] Character creation with races, professions, and attributes.
- [x] Party roster and adventure party selection.
- [x] Exploration map and player movement.
- [x] Exploration events.
- [x] Random monster encounters.
- [x] Combatant model with hit points, attack, and defense.
- [x] Turn-based combat model.
- [x] Combat screen with attack, defend, and flee actions.
- [x] Combat victory and defeat states.
- [x] Combat integration with exploration.
- [x] Automated combat and combat-screen tests.
- [x] Fix character reroll input interfering with name entry.
- [x] Reset character-creation fields when starting another character.
- [x] Prevent the keypress that opens character creation from
      appearing in the new character's name.

### Latest Test Results

The most recent reported full test run on Linux Mint completed with:

- 140 tests passed.
- One Pygame AVX2 performance warning.
- No failing tests.

The warning concerns Pygame's build configuration and does not indicate
a failing test.

The character-creation fixes were subsequently tested manually and
both reported issues were resolved.

Run the complete test suite after making further changes:

    python -m pytest

### Development Environment

- Ubuntu laptop: used for development and editing with gedit.
- Linux Mint desktop: also used for development and testing.
- GitHub: used to synchronize committed source code between systems.

Keep Python dependencies and virtual environments configured
appropriately on each machine. A Git pull does not synchronize
installed Python packages or virtual environments.

Do not commit virtual environments, Python cache files, or temporary
editor backups.

## Immediate Next Steps

### 1. Commit and Push the Current Changes

The combat implementation and the recent character-creation fixes
need to be accounted for in Git.

Before committing:

- [ ] Check the current branch and working-tree status.
- [ ] Review all uncommitted changes with `git diff`.
- [ ] Confirm which combat-related changes are already committed.
- [ ] Review the character-creation fixes.
- [ ] Run Python compilation checks.
- [ ] Run the complete test suite.
- [ ] Run `git diff --check`.
- [ ] Stage only the intended files.
- [ ] Commit coherent changes with descriptive commit messages.
- [ ] Push commits to GitHub when authentication is available.
- [ ] Verify that the local branch and remote are synchronized.

Suggested commit messages, depending on what is already committed:

    Add turn-based combat system

    Fix character creation input handling and reset

Do not create duplicate commits for changes that have already been
committed.

Do not force-push if Git reports that the remote contains unexpected
commits. Inspect and reconcile the branch first.

### 2. Verify Changes Across Both Computers

- [ ] Push committed changes from the machine holding the latest work.
- [ ] Pull the changes on the other development machine.
- [ ] Run the test suite on both systems.
- [ ] Investigate any differences in Python versions or dependencies.
- [ ] Confirm that both systems can launch the game successfully.

Do not assume that a clean working tree on one computer means the
other computer has the same files or environment.

## Combat Improvements

### 3. Exercise Combat Through the Game

Test the combat system through normal gameplay rather than relying
only on unit tests.

- [ ] Start a new game and create characters.
- [ ] Select an adventure party.
- [ ] Explore until a monster encounter occurs.
- [ ] Confirm that the combat screen opens.
- [ ] Verify that attacks reduce hit points correctly.
- [ ] Verify that defeated monsters cannot attack.
- [ ] Verify that defeated party members cannot act.
- [ ] Verify that defense reduces incoming damage correctly.
- [ ] Verify that fleeing returns to exploration.
- [ ] Verify that victory returns to exploration.
- [ ] Verify that defeat follows the intended game flow.
- [ ] Check that starting a new encounter resets combat state.

### 4. Improve Turn Handling

The current combat implementation lets the selected party member
attack, then allows surviving monsters to retaliate.

Decide how party turns should work before expanding the combat rules.

Potential improvements:

- [ ] Allow every living party member to take a turn.
- [ ] Define the order in which party members and monsters act.
- [ ] Prevent defeated combatants from taking turns.
- [ ] Make defending reduce damage for the intended duration.
- [ ] Clear temporary defensive states at the correct time.
- [ ] Add tests for multi-member parties and multiple monsters.

Keep combat rules in the combat model where practical, rather than
duplicating game rules in the screen implementation.

### 5. Improve Combat Feedback

- [ ] Display clear messages for attacks, damage, and defeats.
- [ ] Make the active party member easy to identify.
- [ ] Make enemy status and remaining hit points clear.
- [ ] Ensure that victory and defeat messages are understandable.
- [ ] Verify that fleeing and other combat actions produce appropriate
      feedback.
- [ ] Keep text within the logical 320-by-200 display.

## Character Progression

### 6. Add Experience and Levels

The Monster model already defines an `experience_reward`, but the
character model does not yet have experience or level fields.

Before implementing rewards:

- [ ] Decide how character progression will be represented.
- [ ] Preserve the existing immutable Character model if practical.
- [ ] Define starting experience and level.
- [ ] Define how much experience is needed for each level.
- [ ] Decide whether experience is awarded individually or shared.
- [ ] Add validation and unit tests for progression rules.

### 7. Award Combat Rewards

- [ ] Award experience when all monsters are defeated.
- [ ] Ensure rewards are granted only once per encounter.
- [ ] Do not award victory experience for fleeing or defeat.
- [ ] Display a victory message and the experience gained.
- [ ] Add tests for single-monster and multiple-monster encounters.

### 8. Add Level-Up Mechanics

After experience rewards are working:

- [ ] Define level-up thresholds.
- [ ] Decide which attributes or statistics improve on level-up.
- [ ] Display level-up notifications.
- [ ] Test characters gaining one or more levels.
- [ ] Ensure progression remains consistent across encounters.

Use the original Commodore 64 version of Phantasie III as a reference
when deciding how closely to reproduce its character progression.

## Saving and Loading

### 9. Persist Game Progress

- [ ] Choose a save-file format, such as JSON.
- [ ] Save character names, races, professions, and attributes.
- [ ] Save experience and levels when implemented.
- [ ] Save party membership and relevant adventure progress.
- [ ] Validate save data when loading.
- [ ] Handle missing, invalid, or incompatible save files safely.
- [ ] Add round-trip serialization tests.

## Gameplay Improvements

### 10. Expand Exploration

- [ ] Connect exploration events to meaningful game mechanics.
- [ ] Add additional encounters and encounter variety.
- [ ] Consider treasure, equipment, and other discoveries.
- [ ] Keep exploration deterministic in tests by injecting random
      number generators where appropriate.
- [ ] Ensure exploration and combat state remain consistent when
      transitioning between screens.

### 11. Improve Character Creation

The basic character-creation system is implemented, and recent
keyboard-handling issues have been fixed.

Future improvements should preserve those fixes.

- [x] Prevent the reroll shortcut from interfering with name entry.
- [x] Clear the previous name when starting another character.
- [x] Prevent the opening character-creation shortcut from becoming
      part of the character's name.
- [ ] Review the character-creation flow for usability.
- [ ] Consider a more deliberate sequence for entering a name,
      choosing a race and profession, and rolling attributes.
- [ ] Make rerolling an explicit action outside the name field.
- [ ] Add regression tests for keyboard input and screen transitions.
- [ ] Compare character-generation rules with the original C64 game.

Do not redesign the entire character-creation system unless the
existing implementation or gameplay requirements justify it.

## Quality and Maintenance

### 12. Keep the Project Stable

For each feature:

- [ ] Add or update unit tests.
- [ ] Add integration tests for screen transitions where appropriate.
- [ ] Run `python -m pytest`.
- [ ] Run `git diff --check`.
- [ ] Review `git diff` before staging.
- [ ] Commit each coherent milestone separately.
- [ ] Push completed milestones to GitHub when authentication is
      available.
- [ ] Verify changes on the other development machine.

Avoid committing virtual environments, Python cache files, temporary
editor files, or backup files unless they are intentionally part of
the project.

### 13. Maintain Cross-Platform Development

- [ ] Keep dependencies documented in the project requirements files.
- [ ] Check Python and Pygame versions when behavior differs between
      systems.
- [ ] Verify that the project installs and runs in its virtual
      environment on each machine.
- [ ] Avoid relying on machine-specific paths.
- [ ] Run the test suite after pulling changes on another computer.
- [ ] Keep Git history and commit messages clear enough to identify
      completed work.

## Suggested Development Order

1. Verify, commit, and push the outstanding combat and character-
   creation changes.
2. Synchronize both development machines.
3. Test the complete exploration-to-combat flow in the running game.
4. Finalize party and monster turn handling.
5. Improve combat messages and status displays.
6. Add character experience and leveling.
7. Award experience for victories.
8. Add save and load support.
9. Expand exploration and gameplay.
10. Polish the interface and balance combat.
11. Continue improving fidelity to the Commodore 64 version.

## Current Milestone

**Milestone:** Initial turn-based combat integration and character-
creation input fixes.

**Completed recently:**

- Fixed the reroll shortcut interfering with character-name entry.
- Fixed the character-creation form retaining the previous character's
  name.
- Fixed the opening character-creation shortcut appearing in the
  character's name.
- Verified the fixes manually.
- Achieved a full test run of 140 passing tests on Linux Mint before
  the latest character-creation changes.

**Immediate goal:** Verify the current Git state, commit the outstanding
changes, push when authentication is available, synchronize the
development machines, and then continue improving the combat system.
