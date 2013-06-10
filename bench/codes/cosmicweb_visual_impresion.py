execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/","CLUES/2710/","CLUES/10909/","CLUES/16953/"]
#Labels of graphs
labels = ["BOLSHOI","CLUES 1","CLUES 2","CLUES 3"]
#Box lenght
Box_L = [250,64,64,64]
#Number of sections
N_sec = [256,64,64,64]
#Smooth parameter
smooth = '_s1'
#Coordinate to cut (1 -- X, 2 -- Y, 3 -- Z)
axe = 1
#Cut
Cut = 10

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
#plt.figure( figsize=(16,3*N_sim) )
plt.figure( figsize=(10,2*N_sim) )

for fold in folds:
    #Extent
    extent = [0, Box_L[i_fold], 0, Box_L[i_fold]]

    #Loading Density filename
    delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
    #Loading Vweb filename
    eigV_filename = '%s%sVweb/%d/Eigen%s'%(foldglobal,fold,N_sec[i_fold],smooth)
    
    #Current label simulation
    label = labels[i_fold]
	
    #Loading Fields
    delta = CutFieldZ( delta_filename, Cut, 32, Coor = axe )
    eigV1 = CutFieldZ( eigV_filename+"_1", Cut, 16, Coor = axe )
    eigV2 = CutFieldZ( eigV_filename+"_2", Cut, 16, Coor = axe )
    eigV3 = CutFieldZ( eigV_filename+"_3", Cut, 16, Coor = axe )

    #Density Plot
    plt.subplot( N_sim, 5, 5*i_fold+1 )
    plt.imshow( np.log(1+delta), extent = extent, cmap = "binary" )
    if i_fold == 0: 
	plt.title( "Density\nField" )
    plt.ylabel( '%s'%(label) )
    plt.yticks( (0,Box_L[i_fold]) )
    plt.xticks( (0,Box_L[i_fold]) )
    #if i_fold == N_sim - 1:
	#plt.xlabel( "[$h^{-1}$ Mpc]" )
	
	
    #Vweb Plot with Lambda_th = 0
    plt.subplot( N_sim, 5, 5*i_fold+2 )
    plt.imshow( -Scheme( eigV1, eigV2, eigV3, 0.0 ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    if i_fold == 0: 
	plt.title( "V-web\n$\lambda_{th} = 0$" )
    plt.yticks( (),() )
    plt.xticks( (0,Box_L[i_fold]) )
    #if i_fold == N_sim - 1:
	#plt.xlabel( "[$h^{-1}$ Mpc]" )
    
    
    #Vweb Plot with Lambda_th = 0.1
    plt.subplot( N_sim, 5, 5*i_fold+3 )
    plt.imshow( -Scheme( eigV1, eigV2, eigV3, 0.1 ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    if i_fold == 0: 
	plt.title( "V-web\n$\lambda_{th} = 0.1$" )
    plt.yticks( (),() )
    plt.xticks( (0,Box_L[i_fold]) )
    if i_fold == N_sim - 1:
	plt.xlabel( "[$h^{-1}$ Mpc]" )
    
    
    #Vweb Plot with Lambda_th = 0.3
    plt.subplot( N_sim, 5, 5*i_fold+4 )
    plt.imshow( -Scheme( eigV1, eigV2, eigV3, 0.3 ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    if i_fold == 0: 
	plt.title( "V-web\n$\lambda_{th} = 0.3$" )
    plt.yticks( (),() )
    plt.xticks( (0,Box_L[i_fold]) )
    #if i_fold == N_sim - 1:
	#plt.xlabel( "[$h^{-1}$ Mpc]" )
    
    
    #Vweb Plot with Lambda_th = 0.5
    plt.subplot( N_sim, 5, 5*i_fold+5 )
    plt.imshow( -Scheme( eigV1, eigV2, eigV3, 0.5 ), extent = extent, vmin=-3, vmax=0, cmap = my_cmap4 )
    if i_fold == 0: 
	plt.title( "V-web\n$\lambda_{th} = 0.5$" )
    plt.yticks( (),() )
    plt.xticks( (0,Box_L[i_fold]) )
    #if i_fold == N_sim - 1:
	#plt.xlabel( "[$h^{-1}$ Mpc]" )
    

    plt.xlim( (0,Box_L[i_fold]) )
    plt.ylim( (0,Box_L[i_fold]) )

    i_fold += 1
    

#plt.subplots_adjust(  )    
plt.show()