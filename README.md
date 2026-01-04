# MPI Distributed Programming Project

This repository contains solutions for the Distributed Programming assignment using `mpi4py`. It implements a parallel prefix sum algorithm and a custom tree-based reduction, along with performance benchmarking.

## 📂 Project Structure

- **`src/problem1/`**: Contains `prefix_sum.py` (Parallel Prefix Sum implementation).
- **`src/problem2/`**: Contains `manual_reduce.py` (Tree-based Reduce) and `benchmark.py` (Performance comparison).
- **`src/common/`**: Shared utility functions for data generation and verification.
- **`simgrid/`**: XML configuration files for SimGrid simulations.
- **`Makefile`**: Shortcuts for running tests and benchmarks.

## 🚀 How to Run

### Prerequisites
- Python 3.x
- MPI implementation (OpenMPI, MPICH)
- `mpi4py` library (`pip install mpi4py`)
- `numpy` library (`pip install numpy`)

### Using Make (Recommended)

Run Problem 1 (Prefix Sum):
```bash
make p1
```

Run Problem 2 (Benchmark):
```bash
make p2
```

Run Both:
```bash
make all
```

Change number of processes (e.g., to 8):
```bash
make p1 NP=8
```

### Manual Execution

**Problem 1:**
```bash
mpiexec -n 4 python3 src/problem1/prefix_sum.py
```

**Problem 2:**
```bash
mpiexec -n 4 python3 src/problem2/benchmark.py
```

## 🧪 Testing on University Server (CentOS 7.7)

1.  **Connect to the Cluster**:
    Use MobaXterm or your terminal to SSH into the head node.
    ```bash
    ssh username@cluster-address
    ```

2.  **Clone the Repository**:
    ```bash
    git clone git@github.com:LeadstarlingX/MPI_Distributed_Programming.git
    cd MPI_Distributed_Programming
    ```

3.  **Load Environment (If required)**:
    Some university clusters require loading modules. Check if you need to run:
    ```bash
    module load mpi/openmpi-x.x
    module load python/3.x
    ```

4.  **Install/Check Dependencies**:
    Ensure `mpi4py` is installed in your user environment:
    ```bash
    pip3 install --user mpi4py numpy
    ```

5.  **Run**:
    ```bash
    make all
    ```
