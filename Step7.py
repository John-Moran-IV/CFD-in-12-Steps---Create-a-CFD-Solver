import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

nx = 31  # Set grid number in the x-dir.
ny = 31  # Set grid number in the y-dir.
nt = 17  # Set the number of time steps.
nu = 0.05  # Set the kinematic viscosity.
dx = 2 / (nx - 1)  # Set the spacial distance between x-dir grid points.
dy = 2 / (ny - 1)  # Set the spacial distance between y-dir grid points.
sigma = 0.25  # Set the Courant/CFL number.
dt = sigma * dx * dy / nu  # The time step duration is a function of the
# Courant number, spacial distance in x and y directions, and the viscosity.

x = numpy.linspace(0, 2, nx)  # Create 'nx' x-dir grid points, from 0 to 2.
y = numpy.linspace(0, 2, ny)  # Create 'ny' y-dir grid points, from 0 to 2.

u = numpy.ones((ny, nx))  # Create a grid matrix with dimensions ny x nx.
un = numpy.ones((ny, nx))  # Create a grid matrix with dimensions ny x nx.

# Assign initial conditions:
# Set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2.
u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2

fig = pyplot.figure()  # Set plot size and resolution.
ax = fig.gca(projection='3d')  # Project the surface in 3D.
X, Y = numpy.meshgrid(x, y)  # Takes values of x and y then makes X, Y pairs.

# Create a 3D surface using X and Y coord pairs, Z axis uses u matrix values.
surf = ax.plot_surface(X, Y, u, rstride=1, cstride=1, cmap=cm.viridis,
        linewidth=0, antialiased=False)

ax.set_xlim(0, 2)  # Set the x-dir axis limits of 0 to 2.
ax.set_ylim(0, 2)  # Set the y-dir axis limits of 0 to 2.
ax.set_zlim(1, 2.5)  # Set the z-dir axis limits of 1 to 2.5.

ax.set_xlabel('$x$')  # Set the x-dir axis label as 'x'.
ax.set_ylabel('$y$')  # Set the y-dir axis label as 'y'.


# User defined diffusion function.
def diffuse(nt):
    # Setting IC/BC's.
    u[int(.5 / dy):int(1 / dy + 1), int(.5 / dx):int(1 / dx + 1)] = 2

    # Step through time loop to solve for diffusion.
    for n in range(nt + 1):
        un = u.copy()  # Make duplicates of the u initial values.
        u[1:-1, 1:-1] = (un[1:-1, 1:-1] +
                         nu * dt / dx ** 2 *
                         (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                         nu * dt / dy ** 2 *
                         (un[2:, 1: -1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1]))

        # Making the edges of the diffusion matrix all 1's.
        u[0, :] = 1
        u[-1, :] = 1
        u[:, 0] = 1
        u[:, -1] = 1

    fig = pyplot.figure()  # Set plot size and resolution.
    ax = fig.gca(projection='3d')  # Project the object in 3D.

    # Create a 3D surface using X and Y coord pairs, Z axis uses UPDATED u values.
    surf = ax.plot_surface(X, Y, u[:], rstride=1, cstride=1, cmap=cm.viridis,
                           linewidth=0, antialiased=True)
    ax.set_zlim(1, 2.5)  # Set the z-dir axis limits of 1 to 2.5.
    ax.set_xlabel('$x$')  # Set the x-dir axis label as 'x'.
    ax.set_ylabel('$y$')  # Set the y-dir axis label as 'y'.


pyplot.show()  # Display the plot of the hat function.

# The number plugged into the diffuse function below represents the amount
# of time that passes before the snapshot/current state of the fluid is shown.
diffuse(50)
pyplot.show()  # Display the fluid state/3D surface plot of the diffusion.
