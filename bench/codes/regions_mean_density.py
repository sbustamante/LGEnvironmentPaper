#regions_mean_density.py
#
#This code calculates the mean density (dark matter density) in different zones (void, sheet, 
#filament, knot) in order to define the best value to reproduce the visual impression of the cosmic 
#web.
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
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
webs = ['Vweb', 'Tweb']

#N Lambda
N_l = 100
#Lambdas Extremes
L_min = 0
L_max = 2


#==================================================================================================
#			CONSTRUCTING REGIONS VOLUME
#==================================================================================================

N_sim = len(folds)

plt.figure( figsize=(6.0,2*4) )
for web in webs:
    i_fold = 0
    for fold in folds:
	print fold, web
	
	#Loading eigenvalues
	eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
	#Loading density
	delta_filename = '%s%sTweb/%d/Delta%s'%(foldglobal,fold,N_sec[i_fold],smooth)
	#Loading environment properties of halos
	eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))

	#Calculating mean densities associated to differents kind of regions
	regs = Counts( eigV_filename, delta_filename, L_min, L_max, N_l )
	print 'Mean density of regions for %s: done!'%(fold)
	
	#Lambda_th array
	lambda_th = regs[0]
	#Vacuums mean density
	vacuum_rho = regs[1]/regs[9]
	      
	#Plots the results
	
	#Voids
	plt.subplot( 2,1,1 )
	plt.plot( lambda_th, regs[1]/(1+regs[5]), linewidth = 2, label = '%s'%(web) )
	#Tweb threshold
	plt.vlines( 0.3262, -1.0, 1.0, linestyle = '--', color='green', linewidth = 2 )
	#Vweb threshold
	plt.vlines( 0.1884, -1.0, 1.0, linestyle = '--', color='blue', linewidth = 2 )
	
	#Sheets
	plt.subplot( 2,1,2 )
	plt.plot( lambda_th, regs[2]/(1+regs[6]), linewidth = 2, label = '%s'%(web) )
	#Tweb threshold
	plt.vlines( 0.3262, -1.0, 1.0, linestyle = '--', color='green', linewidth = 2 )
	#Vweb threshold
	plt.vlines( 0.1884, -1.0, 1.0, linestyle = '--', color='blue', linewidth = 2 )
	plt.hlines( 0.0, 0.0, 1.0, linestyle = '--', color='gray', linewidth = 2 )
	
	i_fold += 1
    

#Mean Density
plt.subplot( 2,1,1 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
plt.ylim( (-1.0, 1.0) )
plt.xlim( (0.0, 1.0) )
plt.text( 0.0, 0.5, ' Voids' )
plt.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1)

plt.subplot( 2,1,2 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
plt.ylim( (-1.0, 1.0) )
plt.xlim( (0.0, 1.0) )
plt.text( 0.0, 0.5, ' Sheets' )


plt.show()