from json import JSONDecodeError, dump, load


class HighscoreManager:
    """Load, validate and persist the top-10 highscore table."""

    def is_valid_name(self, name: str) -> bool:
        """Check if the name is 1-10 alphanumeric/space characters."""
        return 0 < len(name) <= 10 and all(
            char.isalnum() or char.isspace() for char in name
        )

    def is_valid_score(self, score: int) -> bool:
        """Check if the score is a non-negative integer."""
        return (
            isinstance(score, int)
            and not isinstance(score, bool)
            and score >= 0
        )

    def load_highscores(self, file_path: str) -> dict[str, int]:
        """Load the highscores, ignoring missing or invalid entries."""
        try:
            with open(file_path, "r") as file:
                highscores = load(file)
        except (FileNotFoundError, JSONDecodeError) as error:
            print(f"Error loading highscores: {error}")
            return {}
        if not isinstance(highscores, dict):
            return {}
        return {
            name: score
            for name, score in highscores.items()
            if self.is_valid_name(name) and self.is_valid_score(score)
        }

    def save_highscores(self, file_path: str,
                        highscores: dict[str, int]) -> None:
        """Merge scores into the existing top-10 and persist the result.

        Invalid entries are ignored; a name keeps its best score.
        """
        scores = self.load_highscores(file_path)
        for name, score in highscores.items():
            if not self.is_valid_name(name) or not self.is_valid_score(score):
                continue
            if name not in scores or score > scores[name]:
                scores[name] = score
        if len(scores) > 10:
            scores = dict(
                sorted(scores.items(),
                       key=lambda item: item[1], reverse=True)[:10]
            )
        with open(file_path, "w") as file:
            dump(scores, file)
