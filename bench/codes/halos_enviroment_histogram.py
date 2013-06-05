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
#			FUNCTIONS
#==================================================================================================
def enviroment_r( r, n ):
    '''
    FUNCTION: Return the local enviroment in a given r coordinate
    ARGUMENTS: r - Local coordinate
	       n - Number of lambda
    RETURN:   Enviroment
	      0 - Void
	      1 - Filament
	      2 - Knot
    '''
    i = np.int(r[0]/Box_lenght*n_x)
    j = np.int(r[1]/Box_lenght*n_x)
    k = np.int(r[2]/Box_lenght*n_x)
    
    return enviroment[n][i,j,k]

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Data filename
fold="../Data/CLUES/16953/"
#fold="../Data/BOLSHOI/"
#Lambda files
#lambda_thr = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0,1.1, 1.2, 1.5]
lambda_thr = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,\
0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0,1.1, 1.2, 1.5]
#Box lenght
Box_lenght = 64.
#Number of grids in each axe
Nx = 64
n_x = 128

#==================================================================================================
#			LOADING ENVIROMENT FILE
#==================================================================================================
enviroment = np.zeros( (len(lambda_thr), n_x, n_x, n_x) )
for n in xrange(0,len(lambda_thr)):
    datos = np.loadtxt( "%s%d/enviroment_Lamb_%1.2f.dat"%(fold,Nx,lambda_thr[n]) )
    enviroment[n] = datos.reshape([n_x,n_x,n_x])
    
#==================================================================================================
#			HALOS AND PAIRS DATA
#==================================================================================================
#Halos Datas
halos = np.transpose( np.loadtxt( '%shalos_catalog.dat'%fold ) )
Nhalos = len(halos[0])		#Number of halos

#Pairs datas
pairs = np.transpose( np.loadtxt( '%sPairs_catalog.dat'%fold ) )
Npairs = len(pairs[0])		#Number of pairs

#Isolated Pairs datas
isop = np.transpose( np.loadtxt( '%sIsoPairs_catalog.dat'%fold ) )
Nisop = len(isop[0])		#Number of isolated pairs

#Log10 of mass cut
Mlog10 = 11.0

#==================================================================================================
#			HISTOGRAMS
#==================================================================================================
Halos_hist = np.zeros((len(lambda_thr),6))
for n in xrange(0,len(lambda_thr)):
    for i in xrange(0, Nhalos):
	for l in xrange(0,3):
	    if enviroment_r( halos[1:4,i], n ) == l and np.log10(halos[8,i])>Mlog10:
		Halos_hist[n,l] += 1
		Halos_hist[n,l+3] += halos[8,i]

M_tot = np.sum(Halos_hist[0,3:6])
Nhalos = np.sum(Halos_hist[0,0:3])

plt.figure(figsize=(16,8.5))
#plt.title('Histograms of halos enviroment')
plt.plot( lambda_thr, Halos_hist[:,0]/Nhalos, label='Number of Halos in voids', marker = 'o', color='blue' )
plt.plot( lambda_thr, Halos_hist[:,3]/M_tot, 's--', label='Mass in voids', color='blue' )

plt.plot( lambda_thr, Halos_hist[:,1]/Nhalos, label='Number of Halos in sheets', marker = 'o', color='red' )
plt.plot( lambda_thr, Halos_hist[:,4]/M_tot, 's--', label='Mass in sheets', color='red' )

plt.plot( lambda_thr, Halos_hist[:,2]/Nhalos, label='Number of Halos in filaments', marker = 'o', color='green' )
plt.plot( lambda_thr, Halos_hist[:,5]/M_tot, 's--', label='Mass in filaments', color='green' )

plt.xlabel('$\Lambda_{th}$')
plt.ylabel('Halos %')
plt.ylim( (0,1) )
plt.legend( bbox_to_anchor=(0., 1.1, 1., 0.0), borderaxespad=0, loc='upper left', ncol=3, mode="expand", handlelength=2, labelspacing=0)
plt.grid()
plt.savefig('fig1', format = 'pdf')
