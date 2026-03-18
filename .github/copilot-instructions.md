# Project Guidelines

## Code Style
- Target Python 3.8+ (source of truth: pyproject.toml).
- Keep CLI orchestration in src/folderize/core.py and custom error types in src/folderize/exceptions.py.
- Prefer raising existing custom exceptions instead of generic exceptions for user-facing CLI failures.
- Keep dependencies minimal; use standard library modules unless an external package is clearly justified.

## Architecture
- The CLI entry point is `folderize`, mapped to `folderize.core:main`.
- `main()` coordinates argument parsing, placeholder substitution, YAML parsing, and filesystem creation.
- `create_from_yaml()` is the recursive filesystem writer; keep traversal behavior deterministic and side effects local to the selected working directory.
- YAML placeholder substitution uses `<KEY>` syntax and `-D/--define KEY=VALUE` values.

## Build and Test
- Install in editable mode for development: `pip install -e .`
- Build a distributable package: `pip install build && python -m build`
- Run CLI locally:
  - `folderize STRUCTURE.yaml`
  - `folderize STRUCTURE.yaml -D project=my_project`
- Because the CLI writes files/directories immediately, run verification commands in a temporary directory unless intentional.
- There is currently no automated test suite under test/; if adding tests, place them in test/ and document the exact test command in this file.

## Conventions
- Default input file is `STRUCTURE.yaml` when no positional file argument is provided.
- The expected structure file format is YAML (not Markdown).
- Keep README and pyproject.toml behavior in sync; if they disagree, align docs with the implemented CLI behavior.
- Release publishing is tag-driven via `.github/workflows/python-publish.yml`.
