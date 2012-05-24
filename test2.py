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
import Gradient as grad

points = []
voxels = []
fin = open('Niffte-event.dat')
for line in fin:
    data = (line.strip()).split()
    volume = int(data[0])
    row = int(data[1])
    column = int(data[2])
    bucket = int(data[3])
    adc = int(data[4])
    voxel = vox.Voxel(volume,row,column,bucket,adc)
    voxels.append(voxel)
    points.append(ngeo.MapVoxeltoXYZ(voxel))

#sort them in order of farthest from the origin (0,0,0) to closest
points.sort(key=attrgetter('mag'),reverse=True)

grad1 = []
for myvox in voxels:
    grad1.append(grad.ComputeGradient(myvox,voxels))

print grad1
