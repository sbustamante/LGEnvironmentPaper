# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# **Analysis of Isolated pairs around cosmic voids**
# ================================
# 
# 
# Throghout this notebook we analyse the spatial distribution of isolated pairs regarding the neighbourhood of cosmic voids.

#==================================================================================================
#Importing all necessary libraries
#==================================================================================================
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# JSAnimation import available at https://github.com/jakevdp/JSAnimation
from JSAnimation import IPython_display
from matplotlib import animation
import numpy as np
import os

#Folder where is stored all simulation data
data_folder = '../../../CosmicData/BOLSHOI/'
#Folder where is stored all binary codes (C)
binary_folder = './'
#Parameter of the simulation
Lbox = 250.0    #[Mpc]
Nbox = 256

#Trheshold parameters for the cosmic web
Tl_th = 0.265
Vl_th = 0.175

#==================================================================================================
#Functions
#==================================================================================================
#Cutting Density field in X/Y/Z axe
def CutField( filename, X, res=32, Coor = 3, N=Nbox ):
    coord = [3,2,1]
    os.system( "%s/Field_Cut%d.out %s %d temp.tmp %d"%( binary_folder, res, filename, X, coord[Coor-1] ) )
    datos = np.loadtxt( 'temp.tmp' )
    N = int(np.sqrt(len( datos )))
    datos = datos.reshape( (N, N) )
    os.system( "rm temp.tmp" )
    return datos

#Field to compute Environment of Cosmic web
def Scheme( eig1, eig2, eig3, Lamb ):
    N1 = len( eig1 )
    N2 = len( eig1[0] )
    sch = 0*eig1
    
    for i in xrange(N1):
        for j in xrange(N2):
            if eig1[i,j] > Lamb: sch[i,j] += 1
            if eig2[i,j] > Lamb: sch[i,j] += 1
            if eig3[i,j] > Lamb: sch[i,j] += 1
    return sch

#==================================================================================================
#Loading all data (catalogues of halos and voids)
#==================================================================================================
#BDM catalogue of halos
#BDM_halos = np.transpose(np.loadtxt( "%s/C_GH_BDM.dat"%(data_folder) ))
##FOF catalogue of halos
#FOF_halos = np.transpose(np.loadtxt( "%s/C_GH_FOF.dat"%(data_folder) ))

##BDM catalogue of isolated pairs
#BDM_ip = np.transpose(np.loadtxt( "%s/C_IP_BDM.dat"%(data_folder) ))
##FOF catalogue of isolated pairs
#FOF_ip = np.transpose(np.loadtxt( "%s/C_IP_FOF.dat"%(data_folder) ))

##BDM catalogue of reduced isolated pairs
#BDM_ip = np.transpose(np.loadtxt( "%s/C_IP_BDM.dat"%(data_folder) ))
##FOF catalogue of reduced isolated pairs
#FOF_ip = np.transpose(np.loadtxt( "%s/C_IP_FOF.dat"%(data_folder) ))

##Catalogue of distances of BDM halos to Tweb-FAG-21 voids
##    Twe-FAG-21 : Void finder based on a Watershed transform over the FA field of the Tweb scheme
##    with a 2nd-order median filtering applied and with boundary removal activated
#dist_Tweb_BDM = np.transpose(np.loadtxt( "%s/Tweb/256/C_GH-voids_s1_BDM_FAG.dat"%(data_folder) ))

#Filename of density field
density_f = "%s/Tweb/256/Delta_s1"%(data_folder)
#Filename of Tweb eigenvalues
eigenT_f = "%s/Tweb/256/Eigen_s1"%(data_folder)
#Filename of Vweb eigenvalues
eigenV_f = "%s/Vweb/256/Eigen_s1"%(data_folder)

#Folder of Tweb-FAG-21 voids
voidsT21_f = "%s/Vweb/256/voidsFAG/voids21/"%(data_folder)

# <markdowncell>

# **Function for plotting a portion of the cosmic web**

# <codecell>

#plot_web
#This function plot certain cubic region of the cosmic web
def plot_web( c, ext, eigen, l_th ):
    
    X = []; Y = []; Z = []; C = []
    #Sweeping X coordinates
    for i in xrange( c[0]-ext, c[0]+ext+1 ):
        #Periodic boundaries
        ir = i
        if i<0: ir+=Nbox
        if i>Nbox: ir-=Nbox
        it = i-(c[0]-ext)
            
        #Calculating visual impresion of this X-slide
        datos = Scheme(CutField( eigen+"_1", ir, 16, 0 ), CutField( eigen+"_2", ir, 16, 0 ), CutField( eigen+"_3", ir, 16, 0 ), l_th )
        
        #Sweeping Y coordinates
        for j in xrange( c[1]-ext, c[1]+ext+1 ):
            #Periodic boundaries
            jr = j
            if j<0: jr+=Nbox
            if j>Nbox: jr-=Nbox
            jt = j-(c[1]-ext)
            
            #Sweeping Z coordinates
            for k in xrange( c[2]-ext, c[2]+ext+1 ):
                #Periodic boundaries
                kr = k
                if k<0: kr+=Nbox
                if k>Nbox: kr-=Nbox
                kt = k-(c[2]-ext)
                    
                #Storing visual impression
                X.append( it )
                Y.append( jt )
                Z.append( kt )
                C.append( datos[jr,kr] )
    return np.array(X), np.array(Y), np.array(Z), np.array(C)

# <codecell>

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z, C = plot_web( [50,50,50], 10, eigenT_f, Tl_th )
#ax.scatter(X, Y, Z, c=C, marker='o', s = 10, linewidth=0.01 )
ax.scatter(X[C==3], Y[C==3], Z[C==3], c=C[C==3], marker='o', s = 10, linewidth=0.01 )
ax.set_xlim( (0,21) )
ax.set_ylim( (0,21) )
ax.set_zlim( (0,21) )
ax.set_axis_off()

plt.show()