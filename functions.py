from typing import Any
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_aer import AerSimulator

def init_circuit(num_qubits = 2) -> QuantumCircuit:
    """ returns a circuit with the number of given qubits """
    return QuantumCircuit(num_qubits)

def run_circuit(circuit: QuantumCircuit, backend: AerSimulator = AerSimulator(), shots: int = 1024) -> Any:
    """ runs the given circuit on the given backend for the given number of shots and returns the result """
    # transpile the circuit using the given backend's run method
    transpiled_circuit = transpile(circuit, backend)

    # run the circuit on the backend for the given number of shots
    job = backend.run(transpiled_circuit, shots=shots)

    # return the result of the job
    return job.result()

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
