import pygame
from enum import Enum
from json import loads, JSONDecodeError


class Action(Enum):
    START_GAME = 0
    VIEW_HIGHSCORES = 1
    INSTRUCTIONS = 2
    EXIT = 3


class MainMenu():
    """Main menu screen for navigating the game.

    Provides a menu interface for starting a new game, viewing highscores,
    viewing instructions, or exiting the application.

    Attributes:
        screen: The pygame display surface.
        actions: List of available menu actions.
        index: Currently selected menu item index.
        current_view: The current screen view.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.actions = list(Action)
        self.index = 0
        self.current_view = "menu"

    def show_instruction(self) -> None:
        """Display the instructions screen overlay."""
        rect = pygame.Rect(0, 0, self.screen.get_width(),
                           self.screen.get_height())
        pygame.draw.rect(self.screen, (0, 0, 0, 128), rect)
        font = pygame.font.SysFont("Latin Modern Roman", 20)
        lines = ["HOW TO PLAY :",
                 "Move with the arrow keys or WASD.",
                 "Eat every pacgum to clear the level.",
                 "Super-pacgums (in the corners) make the ghosts "
                 "edible for a short time.",
                 "Avoid the ghosts: each contact costs you a life.",
                 "Lose all your lives and it's game over.",
                 "Clear every level to win the game!",
                 "P : Pause",
                 "C : Toggle cheat mode",
                 "N : Skip to the next level (cheat mode only)"]
        spacing = 50
        total_height = (len(lines) - 1) * spacing
        start_y = (self.screen.get_height() / 2) - (total_height / 2)

        for i, line in enumerate(lines):
            text = font.render(line.strip(), True, (255, 255, 255))
            rect = text.get_rect(
                center=(self.screen.get_width() / 2, start_y + i * spacing)
            )
            self.screen.blit(text, rect)

        info_font = pygame.font.SysFont("Arial", 24)
        info_text = info_font.render(
            "Press ESC to return to the menu", True, (200, 200, 200)
        )
        info_rect = info_text.get_rect(
            center=(self.screen.get_width() - 200,
                    self.screen.get_height() - 30)
        )
        self.screen.blit(info_text, info_rect)

    def show_highscores(self, file: str) -> None:
        """Display the highscores screen overlay."""
        try:
            with open(file, "r") as fd:
                data = fd.readline()
            scores = loads(data)
        except (FileNotFoundError, JSONDecodeError):
            scores = None

        rect = pygame.Rect(0, 0, self.screen.get_width(),
                           self.screen.get_height())
        pygame.draw.rect(self.screen, (0, 0, 0, 128), rect)
        if scores:
            sorted_scores = dict(sorted(scores.items(),
                                        key=lambda x: x[1],
                                        reverse=True))
            font = pygame.font.SysFont("Latin Modern Roman", 36)
            spacing = 38
            total_height = (len(sorted_scores) - 1) * spacing
            start_y = (self.screen.get_height() / 2) - (total_height / 2)

            for i, (name, score) in enumerate(sorted_scores.items()):
                content = f"{i + 1}. {name} - {score}pts"
                score_text = font.render(content, True, (255, 255, 255))
                score_rect = score_text.get_rect(
                    center=(self.screen.get_width() / 2, start_y + i * spacing)
                )
                self.screen.blit(score_text, score_rect)
        info_font = pygame.font.SysFont("Arial", 24)
        info_text = info_font.render(
            "Press ESC to return to the menu", True, (200, 200, 200)
        )
        info_rect = info_text.get_rect(
            center=(self.screen.get_width() - 200,
                    self.screen.get_height() - 30)
        )
        self.screen.blit(info_text, info_rect)
        return None

    def handle_event(self, event: pygame.event.Event) -> Action | None:
        """Handle keyboard input for menu navigation and selection."""
        if event.type == pygame.KEYDOWN:
            if self.current_view != "menu":
                if event.key == pygame.K_ESCAPE:
                    self.current_view = "menu"
                return None

            if event.key == pygame.K_UP:
                if self.index == 0:
                    pass
                else:
                    self.index -= 1
            elif event.key == pygame.K_DOWN:
                if self.index == 3:
                    pass
                else:
                    self.index += 1
            elif event.key == pygame.K_RETURN:
                return self.actions[self.index]
        return None

    def draw(self, file: str) -> None:
        """Render the current menu screen."""
        if self.current_view == "instructions":
            self.show_instruction()
        elif self.current_view == "highscores":
            self.show_highscores(file)
        else:  # menu
            rect = pygame.Rect(0, 0, self.screen.get_width(),
                               self.screen.get_height())
            pygame.draw.rect(self.screen, (0, 0, 0, 128), rect)

            title_font = pygame.font.SysFont("Arial", 72, bold=True)
            title_text = title_font.render("PACMAN", True, (255, 165, 0))
            title_rect = title_text.get_rect(center=(self.screen.get_width() /
                                                     2, 80))
            self.screen.blit(title_text, title_rect)

            font = pygame.font.SysFont("Arial", 36)

            start_y = self.screen.get_height() / 2 - 90
            spacing = 60

            for i, action in enumerate(self.actions):
                color = (255, 255, 0) if i == self.index else (255, 255, 255)
                action_text = font.render(action.name, True, color)
                action_rect = action_text.get_rect(
                    center=(self.screen.get_width() / 2, start_y + i * spacing)
                )
                self.screen.blit(action_text, action_rect)
