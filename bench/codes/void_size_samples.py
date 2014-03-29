#void_size_samples.py
#
#This code calculate histograms of the size of void regions near to each one of the defined sample
#Usage: python void_size_samples.py <Web_Type>
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
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

N_sim = len(folds)

plt.figure( figsize=(5,4) )
i_fold = 0
for fold in folds:
    print fold, web
  
    #Loading file with sizes of found void regions
    void_size = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
    (foldglobal, fold, web, N_sec[i_fold], smooth, 0.0 ))
    
    
    #Loading voids catalogue of general halos scheme 1 (FOF)
    voids1 = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[0]))
    #Histogram
    voids = void_size[voids1[:,1].astype(int)-1,1]
    size_hist, sizes = np.histogram( np.log10(voids), bins = bins, normed = True, range=(0,5.0) )
    plt.plot( sizes[1:], np.cumsum(size_hist[::-1])[::-1]/np.sum(size_hist), linestyle = "-" ,\
    color = 'black', linewidth = 3, label = 'GH$_{%s}$'%(catalog[0]) )
   
    #Loading voids catalogue of general halos scheme 2 (BDM)
    voids2 = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[1]))
    #Histogram
    voids = void_size[voids2[:,1].astype(int)-1,1]
    size_hist, sizes = np.histogram( np.log10(voids), bins = bins, normed = True, range=(0,5.0) )
    plt.plot( sizes[1:], np.cumsum(size_hist[::-1])[::-1]/np.sum(size_hist), linestyle = "--" ,\
    color = 'black', linewidth = 3, label = 'GH$_{%s}$'%(catalog[1]) )
    
    
    #Loading Indexes of IP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_IP1 = tmp.T[1] 
    #Histogram
    voids = void_size[voids1[i_IP1.astype(int)-1,1].astype(int)-1,1]
    size_hist, sizes = np.histogram( np.log10(voids), bins = bins, normed = True, range=(0,5.0) )
    plt.plot( sizes[1:], np.cumsum(size_hist[::-1])[::-1]/np.sum(size_hist), linestyle = "-" ,\
    color = 'blue', linewidth = 2, label = 'IP$_{%s}$'%(catalog[0]) )
    
    #Loading Indexes of IP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_IP2 = tmp.T[1]
    #Histogram
    voids = void_size[voids2[i_IP2.astype(int)-1,1].astype(int)-1,1]
    size_hist, sizes = np.histogram( np.log10(voids), bins = bins, normed = True, range=(0,5.0) )
    plt.plot( sizes[1:], np.cumsum(size_hist[::-1])[::-1]/np.sum(size_hist), linestyle = "--" ,\
    color = 'blue', linewidth = 2, label = 'IP$_{%s}$'%(catalog[1]) )
  
  
    #Loading Indexes of RIP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_RIP1 = tmp.T[1]
    #Histogram
    voids = void_size[voids1[i_RIP1.astype(int)-1,1].astype(int)-1,1]
    size_hist, sizes = np.histogram( np.log10(voids), bins = bins, normed = True, range=(0,5.0) )
    plt.plot( sizes[1:], np.cumsum(size_hist[::-1])[::-1]/np.sum(size_hist), linestyle = "-" ,\
    color = 'red', linewidth = 2, label = 'RIP$_{%s}$'%(catalog[0]) )
    
    #Loading Indexes of RIP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_RIP2 = tmp.T[1]    
    #Histogram
    voids = void_size[voids2[i_RIP2.astype(int)-1,1].astype(int)-1,1]
    size_hist, sizes = np.histogram( np.log10(voids), bins = bins, normed = True, range=(0,5.0) )
    plt.plot( sizes[1:], np.cumsum(size_hist[::-1])[::-1]/np.sum(size_hist), linestyle = "--" ,\
    color = 'red', linewidth = 2, label = 'RIP$_{%s}$'%(catalog[1]) )
   
    i_fold += 1
    

plt.grid()
plt.xlim( (0.0,5.0) )
plt.ylim( (0.0,1.0) )
plt.text( 0.0, 0.05, " %s"%(web) )
plt.xlabel( "Comoving volume $\log_{10}[ (0.98$ Mpc $h^{-1} )^{-3} ]$" )
plt.ylabel( "Cumlative Distribution $P(\log_{10}V)$" )
#plt.legend( loc='lower left', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )

plt.show()