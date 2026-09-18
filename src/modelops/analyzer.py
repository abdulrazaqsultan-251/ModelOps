def compare_models(model_a: dict, model_b: dict) -> dict:
    """Compare two model metadata dictionaries."""
    return {
        "name": (model_a.get("name"), model_b.get("name")),
        "version": (model_a.get("version"), model_b.get("version")),
        "accuracy": (
            model_a.get("accuracy"),
            model_b.get("accuracy"),
        ),
        "framework": (
            model_a.get("framework"),
            model_b.get("framework"),
        ),
        "architecture": (
            model_a.get("architecture"),
            model_b.get("architecture"),
        ),
    }
