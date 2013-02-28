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
    i = np.int(r[0]/Box_lenght*Nx)
    j = np.int(r[1]/Box_lenght*Nx)
    k = np.int(r[2]/Box_lenght*Nx)
    return enviroment[n][i,j,k]
    
def Mass_center( r1, m1, r2, m2 ):
    '''
    FUNCTION: Return the mass center of a halo pair
    ARGUMENTS: r1, m1 - r coordinate and mass of halo 1
	       r2, m2 - r coordinate and mass of halo 2
    RETURN:   Mass center coordinate
    '''
    return (r1*m1 + r2*m2)/(m1+m2)

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Global Fold
foldglobal = '../Data/'
#Data filename
folds=["CLUES/16953/","CLUES/2710/", "CLUES/10909/"]
#Lambda files
lambda_thr = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1.0,1.1, 1.2, 1.5]
#Box lenght
Box_lenght = 64
#Number of grids in each axe
n_x = [64,128]

LG_index = [ [889,1107], [643,831], [675,895] ]

#==================================================================================================
#			LOADING ENVIROMENT FILES
#==================================================================================================
#Histograms of LG enviroments
LG_enviroment_CM = np.zeros( (len(n_x), len(folds), len(lambda_thr)) )
LG_enviroment_R2 = np.zeros( (len(n_x), len(folds), len(lambda_thr)) )

index = 0
for fold in folds:	    
    #==================================================================================================
    #			HALOS AND PAIRS DATA
    #==================================================================================================
    index_nx = 0
    for Nx in n_x:
	enviroment = np.zeros( (len(lambda_thr), Nx, Nx, Nx) )
	for n in xrange(0,len(lambda_thr)):
	    datos = np.loadtxt( "%s%s%d/enviroment_Lamb_%1.2f.dat"%(foldglobal,fold,Nx,lambda_thr[n]) )
	    enviroment[n] = datos.reshape([Nx,Nx,Nx])


	#Halos Datas
	halos = np.transpose( np.loadtxt( '%s%shalos_catalog.dat'%(foldglobal,fold) ) )
	Nhalos = len(halos[0])		#Number of halos

	#Isolated Pairs datas
	isop = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog.dat'%(foldglobal,fold) ) )
	Nisop = len(isop[0])		#Number of isolated pairs

	#==================================================================================================
	#			HISTOGRAMS
	#==================================================================================================
	for n in xrange(0,len(lambda_thr)):
	    for i in xrange(0, Nisop):
		if (isop[1,i] == LG_index[index][0] and isop[4,i] == LG_index[index][1]) or \
		(isop[1,i] == LG_index[index][1] and isop[4,i] == LG_index[index][0]):
		    r1 = halos[1:4,isop[i,0]]
		    m1 = halos[8,isop[i,0]]
		    r2 = halos[1:4,isop[i,1]]
		    m2 = halos[8,isop[i,1]]
		    Rcm = Mass_center( r1, m1, r2, m2 )
		    R2 = (r1+r2)/2
		    LG_enviroment_CM[index_nx, index, n] = enviroment_r( Rcm, n )
		    LG_enviroment_R2[index_nx, index, n] = enviroment_r( R2, n )
		    break
		    
	index_nx += 1
    print index
    index += 1

#Colors
Colors = ['red', 'green', 'blue']
#Design
Design = ['o--', 's-']
#Linewidth
Linewidths = [1,2]
#Sum
Sum_Dis = [0, 0.1, 0.2]

#Mass Center Graphic
plt.figure(figsize=(16,8.5))
#plt.title('LG enviroment sensitivity (R$_{CM}$)')
for i in xrange(0, len(folds)):
    for n in xrange(0, len(n_x)):
	plt.plot( lambda_thr, LG_enviroment_CM[n, i] + Sum_Dis[i], Design[n], color = Colors[i],\
	label='%s_%d'%(folds[i],n_x[n]), linewidth = Linewidths[n] )

plt.xlabel('$\Lambda_{th}$')
plt.ylabel('Enviroment')
plt.yticks( [-1,0,1,2,3], ['','Void', 'Filament', 'Sheet', 'Knot'] )
plt.legend( bbox_to_anchor=(0., 1.1, 1., 0.0), borderaxespad=0, loc='upper left', ncol=3, mode="expand", handlelength=2, labelspacing=0)
plt.grid()
plt.savefig('LG_enviroment_CM.pdf', format = 'pdf')
plt.close()

#Geometric Center Graphic
plt.figure(figsize=(16,8.5))
#plt.title('LG enviroment sensitivity (R$_{1/2}$)')
for i in xrange(0, len(folds)):
    for n in xrange(0, len(n_x)):
	plt.plot( lambda_thr, LG_enviroment_R2[n, i] + Sum_Dis[i], Design[n], color = Colors[i],\
	label='%s_%d'%(folds[i],n_x[n]), linewidth = Linewidths[n] )

plt.xlabel('$\Lambda_{th}$')
plt.ylabel('Enviroment')
plt.yticks( [-1,0,1,2,3], ['','Void', 'Filament', 'Sheet', 'Knot'] )
plt.legend( bbox_to_anchor=(0., 1.1, 1., 0.0), borderaxespad=0, loc='upper left', ncol=3, mode="expand", handlelength=2, labelspacing=0)
plt.grid()
plt.savefig('LG_enviroment_R2.pdf', format = 'pdf')
