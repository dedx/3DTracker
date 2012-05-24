import numpy as np
import NiffteGeo as ngeo
from operator import attrgetter
 
#class Gradient(object):
#      """An object to store the twenty numbers corresponding to the
#      edge gradients of hexagonal voxels."""
#      
#      def __init__(self,array=np.zeros(20,float))
#      	  self.array = array

def CloseEnough(this,that):
    if (that.row < this.row-1 or that.row > this.row+1): return False
    if (that.column < this.column-1 or that.column > this.column+1): return False
    if (that.bucket < this.bucket+1 or that.bucket > this.bucket+1): return False
    return True
    
def Neighbor(currentVoxel,partner):
    """return true if the partner voxel is the neighbor voxel we
    want"""


def ComputeGradient(currvox,availVox):
    """Compute gradient between current voxel and its neighbors within
    the available voxel list.  If a voxel doesn't exist in availVox,
    give gradient a special value?
    Only voxels within a single volume are passed, so no need to
    search,sort on volume
    """
    localVox = []
    localVox[:] = availVox[:]
    row = currvox.row
    col = currvox.column
    bkt = currvox.bucket
    adc = currvox.adc

    #Gradient array initialized to zeros
    grad = np.zeros(20,float)
    
    #First treat edges, if necessary
    if (row == 0):
       grad[0:5] = adc
    if (col == 0):
       grad[6:8] = adc
    if (bkt == 0):
       grad[0:19:3] = adc
    if (row == ngeo.maxRow):
       grad[14:19] = adc
    if (col == ngeo.maxCol):
       grad[3:5] = adc
       grad[11:13] = adc
       grad[17:19] = adc
    if (bkt == ngeo.maxBkt):
       grad[0:19:3] = adc
    
#    #sort availVox by row,col,bkt
#    sorted(availVox,key=attrgetter('row','column','bucket'))

    localVox[:] = [vox for vox in localVox if CloseEnough(currvox,vox)]

    rindex = row-1
    cindex = col-1
    bindex = bkt-1
    count = 0
    for rindex in range(row-1,row+2):
    	for cindex in range(col-1,col+2):
    	    for bindex in range(bkt-1,bkt+2):
	    	#Skip hex corners
	        if cindex == col-1 and rindex != row: continue 
		#Don't do self-correlation
		if cindex == col and rindex == row and bindex == bkt: continue 
		index = next((i for i in xrange(len(localVox)) if (localVox[i].row == rindex and localVox[i].column == cindex and localVox[i].bucket == bindex)), None)
		if index is not None:
		   grad[count] = currvox.adc-localVox[index].adc
#      	    	   print localVox[index], count, grad[count]
		   del localVox[index]
		count += 1
	      	bindex += 1
	    cindex += 1
	rindex += 1
    return grad
