#!/usr/bin/env python3
"""Simple CLI to log urges with timestamps.

Appends JSON-lines to `data/urges.jsonl` with fields:
- timestamp: ISO 8601 UTC
- urge: the short description provided
- intensity: optional integer (1-10)
- note: optional longer note

Usage examples:
  python log_urge.py "I want to smoke" --intensity 7 --note "after coffee"
  python log_urge.py            # interactive prompt
"""

import argparse
import datetime
import json
import os
import sys


DEFAULT_DIR = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_FILE = os.path.join(DEFAULT_DIR, "urges.jsonl")


def iso_utc_now():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def append_entry(path, entry):
    ensure_dir(os.path.dirname(path))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def build_entry(urge, intensity=None, note=None):
    entry = {
        "timestamp": iso_utc_now(),
        "urge": urge,
    }
    if intensity is not None:
        try:
            intensity_val = int(intensity)
        except Exception:
            raise ValueError("Intensity must be an integer between 1 and 10")
        if not (1 <= intensity_val <= 10):
            raise ValueError("Intensity must be between 1 and 10")
        entry["intensity"] = intensity_val
    if note:
        entry["note"] = note
    return entry


def parse_args(argv):
    p = argparse.ArgumentParser(description="Log an urge with timestamp")
    p.add_argument("urge", nargs="?", help="Short description of the urge")
    p.add_argument("--intensity", "-i", type=int, help="Optional intensity 1-10")
    p.add_argument("--note", "-n", help="Optional longer note")
    p.add_argument("--file", "-f", default=DEFAULT_FILE, help="File to append logs to")
    return p.parse_args(argv)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    if not args.urge:
        try:
            args.urge = input("Describe the urge: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("No urge provided, exiting.")
            return 1

    if not args.urge:
        print("Empty urge — nothing logged.")
        return 1

    try:
        entry = build_entry(args.urge, args.intensity, args.note)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    append_entry(args.file, entry)
    print(f"Logged urge to {args.file}:")
    print(json.dumps(entry, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
