# -*- coding: utf-8 -*-
#!/usr/bin/env python

import numpy as np
import sys
import matplotlib.pylab as plt

#==================================================================================================
#			FUNCTIONS
#==================================================================================================
#Cutting in X axe
def CutX( X, thick, plot=True, color='black' ):
    #Sorting in x axe
    argx = list( np.argsort( datos[1] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if X<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(X - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[1][i] >= X and i1==0:
	    i1 = i
	if datos[1][i] >= X + thick and i2==-1:
	    i2 = i
	    break
	    
    #Plotting results
    if plot == True:
	plt.title('Cut in X axes between %3.1f and %3.1f'%(X, X + thick))
	plt.plot( datos[2][i1:i2], datos[3][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('y [$h^{-1}$Mpc]')
	plt.ylabel('z [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[2][i1:i2], datos[3][i1:i2]]
	
#Cutting in Y axe
def CutY( Y, thick, plot=True, color='black' ):
    #Sorting in x axe
    argx = list( np.argsort( datos[2] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if Y<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(Y - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[2][i] >= Y and i1==0:
	    i1 = i
	if datos[2][i] >= Y + thick and i2==-1:
	    i2 = i
	    break
	    
    #Plotting results	    
    if plot == True:    
	plt.title('Cut in Y axes between %3.1f and %3.1f'%(Y, Y + thick))
	plt.plot( datos[1][i1:i2], datos[3][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('x [$h^{-1}$Mpc]')
	plt.ylabel('z [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[1][i1:i2], datos[3][i1:i2]]

#Cutting in Z axe
def CutZ( Z, thick, plot=True, color='black' ):
    #Sorting in x axe
    argx = list( np.argsort( datos[3] ) )
    for i in xrange(0, ncol):
	datos[i] = datos[i][argx]
    
    if Y<=thick:
	i_star = 0
    else:
	i_star = int(Box_lenght/(Z - thick))
    
    i1 = 0
    i2 = -1
    for i in xrange(i_star,nrow):
	if datos[3][i] >= Y and i1==0:
	    i1 = i
	if datos[3][i] >= Y + thick and i2==-1:
	    i2 = i
	    break
	    
    #Plotting results	    
    if plot == True:    
	plt.title('Cut in Z axes between %3.1f and %3.1f'%(Y, Y + thick))
	plt.plot( datos[1][i1:i2], datos[2][i1:i2], '.', color=color )
	plt.xlim( (0,Box_lenght) )
	plt.ylim( (0,Box_lenght) )
	plt.xlabel('x [$h^{-1}$Mpc]')
	plt.ylabel('y [$h^{-1}$Mpc]')
	plt.show()
    else:
	return [datos[1][i1:i2], datos[3][i1:i2]]

#==================================================================================================
#			PARAMETERS
#==================================================================================================
filename = '../Data/CLUES/2710/halos_catalog.dat'

#==================================================================================================
#			HALO FINDER IN 2D REGION
#==================================================================================================
datos = np.transpose( np.loadtxt( filename ) )
ncol = len(datos)		#Number of columns
nrow = len(datos[0])		#Number of rows

Box_lenght = np.max( tuple(datos[1])+tuple(datos[2])+tuple(datos[3]) )		#h^-1 Mpc

