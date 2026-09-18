# ModelOps

ModelOps is a Python CLI for inspecting, validating, and comparing AI model metadata stored as JSON. The project helps engineers quickly check whether a model definition is complete, consistent with expected conventions, and comparable to another model version.

## Why this project exists

AI and ML teams often work with metadata such as model name, version, architecture, framework, accuracy, and input shape. That metadata is easy to lose track of as models evolve across experiments, release candidates, and production deployments.

ModelOps provides a lightweight command-line workflow for:

- reading model metadata from JSON files
- validating required fields and basic constraints
- comparing metadata between versions
- surfacing simple, readable output in a terminal

This project is intentionally compact, deterministic, and easy to extend without introducing a larger platform or service layer.

## Key features

- Inspect a model metadata file and print each field/value pair
- Validate required model properties and value ranges
- Compare model metadata across two JSON files
- Use a simple argparse-based CLI with predictable exit codes
- Keep the implementation in a standard Python src/ package layout
- Run tests with pytest in a CI workflow

## Current CLI commands

The project exposes three commands through the `modelops` entry point defined in [pyproject.toml](pyproject.toml):

| Command | Purpose |
| --- | --- |
| `modelops inspect <path>` | Load a model metadata JSON file and print its contents. |
| `modelops validate <path>` | Validate the file and report any missing or invalid metadata. |
| `modelops compare <first> <second>` | Compare two model metadata files and print the resulting field comparison. |

## Example model metadata

The repository includes example model metadata in [data/model_v1.json](data/model_v1.json) and [data/model_v2.json](data/model_v2.json). A typical model payload looks like this:

```json
{
  "name": "customer_classifier",
  "version": "1.2.0",
  "framework": "pytorch",
  "architecture": "resnet18",
  "accuracy": 0.94,
  "input_shape": [3, 224, 224]
}
```

This is the schema the project currently validates. The required fields are:

- `name`
- `version`
- `framework`
- `architecture`
- `accuracy`
- `input_shape`

## Installation

This project targets Python 3.11 or later as defined in [pyproject.toml](pyproject.toml).

From the repository root:

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

## Virtual environment setup

On Windows PowerShell, a common setup is:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

After installation, the `modelops` command is available in the activated environment.

## Running the CLI

### Inspect a model

```bash
modelops inspect data/model_v1.json
```

Expected behavior: the command loads the JSON file and prints each key/value pair in the object order defined by the file. For example, the output will include entries such as `name: customer_classifier`, `version: 1.2.0`, and `accuracy: 0.94`.

### Validate a model

```bash
modelops validate data/model_v1.json
```

Expected behavior: the CLI loads the file, checks the required metadata fields, then prints either:

- `VALID: <path>` when the metadata passes validation
- `INVALID: <path>` followed by one or more validation messages when problems are found

Validation checks in the current implementation include:

- required metadata fields are present
- `accuracy` is between `0` and `1` inclusive
- `input_shape` is a non-empty list of positive integers

### Compare two model versions

```bash
modelops compare data/model_v1.json data/model_v2.json
```

Expected behavior: the command loads both files and prints a comparison of the fields that the project compares currently:

- `name`
- `version`
- `accuracy`
- `framework`
- `architecture`

The output is formatted as `field: old_value -> new_value`.

## Running tests

The repository uses pytest. From the project root:

```bash
pytest -q
```

This runs the suite in the [tests](tests) directory. The GitHub Actions workflow defined in [.github/workflows/tests.yml](.github/workflows/tests.yml) installs dependencies and runs the same command on pushes and pull requests targeting `main`.

## Project structure

```text
ModelOps/
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
│       └── tests.yml
├── data/
│   ├── model_v1.json
│   ├── model_v2.json
│   └── sample.csv
├── logs/
├── screenshots/
├── src/
│   └── modelops/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── cli.py
│       ├── exceptions.py
│       ├── loader.py
│       ├── reporter.py
│       └── validator.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_cli.py
│   ├── test_loader.py
│   ├── test_reporter.py
│   └── test_validator.py
├── .gitignore
├── CHANGELOG.md
├── NOTES.md
├── README.md
├── pyproject.toml
└── requirements-dev.txt
```

## Architecture and components

The implementation is intentionally small and modular:

