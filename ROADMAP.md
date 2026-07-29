# Elder Path
## Phase 1 Development Roadmap

| Version | Content | Status |
|---------|---------|--------|
| v0.1 | Core - character, single combat loop | ✅ Complete |
| v0.2 | Combat system - class-specific actions | ✅ Complete |
| v0.3 | Items and inventory | ✅ Complete |
| v0.4 | Rich terminal UI | ✅ Complete |
| v0.5 | Equipment system | ✅ Complete |
| v0.6 | World and exploration | ✅ Complete |
| v0.7 | NPCs and economy | ✅ Complete |
| v0.8 | Enemy variety | ✅ Complete |
| v0.9 | Boss system | ✅ Complete |
| v0.10 | Zone color system | ⏳ Pending |
| v1.0 | Playtest, balance, polish - first release | ⏳ Pending |
| v1.1 | Upgrades and bank | ⏳ Pending |
| v1.2 | World expansion | ⏳ Pending |

---

## v0.1 - Core
**Goal:** A working combat loop. No extra features.

1. Character creation: name + class selection (Warrior, Assassin, Mage)
2. Starting stat distribution by class (HP, STR, DEX, INT, VIT)
3. A single enemy, a single room
4. Only the 'attack' action - damage formula: weapon base + STR/INT bonus
5. Gain XP on enemy death, level up, distribute stats (3 points)
6. Game ends when the player dies

---

## v0.2 - Combat System
**Goal:** Combat loop becomes class-specific, full actions added.

1. Warrior: Stance system (Attack/Defense/Counter) as attack submenu
2. Assassin: Attack type selection (Normal/Rapid/Piercing) as attack submenu
3. Mage: Spell selection + mana system as attack submenu
4. Defend action - reduces incoming damage for that turn
5. Dodge action - DEX-based, not always successful
6. Enemy flee mechanic - normal enemies can flee at low chance
7. Elite and boss: never flees (deferred to v0.9)

---

## v0.3 - Items and Inventory
**Goal:** Items the player can carry and a survival layer.

1. 18-slot inventory system (6 consumable, 12 loot)
2. Basic item drop system (Common and Uncommon)
3. Potion: usable in combat, restores HP
4. Gold system foundation - enemies drop gold
5. Item quality framework (Common/Uncommon/Rare/Epic/Legendary)

---

## v0.4 - Rich Terminal UI
**Goal:** The terminal experience becomes visually rich and readable.

1. Rich library integration
2. Combat screen - styled HP bars, enemy info panel
3. Inventory display - formatted item tables
4. Menus - styled selection prompts
5. Level up screen - stat changes highlighted
6. Color coding - damage types, item qualities, zone danger levels
7. General polish - consistent layout across all screens

---

## v0.5 - Equipment System
**Goal:** Player can equip gear, stats reflect equipment.

1. Weapon slot (main-hand) + off-hand slot
2. Armor slots: helmet, chest, gloves, boots
3. Accessory slot
4. Class-specific equipment restrictions (heavy armor, leather, cloth)
5. Equipment stats - base weapon damage comes from gear
6. Starting equipment by class
7. Quiver and arrow system foundation for Assassin

---

## v0.6 - World and Exploration
**Goal:** The player navigates a world, not just fights.

1. Room-based movement system
2. Random encounter system - enemies spawn by chance in normal rooms
3. Fixed spawn room foundation (groundwork for boss rooms)
4. Basic chest system - open chests inside rooms
5. Simple map: Ember's Cross and the first dungeon
6. Lore: room and zone names drawn from Valdris

---

## v0.7 - NPCs and Economy
**Goal:** Village system gives gold meaningful purpose.

1. Village: Ember's Cross fully realized
2. Weapon Seller - Common/Uncommon weapon stock
3. Armor Seller - Common/Uncommon armor stock
4. Potion Seller - basic potions
5. Inn - restore HP/mana for gold
6. Gold balance test - earn and spend balance
7. Lore: brief lore hints in NPC dialogue

---

## v0.8 - Enemy Variety
**Goal:** Every encounter feels different.

1. Multiple enemy types, each with a unique stat set
2. Zone-based enemy pools (forest enemies vs dungeon enemies)
3. Elite enemy - gatekeeper before boss, can deal elemental damage
4. Enemy lore names (Hollow Demon, Corrupted, etc.)
5. Elemental damage foundation

---

## v0.9 - Boss System
**Goal:** Exploration has purpose and reward.

1. Boss room - fixed spawn, always present
2. Boss-specific mechanic - every boss is different
3. Boss defense action (elites and bosses have intelligence)
4. Boss chest - Rare/Epic item drop
5. 'Cleansed' feeling after defeating a dungeon boss - no respawn
6. Elite and boss never flee mechanic
7. Lore: boss names drawn from Valdris lore

---

## v0.10 - Zone Color System
**Goal:** The world gains meaning through danger levels.

1. Green zone: Village/City - no death, fully safe
2. Yellow zone: Open area/Forest - passive enemies, revive with reduced HP/mana
3. Red zone: Dungeon - aggressive enemies, lose gold on death
4. Black zone: Boss room - lose all items on death
5. Map color coding
6. Bank NPC integration - deposit items before entering black zones

---

## v1.0 - Playtest, Balance, Polish
**Goal:** Phase 1 becomes stable, playable, and fully balanced. First release.

1. Integration testing of all systems
2. XP curve balance - is the leveling speed right?
3. Gold economy balance - is earn and spend in sync?
4. Real playtest of item drop rates
5. Boss mechanic balance - how hard is too hard?
6. Stat balance test - how strong is each class?
7. Remaining lore details added
8. Notes and ideas logged for Phase 2

---

## v1.1 - Upgrades and Bank
**Goal:** The item system reaches full depth.

1. Blacksmith NPC - repair and upgrade service
2. Upgrade system: +1 through +10
3. Common/Uncommon: +1-5 gold only, +6-10 gold + materials
4. Rare and above: always gold + materials
5. Material system foundation - materials from enemy drops and chests
6. Bank NPC - item storage, gold storage

---

## v1.2 - World Expansion
**Goal:** A sense of a wide world beyond a single zone.

1. Multiple regions - selected from the continents of Valdris
2. Progressive map unlock - defeating a boss opens a new region
3. New dungeon - different enemy pool, different boss
4. Valdenmoor, Aurentis, Sylvara, Durnfall region integration
5. Lore: new region names and NPC dialogue

---

*— Elder Path Roadmap — Phase 1 —*