import qiskit.qasm2 
import matplotlib 
import math 
from fractions import Fraction
from qiskit_aer import AerSimulator
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler
from qiskit_aer.primitives import SamplerV2
import pandas as pd 


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

shot_counts = 1000
count = sim.run(circuit, shots=shot_counts).result().get_counts(circuit)

print(type(count))


# organize data 
number_hit =  [] 
frequency  =  []
fraction   =  []
denominator = []

for measured_value in count:
    num = measured_value[::].replace(' ', '')  # remove spaces
    value = count.get(measured_value[::])
    print("value:", value)
    frequency.append(value)
    number_hit.append(int(num, 2))  
    frac = Fraction(int(num, 2),1024).limit_denominator(21)
    fraction.append(frac)
    denominator.append(frac.denominator)

df = pd.DataFrame ({
    "number hit": number_hit,
    "frequency": frequency,
    "fraction": fraction,
    "denominator": denominator
})

print("Original data sampled from the quantum circuit: ")
print(df)
filtered_df = df[df['frequency'] > shot_counts*0.04] # equivalent to more than 40 counts for every 1000 shots  

print("Remove some noisy element that have low count: ")
print(filtered_df)

period = []
for num in filtered_df['denominator']:
    if num not in period and num % 2 == 0:
        period.append(num)

print("possible period value to find the factors: ")
print(period)

for num in period: 
    guess1 = 2**(num//2) + 1 
    guess2 = 2**(num//2) - 1
    if math.gcd(guess1, 21) not in [1, 21]:
        print("factor found: ", math.gcd(guess1, 21))
    if math.gcd(guess2, 21) not in [1, 21]:
        print("factor found: ", math.gcd(guess2, 21))


# from qiskit.visualization import plot_histogram
# plot_histogram(count) 

# import matplotlib.pyplot as plt
# plt.show()