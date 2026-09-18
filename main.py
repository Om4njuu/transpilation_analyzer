"""Pipeline runner for the Quantum Transpilation & Noise Analyzer."""

from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_aer.noise import NoiseModel
from src.benchmarks import build_qft_circuit, build_ghz_circuit
from src.analyzer import TranspilationAnalyzer
from src.evaluator import NoiseEvaluator

def main():
    #setup target hardware layout (Fake 7-qubit backend with coupling map)
    target_backend = GenericBackendV2(num_qubits=7, seed=42)
    
    # instantiate analyzer with target backend
    analyzer = TranspilationAnalyzer(target_backend=target_backend)
    
    #generate benchmark circuits
    ghz = build_ghz_circuit(num_qubits=5)
    qft = build_qft_circuit(num_qubits=5)
    
    print("=== Transpilation Metrics ===")
    for circ in [ghz, qft]:
        df = analyzer.benchmark_circuit(circ)
        print(f"\nResults for {circ.name}:")
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()