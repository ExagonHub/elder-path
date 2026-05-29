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
│   └── enemies.json     # Enemy pool and stats
└── game/
    ├── __init__.py
    ├── character.py     # Character creation and level up
    └── combat.py        # Combat loop and class-specific mechanics
```

## Development Status

| Version | Focus | Status |
|---------|-------|--------|
| v0.1 | Core loop | ✅ Complete |
| v0.2 | Combat system | ✅ Complete |
| v0.3 | Items and inventory | ⏳ Pending |
| v0.4 | Equipment system | ⏳ Pending |
| v0.5+ | World, NPCs, bosses... | ⏳ Pending |
| v1.0 | Playtest, balance, polish | ⏳ Pending |

---

*Elder Path is a solo development project.*