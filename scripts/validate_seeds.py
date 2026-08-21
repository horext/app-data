#!/usr/bin/env python3
"""Validate the repository's canonical seed CSV format."""

import csv
import sys
from pathlib import Path


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    data = path.read_bytes()

    if data.startswith(b"\xef\xbb\xbf"):
        errors.append("must be UTF-8 without a BOM")
    if data and not data.endswith(b"\n"):
        errors.append("must end with a newline")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        return errors + [f"is not valid UTF-8: {error}"]

    try:
        with path.open(encoding="utf-8", newline="") as source:
            rows = list(csv.reader(source, delimiter=",", strict=True))
    except csv.Error as error:
        return errors + [f"is not valid comma-delimited CSV: {error}"]

    if not rows:
        return errors + ["must contain a header row"]

    header = rows[0]
    if len(header) == 1 and ";" in header[0]:
        errors.append("appears to use semicolons instead of commas")
    empty_headers = [str(index + 1) for index, name in enumerate(header) if not name.strip()]
    if empty_headers:
        errors.append(f"has unnamed columns: {', '.join(empty_headers)}")

    normalized = [name.strip().casefold() for name in header]
    duplicates = sorted({name for name in normalized if normalized.count(name) > 1})
    if duplicates:
        errors.append(f"has duplicate columns: {', '.join(duplicates)}")

    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            errors.append(f"row {row_number} has {len(row)} values; expected {len(header)}")

    return errors


def main() -> int:
    failures = 0
    for path in sorted(Path("seeds").glob("*.csv")):
        errors = validate(path)
        if errors:
            failures += 1
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"valid: {path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
