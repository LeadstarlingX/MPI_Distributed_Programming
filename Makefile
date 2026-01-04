
.PHONY: all p1 p2 clean

# Default number of processes
NP ?= 4

all: p1 p2

p1:
	@echo "Running Problem 1 (Prefix Sum) with NP=$(NP)..."
	mpiexec -n $(NP) python3 src/problem1/prefix_sum.py

p2:
	@echo "Running Problem 2 (Benchmark) with NP=$(NP)..."
	mpiexec -n $(NP) python3 src/problem2/benchmark.py

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
