from scipy.integrate import odeint


def r1(w, t):
    # Automatically generated function

    # The state vector
    (x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12)=w 

    # Now the common terms
    t0=k2*(-L2 - x1 + x3)
    t1=-b1*x3 - k1*(-L1 + x1) + t0
    t2=-b2*x4 - t0

    # The ODE system
    dot_x=[x2,
    t1/m1,
    x4,
    t2/m2,
    0,
    -t1/m1**2,
    0,
    0,
    0,
    0,
    0,
    -t2/m2**2]
    
    return dot_x





# the numerical values for this example come from 
# http://wiki.scipy.org/Cookbook/CoupledSpringMassSystem

# Parameter values
# Masses:
m1 = 1.0
m2 = 1.5
# Spring constants
k1 = 8.0
k2 = 40.0
# Natural lengths
L1 = 0.5
L2 = 1.0
# Friction coefficients
b1 = 0.8
b2 = 0.5

# Initial conditions
# x1 and x2 are the initial displacements; y1 and y2 are the initial velocities
x1 = 0.5
x2 = 0.0
x3 = 2.25
x4 = 0.0

# ODE solver parameters
abserr = 1.0e-8
relerr = 1.0e-6
stoptime = 10.0
numpoints = 250

# Create the time samples for the output of the ODE solver.
# I use a large number of points, only because I want to make
# a plot of the solution that looks nice.
t = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]

# Pack up the parameters and initial conditions:
# p = [m1, m2, k1, k2, L1, L2, b1, b2]
w0 = [0.0]*(4+2*4-1) 
w0[0:3] = [x1, x2, x3, x4]

wsol = odeint(r1, w0, t, atol=abserr, rtol=relerr)

# now do some ploting
import matplotlib.pyplot as plt

plt.ion()
plt.figure(1)
plt.hold(True)
plt.plot(t, wsol[:,0])
plt.plot(t, wsol[:,2])



