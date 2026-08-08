# Elder Path — Dev Log

Development diary. Decisions, struggles, and progress notes.

---

## 09 August 2026

### v1.0 completed — playtest, balance, and save system

The first proper release milestone. The goal coming in was simple: make the game actually playable from start to finish by someone who isn't the developer. That meant a save system, a working economy, and combat that doesn't actively punish the player for progressing.

**Save system.** The architecture was always well-positioned for this — the entire game state already lived in a single `player` dict of pure JSON-compatible types. `save_game()` is literally `json.dump(player, file)`. `load_game()` lists saved files, lets the player pick one, reads it back, and drops them into the game loop from wherever they left off. Added a delete flow too — `D` from the load screen, select by number, confirm with Y/N.

The main design decision was where to gate saving: green zones only. Black zone death means losing all items — that penalty has to stay real. If the player could save inside a dungeon, they'd just save before every boss attempt and reload on death, which completely hollows out the risk system. Green zone save keeps the tension where it belongs.

Per-character files (`saves/<name>.json`) instead of a single savegame — no rework needed when multiple characters eventually exist, and the file naming is self-documenting. `save_version` field written into every save for forward compatibility; new fields added in future versions can be read with `.get()` defaults without breaking old saves.

The Load Game menu option was already a `pass` placeholder — the UI shell existed, just needed the internals. That placeholder turned out to be well-placed; wiring it up was straightforward.

One known gap: when a save is deleted or no saves exist, the game exits instead of returning to the main menu. `load_game()` returns `None` and `main()` has no handler for it. The game loop is duplicated between New Game and Load Game right now — `game_loop()` refactor would fix both issues cleanly, but it's a structural change. Deferred to a post-stable cleanup pass.

**The balance pass.** Went in expecting to tune numbers. Found something more fundamental: weapons were weaker than bare hands. Every class's `base_damage` was higher than the damage value on the weapons available to them. Equipping anything made you worse. This was invisible as long as testing happened with the admin sword — the godly weapon masked the entire category of item values being wrong.

Fixed across the board. Scaled by quality tier with a consistent +8 gap between tiers:
- Common Warrior: 18/20 — Uncommon: 28 — Rare: 36
- Common Assassin: 10/12 — Uncommon: 18 — Rare: 26
- Common Mage: 13/15 — Uncommon: 22 — Rare: 30

All prices were also sitting at the v0.5 placeholder of 0. Set relative to the Wolf gold yield (~15 gold average): Health Potion 10 gold, Inn 20 gold, common weapons 60–70 gold, uncommon weapons 100 gold, common armor 40/60 gold (helmet/chest). The progression arc this creates: kill 4-5 Wolves → buy a weapon, kill 6-7 more → rest at the inn, kill 15-20 total → upgrade to uncommon before the dungeon. That feels like the right pacing for a single-dungeon early game.

**Enemy flee rate.** Normal enemies in yellow zone were fleeing at 100% when their HP dropped below 20%. The result: players couldn't reliably earn XP or gold because every fight that went well ended with the enemy running. Changed to a 25% flee chance at the HP threshold — enemies can still escape, but it's now a surprise rather than the guaranteed outcome. Gold drop rate also bumped from 65% to 80% to keep early economy flowing.

**Bugs found during playtest.**

Dungeon enemies (Skeleton, Zombie, Ghoul, etc.) had no `drop` field in `enemies.json`. `enemy_drop()` was doing `enemy["drop"]` instead of `enemy.get("drop")`, so every dungeon kill crashed with `KeyError`. One-character fix, but it would have blocked the entire dungeon.

Armor items weren't routing to the Equip menu. `item_action()` checked `item["type"] in ["weapon", "armor", "accessory"]` — but helmets have `type: "helmet"` and chest pieces have `type: "body_armor"` in `armors.json`. Neither matched, so both fell through to the `else` branch and tried to call `use_item()`, which crashed on `KeyError: 'effect'`. Added `"helmet"` and `"body_armor"` to the type check list. The real fix is standardizing the source data to `"armor"` across all armor entries — noted for a cleanup pass.

Cross-slot weapon swap is incomplete. Equipping a `main_hand` weapon while a `two_hand` is equipped doesn't return the old weapon to inventory. The `equip_item()` logic handles `two_hand → off_hand` cleanup but not `main_hand ↔ two_hand`. Players have to manually unequip first. Logged for a future fix patch.

