from mazegenerator import MazeGenerator


class MazeAdapter:
    """Adapter for interacting with the generated maze.

    Provides methods to query maze properties, check collision detection,
    and regenerate mazes with different seeds.
    """

    def __init__(
        self, width: int, height: int, perfect: bool = True, seed: int = 42
    ) -> None:
        self._width = width
        self._height = height
        self._perfect = perfect
        self._seed = seed
        self._maze_generator = MazeGenerator((width, height),
                                             perfect, seed=seed)
        self._maze = self._maze_generator.maze

    def get_maze(self) -> list[list[int]]:
        """Return the maze."""
        return self._maze

    def get_entry(self) -> tuple[int, int]:
        """Return the entry coordinates (x, y)."""
        return self._maze_generator.maze_entry

    def get_exit(self) -> tuple[int, int]:
        """Return the exit coordinates (x, y)."""
        return self._maze_generator.maze_exit

    def get_corners(self) -> list[tuple[int, int]]:
        """Return the four maze corners as (x, y) coordinate pairs."""
        return [
            (0, 0),
            (self._width - 1, 0),
            (0, self._height - 1),
            (self._width - 1, self._height - 1),
        ]

    def get_ghost_pos(self) -> list[tuple[int, int]]:
        """Return the four ghost position as (x, y) coordinate pairs."""
        return [
            (1, 0),
            (self._width - 1, 1),
            (1, self._height - 1),
            (self._width - 2, self._height - 1),
        ]

    def get_center(self) -> tuple[int, int]:
        """Return the maze center coordinates (x, y)."""
        return (self._width // 2, self._height // 2)

    def get_shortest_path(self) -> str | bool:
        """Return the shortest path or False if impossible."""
        return self._maze_generator.shortest_path

    def get_width(self) -> int:
        """Return the maze width."""
        return self._width

    def get_height(self) -> int:
        """Return the maze height."""
        return self._height

    def get_cell(self, x: int, y: int) -> int:
        """Return the value of a cell."""
        if 0 <= x < self._width and 0 <= y < self._height:
            return self._maze[y][x]
        return -1  # Invalid coordinates

    def regenerate(
        self,
        seed: int | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        """Regenerate the maze, optionally with a new seed and/or size."""
        if seed is None:
            seed = self._seed
        if width is not None:
            self._width = width
        if height is not None:
            self._height = height
        self._seed = seed
        self._maze_generator = MazeGenerator(
            (self._width, self._height), self._perfect, seed=seed
        )
        self._maze = self._maze_generator.maze

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        """Check if there is a wall in a given direction (N, E, S, W)."""
        if not (0 <= x < self._width and 0 <= y < self._height):
            return True

        cell_value = self._maze[y][x]
        wall_bits = {"N": 1, "E": 2, "S": 4, "W": 8}

        if direction not in wall_bits:
            return True

        return (cell_value & wall_bits[direction]) != 0

    def can_move(self, x: int, y: int, direction: str) -> bool:
        """Check if we can move in a direction (N, E, S, W)."""
        return not self.has_wall(x, y, direction)
