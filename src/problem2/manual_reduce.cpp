#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include <numeric>

/**
 * Parallel Tree Reduction Implementation
 * O(log N) communication steps.
 */
void reduce_tree(const int* send_data, int* recv_data, int count, MPI_Comm communicator) {
    int rank, size;
    MPI_Comm_rank(communicator, &rank);
    MPI_Comm_size(communicator, &size);

    std::vector<int> acc(send_data, send_data + count);

    int left = 2 * rank + 1;
    int right = 2 * rank + 2;

    if (left < size) {
        std::vector<int> temp(count);
        MPI_Recv(temp.data(), count, MPI_INT, left, 0, communicator, MPI_STATUS_IGNORE);
        for (int i = 0; i < count; i++) acc[i] += temp[i];
    }
    if (right < size) {
        std::vector<int> temp(count);
        MPI_Recv(temp.data(), count, MPI_INT, right, 0, communicator, MPI_STATUS_IGNORE);
        for (int i = 0; i < count; i++) acc[i] += temp[i];
    }

    if (rank == 0) {
        if (recv_data) memcpy(recv_data, acc.data(), count * sizeof(int));
    } else {
        int parent = (rank - 1) / 2;
        MPI_Send(acc.data(), count, MPI_INT, parent, 0, communicator);
    }
}

/**
 * Sequential Baseline Implementation (Provided by User)
 * Accumulates all data on Rank 0 via MPI_Gather.
 */
void reduce_sequential(const int* send_data, int* recv_data, int count, MPI_Comm communicator) {
    int my_rank, com_size;
    MPI_Comm_rank(communicator, &my_rank);
    MPI_Comm_size(communicator, &com_size);

    int* gather_buffer = NULL;
    if (my_rank == 0) {
        gather_buffer = (int*) calloc(count * com_size, sizeof(int));
    }

    MPI_Gather(send_data, count, MPI_INT, gather_buffer, count, MPI_INT, 0, communicator);

    if (my_rank == 0) {
        memset(recv_data, 0, count * sizeof(int));
        for (int p = 0; p < com_size; p++)
            for (int i = 0; i < count; i++)
                recv_data[i] += gather_buffer[count * p + i];
        free(gather_buffer);
    }
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int count = 1000; // Default
    if (argc > 1) count = atoi(argv[1]);

    std::vector<int> send_array(count, rank);
    std::vector<int> recv_tree(rank == 0 ? count : 0);
    std::vector<int> recv_seq(rank == 0 ? count : 0);

    // Warm-up & Timing: Tree Reduce
    MPI_Barrier(MPI_COMM_WORLD);
    double start_tree = MPI_Wtime();
    reduce_tree(send_array.data(), rank == 0 ? recv_tree.data() : NULL, count, MPI_COMM_WORLD);
    double end_tree = MPI_Wtime();

    // Warm-up & Timing: Sequential Reduce
    MPI_Barrier(MPI_COMM_WORLD);
    double start_seq = MPI_Wtime();
    reduce_sequential(send_array.data(), rank == 0 ? recv_seq.data() : NULL, count, MPI_COMM_WORLD);
    double end_seq = MPI_Wtime();

    if (rank == 0) {
        // Verification
        bool correct = true;
        // Expected sum for each index: sum from 0 to size-1 = (size * (size-1)) / 2
        int expected = (size * (size - 1)) / 2;
        for (int i = 0; i < count; i++) {
            if (recv_tree[i] != expected || recv_seq[i] != expected) {
                correct = false;
                break;
            }
        }

        printf("N: %d | Nodes: %d | Tree: %.6fs | Seq(Gather): %.6fs | Valid: %s\n", 
               count, size, (end_tree - start_tree), (end_seq - start_seq), 
               correct ? "YES" : "NO");
    }

    MPI_Finalize();
    return 0;
}
