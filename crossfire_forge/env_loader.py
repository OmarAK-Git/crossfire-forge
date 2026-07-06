"""Load local `.env` for CLI and live trial scripts (gitignored; never committed)."""

from __future__ import annotations

from pathlib import Path


def load_local_dotenv() -> None:
    """Load repo-root `.env` if present. No-op when file or python-dotenv is missing."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    root = Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env", override=False)
