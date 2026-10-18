# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ LAYOUT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEFAULT			= \033[0m
GREEN			= \033[1;32m
CYAN			= \033[1;36m

ARGS			?= config.json

define ANIMATION
				@for frame in ⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏; do \
				printf "$$frame $(1)...\r"; \
				sleep 0.02; \
				done; \
				printf "\n"
endef


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ RULES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

install:
				$(call ANIMATION,Installing activity dependencies)
				@uv sync

run:
				@uv run python -m src $(ARGS)

package:
				@./build.sh

debug:
				@uv run python -m pdb -m src $(ARGS)

clean:
				$(call ANIMATION,Removing compiled files and caches)
				@rm -rf __pycache__ */__pycache__ .pytest_cache .mypy_cache

lint:
				@uv run flake8 src
				@uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
				@uv run flake8 src
				@uv run mypy src --strict

test:
				@uv run python -m pytest tests -v


help:
				@printf "Usage: make [target]\n"
				@printf "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
				@printf "$(CYAN)install$(DEFAULT)		- Install project dependencies\n"
				@printf "$(CYAN)run$(DEFAULT)		- Run the game (default config: config.json, use ARGS=\"<config_file>\" to override)\n"
				@printf "$(CYAN)package$(DEFAULT)		- Build the distributable Linux package\n"
				@printf "$(CYAN)debug$(DEFAULT)		- Run the game in debug mode (use ARGS=\"<config_file>\" to override)\n"
				@printf "$(CYAN)clean$(DEFAULT)		- Remove compiled Python files and caches\n"
				@printf "$(CYAN)lint$(DEFAULT)		- Run linter and type checker to ensure code quality\n"
				@printf "$(CYAN)lint-strict$(DEFAULT)	- Run linter and type checker with strict settings\n"
				@printf "$(CYAN)test$(DEFAULT)		- Run tests using pytest\n"
				@printf "$(CYAN)help$(DEFAULT)		- Show this help message\n"

.PHONY:			install run package debug clean lint lint-strict test help
