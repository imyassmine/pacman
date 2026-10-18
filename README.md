*This activity has been created as part of the 42 curriculum by yassabda, mdjigo.*

# Pac-Man

## Description

This project is a Python recreation of the classic arcade game **Pac-Man**, built with `pygame`
for rendering and input, and an external `A-Maze-ing` package (assigned by another group) for
maze generation.

The player navigates a procedurally generated maze, eats pacgums and super-pacgums, avoids (or
hunts, once powered up) ghosts, and tries to clear at least 10 levels of increasing size while
keeping track of lives, score, and remaining time. Scores are saved to a persistent, file-based
highscore list, visible from the main menu.

The game is fully driven by a JSON configuration file (comments supported), is resilient to
missing or invalid configuration values, and includes a cheat mode intended to make peer review
easier.

## Instructions

### Requirements

- Python 3.10+
- `pygame`
- The `mazegenerator` package (the assigned `A-Maze-ing` implementation), installed as-is

### Installation

```console
$ make install
```

### Running the game

The program takes exactly one argument: a path to a JSON configuration file.

```console
$ make run ARGS=config.json
```

or, equivalently:

```console
$ make run
```

### Controls

- **Arrow keys** or **WASD**: move
- **P** or **Escape**: pause / resume
- **C**: toggle cheat mode
- **N** (while cheat mode is active): skip to the next level

### Other Makefile targets

- `make debug`: run the game under `pdb`
- `make clean`: remove `__pycache__` and `.mypy_cache`
- `make lint`: run `flake8` and `mypy` with the required flags
- `make lint-strict`: run `flake8` and `mypy --strict`
- `make package`: build the distributable package (runs `build.sh`)
- `make test`: run the test suite with `pytest`
- `make venv`: set up a virtual environment for dependency isolation
- `make help`: list all available targets

## Configuration

The configuration file is JSON, with support for `#`, `//`, and `/* */` comments (stripped
before parsing). All fields are optional — anything missing, invalid, or of the wrong type
falls back to a safe default, and a message is printed to explain what happened; unknown keys
are silently ignored. No configuration error ever produces a crash or a Python traceback.

| Key | Default | Description |
|---|---|---|
| `highscore_filename` | `"highscore.json"` | File used to persist the highscore list |
| `lives` | `3` | Starting number of lives |
| `points_per_pacgum` | `10` | Points earned per pacgum eaten |
| `points_per_super_pacgum` | `50` | Points earned per super-pacgum eaten |
| `points_per_ghost` | `200` | Points earned per edible ghost eaten |
| `seed` | `42` | Seed used to generate the first level's maze |
| `level_max_time` | `90` | Time limit per level, in seconds |
| `pacgum` | `42` | Reserved for future use (pacgum count override) |
| `level` | 10 default levels, from 15×15 to 25×23 | List of `{width, height}` per level, each between 15 and 25 |

If `level` ends up empty after validation, it is replaced with the 10 default levels so the game
always has at least the number of levels required by the subject.

## Highscore

Highscores are stored in a JSON file (`highscore_filename` from the config, `highscore.json` by
default), as a flat `{"name": score}` mapping.

- Loaded once when the highscore screen or the main menu needs them, and saved immediately after
  a score is entered — there is no separate "save on exit" step, so a highscore is never lost
  even if the game is closed abruptly afterward.
- Player names are validated (1–10 characters, alphanumeric and spaces only) and scores must be
  non-negative integers; anything invalid is discarded rather than crashing the load/save.
- If a name already has a saved score, only a strictly higher new score overwrites it.
- Only the top 10 scores are kept on save; the rest are dropped.
- The main menu's "View Highscores" option displays the full top 10, sorted descending.

We chose a single flat JSON file over, e.g., a database, because the requirement is a simple
persistent top-10 list with no concurrent access — a JSON file keeps the implementation
dependency-free and easy to inspect/debug by hand during review.

## Maze Generation

Mazes are produced by the assigned `A-Maze-ing` package (`mazegenerator.MazeGenerator`),
used as-is through a `MazeAdapter` wrapper (`maze/adapter.py`) that exposes only what the game
needs: cell lookup, wall queries per direction, corners, center, entry/exit, and regeneration.

- `MazeAdapter` is instantiated once, with the level 1 dimensions and the configured `seed`
  (fixed, as required for level 1), and with `PERFECT=False` for Pac-Man-compatible corridors.
