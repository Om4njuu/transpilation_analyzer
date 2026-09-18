#execution and fidelity evaluation using Qiskit Aer Primitives

from typing import Dict
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer.primitives import SamplerV2
from qiskit_aer.noise import NoiseModel

#calculate Hellinger distance between two probability distributions (0 = identical, 1 = orthogonal)
def compute_hellinger_distance(p: Dict[str, float], q: Dict[str, float]) -> float:
    all_keys = set(p.keys()).union(set(q.keys()))
    sum_sq_diff = 0.0
    for k in all_keys:
        p_i = p.get(k, 0.0)
        q_i = q.get(k, 0.0)
        sum_sq_diff += (np.sqrt(p_i) - np.sqrt(q_i)) ** 2
    return np.sqrt(sum_sq_diff) / np.sqrt(2)

#simulates transpiled circuits under ideal and noisy backend environments
class NoiseEvaluator:
    
    def __init__(self, noise_model: NoiseModel = None):
        self.noise_model = noise_model

    #executes ideal vs. noisy simulation and returns Hellinger distance
    def evaluate(self, ideal_circuit: QuantumCircuit, transpiled_circuit: QuantumCircuit, shots: int = 4096) -> float:
        #ideal simulation
        ideal_sampler = SamplerV2()
        ideal_job = ideal_sampler.run([ideal_circuit], shots=shots)
        ideal_counts = ideal_job.result()[0].data.meas.get_counts()
        ideal_dist = {k: v / shots for k, v in ideal_counts.items()}

        #noisy simulation
        noisy_sampler = SamplerV2(options={"backend_options": {"noise_model": self.noise_model}}) if self.noise_model else SamplerV2()
        noisy_job = noisy_sampler.run([transpiled_circuit], shots=shots)
        noisy_counts = noisy_job.result()[0].data.meas.get_counts()
        noisy_dist = {k: v / shots for k, v in noisy_counts.items()}

        return compute_hellinger_distance(ideal_dist, noisy_dist)