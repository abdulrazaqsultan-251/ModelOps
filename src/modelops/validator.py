from .exceptions import ModelValidationError

REQUIRED_FIELDS = {
    "name",
    "version",
    "framework",
    "architecture",
    "accuracy",
    "input_shape",
}


def validate_model(model: dict) -> list[str]:
    """Validate model metadata and return validation errors."""
    errors = []

    missing = REQUIRED_FIELDS - model.keys()
    if missing:
        errors.append(f"Missing fields: {', '.join(sorted(missing))}")

    accuracy = model.get("accuracy")
    if accuracy is not None and not 0 <= accuracy <= 1:
        errors.append("accuracy must be between 0 and 1.")

    input_shape = model.get("input_shape")
    if input_shape is not None:
        if not isinstance(input_shape, list) or not input_shape:
            errors.append("input_shape must be a non-empty list.")
        elif not all(isinstance(value, int) and value > 0 for value in input_shape):
            errors.append("input_shape values must be positive integers.")

    return errors


def ensure_valid(model: dict) -> None:
    """Raise an exception when metadata is invalid."""
    errors = validate_model(model)
    if errors:
        raise ModelValidationError("; ".join(errors))
