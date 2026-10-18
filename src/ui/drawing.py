import pygame
from src.core.game_state import GameState
from src.core.entities import SuperPacgum
from src.maze.adapter import MazeAdapter


def to_pixel(x: int, y: int, cell_size: int) -> tuple[int, int]:
    """Convert a grid cell to its center pixel coordinates in the window."""
    return x * cell_size + cell_size // 2, y * cell_size + cell_size // 2


def draw_maze(screen: pygame.Surface,
              maze_adapter: MazeAdapter,
              cell_size: int,
              y_offset: int = 0) -> None:
    wall_color = (0, 80, 220)
    width = maze_adapter.get_width()
    height = maze_adapter.get_height()
    for y in range(height):
        for x in range(width):
            left = x * cell_size
            top = y * cell_size + y_offset

            if maze_adapter.get_cell(x, y) == 15:
                pygame.draw.rect(screen, (0, 0, 139),
                                 (x * cell_size,
                                  y * cell_size + y_offset,
                                  cell_size, cell_size))

            if maze_adapter.has_wall(x, y, 'N'):
                pygame.draw.line(screen, wall_color,
                                 (left, top),
                                 (left + cell_size, top), 2)
            if maze_adapter.has_wall(x, y, 'E'):
                pygame.draw.line(screen, wall_color,
                                 (left + cell_size, top),
                                 (left + cell_size, top + cell_size), 2)
            if maze_adapter.has_wall(x, y, 'S'):
                pygame.draw.line(screen, wall_color,
                                 (left, top + cell_size),
                                 (left + cell_size, top + cell_size), 2)
            if maze_adapter.has_wall(x, y, 'W'):
                pygame.draw.line(screen, wall_color,
                                 (left, top),
                                 (left, top + cell_size), 2)


def draw_entities(screen: pygame.Surface,
                  game_state: GameState,
                  cell_size: int,
                  y_offset: int = 0) -> None:
    """Draw all entities and the player on the maze."""
    for entity in game_state.entities:
        if entity.is_eaten:
            continue
        ex, ey = to_pixel(entity.x, entity.y, cell_size)
        ey += y_offset
        if isinstance(entity, SuperPacgum):
            pygame.draw.circle(screen, (255, 255, 255),
                               (ex, ey), cell_size // 4)
            pygame.draw.circle(screen, (255, 200, 0),
                               (ex, ey), cell_size // 6)
        else:
            pygame.draw.circle(screen, (255, 165, 0),
                               (ex, ey), cell_size // 6)
    px, py = to_pixel(game_state.player.x, game_state.player.y,
                      cell_size)
    py += y_offset

    radius = cell_size // 3
    eye_radius = radius // 4
    pygame.draw.circle(screen, (255, 255, 0), (px, py), radius)
    pygame.draw.circle(screen, (255, 255, 255),
                       (px - radius // 2, py - radius // 4),
                       eye_radius)
    pygame.draw.circle(screen, (255, 255, 255),
                       (px + radius // 2, py - radius // 4),
                       eye_radius)


def draw_ghosts(screen: pygame.Surface,
                game_state: GameState,
                cell_size: int,
                y_offset: int = 0) -> None:
    """Draw all ghosts according to their current state."""
    radius = cell_size // 3
    eye_radius = radius // 4
    i = 0
    for ghost in game_state.ghosts:
        gx, gy = to_pixel(ghost.x, ghost.y, cell_size)
        gy += y_offset

        if ghost.is_eaten:
            continue

        if ghost.is_edible:
            color = [(150, 150, 150),
                     (150, 150, 150),
                     (150, 150, 150),
                     (150, 150, 150)]

        else:
            color = [(255, 0, 0),
                     (255, 100, 0),
                     (0, 200, 0),
                     (0, 100, 255)]

        pygame.draw.circle(screen, color[i], (gx, gy), radius)
        pygame.draw.rect(screen, color[i], (gx - radius,
                                            gy, radius * 2, radius))
        pygame.draw.circle(screen, (255, 255, 255),
                           (gx - radius // 2, gy - radius // 4),
                           eye_radius)
        pygame.draw.circle(screen, (255, 255, 255),
                           (gx + radius // 2, gy - radius // 4),
                           eye_radius)
        i += 1
