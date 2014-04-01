#void_general_statistics_samples.py
#
#This code calculate 2D histograms of distance vs volume of the nearest void regions for the 
#defined samples
#Usage: python void_general_statistics_samples.py <Web_Type> <Catalog_Type> <FA(0) or Environment(1)>
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
#Catalog Scheme [BDM, FOF]
catalog = sys.argv[2]
#Classification scheme [Tweb, Vweb]
web = sys.argv[1]
#Distance limits
Dis_lim = (0.0, 12.0)
#Speherical comoving volume limits (radius)
Vol_lim = (0.0, 6.0)

#Distribution ranges
dist_range = [0, 0.05, 0.1, 0.15, 0.2]
vol_range = [0, 0.1, 0.2, 0.3]

#Bins of IP systems
bins_IP  = 10
#Bins of RIP systems
bins_RIP  = 10

#Lambda_th [ Vweb=0.188, Tweb=0.326 ]
if web == "Vweb": lambda_th = 0.188
else: lambda_th = 0.326

#==================================================================================================
#			CONSTRUCTING STATISTICAL PROPERTIES OF VOIDS
#==================================================================================================
#Function to build the second axe
def tick_function(X):
    return ((10**X*(0.9765625)**3)/( 4*np.pi/3. ))**(1/3.)

i_fold = 0
N_sim = len(folds)

#no labels
nullfmt = NullFormatter()

#definitions for the axes
left, width = 0.1, 0.65
bottom_v, height = 0.1, 0.65
bottom_h = left_h = left+width+0.02

rect_hist2D = [left, bottom_v, width, height]
rect_histx = [left, bottom_h, 1.385*width, 0.2]
rect_histy = [left_h, bottom_v, 0.2, height]

#start with a rectangular Figure
plt.figure(1, figsize=(8,8))

axHist2D = plt.axes(rect_hist2D)
axHistx = plt.axes(rect_histx)
axHisty = plt.axes(rect_histy)

#no labels
axHistx.xaxis.set_major_formatter(nullfmt)
axHisty.yaxis.set_major_formatter(nullfmt)

