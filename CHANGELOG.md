# Changelog
All notable changes to Elder Path will be documented here.

---

## [v0.8] — 2026-07-10
### Added
- New enemies added to `enemies.json`: Bandit, Giant Spider, Wild Boar (forest); Skeleton, Zombie, Ghoul, Shadow Creature (dungeon); Cursed Knight (elite/gatekeeper)
- `dialogue` field added to all enemy entries — normal enemies null, elite/boss carry lore dialogue
- `can_flee`, `element`, `elemental_damage` fields added to Cursed Knight entry
- New loot items added to `items.json`: Boar Tusk, Spider Silk, Bandit's Coin Pouch, Bone Fragment, Rotten Flesh, Ghoul Claw, Shadow Essence, Cursed Knight's Emblem (`LOOT_ELITE_001`)
- `data/dungeons/hollow_depths.json` created — first full dungeon, 10 rooms (entrance, crossroads network, buffer room, gatekeeper hall, boss room placeholder)
- `data/dungeons_index.json` registry created — maps dungeon id to file path and entry points
- `dungeon_entrance` field added to `rooms.json` (`ROOM_007`) — links overworld to dungeon system
- `get_dungeon_data()` added to `world.py` — lazy-load + cache pattern for dungeon files
- `get_location()` added to `world.py` — single source of truth for reading current room data, routes between `rooms.json` and dungeon files based on ID prefix
- `get_room_data()` added to `world.py` — resolves arbitrary room data by id + dungeon context, used for pre-move checks
- `move()` updated — ID prefix routing (`ROOM_` vs `DROOM_`), dungeon entry/exit handling, confirmation prompt before entering `fixed_enemy` rooms, lock mechanic blocking progress past unguarded gatekeeper/boss rooms until cleared
- `encounter()` updated — `fixed_enemy` check triggers direct combat, bypassing normal encounter_chance roll
- `cleared_rooms`, `last_safe_room`, `current_dungeon` fields added to player dict
- `last_safe_room` auto-updates whenever player enters a green zone room
- Elemental damage system — physical damage vs `defense`, elemental damage vs `magic_resistance`, calculated as separate components with a minimum damage floor
- `can_flee` flag — elite/boss enemies never flee regardless of zone type
- Player movement blocked during active `fixed_enemy` combat — cannot leave gatekeeper/boss room until enemy is defeated

### Fixed
- Combat menu ("1 - Combat") now dynamically selects enemy based on current room's `enemy_pool`/`fixed_enemy` — previously always fought a hardcoded Wolf regardless of location
- Enemy flee check and enemy attack block now wrapped in `if enemy["hp"] > 0` — previously a lethal hit could be misread as "badly wounded, flees" due to check-order bug, denying XP/gold/loot
- `death_penalty()` now resets HP/MP in red zone deaths (previously only deducted gold, leaving HP at negative values) and teleports player to `last_safe_room`, resetting `current_dungeon` — respawn is now fully functional
- Equipment bug: `equip_item()` loop variable shadowed the outer `slot` variable, causing `KeyError: None` when re-equipping an already-equipped slot — loop variable renamed
- `item_action()` now shows correct menu (Drop/Back) for loot-type items instead of Use/Drop/Back — previously caused `KeyError: 'effect'` when attempting to use a loot item
- Drop action now properly exits the item menu after dropping (missing `break` added) — item no longer requires a second "Back" to register removal
- `two_hand` equipment slot added to player dict — previously caused `KeyError: 'two_hand'` when equipping two-handed weapons
- `display_equipment()` now shows a Two-hand row and locks Main hand / Off hand display when a two-handed weapon is equipped

