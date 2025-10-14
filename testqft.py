import numpy as np
import pandas as pd
from fractions import Fraction
from math import floor, gcd, log

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT, UnitaryGate
from qiskit.transpiler import CouplingMap, generate_preset_pass_manager
from qiskit.visualization import plot_histogram

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler

num_target = 10 
num_control = num_target
num_output = num_control

control = QuantumRegister(num_control, name="C")
target = QuantumRegister(num_target, name="T")
output = ClassicalRegister(num_output, name="out")
circuit = QuantumCircuit(control, target, output)
circuit.compose(QFT(num_control, inverse=False), qubits=control, inplace=True)
circuit.draw(output="mpl", fold=-1, style="clifford", idle_wires=False)

import matplotlib.pyplot as plt

from qiskit_aer import AerSimulator

sim = AerSimulator() 
pm = generate_preset_pass_manager(optimization_level=3, backend=sim)
transpiled_circuit = pm.run(circuit)
print(pm)

transpiled_circuit.draw(output="mpl", fold=-1, style="clifford", idle_wires=False)
plt.show()
