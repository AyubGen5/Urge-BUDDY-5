#!/usr/bin/env python3
"""Validate and optionally repair `data/urges.jsonl`.

Usage:
  python validate_logs.py          # report issues
  python validate_logs.py --fix    # drop invalid lines and rewrite file

Validation rules:
- `timestamp` must be present (ISO-like string)
- `urge` must be non-empty string
- `intensity` if present must be int 1..10
"""

import argparse
import json
import os
import re
from typing import Tuple

LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "urges.jsonl")

ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def load_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f if l.strip()]


def validate_obj(obj) -> Tuple[bool, str]:
    if not isinstance(obj, dict):
        return False, "not an object"
    ts = obj.get("timestamp")
    if not ts or not isinstance(ts, str) or not ISO_RE.match(ts):
        return False, "invalid or missing timestamp"
    urge = obj.get("urge")
    if not urge or not isinstance(urge, str) or not urge.strip():
        return False, "missing or empty urge"
    if "intensity" in obj:
        try:
            v = int(obj["intensity"])
        except Exception:
            return False, "intensity not integer"
        if not (1 <= v <= 10):
            return False, "intensity out of range"
    return True, "ok"


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--file", "-f", default=LOG_PATH)
    p.add_argument("--fix", action="store_true", help="Rewrite file dropping invalid lines")
    args = p.parse_args(argv)

    lines = load_lines(args.file)
    if not lines:
        print("No log file or empty file:", args.file)
        return 0

    valid = []
    invalid = []
    for i, line in enumerate(lines, start=1):
        try:
            obj = json.loads(line)
        except Exception:
            invalid.append((i, line, "invalid json"))
            continue
        ok, reason = validate_obj(obj)
        if ok:
            valid.append(line)
        else:
            invalid.append((i, line, reason))

    print(f"Read {len(lines)} lines: {len(valid)} valid, {len(invalid)} invalid")
    if invalid:
        print("Invalid entries:")
        for i, line, reason in invalid[:50]:
            print(f"  line {i}: {reason}")

    if args.fix and invalid:
        bak = args.file + ".bak"
        os.rename(args.file, bak)
        with open(args.file, "w", encoding="utf-8") as f:
            for l in valid:
                f.write(l + "\n")
        print(f"Rewrote {args.file} with {len(valid)} valid lines, original saved as {bak}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
