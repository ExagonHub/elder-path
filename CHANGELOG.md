# Changelog

All notable changes to Elder Path will be documented here.

---

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