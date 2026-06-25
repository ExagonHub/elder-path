# Elder Path — Dev Log

Development diary. Decisions, struggles, and progress notes.

---

## 25 June 2026

### v0.6 completed

- `data/rooms.json` created — 7 rooms total: 1 village (Ember's Cross), 5 forest, 1 dungeon (The Hollow Depths). Fields: name, type, zone_type, encounter_chance, enemy_pool, chest, connections.
- `game/world.py` created — world and exploration module.
- `move(player)` — takes N/S/E/W direction input, maps to full direction name, checks connections, updates current_room and previous_room.
- `encounter(player)` — rolls against encounter_chance on room entry. Yellow zone presents Fight/Flee choice. Red zone forces combat automatically. Enemy selected randomly from enemy_pool.
- `death_penalty(player)` — reads zone_type from current room. Yellow: revives at 40% HP / 30% MP. Red: deducts 30% of current gold.
- `open_chest(player, location)` — triggered after combat in rooms with chest. Shows loot_pool items, player selects one, item added to first empty inventory slot, chest marked as opened.
- `display_room(location)` added to ui.py — Panel showing room name, zone type, and available paths in uppercase.
- `display_game_menu()` updated — Travel option added as 3rd choice, Quit Game replaces Exit.
- `player["current_room"]` and `player["previous_room"]` added to player dict in character.py.
- `zone_type` parameter added to `start_combat()` — enemy flee blocked in red zone.
- `encounter(player)` called inside `move()` after every room transition.
- Chest loot reads from weapons.json and armors.json — merged into single dict for lookup.

### Decisions made
- rooms.json over in-code definitions — consistent with data/logic separation pattern.
- N/S/E/W input — immersive, connections stored as full direction names in JSON.
- Flee in yellow zone returns player to previous_room — tracked in player dict, no extra parameters needed.
- Chest only in dungeon (red zone) — risk/reward balance, green and yellow zones need no reward incentive.
- Enemy pool as simple list — weighted pool deferred to v0.8 when enemy variety expands.
- zone_type passed as parameter to start_combat — combat.py stays independent of rooms.json.
- Red zone death penalty village respawn deferred — noted for future version.
- More menu / inventory access from game menu deferred — noted for post-v0.7.
- Terminal clear issue deferred — noted for post-v0.7.
- Player stats not displayed after combat deferred — noted for post-v0.7.

---

## 11 June 2026

### v0.5 completed

- `data/weapons.json` created — 9 weapons across 3 classes. Keys: WEAPON_001 format. Fields: name, type, damage, quality, price, slot, allowed_classes. Prices set to 0 placeholder.
- `data/armors.json` created — 6 armor entries (helmet + chest per class). Fields: name, type, defense, magic_resistance, quality, price, slot, allowed_classes.
- `data/accessories.json` created — ACC_001 Traveler's Amulet, Common quality, xp_luck +5%.
- `game/equipment.py` created — three core functions.
- `get_total_stats(player)` — iterates player["equipment"] slots, merges item stats onto base stats, returns combined dict. Base stats never modified.
- `equip_item(player, index, item)` — checks allowed_classes, handles two_hand slot locking (off_hand item auto-returned to inventory), auto-swaps occupied slots, places item in correct slot, clears inventory slot.
- `unequip_item(player, slot)` — checks inventory space before unequipping, returns item to first empty inventory slot, clears equipment slot.
- `display_equipment(player)` added to ui.py — three Rich Tables rendered side by side via Columns: Armor (helmet/chest/gloves/boots), Character (name/class/level/accessory), Weapons (main_hand/off_hand). Empty slots show [ empty ].
- `display_game_menu()` added to ui.py — in-game navigation panel: Combat, Equipment, Exit.
- Game loop added to main.py — while True loop after character creation, player chooses action before entering combat.
- `item_action()` updated in items.py — Equip option appears only for weapon/armor/accessory types. Equip calls equip_item() with player, index, item.
- player dict updated: defense=0, magic_resistance=0, equipment dict with all slots set to None.
- combat.py updated: base_damage now reads from get_total_stats(). Enemy damage reduced by player defense using max(0, ...) formula.

### Decisions made
- WEAPON_001 key format chosen over type-based keys (SWORD_001) — simpler, consistent with existing patterns.
- speed stat removed from weapons — attack speed meaningless in turn-based combat, deferred to Faz 2.
- magic_resistance added to armors but passive — no magic enemies yet, activates in v0.8.
- Accessory bonuses percentage-based — flat values lose value as economy scales.
- One accessory slot — expandable if a second accessory type is introduced later.
- Equip from inventory chosen over equip from equipment screen — reuses existing select_item flow.
- get_total_stats returns new dict — base stats stay clean, no risk of stat corruption on unequip.
- Starting equipment goes to inventory — player equips manually, consistent with game flow.
- Prices all 0 — balance deferred to v1.0 playtest.

---

## 01 June 2026

### v0.4 completed

- `game/ui.py` created — all visual output centralized here. Separation of concerns: data in character/combat/items, visuals in ui.
- `show_status(player, enemy=None)` — displays Player and Status panels side by side using Rich Columns. If enemy is provided, Enemy panel added as third column with dynamic HP bar.
- `display_inventory(player)` — displays 18-slot inventory as a Rich Table with Slot, Item, Quality columns. Quality color-coded: Common (bright_white), Uncommon (green), Rare (cyan), Epic (purple), Legendary (yellow).
- `display_level_up(player)` — displays level up panel when player levels up. Shows new level and +3 stat points message.
- `display_combat_menu(player)` — displays styled combat action menu (Attack, Defence, Dodge, Use Item) in a Panel.
- `display_attack_menu(player)` — single function handles all three class attack submenus. Shows correct options based on player class.
- `display_main_menu()` — styled main menu panel centered on screen. Title: ELDER PATH, slogan: "Every beginning has its end."
- `display_play_menu()` — styled New Game / Load Game panel. Title: "Welcome to the Beginning."
- `display_class_menu()` — styled class selection panel with short description per class.
- `damage_colors` dict added globally in ui.py — maps damage types to colors (physical, fire, frost, lightning, critical, poison, shadow).
- `attack_to_damage` dict added in combat.py — maps attack_type strings to damage type keys.
- Hasar mesajları renklendirildi — her saldırı tipine göre ilgili renk uygulandı.
- Enemy HP bar implemented manually using █ and ░ characters. Color changes dynamically: green above 50%, yellow above 25%, red below 25%.
- `select_item()` updated — input 0 returns None, None to allow exiting inventory.
- `item_action()` updated — checks for None return from select_item, exits cleanly.
- `max_mp` added to player dict for consistency with max_hp.
- `max_mp` now scales on level up alongside max_hp.

### Decisions made
- ui.py created as separate file — all Rich components live here, not scattered across game files.
- `show_status` extended with optional enemy parameter instead of a separate display_enemy_info call — avoids rendering gap between panels.
- Manual HP bar chosen over Rich Progress — Progress is designed for live updates, not per-turn redraws. Manual bar gives full color control.
- Visual polish details (menu alignment, panel sizing consistency, grid-style inventory) deferred to later versions — noted in TODO.
- Keyboard navigation for menus deferred — requires prompt_toolkit, out of scope for v0.4.
- Item info screen (show item details on selection) deferred — noted in TODO.
- damage_colors and attack_to_damage kept as dicts — clean, extensible, no if/elif chains needed when new damage types are added.

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