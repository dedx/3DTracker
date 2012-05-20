##############################################
#
# LineUtils
#
# module to hold utilities for calculating
# intersection points of lines with planes, etc.
#
# J.L. Klay
# 19-May-2012
#
##############################################
import math
import SpacePoint as sp

epsilon = 0.00000001

def ProjectedLinePointInPlane(start,end,plane,normal):
    """Given two points on a line, find the intersection of the line
    with a plane"""

    #Find the line point closest to the plane
    startDist = math.fabs(normal.x*(plane.x-start.x) + normal.y*(plane.y-start.y) + normal.z*(plane.z-start.z))/normal.mag
    endDist = math.fabs(normal.x*(plane.x-end.x) + normal.y*(plane.y-end.y) + normal.z*(plane.z-end.z))/normal.mag

    if (startDist <= endDist):
       close = sp.SpacePoint(start.x,start.y,start.z,start.wgt)
       far = sp.SpacePoint(end.x,end.y,end.z,end.wgt)
    else:
       far = sp.SpacePoint(start.x,start.y,start.z,start.wgt)
       close = sp.SpacePoint(end.x,end.y,end.z,end.wgt)

    #Get the vector pointing in the direction of the plane
    lineVec = close.subtract(far)

    #Make sure it is not a convergent
    if (lineVec.x < epsilon and lineVec.y < epsilon and lineVec.z < epsilon):
       print "Oops.  A convergent line segment is not allowed.  This should not happen."
       return sp.SpacePoint(-99.0,-99.0,-99.0,0.0) #zero weight and really out there

    #Normalize so we can get the proper distance from the plane
    nline = sp.SpacePoint(lineVec.x/lineVec.mag, lineVec.y/lineVec.mag, lineVec.z/lineVec.mag,lineVec.wgt)

    #Get a vector from a point on the line and a point on the plane.
    lppVec = far.subtract(plane)

    #Calculate the numerator and denominator individually so we can
    #compare if the line lies in the plane or not
    num = lppVec.dot(normal)
    denom = nline.dot(normal)

    if (math.fabs(num) < epsilon and math.fabs(denom) < epsilon):
       print "Oops.  Line is in the plane."
       return sp.SpacePoint(-99.0,-99.0,-99.0,0.0) #zero weight and really out there

    if (math.fabs(denom) < epsilon):
       print "Oops.  Line is parallel to the plane."
       return sp.SpacePoint(-99.0,-99.0,-99.0,0.0) #zero weight and really out there

    #Get the distance from P0 to the point on the plane
    dist = math.fabs(num/denom)

    result = nline.scale(dist)

    return result.add(far)   
