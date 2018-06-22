import numpy
from matplotlib import pyplot

nx = 100  # Number of grid points in x-dir
dx = 2 / (nx - 1)  # Spacing between grid points in x-dir
nt = 20  # Number of time steps to go through
nu = 0.3  # kinematic viscosity constant
sigma = 0.2  # Courant (CFL) number applied to enforce solver stability
dt = sigma * dx**2 / nu  # Time step duration set as a function of the
# Courant (CFL) number, the spacial separation between grid points squared,
# and the kinematic viscosity of the fluid.

u = numpy.ones(nx)  # Initialize 'u' as an array of 1's
u[int(0.5 / dx):int(1 / dx + 1)] = 2  # Apply IC's and BC's

un = numpy.ones(nx)  # Initialize 'un' as an array of 1's

# Iteratively solve the PDE
for n in range(nt):
    un = u.copy()
    for i in range(1, nx - 1):
        # Taylor expansion form of PDE rearranged to solve for u(x,t,nu)
        u[i] = un[i] + nu * dt / dx**2 * (un[i+1] - 2 * un[i] + un[i-1])

# Plot the solution in the x-dir with equally spaced grid points vs 'u'.
pyplot.plot(numpy.linspace(0, 2, nx), u)
pyplot.show()
