#samples_totalmass_FA.py
#
#This code calculate 2D histogram of the total mass of the pair samples vs the fractional anisotropy
#index of each respective system. 1D Histograms are also performed in order to determinate single
#distrbutions of each propertie
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
#Mass limits
MT_lim = (1.0, 10.0)
#FA limits
FA_lim = (0.0, 1.0)

#Mass_norm
M_norm = 1e12

#Distribution ranges
Dist_FA_range = [0, 0.5, 1.0, 1.5, 2.0, 2.5]
Dist_MT_range = [0, 0.1, 0.2, 0.3]

#Bins of IP systems
bins_IP  = 10
#Bins of RIP systems
bins_RIP  = 10

#==================================================================================================
#			COMPUTING VELOCITIES FOR EACH SAMPLE
#==================================================================================================

i_fold = 0
N_sim = len(folds)

#no labels
nullfmt = NullFormatter()

#definitions for the axes
left, width = 0.1, 0.65
bottom_v, height = 0.1, 0.65
bottom_h = left_h = left+width+0.02

rect_hist2D = [left, bottom_v, width, height]
rect_histx = [left, bottom_h, 1.335*width, 0.2]
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
    print fold
    
    #Loading eigenvalues
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    
    #Loading IP sample
    tmp = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog))
    i_IP = tmp.T[1]
    Mtot_IP = (tmp.T[2] + tmp.T[5])/M_norm
    #Fractional Anisotropy
    FA_IP = Fractional_Anisotropy( eig[1][i_IP.astype(int)-1], eig[2][i_IP.astype(int)-1], eig[3][i_IP.astype(int)-1] )
    
    #Loading Indexes of RIP sample for scheme 1
    tmp = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog))
    i_RIP = tmp.T[1]
    Mtot_RIP = (tmp.T[2] + tmp.T[5])/M_norm
    #Fractional Anisotropy
    FA_RIP = Fractional_Anisotropy( eig[1][i_RIP.astype(int)-1], eig[2][i_RIP.astype(int)-1], eig[3][i_RIP.astype(int)-1] )

    #Scatter of RIP systems
    axHist2D.plot( FA_RIP, Mtot_RIP, "o", color = "blue"  )

    #Histogram of IP systems
    Hist_MT_FA = np.transpose(np.histogram2d( FA_IP, Mtot_IP, 
    bins = bins_IP, normed = False, range = (FA_lim, MT_lim)  )[0][::,::-1])
    
    #2D histogram
    map2d = axHist2D.imshow( Hist_MT_FA[::,::], interpolation='nearest', aspect = 'auto',
    cmap = 'binary', extent = (FA_lim[0],FA_lim[1],MT_lim[0],MT_lim[1]) )
    #Create the colorbar
    axc, kw = matplotlib.colorbar.make_axes( axHistx,\
    orientation = "vertical", shrink=1., pad=.1, aspect=10 )
    cb = matplotlib.colorbar.Colorbar( axc, map2d,\
    orientation = "vertical" )
    #Set the colorbar
    map2d.colorbar = cb
   
    #Countorn
    axHist2D.contour( Hist_MT_FA[::-1,::], 7, aspect = 'auto', 
    extent = (FA_lim[0],FA_lim[1],MT_lim[0],MT_lim[1]), linewidth=2.0, interpolation = 'gaussian',\
    colors="black" )
    
    #Scatter of RIP systems
    axHist2D.plot( FA_RIP, Mtot_RIP, "o", color = "blue"  )
    
    #Histogram X
    histx = np.histogram( FA_IP, bins=bins_IP, normed=True, range=FA_lim )
    axHistx.bar( histx[1][:-1], histx[0], width = (FA_lim[1]-FA_lim[0])/bins_IP, linewidth=2.0, color="gray" )
    #Histogram Y
    histy = np.histogram( Mtot_IP, bins=bins_IP, normed=True, range=MT_lim )
    axHisty.barh( histy[1][:-1], histy[0], height = (MT_lim[1]-MT_lim[0])/bins_IP, linewidth=2.0, color="gray" )
  
      
    i_fold += 1

axHistx.set_xlim( axHist2D.get_xlim() )
axHistx.set_xticks( np.linspace( FA_lim[0],FA_lim[1],bins_IP+1 ) )
axHistx.set_yticks( Dist_FA_range )
axHistx.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHistx.set_ylabel( "Normed distribution" )

axHisty.set_ylim( axHist2D.get_ylim() )
axHisty.set_yticks( np.linspace( MT_lim[0],MT_lim[1],bins_IP+1 ) )
axHisty.set_xticks( Dist_MT_range )
axHisty.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHisty.set_xlabel( "Normed distribution" )

axHist2D.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHist2D.set_xticks( np.linspace( FA_lim[0],FA_lim[1],bins_IP+1 ) )
axHist2D.set_yticks( np.linspace( MT_lim[0],MT_lim[1],bins_IP+1 ) )
axHist2D.set_xlabel( "Fractional Anisotropy FA", fontsize=15 )
axHist2D.set_ylabel( "$M_{tot} = M_A + M_B$ [$\\times 10 ^{12}h^{-1}\ M_{\odot}$]", fontsize=15 )

#Fixing ranges of total mass
for i in xrange(1,5):
    axHist2D.hlines(MT_lim[0] + i*(MT_lim[1] - MT_lim[0])/5., FA_lim[0], FA_lim[1],\
    linestyle="--", color="black", linewidth = 2.0, alpha = 0.8 )


plt.show()