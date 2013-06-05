execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Data filename
folds = ["BOLSHOI/"]
#Catalog Scheme
catalog = 'FOF'
#Number of Mass intervals
N_mass = 20
#Labels of graphs
labels = ["Bolshoi"]
#Index of each LG halos
LG_index = [ False ]
#Minim mass Range
MLog10 = 11.
#Colors array
Colors = ['black']
#Linewidths
Linewidths = [2]
#Figure size
plt.figure( figsize=(6,6) )

#==================================================================================================
#			HALOS AND PAIRS DATA
#==================================================================================================
i_fold = 0
for fold in folds:
    #Halos Datas
    halos = np.transpose( np.loadtxt( '%s%s/C_GH_%s.dat'%(foldglobal,fold, catalog) ) )
    Nhalos = len(halos[0])		#Number of halos
    halos[:,:] = halos[:,np.argsort(halos[8,:])]
    
    #IsoPairs datas
    isopairs = np.transpose( np.loadtxt( '%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog) ) )
    Npairs = len(isopairs[0])		#Number of pairs

    #Construction of Mass axes
    Mmin = np.min(halos[8])
    if MLog10 != False:
	Mmin = 10**MLog10
	
    Mmax = np.max(halos[8])
    Mass_array = 10**( np.linspace( np.log10( Mmin ), np.log10( Mmax ), N_mass ) )
    
    #Integrated mass 
    IMPD = np.zeros( N_mass )
    
    #Mass of LG halos
    Mass_LG = [0,0]

    #==================================================================================================
    #			HISTOGRAMS
    #==================================================================================================
    n = 0
    for i in xrange(0, Nhalos):
	if halos[8,i] >= Mass_array[n]:
	    IMPD[n] += Nhalos - i
	    n += 1
	if LG_index[i_fold] != False:
	    for j in range(2):
		if halos[0,i] == LG_index[i_fold][j]:
		    Mass_LG[j] = halos[8,i]

    print i_fold
    plt.loglog( Mass_array, IMPD/IMPD[0], label=labels[i_fold], color = Colors[i_fold], linewidth = Linewidths[i_fold] )
    plt.vlines( Mass_LG[0], 1e-6, 1, color = Colors[i_fold], linestyle = '--', linewidth = 0.5 )
    plt.vlines( Mass_LG[1], 1e-6, 1, color = Colors[i_fold], linestyle = '--', linewidth = 0.5 )
    i_fold += 1
    
#plt.title('Histograms of halos mass')
plt.xlabel('Mass [$M_{\odot}$]')
plt.ylabel('Halos percent')
plt.ylim( (1e-6, 1.0) )
plt.xlim( (1e11, 1e15) )
plt.grid()
#plt.legend(labels)
plt.savefig( 'halos_IMF.pdf', format='pdf' )
plt.show()