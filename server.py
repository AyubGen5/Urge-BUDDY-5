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


@APP.route("/download/csv")
def download_csv():
  # Generate CSV in-memory from current JSONL logs and stream as attachment
  import io
  import csv

  rows = read_jsonl(LOG_PATH)
  fieldnames = ["timestamp", "urge", "intensity", "note"]
  buf = io.StringIO()
  writer = csv.DictWriter(buf, fieldnames=fieldnames)
  writer.writeheader()
  for r in rows:
    writer.writerow({k: r.get(k, "") for k in fieldnames})
  csv_data = buf.getvalue()
  return APP.response_class(csv_data, mimetype='text/csv', headers={
    'Content-Disposition': 'attachment; filename="urges.csv"'
  })


@APP.route("/")
def index():
    html = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Urge-BUDDY - Logs</title>
        <style>body{font-family: Arial; padding:20px;} table{border-collapse:collapse;} td,th{border:1px solid #ccc;padding:6px;}</style>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      </head>
      <body>
        <h1>Urge Logs</h1>
        <p>Loads `data/urges.jsonl` and shows recent entries.</p>

        <div style="margin-bottom:12px">
          <label>Min intensity: <select id="minIntensity"><option value="0">Any</option>
            <option>1</option><option>2</option><option>3</option><option>4</option><option>5</option>
            <option>6</option><option>7</option><option>8</option><option>9</option><option>10</option>
          </select></label>
          <label style="margin-left:12px">Search: <input id="q"/></label>
          <button id="refresh">Refresh</button>
        </div>

        <canvas id="chart" width="600" height="200" style="max-width:700px"></canvas>

        <table id="tbl" style="margin-top:12px"><thead><tr><th>Timestamp</th><th>Urge</th><th>Intensity</th><th>Note</th></tr></thead><tbody></tbody></table>
        <script>
          let chart = null;
          async function load(){
            const res = await fetch('/api/urges');
            const data = await res.json();
            renderTable(data);
            renderChart(data);
          }

          function renderTable(data){
            const tbody = document.querySelector('#tbl tbody'); tbody.innerHTML='';
            const minI = parseInt(document.getElementById('minIntensity').value || '0', 10);
            const q = document.getElementById('q').value.toLowerCase();
            data.slice().reverse().forEach(row => {
              const intensity = row.intensity || '';
              if(minI && (!intensity || intensity < minI)) return;
              if(q && !(row.urge||'').toLowerCase().includes(q) && !(row.note||'').toLowerCase().includes(q)) return;
              const tr = document.createElement('tr');
              ['timestamp','urge','intensity','note'].forEach(k=>{
                const td = document.createElement('td');
                td.textContent = row[k] ?? '';
                tr.appendChild(td);
              });
              tbody.appendChild(tr);
            });
          }

          function renderChart(data){
            const counts = Array(11).fill(0);
            data.forEach(r => { if(r.intensity) counts[r.intensity]++; });
            const labels = [...Array(10)].map((_,i)=>String(i+1));
            const values = labels.map((l,i)=>counts[i+1]);
            const ctx = document.getElementById('chart').getContext('2d');
            if(chart) chart.destroy();
            chart = new Chart(ctx, {type:'bar', data:{labels, datasets:[{label:'Intensity count', data:values, backgroundColor:'rgba(54,162,235,0.6)'}]}});
          }

          document.getElementById('refresh').addEventListener('click', load);
          document.getElementById('minIntensity').addEventListener('change', load);
          document.getElementById('q').addEventListener('input', ()=>{ setTimeout(load,200); });

          load();
        </script>
      </body>
    </html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    APP.run(debug=True)
