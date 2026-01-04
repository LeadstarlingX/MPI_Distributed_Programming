# MPI Distributed Programming Assignment

This project implements fundamental distributed algorithms using **Python** and **mpi4py**. It focuses on two core problems: Parallel Prefix Sum and a Manual Tree-based Reduction, emphasizing correct distributed logic, cluster compatibility, and performance analysis.

---

## 🏛️ Project Architecture

The project is structured for modularity and scalability:

```text
├── src/
│   ├── common/         # Data generation and verification helpers
│   ├── problem1/       # Parallel Prefix Sum implementation
│   └── problem2/       # Manual Tree Reduce & Benchmarking
├── Makefile            # Cluster-aware automation (Install, Run, Test)
├── run_tests.sh        # CI/CD Smoke tests
└── simgrid/            # Simulation configurations (XML)
```

---

## 🔬 Implementation Details

### Problem 1: Parallel Prefix Sum
Computes the cumulative sum of a distributed vector using a highly efficient **3-step Parallel Scan** algorithm:

1.  **Local Scan (`np.cumsum`)**: Each process computes the prefix sum of its own data slice.
2.  **Global Offset Calculation**: 
    *   Processes `Gather` their individual total sums to Rank 0.
    *   Rank 0 computes the cumulative offsets for each rank.
    *   Offsets are `Scatter`ed back to each process.
3.  **Local Adjustment**: Each process adds its assigned offset to its local prefix sum to achieve the global distributed result.

### Problem 2: Manual Tree-based Reduce
Replaces the standard `MPI_Reduce` with a custom implementation using a **Binary Tree Topology**:

*   **Topology**: Nodes are mapped to a tree where rank $i$ has children $2i+1$ and $2i+2$.
*   **Communication**: 
    *   Leaf nodes send their data to their parents.
    *   Intermediate nodes aggregate their local data with data received from children before forwarding to their parent.
    *   The **Root (Rank 0)** performs the final aggregation.
*   **Efficiency**: Reduces time complexity from $O(N)$ (linear) to $O(\log N)$ relative to the number of processes.

---

## 🚀 Deployment on Cluster (CentOS 7.7)

The project includes advanced support for legacy cluster environments:

### Environment Compatibility
*   **Python Legality**: Code is strictly compatible with Python 3.5+ (uses `.format()` instead of f-strings).
*   **Path Management**: The `Makefile` automatically handles `PYTHONPATH` propagation to worker nodes via `mpiexec -genv`.
*   **Dependency Locking**: `make install` forces `mpi4py==3.1.6` compilation from source to ensure binary compatibility with system MPI libraries.

### Quick Start (Cluster)
```bash
# 1. Install dependencies (compiled for the cluster)
make install

# 2. Run Problem 1 (Correctness Test)
make p1

# 3. Run Problem 2 Benchmarks
make p2

# 4. Verify Problem 2 Logic explicitly
make test_p2
```

---

## 📊 Experimental Results (4-Core Cluster)

The following metrics were gathered on a university cluster using 4 distributed processes:

### Problem 1 Verification
*   **Status**: ✅ SUCCESS 
*   **Logic**: Automatic comparison between parallel output and sequential `np.cumsum`.

### Problem 2 Performance Benchmarking
| Algorithm | Vector Size ($N$) | Seq Time (s) | Par Time (s) |
| :--- | :--- | :--- | :--- |
| **Tree-Reduce** | 1,000 | 0.000040 | 0.000248 |
| **Tree-Reduce** | 10,000 | 0.000022 | 0.000385 |
| **Tree-Reduce** | 100,000 | 0.000114 | 0.003544 |
| **Tree-Reduce** | 1,000,000 | 0.000868 | 0.029818 |

> [!NOTE]
> Parallel overhead (communication latency) is significant for smaller sizes. The efficiency gains of the Tree-Reduce algorithm become more apparent as $N$ scales or when the number of processes increases significantly.

---

## 🛠️ Software Engineering Standards
*   **Git Workflow**: Developed using feature branches (`feat/...`) with atomic commits.
*   **Multi-Remote**: Configured for both **GitHub** (CI) and **University GitLab** (Clean submission).
*   **CI/CD**: Integrated with GitHub Actions for automated sanity checks on every push.
