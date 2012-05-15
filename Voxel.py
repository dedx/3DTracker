###########################################
#
# Class defining a NIFFTE Voxel
#
# J.L. Klay
# 14-May-2012
#
###########################################

class Voxel(object):
      """represents a point in NIFFTE detector using index space """
      
      def __init__(self,volume=0,row=0,column=0,bucket=0,adc=0):
      	  self.volume = volume
	  self.row = row
	  self.column = column
	  self.bucket = bucket
	  self.adc = adc

      def __str__(self):
      	  return '(%d, %d, %d, %d, %d)' % (self.volume, self.row, self.column, self.bucket, self.adc)
