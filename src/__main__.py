from argparse import ArgumentParser
from src.qec import qec_circuit
from .utils import get_args

if __name__ == "__main__":
    # Get command line arguments
    ARGS = get_args()
    # Run Circuit
    # Set tracking variables
    total_successes : int = 0
    total_failures : int = 0
    avg_deviation : float = 0
    # Loop for each iteration
    for i in range(ARGS.iterations):
        # Run the circuit
        success_rate, successes, failures, deviation = qec_circuit(
            initial_state=ARGS.topical_value,
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
