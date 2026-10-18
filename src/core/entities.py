class Entity:
    """Base class for collectible entities in the game.

    Represents items that can be collected by the player for points.

    Attributes:
        position: The (x, y) coordinates of the entity.
        x: The x-coordinate of the entity.
        y: The y-coordinate of the entity.
        points: The points awarded when this entity is eaten.
        is_eaten: Whether this entity has been consumed.
    """

    def __init__(
        self,
        position: tuple[int, int],
        points: int,
        is_eaten: bool = False,
    ) -> None:
        self.position = position
        self.x, self.y = position
        self.points = points
        self.is_eaten = is_eaten

    def eat(self) -> int:
        """Mark this entity as eaten and return its point value."""
        if self.is_eaten:
            return 0
        self.is_eaten = True
        return self.points


class Pacgum(Entity):
    """Represents a regular pacgum item."""

    def __init__(self, position: tuple[int, int], points: int) -> None:
        """Initialize a Pacgum."""
        super().__init__(position=position, points=points)


class SuperPacgum(Entity):
    """Represents a super pacgum (power-up) item."""

    def __init__(self, position: tuple[int, int], points: int) -> None:
        """Initialize a SuperPacgum."""
        super().__init__(position=position, points=points)