for fold in folds:
    print fold, web
        
    #Loading voids catalogue of general halos detecting scheme
    voids1 = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog))
  
    #Loading file with sizes of found void regions
    void_size = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
    (foldglobal, fold, web, N_sec[i_fold], smooth, 0.0 ))

    #Loading Indexes of IP sample for halos detecting scheme
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog))
    i_IP = tmp.T[1] 
    
    #2D Histogram of distance vs Volume of GH
    Hist_D_R = np.transpose(np.histogram2d( voids1[i_IP.astype('int')-1,0], 
    np.log10(void_size[voids1[i_IP.astype('int')-1,1].astype('int')-1,1]), 
    bins = bins_IP, normed = False, range = (Dis_lim, Vol_lim)  )[0][::,::-1])

    #2D histogram
    map2d = axHist2D.imshow( Hist_D_R[::,::], interpolation='nearest', aspect = 'auto',
    cmap = 'binary', extent = (Dis_lim[0],Dis_lim[1],Vol_lim[0],Vol_lim[1]), alpha = 0.8 )
    #Create the colorbar
    axc, kw = matplotlib.colorbar.make_axes( axHistx,\
    orientation = "vertical", shrink=1., pad=.0, aspect=10, anchor=(0.3,1.3) )
    cb = matplotlib.colorbar.Colorbar( axc, map2d,\
    orientation = "vertical" )
    #Set the colorbar
    map2d.colorbar = cb
    
    #Countorn
    axHist2D.contour( Hist_D_R[::-1,::], 7, aspect = 'auto', 
    extent = (Dis_lim[0],Dis_lim[1],Vol_lim[0],Vol_lim[1]), linewidth=2.0, interpolation = 'gaussian',\
    colors="black" )
  
    #Histogram X
    histx = np.histogram( voids1[i_IP.astype('int')-1,0], bins=bins_IP, normed=True, range=Dis_lim )
    axHistx.bar( histx[1][:-1], histx[0], width = (Dis_lim[1]-Dis_lim[0])/bins_IP, linewidth=2.0, color="gray" )
    #Histogram Y
    histy = np.histogram( np.log10(void_size[voids1[i_IP.astype('int')-1,1].astype('int')-1,1]), bins=bins_IP,
    normed=True, range=Vol_lim )
    axHisty.barh( histy[1][:-1], histy[0], height = (Vol_lim[1]-Vol_lim[0])/bins_IP, linewidth=2.0, color="gray" )

    #RIP systems (Cataloguing according to the host kind of environment)

    #Loading Indexes of RIP sample for halos detecting scheme
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog))
    i_RIP = tmp.T[1] 
    vol_RIP = np.log10(void_size[voids1[i_RIP.astype(int)-1,1].astype(int)-1,1])
    dist_RIP = voids1[i_RIP.astype(int)-1,0]
    
    #Loading eigenvalues
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    #Loading environment properties of halos classification scheme
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    #Eigenvalues for the RIP sample
    eig1_RIP = eig[1][i_RIP.astype(int)-1]
    eig2_RIP = eig[2][i_RIP.astype(int)-1]
    eig3_RIP = eig[3][i_RIP.astype(int)-1]


    #Scatter of RIP systems
    
    if sys.argv[3] == "1":
	#Constructing volume and distances for each subsample according to their host environment
	#Voids
	i_RIP_voids = tmp.T[1,(eig1_RIP<=lambda_th)*(eig2_RIP<=lambda_th)*(eig3_RIP<=lambda_th)]
	vol_RIP_V = np.log10(void_size[voids1[i_RIP_voids.astype(int)-1,1].astype(int)-1,1])
	dist_RIP_V = voids1[i_RIP_voids.astype(int)-1,0]
	axHist2D.plot( dist_RIP_V, vol_RIP_V, "o", color = "dodgerblue", label = 'RIP in voids' )
	#Sheets
	i_RIP_sheets = tmp.T[1,(eig1_RIP>lambda_th)*(eig2_RIP<=lambda_th)*(eig3_RIP<=lambda_th)]
	vol_RIP_S = np.log10(void_size[voids1[i_RIP_sheets.astype(int)-1,1].astype(int)-1,1])
	dist_RIP_S = voids1[i_RIP_sheets.astype(int)-1,0]
	axHist2D.plot( dist_RIP_S, vol_RIP_S, "o", color = "red", label = 'RIP in sheets' )
	#Filaments
	i_RIP_filaments = tmp.T[1,(eig1_RIP>lambda_th)*(eig2_RIP>lambda_th)*(eig3_RIP<=lambda_th)]
	vol_RIP_F = np.log10(void_size[voids1[i_RIP_filaments.astype(int)-1,1].astype(int)-1,1])
	dist_RIP_F = voids1[i_RIP_filaments.astype(int)-1,0]
	axHist2D.plot( dist_RIP_F, vol_RIP_F, "o", color = "darkgreen", label = 'RIP in filaments' )
	#Knots
	i_RIP_knots = tmp.T[1,(eig1_RIP>lambda_th)*(eig2_RIP>lambda_th)*(eig3_RIP>lambda_th)]
	vol_RIP_K = np.log10(void_size[voids1[i_RIP_knots.astype(int)-1,1].astype(int)-1,1])
	dist_RIP_K = voids1[i_RIP_knots.astype(int)-1,0]
	axHist2D.plot( dist_RIP_K, vol_RIP_K, "o", color = "orange", label = 'RIP in knots' )
    elif sys.argv[3] == "0":
	#Using colors according to FA
	FA_RIP = Fractional_Anisotropy( eig1_RIP, eig2_RIP, eig3_RIP )
	scatter2d = axHist2D.scatter( dist_RIP, vol_RIP, c=FA_RIP, s=50, cmap='hot')
	#Create the colorbar
	axc, kw = matplotlib.colorbar.make_axes( axHistx,\
	orientation = "vertical", shrink=1., pad=.0, aspect=10, anchor=(.5,1.5) )
	cb = matplotlib.colorbar.Colorbar( axc, scatter2d,\
	orientation = "vertical" )
	#Set the colorbar
	map2d.colorbar = cb
    elif sys.argv[3] == "2":
      	#Using colors according to FA
	FA_RIP = Fractional_Anisotropy( eig1_RIP, eig2_RIP, eig3_RIP )
	#Constructing volume and distances for each subsample according to their FA range
	#Ranges according quartiles
	FA_RIP_sorted = np.sort(FA_RIP)
	R1 = FA_RIP_sorted[ int(len(FA_RIP)*1/4.) ]
	R2 = FA_RIP_sorted[ int(len(FA_RIP)*2/4.) ]
	R3 = FA_RIP_sorted[ int(len(FA_RIP)*3/4.) ]
	#First range ----------------------------------------------------------------
	i_RIP_R1 = tmp.T[1,(0<=FA_RIP)*(FA_RIP<R1)]
	vol_RIP_R1 = np.log10(void_size[voids1[i_RIP_R1.astype(int)-1,1].astype(int)-1,1])
	dist_RIP_R1 = voids1[i_RIP_R1.astype(int)-1,0]
	axHist2D.plot( dist_RIP_R1, vol_RIP_R1, "o", color = "lime", label = '$%1.2f\leq FA<%1.2f$'%(np.min(FA_RIP), R1) )
	#Histogram X
	histx = np.histogram( dist_RIP_R1 , bins=bins_IP, normed=True, range=Dis_lim )
	axHistx.bar( histx[1][:-1], histx[0], width = (Dis_lim[1]-Dis_lim[0])/bins_IP, linewidth=2.0, color="lime", alpha = 0.3 )
	#Histogram Y
	histy = np.histogram( vol_RIP_R1, bins=bins_IP, normed=True, range=Vol_lim )
	axHisty.barh( histy[1][:-1], histy[0], height = (Vol_lim[1]-Vol_lim[0])/bins_IP, linewidth=2.0, color="lime", alpha = 0.3 )
	
	#Second Range ----------------------------------------------------------------
	i_RIP_R2 = tmp.T[1,(R1<=FA_RIP)*(FA_RIP<R2)]
	vol_RIP_R2 = np.log10(void_size[voids1[i_RIP_R2.astype(int)-1,1].astype(int)-1,1])
	dist_RIP_R2 = voids1[i_RIP_R2.astype(int)-1,0]
	axHist2D.plot( dist_RIP_R2, vol_RIP_R2, "o", color = "yellow", label = '$%1.2f\leq FA<%1.2f$'%(R1, R2) )
	#Histogram X
	histx = np.histogram( dist_RIP_R2 , bins=bins_IP, normed=True, range=Dis_lim )
	axHistx.bar( histx[1][:-1], histx[0], width = (Dis_lim[1]-Dis_lim[0])/bins_IP, linewidth=2.0, color="yellow", alpha = 0.3 )
	#Histogram Y
	histy = np.histogram( vol_RIP_R2, bins=bins_IP, normed=True, range=Vol_lim )
	axHisty.barh( histy[1][:-1], histy[0], height = (Vol_lim[1]-Vol_lim[0])/bins_IP, linewidth=2.0, color="yellow", alpha = 0.3 )
	
	#Third Range ----------------------------------------------------------------
	i_RIP_R3 = tmp.T[1,(R2<=FA_RIP)*(FA_RIP<R3)]
	vol_RIP_R3 = np.log10(void_size[voids1[i_RIP_R3.astype(int)-1,1].astype(int)-1,1])
	dist_RIP_R3 = voids1[i_RIP_R3.astype(int)-1,0]
	axHist2D.plot( dist_RIP_R3, vol_RIP_R3, "o", color = "red", label = '$%1.2f\leq FA<%1.2f$'%(R2, R3) )
	#Histogram X
	histx = np.histogram( dist_RIP_R3 , bins=bins_IP, normed=True, range=Dis_lim )
	axHistx.bar( histx[1][:-1], histx[0], width = (Dis_lim[1]-Dis_lim[0])/bins_IP, linewidth=2.0, color="red", alpha = 0.3 )
	#Histogram Y
	histy = np.histogram( vol_RIP_R3, bins=bins_IP, normed=True, range=Vol_lim )
	axHisty.barh( histy[1][:-1], histy[0], height = (Vol_lim[1]-Vol_lim[0])/bins_IP, linewidth=2.0, color="red", alpha = 0.3 )
	
	#Fourth Range ----------------------------------------------------------------
	i_RIP_R4 = tmp.T[1,(R3<=FA_RIP)*(FA_RIP<1.0)]
	vol_RIP_R4 = np.log10(void_size[voids1[i_RIP_R4.astype(int)-1,1].astype(int)-1,1])
	dist_RIP_R4 = voids1[i_RIP_R4.astype(int)-1,0]
	axHist2D.plot( dist_RIP_R4, vol_RIP_R4, "o", color = "black", label = '$%1.2f\leq FA<%1.2f$'%(R3, np.max(FA_RIP)) )
	#Histogram X
	histx = np.histogram( dist_RIP_R4 , bins=bins_IP, normed=True, range=Dis_lim )
	axHistx.bar( histx[1][:-1], histx[0], width = (Dis_lim[1]-Dis_lim[0])/bins_IP, linewidth=2.0, color="black", alpha = 0.3 )
	#Histogram Y
	histy = np.histogram( vol_RIP_R4, bins=bins_IP, normed=True, range=Vol_lim )
	axHisty.barh( histy[1][:-1], histy[0], height = (Vol_lim[1]-Vol_lim[0])/bins_IP, linewidth=2.0, color="black", alpha = 0.3 )

    i_fold += 1
    
    
