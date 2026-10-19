from typing import Any

from src.core.entities import Entity, SuperPacgum
from src.maze.adapter import MazeAdapter


class Player:
    """Represents the player controlled character in the game.

    The player can move through the maze, collect pacgums, eat ghosts,
    and respawn when reaching specific conditions.

    Attributes:
        x: Current x-coordinate of the player.
        y: Current y-coordinate of the player.
        points: Current points/score of the player.
        lives: Number of lives remaining.
        maze_adapter: Adapter for maze navigation and collision detection.
    """

    def __init__(
        self,
        position: tuple[int, int],
        points: int,
        lives: int,
        maze_adapter: MazeAdapter,
    ) -> None:
        self.x, self.y = position
        self.points = points
        self.lives = lives
        self.maze_adapter = maze_adapter
        self.direction: str | None = None
        self.move_timer: float = 0.0
        self.move_interval: float = 0.1

    def get_points(self) -> int:
        """Get the current points/score."""
        return self.points

    def respawn(self, position: tuple[int, int]) -> None:
        """Move the player back to the given position."""
        self.x, self.y = position

    def check_collisions(self, entities: list[Entity],
                         ghosts: list[Any]) -> int:
        """Eat entities at the player's position."""
        count = 0
        for entity in entities:
            if not entity.is_eaten and entity.position == (self.x, self.y):
                count += 1
                self.points += entity.eat()
                if isinstance(entity, SuperPacgum):
                    for ghost in ghosts:
                        ghost.is_edible = True
                        ghost.edible_timer = 8.0

        return count

    def check_ghost_collision(self, ghost: Entity) -> bool:
        """Check if the player collides with any ghosts."""
        return not ghost.is_eaten and (ghost.x, ghost.y) == (self.x, self.y)

    def set_direction(self, direction: str) -> None:
        """Store the direction currently requested by the player."""
        self.direction = direction

    def move_in_current_direction(self, dt: float) -> bool:
        """Move the player one cell in the active direction when possible."""
        if self.direction is None:
            return False

        self.move_timer += dt
        if self.move_timer < self.move_interval:
            return False

        self.move_timer -= self.move_interval

        if not self.maze_adapter.can_move(self.x, self.y, self.direction):
            return False

        self.move(self.direction)
        return True

    def move(self, direction: str) -> None:
        """Move the player in the specified direction."""
        if self.maze_adapter.can_move(self.x, self.y, direction):
            if direction == "N":
                self.y -= 1
            elif direction == "S":
                self.y += 1
            elif direction == "E":
                self.x += 1
            elif direction == "W":
                self.x -= 1
