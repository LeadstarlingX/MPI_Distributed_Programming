# problem2/benchmark.py
from mpi4py import MPI
import numpy as np
import time
import sys
import os

# Add common directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import utils
from problem2.manual_reduce import manual_reduce

def run_benchmark():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Test cases: Array Size N
    sizes = [1000, 10000, 100000, 1000000]
    
    if rank == 0:
        print(f"{'Structure':<15} | {'Size':<10} | {'Processes':<10} | {'Seq Time (s)':<15} | {'Par Time (s)':<15}")
        print("-" * 80)
        
    for N in sizes:
        # Generate data
        local_vec = np.random.randint(0, 10, N // size if N >= size else N).astype(np.int32)
        full_data = None
        if rank == 0:
            full_data = np.random.randint(0, 10, N).astype(np.int32)
            
        comm.Barrier()
        
        # 1. Sequential Time (Only Rank 0 measures this for baseline)
        seq_time = 0.0
        if rank == 0:
            start = MPI.Wtime()
            _ = np.sum(full_data)
            end = MPI.Wtime()
            seq_time = end - start
            
        # Broadcast seq_time to all if needed, or just keep on Rank 0
        
        # 2. Parallel Manual Reduce Time
        # We need to distribute data or just use random local data
        # For fair comparison, we should really scatter, but assuming local_vec is already the chunk.
        
        comm.Barrier()
        start_par = MPI.Wtime()
        
        recvbuf = np.zeros(1, dtype=np.int32) if rank == 0 else None
        # Sum local first? Yes, reduce assumes we are reducing a value or vector. 
        # Requirement: "receive arrays... adds... sends resulting array"
        # If we reduce a single scalar per process vs vector:
        # The prompt says "receives arrays... adds... resulting array". Implies vector reduction.
        # But if we want to sum N numbers, typical MPI way is each sums local chunk -> scalar, then Reduce scalars.
        # However, "array dimension" in table implies we might be reducing arrays of size N? NO.
        # "Prefix sum of sequence"... "Parallel version of prefix sum".
        # For Reduce: "root of reduction... data type is MPI_INT".
        # "receive arrays... adds...". This implies we are doing an element-wise sum of arrays? 
        # OR it means we are reducing a large array where each process has a chunk?
        # Usually "Reduce" reduces inputs from all process to one. 
        # If input is an array of size M, output is array of size M (element-wise sum).
        # Let's assume we are reducing arrays of size M = 10 (or whatever) to show "array dimension".
        # Wait, "Execution time... for different array sizes". 
        # This usually means the workload size.
        # If we reduce a SCALAR (sum of N numbers), the message size is 1 INT.
        # If we reduce a VECTOR (element-wise sum of N-arrays), message size is N INTs.
        # Given "receives arrays... adds... sends resulting array", it likely means Vector Reduction.
        
        # Let's treat N as the Vector Length.
        
        # Adjust local_vec to be size N (all processes have vector of size N)
        # Or N is total elements and we sum them? 
        # "Prefix sum" was Problem 1.
        # Problem 2 is "Reduce operation... data type MPI_INT... receive arrays... adds...".
        # This strongly suggests Vector Reduction of size N.
        
        # So each process creates array of size N.
        local_arr = np.random.randint(0, 10, N).astype(np.int32)
        recv_arr = np.zeros(N, dtype=np.int32) if rank == 0 else None
        
        manual_reduce(local_arr, recv_arr, op=MPI.SUM, root=0, comm=comm)
        
        end_par = MPI.Wtime()
        par_time = end_par - start_par
        
        if rank == 0:
            print(f"{'Tree-Reduce':<15} | {N:<10} | {size:<10} | {seq_time:.6f}          | {par_time:.6f}")

if __name__ == "__main__":
    run_benchmark()
