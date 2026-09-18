import argparse
import sys

from .analyzer import compare_models
from .exceptions import ModelOpsError
from .loader import load_model
from .reporter import format_comparison, format_validation
from .validator import validate_model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="modelops",
        description="Inspect, validate, and compare AI model metadata.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("path")

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("path")

    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("first")
    compare_parser.add_argument("second")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "inspect":
            model = load_model(args.path)
            for key, value in model.items():
                print(f"{key}: {value}")
            return 0

        if args.command == "validate":
            model = load_model(args.path)
            errors = validate_model(model)
            print(format_validation(args.path, errors))
            return 1 if errors else 0

        if args.command == "compare":
            first = load_model(args.first)
            second = load_model(args.second)
            comparison = compare_models(first, second)
            print(format_comparison(comparison))
            return 0

        return 0

    except ModelOpsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())