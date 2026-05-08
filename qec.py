import qiskit
import qiskit_aer
import numpy
import argparse
import random

def encodingphase(topical_state: qiskit.QuantumCircuit,):
    pass

def noise_simulation(qubits: qiskit.QuantumCircuit, ):
    pass

def recovery_phase(qubits: qiskit.QuantumCircuit, ancilla: qiskit.QuantumCircuit = qiskit.QuantumCircuit(2)):
    pass

def correction_phase(qubits: qiskit.QuantumCircuit, ancilla: qiskit.QuantumCircuit = qiskit.QuantumCircuit(2)):
    pass

def qec_circuit(
        topical_value : float = 0,
        p_bit_flip : float = 0,
        shots : int = 1024,
        circuit: qiskit.QuantumCircuit | None = None,
        register : qiskit.ClassicalRegister | None = None,
        simulator : qiskit_aer.AerSimulator | None = None,
        error_bit_flip : qiskit_aer.noise.QuantumError | None = None,
        draw_circuit: bool = False,
) -> {float, int, int}:
    # ==================== Definitions ====================
    # Define the registers
    quantum_register = qiskit.QuantumRegister(5, 'quantum')
    if ARGS.debug or ARGS.verbose:
        print("V: Quantum register defined with 5 qubits")
    syndrome = qiskit.ClassicalRegister(2, 'syndrome')
    if ARGS.debug or ARGS.verbose:
        print("V: Syndrome register defined with 2 bits")
    if register == None:
        register = qiskit.ClassicalRegister(3, 'Full Register')
    if ARGS.debug or ARGS.verbose:
        print("V: Full register defined with 5 bits")
    
    # Define the circuit if not previously defined
    if circuit == None:
        circuit = qiskit.QuantumCircuit(quantum_register, syndrome, register)
    if ARGS.debug or ARGS.verbose:
        print("V: Quantum circuit defined with the quantum register and the classical registers")

    # Define the simulator and set the noise if not already defined
    if simulator == None:
        simulator = qiskit_aer.AerSimulator()
    if ARGS.debug or ARGS.verbose:
        print("V: Simulator defined with the AerSimulator backend")
    if error_bit_flip == None:
        error_bit_flip = qiskit_aer.noise.errors.pauli_error([('X', p_bit_flip), ('I', 1 - p_bit_flip)])
    if ARGS.debug or ARGS.verbose:
        print(f"V: Bit-flip error defined with probability {p_bit_flip} for X and {1 - p_bit_flip} for I")

    # Define the topical state
    # FIXME: improve options for how topical state is determined 
        # i.e. the topical value parameter should mean the probability of 1 state
        # if topical_value equals 1, then the qubit should be |1>
        # if topical_value equals 0, then qubiut should be |0>
        # else (if topical_value not equal to (1 or 0)) qubit should be (1-topical_value)|0> + (topical_value)|1>
    if topical_value % 2 == 1:
        circuit.x(0)
    elif topical_value % 2 != 0:
        circuit.h(0)
    if ARGS.debug or ARGS.verbose:
        print(f"V: Topical state defined with value {topical_value} and applied to the first qubit")
    
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
    transpiled_circuit = qiskit.compiler.transpile(circuit, simulator)

    # run the circuit on the simulator
    result = simulator.run(transpiled_circuit, shots=shots).result()
    counts = result.get_counts(transpiled_circuit)
    if draw_circuit:
        print(counts)

    # determine if the error correction was successful
    # Expected state: if topical_value is 0, expect "000"; if 1, expect "111"
    if topical_value % 2 == 0:
        expected_states = ["000"]
    elif topical_value % 2 == 1:
        expected_states = ["111"]
    else:
        expected_states = ["000", "111"]

    sucesses: int = 0
    failures: int = 0
    success_rate: float = 0
    for count in counts:
        if count[:3] in expected_states:
            sucesses += counts[count]
            if ARGS.debug or ARGS.verbose:
                print(f"V: Count {count} is a success with {counts[count]} shots")
        else:
            failures += counts[count]
            if ARGS.debug or ARGS.verbose:
                print(f"V: Count {count} is a failure with {counts[count]} shots")
    success_rate = sucesses / (sucesses + failures) if (sucesses + failures) > 0 else 0
    return success_rate, sucesses, failures

def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="A simple implementation of the 3-qubit bit-flip code in Qiskit.")
    parser.add_argument("-v", "--topical_value", type=float, default=0, help="The value of the topical state to be encoded. (default: 0)")
    parser.add_argument("-p", "--p_bit_flip", type=float, default=0, help="The probability of a bit-flip error occurring on each qubit during the noise simulation phase. (default: 0)")
    parser.add_argument("-s", "--shots", type=int, default=1024, help="The number of shots to run the circuit on the simulator. (default: 1024)")
    parser.add_argument("-it", "--iterations", type=int, default=1, help="The number of times to run the circuit with the same parameters. (default: 1)")
    parser.add_argument("--iterate_up", action="store_true", help="Increase the probability of bit flip error with each iteration.")
    parser.add_argument("--iterate_down", action="store_true", help="Decrease the probability of bit flip error with each iteration.")
    parser.add_argument("-d", "--draw", action="store_true", help="Draw the circuit at iteration")
    parser.add_argument("-V", "--verbose", action="store_true", help="Print the circuit and the results in a more verbose format.")
    parser.add_argument("-D", "--debug", action="store_true", help="Turns on the debug mode, which sets the verbose mode and prints any errors that occur")
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
    step_size = (1 - ARGS.p_bit_flip) / ARGS.iterations if ARGS.iterate_down or ARGS.iterate_up else 0
    for i in range(ARGS.iterations):
        if ARGS.verbose or ARGS.debug:
            print(f"V: Iteration {i+1}/{ARGS.iterations}")
        rate, success, failure = qec_circuit(
            topical_value=ARGS.topical_value,
            p_bit_flip=ARGS.p_bit_flip,
            shots=ARGS.shots,
            draw_circuit=ARGS.draw,
        )
        if ARGS.verbose or ARGS.debug:
            print(f"V: Iteration {i+1}/{ARGS.iterations} finished running with success rate of {rate}")
        successes += success
        failures += failure
        print(f"Finished Running circuit {i+1}: Succesful shots: {success}, Failed shots: {failure}, Success rate: {rate:.2%}")
        if ARGS.iterate_up:
            ARGS.p_bit_flip += step_size
        elif ARGS.iterate_down:
            ARGS.p_bit_flip -= step_size
    sucess_rate = successes / (successes + failures)
    print(f"Total successful shots: {successes}, Total failed shots: {failures}, Overall success rate: {(sucess_rate):.2%}")
    return 0

if __name__ == "__main__":
    if main() != 0:
        raise RuntimeError("Error occured during runtime")