### Decisions made
- Each dungeon stored in its own JSON file under `data/dungeons/`, rather than one shared `dungeon.json` — keeps future dungeons (v1.2) independently scalable, avoids a monolithic file as world content grows
- `dungeons_index.json` acts as a lightweight registry rather than embedding dungeon metadata elsewhere — single lookup point for file path and entry rooms
- Gatekeeper room requires explicit confirmation before entry and blocks flee once combat starts — reinforces "final trial before the boss" tension without adding a full player-flee system prematurely
- Respawn point is the last visited green zone (`last_safe_room`), not a hardcoded village — scales naturally when new towns arrive in v1.2; simpler alternatives (checkpoint lists, hearthstone selection) deferred until multiple green zones exist
- Elemental damage formula kept as a simple subtraction with a damage floor, not a diminishing-returns curve — avoids over-engineering before real itemization data (magic_resistance spread across armors) exists; v1.1 enchant system will build on top of this formula without needing to change it
- Dungeon room network built from a manually diagrammed layout rather than procedural generation — three exploration paths converge at a single crossroads (Room 5) before a buffer room, avoiding an unsolvable "three doors into one room" direction conflict
- Buffer room ("The Last Respite") added between the crossroads and the gatekeeper hall — gives players a lower-risk room to assess readiness before an unfleeable elite encounter

### Known issues (deferred to v0.8.1 patch)
- Level up: `max_hp`/`max_mp` increase by a flat amount instead of scaling proportionally with stats; XP overflow past `xp_to_next_level` is not properly reset/carried
- `display_room()` Paths list doesn't include `dungeon_entrance` connections — valid dungeon entry direction isn't shown to the player
- "Press Enter to enter the dungeon..." message appears on every red zone encounter, not just the actual dungeon entrance
- More menu "Back" doesn't clear the terminal
- Dropping an item returns player to Game Menu instead of the inventory list
- General player flee action during combat is still missing (only the pre-combat Fight/Flee choice exists)
- UI table widths don't dynamically adjust to terminal size

## [v0.7.1] — 2026-07-08
### Fixed
- Equipment screen now shows inventory — equip can be performed from equipment menu
- Inn menu now exits automatically after resting — no manual Leave required
- `clear_terminal()` integrated into NPC interactions — shop purchase, rest, and leave transitions now render clean screen
- Game menu invalid input now shows error message instead of re-rendering menu
- Inventory exit now clears terminal — `clear_terminal()` added to slot 0 exit in `select_item()`

### Added
- `display_equipment_menu()` added to `ui.py` — Equip / Unequip / Back options after equipment screen
- `item_action()` restructured — weapon/armor/accessory shows Equip/Drop/Back; potion shows Use/Drop/Back
- `show_status(player)` added to game menu loop — player info visible at all times in game menu
- Version panel added to main menu — displays current version (bottom left, italic)
- `use_item()` now checks item type — weapons, armor, accessories cannot be used, only equipped
- `weapons.json` item `type` field standardized to `"weapon"` — previously stored subtype (e.g. `"sword"`)
- Inventory exit hint added — input prompt now shows `(0 to exit)`

### Decisions made
- `display_equipment_menu()` created as separate function — separation of concerns, equipment screen stays display-only
- Item type standardized to category (`"weapon"`, `"armor"`) not subtype (`"sword"`, `"bow"`) — subtype can be added as `subtype` field if needed in future versions
- Version number displayed on main menu only — not in game menu, consistent with most games

## [v0.7] — 2026-07-02
### Added
- `data/npcs.json` created — 4 NPCs defined: Aldric (weapon_seller), Maren (armor_seller), Syra (potion_seller), Dorin (inn). Fields: name, job, location, stock/price, dialogue
- `game/npc.py` created — NPC interaction module
- `talk_to_npc(player, npc)` — routes to correct function based on npc job
- `shop(player, npc)` — displays stock with name, quality, price; handles purchase flow, gold deduction, inventory placement
- `rest(player, npc)` — restores HP/MP for gold; checks full HP/MP and insufficient gold
- `display_more_menu(player, rooms)` added to `ui.py` — dynamic More menu; NPC's option visible only in green zones
- `display_npc_list(npcs, rooms, player)` added to `ui.py` — lists NPCs present in current location
- `display_game_menu()` updated — Quit Game moved to More menu, replaced with More option
- `npcs.json` loaded in `main.py` — NPC data available throughout game loop
- `price` field added to `weapons.json` and `armors.json` — placeholder value 0

