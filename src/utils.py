from typing import Any
from argparse import ArgumentParser

def get_args() -> Any: 
    argument_parser = ArgumentParser(
        prog="python -m qec",
        description="Simulate the 3-qubit bit-flip quantum error-correction code in Qiskit: prepare and encode a qubit, apply independent Pauli-X errors, measure error syndromes, correct a single bit flip, and report the resulting success rate and deviation.",
    )
    # Add Arguments
    argument_parser.add_argument("-v", "--topical-value", type=float, default=0, help="Initial state of the logical qubit, given as the probability of measuring |1⟩ (0.0 = |0⟩, 1.0 = |1⟩; values in between prepare a superposition). (default: 0)")
    argument_parser.add_argument("-p", "--p-bit-flip", type=float, default=0, help="Probability that an independent Pauli-X (bit-flip) error is applied to each of the three data qubits during the noise simulation phase. (default: 0)")
    argument_parser.add_argument("-s", "--shots", type=int, default=1024, help="Number of shots the simulator runs per circuit. (default: 1024)")
    argument_parser.add_argument("-it", "--iterations", type=int, default=1, help="Number of times the full circuit is built and run with the given parameters. Unlike --shots, which repeats measurement of one fixed circuit, each iteration constructs a fresh circuit — combine with --iterate_up/--iterate_down to vary the bit-flip probability across iterations. (default: 1)")
    argument_parser.add_argument("--iterate-up", action="store_true", help="Increase --p_bit_flip by a fixed step each iteration (step = (1 - initial p_bit_flip) / iterations). Cannot be combined with --iterate_down.")
    argument_parser.add_argument("--iterate-down", action="store_true", help="Decrease --p_bit_flip by a fixed step each iteration (step = (1 - initial p_bit_flip) / iterations). Cannot be combined with --iterate_up.")
    argument_parser.add_argument("-d", "--draw",action="store_true" , help="Print the generated circuit — including the encoding, noise, recovery, and correction phases — and the resulting measurement counts, for each iteration.")
    argument_parser.add_argument("-V", "--verbose", action="store_true", help="Print step-by-step detail about circuit construction and execution as the simulation runs.")
    argument_parser.add_argument("-D", "--debug", action="store_true", help="Enable debug mode. Implies --verbose.")
    
    # Parse Arguments
    ARGS = argument_parser.parse_args()
    if ARGS.iterate_down and ARGS.iterate_up:
        raise ValueError("Error: Cannot iterate both up and down. Please choose one or the other.")

    # Print verbose outputs
    if ARGS.debug:
        ARGS.verbose = True
        print("V: Debug mode is set to true")
    if ARGS.verbose:
        print("V: Verbose mode is set to true")
    if ARGS.verbose or ARGS.debug:
        print(f"V: Topical value: {ARGS.topical_value}")
        print(f"V: Probability of bit-flip error: {ARGS.p_bit_flip}")
        print(f"V: Number of shots: {ARGS.shots}")
        print(f"V: Number of iterations: {ARGS.iterations}")
    
    return ARGS

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
