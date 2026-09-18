# Quantum Transpilation & Noise Analyzer

A modular Python framework built with **Qiskit 1.0+** to benchmark quantum circuit compile passes, analyze two-qubit gate routing overhead on physical backend coupling topologies, and evaluate simulation fidelity using Hellinger distance under noisy backend models.

---

## Key Features

- **Circuit Benchmarking Suite** - Automated generation of standard benchmark algorithms (QFT, GHZ, QAOA Ansätze).
- **Target Topologies** - Mapping circuits onto `BackendV2` target representations (e.g., IBM Heron/Eagle hardware coupling graphs).
- **Optimization Level Analysis** - Extraction of circuit depth, CNOT/ECR gate counts, and SWAP overhead across transpiler optimization levels (0–3).
- **Noisy Simulation & Verification** - Execution via Qiskit Aer `SamplerV2` primitives using realistic thermal relaxation and gate error models.

---

## Requirements
qiskit>=1.0.0
qiskit-aer>=0.13.0
qiskit-ibm-runtime>=0.20.0
pandas>=2.0.0
numpy>=1.23.0
matplotlib>=3.7.0