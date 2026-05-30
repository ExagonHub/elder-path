# Elder Path — Dev Log

Development diary. Decisions, struggles, and progress notes.

---

## 29 May 2026

### v0.3 completed

- `data/items.json` created with POTION_001 (Health Potion) and LOOT_001 (Wolf Fang).
- `game/items.py` created with full inventory management system.
- `show_inventory(player)` — displays all 18 slots with item names or "Empty".
- `select_item(player)` — shows inventory, takes slot input, validates range and content, returns index and item. try/except handles non-numeric input.
- `use_item(player, index, item)` — applies item effect based on `item["effect"]`. Heal uses `min()` to cap HP at max_hp. Slot set to None after use.
- `drop_item(player, index)` — sets slot to None.
- `item_action(player)` — chains select_item with use/drop choice menu.
- `enemy_drop(player, enemy)` — 33% item drop chance, 65% gold drop chance. Item read from items.json via enemy's drop field. Gold randomized between gold_min and gold_max. Quality shown on drop.
- `player` dict updated: added `inventory`, `gold`, `max_hp`.
- `enemies.json` updated: added `drop`, `gold_min`, `gold_max` fields per enemy.
- Combat menu extended to 4 actions: Attack, Defence, Dodge, Use Item.

### Decisions made
- Item drop at 33%, gold drop at 65% — gold is more common to give economy purpose early.
- `max_hp` added to player for potion cap logic. Updated in `level_up` as well.
- Loot items have no `effect` or `value` — they exist only as sellable drops for the economy system in v0.7.
- Full inventory test deferred to v0.4 — Rich UI will make it much easier to verify visually.

### v0.2 completed

- `warrior_attack()`, `assassin_attack()`, `mage_attack()` functions added to `combat.py`.
- Each class now has a combat submenu inside the Attack action.
- Warrior stances: Normal (standard damage), Defensive (0.5x damage + damage reduction), Counter (50% chance 1.5x damage, 50% miss).
- Assassin attack types: Normal, Rapid (2x hits at 0.5x damage each), Piercing (50% chance 1.5x, 50% miss).
- Mage spells: Fireball (50% chance 1.5x damage), Frost (normal damage + 50% stun chance), Lightning (guaranteed normal damage).
- Defend action added — sets `is_defending = True`, halves enemy damage for that turn.
- Dodge action added — DEX * 5% success chance, avoids enemy attack entirely on success.
- Enemy flee mechanic added — enemy flees when HP drops below 20% of max HP. `max_hp` stored at combat start.
- `stunned`, `is_defending`, `dodged` state variables managed per turn in `start_combat`.

### Decisions made
- Rapid attack deals `damage // 2` per hit, applied as `damage * 2` total — keeps formula clean.
- Frost stun is handled in `start_combat` via `stunned` flag, not inside `mage_attack`.
- Enemy flee deferred for elite/boss — will be addressed in v0.8.
- Dodge chance scales with DEX to reward stat investment.

---

## 28 May 2026

### v0.1 completed

- Set up full project structure: `main.py`, `game/`, `data/`, documentation files.
- `data/classes.json` created with starting stats for Warrior, Assassin, and Mage.
- `data/enemies.json` created with initial enemy pool (Wolf, Goblin).
- `game/character.py`: `create_character()` handles name input, class selection, and builds the player dict from JSON data. `level_up()` handles XP check, HP/MP auto-increase, level increment, xp_to_next_level scaling (+50 per level), and 3-point manual stat distribution.
- `game/combat.py`: `start_combat()` runs the turn-based combat loop. Player attacks with class-specific damage formula (base_damage + 50% of STR/DEX/INT). Enemy attacks back each valid turn. Victory awards XP and triggers level_up check. Defeat ends the game.
- `main.py`: Main menu (Play, Settings, Quit), Play submenu (New Game, Load Game — Load Game is a placeholder), character creation and combat wired together.

### Decisions made
- Damage bonus set at 50% of primary stat — kept flat for now, will revisit at v1.0 balance pass.
- HP +10 and MP +5 per level up, fixed values chosen over percentage to keep scaling predictable.
- xp_to_next_level starts at 90 (~6 basic enemy kills), scales +50 per level.
- Load Game left as pass — save system planned for a later version.
- enemies.json uses ENEMY_001 style keys for flexibility.