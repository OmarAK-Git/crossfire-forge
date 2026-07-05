"""Minimal smoke tests for Phase 1 Task 1 skeleton."""

import httpx
import pydantic
import typer

import crossfire_forge
from crossfire_forge.cli import app


def test_package_version() -> None:
    assert crossfire_forge.__version__ == "0.1.0"


def test_dependencies_importable() -> None:
    assert pydantic.__version__.startswith("2.")
    assert isinstance(app, typer.Typer)
    assert httpx.__version__
