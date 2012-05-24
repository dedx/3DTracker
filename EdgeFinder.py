####################################
#
# Find the 3d connected tracks in
# a list of points and return a
# list of point arrays
#
# J.L. Klay
# 19-May-2012
#
####################################
import math
import numpy as np
import SpacePoint as sp
import Voxel as vox



def FindTracks(voxels):
    """Given an array of voxels, find the ones that belong to
    straight line tracks.  Return a list of track arrays of space points"""

    tracks = []

    #compute the gradient for every voxel by taking the difference
    between the current adc and the neighbor adc in all directions.
    Each voxel will then have 
    for pt in points:
    	
