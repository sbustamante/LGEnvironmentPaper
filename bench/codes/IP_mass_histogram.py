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
folds = ["BOLSHOI/", "CLUES/16953/","CLUES/2710/", "CLUES/10909/"]
#fold="../Data/BOLSHOI/"
#Box lenght
Box_lenght = 64.
#Number of Mass intervals
N_mass = 20

plt.figure( figsize=(16,8.5) )
#Colors
colors = ['black','green','red','blue']
#MarkerSizes
markers = [2, 8, 8, 8]
#LG index
LG_index = [ False, [889,1107], [643,831], [675,895] ]
#==================================================================================================
#			HALOS AND PAIRS DATA
#==================================================================================================
index = 0
for fold in folds:
    #Halos Datas
    halos = np.transpose( np.loadtxt( '%s%shalos_catalog.dat'%(folder,fold) ) )
    Nhalos = len(halos[0])		#Number of halos

    #Pairs datas
    pairs = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog.dat'%(folder,fold) ) )
    Npairs = len(pairs[0])		#Number of pairs

    #PairsIndex
    IndexMass = []
    #==================================================================================================
    #			HISTOGRAMS
    #==================================================================================================
    for i in xrange(0, Npairs):
	i1 = pairs[1,i]
	i2 = pairs[4,i]
	if halos[8,i1] > halos[8,i2]:
	    IndexMass.append( (i1,i2) )
	else:
	    IndexMass.append( (i2,i1) )
	    
    IndexMass = np.transpose(IndexMass)
    
    plt.loglog( halos[8,[IndexMass[0]]][0], halos[8,[IndexMass[1]]][0], '.', label=fold, markersize = markers[index], color=colors[index] )
    if LG_index[index] != False:
	plt.loglog( [halos[8,LG_index[index][0]],], [halos[8,LG_index[index][1]],], 'o', label='LG %s'%fold, markersize = 10, color=colors[index] )
    index += 1

plt.title('Dispersion diagram of isolated pairs mass')
plt.xlabel('Mass $M_{\odot}$')
plt.ylabel('Mass $M_{\odot}$')
plt.xlim( (5e11, 5e12) )
plt.ylim( (5e11, 5e12) )

axex_ticks = np.linspace( 5e11, 5e12, 10 )
axes_label = [ '5e11', '10e11', '15e11', '20e11', '25e11', '30e11', '35e11', '40e11','45e11', '50e11']
plt.xticks( axex_ticks, axes_label )
plt.yticks( axex_ticks, axes_label )

plt.legend( loc='upper left' )
plt.plot(axex_ticks, axex_ticks,'--', color='black', linewidth = 0.5)
plt.grid()
plt.savefig( 'pairs_mass.pdf', format='pdf' )
plt.show()