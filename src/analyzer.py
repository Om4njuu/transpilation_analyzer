#transpilation analysis engine using Qiskit 1.0+ transpile API

from typing import List
import pandas as pd
from qiskit import QuantumCircuit, transpile
from qiskit.providers import BackendV2

#analyzes circuit overhead across optimization levels and backend targets
class TranspilationAnalyzer:
    
    def __init__(self, target_backend: BackendV2):
        self.backend = target_backend

    def benchmark_circuit(self, circuit: QuantumCircuit, opt_levels: List[int] = [0, 1, 2, 3]) -> pd.DataFrame:
        results = []
        for level in opt_levels:
            transpiled_qc = transpile(
                circuit,
                backend=self.backend,
                optimization_level=level,
                seed_transpiler=42
            )
            ops = transpiled_qc.count_ops()
            two_qubit_gates = ops.get('cx', 0) + ops.get('ecr', 0) + ops.get('cz', 0)
            
            results.append({
                "circuit_name": circuit.name,
                "optimization_level": level,
                "depth": transpiled_qc.depth(),
                "total_gates": sum(ops.values()),
                "two_qubit_gates": two_qubit_gates,
                "swap_gates": ops.get('swap', 0),
            })
            
        return pd.DataFrame(results)