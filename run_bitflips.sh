# Runs mutiple bit flip simulations with the parameters specified in qec.py. See qec.py for more details on the parameters that can be set.
#!/bin/bash

# Run bit flip with 0% bit flip probability
echo "Running bit flip with 0% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.00

# Run bit flip with 1% bit flip probability
echo "Running bit flip with 1% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.01

# Run bit flip with 5% bit flip probability
echo "Running bit flip with 5% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.05

# Run bit flip with 10% bit flip probability
echo "Running bit flip with 10% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.10

# Run bit flip with 20% bit flip probability
echo "Running bit flip with 20% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.20

# Run bit flip with 25% bit flip probability
echo "Running bit flip with 25% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.25

# Run bit flip with 33% bit flip probability
echo "Running bit flip with 33% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.33

# Run bit flip with 50% bit flip probability
echo "Running bit flip with 50% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.50

# Run bit flip with 67% bit flip probability
echo "Running bit flip with 67% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.67

# Run bit flip with 75% bit flip probability
echo "Running bit flip with 75% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.75

# Run bit flip with 80% bit flip probability
echo "Running bit flip with 80% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.80

# Run bit flip with 90% bit flip probability
echo "Running bit flip with 90% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.90

# Run bit flip with 95% bit flip probability
echo "Running bit flip with 95% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.95

# Run bit flip with 99% bit flip probability
echo "Running bit flip with 99% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 0.99

# Run bit flip with 100% bit flip probability
echo "Running bit flip with 100% bit flip probability"
python3 qec.py -v 1 -s 1024 -it 1000 -p 1.00
