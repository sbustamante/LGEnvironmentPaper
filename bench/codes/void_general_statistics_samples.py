#void_distance_samples.py
#
#This code calculate histograms of distance to void regions of the near one for each defined sample
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
    
    #Loading voids catalogue of general halos scheme 1 (FOF)
    voids1 = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[0]))
    #Histogram
    dist_hist, distances = np.histogram( voids1[:,0], bins = bins, normed = True, range=(0,30.0) )
    plt.plot( distances[1:], np.cumsum(dist_hist[::-1])[::-1]/np.sum(dist_hist), linestyle = "-" ,
    color = 'black', linewidth = 3, label = 'GH$_{%s}$'%(catalog[0]) )
   
    #Loading voids catalogue of general halos scheme 2 (BDM)
    voids2 = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[1]))
    #Histogram
    dist_hist, distances = np.histogram( voids2[:,0], bins = bins, normed = True, range=(0,30.0) )
    plt.plot( distances[1:], np.cumsum(dist_hist[::-1])[::-1]/np.sum(dist_hist), linestyle = "--" ,\
    color = 'black', linewidth = 3, label = 'GH$_{%s}$'%(catalog[1]) )
    
    
    #Loading Indexes of IP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_IP1 = tmp.T[1] 
    #Histogram
    dist_hist, distances = np.histogram( voids1[i_IP1.astype(int)-1,0], bins = bins, normed = True, range=(0,30.0) )
    plt.plot( distances[1:], np.cumsum(dist_hist[::-1])[::-1]/np.sum(dist_hist), linestyle = "-" ,\
    color = 'blue', linewidth = 2, label = 'IP$_{%s}$'%(catalog[0]) )
    
    #Loading Indexes of IP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_IP2 = tmp.T[1]
    #Histogram
    dist_hist, distances = np.histogram( voids1[i_IP2.astype(int)-1,0], bins = bins, normed = True, range=(0,30.0) )
    plt.plot( distances[1:], np.cumsum(dist_hist[::-1])[::-1]/np.sum(dist_hist), linestyle = "--" ,\
    color = 'blue', linewidth = 2, label = 'IP$_{%s}$'%(catalog[1]) )
  
  
    #Loading Indexes of RIP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_RIP1 = tmp.T[1]
    #Histogram
    dist_hist, distances = np.histogram( voids1[i_RIP1.astype(int)-1,0], bins = bins, normed = True, range=(0,30.0) )
    plt.plot( distances[1:], np.cumsum(dist_hist[::-1])[::-1]/np.sum(dist_hist), linestyle = "-" ,\
    color = 'red', linewidth = 2, label = 'RIP$_{%s}$'%(catalog[0]) )

    #Loading Indexes of RIP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_RIP2 = tmp.T[1]    
    #Histogram
    dist_hist, distances = np.histogram( voids1[i_RIP2.astype(int)-1,0], bins = bins, normed = True, range=(0,30.0) )
    plt.plot( distances[1:], np.cumsum(dist_hist[::-1])[::-1]/np.sum(dist_hist), linestyle = "--" ,\
    color = 'red', linewidth = 2, label = 'RIP$_{%s}$'%(catalog[1]) )
   
   
    i_fold += 1
    

plt.grid()
plt.xlim( (0.0,14) )
plt.ylim( (0.0,1.0) )
plt.text( 0.0, 0.05, " %s"%(web) )
plt.xlabel( "Distance to the nearest void region [Mpc $h^{-1}$]" )
plt.ylabel( "Cumlative Distribution $P(d)$" )
plt.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )

plt.show()