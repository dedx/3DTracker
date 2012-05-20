##############################################
#
# 3D Least Squares Fit
#
#
#Given a set of data, (x_k, y_k, z_k) for k = 1,...,n
#The following set of equations will determine the parameters that
#describe the straight line through them, parameterized using the
#intersection point of the line with a plane that is perpendicular to
#the line and containing the origin:
#
#    z = ax+by (Plane)
#    w = au+bv (intersection point, H(u,v,w) of line and plane)
#
#   From: 
#
#   REGRESSIONS et TRAJECTOIRES en 3D.
#   By Jean Jacquelin
#   http://www.scribd.com/doc/31477970/Regressions-et-trajectoires-3D    
#
#
##############################################
from operator import attrgetter
import numpy as np
import math

import SpacePoint as sp
import TrackFit as tf
import LineUtils as lin

def LSQ3D(points,weighted=False):
    """Given a set of space points, find the 3D least squares minimized
    best fit line"""

    #Transform to numpy arrays for fast calculations
    x = np.zeros(len(points),float)
    y = np.zeros(len(points),float)
    z = np.zeros(len(points),float)
    wgt = np.zeros(len(points),float)
    i = 0
    for point in points:
    	x[i] = point.x
    	y[i] = point.y
    	z[i] = point.z
    	wgt[i] = point.wgt
    	i += 1

    # find the data point that is furthest from the point furthest
    # from the origin.  We do it this way because tracks can cross the axes
    start = points[0]
    dist = 0.0
    for pt in points:
    	if (pt.distance(start) > dist):
       	   dist = pt.distance(start)
       	   end = pt

    # Calculate the mean value of each cartesian coordinate, which will
    # be one point on the best fit line
    Xm = sum(x)/len(x)
    Ym = sum(y)/len(y)
    Zm = sum(z)/len(z)

    if (weighted):
       Xm = sum(x*wgt)/sum(wgt)
       Ym = sum(y*wgt)/sum(wgt)
       Zm = sum(z*wgt)/sum(wgt)

    #Calculate the correlation factors
    Sxx = -Xm**2 + sum(x*x)/len(x)
    Sxy = -Xm*Ym + sum(x*y)/len(x)
    Syy = -Ym**2 + sum(y*y)/len(y)
    Sxz = -Xm*Zm + sum(x*z)/len(x)
    Szz = -Zm**2 + sum(z*z)/len(z)
    Syz = -Ym*Zm + sum(y*z)/len(y)

    if (weighted):
       Sxx = -Xm**2 + sum(x*x*wgt)/sum(wgt)
       Sxy = -Xm*Ym + sum(x*y*wgt)/sum(wgt)
       Syy = -Ym**2 + sum(y*y*wgt)/sum(wgt)
       Sxz = -Xm*Zm + sum(x*z*wgt)/sum(wgt)
       Szz = -Zm**2 + sum(z*z*wgt)/sum(wgt)
       Syz = -Ym*Zm + sum(y*z*wgt)/sum(wgt)

    #Angle
    theta = 0.5*np.arctan(2.0*Sxy/(Sxx-Syy))
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    cos2theta = costheta**2
    sin2theta = sintheta**2

    #More correlation factors
    K11 = (Syy+Szz)*cos2theta+(Sxx+Szz)*sin2theta-2.0*Sxy*costheta*sintheta
    K22 = (Syy+Szz)*sin2theta+(Sxx+Szz)*cos2theta+2.0*Sxy*costheta*sintheta
    K12 = -Sxy*(cos2theta-sin2theta)+(Sxx-Syy)*costheta*sintheta
    K10 = Sxz*costheta+Syz*sintheta
    K01 = -Sxz*sintheta+Syz*costheta
    K00 = Sxx+Syy

    #Simplify
    c2 = -K00-K11-K22
    c1 = K00*K11+K00*K22+K11*K22-K01**2-K10**2
    c0 = K01**2*K11+K10**2*K22-K00*K11*K22

    p = c1-(1./3.)*c2**2
    q = (2./27.)*c2**3-(1./3.)*c1*c2+c0
    R = (1./4.)*q**2+(1./27.)*p**3

    dm2 = 0.0
    if R > 0:
       dm2 = (-1./3.)*c2+((-1./2.)*q+np.sqrt(R))**(1./3.)+((-1./2.)*q-np.sqrt(R))**(1./3.)
    else:
	rho = np.sqrt((-1./27.)*p**3)
	phi = np.arccos(-q/(2.0*rho))
	aa = (-1./3.)*c2 + 2.0*rho**(1./3.)*np.cos((1./3.)*phi)
	bb = (-1./3.)*c2 + 2.0*rho**(1./3.)*np.cos((1./3.)*(phi+2.0*np.pi))
	cc = (-1./3.)*c2 + 2.0*rho**(1./3.)*np.cos((1./3.)*(phi+4.0*np.pi))
   	val = [aa,bb,cc]
   	dm2 = min(val)

    #Now, finally, the line parameters
    a = (-K10/(K11-dm2))*costheta + (K01/(K22-dm2))*sintheta
    b = (-K10/(K11-dm2))*sintheta + (-K01/(K22-dm2))*costheta

    u = (1./(1.+a**2+b**2))*((1.+b**2)*Xm-a*b*Ym+a*Zm)
    v = (1./(1.+a**2+b**2))*(-a*b*Xm+(1.+a**2)*Ym+b*Zm)
    w = (1./(1.+a**2+b**2))*(a*Xm+b*Ym+(a**2+b**2)*Zm)

    #Result is two points on the line:
    lsqend = sp.SpacePoint(u,v,w)
    lsqstart = sp.SpacePoint(Xm,Ym,Zm)

    #Now find the points on this line closest to the start and end
    #data points, by projecting the line to the planes through those
    #points
    znormal = sp.SpacePoint(0.,0.,-1.)
    if (end.z < 0.):
       znormal.z = -1.0
    linestart = lin.ProjectedLinePointInPlane(start,lsqend,end,znormal)

    znormal.z = 1.0
    if (start.z < 0.):
       znormal.z = -1.0
    lineend = lin.ProjectedLinePointInPlane(linestart,lsqstart,start,znormal)

    #Create a trackfit object from these two points and return it to
    #the calling program
    result = tf.TrackFit(linestart,lineend)

    return result





