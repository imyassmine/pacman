import sys
from pathlib import Path
import pygame
from src.config.loader import get_config
from src.core.game_state import GameState
from src.ui.drawing import draw_maze, draw_entities, draw_ghosts
from src.ui.game_screens import Game
from src.ui.menu import Action, MainMenu
from src.ui.pause import PauseMenu
from src.ui.hud import draw_hud

CELL_SIZE = 60
HUD_HEIGHT = 60

DIRECTIONS = {
    pygame.K_UP: "N",
    pygame.K_w: "N",
    pygame.K_DOWN: "S",
    pygame.K_s: "S",
    pygame.K_LEFT: "W",
    pygame.K_a: "W",
    pygame.K_RIGHT: "E",
    pygame.K_d: "E",
}


def main() -> None:
    """Main game loop."""
    pygame.init()
    pygame.display.set_caption("PACMAN")
    clock = pygame.time.Clock()

    if len(sys.argv) == 1 and getattr(sys, "frozen", False):
        config_path = Path(sys.executable).resolve().parent / "config.json"
    elif len(sys.argv) == 2:
        config_path = Path(sys.argv[1])
    else:
        print("[STDERR] Usage: python -m src <config_file>")
        sys.exit(1)

    config = get_config(str(config_path))
    max = {"width": 0, "height": 0}
    for level in config.level:
        if level.width > max["width"]:
            max["width"] = level.width
        if level.height > max["height"]:
            max["height"] = level.height
    screen = pygame.display.set_mode(
        (
            max["width"] * CELL_SIZE + 2,
            max["height"] * CELL_SIZE + HUD_HEIGHT + 2,
        )
    )
    main_menu = MainMenu(screen)
    pause_menu = PauseMenu(screen)
    game = Game(screen)
    view: str = "menu"
    game_state: GameState | None = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if view == "menu":
                action = main_menu.handle_event(event)
                if action == Action.START_GAME:
                    game_state = GameState(config)
                    view = "playing"
                elif action == Action.INSTRUCTIONS:
                    main_menu.current_view = "instructions"
                elif action == Action.VIEW_HIGHSCORES:
                    main_menu.current_view = "highscores"
                elif action == Action.EXIT:
                    running = False
                continue

            if view == "playing" and game_state:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        view = "paused"
                        continue
                    if event.key == pygame.K_c:
                        game_state.cheat_mode = not game_state.cheat_mode
                        continue
                    if game_state.cheat_mode and event.key == pygame.K_n:
                        game_state.level_up()
                        if game_state.is_victory():
                            game.victory(game_state.score)
                            view = "name_input"
                        continue
                    direction = DIRECTIONS.get(event.key)
                    if direction:
                        game_state.player.set_direction(direction)
                continue

            if view == "paused":
                if event.type == pygame.KEYDOWN:
                    pause_action = pause_menu.handle_event(event)
                    if pause_action == "playing":
                        view = "playing"
                    elif pause_action == "menu":
                        view = "menu"
                        game_state = None
                continue

            if view == "name_input":
                if game.handle_event(config.highscore_filename, event):
                    view = "menu"
                    game_state = None

        screen.fill((0, 0, 0))

        if view == "playing" and game_state:
            dt = clock.get_time() / 1000
            game_state.player.move_in_current_direction(dt)
            game_state.update_score()

        if view == "menu":
            main_menu.draw(config.highscore_filename)
        elif view == "playing" and game_state:
            maze_adapter = game_state.player.maze_adapter
            draw_maze(screen, maze_adapter, CELL_SIZE, HUD_HEIGHT)
            draw_entities(screen, game_state, CELL_SIZE, HUD_HEIGHT)
            draw_ghosts(screen, game_state, CELL_SIZE, HUD_HEIGHT)
            draw_hud(screen, game_state)
            game_state.ghosts_update(clock.get_time() / 1000)
            game_state.update_time(1 / 60)

            if game_state.is_game_over():
                game.game_over(game_state.score)
                view = "name_input"
            elif game_state.is_victory():
                game.victory(game_state.score)
                view = "name_input"
            elif game_state.is_level_complete():
                game_state.level_up()
                view = "playing"
        elif view == "paused":
            pause_menu.draw_pause_menu()
        elif view == "name_input":
            game.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
