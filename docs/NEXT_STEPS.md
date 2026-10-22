# Phantasie III — Development Roadmap

## Current Status

The project has a working foundation for a retro-style RPG inspired by
Phantasie III.

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

### Latest Test Results

The most recent reported full test run completed with:

- 140 tests passed.
- One Pygame AVX2 performance warning.

The warning concerns Pygame's build configuration and does not indicate
a failing test.

Re-run the test suite before committing future changes:

    python3 -m pytest -q

## Immediate Next Steps

### 1. Verify and Commit the Combat Milestone

- [ ] Review the changes to the combat model, combat screen, exploration
      screen, and game integration.
- [ ] Review the new combat tests.
- [ ] Run Python compilation checks.
- [ ] Run the complete test suite.
- [ ] Run `git diff --check`.
- [ ] Stage only the intended files.
- [ ] Commit the changes.
- [ ] Push the commit to GitHub.
- [ ] Verify that the local branch and remote are synchronized.

Suggested commit message:

    Add turn-based combat system

Do not force-push if Git reports that the remote contains unexpected
commits. Inspect and reconcile the branch first.

## Combat Improvements

### 2. Exercise Combat Through the Game

- [ ] Start a new game and select an adventure party.
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

### 3. Improve Turn Handling

The current combat implementation lets the selected party member attack,
then allows surviving monsters to retaliate.

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

## Character Progression

### 4. Add Experience and Levels

The Monster model already defines an `experience_reward`, but the
character model does not yet have experience or level fields.

Before implementing rewards:

- [ ] Decide how character progression will be represented.
- [ ] Preserve the existing immutable Character model if practical.
- [ ] Define starting experience and level.
- [ ] Define how much experience is needed for each level.
- [ ] Decide whether experience is awarded individually or shared.
- [ ] Add validation and unit tests for progression rules.

### 5. Award Combat Rewards

- [ ] Award experience when all monsters are defeated.
- [ ] Ensure rewards are granted only once per encounter.
- [ ] Do not award victory experience for fleeing or defeat.
- [ ] Display a victory message and the experience gained.
- [ ] Add tests for single-monster and multiple-monster encounters.

### 6. Add Level-Up Mechanics

After experience rewards are working:

- [ ] Define level-up thresholds.
- [ ] Decide which attributes or statistics improve on level-up.
- [ ] Display level-up notifications.
- [ ] Test characters gaining one or more levels.
- [ ] Ensure progression remains consistent across encounters.

## Saving and Loading

### 7. Persist Game Progress

- [ ] Choose a save-file format, such as JSON.
- [ ] Save character names, races, professions, and attributes.
- [ ] Save experience and levels when implemented.
- [ ] Save party membership and relevant adventure progress.
- [ ] Validate save data when loading.
- [ ] Handle missing, invalid, or incompatible save files safely.
- [ ] Add round-trip serialization tests.

## Gameplay Improvements

### 8. Expand Exploration

- [ ] Connect exploration events to meaningful game mechanics.
- [ ] Add additional encounters and encounter variety.
- [ ] Consider treasure, equipment, and other discoveries.
- [ ] Keep exploration deterministic in tests by injecting random
      number generators where appropriate.

### 9. Improve the Combat Interface

- [ ] Show current and maximum hit points.
- [ ] Make the selected character and target easier to identify.
- [ ] Improve combat messages so players can understand each action.
- [ ] Display experience rewards and level-up results.
- [ ] Check that text fits the logical 320-by-200 display.

## Quality and Maintenance

### 10. Keep the Project Stable

For each feature:

- [ ] Add or update unit tests.
- [ ] Add integration tests for screen transitions where appropriate.
- [ ] Run `python3 -m pytest -q`.
- [ ] Run `git diff --check`.
- [ ] Review `git diff` before staging.
- [ ] Commit each coherent milestone separately.
- [ ] Push completed milestones to GitHub.

Avoid committing virtual environments, Python cache files, temporary
editor files, or backup files unless they are intentionally part of
the project.

## Suggested Development Order

1. Verify, commit, and push the current combat milestone.
2. Test the complete exploration-to-combat flow in the running game.
3. Finalize party and monster turn handling.
4. Add character experience and leveling.
5. Award experience for victories.
6. Add save and load support.
7. Expand exploration and gameplay.
8. Polish the interface and balance combat.

## Current Milestone

**Milestone:** Initial turn-based combat integration.

**Immediate goal:** Verify the combat implementation, run the complete
test suite, and commit and push the work to GitHub before adding
character progression.
