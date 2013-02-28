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
#fold="../Data/BOLSHOI/"
#Box lenght
Box_lenght = 64.
#Number of Mass intervals
N_mass = 20

plt.figure( figsize=(16,8.5) )
#==================================================================================================
#			HALOS AND PAIRS DATA
#==================================================================================================
for fold in folds:
    #Halos Datas
    halos = np.transpose( np.loadtxt( '%s%shalos_catalog.dat'%(folder,fold) ) )
    Nhalos = len(halos[0])		#Number of halos

    Mmin = np.min(halos[8])
    Mmax = np.max(halos[8])
    Mass_array = 10**( np.linspace( np.log10( Mmin ), np.log10( Mmax ), N_mass ) )
    Mass_count = np.zeros( N_mass )

    #==================================================================================================
    #			HISTOGRAMS
    #==================================================================================================
    for i in xrange(0, Nhalos):
	for n in xrange(0,N_mass-1):
	    if halos[8,i] >= Mass_array[n] and halos[8,i] < Mass_array[n+1]:
		Mass_count[n] += 1


    plt.loglog( Mass_array, Mass_count/Nhalos, label=fold, marker = 'o' )
plt.title('Histograms of halos mass')
plt.xlabel('Mass $M_{\odot}$')
plt.ylabel('Halos %')
plt.legend()
plt.grid()
plt.savefig( 'halos_histogram.pdf', format='pdf' )