import pygame
from src.persistence.highscore import HighscoreManager as hg


class Game():
    """Manages the game over and victory screens with name input.

    Handles the display of game over or victory screens, manages
    player name input, and saves high scores.

    Attributes:
        screen: The pygame display surface.
        is_victory: Whether the game ended in victory.
        state: Current screen state ('playing' or 'name_input').
        input_name: The name entered by the player.
        score: The final score from the game.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.is_victory = False
        self.state = "playing"
        self.input_name = ""
        self.score = 0
        self.hg_manager = hg()

    def game_over(self, score: int) -> None:
        """Transition to game over screen with name input."""
        self.state = "name_input"
        self.score = score
        self.input_name = ""
        self.is_victory = False

    def victory(self, score: int) -> None:
        """Transition to victory screen with name input."""
        self.state = "name_input"
        self.score = score
        self.input_name = ""
        self.is_victory = True

    def _save_score(self, file: str) -> None:
        """Save the score to highscores.json."""
        highscores = self.hg_manager.load_highscores(file)
        highscores[self.input_name] = self.score
        self.hg_manager.save_highscores(file, highscores)

    def handle_event(self, file: str, event: pygame.event.Event) -> bool:
        """
        Handle keyboard input for name entry.
        Returns True if the player saved their score (go back to menu).
        """
        if self.state != "name_input":
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_name = self.input_name[:-1]

            elif event.key == pygame.K_RETURN:
                if self.hg_manager.is_valid_name(self.input_name):
                    self._save_score(file)
                    return True
                return False

            elif (
                len(self.input_name) < 10
                and event.unicode
                and (event.unicode.isalnum() or event.unicode.isspace())
            ):
                self.input_name += event.unicode

        return False

    def draw(self) -> None:
        """Draw the current screen."""
        if self.state == "name_input":
            self._draw_name_input()

    def _draw_name_input(self) -> None:
        """Draw the name input screen."""
        rect = pygame.Rect(0, 0, self.screen.get_width(),
                           self.screen.get_height())
        pygame.draw.rect(self.screen, (0, 0, 0, 128), rect)

        # Titre
        title_font = pygame.font.SysFont("Arial", 72, bold=True)
        if self.is_victory:
            title = title_font.render("VICTORY!", True, (0, 255, 0))
        else:
            title = title_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title.get_rect(center=(self.screen.get_width() / 2, 100))
        self.screen.blit(title, title_rect)

        # Score
        score_font = pygame.font.SysFont("Arial", 48)
        score_text = score_font.render(
            f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(
            center=(self.screen.get_width() / 2, 220))
        self.screen.blit(score_text, score_rect)

        # Label pour le nom
        label_font = pygame.font.SysFont("Arial", 36)
        label_text = label_font.render(
            "Enter your name:", True, (255, 255, 255))
        label_rect = label_text.get_rect(
            center=(self.screen.get_width() / 2, 320))
        self.screen.blit(label_text, label_rect)

        # Champ de saisie (rectangle + texte)
        input_box = pygame.Rect(
            self.screen.get_width() / 2 - 150,
            380,
            300,
            50
        )
        pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)

        name_text = label_font.render(self.input_name,
                                      True, (255, 255, 255))
        name_rect = name_text.get_rect(center=input_box.center)
        self.screen.blit(name_text, name_rect)

        info_font = pygame.font.SysFont("Arial", 24)
        info_text = info_font.render(
            "Press ENTER to save", True, (200, 200, 200))
        info_rect = info_text.get_rect(
            center=(self.screen.get_width() - 150,
                    self.screen.get_height() - 30))
        self.screen.blit(info_text, info_rect)
