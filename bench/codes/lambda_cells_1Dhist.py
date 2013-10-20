#Lambda_cells_1Dhist.py
#
#This code calculate the histogram of eigenvalues for both defined web schemes and for both halos 
#finding schemes. The plot is done for cells of the simulation, IP sample and RIP sample.
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

#N Lambda
N_l_Bolsh = 250
N_l_BolshH = 100

#Lambdas Extreme
L_ext = 4.0
#Lambda threshold
if web == "Vweb": lambda_th = 0.188
else: lambda_th = 0.326

#Eigenvalue
eigen = sys.argv[2]
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
    #Loading environment properties of halos scheme 2
    eig2 = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[1])))
    
    #Loading Indexes of IP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_IP1 = tmp.T[1] 
    #Loading Indexes of IP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_IP2 = tmp.T[1]
    
    #Loading Indexes of RIP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_RIP1 = tmp.T[1] 
    #Loading Indexes of RIP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_RIP2 = tmp.T[1]    
    
    if eigen == "1":
	#LAMBDA 1 --------------------
	print "Eigen 1"
	#Cells
	#Lamb, LV1_min, LV1_max = EigenHist1DVariance( eigV_filename, 1, L_ext, N_l_Bolsh, 4 )
	#plt.fill_between( Lamb, np.cumsum(LV1_min)/np.sum(LV1_min), np.cumsum(LV1_max)/np.sum(LV1_max),\
	#color = 'black', alpha = 0.5 )
	LambdaB1 = EigenHist1D( eigV_filename, 1, L_ext, N_l_Bolsh )
	plt.plot( LambdaB1[0], np.cumsum(LambdaB1[1])/np.sum(LambdaB1[1]), 
	color = "black", linewidth = 2.5, label = 'Cells' )
	    
	#Isolated Pairs for scheme 1
	L1IP, C_L1IP = Hist1D( eig1[1][i_IP1.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L1IP, np.cumsum(C_L1IP)/np.sum(C_L1IP), 
	color = "blue",linewidth = 2.0, linestyle = '-', label = 'IP$_{%s}$'%(catalog[0]) )
	#Isolated Pairs for scheme 2
	L1IP, C_L1IP = Hist1D( eig2[1][i_IP2.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L1IP, np.cumsum(C_L1IP)/np.sum(C_L1IP), 
	color = "red",linewidth = 2.0, linestyle = '-', label = 'IP$_{%s}$'%(catalog[1]) )
	
	#Reduced Isolated Pairs for scheme 1
	L1RIP, C_L1RIP = Hist1D( eig1[1][i_RIP1.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L1RIP, np.cumsum(C_L1RIP)/np.sum(C_L1RIP), 
	color = "blue",linewidth = 2.0, linestyle = '--', label = 'RIP$_{%s}$'%(catalog[0]) )
	#Isolated Pairs for scheme 2
	L1RIP, C_L1RIP = Hist1D( eig2[1][i_RIP2.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L1RIP, np.cumsum(C_L1RIP)/np.sum(C_L1RIP), 
	color = "red",linewidth = 2.0, linestyle = '--', label = 'RIP$_{%s}$'%(catalog[1]) )
    
    
    if eigen == "2":
	#LAMBDA 2 --------------------
	print "Eigen 2"
	#Cells
	#Lamb, LV2_min, LV2_max = EigenHist1DVariance( eigV_filename, 2, L_ext, N_l_Bolsh, 4 )
	#plt.fill_between( Lamb, np.cumsum(LV2_min)/np.sum(LV2_min), np.cumsum(LV2_max)/np.sum(LV2_max),\
	#color = 'black', alpha = 0.5 )
	LambdaB2 = EigenHist1D( eigV_filename, 2, L_ext, N_l_Bolsh )
	plt.plot( LambdaB2[0], np.cumsum(LambdaB2[1])/np.sum(LambdaB2[1]), 
	color = "black", linewidth = 2.5, label = 'Cells' )
	
	#Isolated Pairs for scheme 1
	L2IP, C_L2IP = Hist1D( eig1[2][i_IP1.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L2IP, np.cumsum(C_L2IP)/np.sum(C_L2IP), 
	color = "blue",linewidth = 2.0, linestyle = '-', label = 'IP$_{%s}$'%(catalog[0]) )
	#Isolated Pairs for scheme 2
	L2IP, C_L2IP = Hist1D( eig2[2][i_IP2.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L2IP, np.cumsum(C_L2IP)/np.sum(C_L2IP), 
	color = "red",linewidth = 2.0, linestyle = '-', label = 'IP$_{%s}$'%(catalog[1]) )
	
	#Reduced Isolated Pairs for scheme 1
	L2RIP, C_L2RIP = Hist1D( eig1[2][i_RIP1.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L2RIP, np.cumsum(C_L2RIP)/np.sum(C_L2RIP), 
	color = "blue",linewidth = 2.0, linestyle = '--', label = 'RIP$_{%s}$'%(catalog[0]) )
	#Isolated Pairs for scheme 2
	L2RIP, C_L2RIP = Hist1D( eig2[2][i_RIP2.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L2RIP, np.cumsum(C_L2RIP)/np.sum(C_L2RIP), 
	color = "red",linewidth = 2.0, linestyle = '--', label = 'RIP$_{%s}$'%(catalog[1]) )
    
    
    if eigen == "3":
	#LAMBDA 3 --------------------
	print "Eigen 3"
	#Cells
	#Lamb, LV3_min, LV3_max = EigenHist1DVariance( eigV_filename, 3, L_ext, N_l_Bolsh, 4 )
	#plt.fill_between( Lamb, np.cumsum(LV3_min)/np.sum(LV3_min), np.cumsum(LV3_max)/np.sum(LV3_max),\
	#color = 'black', alpha = 0.5 )
	LambdaB3 = EigenHist1D( eigV_filename, 3, L_ext, N_l_Bolsh )
	plt.plot( LambdaB3[0], np.cumsum(LambdaB3[1])/np.sum(LambdaB3[1]), 
	color = "black", linewidth = 2.5, label = 'Cells' )
	
	#Isolated Pairs for scheme 1
	L3IP, C_L3IP = Hist1D( eig1[3][i_IP1.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L3IP, np.cumsum(C_L3IP)/np.sum(C_L3IP), 
	color = "blue",linewidth = 2.0, linestyle = '-', label = 'IP$_{%s}$'%(catalog[0]) )
	#Isolated Pairs for scheme 2
	L3IP, C_L3IP = Hist1D( eig2[3][i_IP2.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L3IP, np.cumsum(C_L3IP)/np.sum(C_L3IP), 
	color = "red",linewidth = 2.0, linestyle = '-', label = 'IP$_{%s}$'%(catalog[1]) )
	
	#Reduced Isolated Pairs for scheme 1
	L3RIP, C_L3RIP = Hist1D( eig1[3][i_RIP1.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L3RIP, np.cumsum(C_L3RIP)/np.sum(C_L3RIP), 
	color = "blue",linewidth = 2.0, linestyle = '--', label = 'RIP$_{%s}$'%(catalog[0]) )
	#Isolated Pairs for scheme 2
	L3RIP, C_L3RIP = Hist1D( eig2[3][i_RIP2.astype(int)-1], L_ext, N_l_BolshH )
	plt.plot( L3RIP, np.cumsum(C_L3RIP)/np.sum(C_L3RIP), 
	color = "red",linewidth = 2.0, linestyle = '--', label = 'RIP$_{%s}$'%(catalog[1]) )
      
    i_fold += 1


if eigen == "1":
    #plt.subplot(1,3,1)
    plt.grid()
    plt.xlim( (-1.0,4.0) )
    plt.ylim( (0.0,1.0) )
    plt.xlabel( "$\lambda_1$" )
    plt.ylabel( "Cumulative Distribution [Normed]" )
    plt.vlines( lambda_th, 0.0, 1.0, linestyle='--', color='black', linewidth=2.5 )
    plt.text( -1.0, 0.05, " %s"%(web) )
    #plt.text( lambda_th, 0.9, " $\lambda_{th}$", fontsize = 16 )
    plt.legend( loc='lower right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )

if eigen == "2":
    #plt.subplot(1,3,2)
    plt.grid()
    plt.xlim( (-1.0,1.0) )
    plt.ylim( (0.0,1.0) )
    plt.xlabel( "$\lambda_2$" )
    plt.ylabel( "Cumulative Distribution [Normed]" )
    plt.vlines( lambda_th, 0.0, 1.0, linestyle='--', color='black', linewidth=2.5 )
    plt.text( -1.0, 0.05, " %s"%(web) )
    #plt.text( lambda_th, 0.05, " $\lambda_{th}$", fontsize = 16 )

if eigen == "3":
    #plt.subplot(1,3,3)
    plt.grid()
    plt.xlim( (-1.5,0.5) )
    plt.ylim( (0.0,1.0) )
    plt.xlabel( "$\lambda_3$" )
    plt.ylabel( "Cumulative Distribution [Normed]" )
    plt.vlines( lambda_th, 0.0, 1.0, linestyle='--', color='black', linewidth=2.5 )
    plt.text( -1.5, 0.05, " %s"%(web) )
    #plt.text( lambda_th, 0.05, " $\lambda_{th}$", fontsize = 16 )


plt.show()