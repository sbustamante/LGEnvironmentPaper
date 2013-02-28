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
#Data filename
folder = "../Data/"
folds = ["CLUES/16953/","CLUES/2710/", "CLUES/10909/", "BOLSHOI/"]
#Box lenght
Box_lenght = 64.
#Number of Mass intervals
N_mass = 15

plt.figure( figsize=(16,8.5) )
#==================================================================================================
#			HALOS AND PAIRS DATA
#==================================================================================================
for fold in folds:
    #Halos Datas
    halos = np.transpose( np.loadtxt( '%s%shalos_catalog.dat'%(folder,fold) ) )
    Nhalos = len(halos[0])		#Number of halos
    
    #Pairs datas
    pairs = np.transpose( np.loadtxt( '%s%sPairs_catalog.dat'%(folder,fold) ) )
    Npairs = len(pairs[0])		#Number of pairs
    
    MminPairs = np.min(halos[8, [pairs[1,:]]] + halos[8, [pairs[4,:]]])
    MmaxPairs = np.max(halos[8, [pairs[1,:]]] + halos[8, [pairs[4,:]]])
    
    Mass_array = 10**( np.linspace( np.log10( 2*MminPairs ), np.log10( MmaxPairs ), N_mass ) )
    Mass_count = np.zeros( N_mass )

    #==================================================================================================
    #			HISTOGRAMS
    #==================================================================================================
    for i in xrange(0, Npairs):
	for n in xrange(0,N_mass-1):
	    i1 = pairs[1,i]
	    i2 = pairs[4,i]
	    if halos[8,i1] + halos[8,i2] >= Mass_array[n] and halos[8,i1] + halos[8,i2] < Mass_array[n+1]:
		Mass_count[n] += 1
    plt.semilogy( Mass_array, Mass_count/np.sum(Mass_count), label=fold, marker = 'o' )
    
plt.title('Histograms of halo pairs mass')
plt.xlabel('Mass $M_{\odot}$')
plt.ylabel('Halo pairs %')
plt.xlim((1e12,1e13))
plt.legend()
plt.grid()
plt.savefig( 'pairs_histogram.pdf', format='pdf' )
plt.show()