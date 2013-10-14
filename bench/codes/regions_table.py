#regions_table.py
#
#This code computes the different percentages for each sample, and for all the cells of the 
#simulation
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
#Lambda_th [ Vweb=0.188, Tweb=0.326 ]
if web == "Vweb": lambda_th = 0.188
else: lambda_th = 0.326

#==================================================================================================
#			CONSTRUCTING EIGENVALUES 1D HISTOGRAMS
#==================================================================================================

i_fold = 0

for fold in folds:
    print fold

    #Loading eigenvalues
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    #Loading density
    delta_filename = '%s%s%s/%d/Delta%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    #Counting eigenvalues of each cell of the simulation
    regs = Counts( eigV_filename, delta_filename, lambda_th, lambda_th, 1 )
    
    
    #Loading environment properties of halos scheme 1
    eig1 = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[0])))
    #Counting halos
    L, count_GH1 = Scheme1D( eig1[1], eig1[2], eig1[3],\
    lambda_th, lambda_th, 1 )
  
    #Loading environment properties of halos scheme 2
    eig2 = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog[1])))
    #Counting halos
    L, count_GH2 = Scheme1D( eig2[1], eig2[2], eig2[3],\
    lambda_th, lambda_th, 1 )    
    
    
    #Loading Indexes of IP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_IP1 = tmp.T[1]
    #Counting pairs
    L, count_IP1 = Scheme1D( eig1[1][i_IP1.astype(int)-1], eig1[2][i_IP1.astype(int)-1], eig1[3][i_IP1.astype(int)-1],\
    lambda_th, lambda_th, 1 )
    
    #Loading Indexes of IP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_IP2 = tmp.T[1]
    #Counting pairs
    L, count_IP2 = Scheme1D( eig2[1][i_IP2.astype(int)-1], eig2[2][i_IP2.astype(int)-1], eig2[3][i_IP2.astype(int)-1],\
    lambda_th, lambda_th, 1 )
    
    
    #Loading Indexes of RIP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[0]))
    i_RIP1 = tmp.T[1] 
    #Counting pairs
    L, count_RIP1 = Scheme1D( eig1[1][i_RIP1.astype(int)-1], eig1[2][i_RIP1.astype(int)-1], eig1[3][i_RIP1.astype(int)-1],\
    lambda_th, lambda_th, 1 )
    
    #Loading Indexes of RIP sample for scheme 2
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog[1]))
    i_RIP2 = tmp.T[1]
    #Counting pairs
    L, count_RIP2 = Scheme1D( eig2[1][i_RIP2.astype(int)-1], eig2[2][i_RIP2.astype(int)-1], eig2[3][i_RIP2.astype(int)-1],\
    lambda_th, lambda_th, 1 )
  
    #Printing table
    print "Web Scheme: %s"%(web)
    print "region\t\t\tCells\t\t\tGH_%s\t\tGH_%s\t\t\tIP_%s\t\tIP_%s\t\t\tRIP_%s\t\tRIP_%s\n"%\
    ( catalog[0],catalog[1], catalog[0],catalog[1], catalog[0],catalog[1] )
  
    print "voids\t\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\n"%\
    ( regs[5]/regs[9],\
      count_GH1[0][0]/np.sum(count_GH1), count_GH2[0][0]/np.sum(count_GH2),\
      count_IP1[0][0]/np.sum(count_IP1), count_IP2[0][0]/np.sum(count_IP2),\
      count_RIP1[0][0]/np.sum(count_RIP1), count_RIP2[0][0]/np.sum(count_RIP2) )
    
    print "sheets\t\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\n"%\
    ( regs[6]/regs[9],\
      count_GH1[1][0]/np.sum(count_GH1), count_GH2[1][0]/np.sum(count_GH2),\
      count_IP1[1][0]/np.sum(count_IP1), count_IP2[1][0]/np.sum(count_IP2),\
      count_RIP1[1][0]/np.sum(count_RIP1), count_RIP2[1][0]/np.sum(count_RIP2) )
    
    print "filaments\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\n"%\
    ( regs[7]/regs[9],\
      count_GH1[2][0]/np.sum(count_GH1), count_GH2[2][0]/np.sum(count_GH2),\
      count_IP1[2][0]/np.sum(count_IP1), count_IP2[2][0]/np.sum(count_IP2),\
      count_RIP1[2][0]/np.sum(count_RIP1), count_RIP2[2][0]/np.sum(count_RIP2) )
    
    print "knots\t\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\t\t\t%1.3f\t\t%1.3f\n"%\
    ( regs[8]/regs[9],\
      count_GH1[3][0]/np.sum(count_GH1), count_GH2[3][0]/np.sum(count_GH2),\
      count_IP1[3][0]/np.sum(count_IP1), count_IP2[3][0]/np.sum(count_IP2),\
      count_RIP1[3][0]/np.sum(count_RIP1), count_RIP2[3][0]/np.sum(count_RIP2) )