- [src/modelops/cli.py](src/modelops/cli.py): defines the CLI with argparse and dispatches to the correct handler for inspect, validate, and compare commands.
- [src/modelops/loader.py](src/modelops/loader.py): loads a JSON file from disk and raises `ModelLoadError` when the file is missing, invalid, or not an object.
- [src/modelops/validator.py](src/modelops/validator.py): checks required metadata keys and validates numeric constraints such as accuracy range and `input_shape` format.
- [src/modelops/analyzer.py](src/modelops/analyzer.py): compares core model fields between two metadata dictionaries.
- [src/modelops/reporter.py](src/modelops/reporter.py): formats validation and comparison output for terminal display.
- [src/modelops/exceptions.py](src/modelops/exceptions.py): defines the custom exception types used for loader and validation failures.

This creates a clean separation between loading data, validating it, comparing it, and formatting the output.

## Validation behavior

The validation logic currently enforces the following rules:

- all required fields must be present
- `accuracy` must be within the inclusive range `0` to `1`
- `input_shape` must be a non-empty list
- every entry in `input_shape` must be a positive integer

A model is considered invalid when any of these checks fail. The validation function returns a list of human-readable messages, and the CLI prints them in a readable format.

## Error handling

The project uses simple, explicit exceptions for operational failures:

- `ModelLoadError` is raised when a model file cannot be found, cannot be parsed as JSON, or is not a JSON object.
- `ModelValidationError` is defined for validation failures but is not used directly by the current CLI entrypoint flow.

The CLI returns exit code `1` for validation errors in the `validate` command and `0` otherwise. Missing or malformed data files raise load errors instead of being silently accepted.

## Git and GitHub workflow

The repository follows a straightforward workflow typical of a small Python project:

1. Work from a feature branch or focused task branch.
2. Inspect the existing code and tests before editing.
3. Make the smallest change necessary to address the requirement.
4. Run the relevant tests and then the full pytest suite.
5. Review the diff before finishing.
6. Open a pull request against `main`.

This matches the guidance in [.github/copilot-instructions.md](.github/copilot-instructions.md) and the CI setup in [.github/workflows/tests.yml](.github/workflows/tests.yml).

## Pull request workflow

When submitting changes:

- keep the scope narrow and aligned to the task
- update or add tests when behavior changes
- confirm the code remains consistent with the repository’s src/ layout and Python 3.11+ requirement
- verify the PR passes the GitHub Actions test workflow before merging

The project is intentionally small, so the recommended review approach is to keep changes readable, focused, and easy to validate.

## GitHub Actions CI

The test workflow in [.github/workflows/tests.yml](.github/workflows/tests.yml) runs on pushes and pull requests to `main` and performs the following steps:

- checks out the repository
- sets up Python 3.11
- installs dependencies from [requirements-dev.txt](requirements-dev.txt)
- installs the package in editable mode with `pip install -e .`
- runs `pytest -q`

This ensures the CLI behavior remains validated in CI as the repository evolves.

## Vibe Coding development workflow

The repository’s guidance in [.github/copilot-instructions.md](.github/copilot-instructions.md) describes a lightweight, review-first development flow:

1. Understand the requested change.
2. Inspect the existing code before editing.
3. Make the smallest focused change.
4. Review the diff.
5. Run the relevant tests.
6. Run the full test suite before committing.
7. Use conventional commit messages.

The project also emphasizes that agent-generated code should be reviewed closely to ensure it follows the repository constraints and does not add unnecessary scope.

## Current project status

ModelOps is a compact, early-stage Python CLI for metadata inspection and validation. It is suitable for learning, experimentation, and portfolio demonstration, and it currently focuses on a JSON-driven workflow for model metadata rather than a full model registry, API service, or deployment platform.

The package version in [pyproject.toml](pyproject.toml) is `0.1.0`, which indicates that the project is in an initial development phase.

## Contributing

Contributions are welcome when they remain consistent with the project’s current scope:

- keep the CLI behavior simple and deterministic
- avoid adding secrets, credentials, or private files
- use the existing src/ layout and pytest conventions
- prefer focused changes backed by tests

## Notes

The repository contains sample data and screenshots, but the actual CLI implementation is intentionally limited to file-based JSON metadata inspection, validation, and comparison. It does not provide a web UI, database, or deployment system.
