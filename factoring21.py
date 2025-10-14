import qiskit.qasm2 
import matplotlib 

from qiskit_aer import AerSimulator
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler
from qiskit_aer.primitives import SamplerV2

program = """
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
 
    h q[0];
    cx q[0], q[1];
 
    measure q -> c;
"""

circuit = qiskit.qasm2.load('factor21.qasm')

print(circuit)

sim = AerSimulator(method='statevector')
pm = generate_preset_pass_manager(backend=sim, optimization_level=0)
qc = pm.run(circuit)
print(qc)

count = sim.run(circuit, shots=100).result().get_counts(circuit)
# print(count)

for measured_value in count:
   binary_str = ''.join(measured_value[::-1])
   print(binary_str)

from qiskit.visualization import plot_histogram
plot_histogram(count) 

import matplotlib.pyplot as plt
plt.show()