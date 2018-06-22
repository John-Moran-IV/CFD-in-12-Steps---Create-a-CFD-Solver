import numpy
import timeit

u = numpy.array((0, 1, 2, 3, 4, 5))  # Create an array for 'u'.

for i in range(1, len(u)):  # Loop for the number of values in the 'u' array, minus 1.
    print(u[i] - u[i-1])  # Find the difference between each pair of adjacent numbers
    # using array operations.

nx = 81  # Number of x-dir grid points.
ny = 81  # Number of y-dir grid points.
nt = 100  # Number of time steps.
c = 1  # Wave speed constant.
dx = 2 / (nx - 1)  # Spacing in the x-dir, as a function of the number of points in x.
dy = 2 / (ny - 1)  # Spacing in the y-dir, as a function of the number of points in y.
sigma = 0.2  # The CFL/Courant number.
dt = sigma * dx  # Duration of the time steps, as a function of the CFL number and
# the x-dir grid spacing.

x = numpy.linspace(0, 2, nx)  # Create an array from 0-2 with the number of values = nx.
y = numpy.linspace(0, 2, ny)  # Create an array from 0-2 with the number of values = ny.

u = numpy.ones((ny, nx))  # Create a matrix of 1's with dimensions nx by ny.
un = numpy.ones((ny, nx))  # Create a placeholder matrix of 1's with dimensions nx by ny.

# Set IC/BC's
u[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2

u = numpy.ones((ny, nx))
u[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2

# Marks a reference point to get the time value at.
Ref1 = timeit.timeit(number=3)

# Solving the differential equation iteratively using for loops.
for n in range(nt + 1):
    un = u.copy()
    row, col = u.shape
    for j in range (1, row):
        u[j, i] = (un[j, i] - (c * dt / dx *
                    (un[j, i] - un[j, i - 1])) -
                    (c * dt / dy *
                    (un[j, i] - un[j - 1, i])))
        u[0, :] = 1
        u[-1, :] = 1
        u[:, 0] = 1
        u[:, -1] = 1

# Prints the amount of time that passed between the start and end of the loop.
print("First method time elapsed")
print(Ref1 - timeit.timeit(number=3))

# Reset the matrix IC/BC's
u = numpy.ones((ny, nx))
u[int(0.5 / dy): int(1 / dy + 1), int(0.5 / dx): int(1 / dx + 1)] = 2

# Marks a reference point to get the time value at.
Ref2 = timeit.timeit(number=3)

# Solving the differential equation using array operations.
for n in range(nt + 1):
    un = u.copy()
    u[1:, 1:] - ((c * dt / dx * (un[1:, 1:] - un[1:, 0:-1])) -
                 (c * dt / dy * (un[1:, 1:] - un[0:-1, 1:])))
    u[0, :] = 1
    u[-1, :] = 1
    u[:, 0] = 1
    u[:, -1] = 1

# Prints the amount of time that passed between the start and end of the loop.
print("Second method time elapsed")
print(Ref2 - timeit.timeit(number=3))
