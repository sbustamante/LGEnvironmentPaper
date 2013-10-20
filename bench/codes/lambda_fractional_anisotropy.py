#Lambda_fractional_anisotropy.py
#
#This code calculate the histogram of the fractional of anisotropy of each sample and for each web
#scheme.
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
#Catalog Schemes
catalog = ['FOF', 'BDM']
#Web Scheme [Vweb, Tweb]
web = sys.argv[1]
#Nbins
bins = 50


#==================================================================================================
#			CONSTRUCTING EIGENVALUES 1D HISTOGRAMS
#==================================================================================================

i_fold = 0

plt.figure( figsize=(5,4) )
for fold in folds:
    print fold

    #Loading eigenvalues
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    
    #Loading environment properties of halos scheme 1
    eig1 = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[0])))
    #Fractional Anisotropy
    FA_GH1 = Fractional_Anisotropy( eig1[1], eig1[2], eig1[3] )
    FA, FA_bins = np.histogram( FA_GH1, bins = bins, normed = True, range=(0,1.0) )
    plt.plot( FA_bins[1:], np.cumsum(FA)/np.sum(FA), linestyle = "-" ,color = 'black', linewidth = 3,\
    label = 'GH$_{%s}$'%(catalog[0]) )
    
    #Loading environment properties of halos scheme 2
    eig2 = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[1])))
    #Fractional Anisotropy
    FA_GH2 = Fractional_Anisotropy( eig2[1], eig2[2], eig2[3] )
    FA, FA_bins = np.histogram( FA_GH2, bins = bins, normed = True, range=(0,1.0) )
    plt.plot( FA_bins[1:], np.cumsum(FA)/np.sum(FA), linestyle = "--" ,color = 'black', linewidth = 3,\
    label = 'GH$_{%s}$'%(catalog[1]) )
  
  
  
    #Loading Indexes of IP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_IP1 = tmp.T[1] 
    #Fractional Anisotropy
    FA_IP1 = Fractional_Anisotropy( eig1[1][i_IP1.astype(int)-1],\
    eig1[2][i_IP1.astype(int)-1], eig1[3][i_IP1.astype(int)-1] )
    FA, FA_bins = np.histogram( FA_IP1, bins = bins, normed = True, range=(0,1.0) )
    plt.plot( FA_bins[1:], np.cumsum(FA)/np.sum(FA), linestyle = "-" ,color = 'blue', linewidth = 3,\
    label = 'IP$_{%s}$'%(catalog[0]) )
  
    #Loading Indexes of IP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_IP2 = tmp.T[1]
    #Fractional Anisotropy
    FA_IP2 = Fractional_Anisotropy( eig2[1][i_IP2.astype(int)-1],\
    eig2[2][i_IP2.astype(int)-1], eig2[3][i_IP2.astype(int)-1] )
    FA, FA_bins = np.histogram( FA_IP2, bins = bins, normed = True, range=(0,1.0) )
    plt.plot( FA_bins[1:], np.cumsum(FA)/np.sum(FA), linestyle = "--" ,color = 'blue', linewidth = 3,\
    label = 'IP$_{%s}$'%(catalog[1]) )  
  
  
    #Loading Indexes of RIP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_RIP1 = tmp.T[1]
    #Fractional Anisotropy
    FA_RIP1 = Fractional_Anisotropy( eig1[1][i_RIP1.astype(int)-1],\
    eig1[2][i_RIP1.astype(int)-1], eig1[3][i_RIP1.astype(int)-1] )
    FA, FA_bins = np.histogram( FA_RIP1, bins = bins, normed = True, range=(0,1.0) )
    plt.plot( FA_bins[1:], np.cumsum(FA)/np.sum(FA), linestyle = "-" ,color = 'red', linewidth = 3,\
    label = 'RIP$_{%s}$'%(catalog[0]) )
    #Loading Indexes of RIP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_RIP2 = tmp.T[1]    
    #Fractional Anisotropy
    FA_RIP2 = Fractional_Anisotropy( eig2[1][i_RIP2.astype(int)-1],\
    eig2[2][i_RIP2.astype(int)-1], eig2[3][i_RIP2.astype(int)-1] )
    FA, FA_bins = np.histogram( FA_RIP2, bins = bins, normed = True, range=(0,1.0) )
    plt.plot( FA_bins[1:], np.cumsum(FA)/np.sum(FA), linestyle = "--" ,color = 'red', linewidth = 3,\
    label = 'RIP$_{%s}$'%(catalog[1]) )

    
plt.grid()
plt.xlim( (0.0,1.0) )
plt.ylim( (0.0,1.0) )
plt.text( 0.0, 0.05, " %s"%(web) )
plt.xlabel( "$FA$" )
plt.ylabel( "Cumlative Distribution $P(FA)$" )
plt.legend( loc='upper left', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )


plt.show()