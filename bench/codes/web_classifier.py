#==================================================================================================
#			HEADERS
#==================================================================================================
from struct import *
import numpy as np
import sys
import matplotlib
import os

import matplotlib.pyplot as plt
from pylab import *

#==================================================================================================
#			PARAMETERS
#==================================================================================================
lambda_filename="../Data/CLUES/10909/64/snap_191.s2.00.eigen_"
#lambda_filename="../Data/BOLSHOI/256/PMcrsFULL.0416.DAT.eigen_"
#lambda_thr = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0,1.1, 1.2, 1.5]
#lambda_thr = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
lambda_thr = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0,1.1, 1.2, 1.5]
#lambda_thr = [0.5]
Box_lenght = 64.

#==================================================================================================
#			FUNCTIONS
#==================================================================================================
def read_CIC_scalar(filename, double=False):
    f = open(filename, "rb")
    dumb = f.read(38)

    dumb = f.read(4)
    n_x = f.read(4)
    n_y = f.read(4)
    n_z = f.read(4)
    nodes = f.read(4)
    x0 = f.read(4)
    y0 = f.read(4)
    z0 = f.read(4)
    dx = f.read(4)
    dy = f.read(4)
    dz = f.read(4)
    dumb = f.read(4)

    n_x = (unpack('i', n_x))[0]
    n_y = (unpack('i', n_y))[0]
    n_z = (unpack('i', n_z))[0]
    nodes = (unpack('i', nodes))[0]
    dx = (unpack('f', dx))[0]
    dy = (unpack('f', dy))[0]
    dz = (unpack('f', dz))[0]
    x0 = (unpack('f', x0))[0]
    y0 = (unpack('f', y0))[0]
    z0 = (unpack('f', z0))[0]
    print n_x, n_y, n_z, nodes, dx, dy, dz

    total_nodes = n_x * n_y * n_z
    dumb = f.read(4)
    if(double==False):
        array_data = f.read(total_nodes*4)
        format_s = str(total_nodes)+'f'
    else:
        array_data = f.read(total_nodes*8)
        format_s = str(total_nodes)+'d'
    dumb = f.read(4)

    array_data = unpack(format_s, array_data)
    f.close()
    array_data  = np.array(array_data)
    new_array_data = np.reshape(array_data, (n_x,n_y,n_z), order='F')
    return new_array_data, n_x, dx

#==================================================================================================
#			CALCULATING ENVIROMENT
#==================================================================================================
lambda_val = []
for i in xrange(1,4):
    lv,n_x,dx =read_CIC_scalar("%s%d"%(lambda_filename,i))
    lambda_val.append( lv )

#n_x = n_x

enviroment = np.zeros( (len(lambda_thr), n_x, n_x, n_x) )

#Code of enviroment
# 0 -- Void
# 1 -- Sheet
# 2 -- Filament
# 3 -- Knot

for i in xrange(0,n_x):
    for j in xrange(0,n_x):
	for k in xrange(0,n_x):
	   for l in xrange(0,3):
		for n in xrange(0,len(lambda_thr)):
		    if lambda_val[l][i,j,k] >= lambda_thr[n]:
			enviroment[n,i,j,k] += 1

#Saving File
for n in xrange(0,len(lambda_thr)):
    np.savetxt("enviroment_Lamb_%1.2f.dat"%(lambda_thr[n]), enviroment[n].flatten(), fmt='%d')