import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

nx = 41  # Number of x-dir grid points.
ny = 41  # Number of y-dir grid points.
nt = 500  # Number of time steps.
nit = 50  # Number of iterations for Poisson Pressure function to go through.
c = 1  # Wave speed constant.
dx = 2 / (nx - 1)  # Grid spacing in the x-dir.
dy = 2 / (ny - 1)  # Grid spacing in the y-dir.

# Create evenly spaced x and y position points to help with plotting.
x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 2, ny)
X, Y = numpy.meshgrid(x, y)  # Matrix of points of dimensions x by y.

rho = 1  # Fluid density.
nu = .1  # Fluid kinematic viscosity.
dt = .001  # Time step duration.

# Set initial conditions of 0's in a matrix of dimensions nx by ny.
u = numpy.zeros((ny, nx))
v = numpy.zeros((ny, nx))
p = numpy.zeros((ny, nx))
b = numpy.zeros((ny, nx))

# Build up function that acts as a way to manage the size for the PDE for
# the Poisson Pressure equation. Represents the u and v direction momentum.
def build_up_b(b, rho, dt, u, v, dx, dy):
    b[1:-1, 1:-1] = (rho * (1 / dt *
                            ((u[1:-1, 2:] - u[1:-1, 0:-2]) /
                             (2 * dx) + (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) -
                            ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx)) ** 2 -
                            2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) *
                                 (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) -
                            ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) ** 2))

    return b  # Return the momentum aspect of the equation.


# Poisson Pressure Equation, notice how there is a multiplied 'b' variable at
# the end of the equation, which is the "build up" function for momentum being
# applied to complete the PDE.
def pressure_poisson(p, dx, dy, b):
    pn = numpy.empty_like(p)
    pn = p.copy()

    for q in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy ** 2 +
                          (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx ** 2) /
                         (2 * (dx ** 2 + dy ** 2)) -
                         dx ** 2 * dy ** 2 / (2 * (dx ** 2 + dy ** 2)) *
                         b[1:-1, 1:-1])

        # Boundary conditions for the Poisson Pressure equation.
        p[:, -1] = p[:, -2]  # dp/dy = 0 at x = 2
        p[0, :] = p[1, :]  # dp/dy = 0 at y = 0
        p[:, 0] = p[:, 1]  # dp/dx = 0 at x = 0
        p[-1, :] = 0  # p = 0 at y = 2

    return p  # Returns the pressure at the various grid points.


# Combining the velocity components with the Poisson pressure for the whole flow.
def cavity_flow(nt, u, v, dt, dx, dy, p, rho, nu):
    # Creating placeholder arrays of 0's for the u and v direction positions.
    un = numpy.empty_like(u)
    vn = numpy.empty_like(v)
    # Creating placeholder matrix for the momentum from "build up" equation.
    b = numpy.zeros((ny, nx))

    for n in range(nt):
        un = u.copy()
        vn = v.copy()

        b = build_up_b(b, rho, dt, u, v, dx, dy)
        p = pressure_poisson(p, dx, dy, b)

        u[1:-1, 1:-1] = (un[1:-1, 1:-1] -
                         un[1:-1, 1:-1] * dt / dx *
                         (un[1:-1, 1:-1] - un[1:-1, 0:-2]) -
                         vn[1:-1, 1:-1] * dt / dy *
                         (un[1:-1, 1:-1] - un[0:-2, 1:-1]) -
                         dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, 0:-2]) +
                         nu * (dt / dx ** 2 *
                               (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                               dt / dy ** 2 *
                               (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])))

        v[1:-1, 1:-1] = (vn[1:-1, 1:-1] -
                         un[1:-1, 1:-1] * dt / dx *
                         (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) -
                         vn[1:-1, 1:-1] * dt / dy *
                         (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) -
                         dt / (2 * rho * dy) * (p[2:, 1:-1] - p[0:-2, 1:-1]) +
                         nu * (dt / dx ** 2 *
                               (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) +
                               dt / dy ** 2 *
                               (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1])))

        # Setting BC's for the u and v direction.
        u[0, :] = 0
        u[:, 0] = 0
        u[:, -1] = 0
        u[-1, :] = 1  # set velocity on cavity lid equal to 1
        v[0, :] = 0
        v[-1, :] = 0
        v[:, 0] = 0
        v[:, -1] = 0

    return u, v, p

# >>> Going through the cavity flow solution with 100 time steps:
# Set initial conditions of 0's in a matrix of dimensions nx by ny.
u = numpy.zeros((ny, nx))
v = numpy.zeros((ny, nx))
p = numpy.zeros((ny, nx))
b = numpy.zeros((ny, nx))
# Set number of time steps for the solver to run.
nt = 100
# Calls the cavity flow equation and inputs all variables.
u, v, p = cavity_flow(nt, u, v, dt, dx, dy, p, rho, nu)

# Plotting the results:
fig = pyplot.figure(figsize=(11,7), dpi=100)
# Plotting the pressure field as a contour.
pyplot.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
pyplot.colorbar()
# Plotting the pressure field outlines.
pyplot.contour(X, Y, p, cmap=cm.viridis)
# Plotting velocity field.
pyplot.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])
pyplot.xlabel('X')
pyplot.ylabel('Y');

# >>> Going through the cavity flow solution with 700 time steps:
# Set initial conditions of 0's in a matrix of dimensions nx by ny.
u = numpy.zeros((ny, nx))
v = numpy.zeros((ny, nx))
p = numpy.zeros((ny, nx))
b = numpy.zeros((ny, nx))
# Set number of time steps for the solver to run.
nt = 700
# Calls the cavity flow equation and inputs all variables.
u, v, p = cavity_flow(nt, u, v, dt, dx, dy, p, rho, nu)

# Plotting the results:
fig = pyplot.figure(figsize=(11, 7), dpi=100)
# Plotting the pressure field as a contour.
pyplot.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
pyplot.colorbar()
# Plotting the pressure field outlines.
pyplot.contour(X, Y, p, cmap=cm.viridis)
# Plotting velocity field.
pyplot.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])
pyplot.xlabel('X')
pyplot.ylabel('Y');

# Display the results of the first, and then second case.
pyplot.show()
