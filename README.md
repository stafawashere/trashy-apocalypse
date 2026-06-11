# Trashy Apocalypse

A small top-down survival game built with the [Arcade](https://api.arcade.academy/)
library. You play a janitor in a trash apocalypse — right now you can walk around
the map. This README is written to help someone new to Python (or just new to this
project) find their way around quickly.

## Controls

| Key        | Action     |
| ---------- | ---------- |
| `W` / `↑`  | Walk up    |
| `A` / `←`  | Walk left  |
| `S` / `↓`  | Walk down  |
| `D` / `→`  | Walk right |

## Run it

Python **3.11 or newer** is recommended (3.11–3.12 are the most tested).

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. Play
python main.py
```

## Project layout

```
trashy-apocalypse/
├── main.py            Entry point — run this. Creates the window and starts the game.
├── game.py            The Process window: builds the world and runs the per-frame loop.
│
├── objects/           "Nouns" — things that exist in the world (state + sprite).
│   ├── screen.py        Screen: window size and handy corner/centre coordinates.
│   ├── map.py           Map: the background image and its world dimensions.
│   ├── entities.py      LocalPlayer: the player you control, walk + hold animation.
│   └── item.py          Item: a named pick-up sprite (the windex bottle).
│
├── handlers/          "Verbs" — systems that act on objects every frame.
│   ├── movement.py      Movement: turns held keys into player velocity.
│   ├── camera.py        Camera: follows the player, clamped to the map edges.
│   ├── boundary.py      Boundary: keeps the player inside the map.
│   ├── spawner.py       Spawner: drops the windex once, at a random spot inside the view.
│   ├── pickup.py        Pickup: collects items the player walks over.
│   └── aim.py           Aim: rotates the held item to point at the mouse.
│
├── assets/            Images.
│   ├── background.png   The map.
│   ├── local_player/    Player sprite sheets (walk, idle, hold).
│   └── windex_item/     The windex bottle (held item).
│
└── docs/
    └── sprite-sizing.md  How to size new sprite art for this game's camera.
```

## How it works

The whole game is one `arcade.Window` subclass — `Process`, in `game.py`. Arcade
drives it by calling a few methods for you:

1. **`setup()`** runs once when the game starts (`main.py` calls it). It builds the
   world: the map, the player, and the handlers that drive them. Each sprite is
   added to a `SpriteList` — Arcade's batch of sprites it can draw and update
   together.

2. **`on_update(delta_time)`** runs ~60 times a second. This is the heartbeat, and
   it calls each handler in a deliberate order:

   ```
   movement.update()                  read held keys  → set player velocity
   player_list.update()               apply velocity  → move the player sprite
   boundary.update()                  snap the player back if it left the map
   camera.update()                    re-centre the view on the player
   spawner.update()                   drop the windex once, inside the view
   pickup.update()                    collect a windex the player is touching
   local_player.update_animation()    pick walk/hold frame; pin a held item to the hand
   aim.update()                       rotate the held item toward the mouse
   ```

3. **`on_draw()`** runs every frame: clear the screen, point the camera, then draw
   the map, the loose items, the player, and finally anything held (back to front).

Key presses don't move anything directly — `on_key_press` / `on_key_release` just
tell `Movement` which keys are held. The actual movement happens in the loop above.

### The two-folder mental model

- **`objects/`** is *what exists*: a player, a map, the screen. They hold state
  (position, health, sprite) but don't decide anything on their own.
- **`handlers/`** is *what happens*: movement, the camera, boundaries. Each handler
  is handed the objects it needs and exposes an `update()` that the game loop calls.

So when you're reading the code: to learn *what a thing is*, open `objects/`; to
learn *how it behaves*, open `handlers/`.

### A good reading order

1. `main.py` — three lines; see how the program starts.
2. `game.py` — read `setup()` then `on_update()`. This is the spine; everything
   else hangs off it.
3. `handlers/movement.py` — the simplest handler, and a clean example of the
   pattern every handler follows.
4. `objects/entities.py` — `LocalPlayer`, and how the walk animation chooses a
   facing and cycles through frames.

## Code style

The code is meant to read without comments — names carry the meaning. See
[CLAUDE.md](CLAUDE.md) for the rules (named constants instead of magic numbers,
`is_` / `has_` booleans, no "what" comments). When adding new sprite art, size it
using [docs/sprite-sizing.md](docs/sprite-sizing.md).
