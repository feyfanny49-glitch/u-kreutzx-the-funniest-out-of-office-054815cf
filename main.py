#!/usr/bin/env python3
"""Write the single judged out-of-office line to /output/entry.txt.

The whole artifact is one line of UTF-8 text, 1..140 characters, with no
trailing newline. The write is atomic: bytes go to a temp file in the
output directory, are flushed and fsynced, then os.replace puts them at
the artifact path. A readback verifies what the gate will read.
Standard library only; no network, no secrets, no files read elsewhere.
"""

import hashlib
import os
import sys
import tempfile

ENTRY_TEXT = "I'm out of office. I'll be in touch the moment I need something from you."
ARTIFACT_NAME = "entry.txt"
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def encoded_artifact(text: str) -> bytes:
    """Enforce the gate before any byte reaches /output."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text.startswith("\ufeff"):
        raise ValueError("entry must not carry a BOM")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if not 1 <= len(text) <= 140:
        raise ValueError(f"entry length {len(text)} outside 1..140")
    return text.encode("utf-8")


def write_atomically(directory: str, name: str, data: bytes) -> bytes:
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, name)
    fd, temp_path = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_path, 0o644)
        os.replace(temp_path, target)
    except BaseException:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass
        raise
    with open(target, "rb") as handle:
        written = handle.read()
    if written != data:
        raise OSError("artifact readback differs from the bytes written")
    return written


def main() -> int:
    data = encoded_artifact(ENTRY_TEXT)
    written = write_atomically(OUTPUT_DIR, ARTIFACT_NAME, data)
    print(
        f"{ARTIFACT_NAME}: {len(ENTRY_TEXT)} chars, {len(written)} bytes, "
        f"sha256 {hashlib.sha256(written).hexdigest()}, single line, no trailing newline"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