### Decisions made
- NPC data in separate `npcs.json` — consistent with data/logic separation pattern
- `stock` field stores item ID list — item details stay in their respective JSON files
- `dialogue` field added to each NPC — avoids hardcoding strings in logic
- More menu is zone-aware — options appear/disappear based on current zone_type
- NPC list filters by `location` field — only shows NPCs in current room
- Lore NPC (Guide) deferred to Faz 2 — lore presentation requires visuals
- Price balancing deferred to v1.0 playtest

## [v0.6.1] — 2026-06-29
### Fixed
- `clear_terminal()` added to `ui.py` — clears terminal before each new screen render
- Terminal no longer grows downward during gameplay; each action renders a clean screen
- `clear_terminal()` integrated into: combat loop, post-combat, enemy flee, player death, chest interactions, room transitions, green zone combat attempt
- Direction connections in `rooms.json` corrected — ROOM_002, 003, 004, 005 had wrong return directions
- `zone_type` now passed correctly to `start_combat()` from `main.py`
- Green zone combat attempt now shows "There are no enemies here." instead of crashing
- Dungeon entry now shows room info before combat begins

### Added
- Welcome screen after character creation — name, class, Enter to continue
- "Press Enter to continue..." flow added to all major transitions
- Revive message on player death — "A true warrior never gives up..."
- Dungeon entry prompt — "Press Enter to enter the dungeon..."

## [v0.6] — 2026-06-25
### Added
- `data/rooms.json` created — 7 rooms (1 village, 5 forest, 1 dungeon), zone types, connections, encounter chances
- `game/world.py` created — world and exploration module
- `move(player)` — room-based navigation via N/S/E/W direction input, updates current_room and previous_room
- `encounter(player)` — random encounter system based on encounter_chance; yellow zone offers Fight/Flee choice, red zone forces combat
- `death_penalty(player)` — zone-based death penalty; yellow revives at 40% HP / 30% MP, red zone deducts 30% gold
- `open_chest(player, location)` — chest interaction after combat; shows loot pool, player selects item, added to inventory, chest marked as opened
- `display_room(location)` added to `ui.py` — shows room name, zone type, and available paths
- `display_game_menu()` updated — Travel option added, Exit renamed to Quit Game
- `player["current_room"]` and `player["previous_room"]` added to player dict
- `zone_type` parameter added to `start_combat()` — prevents enemy flee in red zone

### Decisions made
- rooms.json chosen over in-code room definitions — consistent with existing data/logic separation
- N/S/E/W direction input — immersive, connections stored as full direction names in JSON
- Flee in yellow zone returns player to previous_room
- Chest only in dungeon (red zone) — risk/reward balance
- Enemy pool stored as list in rooms.json — weighted pool deferred to v0.8
- `previous_room` tracked in player dict — enables flee mechanic without extra parameters
- Red zone death penalty defers village respawn to a later version

