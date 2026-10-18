from src.core.player import Player
from src.maze.adapter import MazeAdapter
from src.core.entities import Entity


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
        distances = {}
        if self.maze_adapter.can_move(self.x, self.y, "E"):
            distances["E"] = (
                abs(self.x + 1 - player.x)
                + abs(self.y - player.y)
            )
        if self.maze_adapter.can_move(self.x, self.y, "W"):
            distances["W"] = (
                abs(self.x - 1 - player.x)
                + abs(self.y - player.y)
            )
        if self.maze_adapter.can_move(self.x, self.y, "S"):
            distances["S"] = (
                abs(self.x - player.x)
                + abs(self.y + 1 - player.y)
            )
        if self.maze_adapter.can_move(self.x, self.y, "N"):
            distances["N"] = (
                abs(self.x - player.x)
                + abs(self.y - 1 - player.y)
            )
        if not distances:
            return
        direction = min(distances.items(), key=lambda item: item[1])[0]
        if direction == "W":
            self.x -= 1
        elif direction == "E":
            self.x += 1
        elif direction == "S":
            self.y += 1
        elif direction == "N":
            self.y -= 1
        self.position = (self.x, self.y)

    def move_away(self, player: Player) -> None:
        """Move the ghost away from the player."""
        distances = {}
        if self.maze_adapter.can_move(self.x, self.y, "E"):
            distances["E"] = (
                abs(self.x + 1 - player.x)
                + abs(self.y - player.y)
            )
        if self.maze_adapter.can_move(self.x, self.y, "W"):
            distances["W"] = (
                abs(self.x - 1 - player.x)
                + abs(self.y - player.y)
            )
        if self.maze_adapter.can_move(self.x, self.y, "S"):
            distances["S"] = (
                abs(self.x - player.x)
                + abs(self.y + 1 - player.y)
            )
        if self.maze_adapter.can_move(self.x, self.y, "N"):
            distances["N"] = (
                abs(self.x - player.x)
                + abs(self.y - 1 - player.y)
            )
        if not distances:
            return
        direction = max(distances.items(), key=lambda item: item[1])[0]
        if direction == "W":
            self.x -= 1
        elif direction == "E":
            self.x += 1
        elif direction == "S":
            self.y += 1
        elif direction == "N":
            self.y -= 1
        self.position = (self.x, self.y)
