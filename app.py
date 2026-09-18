import json
from pathlib import Path

from flask import Flask, jsonify, request, render_template_string
from qiskit.providers.fake_provider import GenericBackendV2

from src.analyzer import TranspilationAnalyzer
from src.benchmarks import build_ghz_circuit, build_qft_circuit

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Quantum Transpilation Analyzer</title>
    <style>
      :root {
        --bg: #0b1020;
        --panel: #121a2b;
        --panel-alt: #1a2338;
        --accent: #7c9cff;
        --accent-2: #6ee7b7;
        --text: #e8edf8;
        --muted: #a7b0c8;
        --border: rgba(255,255,255,0.08);
      }

      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(180deg, #0b1020 0%, #101827 100%);
        color: var(--text);
      }
      .container {
        max-width: 1100px;
        margin: 0 auto;
        padding: 40px 20px 60px;
      }
      .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        margin-bottom: 32px;
      }
      h1 {
        margin: 0;
        font-size: clamp(2rem, 4vw, 3rem);
      }
      .badge {
        background: rgba(124, 156, 255, 0.12);
        color: var(--accent-2);
        border: 1px solid var(--border);
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 0.82rem;
        letter-spacing: 0.04em;
      }
      .panel {
        background: rgba(18, 26, 43, 0.9);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
      }
      .grid {
        display: grid;
        grid-template-columns: 1.1fr 1.4fr;
        gap: 24px;
      }
      label {
        display: block;
        margin-bottom: 8px;
        color: var(--muted);
        font-size: 0.95rem;
      }
      select, input, button {
        width: 100%;
        padding: 12px 14px;
        border-radius: 10px;
        border: 1px solid var(--border);
        background: var(--panel-alt);
        color: var(--text);
        font-size: 1rem;
      }
      button {
        cursor: pointer;
        background: linear-gradient(135deg, var(--accent), #98a9ff);
        color: #091225;
        font-weight: 700;
        border: none;
        transition: transform 0.15s ease;
      }
      button:hover { transform: translateY(-1px); }
      .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
      .field { margin-bottom: 18px; }
      .result-box {
        margin-top: 24px;
        background: rgba(16, 24, 39, 0.85);
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
      }
      table {
        width: 100%;
        border-collapse: collapse;
      }
      th, td {
        padding: 12px 14px;
        text-align: left;
        border-bottom: 1px solid var(--border);
      }
      th {
        background: rgba(124, 156, 255, 0.08);
      }
      .muted { color: var(--muted); }
      .status {
        margin-top: 18px;
        padding: 12px 14px;
        border-radius: 10px;
        background: rgba(110, 231, 183, 0.08);
        border: 1px solid rgba(110, 231, 183, 0.2);
        color: var(--accent-2);
        display: none;
      }
      .status.visible { display: block; }
      @media (max-width: 780px) {
        .grid, .row { grid-template-columns: 1fr; }
        .header { flex-direction: column; align-items: flex-start; }
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>Quantum Transpilation Analyzer</h1>
        <div class="badge">Online Benchmark Tool</div>
      </div>

      <div class="grid">
        <section class="panel">
          <h2>Run a benchmark</h2>
          <div class="field">
            <label for="benchmark">Circuit type</label>
            <select id="benchmark">
              <option value="ghz">GHZ</option>
              <option value="qft">QFT</option>
            </select>
          </div>

          <div class="row">
            <div class="field">
              <label for="qubits">Qubits</label>
              <input id="qubits" type="number" min="2" max="12" value="5" />
            </div>
            <div class="field">
              <label for="backend">Backend size</label>
              <input id="backend" type="number" min="2" max="20" value="7" />
            </div>
          </div>

          <button id="runBtn" type="button">Analyze circuit</button>
          <div id="status" class="status"></div>
        </section>

        <section class="panel">
          <h2>Performance summary</h2>
          <div class="muted">Optimization levels 0 through 3 compare circuit depth and 2-qubit gate counts.</div>
          <div class="result-box">
            <table>
              <thead>
                <tr>
                  <th>Level</th>
                  <th>Depth</th>
                  <th>2Q Gates</th>
                  <th>SWAP</th>
                </tr>
              </thead>
              <tbody id="resultsBody">
                <tr><td colspan="4" class="muted">No data generated yet.</td></tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>

    <script>
      const runBtn = document.getElementById('runBtn');
      const status = document.getElementById('status');
      const resultsBody = document.getElementById('resultsBody');

      const renderResults = (results) => {
        resultsBody.innerHTML = results.map(r => `
          <tr>
            <td>${r.optimization_level}</td>
            <td>${r.depth}</td>
            <td>${r.two_qubit_gates}</td>
            <td>${r.swap_gates}</td>
          </tr>
        `).join('');
      };

      runBtn.addEventListener('click', async () => {
        const payload = {
          benchmark: document.getElementById('benchmark').value,
          qubits: Number(document.getElementById('qubits').value),
          backend_qubits: Number(document.getElementById('backend').value),
        };

        status.textContent = 'Running benchmark...';
        status.classList.add('visible');

        try {
          const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });

          const data = await response.json();
          if (!response.ok) throw new Error(data.error || 'Request failed');

          renderResults(data.results);
          status.textContent = `${data.benchmark} benchmark completed for ${data.qubits} qubits.`;
          status.classList.add('visible');
        } catch (error) {
          status.textContent = error.message;
          status.classList.add('visible');
        }
      });
    </script>
  </body>
</html>
"""


def _build_benchmark(name: str, num_qubits: int):
    if name == 'ghz':
        return build_ghz_circuit(num_qubits)
    if name == 'qft':
        return build_qft_circuit(num_qubits)
    raise ValueError(f'Unsupported benchmark: {name}')


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        payload = request.get_json(force=True, silent=True) or {}
        benchmark = payload.get('benchmark', 'ghz')
        qubits = int(payload.get('qubits', 5))
        backend_qubits = int(payload.get('backend_qubits', max(7, qubits)))

        if qubits < 2:
            return jsonify({'error': 'Qubits must be at least 2.'}), 400
        if backend_qubits < qubits:
            return jsonify({'error': 'Backend qubits must be >= circuit qubits.'}), 400

        circuit = _build_benchmark(benchmark, qubits)
        backend = GenericBackendV2(num_qubits=backend_qubits, seed=42)
        analyzer = TranspilationAnalyzer(target_backend=backend)
        df = analyzer.benchmark_circuit(circuit)

        results = df.to_dict(orient='records')
        return jsonify({
            'benchmark': benchmark,
            'qubits': qubits,
            'results': results,
        })
    except Exception as exc:  # pragma: no cover - defensive error handling
        return jsonify({'error': str(exc)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
