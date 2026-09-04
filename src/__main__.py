from argparse import ArgumentParser
# TODO: remove main from imports
from qec import qec_circuit, main

if __name__ == "__main__":
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
    global ARGS
    ARGS = argument_parser.parse_args()
    global debug
    debug = ARGS.debug
    global verbose
    verbose = ARGS.verbose
    
    # Run Circuit
    # Set tracking variables
    total_successes : int = 0
    total_failures : int = 0
    avg_deviation : float = 0
    # Loop for each iteration
    for i in range(ARGS.iterations):
        # Run the circuit
        success_rate, successes, failures, deviation = qec_circuit(
            inital_state=ARGS.topical_value,
            p_bit_flip=ARGS.p_bit_flip, 
            shots=ARGS.shots,
            draw_circuit=ARGS.draw,
        )
        # Print the results
        print(f"Circuit #{i+1} finished running.\tSuccessful shots: {successes}\tFailed shots: {failures}\tSuccess rate: {success_rate}\tDeviation: {deviation}")
        # Save the results
        total_successes += successes
        total_failures += failures
        avg_deviation += deviation

    # Evaluate results
    print(f"All {ARGS.iterations} circuit(s) finished running")
    total_shots : int = total_successes + total_failures
    overall_success_rate : float = total_successes / total_shots
    avg_deviation /= ARGS.iterations
    print(f"Total successful shots: {total_successes}\tTotal failed shots: {total_failures}\tOverall success rate: {overall_success_rate}\tAverage deviation: {avg_deviation:.2%}")
