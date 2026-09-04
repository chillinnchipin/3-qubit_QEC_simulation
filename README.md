## 3-qubit QEC simulation
This project simulates the 3-qubit bit-flip quantum error-correction code in Qiskit. It prepares a qubit in a configurable state, encodes it across three data qubits, applies independent Pauli-X errors with a chosen probability, and uses two syndrome qubits to identify and correct a single bit-flip error. The circuit is executed with Qiskit Aer, and the program reports successful and failed shots, the overall success rate, and the deviation of the measured result from the input state.

The simulation can run one or more iterations, optionally changing the bit-flip probability between iterations, and can draw each generated circuit for inspection.
# Usage
To use this project, simply run the qec.py file:
```bash 
python qec.py 
```
This runs the default values for the qec which passes a qubit of ket 0 through a noiseless channel.

For more information on options run
```bash
python qec.py -h
```
or read below
## Arguments
Add arguments to set the values of the simulation
### Initial value of the qubit (-v, --topical-value)
Initial state of the logical qubit, given as the probability of measuring |1⟩ (0.0 = |0⟩, 1.0 = |1⟩; values in between prepare a superposition). (default: 0)
```bash
python qec.py -topical-value 1
```
### Probability of bit-flip error (-p, --p-bit-flip)
Probability that an independent Pauli-X (bit-flip) error is applied to each of the three data qubits during the noise simulation phase. (default: 0)
```bash
python qey.py --p-bit-flip 0.5
``` 
### Number of shots (-s, --shots)
Number of shots the simulator runs per circuit. (default: 1024)
```bash
python qec.py --shots 1024
```
### Run multiple simulations (-it, --iterations)
Number of times the full circuit is built and run with the given parameters. Unlike --shots, which repeats measurement of one fixed circuit, each iteration constructs a fresh circuit — combine with --iterate_up/--iterate_down to vary the bit-flip probability across iterations. (default: 1)

**Note:** This is different from --shots, as --shots increasing the number of times the AerSimulator runs with the error occurring on the same qubits. --iterations increases the number of times the entire circuit is run. Each iteration has a bit-flip error occurring on different qubits. 
```bash
python qec.py --iterations 100
```
## Draw the circuit (-d, --draw)
Print the generated circuit — including the encoding, noise, recovery, and correction phases — and the resulting measurement counts, for each iteration.
```bash
python qec.py --draw
```
## Helper arguments (-D, -V, --debug, --verbose)
--debug Enable debug mode. Implies --verbose.
```bash
python qec.py --debug
```
--verbose Print step-by-step detail about circuit construction and execution as the simulation runs. 
```bash
python qec.py --verbose
```
**NOTE:** --debug also sets verbose outputs to true
# Installation
## Installation Requirments
1. python3.10 or newer
2. pip 
## Installation Steps
1. Unzip the project directory onto your local machine
2. Install the required dependacies using pip
```bash
pip install -r requirments.txt
```
3. Run the files using python to ensure correct installation
```bash
python qec.py
```