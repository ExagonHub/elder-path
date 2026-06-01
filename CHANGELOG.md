# Changelog
All notable changes to Elder Path will be documented here.

---

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