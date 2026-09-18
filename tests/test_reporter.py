from modelops.reporter import format_validation, format_comparison


def test_format_valid_validation():
    result = format_validation("model.json", [])

    assert result == "VALID: model.json"


def test_format_invalid_validation():
    result = format_validation("model.json", ["bad accuracy"])

    assert "INVALID: model.json" in result
    assert "- bad accuracy" in result


def test_format_comparison():
    result = format_comparison(
        {"accuracy": (0.94, 0.96), "version": ("1.2.0", "1.3.0")}
    )

    assert "accuracy: 0.94 -> 0.96" in result
