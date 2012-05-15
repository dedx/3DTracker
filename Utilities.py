##################################
#
# Utility functions for the 3DTracker project
#
# J.L. Klay
# 14-May-2012
#
##################################

def printAttributes(object):
    for attr in object.__dict__:
    	print attr, getattr(object,attr)

def findDefiningClass(obj, meth_name): 
    for ty in type(obj).mro():
    	if meth_name in ty.__dict__: 
	   return ty
