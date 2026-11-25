#!/usr/bin/env python3
"""One Line, One Chill — entrypoint.

Writes the entry's single sentence of horror to entry.txt in the output
directory. The gate accepts UTF-8 text of 1 to 200 characters, so the line
is written exactly, with no trailing newline.

Pure standard library: the grading sandbox has no third-party packages.
"""

import os
import sys

LINE = (
    "We heard the whole lake crack at once, and then, from under the ice, "
    "something knocked three times, politely, like it was asking to come up."
)


def output_candidates() -> list:
    """Directories to try for entry.txt, most preferred first."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append(os.path.join(os.getcwd(), "output"))
    return candidates


def check_gate(text: str) -> None:
    """Mirror the sealed gate: UTF-8 text of 1 to 200 characters, not blank."""
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry is {len(text)} characters, outside 1..200")
    if not text.strip():
        raise ValueError("entry is only white space")


def main() -> int:
    check_gate(LINE)
    errors = []
    for target_dir in output_candidates():
        path = os.path.join(target_dir, "entry.txt")
        try:
            os.makedirs(target_dir, exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(LINE)
            with open(path, "r", encoding="utf-8") as handle:
                written = handle.read()
            if written != LINE:
                raise IOError(f"read-back mismatch in {path}")
            return 0
        except OSError as exc:
            errors.append(f"{path}: {exc}")
    for message in errors:
        print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
