execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
#folds = ["BOLSHOI/","CLUES/10909/","CLUES/16953/","CLUES/2710/"]
folds = ["BOLSHOI/"]
#Number of sections
#N_sec = [256,64,64,64]
N_sec = [256]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#N Lambda
N_l = 100
#Lambdas Extremes
L_min = 0
L_max = 2


#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

i_fold = 0
N_sim = len(folds)

plt.figure( figsize=(2*5,2*3) )
for fold in folds:
    print fold
    
    #Loading eigenvalues
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    #Loading density
    delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
    #Loading environment properties of halos
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))

    #Calculating mean densities associated to differents kind of regions
    regs = Counts( eigV_filename, delta_filename, L_min, L_max, N_l )
    print 'Mean density of regions for %s: done!'%(fold)
    
    Lambda_th = 0.2
    
    void_matrix = void_matrix_builder( eigV_filename, Lambda_th, './void_matrix' )
    print 'Void matrix for %s: done!'%(fold)
       
    #Plots the results
    plt.subplot( 2,2,1 )
    plt.plot( regs[0], regs[1]/regs[9], color = 'black', linewidth = 2, label = 'Bolshoi' )
    plt.subplot( 2,2,2 )
    plt.plot( regs[0], regs[2]/regs[9], color = 'black', linewidth = 2, label = 'Bolshoi' )
    plt.subplot( 2,2,3 )
    plt.plot( regs[0], regs[3]/regs[9], color = 'black', linewidth = 2, label = 'Bolshoi' )
    plt.subplot( 2,2,4 )
    plt.plot( regs[0], regs[4]/regs[9], color = 'black', linewidth = 2, label = 'Bolshoi' )
    
    i_fold += 1
    

plt.subplots_adjust( bottom = 0.08, top = 0.97 )

#Mean Density
plt.subplot( 2,2,1 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.legend( loc='upper center', fancybox = True, shadow = True, ncol = 2) #, title="Simulations" )
plt.grid()
#plt.xticks( (0.0,0.2,0.4,0.6,0.8,1.0), ("","","","","","") )
plt.yticks( (-0.3, -0.2, -0.1, 0.0 ) )
plt.text( 0.62, -0.33, 'Vacuums' )

plt.subplot( 2,2,2 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
#plt.xticks( (0.0,0.2,0.4,0.6,0.8,1.0), ("","","","","","") )
plt.yticks( (-0.3, -0.2, -0.1, 0.0, 0.1 ) )
plt.text( 0.62, -0.28, 'Sheets' )

plt.subplot( 2,2,3 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
#plt.xticks( (0.0,0.2,0.4,0.6,0.8,1.0), ("","","","","","") )
plt.yticks( (0.0, 0.1, 0.2, 0.3 ) )
plt.text( 0.62, 0.22, 'Filaments' )

plt.subplot( 2,2,4 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
plt.yticks( (0.0, 0.1, 0.2, 0.3 ) )
plt.text( 0.62, 0.22, 'Knots' )

plt.show()