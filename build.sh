#!/bin/bash

set -e

make install

rm -rf build dist

uv run python -m PyInstaller \
    --onedir \
    --windowed \
    --name Pacman \
    --paths . \
    --add-data "config.json:." \
    --add-data "highscore.json:." \
    --add-data "INSTRUCTIONS.txt:." \
    src/__main__.py

echo "Game package completed."
