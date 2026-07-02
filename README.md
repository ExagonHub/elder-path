# Elder Path

A terminal-based RPG set in a dark and unforgiving world. Choose your path, fight your enemies, and survive.

## Features

- Multiple character classes, each with unique playstyles
- Turn-based combat with class-specific mechanics
- Exploration, loot, and equipment systems
- A world full of secrets — tread carefully

> ⚠️ Active development. Currently in early stages.

## Requirements

- Python 3.14.4 or higher

## Installation

```bash
git clone https://github.com/ExagonHub/elder-path.git
cd elder-path
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Project Structure

```
elder-path/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── README.md            # This file
├── ROADMAP.md           # Development roadmap
├── CHANGELOG.md         # Version history
├── DEVLOG.md            # Development diary
├── .gitignore
├── data/
│   ├── classes.json     # Class definitions and starting stats
│   ├── enemies.json     # Enemy pool and stats
│   ├── items.json       # Item pool (potions, loot)
│   ├── weapons.json     # Weapon pool and stats
│   ├── armors.json      # Armor pool and stats
│   ├── accessories.json # Accessory pool and stats
│   └── rooms.json       # Room definitions, connections, zone types
└── game/
    ├── __init__.py
    ├── character.py     # Character creation and level up
    ├── combat.py        # Combat loop and class-specific mechanics
    ├── items.py         # Inventory management, item drop, gold
    ├── equipment.py     # Equipment system, stat merging
    ├── world.py         # World navigation, encounters, death penalty
    └── ui.py            # Rich terminal UI — all visual output
```

## Development Status

| Version | Focus | Status |
|---------|-------|--------|
| v0.1 | Core loop | ✅ Complete |
| v0.2 | Combat system | ✅ Complete |
| v0.3 | Items and inventory | ✅ Complete |
| v0.4 | Rich Terminal UI | ✅ Complete |
| v0.5 | Equipment system | ✅ Complete |
| v0.6 | World and exploration | ✅ Complete |
| v0.7 | NPCs and economy | ✅ Complete |
| v0.8 | Enemy variety | ⏳ Pending |
| v0.9 | Boss system | ⏳ Pending |
| v0.10 | Zone color system | ⏳ Pending |
| v1.0 | Playtest, balance, polish | ⏳ Pending |
| v1.1 | Upgrades and bank | ⏳ Pending |
| v1.2 | World expansion | ⏳ Pending |

---

*Elder Path is a solo development project.*