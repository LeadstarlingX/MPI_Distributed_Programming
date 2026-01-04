#!/bin/bash
set -e

echo "Running Problem 1: Prefix Sum (NP=3)"
mpiexec --oversubscribe -n 3 python3 src/problem1/prefix_sum.py

echo "-----------------------------------"
echo "Running Problem 2: Manual Reduce Benchmark (NP=3)"
mpiexec --oversubscribe -n 3 python3 src/problem2/benchmark.py
