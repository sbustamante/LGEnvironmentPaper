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

import halo_cuts as HC

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Folder
folds=["../Data/CLUES/2710/"]
#Resolution
n_x = 64


#lambda_thr = [0.5, 0.7, 1.0, 1.5]
lambda_thr = [0.5]

#==================================================================================================
#			CALCULATING ENVIROMENT
#==================================================================================================
for fold in folds:	    
    enviroment = np.zeros( (len(lambda_thr), n_x, n_x, n_x) )
    for n in xrange(0,len(lambda_thr)):
	datos = np.loadtxt( "%s%d/enviroment_Lamb_%1.2f.dat"%(fold,n_x,lambda_thr[n]) )
	enviroment[n] = datos.reshape([n_x,n_x,n_x])


files = []
extent = [0, HC.Box_lenght, 0, HC.Box_lenght]
#MyColours
jet3 = plt.cm.get_cmap('jet', 3)
for i in xrange( 0, len(enviroment[0]) ):
    #Image size
    plt.figure( figsize=(10,8) )
    for n in xrange( 0, len(lambda_thr) ):
	plt.subplot('%d%d%d'%(int(np.sqrt(len(lambda_thr))),int(np.sqrt(len(lambda_thr))),n+1))
	plt.imshow( np.transpose(enviroment[n,i,:,::-1]), extent=extent, vmin=0, vmax=2, cmap = jet3 )
	plt.colorbar()
	HC.CutX(i*HC.Box_lenght/(1.0*n_x), HC.Box_lenght/(1.0*n_x))
	plt.title( "$\lambda_{thr}$ = %1.2f, x=%1.2f"%(lambda_thr[n],i*HC.Box_lenght/(1.0*n_x)) )
	
    fname='_tmp-%03d.png'%i
    plt.savefig(fname)
    files.append(fname)
    plt.close()

print 'Making movie animation.mpg - this make take a while'
os.system("ffmpeg -qscale 1 -r 10 -b 9600 -i _tmp-%03d.png  video.mp4")

os.system('rm -rf *.png')