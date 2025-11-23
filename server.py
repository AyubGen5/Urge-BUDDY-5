"""Tiny Flask server to view urges and serve a minimal web UI.

Run with: `python server.py` and open http://127.0.0.1:5000/
"""
from flask import Flask, jsonify, send_from_directory, render_template_string
import json
import os

APP = Flask(__name__, static_folder="static", template_folder="static")

LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "urges.jsonl")


def read_jsonl(path):
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except Exception:
                continue
    return entries


@APP.route("/api/urges")
def api_urges():
    return jsonify(read_jsonl(LOG_PATH))


@APP.route("/")
def index():
    html = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Urge-BUDDY - Logs</title>
        <style>body{font-family: Arial; padding:20px;} table{border-collapse:collapse;} td,th{border:1px solid #ccc;padding:6px;}</style>
      </head>
      <body>
        <h1>Urge Logs</h1>
        <p>Loads `data/urges.jsonl` and shows recent entries.</p>
        <table id="tbl"><thead><tr><th>Timestamp</th><th>Urge</th><th>Intensity</th><th>Note</th></tr></thead><tbody></tbody></table>
        <script>
          async function load(){
            const res = await fetch('/api/urges');
            const data = await res.json();
            const tbody = document.querySelector('#tbl tbody');
            data.slice().reverse().forEach(row => {
              const tr = document.createElement('tr');
              ['timestamp','urge','intensity','note'].forEach(k=>{
                const td = document.createElement('td');
                td.textContent = row[k] ?? '';
                tr.appendChild(td);
              });
              tbody.appendChild(tr);
            });
          }
          load();
        </script>
      </body>
    </html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    APP.run(debug=True)
