import numpy
from matplotlib import pyplot

# Creating a function to converge on a solution
# The function input argument is the total number of grid points.


def linearconv(nx):
    dx = 2 / (nx - 1)  # The grid spacing in the x-dir depends on the total grid number.
    nt = 20  # Total number of time steps.
    c = 1  # Wave speed constant.
    sigma = 0.5  # The CFL/Courant number.

    dt = sigma * dx  # The duration of the time step depends on the CFL number and number of
    # grid points.

    u = numpy.ones(nx)  # Create an array of 1's.
    u[int(0.5/dx):int(1 / dx + 1)] = 2  # Setting initial conditions.

    un = numpy.ones(nx)  # Creating a placeholder array of 1's.

    for n in range(nt):  # Loop for the number of total time steps.
        un = u.copy()  # Copy the 'u' array into a 'un' placeholder array.
        for i in range(1, nx):  # Loop for the number of total grid points, minus 1.
            u[i] = un[i] - c * dt / dx * (un[i] - un[i-1])

    pyplot.plot(numpy.linspace(0, 2, nx), u)
    pyplot.show()  # Show the plotted solution.


linearconv(100)  # Call the function with the number of grid points in the x-dir.
