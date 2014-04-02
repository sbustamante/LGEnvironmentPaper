#correlation_dynamical_properties.py
#
#This code calculate box plots of all dynamical properties of IP and RIP samples, including total
#mass, mass ratio, radial and tangential velocities, angular momentum, specific energy, reduced
#spin. For each property, it is performed a box plot for the more likely range regarding quintiles
#of FA, distance and volume to the nearest void.
#
#by: Sebastian Bustamante

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
#Catalog Scheme [BDM, FOF]
catalog = sys.argv[2]
#Classification scheme [Tweb, Vweb]
web = sys.argv[1]

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
plt.figure(1, figsize=(8,8))

for fold in folds:
    print fold
    
    #Loading voids catalogue of general
    voids = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog))
    #Volumes of each void region
    volume = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
    (foldglobal, fold, web, N_sec[i_fold], smooth, Lambda_th ))
    
    #Loading IP sample
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog))
    i_IP = tmp.T[1].astype(int)-1
    Mtot_IP = (tmp.T[2] + tmp.T[5])/M_norm
    #Volume of the nearest void region
    voids_IP = np.log10(volume[voids.T[1][i_IP].astype(int)-1,1])
    
    
    #Loading Indexes of RIP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog))
    i_RIP = tmp.T[1].astype(int)-1
    Mtot_RIP = (tmp.T[2] + tmp.T[5])/M_norm
    #Volume of the nearest void region
    voids_RIP = np.log10(volume[voids.T[1][i_RIP].astype(int)-1,1])

    #Fixing ranges of total mass
    for i in xrange(1,6):
	Mmin = MT_lim[0] + (i-1)*(MT_lim[1] - MT_lim[0])/5.
	Mmax = MT_lim[0] + i*(MT_lim[1] - MT_lim[0])/5.
	
	#Histogram of RIP systems for each interval
	voids_RIP_sin = voids_RIP[(Mmin <= Mtot_RIP)*(Mtot_RIP < Mmax)]
	#Histogram of IP systems for each interval
	voids_IP_sin = voids_IP[(Mmin <= Mtot_IP)*(Mtot_IP < Mmax)]
	
	plt.subplot(5,1,5-i+1)
	if len(voids_RIP_sin) > 0:
	    plt.hist( voids_RIP_sin, bins=bins_RIP, normed=True, range=VD_lim, \
	    label = "RIP %2.2f%%"%(100*len(voids_RIP_sin)/(1.0*len(voids_RIP))) )
	else:
	    plt.hist( [-VD_lim[1]], bins=bins_RIP, normed=True, range=VD_lim, label = "RIP  0.00%" )
	if len(voids_IP_sin) > 0:
	    histx = np.histogram( voids_IP_sin, bins=bins_IP, normed=True, range=VD_lim )
	    plt.plot( histx[1][:-1]+(histx[1][1]-histx[1][0])/2.0, histx[0], linewidth=2.0, color="black", \
	    label = "IP %2.2f%%"%(100*len(voids_IP_sin)/(1.0*len(voids_IP))) )
	plt.text( 4.5, 0.45\
	,"$%1.2f\leq M_{tot}/(1\\times 10 ^{12}h^{-1}\ M_{\odot})<%1.2f$"%( Mmin, Mmax ),\
	horizontalalignment='center', verticalalignment='center', fontsize=13 )

    i_fold += 1


for i in xrange(1,6):
    plt.subplot(5,1,i)
    plt.yticks( ytick )
    plt.ylim( ylimits )
    if i<5:
	plt.xticks( np.linspace(VD_lim[0], VD_lim[1], 11), ["",""] )
    else:
	plt.xlabel("Distance to the nearest void region [Mpc $h^{-1}$]")
	plt.xticks( np.linspace(VD_lim[0], VD_lim[1], 11) )
    if i == 3:
	plt.ylabel("Normed distribution")
    plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
    plt.grid()
        
plt.subplots_adjust( hspace = 0.05 )
        
plt.show()