# MPI Distributed Programming Assignment

Implementation of Prefix Sum and Tree-based Reduce using mpi4py.

## Requirements
- Python 3
- mpi4py
- OpenMPI (System installed)

## Usage

### 1. Parallel Prefix Sum (Problem 1)
```bash
mpiexec -n <NP> python3 src/problem1/prefix_sum.py
```

### 2. Manual Tree Reduce & Benchmark (Problem 2)
```bash
mpiexec -n <NP> python3 src/problem2/benchmark.py
```

### 3. SimGrid Simulation
SimGrid configurations are provided in `simgrid/`. 
To run with SimGrid (if SMPI/Python bindings are configured):
```bash
smpirun -platform simgrid/platform.xml -hostfile ... python3 src/problem2/benchmark.py
```

## Running Tests
Execute the helper script:
```bash
bash run_tests.sh
```
