execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["CLUES/2710/","CLUES/10909/","CLUES/16953/","BOLSHOI/"]
#Number of sections
N_sec = [64,64,64,256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#==================================================================================================
#			CONSTRUCTING EIGENVALUES EXTREME VALUES
#==================================================================================================
N_sim = len( folds )
ax = np.zeros( (3, N_sim) )

i_fold = 0
Lambda = 10*np.ones( (2,3) ); Lambda[1] = -Lambda[1]
for fold in folds:
    if fold == "BOLSHOI/":
	i_fold += 1
	continue
    print fold
    #Loading LG index of each simulation
    LG_Index = np.loadtxt('%s%s/LG_index_%s.dat'%(foldglobal,fold, catalog))
    #Loading environment properties of halos
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    #Loading environment of LG
    LG_prop = [ eig[:,int(LG_Index[0]-1)], eig[:,int(LG_Index[1]-1)] ]
    print LG_prop[0][1:4],"\n", LG_prop[1][1:4], "\n\n"
    
    for l in xrange(0,3):
	#minim value
	if LG_prop[0][l+1] <= Lambda[0,l]:
	    Lambda[0,l] = LG_prop[0][l+1]
	if LG_prop[1][l+1] <= Lambda[0,l]:
	    Lambda[0,l] = LG_prop[1][l+1]
	    
	#maxim value
	if LG_prop[0][l+1] >= Lambda[1,l]:
	    Lambda[1,l] = LG_prop[0][l+1]
	if LG_prop[1][l+1] >= Lambda[1,l]:
	    Lambda[1,l] = LG_prop[1][l+1]
	    
print Lambda,'\n\n\n'
	    
    
#==================================================================================================
#			CONSTRUCTING CLG SAMPLE
#==================================================================================================
i_fold = 0
for fold in folds:
    print fold
    #Loading halos catalogs
    IP = np.transpose(np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold, catalog)))
    Nip = len(IP[0])
    
    #Loading environment properties of halos
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    count = 0
    Index = []
    for i in xrange(Nip):
	i1 = IP[1,i] - 1
	i2 = IP[4,i] - 1
	
	Pass = True
	for l in xrange(0,3):
	    h = 0*abs(Lambda[0,l] - Lambda[1,l])/2.
	    if ( eig[l+1,i1] < Lambda[0,l] - h or Lambda[1,l] < eig[l+1,i1] - h ) or \
	    ( eig[l+1,i2] < Lambda[0,l] - h or Lambda[1,l] < eig[l+1,i2] - h ):
		Pass = False
	
	if Pass == True:
	    count += 1
	    Index.append(i)
	    
    print count
    
    #Saving Catalog
    np.savetxt('%s%s/C_CLGV_%s.dat'%(foldglobal,fold,catalog), np.transpose(IP[:,Index]),\
    fmt="%d\t%d\t%1.4e\t%d\t%d\t%1.4e\t%d\t%4.3f\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%4.3f\t%d\t%d\t%d" )
    i_fold += 1