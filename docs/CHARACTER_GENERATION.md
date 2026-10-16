# Phantasie III — Character Generation Research

## Purpose

This document records the character-creation rules for the Commodore 64 version of *Phantasie III: The Wrath of Nikademus*.
Its purpose is to distinguish verified game mechanics from unresolved questions before implementing the character generator.
The implementation must reproduce the original C64 game's behavior as faithfully as the available evidence permits. Rules from other versions of Phantasie must not be assumed to apply without verification.

## Primary references

1. **Phantasie III C64 Rule Book**, hosted by Lemon64:
   https://www.lemon64.com/doc/phantasie-3/445

2. **Supplemental Rules for the Commodore 64 Version**, hosted by DigitPress:
   https://www.digitpress.com/library/manuals/c64/phantasie.pdf

3. **Phantasie III Manual**, hosted by Scribd:
   https://www.scribd.com/document/970942316/Phantasie-III-Manual-ENG

4. **Phantasie III C64 Guide**, hosted by GameFAQs:
   https://gamefaqs.gamespot.com/c64/567264-phantasie-iii-the-wrath-of-nikademus/faqs/15136

The rulebook is the primary source for documented mechanics. The C64 supplemental rules establish platform-specific differences. The other references are secondary sources that may help investigate gameplay and technical behavior.

## 1. Primary attributes

The C64 rulebook documents five primary attributes.

Attribute	Abbreviation	Documented purpose
Strength	STR	Physical strength, heavy equipment requirements, and melee damage
Intelligence	INT	Mental ability and spellcasting
Dexterity	DEX	Accuracy, avoidance, weapon eligibility, certain skills, and spellcasting
Constitution	CON	Endurance, toughness, and modification of hit points
Charisma	CHA	Training and spell-learning costs

The documented attribute range is 3–22.

Status: Confirmed by the Phantasie III rulebook.

The range alone does not establish the order in which initial random values, profession modifiers, and racial limits are applied.

2. Races and racial maximums

The rulebook documents 15 races, divided into five standard races and ten less civilized humanoid or fairy-like races described as random creatures.

Attribute order: STR, INT, DEX, CON, CHA.

Race	STR	INT	DEX	CON	CHA
Human	18	18	18	18	18
Dwarf	20	17	17	19	17
Elf	17	19	19	17	18
Gnome	19	17	18	19	17
Halfling	16	18	20	18	17
Gnoll	20	13	17	21	11
Goblin	17	14	18	17	11
Kobold	17	15	19	19	13
Lizard Man	19	14	17	18	13
Minotaur	20	14	16	19	12
Ogre	21	14	16	19	13
Orc	19	16	17	18	14
Pixie	16	18	21	16	17
Sprite	16	18	22	16	17
Troll	22	13	15	20	12

Status: The table matches the racial maximums in the C64 rulebook.

The implementation uses Race.LIZARD_MAN; the manual's table shortens the name to Lizard.

These values describe racial maximums. They do not establish whether the original generator applies racial limits before or after profession modifiers.

3. Professions and attribute modifiers

The game has six professions.

Attribute order: STR, INT, DEX, CON, CHA.

Profession	STR	INT	DEX	CON	CHA
Fighter	+2	-2	+1	0	-1
Monk	0	0	+1	0	0
Priest	0	+2	0	0	0
Ranger	0	+1	0	0	+1
Thief	-2	0	+2	0	-1
Wizard	-4	+3	-2	0	+1

Status: The table matches the profession-modifier table in the C64 rulebook.

The modifiers must not be confused with initial attribute values. The exact character-generation procedure must be established specifically for Phantasie III.

4. Profession eligibility

The manual distinguishes the five standard races from random creatures.

Its descriptions state that random creatures can be Fighters or Thieves only. The standard race descriptions recommend particular professions, but recommendations are not necessarily hard eligibility restrictions.

Examples of recommended combinations include:

Fighters: Humans, Dwarves, and Gnomes.
Monks: Humans, Elves, and Halflings.
Priests: Humans.
Rangers: Humans and Dwarves.
Thieves: Humans, Halflings, and Gnomes.
Wizards: Humans and Elves.

These are descriptions of races that make good choices for each profession, not a complete eligibility matrix.

Status: The random-creature restriction is documented. The complete set of legal combinations and the exact behavior of the C64 character-creation interface still require verification.

Do not implement the recommendations above as hard restrictions without further evidence.

5. Confirmed character-creation behavior

The Phantasie III rulebook establishes that:

