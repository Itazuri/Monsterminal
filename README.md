# Monsterminal

A terminal-based monster battling roguelike. Fight your way through acts of increasingly tough enemies, level up your creature, and build a moveset as you go.

## How it works

Each act has 3 stages followed by a boss. At each stage you choose a path — battle, elite fight, campfire, or mystery event. Every fight you win earns your creature a level.

### Combat

Each turn you pick one of your creature's active moves. Move order is decided by speed, with a coinflip on ties. Moves can deal damage or apply stat changes:

- **Damage moves** — scale with your attack vs the enemy's defense
- **Defense down** — lowers the enemy's defense stage
- **Attack up / Defense up** — raises your own stats temporarily

Stat stages reset between battles (unless you skip the heal at a campfire).

### Leveling & Moves

Your creature has a personal learnset — a set of moves it learns at specific levels, fitting its type and style. You can have a maximum of **4 active moves** at a time.

- Below 4 moves: new moves are learned automatically on level up
- At 4 moves: you're prompted to replace one of your existing moves or skip learning the new one

Enemies scale with the act. Each act you gain 4 levels (3 fights + 1 boss), and enemies are tuned to match.

### Relics

Relics are passive items that modify combat in various ways. You can earn them from elite fights and act-clear rewards.

## Status

Early development. Planned additions include more creatures, moves, relics, events, and paths.