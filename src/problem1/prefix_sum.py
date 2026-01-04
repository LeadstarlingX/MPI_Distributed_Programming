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
    Step 1: Local Prefix Sum
    Step 2: Exchange Block Sums (Sequential on Rank 0 usually, or Allgather)
    Step 3: Add offsets
    """
    # Step 1: Local Prefix Sum
    local_prefix = [] # Placeholder
    
    # Step 2: Block sums
    
    # Step 3: Add offsets
    
    return local_prefix

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Placeholder for logic
    if rank == 0:
        print(f"Running Prefix Sum with {size} processes")

if __name__ == "__main__":
    main()
