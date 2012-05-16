from numpy import *

x = arange(0,5.4)
m,b = 0.8,-0.62
y_true = m*x+b
y_meas = y_true + 0.2*random.randn(len(x))

def residuals(p,y,x):
    m,b = p
    err = y-m*x+b
    return err

def peval(x, p):
    return p[0]*x+p[1]

p0 = [0.5,-0.1]
print "Initial guess: ",array(p0)

from scipy.optimize import leastsq
plsq = leastsq(residuals, p0, args=(y_meas, x))
print "Found: ",plsq[0]
print "Truth: ", array([m,b])

import matplotlib.pyplot as plt
plt.plot(x,peval(x,plsq[0]),x,y_meas,'o',x,y_true)
plt.title('Least squares fit to straight line data')
plt.legend(['Fit','Data','True'])
plt.show()
print y_meas
