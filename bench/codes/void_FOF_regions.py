#void_matrix_builder.py
#
#This code builds the matrix associated with voids regions, where 0 isn't a void and 1 corresponds 
#to one. All of this for a specific lambda_th value (given). Besides, this code calculates the mean
#density (dark matter density) in different zones (void, sheet, filament, knot) in order to define 
#the best value to reproduce the visual impression of the cosmic web.
#
#by: Sebastian Bustamante

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
#Web Scheme
webs = ['Vweb', 'Tweb'] 

#Lambda values
Lambda_th = np.arange( 0, 1.0, 0.01 )

#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

i_fold = 0
N_sim = len(folds)

plt.figure( figsize=(7,2*5) )
for web in webs:
    for fold in folds:
	print fold, web
	
	N_voids = []
	Vol_1void = []
	
	for lamb in Lambda_th:
	    void_regs = np.transpose(np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
	    (foldglobal, fold, web, N_sec[i_fold], smooth, lamb )))
	    
	    N_voids.append( void_regs[0,-1] )
	    Vol_1void.append( void_regs[1,0]/np.sum(1.0*void_regs[1]) )
	    
	plt.subplot( 2,1,1 )
	plt.plot( Lambda_th, N_voids/N_voids[0], '-', linewidth = 2, label="%s"%(web) )
	
	plt.subplot( 2,1,2 )
	plt.plot( Lambda_th, Vol_1void , '-', linewidth = 2 )
    
    
plt.subplot( 2,1,1 )
plt.grid()
plt.ylabel( "Number of voids $N/N_0$" )
plt.xlabel( "$\lambda_{th}$" )
plt.legend()

plt.subplot( 2,1,2 )
plt.grid()
plt.ylabel( "Largest void volume  $V/V_{all}$" )
plt.xlabel( "$\lambda_{th}$" )

plt.show()