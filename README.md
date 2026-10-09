# Trashy Apocalypse

A top-down zombie survival shooter built on Python's Arcade library by our AP Computer Science Principles team at the High School of Arts and Technology. It was our school's entry at the annual arts event.

You move through a trashed wasteland, aim with the mouse, and spray down waves of zombies with a cleaning-bottle blaster. Pickups spawn around the map, and your kill count is saved to a high-score board.

## Running it

Python 3 and Arcade 3.3.3.

```bash
pip install -r requirements.txt
python main.py
```

## Controls

- WASD or the arrow keys to move
- Mouse to aim, click to shoot
- Esc to pause

## Layout

- `scenes/` title, gameplay, pause and game-over screens
- `systems/` combat, enemy spawning, input, items and the world
- `entities/` the player, zombies, projectiles and items
- `core/` and `ui/` shared game plumbing and the HUD
- `assets/` sprites, fonts and the layered audio
