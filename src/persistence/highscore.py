from json import JSONDecodeError, load, dump
from typing import Protocol


class Config(Protocol):
    def is_valid_name(self, name: str) -> bool:
        pass

    def is_valid_score(self, score: int) -> bool:
        pass

    def load_highscores(self, file_path: str) -> dict[str, int]:
        pass

    def save_highscores(self, file_path: str,
                        highscores: dict[str, int]) -> None:
        pass


class HighscoreManager:
    def is_valid_name(self, name: str) -> bool:
        """
        Check if the provided name is valid.
        A valid name is a non-empty string that contains at most 10 characters,
        and only alphanumeric and spaces.
        """
        for char in name:
            if not (char.isalnum() or char.isspace()):
                return False
        return len(name) > 0 and len(name) <= 10

    def is_valid_score(self, score: int) -> bool:
        """
        Check if the provided score is valid.
        A valid score is a non-negative integer.
        """
        return (
            isinstance(score, int)
            and not isinstance(score, bool) and score >= 0
            )

    def load_highscores(self, file_path: str) -> dict[str, int]:
        """
        Load highscores from a JSON file.
        Returns a dictionary with the name as key and the score as value.
        If the file does not exist, is empty or invalid, returns
        an empty dictionary.
        """
        try:
            with open(file_path, 'r') as file:
                highscores = load(file)
        except (FileNotFoundError, JSONDecodeError) as e:
            print(f"Error loading highscores: {e}")
            return {}
        if not isinstance(highscores, dict):
            return {}
        valid_scores = {}
        for name, score in highscores.items():
            if self.is_valid_name(name) and self.is_valid_score(score):
                valid_scores[name] = score
        return valid_scores

    def save_highscores(self, file_path: str,
                        highscores: dict[str, int]) -> None:
        """
        Save highscores to a JSON file.
        Adds new scores to the existing highscores and
        keeps only the top 10 scores.
        If a name already exists, its score is updated only
        if the new score is higher.
        If any name or score is invalid, the function does nothing.
        """
        scores = self.load_highscores(file_path)
        for name, score in highscores.items():
            if not self.is_valid_name(name) or not self.is_valid_score(score):
                continue
            if name not in scores.keys() or score > scores[name]:
                scores[name] = score
        if len(scores) > 10:
            scores = dict(
                sorted(scores.items(),
                       key=lambda item: item[1], reverse=True)[:10]
                )
        with open(file_path, 'w') as file:
            dump(scores, file)
