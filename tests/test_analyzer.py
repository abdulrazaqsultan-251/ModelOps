from modelops.analyzer import compare_models


def test_compare_models():
    first = {"name": "model", "version": "1.0", "accuracy": 0.90}
    second = {"name": "model", "version": "2.0", "accuracy": 0.95}

    result = compare_models(first, second)

    assert result["version"] == ("1.0", "2.0")
    assert result["accuracy"] == (0.90, 0.95)