NPC shop crashes on out-of-range input — entering a number higher than the stock list throws `IndexError`. Needs a `try/except` around `npc["stock"][int(choose) - 1]`. Logged.

### Testing outcome
Full playthrough with Warrior: yellow zone grind → bought common sword and armor → upgraded to uncommon sword → entered Hollow Depths with 11 health potions → cleared Skeleton/Zombie/Ghoul rooms → defeated Cursed Knight, chose gatekeeper weapon → defeated The Hollow Sovereign. Save and load verified with equipment intact across sessions.

### Decisions made
- v0.10 Zone Color System removed from roadmap — map color coding requires a visible map to be meaningful; both features will come together when the map is designed, likely v1.2 or later
- Balance pass scoped to playability, not precision — the goal was to remove hard blockers (flee denial, gold starvation, weapons weaker than fists); fine-tuning deferred until more content exists to test against
- game_loop refactor deferred — structural change, post-stable cleanup pass
- `armors.json` type standardization deferred — workaround in place, doesn't affect gameplay

---

## 03 August 2026

### v0.9.1 completed — post-v0.9 fix patch

A consolidated bug/UX patch bundling everything that was deferred out of v0.9 scope, plus a handful of issues that only surfaced during a fresh full playthrough test. No new version scope — every item here is a fix, a polish pass, or a design confirmation. Kept as a single patch (v0.9.1) rather than splitting into two.

Approach this time: instead of fixing bugs the moment they appeared, ran a full playthrough from a fresh character and logged every issue first, then triaged and fixed them together. This kept version scope clean and avoided the trap of fixing one thing while breaking another mid-session.

**Level up rework.** `max_hp`/`max_mp` gains were flat regardless of class, which made the three classes converge over time. Now scaled per class — Warrior +15 HP / +3 MP, Assassin +10 HP / +5 MP, Mage +8 HP / +8 MP — reinforcing class identity as the player levels. XP overflow was also broken: excess XP past the threshold displayed as inflated values like "175/140" instead of carrying forward. Now the excess is subtracted and applied to the next level cleanly. The full heal on level up was reviewed and kept — it's intentional design, a small reward for leveling, not a bug.

**Player flee, finally.** The in-combat flee action was originally scoped for v0.2 and never actually implemented — only the pre-combat Fight/Flee choice existed. Added it now: DEX-based success chance (DEX * 5%), returns to `previous_room` on success, takes an attack on failure. Correctly hidden in fixed_enemy rooms via the `is_fixed` parameter — gatekeeper and boss fights remain unfleeable, as their lore identities demand.

**The gatekeeper chest regression — the big one.** After defeating the Cursed Knight, the reward chest simply wasn't opening. The frustrating part: everything *looked* right. "Victory!" printed, XP was awarded, the drop message appeared. But no chest.

Traced it step by step with temporary debug prints. `start_combat()` was genuinely returning `"victory"` — confirmed by a debug line right before the return. But the chest-opening code in `main.py`'s `game_choice == "1"` block never ran. The `DEBUG RESULT` print there never fired. That was the tell: the code path I was staring at wasn't the one being executed.

The root cause was a regression from an earlier version. The gatekeeper fight had been moved into `encounter()` so it auto-triggers on room entry — but the chest-opening logic was left behind in the `main.py` manual-Combat block. Since the fixed_enemy flow no longer passes through that block at all, the chest code was dead on arrival. The fight resolved in `encounter()`, returned victory, and then... nothing, because the reward logic lived somewhere the flow never reached.

Fix: relocated the chest logic (`result == "victory"` check → `open_chest()` → `return`) into `encounter()`'s fixed_enemy block, right where the fight actually resolves. Added a `return` so the function stops there instead of falling through into a second encounter roll. The dead `main.py` block is left in place for now — it's harmless, and "if it works, don't touch it" applies until the post-stable cleanup pass sweeps the whole codebase.

The lesson logged for future refactors: when combat gets relocated between modules, its reward/chest logic has to move *with* it. This is exactly the kind of thing that breaks silently.

**The double-source weapon.** While fixing the chest, noticed the Cursed Knight's weapon was arriving twice — once as a class-based `enemy_drop()`, and again from the gatekeeper chest selection. The chest choice was always the intended source (a conscious pick between three weapons), so the `drop` field was removed from `ELITE_ENEMY_001` in `enemies.json`. Weapon now comes from the chest only. Gold still drops normally since the gatekeeper's gold fields are untouched.

