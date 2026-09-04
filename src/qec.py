from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.compiler import transpile 
from qiskit_aer import AerSimulator
from qiskit_aer.noise import QuantumError, pauli_error
from numpy import sqrt, arcsin
from argparse import ArgumentParser
import random

def qec_circuit(
        inital_state : float = 0,
        p_bit_flip : float = 0,
        shots : int = 1024,
        circuit: QuantumCircuit | None = None,
        register : ClassicalRegister | None = None,
        simulator : AerSimulator | None = None,
        error_bit_flip : QuantumError | None = None,
        draw_circuit: bool = False,
) -> tuple:
    # ==================== Definitions ====================
    # Define the registers
    quantum_register = QuantumRegister(5, 'quantum')
    if ARGS.debug or ARGS.verbose:
        print("V: Quantum register defined with 5 qubits")
    syndrome = ClassicalRegister(2, 'syndrome')
    if ARGS.debug or ARGS.verbose:
        print("V: Syndrome register defined with 2 bits")
    if register == None:
        register = ClassicalRegister(3, 'Full Register')
    if ARGS.debug or ARGS.verbose:
        print("V: Full register defined with 5 bits")
    
    # Define the circuit if not previously defined
    if circuit == None:
        circuit = QuantumCircuit(quantum_register, syndrome, register)
    if ARGS.debug or ARGS.verbose:
        print("V: Quantum circuit defined with the quantum register and the classical registers")

    # Define the simulator and set the noise if not already defined
    if simulator == None:
        simulator = AerSimulator()
    if ARGS.debug or ARGS.verbose:
        print("V: Simulator defined with the AerSimulator backend")
    if error_bit_flip == None:
        error_bit_flip = pauli_error([('X', p_bit_flip), ('I', 1 - p_bit_flip)])
    if ARGS.debug or ARGS.verbose:
        print(f"V: Bit-flip error defined with probability {p_bit_flip} for X and {1 - p_bit_flip} for I")

    circuit.ry(2 * arcsin(sqrt(inital_state)), 0)
    if ARGS.debug or ARGS.verbose:
        print(f"V: Inital state defined with value {inital_state} and applied to the first qubit")
    
    # ==================== Encoding phase ====================
    # Use CNOT(0,1) to set the state of the 1st qubit
    circuit.cx(0,1)

    # Use CNOT(0,2) to set the state of the 2nd qubit
    circuit.cx(0,2)

    # Divide and draw the phase
    circuit.barrier()
    encodingphase = circuit.draw()
    if ARGS.debug or ARGS.verbose:
        print("V: Encoding phase completed and drawn")
        print(f"\tEncoding phase:\n{encodingphase}")

    # ==================== Error simualtion phase ====================

    # Simulate the chance of bit-flip on qubit 0
    circuit.append(error_bit_flip, [0])
    if ARGS.debug or ARGS.verbose:
        print(f"V: Added chance of bit flip error to qubit 0 with chance {p_bit_flip}")
    
    # Simulate the chance of bit-flip on qubit 1
    circuit.append(error_bit_flip, [1])
    if ARGS.debug or ARGS.verbose:
        print(f"V: Added chance of bit flip error to qubit 1 with chance {p_bit_flip}")

    # Simulate the chance of bit-flip on qubit 2
    circuit.append(error_bit_flip, [2])
    if ARGS.debug or ARGS.verbose:
        print(f"V: Added chance of bit flip error to qubit 2 with chance {p_bit_flip}")
    
    # Divide and draw the phase
    circuit.barrier()
    noise_phase = circuit.draw()
    if ARGS.debug or ARGS.verbose:
        print("V: Noise simulation phase completed and drawn")
        print(f"\tNoise simulation phase:\n{noise_phase}")

    # ==================== Recovery operation phase ====================

    # Set ancilla1 value using CNOT(0,a1) and CNOT(1,a1)
    circuit.cx(0,3)
    circuit.cx(1,3)

    # Set ancilla2 value using CNOT(1,a2) and CNOT(2,a2)
    circuit.cx(1,4)
    circuit.cx(2,4)

    # Divide and draw the phase
    circuit.barrier()
    recovery_phase = circuit.draw()
    if ARGS.debug or ARGS.verbose:
        print("V: Recovery operation phase completed and drawn")
        print(f"\tRecovery operation phase:\n{recovery_phase}")

    # ==================== Error correction phase ====================

    # measure the qubits in the ancilla
    circuit.measure(quantum_register[3], syndrome[0])
    circuit.measure(quantum_register[4], syndrome[1])
    circuit.barrier()
    if ARGS.debug or ARGS.verbose:
        print("V: Ancilla measured and syndrome register updated")

    # apply corrections based on the measured of the ancilla
    with circuit.if_test((syndrome, 1)):
        circuit.x(quantum_register[0])
        if ARGS.debug or ARGS.verbose:
            print("V: Correction applied to qubit 0 based on syndrome measurement")
    with circuit.if_test((syndrome, 3)):
        circuit.x(quantum_register[1])
        if ARGS.debug or ARGS.verbose:
            print("V: Correction applied to qubit 1 based on syndrome measurement")
    with circuit.if_test((syndrome, 2)):
        circuit.x(quantum_register[2])
        if ARGS.debug or ARGS.verbose:
            print("V: Correction applied to qubit 2 based on syndrome measurement")

    # Divide and draw the phase
    circuit.barrier()
    correction_phase = circuit.draw()
    if ARGS.debug or ARGS.verbose:
        print("V: Error correction phase completed and drawn")
        print(f"\tError correction phase:\n{correction_phase}")
    
    # ==================== Evaluate the circuit ====================

    # measure the qubits in the quantum register
    circuit.measure(quantum_register[0], register[0])
    circuit.measure(quantum_register[1], register[1])
    circuit.measure(quantum_register[2], register[2])

    # draw and print the final circuit
    final_circuit = circuit.draw()
    if draw_circuit:
        print(final_circuit)
    
    # compile the circuit
    transpiled_circuit = transpile(circuit, simulator)

    # run the circuit on the simulator
    result = simulator.run(transpiled_circuit, shots=shots).result()
    counts = result.get_counts(transpiled_circuit)
    if draw_circuit:
        print(counts)

    # determine if the error correction was successful
    # Expected state: if topical_value is 0, expect "000"; if 1, expect "111"
    successes : int = 0
    failures : int = 0
    states_111 : int = 0
    states_000 : int = 0
    # determine the expected states
    if inital_state % 2 == 0:
        expected_states = ["000"]
    elif inital_state % 2 == 1:
        expected_states = ["111"]
    else:
        expected_states = ["000", "111"]
    # gather the number of different states
    for count, total in counts.items():
        state = count[:3]
        if state in expected_states: successes += total
        else: failures += total
        if state == "111": states_111 += total
        else: states_000 += total
    # Ge the success rate
    success_rate : float = successes / (successes + failures) if (successes + failures) > 0 else 0
    # Determine the probabalistic 
    final_state = states_111 / successes if successes > 0 else 0
    deviation = abs(inital_state - final_state)
    # return results
    return success_rate, successes, failures, deviation

