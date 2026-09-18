from modelops.cli import build_parser, main


def test_cli_parser_inspect():
    parser = build_parser()

    args = parser.parse_args(["inspect", "model.json"])

    assert args.command == "inspect"
    assert args.path == "model.json"


def test_cli_parser_compare():
    parser = build_parser()

    args = parser.parse_args(["compare", "a.json", "b.json"])

    assert args.command == "compare"
    assert args.first == "a.json"
    assert args.second == "b.json"


def test_cli_handles_missing_file(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["modelops", "inspect", "missing.json"],
    )

    result = main()

    captured = capsys.readouterr()

    assert result == 1
    assert "error:" in captured.err
    assert "Model file not found" in captured.err
