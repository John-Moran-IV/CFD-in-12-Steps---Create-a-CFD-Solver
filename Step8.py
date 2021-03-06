import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

nx = 41  # Set grid number in the x-dir.
ny = 41  # Set grid number in the y-dir.
nt = 120  # Set the number of time steps.
c = 1  # Set the wave speed.
dx = 2 / (nx - 1)  # Set the spacial distance between x-dir grid points.
dy = 2 / (ny - 1)  # Set the spacial distance between y-dir grid points.
sigma = .0009  # Set the Courant/CFL number.
nu = 0.01  # Set the kinematic viscosity.
dt = sigma * dx * dy / nu  # The time step duration is a function of the
# Courant number, spacial distance in x and y directions, and the viscosity.

x = numpy.linspace(0, 2, nx)  # Create 'nx' x-dir grid points, from 0 to 2.
y = numpy.linspace(0, 2, ny)  # Create 'ny' y-dir grid points, from 0 to 2.

u = numpy.ones((ny, nx))  # Create a grid matrix with dimensions ny x nx.
v = numpy.ones((ny, nx))  # Create a grid matrix with dimensions ny x nx.
un = numpy.ones((ny, nx))  # Creating place holder matrix for u.
vn = numpy.ones((ny, nx))  # Creating place holder matrix for v.

# Assign initial conditions:
# Set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2.
u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2
# Set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2.
v[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2
# Done assigning initial conditions.

# Setting plot parameters for the IC/BC visual representation.
fig = pyplot.figure(figsize=(11, 7), dpi=100)  # Set plot size and resolution.
ax = fig.gca(projection='3d')  # Project the surface in 3D.
X, Y = numpy.meshgrid(x, y)  # Takes values of x and y then makes X, Y pairs.
# in a rectangular grid of dimension x by y.

# Plots a surface in 3D, where the Z axis' are the copied u and v matrix values.
ax.plot_surface(X, Y, u[:], cmap=cm.viridis, rstride=1, cstride=1)
ax.plot_surface(X, Y, v[:], cmap=cm.viridis, rstride=1, cstride=1)

ax.set_xlabel('$x$')  # Set the x-dir axis label as 'x'.
ax.set_ylabel('$y$')  # Set the y-dir axis label as 'y'.
pyplot.show()  # Display the plot of the hat function.

for n in range(nt + 1):  # Go through the time steps from 1 to 'nt'.
    un = u.copy()  # Make duplicates of the u and v initial values.
    vn = v.copy()  # These duplicates will be operated on to preserve u and v.

    # Solved 2D Burgers' equation for the convection component of the fluid.
    u[1:-1, 1:-1] = (un[1:-1, 1:-1] -
                     dt / dx * un[1:-1, 1:-1] *
                     (un[1:-1, 1:-1] - un[1:-1, 0:-2]) -
                     dt / dy * vn[1:-1, 1:-1] *
                     (un[1:-1, 1:-1] - un[0:-2, 1:-1]) +
                     nu * dt / dx ** 2 *
                     (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                     nu * dt / dy ** 2 *
                     (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1]))

    # Solved 2D Burgers' equation for the diffusion component of the fluid.
    v[1:-1, 1:-1] = (vn[1:-1, 1:-1] -
                     dt / dx * un[1:-1, 1:-1] *
                     (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) -
                     dt / dy * vn[1:-1, 1:-1] *
                     (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) +
                     nu * dt / dx ** 2 *
                     (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) +
                     nu * dt / dy ** 2 *
                     (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1]))

    # Making the edges of the convection matrix all 1's.
    u[0, :] = 1
    u[-1, :] = 1
    u[:, 0] = 1
    u[:, -1] = 1

    # Making the edges of the diffusion matrix all 1's.
    v[0, :] = 1
    v[-1, :] = 1
    v[:, 0] = 1
    v[:, -1] = 1

fig = pyplot.figure(figsize=(11, 7), dpi=100)  # Set plot size and resolution.
ax = fig.gca(projection='3d')  # Project the object in 3D.
X, Y = numpy.meshgrid(x, y)  # Takes values of x and y then makes X, Y pairs.
# Plots a surface in 3D, where the Z axis' are the UPDATED 'u' and 'v' values.
ax.plot_surface(X, Y, u, cmap=cm.viridis, rstride=1, cstride=1)
ax.plot_surface(X, Y, v, cmap=cm.viridis, rstride=1, cstride=1)
ax.set_xlabel('$x$')  # Set the x-dir axis label as 'x'.
ax.set_ylabel('$y$')  # Set the y-dir axis label as 'y'.
pyplot.show()  # Display the plot of the hat function.
