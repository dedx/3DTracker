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



def FindTracks(points):
    """Given and array of space points, find the ones that belong to
    straight line tracks.  Return a list of track arrays of points"""

    tracks = []

    for pt in points:
    	
