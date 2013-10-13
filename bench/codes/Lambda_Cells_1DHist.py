execfile('_Head.py')

#==================================================================================================
#			PARAMETERS
#==================================================================================================
#Simulation
folds = ["BOLSHOI/","CLUES/10909/","CLUES/16953/","CLUES/2710/"]
#Number of sections
N_sec = [256,64,64,64]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Vweb'

#N Lambda
N_l_Bolsh = 250
N_l_BolshH = 100

N_l_Clues = 500
N_l_CluesH = 100
#Lambdas Extreme
L_ext = 2


#==================================================================================================
#			CONSTRUCTING EIGENVALUES 1D HISTOGRAMS
#==================================================================================================

i_fold = 0
Lambda1 = np.zeros( (2,N_l_Clues) )
Lambda2 = np.zeros( (2,N_l_Clues) )
Lambda3 = np.zeros( (2,N_l_Clues) )

Lambda1H = []
Lambda2H = []
Lambda3H = []

plt.figure( figsize=(4,4) )
for fold in folds:
    print fold

    #Loading eigenvalues
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    #Loading environment properties of halos
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%(foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    
    #CLUES simulation
    if fold != "BOLSHOI/":
      	#LAMBDA 1 --------------------
	#Cells
	tmp = EigenHist1D( eigV_filename, 1, L_ext, N_l_Clues )
	Lambda1[0] = tmp[0]
	Lambda1[1] += tmp[1]
	#Halos
	Lambda1H += list(eig[1])
	if i_fold == len(folds)-1:
	    #Cells
	    plt.plot( Lambda1[0], Lambda1[1]/(np.sum(Lambda1[1])*2.*L_ext/N_l_Clues ), 
	    color = "blue",linewidth = 2, label = 'CLUES' )
	    #Halos
	    L1H, C_L1H = Hist1D( Lambda1H, L_ext, N_l_CluesH )
	    plt.plot( L1H, C_L1H /(np.sum(C_L1H )*2.*L_ext/N_l_CluesH ), 
	    color = "blue",linewidth = 1.5, linestyle = '--' )

	##LAMBDA 2 --------------------
	##Cells
	#tmp = EigenHist1D( eigV_filename, 2, L_ext, N_l_Clues )
	#Lambda2[0] = tmp[0]
	#Lambda2[1] += tmp[1]
	##Halos
	#Lambda2H += list(eig[2])
	#if i_fold == len(folds)-1:
	    ##Cells
	    #plt.plot( Lambda2[0], Lambda2[1]/(np.sum(Lambda2[1])*2.*L_ext/N_l_Clues ), 
	    #color = "blue",linewidth = 2, label = 'CLUES' )
	    ##Halos
	    #L2H, C_L2H = Hist1D( Lambda2H, L_ext, N_l_CluesH )
	    #plt.plot( L2H, C_L2H /(np.sum(C_L2H )*2.*L_ext/N_l_CluesH ), 
	    #color = "blue",linewidth = 1.5, linestyle = '--' )
	    
	##LAMBDA 3 --------------------
	##Cells
	#tmp = EigenHist1D( eigV_filename, 3, L_ext, N_l_Clues )
	#Lambda3[0] = tmp[0]
	#Lambda3[1] += tmp[1]
	##Halos
	#Lambda3H += list(eig[3])
	#if i_fold == len(folds)-1:
	    ##Cells
	    #plt.plot( Lambda3[0], Lambda3[1]/(np.sum(Lambda3[1])*2.*L_ext/N_l_Clues ), 
	    #color = "blue",linewidth = 2, label = 'CLUES' )
	    ##Halos
	    #L3H, C_L3H = Hist1D( Lambda3H, L_ext, N_l_CluesH )
	    #plt.plot( L3H, C_L3H /(np.sum(C_L3H )*2.*L_ext/N_l_CluesH ), 
	    #color = "blue",linewidth = 1.5, linestyle = '--' )
    
    
    #Cosmic Variance and Bolshoi simulation
    if fold == "BOLSHOI/":
      	#LAMBDA 1 --------------------
	#Cells
	Lamb, LV1_min, LV1_max = EigenHist1DVariance( eigV_filename, 1, L_ext, N_l_Bolsh, 4 )
	plt.fill_between( Lamb, LV1_min, LV1_max, color = 'red', alpha = 0.5 )
	LambdaB1 = EigenHist1D( eigV_filename, 1, L_ext, N_l_Bolsh )
	plt.plot( LambdaB1[0], LambdaB1[1]/( np.sum(LambdaB1[1])*2.*L_ext/N_l_Bolsh ), 
	color = "black", linewidth = 2, label = 'Bolshoi' )
	#Halos
	L1H, C_L1H = Hist1D( eig[1], L_ext, N_l_BolshH )
	plt.plot( L1H, C_L1H /(np.sum(C_L1H )*2.*L_ext/N_l_BolshH ), 
	color = "black",linewidth = 1.5, linestyle = '--' )
      
	##LAMBDA 2 --------------------
	##Cells
	#Lamb, LV2_min, LV2_max = EigenHist1DVariance( eigV_filename, 2, L_ext, N_l_Bolsh, 4 )
	#plt.fill_between( Lamb, LV2_min, LV2_max, color = 'red', alpha = 0.5 )
	#LambdaB2 = EigenHist1D( eigV_filename, 2, L_ext, N_l_Bolsh )
	#plt.plot( LambdaB2[0], LambdaB2[1]/( np.sum(LambdaB2[1])*2.*L_ext/N_l_Bolsh ), 
	#color = "black", linewidth = 2, label = 'Bolshoi' )
	##Halos
	#L2H, C_L2H = Hist1D( eig[2], L_ext, N_l_BolshH )
	#plt.plot( L2H, C_L2H /(np.sum(C_L2H )*2.*L_ext/N_l_BolshH ), 
	#color = "black",linewidth = 1.5, linestyle = '--' )
	
	##LAMBDA 3 --------------------
	##Cells
	#Lamb, LV3_min, LV3_max = EigenHist1DVariance( eigV_filename, 3, L_ext, N_l_Bolsh, 4 )
	#plt.fill_between( Lamb, LV3_min, LV3_max, color = 'red', alpha = 0.5 )
	#LambdaB3 = EigenHist1D( eigV_filename, 3, L_ext, N_l_Bolsh )
	#plt.plot( LambdaB3[0], LambdaB3[1]/( np.sum(LambdaB3[1])*2.*L_ext/N_l_Bolsh ), 
	#color = "black", linewidth = 2, label = 'Bolshoi' )
	##Halos
	#L3H, C_L3H = Hist1D( eig[3], L_ext, N_l_BolshH )
	#plt.plot( L3H, C_L3H /(np.sum(C_L3H )*2.*L_ext/N_l_BolshH ), 
	#color = "black",linewidth = 1.5, linestyle = '--' )
    
        
    i_fold += 1


#plt.subplot(1,3,1)
plt.grid()
plt.xlim( (-0.5,1.5) )
plt.ylim( (0.0,6) )
plt.xlabel( "$\lambda_1$" )
plt.ylabel( "Distribution [Normalized Area]" )
plt.legend( loc='upper center', fancybox = True, shadow = True, title="Simulations", ncol = 2 )

#plt.subplot(1,3,2)
#plt.grid()
#plt.xlim( (-1,1) )
#plt.ylim( (0.0,6) )
#plt.xlabel( "$\lambda_2$" )
#plt.ylabel( "Distribution [Normalized Area]" )
#plt.title( "Distribution of V-web eigenvalues in cells\n" )

#plt.subplot(1,3,3)
#plt.grid()
#plt.xlim( (-1.5,0.5) )
#plt.ylim( (0.0,6) )
#plt.xlabel( "$\lambda_3$" )
#plt.ylabel( "Distribution [Normalized Area]" )


plt.show()