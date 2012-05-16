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
import numpy as np

#example data
#x = np.array([33.44, 28.58, 30.74, 32.35, 17.09, 15.63, 27.48, 19.6, 27.4, 17.44])
#y = np.array([12.63, 10.23, 11.37, 12.09, 4.55, 3.88, 9.79, 5.75, 9.65, 4.74])
#z = np.array([0.314, 2.729, 1.618, 0.82, 8.409, 9.173, 3.279, 7.18, 3.295, 8.257])

import Utilities as util
import SpacePoint as sp
import NiffteGeo as ngeo
import Voxel as vox

points = []
fin = open('Niffte-event.dat')
for line in fin:
    data = (line.strip()).split()
    volume = int(data[0])
    row = int(data[1])
    column = int(data[2])
    bucket = int(data[3])
    adc = int(data[4])
    voxel = vox.Voxel(volume,row,column,bucket,adc)
    points.append(ngeo.MapVoxeltoXYZ(voxel))

x = np.zeros(len(points),float)
y = np.zeros(len(points),float)
z = np.zeros(len(points),float)
i = 0
for point in points:
    x[i] = point.x
    y[i] = point.y
    z[i] = point.z
    i += 1

print "Finding best fit line..."

Xm = sum(x)/len(x)
#print "Xm = 24.975 = ",Xm
Ym = sum(y)/len(y)
#print "Ym = 8.468 = ",Ym
Zm = sum(z)/len(z)
#print "Zm = 4.5074 =",Zm

Sxx = -Xm**2 + sum(x*x)/len(x)
#print "Sxx = 41.9603 = ",Sxx
Sxy = -Xm*Ym + sum(x*y)/len(x)
#print "Sxy = ??? = ",Sxy
Syy = -Ym**2 + sum(y*y)/len(y)
#print "Syy = 10.2798 = ",Syy
Sxz = -Xm*Zm + sum(x*z)/len(x)
#print "Sxz = ??? = ",Sxz
Szz = -Zm**2 + sum(z*z)/len(z)
#print "Szz = 10.3864 = ",Szz
Syz = -Ym*Zm + sum(y*z)/len(y)
#print "Syz = ??? = ",Syz

theta = 0.5*np.arctan(2.0*Sxy/(Sxx-Syy))
#print "Theta = 0.459591 = ",theta

cos2theta = np.cos(theta)**2
sin2theta = np.sin(theta)**2

K11 = (Syy+Szz)*cos2theta+(Sxx+Szz)*sin2theta-2.0*Sxy*np.cos(theta)*np.sin(theta)
#print "K11 = 10.3877 = ",K11
K22 = (Syy+Szz)*sin2theta+(Sxx+Szz)*cos2theta+2.0*Sxy*np.cos(theta)*np.sin(theta)
#print "K22 = 62.6252 = ",K22
K12 = -Sxy*(cos2theta-sin2theta)+(Sxx-Syy)*np.cos(theta)*np.sin(theta)
#print "K12 = ??? = ",K12
K10 = Sxz*np.cos(theta)+Syz*np.sin(theta)
#print "K10 = -23.2928 = ",K10
K01 = -Sxz*np.sin(theta)+Syz*np.cos(theta)
#print "K01 = 0.0004035 = ",K01
K00 = Sxx+Syy
#print "K00 = 52.2401 = ",K00

c2 = -K00-K11-K22
#print "c2 = -125.25307 = ",c2
c1 = K00*K11+K00*K22+K11*K22-K01**2-K10**2
#print "c1 = 3922.1842 = ",c1
c0 = K01**2*K11+K10**2*K22-K00*K11*K22
#print "c0 = -6.348499 = ",c0

p = c1-(1./3.)*c2**2
#print "p = -1307.2596 = ",p
q = (2./27.)*c2**3-(1./3.)*c1*c2+c0
#print "q = 18192.1842 = ",q
R = (1./4.)*q**2+(1./27.)*p**3
#print "R = -0.22724546 = ",R

dm2 = 0.0
if R > 0:
   dm2 = (-1./3.)*c2+((-1./2.)*q+np.sqrt(R))**(1./3.)+((-1./2.)*q-np.sqrt(R))**(1./3.)
else:
   rho = np.sqrt((-1./27.)*p**3)
#   print "rho = 9096.2182 = ",rho
   phi = np.arccos(-q/(2.0*rho))
#   print "phi = 3.1415402 = ",phi
   aa = (-1./3.)*c2 + 2.0*rho**(1./3.)*np.cos((1./3.)*phi)
#   print "aa = 62.6264 = ",aa
   bb = (-1./3.)*c2 + 2.0*rho**(1./3.)*np.cos((1./3.)*(phi+2.0*np.pi))
#   print "bb = 0.00161869 = ",bb
   cc = (-1./3.)*c2 + 2.0*rho**(1./3.)*np.cos((1./3.)*(phi+4.0*np.pi))
#   print "cc = 62.6251 = ",cc
   val = [aa,bb,cc]
   dm2 = min(val)

#print "dm2 = 0.00161869 = ",dm2

a = (-K10/(K11-dm2))*np.cos(theta) + (K01/(K22-dm2))*np.sin(theta)
#print "a = 2.009691 = ",a
b = (-K10/(K11-dm2))*np.sin(theta) + (-K01/(K22-dm2))*np.cos(theta)
#print "b = 0.994669 = ",b

u = (1./(1.+a**2+b**2))*((1.+b**2)*Xm-a*b*Ym+a*Zm)
#print "u = 6.93663 = ",u
v = (1./(1.+a**2+b**2))*(-a*b*Xm+(1.+a**2)*Ym+b*Zm)
#print "v = -0.459842 = ",v
w = (1./(1.+a**2+b**2))*(a*Xm+b*Ym+(a**2+b**2)*Zm)
#print "w = 13.4831 = ",w

print "Two points on the best fit line: \n",Xm,Ym,Zm,"\n",u,v,w

# 3D line is S+lu, where S is the start point (x0,y0,z0), l is the
# length of the line, and u is the direction vector (ux,uy,uz)

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
for pt in points:
    ax.scatter(pt.x,pt.y,pt.z,color='r',marker='*')

ax.set_xlim3d(-10.,10.)
ax.set_ylim3d(-10.,10.)
ax.set_zlim3d(-10.,10.)

plt.show()

