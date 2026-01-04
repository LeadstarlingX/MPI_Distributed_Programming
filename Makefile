# Default number of processes
NP ?= 4

# Use the specific python binary found in host shell (which is 3.6.10)
PYTHON := /usr/bin/python
PYTHON_VERSION := 3.6

# Ensure user site-packages are visible for the correct version
PYTHONPATH := $(HOME)/.local/lib/python$(PYTHON_VERSION)/site-packages:$(PYTHONPATH)
export PYTHONPATH

all: p1 p2

install:
	$(PYTHON) -m pip install --user --upgrade pip
	$(PYTHON) -m pip install --user numpy
	$(PYTHON) -m pip install --user --force-reinstall --no-binary=mpi4py "mpi4py==3.1.6"

p1:
	@echo "Running Problem 1 (Prefix Sum) with NP=$(NP)..."
	@echo "Using $(PYTHON) (Version: $$($(PYTHON) --version))"
	mpiexec -n $(NP) -genv PYTHONPATH $(PYTHONPATH) $(PYTHON) src/problem1/prefix_sum.py

p2:
	@echo "Running Problem 2 (Benchmark) with NP=$(NP)..."
	@echo "Using $(PYTHON) (Version: $$($(PYTHON) --version))"
	mpiexec -n $(NP) -genv PYTHONPATH $(PYTHONPATH) $(PYTHON) src/problem2/benchmark.py

test_p2:
	@echo "Running Problem 2 Correctness Test with NP=$(NP)..."
	mpiexec -n $(NP) -genv PYTHONPATH $(PYTHONPATH) $(PYTHON) src/problem2/manual_reduce.py

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
