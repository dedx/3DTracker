#######################################
#
# Niffte geometry methods to convert
# voxel to space point in cm
#
# J.L. Klay
# 14-May-2012
#
#######################################
import math
import Voxel as vox
import SpacePoint as sp

def MapVoxeltoXYZ(voxel):
    """Map the indices to x,y,z coordinates for
    the NIFFTE detector geometry.
    """
    fA = 0.1 # (cm) parameter for hexagonal geometry
    fB = 2.0 * fA / math.sqrt(3.0) # (cm) parameter for hexagonal geometry
    fCenterX = 47.0 # (cm) offset to center of volume
    fCenterY = 61.0 # (cm) offset to center of volume

    # In this (r,c) coordinate system, the Hex at (0,1) is
    # down and to the right of (0,0).
    x = voxel.column * 1.5 * fB
    y = -voxel.row * 2.0 * fA + math.fabs((voxel.column+1) % 2 * fA)

    # Shift the row/col coordinate system so that x=y=0.0
    # is at the center of the row/col field
    x -= fCenterX * fB;
    y += fCenterY * fA;

    # Now work on z coordinate
    fDriftDistance = 5.4 # (cm) size of drift volume
    fClockRate = 50.0 # MHz
    fDriftSpeed = 5.2 # (cm/us) default value
    fNumberOfBuckets = int(fDriftDistance * fClockRate / fDriftSpeed) # number of buckets per volume
    z = (fDriftDistance - float(voxel.bucket) + 0.5) * fDriftDistance/fNumberOfBuckets

    if (voxel.volume == 0):
        z = -z
    if (voxel.volume == 1):
       x = -x

    point = sp.SpacePoint(x,y,z)
    return point
