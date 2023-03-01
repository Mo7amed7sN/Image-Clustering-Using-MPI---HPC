import math
import csv
import time
import numpy as np
import collections
from mpi4py import MPI
from scipy.spatial import distance
from scipy import misc
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
cluster_id = []
num_clusters = 3

#print("Enter the number of clusters you want to make: ")
#num_clusters = input()
#num_clusters = int(num_clusters)
array_cluster = np.array([])
#generate centroid
img_1d = np.array([])
centroid = np.array([])
#test_list = [10,52,38,44,120,85,10,35,98,74,95,14,0,75,22,32,23,25,27,21,14]
k = comm.bcast(num_clusters, root=0)
if rank == 0:
    img = np.array(misc.imread('/home/hpcuser/Desktop/images.jpg', True))
	new_img = img.flatten()
	print("image size : " + str(len(new_img)))

	centroid = np.random.randint(low=20, high=120, size=num_clusters)
	centroids = comm.bcast(centroid, root=0)
	img_split = np.array_split(new_img, size-1)

	for i in range(len(img_split)):
		comm.send(img_split[i], dest=i + 1)


	#print ("image length : "+ str(len(new_img)))

	for i in range(size-1):
		ee = comm.recv(source=i + 1)
		print(" length ee: " + str(i+1) + str(len(ee)))

		cluster_id.append(ee)
	print(" length of cluster id: " + str(len(cluster_id[0][:])))
	#print("cluster_ID")
	#print(cluster_id)
	#recive data
	print("aaa")


else:
	dst = []  # store min destance in list
	sub_array_img = comm.recv(source=0)
	d = 10000
	kk = comm.bcast(centroid, root=0)
	#print("kk")
	#print(kk)
	cluster_num = -1

	#print("len of sub")
	#print(len(sub_array_img))
	for i in range(len(sub_array_img)):
	#	print("sub")
	#	print(sub_array_img[i])
		for j in range(len(kk)):
			x = int(np.abs(sub_array_img[i]-kk[j]))
	#		print ("destance")
	#		print(x)
			if x < d:
				d = x
				cluster_num = j
		dst.append(cluster_num)

	#print(dst)
	#print("fff")
	comm.send(dst, dest=0)
	print("vvv")


'''
	sub_array_img = comm.recv(source = 0)
	for i in range (len(sub_array_img)):
		for j in range (len (kk)):
'''

'''
	for i in range (k):
		for j in range (len(sub_array_img)):
			dst = distance.euclidean(centroids[0], sub_array_img[j])
			break
	print(dst)
'''

'''2d to 1d array
b = np.reshape(a, (1,np.product(a.shape)))
gray scale 
imread(path , true )
cul distance 
from scipy.spatial import distance
a = (1, 2, 3)
b = (4, 5, 6)
dst = distance.euclidean(a, b)

a =np.array ([[1, 2, 3],[5,6,7],[10,20,52]])
b = (4, 5, 6)
h = np.product(a.shape)
c = np.reshape(a, (1,np.product(a.shape)))
print(a)
print(c[0][2])
np.random.randint(low=20, high=150, size=k)
'''