- On every subsequent level, instead of creating a new adapter, `regenerate()` is called on the
  same instance with a new random seed and the next level's `width`/`height` — this keeps a
  single `MazeAdapter`/`Player` pairing alive for the whole game instead of juggling several
  maze objects.
- The player's spawn point is computed as the open cell closest to the maze's geometric center
  (Manhattan distance), matching the "player starts in the middle of the maze" requirement even
  though the generator itself doesn't guarantee an open center cell.
- If maze generation fails, `get_config` and the surrounding `try/except` blocks ensure the
  failure is reported with a clear message instead of propagating a traceback.

## Implementation

- **Entities**: `Pacgum` and `SuperPacgum` (`core/entities.py`) are simple collectible objects
  with a position and a point value; super-pacgums are placed on the 4 maze corners, regular
  pacgums on every other open cell except the player's spawn point.
- **Player**: moves one cell at a time in cardinal directions, blocked by `MazeAdapter.can_move`,
  and collects entities on its current cell (`check_collisions`).
- **Ghosts**: `core/ghosts.py` defines chase/flee behavior (Manhattan-distance-based) and a
  respawn-to-corner mechanic. The 4 ghosts are instantiated one per maze corner and updated
  every frame in the main loop: they chase the player while not edible, flee while edible
  (after a super-pacgum is eaten), and respawn to their corner after being eaten.
- **Game state**: `GameState` (`core/game_state.py`) owns the current level, score, timer, and
  entity list; it builds the first level in its constructor and regenerates the maze in place on
  `level_up()`. It exposes `is_game_over`, `is_level_complete`, and `is_victory` so the main loop
  can decide what to do next without knowing the underlying rules.
- **Rendering**: `ui/drawing.py` converts maze/entity/player grid coordinates into pixels and
  draws walls as line segments, entities and the player as circles; `ui/hud.py` renders score,
  lives, level, and remaining time.
- **Screens**: `ui/menu.py` (main menu, instructions, highscores), `ui/pause.py` (pause menu),
  and `ui/game_screens.py` (game over / victory name-entry screen) each own their own input
  handling and drawing.
- **Cheat mode**: toggled with `C`; while active, `is_game_over` is bypassed (invincibility) and
  `N` immediately advances to the next level, to let a reviewer walk through all levels and the
  victory screen quickly.

## General Software Architecture

```
src/
  __main__.py            # entry point: argument parsing, main loop, view dispatch
  config/
    loader.py            # GameConfig / LevelConfig (pydantic), JSON-with-comments parsing
  core/
    entities.py          # Entity, Pacgum, SuperPacgum
    ghosts.py            # Ghost (chase / flee / respawn)
    player.py            # Player (movement, collisions, respawn)
    game_state.py        # GameState (level lifecycle, score, win/lose rules)
  maze/
    adapter.py           # MazeAdapter, wraps the external MazeGenerator
  persistence/
    highscore.py         # HighscoreManager (load/save/validate)
  ui/
    drawing.py           # maze/entities/player rendering
    hud.py               # in-game HUD
    menu.py              # main menu + instructions + highscores overlay
    pause.py             # pause menu
    game_screens.py      # game-over / victory name-entry screen
```

`src/__main__.py` only coordinates: it owns the `pygame` event loop and the current "view"
(`menu`, `playing`, `paused`, `name_input`), and delegates all game rules to `GameState`, all
rendering to `ui/`, and all persistence to `persistence/highscore.py`. `GameState` depends on
`Player` and `MazeAdapter` but knows nothing about `pygame` — it can be tested independently of
the UI.

## Packaging

The Pacman game is downloadable and available on https://yassmarie.itch.io/pacman
To generate the zip file, run :
- ./build.sh
- cd dist
- zip -r Pacman-Linux.zip Pacman/

Your Pacman-Linux.zip file is now your package !


## Project Management

See the [`project-management/`](./project-management) directory for the team's timeline,
task split, and acceptance test notes.

## Resources

- [Pygame documentation](https://www.pygame.org/docs/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- Original Pac-Man ghost AI reference (chase/scatter/frightened behavior)

### AI usage

An AI assistant (Claude) was used throughout this activity for:

- Refactoring and simplifying `pac-man.py` (extracting event-handling and drawing helpers,
  removing duplicated geometry/spawn-finding logic).
- Discussing trade-offs between code brevity and readability (e.g., keeping explicit `if`
  statements over a lookup-table for wall directions).

All AI-suggested changes were reviewed and adapted before being integrated; complex parts (ghost
behavior, highscore persistence rules, level/maze regeneration) were discussed and understood
rather than pasted as-is.
