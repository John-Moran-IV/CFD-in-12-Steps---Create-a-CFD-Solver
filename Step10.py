import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

# Parameters:
nx = 50  # Number of x-dir grid points.
ny = 50  # Number of y-dir grid points.
nt = 100  # Number of time steps.
xmin = 0  # Minimum x value.
xmax = 2  # Maximum x value.
ymin = 0  # Minimum y value.
ymax = 1  # Maximum y value.

dx = (xmax - xmin) / (nx - 1)  # Grid spacing in the x-dir.
dy = (ymax - ymin) / (ny - 1)  # Grid spacing in the y-dir.

# Initialization:
p = numpy.zeros((ny, nx))  # 'p' matrix, consisting of 0's with dimensions nx by ny.
pd = numpy.zeros((ny, nx))  # 'pd' matrix, consisting of 0's with dimensions nx by ny.
b = numpy.zeros((ny, nx))  # 'b' matrix, consisting of 0's with dimensions nx by ny.
x = numpy.linspace(xmin, xmax, nx)  # Creates an array going from xmin to xmax with
# the number of of values between them equal to 'nx'.
y = numpy.linspace(ymin, ymax, ny)  # Creates an array going from ymin to ymax with
# the number of of values between them equal to 'ny'.

# Source
b[int(ny / 4), int(nx / 4)] = 100
b[int(3 * ny / 4), int(3 * nx / 4)] = -100

# Solving the equation with array operations.
for it in range(nt):

    pd = p.copy()

    p[1:-1,1:-1] = (((pd[1:-1, 2:] + pd[1:-1, :-2]) * dy**2 +
                    (pd[2:, 1:-1] + pd[:-2, 1:-1]) * dx**2 -
                    b[1:-1, 1:-1] * dx**2 * dy**2) /
                    (2 * (dx**2 + dy**2)))

    p[0, :] = 0
    p[ny-1, :] = 0
    p[:, 0] = 0
    p[:, nx-1] = 0


# Creating a function which sets up 2-D plots expressed as 3-D surfaces.
def plot2d(x, y, p):
    fig = pyplot.figure(figsize=(11, 7), dpi=100)  # Setting size and resolution.
    ax = fig.gca(projection='3d')  # Project the surface in 3-D space.
    X, Y = numpy.meshgrid(x, y)  # Makes an evenly spaced grid of points.
    # Defining the surface inputs and graphical options.
    surf = ax.plot_surface(X, Y, p[:], rstride=1, cstride=1, cmap=cm.viridis,
            linewidth=0, antialiased=False)
    ax.view_init(30, 225)  # Setting viewing angle at 30 deg, azimuth angle at 225 deg.
    ax.set_xlabel('$x$')  # Setting labels for the x-axis and y-axis
    ax.set_ylabel('$y$')


plot2d(x, y, p)  # Creates the 2-D plot.
pyplot.show()  # Displays the 2-D plot as a 3-D surface.
