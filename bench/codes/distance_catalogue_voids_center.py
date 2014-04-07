#distance_catalogue_voids_center.py
#
#This code calculate a new catalogue of distances to the center of the nearest void based upon the
#already done catalogue of distances to the nearest cell of the nearest bulk void constructued by
#using the Void_Finder and Halos_distance packages. Instead of modifying the complete package in
#C to include this new criteria, which means a lot of computing time, it is performed this analysis
#over the already found regions, what are expected to be also the nearest regions according to the 
#geometric center.
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
#Size of the cubic simulation
L_box = [250.0]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme [BDM, FOF]
catalog = sys.argv[2]
#Classification scheme [Tweb, Vweb]
web = sys.argv[1]
#Lambda_th
Lambda_th = 0.0
#Numbers of close voids according to the distance to the nearest cell of the bulk void
N_voids = 3


#==================================================================================================
#			FUNCTION OF DISTANCES
#==================================================================================================
def distances( r, void, N_grid, L_box ):
    dist = np.zeros(3)
    for i_v in range( len(void) ):
	for i in range( 3 ): #X Y Z
	    try:
		distance = abs( r[i] - void[i_v,i]*L_box/N_grid )
	    except:
		distance = abs( r[i] - void[i]*L_box/N_grid )
	    if distance >= L_box/2.0: distance = abs( distance - L_box )
	    dist[i] += distance
    dist*=1.0/len(void)
    return norm(dist)

#==================================================================================================
#			CONSTRUCTING NEW CATALOGUE OF DISTANCES
#==================================================================================================

N_sim = len(folds)

i_fold = 0
for fold in folds:
    print fold, web
	    
    GH = np.loadtxt('%s%s/C_GH_%s.dat'%\
    (foldglobal,fold,catalog))
	
    IP = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog))
    i_IP = IP.T[1].astype(int)-1
	
    #Loading voids catalogue of general halos detecting scheme
    GH_catalogue1 = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog))
        
    #Distances for the current halo:
    dist_GH = np.zeros( (len(IP),2*N_voids+1) )
        
    for i_ip in xrange( len(IP) ):
	i_h = i_IP[i_ip]
	progress(50, int(100.*i_ip/len(IP)) )
	for i_v in xrange( N_voids ):
	    #Loading all cells of the current void
	    void_cells = np.loadtxt('%s%s%s/%d/voids%s/voids_%1.2f/void_%d.dat'%\
	    (foldglobal,fold,web,N_sec[i_fold],smooth,Lambda_th,GH_catalogue1[i_h,1+2*i_v]))
	    dist_GH[i_ip,1+2*i_v] = distances( GH[i_h,1:4], void_cells, N_sec[i_fold], L_box[i_fold] )
	    dist_GH[i_ip,2+2*i_v] = GH_catalogue1[i_h,1+2*i_v]
	    dist_GH[i_ip,0] = i_h + 1
	    
    np.savetxt( "./C_IP-GC_voids_s1_%s.dat"%(catalog), dist_GH, fmt="%d\t\t%1.6e\t%d\t%1.6e\t%d\t%1.6e\t%d" )
	    
    i_fold += 1