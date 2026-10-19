import random

from src.config.loader import GameConfig
from src.core.entities import Entity, Pacgum, SuperPacgum
from src.core.ghosts import Ghost
from src.core.player import Player
from src.maze.adapter import MazeAdapter

WALL_CELL = 15


def get_centered_open_cell(maze_adapter: MazeAdapter) -> tuple[int, int]:
    """Find the open cell closest to the maze center."""
    width, height = maze_adapter.get_width(), maze_adapter.get_height()
    center_x, center_y = maze_adapter.get_center()
    open_cells = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if maze_adapter.get_cell(x, y) != WALL_CELL
        and any(not maze_adapter.has_wall(x, y, direction)
                for direction in ("N", "E", "S", "W"))
    ]
    return min(open_cells,
               key=lambda p: abs(p[0] - center_x) + abs(p[1] - center_y))


def get_pacgum_pos(config: GameConfig,
                   maze_adapter: MazeAdapter) -> list[tuple[int, int]]:
    """Return the randomly sampled pacgum positions."""
    return [
        (random.randint(0, maze_adapter.get_width() - 1),
         random.randint(0, maze_adapter.get_height() - 1))
        for _ in range(config.pacgum)
    ]


def init_entities(
    maze_adapter: MazeAdapter,
    config: GameConfig,
) -> tuple[list[Entity], list[Ghost]]:
    """Populate a maze with pacgums and super-pacgums.

    Walls and the player spawn cell are skipped.
    """
    entities: list[Entity] = []
    ghosts: list[Ghost] = []
    corners = set(maze_adapter.get_corners())
    ghost_pos = set(maze_adapter.get_ghost_pos())
    pacgum_pos = set(get_pacgum_pos(config, maze_adapter))
    spawn = get_centered_open_cell(maze_adapter)
    for y, row in enumerate(maze_adapter.get_maze()):
        for x, cell in enumerate(row):
            if cell == WALL_CELL or (x, y) == spawn:
                continue
            position = (x, y)
            if position in corners:
                entities.append(SuperPacgum(position,
                                            config.points_per_super_pacgum))
            elif position in ghost_pos:
                ghosts.append(Ghost(position,
                                    config.points_per_ghost,
                                    maze_adapter))
            elif position in pacgum_pos:
                entities.append(Pacgum(position,
                                       config.points_per_pacgum))

    return (entities, ghosts)


def get_level_seed(config: GameConfig, level_index: int) -> int:
    """Return a deterministic seed for a 1-based level index."""
    return config.seed + level_index - 1


class GameState:
    """Manages the overall game state and logic.

    Builds the first level from the given config on construction, and
    regenerates the maze in place on each level_up().
    """

    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.current_level = 1
        self.total_levels = len(config.level)
        self.score = 0
        self.cheat_mode = False
        self.victory_reached = False
        self.remaining_time_for_level: float = config.level_max_time

        level_config = config.level[0]
        maze_adapter = MazeAdapter(
            level_config.width,
            level_config.height,
            seed=get_level_seed(config, self.current_level),
        )
        self.entities, self.ghosts = init_entities(maze_adapter, config)
        self.player = Player(
            position=get_centered_open_cell(maze_adapter),
            points=0,
            lives=config.lives,
            maze_adapter=maze_adapter,
        )

    def level_up(self) -> None:
        """Advance to the next level, or flag the victory."""
        self.current_level += 1
        self.remaining_time_for_level = self.config.level_max_time
        if self.current_level > self.total_levels:
            self.victory_reached = True
            return
        level_config = self.config.level[self.current_level - 1]
        self.player.maze_adapter.regenerate(
            get_level_seed(self.config, self.current_level),
            level_config.width,
            level_config.height,
        )
        self.player.respawn(get_centered_open_cell(self.player.maze_adapter))
        self.entities, self.ghosts = init_entities(
            self.player.maze_adapter, self.config
        )

    def update_time(self, time_passed: float) -> None:
        """Update the remaining time for the current level."""
        self.remaining_time_for_level -= time_passed
        if self.remaining_time_for_level < 0:
            self.remaining_time_for_level = 0

    def update_score(self) -> None:
        """Update the score based on pacgum and ghost collisions."""
        self.player.check_collisions(self.entities, self.ghosts)
        self.score = self.player.get_points()

    def is_game_over(self) -> bool:
        """Check if the game is over (time out or no lives left)."""
        if self.cheat_mode:
            return False
        return self.remaining_time_for_level == 0 or self.player.lives == 0

    def is_level_complete(self) -> bool:
        """Check if the current level is complete (all pacgums eaten)."""
        return all(
            entity.is_eaten
            for entity in self.entities
            if isinstance(entity, Pacgum)
        )

    def is_victory(self) -> bool:
        """True if the last level has just been completed."""
        return self.victory_reached or (
            self.is_level_complete()
            and self.current_level == self.total_levels
        )

    def _hit_ghost(self, ghost: Ghost) -> None:
        """Apply the effect of the player colliding with a ghost."""
        if ghost.is_edible:
            self.player.points += ghost.eat()
            self.score = self.player.get_points()
            ghost.is_edible = False
            ghost.respawn_timer = 8.0
            return
        self.player.lives -= 1
        self.player.respawn(get_centered_open_cell(self.player.maze_adapter))

    def ghosts_update(self, dt: float) -> None:
        """Update the state of all ghosts."""
        for ghost in self.ghosts:
            ghost.update(dt)
            if ghost.is_eaten:
                continue

            if self.player.check_ghost_collision(ghost):
                self._hit_ghost(ghost)
                continue

            if not ghost.can_move_this_frame(dt):
                continue

            if ghost.is_edible:
                ghost.move_away(self.player)
            else:
                ghost.chase_player(self.player)
            if self.player.check_ghost_collision(ghost):
                self._hit_ghost(ghost)
