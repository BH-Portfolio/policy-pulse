"""Sanity check that the project skeleton and test runner are wired up correctly."""
from pathlib import Path


def test_project_structure_exists():
    root = Path(__file__).parent.parent
    expected_dirs = ["src/ingestion", "src/processing", "src/agents", "src/storage", "src/eval", "src/api"]
    for d in expected_dirs:
        assert (root / d).is_dir(), f"Missing expected directory: {d}"


def test_src_is_importable():
    import src  # noqa: F401
    