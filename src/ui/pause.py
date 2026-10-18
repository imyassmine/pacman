import pygame


class PauseMenu():
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.index = 0

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle keyboard navigation in the pause menu."""
        if event.key in (pygame.K_ESCAPE, pygame.K_p):
            return "playing"
        if event.key in (pygame.K_UP, pygame.K_w):
            self.index = 0
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.index = 1
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.index == 0:
                return "playing"
            return "menu"
        return None

    def draw_pause_menu(self) -> tuple[pygame.Rect, pygame.Rect]:
        """Draw the pause menu."""
        rect = pygame.Rect(0, 0, self.screen.get_width(),
                           self.screen.get_height())
        pygame.draw.rect(self.screen, (0, 0, 0, 128), rect)
        font = pygame.font.SysFont("Latin Modern Roman", 36)

        resume_color = (255, 255, 0) if self.index == 0 else (255, 255, 255)
        main_menu_color = (255, 255, 0) if self.index == 1 else (255, 255, 255)

        resume_text = font.render("RESUME THE GAME", True, resume_color)
        resume_rect = resume_text.get_rect(
            center=(self.screen.get_width() / 2,
                    self.screen.get_height() / 2 - 50))
        self.screen.blit(resume_text, resume_rect)

        main_menu_text = font.render("RETURN TO MAIN MENU",
                                     True,
                                     main_menu_color)
        main_menu_rect = main_menu_text.get_rect(
            center=(self.screen.get_width() / 2,
                    self.screen.get_height() / 2 + 50))
        self.screen.blit(main_menu_text, main_menu_rect)
        return resume_rect, main_menu_rect
