import numpy
from matplotlib import pyplot as plt


nx = 41  # Set number of grid points in x-dir
dx = 2 / (nx - 1)  # Set spacial separation between grid points
nt = 20  # Number of time steps
dt = .025  # Time step duration
u = numpy.ones(nx)  # Create an array of 1's of length nx
u[int(.5 / dx): int(1 / dx + 1)] = 2  # Set IC's and BC's

un = numpy.ones(nx)  # Initialize placeholder 1's for time-step solution

# Iterative loop to solve the PDE
for n in range(nt):
    un = u.copy()  # Copy 'u' values and store in un
    for i in range(1, nx):
        # Taylor expansion form of PDE rearranged to solve for u(x,t)
        u[i] = un[i] - un[i] * dt / dx * (un[i] - un[i-1])

# Plot the solution in the x-dir with equally spaced grid points vs 'u'.
plt.plot(numpy.linspace(0, 2, nx), u)
plt.show()
