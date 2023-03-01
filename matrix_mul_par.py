from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_proc = comm.Get_size()


def sub_mat_vec_mul(mat, vec):
    result_mat = []
    for row in mat:
        local_sum = 0
        for element in range(len(row)):
            local_sum += row[element] * vec[element]
        result_mat.append(local_sum)
    return result_mat


if rank == 0:
    matrixa = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]).reshape(4, 4)
    matrixb = np.array([1, 2, 3, 4])

    result_matrix = np.array([])

    print('Matrix a: \n', matrixa)
    print('Matrix b: \n', matrixb)

    matrixa_chunks = np.array_split(matrixa, n_proc - 1)

    for i in range(n_proc - 1):
        comm.isend(matrixa_chunks[i], dest=i + 1)
        print("Matrix A chunk {0}, is {1}".format(i, matrixa_chunks[i]))
        comm.isend(matrixb, dest=i + 1)

    for i in range(1, n_proc):
        sub_matrix = comm.recv(source=i)
        result_matrix = np.append(result_matrix, sub_matrix)

    print('Result matrix: ', result_matrix)

else:
    rec_req1 = comm.irecv(source=0)
    rec_req2 = comm.irecv(source=0)
    result = sub_mat_vec_mul(rec_req1.wait(), rec_req2.wait())
    comm.send(result, dest=0)
