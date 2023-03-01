from mpi4py import MPI
import numpy as np
from datetime import datetime

array_size = 10
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_proc = comm.Get_size()
result_array = np.array([])

if rank == 0:
    array_a = np.random.randint(1, 100, array_size)
    array_b = np.random.randint(1, 100, array_size)
    print ('Array a: ', array_a)
    print ('Array b: ', array_b)
    start_time = datetime.now()
    a_chunks = np.array_split(array_a, n_proc-1)
    b_chunks = np.array_split(array_b, n_proc-1)
    for i in range(len(a_chunks)):
        comm.send(a_chunks[i], dest=i+1, tag=1)
        comm.send(b_chunks[i], dest=i+1, tag=2)

    for i in range(len(a_chunks)):
        sub_result = comm.recv(source= i+1)
        result_array = np.append(result_array, sub_result)

    elasped_time = datetime.now() - start_time
    print ('Elasped time ', elasped_time)

    print('Result array: ', result_array)


else:
    sub_array_a = comm.recv(source= 0,tag=1)
    sub_array_b = comm.recv(source= 0,tag=2)
    result = sub_array_a + sub_array_b
    comm.send(result, dest=0)