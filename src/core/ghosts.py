from src.core.entities import Entity
from src.core.player import Player
from src.maze.adapter import MazeAdapter

MOVES = {"E": (1, 0), "W": (-1, 0), "S": (0, 1), "N": (0, -1)}


class Ghost(Entity):
    """Represents an enemy ghost in the game.

    Ghosts can chase or flee from the player depending on their state.
    When eaten, they award points to the player.

    Attributes:
        start_x: Starting x-coordinate for respawn.
        start_y: Starting y-coordinate for respawn.
        maze_adapter: Adapter for maze navigation and collision detection.
        is_edible: Whether the ghost can currently be eaten by the player.
    """

    def __init__(
        self,
        position: tuple[int, int],
        points: int,
        maze_adapter: MazeAdapter,
        is_edible: bool = False,
        is_eaten: bool = False,
    ) -> None:
        super().__init__(position=position, points=points, is_eaten=is_eaten)
        self.start_x, self.start_y = position
        self.maze_adapter = maze_adapter
        self.is_edible = is_edible
        self.edible_timer: float = 0.0
        self.respawn_timer: float = 0.0
        self.move_timer: float = 0.0
        self.move_interval: float = 0.15

    def respawn(self) -> None:
        """Reset the ghost position to the starting point."""
        self.x = self.start_x
        self.y = self.start_y
        self.position = (self.x, self.y)
        self.is_edible = False
        self.edible_timer = 0.0
        self.is_eaten = False
        self.respawn_timer = 0.0
        self.move_timer = 0.0

    def update(self, dt: float) -> None:
        """Advance the edible and respawn timers."""
        if self.is_edible:
            self.edible_timer -= dt
            if self.edible_timer <= 0:
                self.is_edible = False
                self.edible_timer = 0.0

        if self.is_eaten:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.respawn()

    def can_move_this_frame(self, dt: float) -> bool:
        """Return whether enough time has elapsed for another move."""
        self.move_timer += dt
        if self.move_timer < self.move_interval:
            return False
        self.move_timer -= self.move_interval
        return True

    def chase_player(self, player: Player) -> None:
        """Move the ghost towards the player."""
        self._move_closest(player, flee=False)

    def move_away(self, player: Player) -> None:
        """Move the ghost away from the player."""
        self._move_closest(player, flee=True)

    def _move_closest(self, player: Player, flee: bool) -> None:
        """Move towards the player, or away from them when fleeing."""
        distances: dict[str, int] = {}
        for direction, (dx, dy) in MOVES.items():
            if self.maze_adapter.can_move(self.x, self.y, direction):
                distances[direction] = (
                    abs(self.x + dx - player.x)
                    + abs(self.y + dy - player.y)
                )
        if not distances:
            return
        pick = max if flee else min
        direction = pick(distances.items(), key=lambda item: item[1])[0]
        dx, dy = MOVES[direction]
        self.x += dx
        self.y += dy
        self.position = (self.x, self.y)