Characters are defined by race, profession, individual attributes, and skill percentages.
Attributes are based on race and profession.
Initial attribute values are generated randomly and modified by race and profession.
The game displays character statistics for inspection.
Characters have a Luck value randomly determined from 8 to 13.
Characters have a social class.
The Guild contains characters who can be selected for a party.
A party contains up to six adventurers.
Characters can be replaced while the party is in town.

The C64 supplemental rules establish a Guild capacity of 21 characters, differing from the Apple version.

The manual also describes six pre-generated, pre-equipped Guild members for the quick-start experience. These should not be assumed to represent the exact defaults used for every newly generated character.

Status: The general creation and party behavior is documented. The exact random-generation algorithm remains unresolved.

6. Derived statistics and skills

The manual documents nine skills:

Attack
Parry
Swim
Listen
Spot Trap
Disarm Trap
Find Item
Pick Lock
Fire Bow

Attributes influence character capabilities and skill percentages. Dexterity is relevant to several skills and combat actions.

The manual also establishes that:

Constitution modifies hit points.
Magic Points depend on profession and attributes.
Maximum Magic Points depend on profession and level.
Social class affects starting gold and gold earned when gaining levels.
Luck is randomly determined from 8 to 13.

Status: These relationships are documented, but the exact formulas and initial values needed for a faithful generator have not all been established.

7. Unresolved character-generation mechanics

The following questions must be resolved before implementing a faithful generator.

7.1 Random attribute generation
What exact random-number algorithm does the C64 executable use?
What is the distribution of initial attribute values?
Are the five attributes generated independently?
Does the algorithm use multiple random rolls per attribute?
Does the procedure differ from earlier Phantasie releases?
7.2 Modifier and limit ordering
Are profession modifiers applied before racial limits?
Are there separate minimum and maximum clamps?
Can a profession modifier produce an attribute below 3?
Are racial maximums applied before or after profession adjustments?
Can attributes be rerolled or adjusted after generation?
7.3 Character acceptance
Can the player reroll a generated character?
Are all attributes regenerated together or individually?
When is the character name entered?
Can the player revise race or profession without restarting?
Does the game reject certain combinations or merely produce weaker characters?
7.4 Initial skills and Luck
How are initial skill percentages calculated?
Which attributes and profession modifiers affect each skill?
Are skills randomized in addition to being derived from attributes?
Is Luck generated independently of other attributes?
Are any skills initialized differently by profession?
7.5 Derived combat statistics
What is the exact initial hit-point formula?
How does Constitution modify the result?
How are initial Magic Points calculated?
Which professions receive initial spells?
Are there any additional race- or profession-specific statistics?
7.6 Starting resources and equipment
How is social class assigned?
What starting-gold amounts correspond to each social class?
Does initial equipment vary by profession or race?
Do newly generated characters start with equipment, or must it be purchased?
Which defaults differ between generated characters and pre-generated Guild members?

Until these questions are resolved, the implementation must not invent formulas or defaults.

8. Research methodology

The next research phase should prioritize:

Inspecting the C64 supplemental rules alongside the main manual.
Locating a technical analysis of the Phantasie III C64 character-generation routine.
Examining the original executable with a C64 emulator or disassembler if documentary evidence is insufficient.
Comparing observed generation behavior against the documented attribute tables.
Recording the source and confidence level for each recovered formula.

A formula found for the original Phantasie or Phantasie II is not sufficient evidence that Phantasie III uses the same algorithm.

Where sources disagree, document the disagreement rather than silently selecting one interpretation.

9. Current implementation status

The initial character package was committed in Git commit 9cf431b.

Current files:

src/phantasie/characters/models.py
src/phantasie/characters/rules.py
src/phantasie/characters/__init__.py
tests/test_characters.py

The package defines:

The five primary attributes.
Fifteen race identifiers.
Six profession identifiers.
Racial maximum tables.
Profession modifier tables.
An upper-bound validation function.

The current validation function checks racial maximums only. It does not implement complete attribute validation or character generation.

The last reported quality-check results were:

Ruff linting: passed.
Ruff formatting verification: passed.
Pytest: 32 tests passed.
Mypy: no issues found in 13 source files.
10. Planned implementation sequence
Add deterministic tests for every racial maximum and profession modifier.
Establish the exact C64 attribute-generation algorithm.
Implement the generator as pure Python with reproducible random inputs.
Test minimums, maximums, modifier ordering, and boundary cases.
Establish initial skills, Luck, hit points, Magic Points, and equipment separately.
Implement complete validation using verified original rules.
Integrate character creation with the existing screen manager once the data model and rules are stable.
Add screen-level tests without coupling the underlying mechanics to Pygame.
Guiding principle

Implement confirmed mechanics, document uncertainty, and avoid substituting generic fantasy RPG conventions for the original game's rules.
