#samples_peculiarvelocity_VCdistance.py
#
#This code calculate 2D histograms of total peculiar velocity regarding the distance to the geometric
#center of the nearest void.
#Usage: python samples_peculiarvelocity_VCdistance.py 
#	* <Web_Type> 
#	* <Catalog_Type> 
#	* <Nearest cell(0),
#	   the nearest void center(1)> 
#	* <total peculiar velocity(0),
#	   radial projection to void geometric center (1),
#	   radial projection to the nearest void cell (2),
#	   tangential projection to void geometric center (3),
#	   tangential projection to the nearest void cell (4)>
#	* <show(0) or save(1)>
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
#Lenght of box [Mpc]
L_box = [250.0]
#Smooth parameter
smooth = '_s1'
#Catalog Scheme [BDM, FOF]
catalog = sys.argv[2]
#Classification scheme [Tweb, Vweb]
web = sys.argv[1]
#Void finder scheme (FOF or LAY)
void_scheme = 'FOF'
#Velocity normalization
V_norm = 1e2

#Distribution ranges
if sys.argv[3] == "0": dist_range = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
else:		       dist_range = [0, 0.02, 0.04, 0.06]
vel_range = [0, 0.1, 0.2, 0.3]

#Bins of IP systems
bins_IP  = 24
#Bins of RIP systems
bins_RIP  = 10


#Label fontsize
lab_font = 14

