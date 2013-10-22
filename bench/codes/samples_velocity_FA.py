execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/"]
#Number of sections
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'BDM'
#Velocity limits
v_rad_lim = (-300, 100)
v_tan_lim = (0, 400)
#Numver of intervals
Nd_IP  = 200
#Classification scheme
web = 'Tweb'

#==================================================================================================
#			CONSTRUCTING EIGENVALUES EXTREME VALUES
#==================================================================================================
N_sim = len( folds )

plt.figure( figsize = (18,6) )
LG1 = []
LG2 = []

i_fold = 0
for fold in folds:
    print fold
  
    #Loading Halos Data
    halos = np.transpose( np.loadtxt( '%s%sC_GH_%s.dat'%(foldglobal,fold,catalog) ) )
    Nhalos = len(halos[0])		#Number of halos
    
    #Loading environment properties of halos
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'
    %(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
  
    if fold == "BOLSHOI/":
	#Loading Pairs Systems----------------------------------------------
	P = np.transpose(np.loadtxt('%s%s/C_P_%s.dat'%(foldglobal,fold, catalog)))
	#Radial and tangential velocities
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
	
	#Anisotropy Index
	EnvBL1_P = eig[ 1,[P[1]-1] ][0]
	EnvBL2_P = eig[ 2,[P[1]-1] ][0]
	EnvBL3_P = eig[ 3,[P[1]-1] ][0]	
	FA_P  = Fractional_Anisotropy( EnvBL1_P, EnvBL2_P, EnvBL3_P )
	
	Hist_rad  = np.transpose(np.histogram2d( FA_P, v_rad_P, 
	bins = 20, normed = False, range = ((0,1),v_rad_lim)  )[0][::,::-1])
	
	Hist_tan  = np.transpose(np.histogram2d( FA_P, v_tan_P,
	bins = 20, normed = False, range = ((0,1),v_tan_lim)  )[0][::,::-1])
	
	plt.subplot(121)
	plt.imshow( Hist_rad, interpolation='nearest', aspect = 'auto',
	cmap = 'binary', \
	extent = (0,1,v_rad_lim[0],v_rad_lim[1]) )	
	plt.colorbar()
	
	plt.subplot(122)
	plt.imshow( Hist_tan, interpolation='nearest', aspect = 'auto',
	cmap = 'binary', \
	extent = (0,1,v_tan_lim[0],v_tan_lim[1]) )
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
	
	#Anisotropy Index
	EnvBL1_IP = eig[ 1,[IP[1]-1] ][0]
	EnvBL2_IP = eig[ 2,[IP[1]-1] ][0]
	EnvBL3_IP = eig[ 3,[IP[1]-1] ][0]	
	FA_IP  = Fractional_Anisotropy( EnvBL1_IP, EnvBL2_IP, EnvBL3_IP )

	Hist_rad  = np.transpose(np.histogram2d( FA_IP, v_rad_IP, 
	bins = 20, normed = False, range = ((0,1),v_rad_lim)  )[0][::,::-1])
	
	Hist_tan  = np.transpose(np.histogram2d( FA_IP, v_tan_IP, 
	bins = 20, normed = False, range = ((0,1),v_tan_lim)  )[0][::,::-1])
	
	plt.subplot(121)
	plt.contour( Hist_rad[::-1,::], 7, aspect = 'auto', 
	extent = (0,1,v_rad_lim[0],v_rad_lim[1]), 
	linewidth=1.5, interpolation = 'gaussian' )
	plt.colorbar()
	
	plt.subplot(122)
	plt.contour( Hist_tan[::-1,::], 7, aspect = 'auto', 
	extent = (0,1,v_tan_lim[0],v_tan_lim[1]), 
	linewidth=1.5, interpolation = 'gaussian' )
	plt.colorbar()
	

#==================================================================================================
#Plot configuration 
#==================================================================================================

plt.subplot(121)
plt.xlabel('Fractional Anisotropy')
plt.ylabel('Radial Velocity $v_{rad}$ [km s$^{-1}$]')
plt.ylim( v_rad_lim )
plt.grid()

plt.subplot(122)
plt.xlabel('Fractional Anisotropy')
plt.ylabel('Tangential Velocity $v_{tan}$ [km s$^{-1}$]')
plt.ylim( v_tan_lim )
plt.grid()

plt.legend( fancybox = True, shadow = True, title="Samples", ncol = 1, loc='upper right')
plt.show()
