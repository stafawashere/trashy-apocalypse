# Trashy Apocalypse

A top-down zombie survival shooter my AP Computer Science Principles team made with Python's Arcade library at the High School of Arts and Technology. I led the coding. It was our school's entry at the annual arts event.

You start in a trashed wasteland with empty hands. A spray bottle shows up somewhere on screen, and once you walk over it you can aim with the mouse and hold the button down to spray. Every shot drains a little of the bottle's tank, and it refills on its own over time. A zombie spawns every three seconds, up to ten at once, and each one takes four hits. Touching one costs you health. When you run out, the game-over screen shows your kill count and your best score, which is saved in `highscore.json`.

## Running it

You need Python 3 and Arcade 3.3.3, which is pinned in `requirements.txt`.

```bash
pip install -r requirements.txt
python main.py
```

## Controls

- WASD or the arrow keys to move
- Mouse to aim, hold a mouse button to spray
- Esc to pause and resume

## Layout

- `scenes/` the title, gameplay, pause and game-over screens
- `systems/` combat, zombie spawning and movement, input, item pickup, the map and the camera
- `entities/` the player, zombies, projectiles and items
- `core/` audio, the high score, screen sizing and fade transitions
- `ui/` the HUD, crosshair and cursor
- `constants/` the tuning numbers, like speeds, damage, spawn rate and volumes
- `assets/` sprites, fonts, music and sound effects

The walls, crates and pipes you bump into come from `tools/scan_map.py`, which reads `assets/background.png`, sorts the pixels by color into those three kinds of obstacle and writes out the rectangles that ended up in `constants/world.py`. It needs Pillow, but the game itself doesn't.
