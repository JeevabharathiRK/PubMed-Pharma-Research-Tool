import pytest
import sys
from pathlib import Path
from pubmed_papers.main import main as start_main

def test_no_flag(monkeypatch, capsys):
    """
    Test that human-readable output is printed when no -f flag is provided.
    """
    test_args = ["get-papers-list", "micrornas genomics biogenesis mechanism inc"]
    monkeypatch.setattr(sys, "argv", test_args)
    try:
        start_main()
    except SystemExit:
        pass  # Acceptable if main() calls sys.exit()
    captured = capsys.readouterr()
    assert "Matched papers" in captured.out or "No matched papers found." in captured.out

def test_file_flag(monkeypatch, tmp_path):
    """
    Test that the CLI runs and creates a CSV file for a simple query.
    """
    test_csv = tmp_path / "results.csv"
    test_args = [
        "get-papers-list",
        "micrornas genomics biogenesis mechanism inc",
        "-f", str(test_csv)
    ]
    monkeypatch.setattr(sys, "argv", test_args)
    try:
        start_main()
    except SystemExit as e:
        # main() may call sys.exit(), which raises SystemExit
        assert e.code == 0 or e.code is None

    assert test_csv.exists()
    content = test_csv.read_text(encoding="utf-8")
    assert "PubmedID" in content
    assert "Title" in content

def test_debug_flag(monkeypatch, capsys):
    """
    Test that debug output is printed when -d is used.
    """
    test_args = [
        "get-papers-list",
        "micrornas genomics biogenesis mechanism inc",
        "-d"
    ]
    monkeypatch.setattr(sys, "argv", test_args)
    try:
        start_main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "[DEBUG]" in captured.err or "[DEBUG]" in captured.out

def test_help_flag(monkeypatch, capsys):
    """
    Test that help output is printed when -h is used.
    """
    test_args = ["get-papers-list", "-h"]
    monkeypatch.setattr(sys, "argv", test_args)
    try:
        start_main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "usage:" in captured.out or "usage:" in captured.err
    assert "get-papers-list" in captured.out or "get-papers-list" in captured.err