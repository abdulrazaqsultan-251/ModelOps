def format_validation(path: str, errors: list[str]) -> str:
    """Format validation results for the CLI."""
    if not errors:
        return f"VALID: {path}"

    lines = [f"INVALID: {path}"]
    lines.extend(f"- {error}" for error in errors)
    return "\n".join(lines)


def format_comparison(comparison: dict) -> str:
    """Format a model comparison."""
    lines = ["Model Comparison"]
    for field, values in comparison.items():
        lines.append(f"{field}: {values[0]} -> {values[1]}")
    return "\n".join(lines)
