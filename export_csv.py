#!/usr/bin/env python3
"""Export `data/urges.jsonl` to CSV (`data/urges.csv`).

Usage:
  python export_csv.py       # writes data/urges.csv
  python export_csv.py --input other.jsonl --output out.csv
"""

import argparse
import csv
import json
import os


def parse_args():
    p = argparse.ArgumentParser(description="Export urges JSONL to CSV")
    p.add_argument("--input", "-i", default="data/urges.jsonl")
    p.add_argument("--output", "-o", default="data/urges.csv")
    return p.parse_args()


def read_jsonl(path):
    if not os.path.exists(path):
        print(f"No input file: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                print("Skipping invalid JSON line:", line)


def main():
    args = parse_args()
    rows = list(read_jsonl(args.input))
    if not rows:
        print("No rows to export.")
        return 1

    # Collect fieldnames from all rows
    fieldnames = ["timestamp", "urge", "intensity", "note"]
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})
    print(f"Wrote {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
