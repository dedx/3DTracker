###########################################
#
# Class defining a TrackFit object
#
# J.L. Klay
# 19-May-2012
#
###########################################
import math
import SpacePoint as sp

class TrackFit(object):
      """Given the start and end point of a line, return various
      useful informations on that line"""

      def __init__(self,start=sp.SpacePoint(),end=sp.SpacePoint()):
      	  self.start = start
	  self.end = end
	  self.length = (self.start).distance(self.end)
	  self.dir = ((self.end).subtract(self.start)).scale(1./self.length)

      def __str__(self):
      	  foo1 = 'Start: %.2f,%.2f,%.2f,\n' % (self.start.x,self.start.y,self.start.z)
	  foo2 = 'End: %.2f,%.2f,%.2f\n' % (self.end.x,self.end.y,self.end.z)
	  foo3 = 'Length: %.2f\n' % (self.length)
	  foo4 = 'Direction: %.2f,%.2f,%.2f\n' % (self.dir.x,self.dir.y,self.dir.z)
	  return foo1+foo2+foo3+foo4
