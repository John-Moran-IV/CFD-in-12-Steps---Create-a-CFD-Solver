import numpy
from matplotlib import pyplot

# 1-D Linear Convection

nx = 40  # grid count
dx = 2 / (nx-1)  # linear spacing, finer with higher nx
nt = 25  # number of time steps to calculate
dt = 0.025  # value of each time step
c = 1  # wave speed

u = numpy.ones(nx)  # Create array of nx number of 1's
u[int(0.5/dx):int(1/dx + 1)] = 2  # Setting IC's and BC's
print(u)  # Shows how the IC/BC's have changed the u array

# Plot the grid vs. the convection conditions at each point
pyplot.plot(numpy.linspace(0, 2, nx), u)

# Step through the 'u' array
for n in range(nt):
    un = u.copy()  # Copy and hold u as un
    # for i in range(1,nx):
    for i in range(nx):
        u[i] = un[i] - c * dt/dx * (un[i] - un[i-1])

# Plotting the convection along the x-dir
pyplot.plot(numpy.linspace(0, 2, nx), u)
pyplot.show()
