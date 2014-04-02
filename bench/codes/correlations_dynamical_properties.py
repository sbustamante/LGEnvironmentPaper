#correlation_dynamical_properties.py
#
#This code calculate box plots of all dynamical properties of IP and RIP samples, including total
#mass, mass ratio, radial and tangential velocities, angular momentum, specific energy, reduced
#spin. For each property, it is performed a box plot for the more likely range regarding quintiles
#of FA, distance and volume to the nearest void.
#
#by: Sebastian Bustamante

execfile('_Head.py')
plt.close("all")
#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/"]
#Number of sections
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme [BDM, FOF]
catalog = sys.argv[2]
#Classification scheme [Tweb, Vweb]
web = sys.argv[1]
#Lambda_th
Lambda_th = 0.0

#Mass_norm
M_norm = 1e12

#Bins of IP systems
bins_IP  = 10
#Bins of RIP systems
bins_RIP  = 10

#==================================================================================================
#			COMPUTING TOTAL MASSES FOR EACH SAMPLE
#==================================================================================================

i_fold = 0
N_sim = len(folds)

#start with a rectangular Figure
plt.figure(1, figsize=(8,12))

#for fold in folds:
    #print fold
    
    ##Loading voids catalogue of general halos
    #voids = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    #(foldglobal,fold,web,N_sec[i_fold],smooth,catalog))
    ##Loading eigenvalues
    #eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    ##Loading environment properties of halos classification scheme
    #eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    #(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))    
    ##Volumes and ditances of each void region
    #volume = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
    #(foldglobal, fold, web, N_sec[i_fold], smooth, Lambda_th ))
    #distance = voids[:,0]
    
    ##Loading IP sample
    #tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog))
    #i_IP = tmp.T[1].astype(int)-1
    ##Eigenvalues for the IP sample
    #eig1_IP = eig[1][i_IP]
    #eig2_IP = eig[2][i_IP]
    #eig3_IP = eig[3][i_IP]
    ##Loading FA
    #FA_IP = Fractional_Anisotropy( eig1_IP, eig2_IP, eig3_IP )
    ##Volume and distance of the nearest void region
    #volume_IP = np.log10(volume[voids.T[1][i_IP].astype(int)-1,1])
    #distance_IP = voids[i_IP,0]
    
    ##Loading RIP sample
    #tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog))
    #i_RIP = tmp.T[1].astype(int)-1
    ##Eigenvalues for the IP sample
    #eig1_RIP = eig[1][i_RIP]
    #eig2_RIP = eig[2][i_RIP]
    #eig3_RIP = eig[3][i_RIP]
    ##Loading FA
    #FA_RIP = Fractional_Anisotropy( eig1_RIP, eig2_RIP, eig3_RIP )
    ##Volume and distance of the nearest void region
    #volume_RIP = np.log10(volume[voids.T[1][i_RIP].astype(int)-1,1])
    #distance_RIP = voids[i_IP,0]
        
    ##Calculating quintiles of each property regarding IP sample
    ##FA quintils
    #FA_IP_sorted = np.sort(FA_IP)
    #FA_quintil = np.ones( 6 )
    #FA_quintil[0] = 0.0
    #FA_quintil[5] = 1.0
    #for i in xrange(1,5):
	#FA_quintil[i] = FA_IP_sorted[ int(len(FA_IP)*i/5.) ]
    ##Distance quintils
    #distance_IP_sorted = np.sort(distance_IP)
    #dist_quintil = np.ones( 6 )
    #dist_quintil[0] = np.min( distance_IP )
    #dist_quintil[5] = np.max( distance_IP )
    #for i in xrange(1,5):
	#dist_quintil[i] = distance_IP_sorted[ int(len(distance_IP)*i/5.) ]
    ##Volume quintils
    #volume_IP_sorted = np.sort(volume_IP)
    #vol_quintil = np.ones( 6 )
    #vol_quintil[0] = np.min( volume_IP )
    #vol_quintil[5] = np.max( volume_IP )
    #for i in xrange(1,5):
	#vol_quintil[i] = volume_IP_sorted[ int(len(volume_IP)*i/5.) ]

        
#Adjusting subplots
plt.subplots_adjust( left = 0.1, right = 1.0, bottom = 0.07, top = 0.99, hspace = 0.09, wspace = 0.05 )
#Number of plots according represented properties
FA_plots = 3*np.arange(7)+1
dist_plots = 3*np.arange(7)+2
vol_plots = 3*np.arange(7)+3

#Formating subplots
for i in xrange(1, 22):
    plt.subplot(7,3,i)
    plt.xlim( (0,1) )
    plt.xticks(np.linspace(0.05,0.95,5), [""])
    plt.grid()	
for i in xrange(1, 22):
    plt.subplot(7,3,i)
    plt.ylim( (0,1) )
    if i not in FA_plots:
	plt.yticks(np.linspace(0,1,6), [""])
    else:
	plt.yticks(np.linspace(0,1,6), fontsize=10)

#X - Labels
for i in xrange( 19, 22 ):
    plt.subplot(7,3,i)
    plt.xticks(np.linspace(0.05,0.95,5), ["Q1","Q2","Q3","Q4","Q5"], fontsize=10)
#FA label
plt.subplot(7,3,19)
plt.xlabel("Fractional Anisotropy", fontsize=10)
#Distance label
plt.subplot(7,3,20)
plt.xlabel("Distance to nearest\nvoid [Mpc $h^{-1}$]", fontsize=10)
#Volume label
plt.subplot(7,3,21)
plt.xlabel("Equivalent spherical\ncomoving radius [Mpc $h^{-1}$]", fontsize=10)

#Y - Labels
#Total mass
plt.subplot(7,3,1)
plt.ylabel("$M_{tot} = M_A + M_B$\n[$10 ^{12}h^{-1}\ M_{\odot}$]  ", fontsize=9)
#Mass Ratio
plt.subplot(7,3,4)
plt.ylabel("$\\xi = M_B/M_A$\n ", fontsize=9)
#Radial velocity
plt.subplot(7,3,7)
plt.ylabel("Radial velocity\n$v_{rad}$ [km s$^{-1}$]  ", fontsize=9)
#Tangential velocity
plt.subplot(7,3,10)
plt.ylabel("Tangential velocity\n$v_{tan}$ [km s$^{-1}$]    ", fontsize=9)
#Angular momentum
plt.subplot(7,3,13)
plt.ylabel("Angular momentum\n$L_{orb}$ [Mpc km s$^{-1}$]  ", fontsize=9)
#Energy
plt.subplot(7,3,16)
plt.ylabel("Mechanical energy\n$e_{tot}$ [$10^{-36}$ Mpc$^2$s$^{-2}$]", fontsize=9)
#Spin parameter
plt.subplot(7,3,19)
plt.ylabel("Spin parameter\nlog$_{10}\lambda$      ", fontsize=9)


plt.savefig( "plot.pdf" )
#plt.show()