def main():
    # Parse the command line arguments
    parser = ArgumentParser(description="Simulate the 3-qubit bit-flip quantum error-correction code in Qiskit. Prepares a single logical qubit in a chosen initial state, encodes it across three physical qubits, applies independent Pauli-X (bit-flip) errors with a configurable probability, measures two syndrome qubits to detect which qubit (if any) was flipped, and applies the corresponding correction. Reports the success rate and deviation from the expected result across one or more runs.")
    parser.add_argument("-v", "--topical_value", type=float, default=0, help="Initial state of the logical qubit, given as the probability of measuring |1⟩ (0.0 = |0⟩, 1.0 = |1⟩; values in between prepare a superposition). (default: 0)")
    parser.add_argument("-p", "--p_bit_flip", type=float, default=0, help="Probability that an independent Pauli-X (bit-flip) error is applied to each of the three data qubits during the noise simulation phase. (default: 0)")
    parser.add_argument("-s", "--shots", type=int, default=1024, help="Number of shots the simulator runs per circuit. (default: 1024)")
    parser.add_argument("-it", "--iterations", type=int, default=1, help="Number of times the full circuit is built and run with the given parameters. Unlike --shots, which repeats measurement of one fixed circuit, each iteration constructs a fresh circuit — combine with --iterate_up/--iterate_down to vary the bit-flip probability across iterations. (default: 1)")
    parser.add_argument("--iterate_up", action="store_true", help="Increase --p_bit_flip by a fixed step each iteration (step = (1 - initial p_bit_flip) / iterations). Cannot be combined with --iterate_down.")
    parser.add_argument("--iterate_down", action="store_true", help="Decrease --p_bit_flip by a fixed step each iteration (step = (1 - initial p_bit_flip) / iterations). Cannot be combined with --iterate_up.")
    parser.add_argument("-d", "--draw", action="store_true", help="Print the generated circuit — including the encoding, noise, recovery, and correction phases — and the resulting measurement counts, for each iteration.")
    parser.add_argument("-V", "--verbose", action="store_true", help="Print step-by-step detail about circuit construction and execution as the simulation runs.")
    parser.add_argument("-D", "--debug", action="store_true", help="Enable debug mode. Implies --verbose.")
    global ARGS
    ARGS = parser.parse_args()
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

    # Run the circuit for the specified number of iterations
    successes: int = 0
    failures: int = 0
    avg_deviation: float = 0
    step_size = (1 - ARGS.p_bit_flip) / ARGS.iterations if ARGS.iterate_down or ARGS.iterate_up else 0
    for i in range(ARGS.iterations):
        if ARGS.verbose or ARGS.debug:
            print(f"V: Iteration {i+1}/{ARGS.iterations}")
        rate, success, failure, deviation = qec_circuit(
            inital_state=ARGS.topical_value,
            p_bit_flip=ARGS.p_bit_flip,
            shots=ARGS.shots,
            draw_circuit=ARGS.draw,
        )
        if ARGS.verbose or ARGS.debug:
            print(f"V: Iteration {i+1}/{ARGS.iterations} finished running with success rate of {rate}")
        successes += success
        failures += failure
        avg_deviation += deviation
        print(f"Finished Running circuit {i+1}\t Succesful shots: {success}\t Failed shots: {failure}\t Success rate: {rate:.2%}\t Deviation: {deviation:.2%}")
        if ARGS.iterate_up:
            ARGS.p_bit_flip += step_size
        elif ARGS.iterate_down:
            ARGS.p_bit_flip -= step_size
    sucess_rate = successes / (successes + failures)
    avg_deviation /= ARGS.iterations
    print(f"Total successful shots: {successes}, Total failed shots: {failures}, Overall success rate: {(sucess_rate):.2%}, Average deviation: {avg_deviation:.2%}")
    return 0

if __name__ == "__main__":
    if main() != 0:
        raise RuntimeError("Error occured during runtime")
