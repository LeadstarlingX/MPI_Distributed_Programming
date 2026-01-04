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
    
    # Initialize accumulator with local data
    # We assume sendbuf is a numpy array. 
    # recvbuf is where result goes on root.
    # We need a temporary buffer equal to sendbuf size/type.
    
    # For simplicity, assume sendbuf is a numpy array or scalar.
    # If scalar, wrap/unwrap. But assume numpy for assignment.
    import numpy as np
    
    # Local accumulator
    acc = np.copy(sendbuf)
    
    # Children
    left = 2 * rank + 1
    right = 2 * rank + 2
    
    # Receive from Left
    if left < size:
        # We need to know the size of data to recv? 
        # In MPI_Reduce, count/datatype are known. Here rely on numpy auto-detect or logic.
        # sendbuf.shape provides the expected shape.
        temp_recv = np.empty_like(sendbuf)
        comm.Recv(temp_recv, source=left, tag=111)
        acc += temp_recv
        
    # Receive from Right
    if right < size:
        temp_recv = np.empty_like(sendbuf)
        comm.Recv(temp_recv, source=right, tag=111)
        acc += temp_recv
        
    # Send to Parent or Store Result
    if rank == root:
        # We are root, result is in acc.
        # Copy to recvbuf.
        if recvbuf is not null: # In mpi4py recvbuf can be None on non-root, but here we are root.
             # Ensure recvbuf is suitable (mutable).
             recvbuf[:] = acc[:]
    else:
        parent = (rank - 1) // 2
        comm.Send(acc, dest=parent, tag=111)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Generate random vector
    N = 10
    local_vec = np.random.randint(0, 10, N).astype(np.int32)
    # print(f"Rank {rank}: {local_vec}")
    
    # Verify with standard Reduce to check correctness
    std_result = np.zeros(N, dtype=np.int32) if rank == 0 else None
    comm.Reduce(local_vec, std_result, op=MPI.SUM, root=0)
    
    # Manual Reduce
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
