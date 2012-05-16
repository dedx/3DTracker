#####################################
#
# Main program for 3DTracker
#
#
# J.L. Klay
# 14-May-2012
#
#####################################
import Utilities as util
import SpacePoint as sp
import NiffteGeo as ngeo
import Voxel as vox
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fin = open('NIFFTE-alphas.dat')
lines = fin.readlines()
lnum = 0
for line in lines:
    lnum += 1
    entries = (line.strip()).split()
    if entries[0] == "####":
       points = []
       event = entries[2]
       ndig = entries[5]
#       print "EVENT ", event, "NDIG ",ndig
       for i in range(int(ndig)):
       	   dataline = lines[lnum+i]
	   data = (dataline.strip()).split()
	   volume = int(data[0])
	   row = int(data[1])
	   column = int(data[2])
	   bucket = int(data[3])
	   adc = int(data[4])
	   voxel = vox.Voxel(volume,row,column,bucket,adc)
	   points.append(ngeo.MapVoxeltoXYZ(voxel))
#	   print voxel

       print "Event ",event," Num points = ",len(points)
       var = raw_input("Press enter to continue to the next event or q to quit.")
       if (var == 'q'):
          break
       if (var == 'p'):
       	  for pt in points:
	      print pt
       if (var == 'g'):
       	  fig = plt.figure()
	  ax = Axes3D(fig)
       	  for pt in points:
	      ax.scatter(pt.x,pt.y,pt.z,color='r',marker='o')
	  plt.show()
