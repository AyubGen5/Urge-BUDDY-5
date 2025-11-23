# Local CLI usage: Log urges with timestamps

This project includes a tiny CLI script to log urges locally to `data/urges.jsonl`.

Quick examples:

- Log non-interactively:

```sh
python log_urge.py "I want to smoke" --intensity 7 --note "after coffee"
```

- Interactive prompt:

```sh
python log_urge.py
# then enter the urge when prompted
```

Each entry is appended as a single JSON object per line (JSON Lines). Example entry:

```json
{"timestamp":"2025-11-23T12:34:56Z","urge":"I want to smoke","intensity":7,"note":"after coffee"}
```

View the log file with `tail` or `jq`:

```sh
tail -n 50 data/urges.jsonl
jq . data/urges.jsonl | less
```

Export to CSV:

```sh
python export_csv.py
```

Run local web UI (requires `Flask`):

```sh
pip install -r requirements.txt
python server.py
# open http://127.0.0.1:5000/
```