if __name__ == '__main__':
   #example data
   x = np.array([33.44, 28.58, 30.74, 32.35, 17.09, 15.63, 27.48, 19.6, 27.4, 17.44])
   y = np.array([12.63, 10.23, 11.37, 12.09, 4.55, 3.88, 9.79, 5.75, 9.65, 4.74])
   z = np.array([0.314, 2.729, 1.618, 0.82, 8.409, 9.173, 3.279, 7.18, 3.295, 8.257])

   testpts = []
   for i in range(len(x)):
       testpts.append(sp.SpacePoint(x[i],y[i],z[i]))

   test = LSQ3D(testpts,weighted=True)

#   print "Xm = 24.975 = ",Xm
#   print "Ym = 8.468 = ",Ym
#   print "Zm = 4.5074 =",Zm

#   print "Sxx = 41.9603 = ",Sxx
#   print "Sxy = ??? = ",Sxy
#   print "Syy = 10.2798 = ",Syy
#   print "Sxz = ??? = ",Sxz
#   print "Szz = 10.3864 = ",Szz
#   print "Syz = ??? = ",Syz

#   print "Theta = 0.459591 = ",theta

#   print "K11 = 10.3877 = ",K11
#   print "K22 = 62.6252 = ",K22
#   print "K12 = ??? = ",K12
#   print "K10 = -23.2928 = ",K10
#   print "K01 = 0.0004035 = ",K01
#   print "K00 = 52.2401 = ",K00

#   print "c2 = -125.25307 = ",c2
#   print "c1 = 3922.1842 = ",c1
#   print "c0 = -6.348499 = ",c0

#   print "p = -1307.2596 = ",p
#   print "q = 18192.1842 = ",q
#   print "R = -0.22724546 = ",R

#   print "rho = 9096.2182 = ",rho
#   print "phi = 3.1415402 = ",phi
#   print "aa = 62.6264 = ",aa
#   print "bb = 0.00161869 = ",bb
#   print "cc = 62.6251 = ",cc
#   print "dm2 = 0.00161869 = ",dm2

#   print "a = 2.009691 = ",a
#   print "b = 0.994669 = ",b
#   print "u = 6.93663 = ",u
#   print "v = -0.459842 = ",v
#   print "w = 13.4831 = ",w

   print test
