execfile('_Head.py')

webs = ["Tweb", "Vweb"]
catalogues = ["BDM", "FOF"]
distances = ["DistVoidCell", "DistVoidCenter"]
velocities = ["PecVel", "RadCenterPecVel", "RadCellPecVel", "TanCenterPecVel", "TanCellPecVel"]

for web in webs:
  for catalogue in catalogues:
    for dist in xrange(2):
      for vel in xrange(5):
	  print "%s_%s_%s_%s.dat"%(velocities[vel], distances[dist], catalogue, web)
	  os.system( "python samples_peculiarvelocity_VCdistance.py %s %s %d %d 1"%(web, catalogue, dist, vel) )
	  os.system( "mkdir voids_figures" )
	  os.system( "mv plotvel.pdf voids_figures/%s_%s_%s_%s.pdf"%(velocities[vel], distances[dist], catalogue, web) )