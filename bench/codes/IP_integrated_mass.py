#==================================================================================================
#			HEADERS
#==================================================================================================
from __future__ import division
from struct import *
import numpy as np
import sys
import matplotlib
import os

import matplotlib.pyplot as plt
from pylab import *
#plt.figure( figsize=(16,8.5) )

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Data filename
folder = "../Data/"
folds = ["CLUES/16953/","CLUES/2710/", "CLUES/10909/", "BOLSHOI/"]
#Number of Mass intervals
Ns_mass = [18, 6, 7, 40]
#Labels of graphs
labels = ["CLUES 16953","CLUES 2710", "CLUES 10909", "Bolshoi"]
#Index of each LG halos
LG_index = [ [889,1107], [643,831], [675,895], False ]
#Colors array
Colors = ['red', 'green', 'blue', 'black']
#Linewidths
Linewidths = [1,1,1,2]
#Markers
Markers = ['','','','']


#==================================================================================================
#			HALOS AND PAIRS DATA
#==================================================================================================
i_fold = 0
for fold in folds:
    #IsoPairs datas
    isopairs = np.transpose( np.loadtxt( '%s%sIsoPairs_catalog.dat'%(folder,fold) ) )
    Npairs = len(isopairs[0])		#Number of pairs

    #Construction of ratio mass index and pair total mass
    RmassIndex = np.zeros((2,Npairs))
    RmassIndex[0] = isopairs[1]
    RmassIndex[1] = isopairs[5]/isopairs[2]
    RmassIndex = RmassIndex[:, np.argsort(RmassIndex[1])]
    
    AllMassPair = np.zeros((2,Npairs))
    AllMassPair[0] = isopairs[1]
    AllMassPair[1] = isopairs[2] + isopairs[5]
    AllMassPair = AllMassPair[:, np.argsort(AllMassPair[1])]

    N_mass = Ns_mass[i_fold]
    #Construction of Mass axes
    Mmin = np.min(AllMassPair[1])
    Mmax = np.max(AllMassPair[1])
    Mass_array = 10**( np.linspace( np.log10( Mmin ), np.log10( Mmax ), N_mass ) )
    Index_array = np.linspace( 0,1,N_mass )
    
    #Integrated mass distributions
    IMPD_RI = np.zeros( N_mass )
    IMPD_AM = np.zeros( N_mass )
    
    #LG halos
    RI_LG = 0
    AM_LG = 0

    #==================================================================================================
    #			HISTOGRAMS
    #==================================================================================================
    n_ri = 0
    n_am = 0
    for i in xrange(Npairs):
	#Verify rigth selection of N_mass
      	#print RmassIndex[1,i], Index_array[n_ri]
	#Ratio Mass Index---------------------------------------------------------
	if RmassIndex[1,i] >= Index_array[n_ri]:
	    IMPD_RI[n_ri] += Npairs - i
	    n_ri += 1
	if LG_index[i_fold] != False:
	    if RmassIndex[0,i] == LG_index[i_fold][0]:
		RI_LG = RmassIndex[1,i]
	    
	#Pairs Mass Index---------------------------------------------------------
	if AllMassPair[1,i] >= Mass_array[n_am]:
	    IMPD_AM[n_am] += Npairs - i
	    n_am += 1
	if LG_index[i_fold] != False:
	    if AllMassPair[0,i] == LG_index[i_fold][0]:
		AM_LG = AllMassPair[1,i]
	    
	    
    plt.subplot(211)
    plt.plot( Index_array, IMPD_RI/IMPD_RI[0], label=labels[i_fold], color = Colors[i_fold],\
    linewidth = Linewidths[i_fold], marker = Markers[i_fold] )
    plt.vlines( RI_LG, 0, 1, color = Colors[i_fold], linestyle = '--', linewidth = 0.5 )
    
    plt.subplot(212)
    plt.loglog( Mass_array, IMPD_AM/IMPD_AM[0], label=labels[i_fold], color = Colors[i_fold],\
    linewidth = Linewidths[i_fold] )
    plt.vlines( AM_LG, 1e-3, 1, color = Colors[i_fold], linestyle = '--', linewidth = 0.5 )
    
    i_fold += 1


#PLOT OF RATIO MASS INDEX ===============================================================
plt.subplot(211)
plt.title('(a)')
plt.xlabel('$M_A/M_B$')
plt.ylabel('Pairs percent')
#plt.ylim( (1e-6, 1.0) )
plt.xlim( (0, 1) )
plt.grid()
plt.legend(labels, loc='lower left')

#PLOT OF PAIR MASS FUNCTION ==============================================================
plt.subplot(212)
plt.title('(b)')
plt.xlabel('$M_A+M_B$ [$M_{\odot}$]')
plt.ylabel('Pairs percent')
plt.ylim( (1e-3, 1.0) )
plt.xlim( (1e12, 1e13) )

ticks = np.linspace(1e12, 1e13, 4)
ticks_lab = ["10$^{12}$", "4$\\times $10$^{12}$", "7$\\times$ 10$^{12}$", "10$^{13}$"]
plt.xticks( ticks, ticks_lab )
plt.grid()
#plt.legend(labels)


#plt.savefig( 'pairs_IPMF.pdf', format='pdf' )
plt.show()