**Smaller fixes in the same pass.**
- Chest could be opened after death in some flows — `start_combat()` now returns `"defeat"`/`"victory"` and the chest flow only runs on victory.
- Player HP could display negative values — clamped with `max(0, player["hp"])`.
- Duplicate "A chest appears!" message — `open_chest()` already prints its own opening line, so the redundant `print()` was removed.
- "Press Enter to enter the dungeon..." was firing on every red zone encounter inside the dungeon, not just at the entrance — reworded to a neutral "Press Enter to continue..." and scoped to the actual entrance.
- Dropping an item bounced the player back to the Game Menu instead of the inventory list — now loops back to inventory for consecutive drops.
- Boss/elite dialogue was plain text — now styled bold red via Rich markup, so it actually reads as a menacing line rather than a system message.
- `clear_terminal()` added to several transitions that were missing it — More menu back, inventory exit, equipment menu, NPC selection, item equip/back.
- Unequip fixed.
- Room info now displays on entering Ember's Cross and after dungeon encounters.
- Cleared fixed_enemy room now shows "You have already defeated the guardian of this place." when Combat is selected, and `encounter()` re-checks `cleared_rooms` so a cleared room can't re-trigger a fight.

### Testing outcome
Full playthrough verified end to end: fought through Hollow Depths, cleared the gatekeeper, confirmed the chest opens and the weapon choice works without duplicating, then defeated The Hollow Sovereign — both fixed_enemy encounters resolve cleanly through `encounter()` with chests opening correctly. `display_room()` double-call confirmed gone; no room double-renders.

### Decisions made
- Two deferred patches (originally planned as v0.9.1 + v0.9.2) merged into a single v0.9.1 — both were post-v0.9 bug/UX work with no new scope, no reason to split.
- Full heal on level up kept as intentional design.
- Room 5 (crossroads) showing no Fight/Flee prompt is by design — red zone means direct combat, not a bug.
- ROOM_007 dungeon entry was never actually broken — it's reached via `south`, and the entry direction is already listed. The old "dungeon_entrance not shown in Paths" note was a non-issue.
- All balance questions pushed to v1.0 — the gatekeeper/elite gold drop (currently 65% chance) and the general item drop rate (33%) aren't bugs, they're tuning decisions. Whether elite gold should be guaranteed and whether these rates feel right belong in the v1.0 playtest/balance pass alongside the full economy tuning, not in a fix patch.
- The dead `main.py` fixed_enemy block stays until a post-stable cleanup — "if it works, don't touch it." The whole codebase gets a parts-cleanup pass once the game reaches a stable release.

### Looking ahead — noted for v1.0
- **Save/Load system.** Flagged as essential for v1.0. Without it, every session starts from scratch, which pushes players away instead of pulling them in. The architecture is already well-positioned: the entire game state lives in a single `player` dict of pure JSON-compatible types, so save is "dump the dict" and load is "read it back". The Load Game menu option already exists as a `pass` placeholder — only the internals need filling. Detailed design (per-character save files, manual save gated to green zones so the black-zone risk stays meaningful, `save_version` for forward compatibility) to be decided during v1.0.

---

## 30 July 2026

### v0.9 completed

Design phase covered seven roadmap items before any code was written: boss room architecture, phase-based mechanic, boss defense action, chest rewards, cleansed behavior, flee rules, and boss identity. All locked before implementation started.

