"""
Problem 2: Benchmark
This file measures and compares execution time between Sequential Sum and the Manual Tree Reduce.
"""
# problem2/benchmark.py
from mpi4py import MPI
import numpy as np
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import utils
from problem2.manual_reduce import manual_reduce

def run_benchmark():
    """
    Executes the benchmarking logic comparing Sequential Sum vs Manual Tree Reduce.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    sizes = [1000, 10000, 100000, 1000000]
    
    if rank == 0:
        print("{:<15} | {:<10} | {:<10} | {:<15} | {:<15}".format('Structure', 'Size', 'Processes', 'Seq Time (s)', 'Par Time (s)'))
        print("-" * 80)
        
    for N in sizes:
        full_data = None
        if rank == 0:
            full_data = np.random.randint(0, 10, N).astype(np.int32)
            
        comm.Barrier()
        
        # Sequential timing
        seq_time = 0.0
        if rank == 0:
            start = MPI.Wtime()
            _ = np.sum(full_data)
            end = MPI.Wtime()
            seq_time = end - start
            
        comm.Barrier()
        
        # Parallel timing
        start_par = MPI.Wtime()
        
        # In a standard MPI_Reduce benchmark, each rank has an array of size N
        # and we perform element-wise reduction.
        local_arr = np.random.randint(0, 10, N).astype(np.int32)
        recv_arr = np.zeros(N, dtype=np.int32) if rank == 0 else None
        
        manual_reduce(local_arr, recv_arr, op=MPI.SUM, root=0, comm=comm)
        
        comm.Barrier()
        end_par = MPI.Wtime()
        
        par_time = end_par - start_par
        
        if rank == 0:
            print("{:<15} | {:<10} | {:<10} | {:.6f}          | {:.6f}".format('Tree-Reduce', N, size, seq_time, par_time))

if __name__ == "__main__":
    run_benchmark()
