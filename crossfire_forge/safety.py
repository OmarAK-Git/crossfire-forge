"""Pre-prompt secret scanner (FR-2)."""

import logging
import tempfile
from collections.abc import Sequence
from pathlib import Path

from detect_secrets.core.secrets_collection import SecretsCollection
from detect_secrets.settings import default_settings

logger = logging.getLogger(__name__)

_GENERIC_ABORT_MESSAGE = "Run aborted: suspected secret in input."


class SafetyAbort(Exception):
    """Abort before model I/O when input may contain credentials."""

    def __init__(self, message: str = _GENERIC_ABORT_MESSAGE) -> None:
        super().__init__(message)


def _suspected_secrets(label: str, content: str) -> bool:
    """Return True when detect-secrets finds secret-like patterns in content."""
    secrets = SecretsCollection()
    with default_settings():
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=Path(label).suffix or ".md",
            delete=False,
        ) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            secrets.scan_file(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    for _ in secrets:
        return True
    return False


def scan_pre_prompt(
    *,
    epic_content: str,
    corpus: Sequence[tuple[str, str]] | None = None,
) -> None:
    """Scan epic and corpus content before any model call; abort on suspicion."""
    if _suspected_secrets("epic.md", epic_content):
        logger.warning("Pre-prompt safety scan aborted run due to suspected secret.")
        raise SafetyAbort()

    for path, content in corpus or ():
        if _suspected_secrets(path, content):
            logger.warning("Pre-prompt safety scan aborted run due to suspected secret.")
            raise SafetyAbort()
