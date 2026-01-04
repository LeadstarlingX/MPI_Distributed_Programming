# problem1/prefix_sum.py
from mpi4py import MPI
import sys
import os

# Add common directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import utils

def prefix_mpi(local_data, comm):
    """
    Computes distributed prefix sum.
    """
    import numpy as np
    
    # Step 1: Local Prefix Sum
    # local_data is a numpy array.
    local_prefix = np.cumsum(local_data)
    
    # Step 2: Exchange Block Sums
    # We need the total sum of this block to send to others
    local_sum = local_prefix[-1]
    
    # Gather all local_sums to Rank 0 (or Allgather to everyone)
    # The requirement says: "In the second step... sequential... prefix sum computed over array of block sums"
    # We can use Allgather so every process knows the offsets, or Gather to 0, calc, then Scatter.
    # Given "sequential implementation provided... loop... full dependency chain", let's Gather to 0, 
    # compute offsets, then scatter/bcast offsets.
    
    size = comm.Get_size()
    rank = comm.Get_rank()
    
    # Gather local sums (each process sends 1 float/int)
    # block_sums will be significant on Rank 0
    block_sums = comm.gather(local_sum, root=0)
    
    block_offset = 0
    if rank == 0:
        # Sequential prefix sum on block_sums (exclude last element for offsets? No, we need offset for block `i`)
        # offset for block 0 is 0.
        # offset for block i is sum(block_sums[0]...block_sums[i-1])
        
        # Calculate offsets
        offsets = np.zeros(size, dtype=int)
        current_acc = 0
        for i in range(size):
            offsets[i] = current_acc
            current_acc += block_sums[i]
            
        block_offset = offsets
        
    # Scatter the offsets back to processes
    # We use scatter. rank 0 sends `offsets[i]` to rank `i`.
    local_offset = comm.scatter(block_offset, root=0)
    
    # Step 3: Add offsets
    # Add local_offset to all elements in local_prefix
    final_prefix = local_prefix + local_offset
    
    return final_prefix

def main():
    import numpy as np
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    N = 12 # Small test size, divisible by 3 and 4 -> 12/3 = 4 elements per process (if size=3)
    # Ideally N should be large and passed as arg, but for skeleton we fix or parse arg.
    
    local_data = None
    
    if rank == 0:
        # Generate Data
        full_data = utils.generate_data(N)
        print(f"Rank 0: Generated data: {full_data}")
        
        # Scatter needs equal chunks if using simple Scatter. 
        # mpi4py Scatter handles numpy arrays if contiguous.
        # We assume N is divisible by size for this assignment simplicity or handle separately.
        chunks = np.array_split(full_data, size)
    else:
        chunks = None
        
    # Scatter
    local_data = comm.scatter(chunks, root=0)
    print(f"Rank {rank}: Received chunk {local_data}")
    
    # Run Prefix Sum
    result_local = prefix_mpi(local_data, comm)
    print(f"Rank {rank}: Local prefix result (adjusted) {result_local}")
    
    # Gather back
    final_result = comm.gather(result_local, root=0)
    
    if rank == 0:
        # Flatten
        final_flat = np.concatenate(final_result)
        print(f"Final Parallel Result: {final_flat}")
        
        # Verify
        is_correct = utils.verify_prefix_sum(full_data, final_flat)
        print(f"Verification: {'SUCCESS' if is_correct else 'FAILURE'}")

if __name__ == "__main__":
    main()
