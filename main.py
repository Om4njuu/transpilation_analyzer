#pipeline runner for the Quantum Transpilation & Noise Analyzer

from qiskit.providers.fake_provider import GenericBackendV2
from src.benchmarks import build_ghz_circuit, build_qft_circuit
from src.analyzer import TranspilationAnalyzer
from src.visualizer import plot_transpilation_results

def main():
    target_backend = GenericBackendV2(num_qubits=7, seed=42)
    analyzer = TranspilationAnalyzer(target_backend=target_backend)
    
    ghz = build_ghz_circuit(num_qubits=5)
    qft = build_qft_circuit(num_qubits=5)
    
    df_ghz = analyzer.benchmark_circuit(ghz)
    df_qft = analyzer.benchmark_circuit(qft)
    
    print("=== Transpilation Metrics ===")
    print(f"\nResults for {ghz.name}:")
    print(df_ghz.to_string(index=False))
    
    print(f"\nResults for {qft.name}:")
    print(df_qft.to_string(index=False))

    # Generate and save metrics plot
    plot_transpilation_results(df_ghz, df_qft)

if __name__ == "__main__":
    main()