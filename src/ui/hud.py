import pygame
from src.core.game_state import GameState


def draw_hud(screen: pygame.Surface,
             game_state: GameState) -> None:
    """Draw the HUD (score, lives, level, and time remaining)."""
    font = pygame.font.SysFont("Latin Modern Roman", 30)
    score_label = f"Score: {game_state.score}"
    if game_state.cheat_mode:
        score_label += " [CHEAT]"
    score_text = font.render(score_label,
                             True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {game_state.player.lives}",
                             True, (255, 255, 255))
    screen.blit(lives_text, (300, 10))
    level_text = font.render(
        f"Level: {game_state.current_level}", True, (255, 255, 255)
    )
    screen.blit(level_text, (450, 10))
    remaining_time_text = font.render(
        f"Time Remaining: {int(game_state.remaining_time_for_level)}s",
        True,
        (255, 255, 255),
    )
    screen.blit(remaining_time_text, (600, 10))
