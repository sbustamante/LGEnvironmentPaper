#void_intertia_tensor.py
#
#This code computes distributions of the eigenvalues of the reduced intertia tensor of each void 
#region found by the FOF scheme. The eigenvalues were sorted such as Lambda1 < Lambda2 < Lambda3.
#Here it will be calculated non-integrated and normed distributions of Lambda1/Lambda2 and 
#Lambda1/Lambda3 in order to determinate the shape of void regions.
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
#Box lenght [Mpc]
L_box = [250.]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme
catalog = 'FOF'
#Web Scheme
web = 'Tweb'
#Lambda_th
Lambda_th = 0.0
#Nbins of each histogram
Nbins = 20

#==================================================================================================
#			COMPUTING EIGENVALUES AND BUILDING THE INERTIA TENSOR
#==================================================================================================

i_fold = 0
N_sim = len(folds)

for fold in folds:
    print fold
    
    
    eigen = np.transpose(np.loadtxt( "%s/%s/%s/%d/voids%s/voids_%1.2f/eigen.dat"%\
    (foldglobal, fold, web, N_sec[i_fold], smooth, Lambda_th )))
  
    plt.subplot(131)
    plt.hist( eigen[0]/eigen[1], bins=Nbins )
    plt.subplot(132)
    plt.hist( eigen[0]/eigen[2], bins=Nbins )
    plt.subplot(133)
    plt.hist( eigen[1]/eigen[2], bins=Nbins )
    
      
    i_fold += 1

plt.subplot(131)
plt.xlim( (0,1) )

plt.subplot(132)
plt.xlim( (0,1) )

plt.subplot(133)
plt.xlim( (0,1) )
plt.show()