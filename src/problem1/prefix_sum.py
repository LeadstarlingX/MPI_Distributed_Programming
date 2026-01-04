"""
Problem 1: Parallel Prefix Sum
This file checks correctness of a distributed prefix sum algorithm on a generated dataset.
"""
# problem1/prefix_sum.py
from mpi4py import MPI
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import utils

def prefix_mpi(local_data, comm):
    """
    Computes distributed prefix sum using a 3-step algorithm.
    """
    import numpy as np
    
    local_prefix = np.cumsum(local_data)
    local_sum = local_prefix[-1]
    
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    block_sums = comm.gather(local_sum, root=0)
    
    block_offset = 0
    if rank == 0:
        offsets = np.zeros(size, dtype=int)
        current_acc = 0
        for i in range(size):
            offsets[i] = current_acc
            current_acc += block_sums[i]
            
        block_offset = offsets
        
    local_offset = comm.scatter(block_offset, root=0)
    final_prefix = local_prefix + local_offset
    
    return final_prefix

def main():
    """
    Main execution function for Parallel Prefix Sum.
    """
    import numpy as np
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    N = 12
    local_data = None
    
    if rank == 0:
        full_data = utils.generate_data(N)
        print(f"Rank 0: Generated data: {full_data}")
        chunks = np.array_split(full_data, size)
    else:
        chunks = None
        
    local_data = comm.scatter(chunks, root=0)
    print(f"Rank {rank}: Received chunk {local_data}")
    
    result_local = prefix_mpi(local_data, comm)
    print(f"Rank {rank}: Local prefix result (adjusted) {result_local}")
    
    final_result = comm.gather(result_local, root=0)
    
    if rank == 0:
        final_flat = np.concatenate(final_result)
        print(f"Final Parallel Result: {final_flat}")
        
        is_correct = utils.verify_prefix_sum(full_data, final_flat)
        print(f"Verification: {'SUCCESS' if is_correct else 'FAILURE'}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