## [v0.5] — 2026-06-11
### Added
- `data/weapons.json` created — 9 weapon entries (Warrior, Assassin, Mage), Common and Uncommon quality
- `data/armors.json` created — 6 armor entries (helmet + chest per class), Common quality
- `data/accessories.json` created — initial accessory pool (Traveler's Amulet), percentage-based XP bonus
- `game/equipment.py` created — equipment system module
- `get_total_stats(player)` — merges base stats with equipped gear, returns combined dict
- `equip_item(player, index, item)` — equips item from inventory to correct slot, class restriction check, two-hand locking, auto-swap if slot occupied
- `unequip_item(player, slot)` — unequips item to inventory, blocks if inventory full
- `display_equipment(player)` added to `ui.py` — three-panel equipment screen (Armor / Character / Weapons)
- `display_game_menu()` added to `ui.py` — in-game menu (Combat, Equipment, Exit)
- Game loop added to `main.py` — player navigates game menu before entering combat
- Equip option added to `item_action()` in `items.py` — weapon, armor, accessory items can be equipped from inventory
- `defense` and `magic_resistance` added to player dict (base value 0)
- `equipment` dict added to player dict — all slots default to None
- Damage calculation updated — base_damage now reads from `get_total_stats()`
- Enemy damage now reduced by player defense — `max(0, enemy_damage - defense)`

### Decisions made
- `magic_resistance` passive for now — activates alongside magic enemies in v0.8
- Attack speed stat deferred to Faz 2 — meaningless in turn-based combat
- Accessory bonuses are percentage-based — flat values lose meaning as game progresses
- Bonus count scales with quality: Common 1, Uncommon 1-2, Rare 2, Epic 2-3, Legendary 3
- One accessory slot for now — expandable to 2 in future versions
- Equip from inventory (Option A) — cleaner separation of concerns
- `get_total_stats()` returns separate dict — base stats never modified, no corruption risk
- Prices set to 0 placeholder — will be balanced post-v1.0 playtest

## [v0.4] — 2026-06-01
### Added
- `game/ui.py` created — centralized UI module using Rich library
- `show_status(player, enemy=None)` — Player and Status panels side by side, optional Enemy panel with dynamic HP bar
- `display_inventory(player)` — 18-slot inventory as Rich Table, quality color-coded
- `display_level_up(player)` — level up notification panel
- `display_combat_menu(player)` — styled combat action panel
- `display_attack_menu(player)` — single function handles all class attack submenus
- `display_main_menu()` — centered main menu panel with title and slogan
- `display_play_menu()` — styled New Game / Load Game panel
- `display_class_menu()` — class selection panel with per-class descriptions
- Enemy HP bar — dynamic █░ bar, color changes by HP ratio (green/yellow/red)
- Damage color system — `damage_colors` dict maps damage types to colors
- `attack_to_damage` dict in combat.py — maps attack types to damage type keys
- Hasar mesajları renklendirildi — physical, fire, frost, lightning damage types
- `max_mp` added to player dict, scales on level up

### Changed
- `show_status` extended with optional `enemy` parameter
- `select_item()` — input 0 exits inventory cleanly
- `item_action()` — handles None return from select_item

## [v0.3] — 2026-05-29
### Added
- 18-slot inventory system (6 consumable, 12 loot) added to player
- Item drop system — enemies drop items at 33% chance based on enemy drop table
- Gold drop system — enemies drop gold at 65% chance within a min/max range
- Potion: usable in combat via "Use Item" action, restores HP up to max
- Item quality framework — quality field displayed on item drop
- `items.py` created: `show_inventory`, `select_item`, `use_item`, `drop_item`, `item_action`, `enemy_drop` functions
- `data/items.json` created with initial item pool (Health Potion, Wolf Fang)

## [v0.2] — 2026-05-29
### Added
- Warrior: Stance system (Normal Attack, Defensive Stance, Counter Attack)
- Assassin: Attack type selection (Normal, Rapid, Piercing)
- Mage: Spell selection (Fireball, Frost, Lightning) with stun mechanic
- Defend action — reduces incoming damage by 50% for that turn
- Dodge action — DEX-based chance (DEX * 5%) to avoid enemy attack
- Enemy flee mechanic — flees when HP drops below 20% of max HP
- Elite and boss flee mechanic deferred to v0.8

## [v0.1] — 2026-05-28
### Added
- Character creation: name + class selection (Warrior, Assassin, Mage)
- Starting stat distribution by class (HP, MP, STR, DEX, INT, VIT, base_damage)
- Single enemy, single room combat
- Attack action with damage formula: base_damage + STR/DEX/INT bonus (50%)
- XP gain on enemy death, level up system, 3-point stat distribution
- Game ends on player death

## [Unreleased]