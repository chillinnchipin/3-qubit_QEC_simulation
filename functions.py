from typing import Any
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_aer import AerSimulator

def create_circuit(number_qubits = 2, number_bits = 2) -> QuantumCircuit:
    """ returns a circuit with the number of given qubits """
    return QuantumCircuit(number_qubits, number_bits)

def compile_circuit(circuit: QuantumCircuit, backend = AerSimulator()) -> QuantumCircuit:
    " returns a compiled circuit using the given backend"
    return transpile(circuit, backend)

def run_circuit(circuit: QuantumCircuit, transpiled: bool = True, backend = AerSimulator(), shots = 1024) -> Any:
    """ runs the given circuit on the given backend for the given number of shots and returns the result """
    if not transpiled:
        circuit = compile_circuit(circuit, backend)
    
    return backend.run(circuit, shots=shots).result()

def insert_block(circuit: QuantumCircuit, block: QuantumCircuit, qubits: list[int]):
    """ inserts the given block into the given circuit at the given qubits """
    circuit.compose(block, qubits=qubits, inplace=True)
    return circuit

def measure_all(circuit: QuantumCircuit):
    """ measures all qubits in the circuit and stores the result in the classical bits """
    circuit.measure_all()
    return circuit

def measure(circuit: QuantumCircuit, qubits: list[int], bits: list[int]):
    """ measures the given qubits in the circuit and stores the result in the given classical bits """
    circuit.measure(qubits, bits)
    return circuit

def draw_circuit(circuit: QuantumCircuit):
    """ draws the given circuit """
    circuit.barrier()
    return circuit.draw()
