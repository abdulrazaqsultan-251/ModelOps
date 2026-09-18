from modelops.validator import validate_model


def valid_model():
    return {
        "name": "customer_classifier",
        "version": "1.2.0",
        "framework": "pytorch",
        "architecture": "resnet18",
        "accuracy": 0.94,
        "input_shape": [3, 224, 224],
    }


def test_valid_model():
    assert validate_model(valid_model()) == []


def test_invalid_accuracy():
    model = valid_model()
    model["accuracy"] = 1.5

    errors = validate_model(model)

    assert "accuracy must be between 0 and 1." in errors


def test_missing_required_field():
    model = valid_model()
    del model["framework"]

    errors = validate_model(model)

    assert any("Missing fields" in error for error in errors)