#axHistx.set_xlim( axHist2D.get_xlim() )
axHistx.set_xlim( Dis_lim )
axHistx.set_xticks( np.linspace( Dis_lim[0],Dis_lim[1],bins_IP+1 ) )
axHistx.set_yticks( dist_range )
axHistx.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHistx.set_ylabel( "Normed distribution" )

#axHisty.set_ylim( axHist2D.get_ylim() )
axHisty.set_ylim( Vol_lim )
axHisty.set_yticks( np.linspace( Vol_lim[0],Vol_lim[1],bins_IP+1 ) )
axHisty.set_xticks( vol_range )
axHisty.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHisty.set_xlabel( "Normed distribution" )

axHist2D.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHist2D.set_xlim( Dis_lim )
axHist2D.set_ylim( Vol_lim )
axHist2D.set_xticks( np.linspace( Dis_lim[0],Dis_lim[1],bins_IP+1 ) )
axHist2D.set_yticks( np.linspace( Vol_lim[0],Vol_lim[1],bins_IP+1 ) )
#Axis turned into equivalent radius of spherical comoving volume
tick_locations = np.linspace( Vol_lim[0],Vol_lim[1],bins_IP+1 )
tick_label = []
for tick in tick_locations:
    tick_label.append( "%1.1f"%tick_function(tick) )
axHist2D.set_yticklabels( tick_label )
axHist2D.set_xlabel( "Distance to nearest void [Mpc $h^{-1}$]" )
axHist2D.set_ylabel( "Equivalent spherical comoving radius Mpc $h^{-1}$" )
axHist2D.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )

plt.show()