import qiskit
import qiskit_aer
import numpy
import argparse
import functions as helpers
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
        simulator : qiskit_aer.AerSimulator | None = None
):
    # ==================== Definitions ====================
    # Define the registers
    quantum_register = qiskit.QuantumRegister(5, 'quantum')
    syndrome = qiskit.ClassicalRegister(2, 'syndrome')
    if register == None:
        register = qiskit.ClassicalRegister(5, 'Full Register')
    
    # Define the circuit if not previously defined
    if circuit == None:
        circuit = qiskit.QuantumCircuit(quantum_register, syndrome, register)

    # Define the simulator and set the noise if not already defined
    if simulator == None:
        # TODO add bit_flip error that only runs during the enviornemt error simulation phase
        simulator = qiskit_aer.AerSimulator()

    # Define the topical state
    if topical_value % 2 == 1:
        circuit.x(0)
    elif topical_value % 2 != 0:
        circuit.h(0)
    
    # ==================== Encoding phase ====================
    # Use CNOT(0,1) to set the state of the 1st qubit
    circuit.cx(0,1)

    # Use CNOT(0,2) to set the state of the 2nd qubit
    circuit.cx(0,2)

    # Divide and draw the phase
    circuit.barrier()
    encodingphase = circuit.draw()

    # ==================== Error simualtion phase ====================

    # Simulate the chance of bit-flip on qubit 0
    if random.random() <= p_bit_flip:
        circuit.x(0)
    
    # Simulate the chance of bit-flip on qubit 1
    if random.random() <= p_bit_flip:
        circuit.x(1)
    
    # Simulate the chance of bit-flip on qubit 2
    if random.random() <= p_bit_flip:
        circuit.x(2)
    
    # Divide and draw the phase
    circuit.barrier()
    noise_phase = circuit.draw()

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

    # ==================== Error correction phase ====================

    # measure the qubits in the ancilla
    circuit.measure(quantum_register[3], syndrome[0])
    circuit.measure(quantum_register[4], syndrome[1])
    circuit.barrier()

    # apply corrections based on the measured of the ancilla
    with circuit.if_test((syndrome, 1)):
        circuit.x(quantum_register[0])
    with circuit.if_test((syndrome, 3)):
        circuit.x(quantum_register[1])
    with circuit.if_test((syndrome, 2)):
        circuit.x(quantum_register[2])

    # Divide and draw the phase
    circuit.barrier()
    correction_phase = circuit.draw()
    
    # ==================== Evaluate the circuit ====================

    # measure the qubits in the quantum register
    circuit.measure(quantum_register[0], register[0])
    circuit.measure(quantum_register[1], register[1])
    circuit.measure(quantum_register[2], register[2])

    # draw and print the final circuit
    final_circuit = circuit.draw()
    print(final_circuit)
    
    # compile the circuit
    transpiled_circuit = qiskit.compiler.transpile(circuit, simulator)

    # run the circuit on the simulator
    result = simulator.run(transpiled_circuit, shots=shots).result()
    counts = result.get_counts(transpiled_circuit)
    print(counts)

def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="A simple implementation of the 3-qubit bit-flip code in Qiskit.")
    parser.add_argument("-v", "--topical_value", type=float, default=0, help="The value of the topical state to be encoded. (default: 0)")
    parser.add_argument("-p", "--p_bit_flip", type=float, default=0, help="The probability of a bit-flip error occurring on each qubit during the noise simulation phase. (default: 0)")
    parser.add_argument("-s", "--shots", type=int, default=1024, help="The number of shots to run the circuit on the simulator. (default: 1024)")
    parser.add_argument("-sh", "--iterations", type=int, default=1, help="The number of times to run the circuit with the same parameters. (default: 1)")
    parser.add_argument("-V", "--verbose", action="store_true", help="Print the circuit and the results in a more verbose format.")
    parser.add_argument("-d", "--debug", action="store_true", help="Turns on the debug mode, which sets the verbose mode and prints any errors that occur")
    global args
    args = parser.parse_args()

    # Print verbose outputs
    if args.debug:
        args.verbose = True
        print("V: Debug mode is set to true")
    if args.verbose:
        print("V: Verbose mode is set to true")
    if args.verbose or args.debug:
        print(f"V: Topical value: {args.topical_value}")
        print(f"V: Probability of bit-flip error: {args.p_bit_flip}")
        print(f"V: Number of shots: {args.shots}")
        print(f"V: Number of iterations: {args.iterations}")

    # Run the circuit for the specified number of iterations
    for i in range(args.iterations):
        if args.verbose or args.debug:
            print(f"V: Iteration {i+1}/{args.iterations}")
        qec_circuit(
            topical_value=args.topical_value,
            p_bit_flip=args.p_bit_flip,
            shots=args.shots
        )
    return 0

if __name__ == "__main__":
    if main() != 0:
        raise RuntimeError("Error occured during runtime")