#==================================================================================================
#			CONSTRUCTING STATISTICAL PROPERTIES OF VOIDS
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
        
    #Loading voids catalogue of general halos
    voidsGH = np.loadtxt('%s%s%s/%d/C_GH-voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog))
  
    #Loading voids catalogue of IP sample
    voidsIP = np.loadtxt('%s%s%s/%d/C_IP-GC_voids%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog))
  
    #Loading file with sizes of found void regions
    void_size = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/void_regions.dat"%\
    (foldglobal, fold, web, N_sec[i_fold], void_scheme, 0.0 ))
    #Loading file with geometric center of void regions
    GC = np.loadtxt("%s/%s/%s/%d/voids%s/voids_%1.2f/GC.dat"%\
    (foldglobal, fold, web, N_sec[i_fold], void_scheme, 0.0 ))

    #Loading information 
    GH = np.loadtxt('%s%s/C_GH_%s.dat'%(foldglobal,fold,catalog))

    #Loading Indexes of IP sample for halos detecting scheme
    IP = np.loadtxt('%s%s/C_IP_%s.dat'%(foldglobal,fold,catalog))
    i_IP = IP.T[1].astype('int')-1

    #Peculiar velocity of IP systems
    #Halo 1
    i_IP1 = GH.T[1].astype(int)-1
    M_IP1 = GH[ i_IP1, 8 ]
    r_IP1 = np.transpose( [GH[ i_IP1, 1 ], GH[ i_IP1, 2 ], GH[ i_IP1, 3 ]] )
    v_IP1 = np.transpose( [GH[ i_IP1, 4 ], GH[ i_IP1, 5 ], GH[ i_IP1, 6 ]] )
    #Halo 2
    i_IP2 = GH.T[4].astype(int)-1
    M_IP2 = GH[ i_IP2, 8 ]
    r_IP2 = np.transpose( [GH[ i_IP2, 1 ], GH[ i_IP2, 2 ], GH[ i_IP2, 3 ]] )
    v_IP2 = np.transpose( [GH[ i_IP2, 4 ], GH[ i_IP2, 5 ], GH[ i_IP2, 6 ]] )
        
    #Distance to the nearest void
    dist_IP = np.zeros( len(i_IP) )
    vel_IP = np.zeros( len(i_IP) )
    pindex_IP = {}
    #Distance to the center of the nearest void
    for i_ip in range( len(i_IP) ):
	dist_array = voidsIP[ i_ip, [1,3,5] ]
	#i_min = dist_array.argsort()[-1]
	i_min = 0
	dist_IP[i_ip] = voidsIP[i_ip, 1+2*i_min]
	#Creating dictionary of Pair index for the RIP sample
	pindex_IP[ "%d"%(IP[i_ip,0]) ] = i_ip
	#Total peculiar velocity
	tot_v_vector = ( M_IP1[i_ip]*v_IP1[i_ip] + M_IP2[i_ip]*v_IP2[i_ip] )/( M_IP1[i_ip] + M_IP2[i_ip] )
	#Center of mass of the pair
	r_vector = ( M_IP1[i_ip]*r_IP1[i_ip] + M_IP2[i_ip]*r_IP2[i_ip] )/( M_IP1[i_ip] + M_IP2[i_ip] )
	
	#Vector towards void center from IP system
	u_center = np.zeros(3)
	try:
	    for i_u in xrange( 3 ):
		u_center[i_u] =  GC[ voidsGH[i_ip,1].astype(int)-1, i_u+1 ] - r_vector[i_u]
		if abs(u_center[i_u]) >= L_box[i_fold]/2.0 and u_center[i_u] > 0:
		    u_center[i_u] -= L_box[i_fold]
		if abs(u_center[i_u]) >= L_box[i_fold]/2.0 and u_center[i_u] < 0:
		    u_center[i_u] += L_box[i_fold]
	    #normalization
	    u_center *= 1.0/norm( u_center )
	except: pass
	
	#Vector towards the nearest cell of the nearest void from IP system
	u_cell = np.zeros(3)
	for i_u in xrange( 3 ):
	    u_cell[i_u] =  (voidsGH[i_ip,2+i_u] + 0.5)*L_box[i_fold]/(1.0*N_sec[i_fold]) - r_vector[i_u]
	    if abs(u_cell[i_u]) >= L_box[i_fold]/2.0 and u_cell[i_u] > 0:
		u_cell[i_u] -= L_box[i_fold]
	    if abs(u_cell[i_u]) >= L_box[i_fold]/2.0 and u_cell[i_u] < 0:
		u_cell[i_u] += L_box[i_fold]
	#normalization
	u_cell *= 1.0/norm( u_cell )
		
	#Different cases of peculiar velocity------------------------------------------------------
	# 0 -- Total magnitude of the peculiar velocity of the Pair
	if sys.argv[4] == '0':
	    vel_IP[i_ip] = norm( tot_v_vector )/V_norm
	# 1 -- Projection on the unitary vector towards the geometric center of the nearest void
	elif sys.argv[4] == '1':
	    vel_IP[i_ip] = np.sum( tot_v_vector*u_center )/V_norm
	# 2 -- Projection on the unitary vector towards the nearest cell of the nearest void
	elif sys.argv[4] == '2':
	    vel_IP[i_ip] = np.sum( tot_v_vector*u_cell )/V_norm
	# 3 -- Perpendicular projection on the unitary vector towards the geometric center of the nearest void
	elif sys.argv[4] == '3':
	    vel_IP[i_ip] = norm( tot_v_vector - tot_v_vector*u_center )/V_norm
	# 4 -- Perpendicular projection on the unitary vector towards the nearest cell of the nearest void
	elif sys.argv[4] == '4':
	    vel_IP[i_ip] = norm( tot_v_vector - tot_v_vector*u_cell )/V_norm
	    
    #Distance to the nearest cell of the nearest void
    if sys.argv[3] == "0":
	dist_IP = voidsGH[i_IP,0]

    #RIP systems ----------------------------------------------------------------------------------
    #Loading Indexes of RIP sample for halos detecting scheme
    RIP = np.loadtxt('%s%s/C_RIP_%s.dat'%(foldglobal,fold,catalog))
    i_RIP = RIP.T[1].astype(int)-1
    
    #Distance to the nearest void
    dist_RIP = np.zeros( len(i_RIP) )
    #Peculiar velocity
    vel_RIP = np.zeros( len(i_RIP) )
    #According to the nearest center of the void
    for i_rip in range( len(i_RIP) ):
	pindex_rip = pindex_IP[ "%d"%(RIP[i_rip,0]) ]
	dist_RIP[i_rip] = dist_IP[pindex_rip]
	vel_RIP[i_rip] = vel_IP[pindex_rip]
	
    #Calculating limits of plots
    #Distance limits
    Dis_lim = (np.min( np.floor(dist_RIP) ), np.max( np.ceil(dist_RIP) ))
    #Total peculiar velocity
    Vel_lim = (np.min( np.floor(vel_RIP) ), np.max( np.ceil(vel_RIP) ))
    if sys.argv[4] == '1' or sys.argv[4] == '2':
	Vel_ext = np.max( np.abs(Vel_lim) )
	Vel_ext = 3.6
	Vel_lim = (-Vel_ext,Vel_ext)

    #Side histograms of IP systems ----------------------------------------------------------------

    #2D Histogram of distance vs peculiar velocity of IP sample
    Hist_D_R = np.transpose(np.histogram2d( dist_IP[abs(vel_IP)>1e-3], vel_IP[abs(vel_IP)>1e-3],
    bins = bins_IP, normed = False, range = (Dis_lim, Vel_lim)  )[0][::,::-1])

    #2D histogram
    map2d = axHist2D.imshow( Hist_D_R[::,::], interpolation='nearest', aspect = 'auto',
    cmap = 'binary', extent = (Dis_lim[0],Dis_lim[1],Vel_lim[0],Vel_lim[1]), alpha = 0.8 )
    #Create the colorbar
    axc, kw = matplotlib.colorbar.make_axes( axHistx,\
    orientation = "vertical", shrink=1., pad=.0, aspect=10, anchor=(0.3,1.3) )
    cb = matplotlib.colorbar.Colorbar( axc, map2d,\
    orientation = "vertical" )
    cb.set_label("IP systems", labelpad=-50, fontsize=10, fontweight="bold")
    #Set the colorbar
    map2d.colorbar = cb
    
    #Countorn
    axHist2D.contour( Hist_D_R[::-1,::], 7, aspect = 'auto', 
    extent = (Dis_lim[0],Dis_lim[1],Vel_lim[0],Vel_lim[1]), linewidth=2.0, interpolation = 'gaussian',\
    colors="black" )
  
    #Histogram X (Distance)
    histx = np.histogram( dist_IP[abs(vel_IP)>1e-3], bins=bins_IP, normed=True, range=Dis_lim )
    axHistx.bar( histx[1][:-1], histx[0], width = (Dis_lim[1]-Dis_lim[0])/bins_IP, linewidth=2.0, color="gray" )
    #Histogram Y (Velocity)
    histy = np.histogram( vel_IP[abs(vel_IP)>1e-3], bins=bins_IP, normed=True, range=Vel_lim )
    axHisty.barh( histy[1][:-1], histy[0], height = (Vel_lim[1]-Vel_lim[0])/bins_IP, linewidth=2.0, color="gray" )


    #Calculating properties of RIP systems --------------------------------------------------------
    #Loading eigenvalues
    eigV_filename = '%s%s%s/%d/Eigen%s'%(foldglobal,fold,web,N_sec[i_fold],smooth)
    #Loading environment properties of halos classification scheme
    eig = np.transpose(np.loadtxt('%s%s%s/%d/E_GH%s_%s.dat'%\
    (foldglobal,fold,web,N_sec[i_fold],smooth,catalog)))
    #Eigenvalues for the RIP sample
    eig1_RIP = eig[1][i_RIP.astype(int)-1]
    eig2_RIP = eig[2][i_RIP.astype(int)-1]
    eig3_RIP = eig[3][i_RIP.astype(int)-1]


    #Using colors according to FA
    FA_RIP = Fractional_Anisotropy( eig1_RIP, eig2_RIP, eig3_RIP )
    scatter2d = axHist2D.scatter( dist_RIP, vel_RIP, c=FA_RIP, s=50, cmap='hot')
    #Create the colorbar
    axc, kw = matplotlib.colorbar.make_axes( axHistx,\
    orientation = "vertical", shrink=1., pad=.0, aspect=10, anchor=(.5,1.5) )
    cb = matplotlib.colorbar.Colorbar( axc, scatter2d,\
    orientation = "vertical" )
    cb.set_label("FA", labelpad=-50, fontsize=10, fontweight="bold")
    #Set the colorbar
    map2d.colorbar = cb
    
    i_fold += 1
        
#Label of ticks
def tick_label( x ):
    label = []
    for i in xrange( len(x) ):
	label.append( "%1.1f"%(x[i]) )
    return label
        
#axHistx.set_xlim( axHist2D.get_xlim() )
axHistx.set_xlim( Dis_lim )
axHistx.set_xticks( np.linspace( Dis_lim[0],Dis_lim[1],bins_IP+1 ) )
axHistx.set_yticks( dist_range )
axHistx.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHistx.set_ylabel( "Normed distribution" )

#axHisty.set_ylim( axHist2D.get_ylim() )
axHisty.set_ylim( Vel_lim )
axHisty.set_yticks( np.linspace( Vel_lim[0],Vel_lim[1],bins_IP+1 ) )
axHisty.set_xticks( vel_range )
axHisty.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHisty.set_xlabel( "Normed distribution" )

axHist2D.grid( color='black', linestyle='--', linewidth=1., alpha=0.3 )
axHist2D.set_xlim( Dis_lim )
axHist2D.set_ylim( Vel_lim )

axHist2D.set_xticks( np.linspace( Dis_lim[0],Dis_lim[1],bins_IP+1 )[::3] )
axHist2D.set_xticklabels( tick_label(np.linspace( Dis_lim[0],Dis_lim[1],bins_IP+1 )[::3]) )

axHist2D.set_yticks( np.linspace( Vel_lim[0],Vel_lim[1],bins_IP+1 ) )
axHist2D.set_yticklabels( tick_label(np.linspace( Vel_lim[0],Vel_lim[1],bins_IP+1 )) )

#X-label
if sys.argv[3] == '0':
    axHist2D.set_xlabel( "Distance to the nearest void [Mpc $h^{-1}$]", fontsize = 12 )
elif sys.argv[3] == '1':
    axHist2D.set_xlabel( "Distance to center of the nearest void [Mpc $h^{-1}$]", fontsize = 12 )

#Y-label
# 0 -- Total magnitude of the peculiar velocity of the Pair
if sys.argv[4] == '0':
    axHist2D.set_ylabel( "$|\\vec{v_{pec}}|$ [$\\times 10^{2} $km s$^{-1}$]", fontsize = lab_font )
# 1 -- Projection on the unitary vector towards the geometric center of the nearest void
elif sys.argv[4] == '1':
    axHist2D.set_ylabel( "$\\vec{v_{pec}}\ \cdot\ \hat{u}_{center}$ [$\\times 10^{2} $km s$^{-1}$]", fontsize = lab_font )
# 2 -- Projection on the unitary vector towards the nearest cell of the nearest void
elif sys.argv[4] == '2':
    axHist2D.set_ylabel( "$\\vec{v_{pec}}\ \cdot\ \hat{u}_{cell}$ [$\\times 10^{2} $km s$^{-1}$]", fontsize = lab_font )
# 3 -- Perpendicular projection on the unitary vector towards the geometric center of the nearest void
elif sys.argv[4] == '3':
    axHist2D.set_ylabel( "$|\\vec{v_{pec}} - (\\vec{v_{pec}}\ \cdot\ \hat{u}_{center})\hat{u}_{center}|$ [$\\times 10^{2} $km s$^{-1}$]",\
    fontsize = lab_font )
# 4 -- Perpendicular projection on the unitary vector towards the nearest cell of the nearest void
elif sys.argv[4] == '4':
    axHist2D.set_ylabel( "$|\\vec{v_{pec}} - (\\vec{v_{pec}}\ \cdot\ \hat{u}_{cell})\hat{u}_{cell}|$ [$\\times 10^{2} $km s$^{-1}$]",\
    fontsize = lab_font )

axHist2D.legend( loc='upper right', fancybox = True, shadow = True, ncol = 1, prop={'size':10} )
axHist2D.text( Dis_lim[-1]*0.8, Vel_lim[0] + (Vel_lim[-1]-Vel_lim[0])*0.03 , "%s %s"%(web,catalog),\
fontweight="bold", color="black",\
fontsize=11 )

if sys.argv[5] == '0':
    plt.show()
else:
    plt.savefig( 'plotvel.pdf' )