- `bosses.json` created as a separate file — boss entries carry fields (`phase_based`, `phase1_defense_chance`, `phase2`) that don't belong in `enemies.json` alongside standard enemy data. Same reasoning as the per-dungeon JSON decision in v0.8: each concern gets its own file.
- The Hollow Sovereign defined as the first boss (`BOSS_001`) — name chosen to echo the dungeon's own name (Hollow Depths), creating an implicit connection without needing explicit lore text. Dialogue tone: cold, dismissive, not confrontational — a being that doesn't consider the player a real threat.
- Phase system implemented via a `phase` local variable in `start_combat()` — Phase 2 triggers once at the 50% HP threshold, updates `base_damage` and `elemental_damage` in place, transition message shown exactly once. `phase_based` flag gates the whole system so normal enemies and the gatekeeper are completely unaffected.
- Boss defense mechanic: Phase 1 is more cautious (30% block chance), Phase 2 is more aggressive (10% block, higher damage). Rationale: a powerful entity getting reckless when wounded fits the character better than getting more defensive. The "rage" archetype also makes Phase 2 feel genuinely dangerous rather than just numerically harder.
- Gatekeeper reward redesigned — Cursed Knight now drops a class-specific weapon (Rare quality) via a new dict-based `drop` field. `enemy_drop()` updated to detect dict vs string format and route accordingly. Three options presented as a conscious choice from a chest, so the player picks intentionally rather than receiving a random drop.
- Boss chest uses a new `type` field (`"normal"`, `"gatekeeper"`, `"boss"`) in `hollow_depths.json` — `open_chest()` reads this field and branches into three different behaviors. Boss chest delivers Core of the Hollow Sovereign + 2000 gold with no selection screen; gatekeeper chest presents a weapon choice list.
- Core of the Hollow Sovereign (`CORE_001`) introduced — first enchantment crystal in the game. Passive for now, will be attachable to weapons via the blacksmith system in v1.1, granting stat bonuses and shadow element. Named with `CORE_` prefix to anticipate `CORE_002`, `CORE_003` from future bosses.
- DROOM_010 fully populated — "The Sovereign's Chamber", zone_type black, fixed_enemy BOSS_001, chest configured.
- DROOM_008 (The Last Respite) encounter_chance corrected to 0 — discovered during testing that the original value of 30 directly contradicted the room's purpose as a safe preparation space before the unfleeable gatekeeper fight.
- Enemy drop order corrected in victory block — `enemy_drop()` now runs before `level_up()`, so drop and gold messages appear before the stat distribution screen instead of after.
- `is_fixed` parameter added to `start_combat()` — previously every enemy kill appended the current room to `cleared_rooms`, including Wolf and Goblin rooms. Now only fixed_enemy encounters (gatekeeper, boss) update the cleared list.

### Testing phase — bugs found and fixed same session

- `cleared_rooms` field had a typo in `character.py` — written as `cleared_room` (missing "s"), causing KeyError on every movement lock check. Single character fix, caught immediately on first travel attempt.
- Boss `phase_based` field had a typo in `bosses.json` — written as `phased_based` (extra "d"), so `enemy.get("phase_based")` always returned None and Phase 2 never triggered. HP dropped to 101 with no transition. Found by checking the JSON directly after ruling out max_hp calculation issues.
- `enemy_drop()` crashed on boss entries with `drop: null` — function assumed drop field always contained a usable value. Added a None check at the top that handles gold drop and returns early.
- `open_chest()` was never called after fixed_enemy combat — `encounter()` ran `start_combat()` and immediately returned without checking for a chest. One line added after `start_combat()` call.
- Boss chest item loading had a typo — `item = items=item_key` instead of `item = items[item_key]`. Caught when opening the chest for the first time.

### Decisions made
- Gatekeeper drops a weapon, boss drops a core — two separate reward layers with different purposes. The weapon is functional (prepares the player for the boss fight and carries them into early v1.2 content). The core is a long-term investment (passive now, powers the enchant system in v1.1).
- Boss chest contains no weapon — deliberate. The player should feel strong after the boss but not invincible. 2000 gold provides economic comfort for the next region without a direct power spike. Weapon upgrades come from new regions in v1.2.
- Cleansed behavior kept minimal — boss room joins `cleared_rooms`, dungeon remains active as a grind space. Elder Path is not a Souls-like; the dungeon serving as a post-boss farming area is a feature, not a failure.
- Phase 2 does not add new attack types — keeping combat mechanics consistent with what the player already knows. The difficulty spike comes from stat changes and reduced defense, not from learning an entirely new pattern. New attack types deferred to future bosses with more design space.

### Known issues — deferred to v0.9.1 patch
- Level up: max_hp/max_mp gains are flat rather than proportional to stats; XP overflow not handled, shows values like "175/140"
- Several menu transitions missing clear_terminal() — More menu, inventory exit, equipment menu, NPC selection
- "Press Enter to enter the dungeon..." message fires on every red zone encounter, not just actual dungeon entry
- display_room() Paths list still doesn't show dungeon_entrance directions
- Dropping an item returns to Game Menu instead of back to inventory
- Boss/elite dialogue shown in plain text — should be bold red via Rich markup
- Player flee-during-combat action still not implemented
- UI table widths don't adjust to terminal size

---

