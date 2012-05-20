##############################################
#
#
#
##############################################
from operator import attrgetter
import numpy as np
import math

import SpacePoint as sp
import NiffteGeo as ngeo
import Voxel as vox

import LineUtils as lin
import TrackFit as tf
import LSQ3D as lsq3d

points = []
fin = open('Niffte-event.dat')
for line in fin:
    data = (line.strip()).split()
    volume = int(data[0])
    row = int(data[1])
    column = int(data[2])
    bucket = int(data[3])
    adc = int(data[4])
    voxel = vox.Voxel(volume,row,column,bucket,adc)
    points.append(ngeo.MapVoxeltoXYZ(voxel))

#sort them in order of farthest from the origin (0,0,0) to closest
points.sort(key=attrgetter('mag'),reverse=True)

print "Finding best fit line...\n"
track = lsq3d.LSQ3D(points)

print track
#newe = (track.start).add((track.dir).scale(track.length))
#print newe

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

for pt in points:
    ax.scatter(pt.x,pt.y,pt.z,color='b',marker='o',alpha=0.15)

x = [track.start.x,track.end.x]
y = [track.start.y,track.end.y]
z = [track.start.z,track.end.z]
ax.plot(x,y,z,color='b',linewidth=2)

ax.set_xlabel("x (cm)")
ax.set_ylabel("y (cm)")
ax.set_zlabel("z (cm)")

ax.set_xlim3d(np.min(x)*1.25,max(np.max(x)*1.25,0.))
ax.set_ylim3d(np.min(y)*1.25,max(np.max(y)*1.25,0.))
ax.set_zlim3d(np.min(z)*1.25,max(np.max(z)*1.25,0.))

plt.show()

