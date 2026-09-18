class ModelOpsError(Exception):
    """Base exception for ModelOps."""


class ModelLoadError(ModelOpsError):
    """Raised when model metadata cannot be loaded."""


class ModelValidationError(ModelOpsError):
    """Raised when model metadata is invalid."""
