#module for generating standard quantum benchmark circuits

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

#generate an n-qubit GHZ state circuit
def build_ghz_circuit(num_qubits: int) -> QuantumCircuit: 
    qc = QuantumCircuit(num_qubits, name=f"GHZ_{num_qubits}q")
    qc.h(0)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
    qc.measure_all()
    return qc

#generate an n-qubit Quantum Fourier Transform circuit with measurements
def build_qft_circuit(num_qubits: int) -> QuantumCircuit:
    qc = QuantumCircuit(num_qubits, name=f"QFT_{num_qubits}q")
    qft_gate = QFT(num_qubits=num_qubits, insert_barriers=True)
    qc.append(qft_gate, list(range(num_qubits)))
    qc.measure_all()
    return qc