## 10 July 2026

### v0.8 completed

Design phase started with six core decisions locked before any code was written: dungeon file architecture, enemy pool distribution, elemental damage foundation, flee rules, dialogue approach, and respawn system. Implementation followed the same order.

- New enemies added to `enemies.json`: Bandit, Giant Spider, Wild Boar (forest pool); Skeleton, Zombie, Ghoul, Shadow Creature (dungeon pool); Cursed Knight (elite gatekeeper, `can_flee: false`, `element: "shadow"`, `elemental_damage` field).
- `dialogue` field added to every enemy entry — null for normal enemies (mindless creatures, no lore reasoning needed), populated for Cursed Knight. Boss dialogue content deferred until v0.9.
- New loot items added to `items.json` for each new enemy drop, priced and qualitied roughly by enemy strength (common forest drops up to epic for Cursed Knight's Emblem).
- Dungeon architecture: after discovering a single shared `dungeon.json` wouldn't scale once multiple dungeons exist (v1.2), switched to one JSON file per dungeon under `data/dungeons/`, with `dungeons_index.json` as a small registry mapping dungeon id to file to entry rooms. `ROOM_007` converted from a dungeon-content room into a proper forest entrance room carrying a `dungeon_entrance` field.
- Dungeon room layout for Hollow Depths hand-drawn by user as a diagram rather than designed purely in JSON — caught a real problem early: three converging paths can't map cleanly onto four cardinal directions. Redesigned around a single crossroads (Room 5) with symmetric side rooms, avoiding the "three doors, one direction" conflict entirely.
- Added a buffer room ("The Last Respite") between the crossroads and the gatekeeper hall — lower-risk room where player can retreat and prepare before the unfleeable elite fight, softening the "no going back" rule without undermining it.
- `world.py`: `get_dungeon_data()` (lazy-load + cache per dungeon file), `get_location()` (single lookup point routing by ID prefix, `ROOM_` vs `DROOM_`), `get_room_data()` (resolves a target room before movement completes, used for pre-move checks).
- `move()` rewritten to route through `get_location()`, handle dungeon entry/exit via `dungeon_entrance`, show a confirmation prompt before entering any `fixed_enemy` room ("no turning back"), and block movement out of an active gatekeeper/boss room until it's in `cleared_rooms`.
- `encounter()` updated to check `fixed_enemy` before rolling `encounter_chance` — direct combat trigger for gatekeeper/boss rooms.
- `cleared_rooms`, `last_safe_room`, `current_dungeon` added to player dict. `last_safe_room` updates automatically on every green zone entry.
- Elemental damage: physical component vs `defense`, elemental component vs `magic_resistance`, calculated separately and summed, with a damage floor so `magic_resistance` can never fully negate elemental damage. Kept deliberately simple (no diminishing-returns curve) — enchant system in v1.1 will raise `magic_resistance` values without requiring the formula itself to change.

### Testing phase — bugs found and fixed same day

Comprehensive testing was deferred until all v0.8 components were written, then run in one long pass. Several bugs were pre-existing but only surfaced because v0.8 content finally exercised code paths nobody had touched before (loot items being "used", two-handed weapons being equipped, high burst damage against low-HP enemies).

- Gatekeeper confirmation prompt worked immediately, but combat never actually started after confirming — `encounter()` had no concept of `fixed_enemy` at all. Added the missing check.
- Combat menu's "1 - Combat" option turned out to always fight a hardcoded Wolf loaded once at game start, completely bypassing room-based enemy selection. Even inside the gatekeeper's own room, "Combat" fought a Wolf. Rewired to read the current room dynamically via `get_location()`.
- Found via the test-only "Godly Sword" item (999,999 gold, absurd damage, added specifically to stress-test combat quickly): one-shotting an enemy triggered the flee message instead of victory. Root cause — flee threshold check and the enemy's counter-attack block weren't gated on the enemy still being alive, so a dead enemy could still "flee" and still hit back. Wrapped both in `if enemy["hp"] > 0`.
- Respawn was effectively non-functional — dying in a red zone deducted gold but never restored HP (could go negative) and never moved the player anywhere. `death_penalty()` now resets HP/MP in all zones and teleports to `last_safe_room`, clearing `current_dungeon`.
- Equipment: re-equipping an already-equipped slot crashed with `KeyError: None` — traced to a loop variable named `slot` shadowing the outer `slot` variable holding the actual equipment key. Renamed the loop variable.
- Two-handed weapons crashed on equip (`KeyError: 'two_hand'`) — the slot was never added to the player's starting equipment dict. Added it, then found the equipment screen didn't display a Two-hand row at all, silently hiding whether the equip had worked. Added the row, with Main hand / Off hand shown as locked when a two-hander is equipped.
- Loot items crashed when "used" (`KeyError: 'effect'`) — `item_action()` had only ever considered weapon/armor/accessory vs. "everything else is a potion". Added a dedicated loot branch (Drop/Back only). First pass forgot to route the Drop choice to `drop_item()`, then forgot to `break` out of the menu after dropping — both fixed.

End-to-end verification: fought through the full Hollow Depths crossroads, confirmed enemy pools per room, triggered the gatekeeper warning, declined once, re-entered, fought and defeated Cursed Knight, confirmed XP/gold/loot awarded correctly and the room lock releasing after the kill.

### Decisions made
- Per-dungeon JSON files over a shared `dungeon.json` — avoids ID collisions and monolithic file growth as more dungeons are added in v1.2.
- Respawn point is the last visited green zone rather than a hardcoded village — currently behaves identically to "always Ember's Cross" since only one green zone exists, but requires no rework once new towns are added.
- Gatekeeper/boss rooms block player flee entirely once entered, reinforced by a pre-entry confirmation — deliberate tension choice. Balanced against red zone deaths only costing gold (no item loss, that's black zone only), keeping the "no turning back" rule meaningful without making failure punishing enough to sour the loop.
- Elemental typing tied to enemy theme/name rather than a fixed Fire/Frost/Lightning set shared with Mage spells — Cursed Knight's "shadow" element fits a cursed gatekeeper better than forcing it into the existing spell trio.
- No element-vs-element weakness matrix yet — only one elemental enemy exists, building a matrix now would be guessing without data. Revisit once v0.9/v1.2 add more elemental variety.

### Known issues — fixed in v0.7.1
- Inventory not visible from equipment screen — equip cannot be performed from equipment menu
- Terminal not fully cleared after some NPC interactions
- Player info missing from game menu screen
- Inn menu does not exit automatically after resting — player must manually select Leave

---

## 08 July 2026

### v0.7.1 completed

- `display_equipment_menu()` added to `ui.py` — shows Equip / Unequip / Back options after equipment screen.
- `item_action()` restructured in `items.py` — weapon/armor/accessory shows Equip/Drop/Back; potion shows Use/Drop/Back. Previously all item types showed the same menu.
- `use_item()` updated — now checks item type before applying effect; weapons, armor, accessories return "This item cannot be used." instead of crashing.
- `weapons.json` item `type` field standardized to `"weapon"` — previously stored subtype (e.g. `"sword"`).
- `show_status(player)` added to game menu loop in `main.py` — player info now visible at all times in game menu.
- Version panel added to `display_main_menu()` in `ui.py` — italic, small panel bottom left showing current version.
- `clear_terminal()` integrated into NPC shop and rest flows — purchase, rest, and leave transitions now render clean screen with Enter prompt.
- Inn `rest()` function now breaks after successful rest — menu no longer loops after HP/MP restored.
- Game menu invalid input now handled — shows error message and clears terminal instead of re-rendering menu silently.
- `select_item()` input prompt updated to show `(0 to exit)` — player now knows how to exit inventory.
- `clear_terminal()` added to `select_item()` slot 0 exit — terminal clears on inventory close.

### Decisions made
- `display_equipment_menu()` created as separate function — equipment screen stays display-only, menu logic separated.
- Item type standardized to category (`"weapon"`, `"armor"`) not subtype (`"sword"`, `"bow"`) — subtype can be added as `subtype` field if needed in future versions.
- Version number displayed on main menu only — not in game menu, consistent with most games.
- `quality_colors` dict keys in `ui.py` standardized to lowercase — consistent with quality values in JSON files.

---

## 02 July 2026

### v0.7 completed

- `data/npcs.json` created — 4 NPCs: Aldric (weapon_seller), Maren (armor_seller), Syra (potion_seller), Dorin (inn). Fields: name, job, location, stock/price, dialogue.
- `game/npc.py` created — NPC interaction module.
- `talk_to_npc(player, npc)` — routes to `shop()` or `rest()` based on npc job field.
- `shop(player, npc)` — loads correct JSON file based on job, displays full stock list with name/quality/price, takes player selection, checks gold, deducts price, adds item to first empty inventory slot.
- `rest(player, npc)` — checks if player is already at full HP/MP, checks gold, deducts price, restores HP and MP to max.
- `display_more_menu(player, rooms)` added to `ui.py` — More menu with zone-aware options; NPC's visible only in green zones, Quit Game and Back always visible.
- `display_npc_list(npcs, rooms, player)` added to `ui.py` — filters NPCs by current location, displays numbered list with Back option, returns choice and NPC list.
- `display_game_menu()` updated — Quit Game removed, More added as 4th option.
- `npcs.json` loaded in `main.py` alongside enemies and rooms.
- More menu logic added to `main.py` — zone-aware routing, NPC selection, talk_to_npc call.
- `price` field added to `weapons.json` and `armors.json` — placeholder value 0.

### Decisions made
- NPC data in separate `npcs.json` — consistent with data/logic separation pattern.
- `stock` field stores item ID list — item details stay in their respective JSON files, no duplication.
- `dialogue` field per NPC in JSON — dialogue strings stay in data layer, not hardcoded in logic.
- More menu is zone-aware — options appear/disappear based on current zone_type, not hardcoded per location.
- NPC list filtered by `location` field — only NPCs in current room are shown.
- `purchased` flag used to break out of shop while loop after successful purchase — avoids nested break complexity.
- Lore NPC (Guide) deferred to Faz 2 — lore presentation requires visuals to be effective.
- Price balancing deferred to v1.0 playtest — all prices placeholder 0.

### Known issues — fixed in v0.7.1
- Inventory not visible from equipment screen — equip cannot be performed from equipment menu
- Terminal not fully cleared after some NPC interactions
- Player info missing from game menu screen
- Inn menu does not exit automatically after resting — player must manually select Leave

---

## 29 June 2026

### v0.6.1 completed

- `clear_terminal()` added to `ui.py` — cross-platform terminal clear using `os.system("cls")` on Windows, `"clear"` on Linux/Mac.
- `clear_terminal()` integrated into all major screen transitions: combat loop start, post-combat (victory and flee), player death, chest open and leave, room transitions, green zone combat attempt, character creation flow.
- Welcome screen added after character creation — shows player name and class, Enter to continue.
- Dungeon entry now shows room information before combat begins — Enter prompt added.
- Revive message added on player death — "A true warrior never gives up. Rise and continue your story..."
- Direction connections in `rooms.json` corrected — ROOM_002 (south), ROOM_003 (north), ROOM_004 (west), ROOM_005 (east) return connections were wrong.
- `zone_type` now correctly passed to `start_combat()` from `main.py`.
- Green zone combat attempt handled — shows "There are no enemies here." instead of crashing.
- `rooms.json` loaded in `main.py` for zone_type access.

### Decisions made
- Terminal clear placed before each new screen render, after player input — ensures current data always visible before clear.
- "Press Enter to continue..." flow added to all transitions — player controls pacing, no information lost.
- Alacritty separate terminal profile for Elder Path added to TODO — terminal color palette overrides Rich colors.
- Game menu version display and Feedback option added to TODO — deferred to v1.0 polish.
- Invalid game menu input (non-listed keys) showing game menu again added to TODO — deferred.

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
- `display_level_up(player)` — displays level up notification panel when player levels up. Shows new level and +3 stat points message.
- `display_combat_menu(player)` — displays styled combat action menu (Attack, Defence, Dodge, Use Item) in a Panel.
- `display_attack_menu(player)` — single function handles all three class attack submenus. Shows correct options based on player class.
- `display_main_menu()` — styled main menu panel centered on screen. Title: ELDER PATH, slogan: "Every beginning has its end."
- `display_play_menu()` — styled New Game / Load Game panel. Title: "Welcome to the Beginning."
- `display_class_menu()` — styled class selection panel with short description per class.
- `damage_colors` dict added globally in ui.py — maps damage types to colors (physical, fire, frost, lightning, critical, poison, shadow).
- `attack_to_damage` dict added in combat.py — maps attack_type strings to damage type keys.
- Hasar mesajlari renklendirildi — her saldiri tipine gore ilgili renk uygulandi.
- Enemy HP bar implemented manually using block characters. Color changes dynamically: green above 50%, yellow above 25%, red below 25%.
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