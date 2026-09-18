import json
from pathlib import Path

from .exceptions import ModelLoadError


def load_model(path: str) -> dict:
    """Load model metadata from a JSON file."""
    file_path = Path(path)

    if not file_path.exists():
        raise ModelLoadError(f"Model file not found: {path}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ModelLoadError(f"Invalid JSON: {path}") from exc

    if not isinstance(data, dict):
        raise ModelLoadError("Model metadata must be a JSON object.")

    return data
