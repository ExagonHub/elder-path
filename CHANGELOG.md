# Changelog
All notable changes to Elder Path will be documented here.

---

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