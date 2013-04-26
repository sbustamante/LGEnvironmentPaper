execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["CLUES/2710/"]
#Labels of graphs
labels = ["CLUES 1"]
#Box lenght
Box_L = [64,64,64]
#Number of sections
N_sec = [64,64,64]
#Smooth parameter
smooth = '_s1'
#Catalog scheme
catalog = 'FOF'
#Coordinate to cut (1 -- X, 2 -- Y, 3 -- Z)
axe = 1
#Coordinates in plots
axe_label = ["x","y","z","x","y","z"]
#Lambda_Th
Lambda_th = 0.6
#Cosmic web scheme
Web = 'Tweb'

#Colors
my_cmapC = plt.cm.get_cmap('gray')
my_cmap4 = plt.cm.get_cmap('gray', 4)


#==================================================================================================
#			PLOTING EACH CLUES SIMULATION AND RESPECTIVE LG
#==================================================================================================
'''
FIGURE SCHEME
-------------------
|  1  |  2  |  3  |
-------------------
'''

N_sim = len( folds )
ax = np.zeros( (3, N_sim) )

i_fold = 0


for fold in folds:
    #Extent
    extent = [0, Box_L[i_fold], 0, Box_L[i_fold]]

    #Loading Eigenvalues Vweb filename
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,Web,N_sec[i_fold],smooth)
    #Loading LG index of each simulation
    LG_Index = np.loadtxt('%s%s/LG_index_%s.dat'%(foldglobal,fold, catalog))
    #Loading All properties of Halos
    halos = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold, catalog)))
    
    LG_prop = [ halos[0:4,int(LG_Index[0]-1)], halos[0:4,int(LG_Index[1]-1)] ]

    #Current label simulation
    label = labels[i_fold]
	
    #Loading Fields
    Ns = int((LG_prop[0][axe]/Box_L[i_fold])*N_sec[i_fold])
    eigV1 = CutFieldZ( eigV_filename+"_1", Ns, 16, Coor = axe )
    eigV2 = CutFieldZ( eigV_filename+"_2", Ns, 16, Coor = axe )
    eigV3 = CutFieldZ( eigV_filename+"_3", Ns, 16, Coor = axe )

    #Plotting
    plt.subplot( 1, N_sim, i_fold+1 )
    plt.imshow( -np.transpose(Scheme( eigV1, eigV2, eigV3, Lambda_th )[::,::-1]), 
    extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    plt.title( "%s for %s\n%s = %1.2f"%
    ( Web, labels[i_fold],axe_label[axe-1], Box_L[i_fold]*Ns/N_sec[i_fold] ) )
    if i_fold == 0:
	plt.ylabel( '%s [Mpc $h^{-1}$]'%(axe_label[axe]) )
    plt.xlabel( '%s [Mpc $h^{-1}$]'%(axe_label[axe+1]) )

    if axe == 1:
	plt.plot( 
	(LG_prop[0][2],LG_prop[1][2]), 
	(LG_prop[0][3],LG_prop[1][3]), 
	'o', markersize = 8, color = 'red', label='LG' )
    if axe == 2:
	plt.plot( 
	(LG_prop[0][1],LG_prop[1][1]), 
	(LG_prop[0][3],LG_prop[1][3]), 
	'o', markersize = 8, color = 'red', label='LG' )
    if axe == 3:
	plt.plot( 
	(LG_prop[0][1],LG_prop[1][1]), 
	(LG_prop[0][2],LG_prop[1][2]), 
	'o', markersize = 8, color = 'red', label='LG' )
    
    plt.xlim( (0,Box_L[i_fold]) )
    plt.ylim( (0,Box_L[i_fold]) )

    i_fold += 1
    
plt.show()