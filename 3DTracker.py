#####################################
#
# Main program for 3DTracker
#
#
# J.L. Klay
# 14-May-2012
#
#####################################
from operator import attrgetter
import numpy as np
import math
import time

import SpacePoint as sp
import TrackFit as tf
import NiffteGeo as ngeo
import Voxel as vox
import LSQ3D as lsq3d
import LineUtils as lin

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pylab

pylab.ion()
#pylab.hold(False)
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

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

       #sort them in order of farthest from the origin (0,0,0) to closest
       points.sort(key=attrgetter('mag'),reverse=True)

       print "Finding best fit line...\n"
       track = lsq3d.LSQ3D(points,weighted=True)

       print track

       #Plot results
       ax.clear()
       for pt in points:
	   ax.scatter(pt.x,pt.y,pt.z,color='r',marker='o',alpha=0.15)

       x = [track.start.x,track.end.x]
       y = [track.start.y,track.end.y]
       z = [track.start.z,track.end.z]
       ax.plot(x,y,z,color='b',linewidth=2)

       ax.set_xlabel("x (cm)")
       ax.set_ylabel("y (cm)")
       ax.set_zlabel("z (cm)")

       ax.set_xlim3d(-5.,5.)
       ax.set_ylim3d(-5.,5.)
       ax.set_zlim3d(-5.,5.)


#       ax.set_xlim3d(np.min(x)*1.25,max(np.max(x)*1.25,0.))
#       ax.set_ylim3d(np.min(y)*1.25,max(np.max(y)*1.25,0.))
#       ax.set_zlim3d(np.min(z)*1.25,max(np.max(z)*1.25,0.))

       plt.draw()
       var = raw_input("Press enter to continue or q to quit")
       if (var == 'q'):
          break

