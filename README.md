## 3-qubit QEC simulation
A simple simulation of the 3-qubit Quantum error correction for pauli-x (bit-flip) error
Allows for the simulation of passing a qubit through a nosiy channel and correcting bit-flip errors using the 3-qubit bit flip QEC
# Usage
To use this project, simply run the qec.py file:
```bash 
python qec.py 
```
This runs the defualt values for the qec which passes a qubit of ket 0 through a nosieless channel.

For more information on options run
```bash
python qec.py -h
```
or read below
## Arguments
Add arguments to set the values of the simulation
### Probability of bit-flip error (-p, --p-bit-flip)
Probability of Bit-flip error occuring.
The probability of a bitflip error occuring on any qubit during the error simulation phase of the simulation
```bash
python qey.py --p-bit-flip 0.5
``` 
### Number of shots (-s, --shots)
Set the number of shots to run during the simulation
```bash
python qec.py --shots 1024
```
### Run multiple simulatios (-it, --iterations)
Run multiple simulations with different bit-flip errors

**Note:** This is different from --shots, as --shots increasing the number of times the AerSimulator runs with the error occuring on the same qubits. --iterations increases the number of times the entire circuit is run. Each iteration has a bit-flip error occuring on different qubits. 
```bash
python qec.py --iterations 100
```
## Draw the circuit (-d, --draw)
Draws the generated circuit at each iteration, including the errors occuring
```bash
python qec.py --draw
```
## Helper arguments (-D, -V, --debug, --verbose)
--debug enters debug mode for easier understanding of errors
```bash
python qec.py --debug
```
--verbose sets verbose outputs to true 
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