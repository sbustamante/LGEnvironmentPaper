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

plt.figure( figsize=(2*5,2*3) )
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
	plt.subplot( 2,2,1 )
	plt.plot( lambda_th, regs[1]/regs[9], linewidth = 2, label = '%s'%(web) )
	#Tweb threshold
	plt.vlines( 0.61, -1.0, 1.0, linestyle = '--', color='green', linewidth = 2 )
	#Vweb threshold
	plt.vlines( 0.26, -1.0, 1.0, linestyle = '--', color='blue', linewidth = 2 )
	
	#Sheets
	plt.subplot( 2,2,2 )
	plt.plot( lambda_th, regs[2]/regs[9], linewidth = 2, label = '%s'%(web) )
	#Tweb threshold
	plt.vlines( 0.9, -1.0, 1.0, linestyle = '--', color='green', linewidth = 2 )
	#Vweb threshold
	plt.vlines( 0.5, -1.0, 1.0, linestyle = '--', color='blue', linewidth = 2 )
	
	#Filaments
	plt.subplot( 2,2,3 )
	plt.plot( lambda_th, regs[3]/regs[9], linewidth = 2, label = '%s'%(web) )
	#Tweb threshold
	plt.vlines( 0.13, -1.0, 1.0, linestyle = '--', color='green', linewidth = 2 )
	#Vweb threshold
	plt.vlines( 0.14, -1.0, 1.0, linestyle = '--', color='blue', linewidth = 2 )
		
	#Knots
	plt.subplot( 2,2,4 )
	plt.plot( lambda_th, regs[4]/regs[9], linewidth = 2, label = '%s'%(web) )
		
	i_fold += 1
    

plt.subplots_adjust( bottom = 0.08, top = 0.97 )

#Mean Density
plt.subplot( 2,2,1 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
#plt.legend( loc='upper center', fancybox = True, shadow = True, ncol = 1) #, title="Simulations" )
plt.grid()
#plt.xticks( (0.0,0.2,0.4,0.6,0.8,1.0), ("","","","","","") )
plt.yticks( (-0.5, -0.4, -0.3, -0.2, -0.1, 0.0 ) )
plt.ylim( (-0.5, 0.0) )
plt.text( 0.62, -0.38, 'Voids' )

plt.subplot( 2,2,2 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
#plt.xticks( (0.0,0.2,0.4,0.6,0.8,1.0), ("","","","","","") )
plt.yticks( (-0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2 ) )
plt.ylim( (-0.4, 0.2) )
plt.text( 0.52, -0.28, 'Sheets' )

plt.subplot( 2,2,3 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
#plt.xticks( (0.0,0.2,0.4,0.6,0.8,1.0), ("","","","","","") )
plt.yticks( (0.0, 0.1, 0.2, 0.3 ) )
plt.ylim( (-0.05, 0.3) )
plt.text( 0.52, 0.15, 'Filaments' )

plt.subplot( 2,2,4 )
plt.ylabel( "$\\bar \delta$" )
plt.xlabel( "$\lambda_{th}$" )
plt.grid()
plt.yticks( (0.0, 0.1, 0.2, 0.3 ) )
plt.text( 0.52, 0.15, 'Knots' )
plt.legend( fancybox = True, shadow = True, ncol = 1)

plt.show()