import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

# Creating a function which sets up 2-D plots expressed as 3-D surfaces.
def plot2D(x, y, p):
    fig = pyplot.figure(figsize=(11, 7), dpi=100)  # Setting size and resolution.
    ax = fig.gca(projection='3d')  # Project the surface in 3-D space.
    X, Y = numpy.meshgrid(x, y)  # Makes an evenly spaced grid of points.
    # Defining the surface inputs and graphical options.
    surf = ax.plot_surface(X, Y, p[:], rstride=1, cstride=1, cmap=cm.viridis,
            linewidth=0, antialiased=False)
    ax.set_xlim(0, 2)  # Setting axis limits for x-dir.
    ax.set_ylim(0, 1)  # Setting axis limits for y-dir.
    ax.view_init(30, 225)  # Setting viewing angle at 30 deg, azimuth angle at 225 deg.
    ax.set_xlabel('$x$')  # Setting labels for the x-axis and y-axis
    ax.set_ylabel('$y$')


# Create a function that takes a matrix, 'p', the 'y' array, the x and y spacing, and
# a target error value as the input arguments.
def laplace2d(p, y, dx, dy, l1norm_target):
    l1norm = 1  # Initial error value of 1, or 100% difference.
    pn = numpy.empty_like(p)  # Creates an uninitialized array that has the same size
    # and type to that of the 'p' array.

    # While the error is larger than the target error, keep looping.
    while l1norm > l1norm_target:
        pn = p.copy()  # Stores the last 'p' matrix in 'pn' as a place holder.
        p[1:-1, 1:-1] = ((dy ** 2 * (pn[1:-1, 2:] + pn[1:-1, 0:-2]) +
                          dx ** 2 * (pn[2:, 1:-1] + pn[0:-2, 1:-1])) /
                         (2 * (dx ** 2 + dy ** 2)))
        # BC's
        p[:, 0] = 0  # p = 0 @ x = 0
        p[:, -1] = y  # p = y @ x = 2
        p[0, :] = p[1, :]  # dp/dy = 0 @ y = 0
        p[-1, :] = p[-2, :]  # dp/dy = 0 @ y = 1

        # Check the values of 'p' against the values of 'pn' to check for error and
        # confirm that the solution is converging.
        l1norm = (numpy.sum(numpy.abs(p[:]) - numpy.abs(pn[:])) /
                  numpy.sum(numpy.abs(pn[:])))

    return p  # Returns the first 'p' matrix solution that meets the error criteria.


nx = 31  # Number of x-dir grid points.
ny = 31  # Number of y-dir grid points.
c = 1  # Wave speed constant.
dx = 2 / (nx - 1)  # Grid spacing in the x-dir.
dy = 2 / (ny - 1)  # Grid spacing in the y-dir.

# Set initial conditions of 0's in a matrix of dimensions nx by ny.
p = numpy.zeros((ny, nx))

# Create evenly spaced x and y position points to help with plotting.
x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 1, ny)

# Set boundary conditions at the edges of the plot.
p[:, 0] = 0  # p = 0 @ x = 0
p[:, -1] = y  # p = y @ x = 2
p[0, :] = p[1, :]  # dp/dy = 0 @ y = 0
p[-1, :] = p[-2, :]  # dp/dy = 0 @ y = 1

p = laplace2d(p, y, dx, dy, 1e-4)  # Solves the system using the laplace function then
# stores the solutions in the 'p' matrix. The last input is the max allowable difference
# between the values (the error).

plot2D(x, y, p)  # Create the 2-D plot.
pyplot.show()  # Display the 2-D plot as a 3-D surface.
