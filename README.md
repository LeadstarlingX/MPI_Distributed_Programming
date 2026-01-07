# MPI Hybrid Distributed Framework

This project contains a dual-layer implementation of distributed algorithms, combining physical cluster deployment (Python/mpi4py) with high-fidelity network simulation (C++/SimGrid).

---

## 📂 Project Structure

```bash
.
├── Makefile                # Multi-language build/run system
├── platforms/              # SimGrid Topology Definitions (XML)
│   ├── crossbar.xml        # Non-blocking all-to-all
│   ├── dragonfly.xml       # High-dimensional router network
│   ├── fat_tree.xml        # Hierarchical tree topology
│   ├── shared_backbone.xml # Single shared bus communication
│   └── torus.xml           # 2D/3D Mesh/Torus
├── src/
│   ├── common/             # Shared utilities (Python)
│   ├── problem1/           # Python Prefix Sum (Cluster Implementation)
│   └── problem2/           # C++ Manual Reduce (SimGrid Simulation)
└── README.md               # You are here
```

---

## 🏛️ Hybrid Architecture

### Problem 1: Parallel Prefix Sum (Python)
*   **Platform**: University Cluster (CentOS 7.7).
*   **Logic**: 3-step Parallel Scan (Local Sum -> Scatter/Gather Offsets -> Adjust).
*   **Tech**: Python 3.6, `mpi4py`, `numpy`.
*   **Goal**: Demonstrate real-world deployment and version compatibility.

### Problem 2: Tree-based Reduction (C++)
*   **Platform**: Local Container (SimGrid 4.1 SMPI).
*   **Logic**: Binary Tree Reduction ($O(\log N)$ communication).
*   **Tech**: C++, `MPI (smpi)`, `Makefile`.
*   **Goal**: Analyze performance across different network topologies (Fat-Tree, Dragonfly, etc.).

---

## 🔬 Experimental Results

### 1. Problem 1 Verification (Cluster)
*   **Status**: ✅ SUCCESS
*   **Nodes**: 4 processes on 172.25.1.81.
*   **Validation**: Parallel output matched sequential `np.cumsum` results.

### 2. Problem 2: Comparative Reduction (Simulation)
Comparing **Parallel Tree Reduce** vs **Sequential Gather Accumulation**.
*Result for NP=4 (Nodes):*

| Topology | Vector Size (N) | Tree Reduce (s) | Seq(Gather) (s) | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Fat-Tree** | 10 | 0.001428 | 0.000816 | ✅ Valid |
| **Fat-Tree** | 1,000 | 0.001476 | 0.000877 | ✅ Valid |
| **Fat-Tree** | 1,000,000 | 0.138623 | 0.113750 | ✅ Valid |
| **Dragonfly** | 10 | 0.001508 | 0.001016 | ✅ Valid |
| **Dragonfly** | 1,000 | 0.001566 | 0.001031 | ✅ Valid |
| **Dragonfly** | 1,000,000 | 0.136611 | 0.115901 | ✅ Valid |

> [!NOTE]
> **Performance Insight**: With a low node count (NP=4), the Sequential (Gather) approach is slightly faster than the Tree approach due to lower communication overhead. The Tree algorithm's $O(\log N)$ scaling advantage becomes significantly more apparent as the process count (NP) increases into the dozens or hundreds.

---

## 🛠️ SimGrid Performance & Calibration

To ensure the simulation timings are scientifically valid, we use **Host-Speed Calibration**.

### What is Host-Speed?
SimGrid translates the physical execution time on your laptop into a "simulated time" based on the platform's CPU power. We run a calibration benchmark once to determine the laptop's Gflop rate.

### Optimization
In the provided `Makefile`, the `bench_all` target performs **One-Time Calibration**:
1.  **Detect**: It runs a single-process simulation with `host-speed:auto` to measure the laptop's power.
2.  **Propagate**: It captures the result (e.g., `6.43Gf`) and injects it into all subsequent benchmarks for the remainder of the session.
*   **Benefits**: 
    1.  **Deterministic Results**: Ensures all comparison tests (Fat-Tree vs Dragonfly) use the exact same CPU baseline.
    2.  **Accuracy**: Automatically adapts to your laptop's current state (thermal throttling, background load) at the moment the test begins.
    3.  **Speed**: Only pays the "calibration tax" (2.5s) once, rather than on every run.

---

## 🚀 How to Run

### Problem 1 (Cluster)
*Prerequisite: Accessible MPI cluster with Python 3.6.*
```bash
make install  # Build mpi4py from source for compatibility
make p1       # Run Prefix Sum
```

### Problem 2 (Simulation)
*Prerequisite: Docker image `simgrid/tuto-smpi`.*
```powershell
# Start container
docker run -it --rm -v "${PWD}:/source" -w /source simgrid/tuto-smpi bash

# Inside container:
make bench_all NP=8 N=1000000
```
> [!NOTE]
> **NP Variable**: The number of processes defaults to **4** but can be overridden as shown above.

---

## ✅ Delivery Status
- [x] Python Prefix Sum (Correctness Verified on Cluster).
- [x] C++ Tree Reduce (Correctness Verified in Simulation).
- [x] Multi-Topology XML Infrastructure.
- [x] Final Comparative Performance Report.
