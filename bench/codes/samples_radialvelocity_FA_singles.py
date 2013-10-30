#samples_radialvelocity_FA_single.py
#
#This code calculate histogram of the radial velocity of the pair samples vs the fractional 
#anisotropy index of each respective system. Each histogram is calculated for different velocity 
#ranges in order to evaluate possible bias or correlations.
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
#Mass limits
P_lim = (-250., 0.0)
#FA limits
FA_lim = (0.0, 1.0)
#Yticks of the distribution
ytick = [ 0.0, 1.0, 2.0, 3.0, 4.0, 5.0 ]
ylimits = (0.0, 5.5) 


#Bins of IP systems
bins_IP  = 20
#Bins of RIP systems
bins_RIP  = 10

#==================================================================================================
#			COMPUTING VELOCITIES FOR EACH SAMPLE
#==================================================================================================

i_fold = 0
N_sim = len(folds)

#start with a rectangular Figure
plt.figure(1, figsize=(8,8))

for fold in folds:
    print fold
    
    #Loading eigenvalues
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    #Loading GH sample
    halos = np.transpose(np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold,catalog)))
    
    #Loading IP sample
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog))
    i_IP = tmp.T[1].astype(int)-1
    #Fractional Anisotropy
    FA_IP = Fractional_Anisotropy( eig[1][i_IP], eig[2][i_IP], eig[3][i_IP] )
    #Radial and Tangential velocity
    #Halo 1
    I1 = tmp.T[1].astype(int)-1
    M1 = halos[ 8, I1 ]
    x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
    vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
    #Halo 2
    I2 = tmp.T[4].astype(int)-1
    M2 = halos[ 8, I2 ]
    x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
    vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
    P_IP, v_tan_IP = Velocities( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)
    
    
    #Loading Indexes of RIP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog))
    i_RIP = tmp.T[1].astype(int)-1
    #Fractional Anisotropy
    FA_RIP = Fractional_Anisotropy( eig[1][i_RIP], eig[2][i_RIP], eig[3][i_RIP] )
    #Radial and Tangential velocity
    #Halo 1
    I1 = tmp.T[1].astype(int)-1
    M1 = halos[ 8, I1 ]
    x1 = halos[ 1, I1 ];  y1 = halos[ 2, I1 ]; z1 = halos[ 3, I1 ]
    vx1 = halos[ 4, I1 ]; vy1 = halos[ 5, I1 ]; vz1 = halos[ 6, I1 ]
    #Halo 2
    I2 = tmp.T[4].astype(int)-1
    M2 = halos[ 8, I2 ]
    x2 = halos[ 1, I2 ];  y2 = halos[ 2, I2 ]; z2 = halos[ 3, I2 ]
    vx2 = halos[ 4, I2 ]; vy2 = halos[ 5, I2 ]; vz2 = halos[ 6, I2 ]
    P_RIP, v_tan_RIP = Velocities( M1, x1, y1, z1, vx1, vy1, vz1, M2, x2, y2, z2, vx2, vy2, vz2)

    #Fixing ranges of total mass
    for i in xrange(1,6):
	Mmin = P_lim[0] + (i-1)*(P_lim[1] - P_lim[0])/5.
	Mmax = P_lim[0] + i*(P_lim[1] - P_lim[0])/5.
	
	#Histogram of RIP systems for each interval
	FA_RIP_sin = FA_RIP[(Mmin <= P_RIP)*(P_RIP < Mmax)]
	#Histogram of IP systems for each interval
	FA_IP_sin = FA_IP[(Mmin <= P_IP)*(P_IP < Mmax)]
	
	plt.subplot(5,1,5-i+1)
	if len(FA_RIP_sin) > 0:
	    plt.hist( FA_RIP_sin, bins=bins_RIP, normed=True, range=FA_lim, \
	    label = "RIP %2.2f%%"%(100*len(FA_RIP_sin)/(1.0*len(FA_RIP))) )
	else:
	    plt.hist( [-FA_lim[1]], bins=bins_RIP, normed=True, range=FA_lim, label = "RIP  0.00%" )
	if len(FA_IP_sin) > 0:
	    histx = np.histogram( FA_IP_sin, bins=bins_IP, normed=True, range=FA_lim )
	    plt.plot( histx[1][1:], histx[0], linewidth=2.0, color="black", \
	    label = "IP %2.2f%%"%(100*len(FA_IP_sin)/(1.0*len(FA_IP))) )
	plt.text( 0.75, 4.5\
	,"$%1.2f\leq v_{rad}<%1.2f$"%( Mmin, Mmax ),\
	horizontalalignment='center', verticalalignment='center', fontsize=13 )

    i_fold += 1


for i in xrange(1,6):
    plt.subplot(5,1,i)
    plt.yticks( ytick )
    plt.ylim( ylimits )
    if i<5:
	plt.xticks( np.linspace(FA_lim[0], FA_lim[1], 11), ["",""] )
    else:
	plt.xlabel("Fractional Anisotropy FA")
	plt.xticks( np.linspace(FA_lim[0], FA_lim[1], 11) )
    if i == 3:
	plt.ylabel("Normed distribution")

    plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
    plt.grid()
        
plt.subplots_adjust( hspace = 0.05 )
        
plt.show()