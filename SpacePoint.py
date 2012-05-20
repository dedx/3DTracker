###########################################
#
# Class defining a SpacePoint
#
# J.L. Klay
# 14-May-2012
#
###########################################
import math

class SpacePoint(object):
      """represents a point in 3-D space in cartesian coordinates in centimeters"""
      
      def __init__(self,x=0.0,y=0.0,z=0.0,wgt=1.0):
      	  self.x = x
	  self.y = y
	  self.z = z	
	  self.wgt = wgt	
	  self.mag = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

      def __str__(self):
      	  return '(%.2f, %.2f, %.2f, %.2f) \t%.2f' % (self.x, self.y, self.z, self.wgt, self.mag)

      def distance(self,other):
      	  return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2+(self.z-other.z)**2)

      def dot(self,other):
      	  return self.x*other.x+self.y*other.y+self.z*other.z

      def subtract(self,other):
      	  res = SpacePoint(self.x-other.x,self.y-other.y,self.z-other.z,self.wgt)
      	  return res

      def add(self,other):
      	  res = SpacePoint(self.x+other.x,self.y+other.y,self.z+other.z,self.wgt)
      	  return res

      def scale(self,val):
      	  res = SpacePoint(self.x*val,self.y*val,self.z*val,self.wgt)
      	  return res
