###########################################
#
# Class defining a SpacePoint
#
# J.L. Klay
# 14-May-2012
#
###########################################

class SpacePoint(object):
      """represents a point in 3-D space in cartesian coordinates in centimeters"""
      
      def __init__(self,x=0.0,y=0.0,z=0.0):
      	  self.x = x
	  self.y = y
	  self.z = z	
	
      def __str__(self):
      	  return '(%.2f, %.2f, %.2f)' % (self.x, self.y, self.z)
