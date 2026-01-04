"""
Problem 2: Manual Tree Reduce
This file contains the implementation of a custom tree-based reduction function mimicking MPI_Reduce.
"""
# problem2/manual_reduce.py
from mpi4py import MPI
import numpy as np

def manual_reduce(sendbuf, recvbuf, op=MPI.SUM, root=0, comm=MPI.COMM_WORLD):
    """
    Implementation of MPI_Reduce using tree-based communication.
    Toplogy:
      rank i children: 2*i+1, 2*i+2
      rank i parent: (i-1)//2
    """
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    import numpy as np
    
    acc = np.copy(sendbuf)
    
    left = 2 * rank + 1
    right = 2 * rank + 2
    
    if left < size:
        temp_recv = np.empty_like(sendbuf)
        comm.Recv(temp_recv, source=left, tag=111)
        acc += temp_recv
        
    if right < size:
        temp_recv = np.empty_like(sendbuf)
        comm.Recv(temp_recv, source=right, tag=111)
        acc += temp_recv
        
    if rank == root:
        if recvbuf is not None:
             recvbuf[:] = acc[:]
    else:
        parent = (rank - 1) // 2
        comm.Send(acc, dest=parent, tag=111)

def main():
    """
    Main execution function/Test for Manual Reduce.
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    N = 10
    local_vec = np.random.randint(0, 10, N).astype(np.int32)
    
    std_result = np.zeros(N, dtype=np.int32) if rank == 0 else None
    comm.Reduce(local_vec, std_result, op=MPI.SUM, root=0)
    
    manual_result = np.zeros(N, dtype=np.int32) if rank == 0 else None
    manual_reduce(local_vec, manual_result, op=MPI.SUM, root=0, comm=comm)
    
    if rank == 0:
        if np.array_equal(std_result, manual_result):
            print("Rank 0: Manual Tree Reduce SUCCESS")
            print(f"Result: {manual_result[:5]}...")
        else:
            print("Rank 0: Manual Tree Reduce FAILURE")
            print(f"Std: {std_result}")
            print(f"Man: {manual_result}")
