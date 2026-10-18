from json import loads, JSONDecodeError
from pydantic import BaseModel, Field, ValidationError


class LevelConfig(BaseModel):
    """Configuration for a game level."""

    width: int = Field(ge=14, le=20)
    height: int = Field(ge=14, le=15)


def default_levels() -> list[LevelConfig]:
    """Generate and return the default level configurations for the game."""
    return [
        LevelConfig(width=14, height=14),
        LevelConfig(width=14, height=14),
        LevelConfig(width=14, height=14),
        LevelConfig(width=14, height=14),
        LevelConfig(width=14, height=14),
        LevelConfig(width=15, height=15),
        LevelConfig(width=15, height=15),
        LevelConfig(width=15, height=15),
        LevelConfig(width=15, height=15),
        LevelConfig(width=15, height=15),
    ]


class GameConfig(BaseModel):
    """Main game configuration model."""

    highscore_filename: str = "highscore.json"
    lives: int = Field(default=3, ge=1)
    points_per_pacgum: int = Field(default=10, ge=1)
    points_per_super_pacgum: int = Field(default=50, ge=1)
    points_per_ghost: int = Field(default=200, ge=1)
    seed: int = Field(default=42, ge=1)
    level_max_time: int = Field(default=90, ge=1)
    pacgum: int = Field(default=42, ge=1)
    level: list[LevelConfig] = Field(default_factory=default_levels)


def strip_json_comments(text: str) -> str:
    """Remove comments from a JSON string."""
    result = str()
    i = 0
    length = len(text)

    while i < length:
        if text[i] == "#":
            while i < length and text[i] != "\n":
                i += 1

        elif text[i] == "/" and i + 1 < length:
            if text[i + 1] == "/":
                i += 2
                while i < length and text[i] != "\n":
                    i += 1

            elif text[i + 1] == "*":
                i += 2
                while i + 1 < length:
                    if text[i] == "*" and text[i + 1] == "/":
                        i += 2
                        break
                    i += 1

        else:
            result += text[i]
            i += 1
    return result


def get_config(fichier: str) -> GameConfig:
    """Load game configuration from a JSON file with comment support.

    Attempts to load and parse a configuration file. If the file doesn't exist,
    is invalid, or fails validation, returns a default GameConfig instance.
    """
    try:
        with open(fichier, "r") as fd:
            content = fd.read()
        data = strip_json_comments(content)
        return GameConfig(**loads(data))

    except OSError as msg:
        print(f"Erreur d'ouverture du fichier : {msg}")
    except ValidationError as msg:
        print(f"Valeurs de configuration invalides : {msg}")
    except JSONDecodeError as msg:
        print(f"Fichier config invalid :{msg}")

    print("Chargement de la configuration par défaut.")
    return GameConfig()
