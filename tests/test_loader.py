import json

import pytest

from modelops.loader import load_model
from modelops.exceptions import ModelLoadError


def test_load_valid_model(tmp_path):
    path = tmp_path / "model.json"
    path.write_text(json.dumps({"name": "demo"}), encoding="utf-8")

    result = load_model(str(path))

    assert result["name"] == "demo"


def test_load_missing_model():
    with pytest.raises(ModelLoadError):
        load_model("missing.json")


def test_load_invalid_json(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(ModelLoadError):
        load_model(str(path))
