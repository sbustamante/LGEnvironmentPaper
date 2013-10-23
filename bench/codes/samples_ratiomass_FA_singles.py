#samples_ratiomass_FA_single.py
#
#This code calculate histogram of the ratio mass of the pair samples vs the fractional anisotropy
#index of each respective system. Each histogram is calculated for different ratio mass ranges in 
#order to evaluate possible bias or correlations.
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
MT_lim = (0.0, 1.0)
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
    
    #Loading IP sample
    IP = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog))
    i_IP = IP.T[1].astype(int) - 1
    Mtot_IP = (IP.T[5]/IP.T[2])
    #Fractional Anisotropy
    FA_IP = Fractional_Anisotropy( eig[1][i_IP], eig[2][i_IP], eig[3][i_IP] )
    
    #Loading Indexes of RIP sample for scheme 1
    RIP = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog))
    i_RIP = RIP.T[1].astype(int) - 1
    Mtot_RIP = (RIP.T[5]/RIP.T[2])
    #Fractional Anisotropy
    FA_RIP = Fractional_Anisotropy( eig[1][i_RIP], eig[2][i_RIP], eig[3][i_RIP] )

    #Fixing ranges of total mass
    for i in xrange(1,6):
	Mmin = MT_lim[0] + (i-1)*(MT_lim[1] - MT_lim[0])/5.
	Mmax = MT_lim[0] + i*(MT_lim[1] - MT_lim[0])/5.
	
	#Histogram of RIP systems for each interval
	FA_RIP_sin = FA_RIP[(Mmin <= Mtot_RIP)*(Mtot_RIP < Mmax)]
	#Histogram of IP systems for each interval
	FA_IP_sin = FA_IP[(Mmin <= Mtot_IP)*(Mtot_IP < Mmax)]
	
	plt.subplot(5,1,5-i+1)
	if len(FA_RIP_sin) > 0:
	    plt.hist( FA_RIP_sin, bins=bins_RIP, normed=True, range=FA_lim, label = "RIP" )
	else:
	    plt.hist( [-FA_lim[1]], bins=bins_RIP, normed=True, range=FA_lim, label = "RIP" )
	if len(FA_IP_sin) > 0:
	    histx = np.histogram( FA_IP_sin, bins=bins_IP, normed=True, range=FA_lim )
	    plt.plot( histx[1][1:], histx[0], linewidth=2.0, color="black", label = "IP" )
	plt.text( 0.75, 4.5\
	,"$%1.2f\leq \\xi = M_B/M_A<%1.2f$"%( Mmin, Mmax ),\
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
    if i == 5:
	plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
    plt.grid()
        
plt.subplots_adjust( hspace = 0.05 )
        
plt.show()