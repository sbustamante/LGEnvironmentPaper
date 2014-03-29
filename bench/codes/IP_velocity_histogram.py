execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/", "CLUES/10909/","CLUES/16953/","CLUES/2710/"]
#Number of sections
N_sec = [256,64,64,64]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Velocity limits
v_rad_lim = (-250, 250)
v_tan_lim = (0, 250)
#Numver of intervals
Nd_IP  = 200
Nd_CLG = 100
#Classification scheme
web = 'Vweb'

#==================================================================================================
#			CONSTRUCTING EIGENVALUES EXTREME VALUES
#==================================================================================================
N_sim = len( folds )

plt.figure( figsize = (8,6) )
LG1 = []
LG2 = []

i_fold = 0
for fold in folds:
    print fold
  
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sC_GH_%s.dat'%(foldglobal,fold,catalog) ) )
    Nhalos = len(halos[0])		#Number of halos
  
    if fold == "BOLSHOI/":
	#Loading Pairs Systems----------------------------------------------
	P = np.transpose(np.loadtxt('%s%s/C_P_%s.dat'%(foldglobal,fold, catalog)))
	#Energy and Angular Momentum
	I1 = list(P[1]-1)
	M1 = halos[ 8, I1 ]
	x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
	vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
	
	I2 = list(P[4]-1)
	M2 = halos[ 8, I2 ]
	x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
	vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
	
	v_rad_P, v_tan_P = \
	Velocities( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)
	
	Hist  = np.transpose(np.histogram2d( v_rad_P, v_tan_P, 
	bins = 20, normed = False, range = (v_rad_lim,v_tan_lim)  )[0][::,::-1])
	
	plt.imshow( Hist, interpolation='nearest', aspect = 'auto',
	cmap = 'binary', \
	extent = (v_rad_lim[0],v_rad_lim[1],v_tan_lim[0],v_tan_lim[1]) )	
	plt.colorbar()
	
      
	#Loading Isolated Pairs Systems----------------------------------------------
	IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
	#Energy and Angular Momentum
	I1 = list(IP[1]-1)
	M1 = halos[ 8, I1 ]
	x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
	vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
	
	I2 = list(IP[4]-1)
	M2 = halos[ 8, I2 ]
	x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
	vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
	
	v_rad_IP, v_tan_IP = \
	Velocities( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)
	
	Hist  = np.transpose(np.histogram2d( v_rad_IP, v_tan_IP, 
	bins = 15, normed = False, range = (v_rad_lim,v_tan_lim)  )[0][::,::-1])
		
	plt.contour( Hist[::-1,::], 7, aspect = 'auto', 
	extent = (v_rad_lim[0],v_rad_lim[1],v_tan_lim[0],v_tan_lim[1]), 
	linewidth=1.5, interpolation = 'gaussian' )
	plt.colorbar()
	

	#Loading CLG Pairs Systems --------------------------------------------------
	CLG = np.transpose(np.loadtxt('%s%s/C_CLG%s_%s.dat'%(foldglobal,fold,web[0],catalog)))
	#Energy and Angular Momentum
	I1 = list(CLG[1]-1)
	M1 = halos[ 8, I1 ]
	x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
	vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
	
	I2 = list(CLG[4]-1)
	M2 = halos[ 8, I2 ]
	x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
	vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
	
	v_rad_CLG, v_tan_CLG = \
	Velocities( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)
	
	plt.plot( v_rad_CLG, v_tan_CLG,
	'o', markersize=7, color = "blue", label='CLG Sample' )


    if fold != "BOLSHOI/":
	#Loading LG Pairs Systems----------------------------------------------------
	LG = np.loadtxt('%s%s/C_LG_%s.dat'%(foldglobal,fold, catalog))
	#Energy and Angular Momentum
	I1 = list([LG[1]-1,])
	M1 = halos[ 8, I1 ]
	x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
	vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
	
	I2 = list([LG[4]-1,])
	M2 = halos[ 8, I2 ]
	x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
	vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
	
	v_rad_LG, v_tan_LG = \
	Velocities( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)
	
	LG1.append( v_rad_LG )
	LG2.append( v_tan_LG )
	
	if i_fold == 2:
	    plt.plot( v_rad_LG, v_tan_LG,
	    'o', markersize=10, color = "red", label='LG Sample' )
	else:
	    plt.plot( v_rad_LG, v_tan_LG,
	    'o', markersize=10, color = "red" )

    i_fold += 1


#==================================================================================================
#Plot configuration 
#==================================================================================================

plt.xlim( v_rad_lim )
plt.ylim( v_tan_lim )
plt.ylabel('Tangential Velocity $v_{tan}$ [km s$^{-1}$]')
plt.xlabel('Radial Velocity $v_{rad}$ [km s$^{-1}$]')
plt.legend( fancybox = True, shadow = True, title="Samples", ncol = 1, loc='upper right')
plt.grid()
plt.show()
