import numpy
import sympy
from sympy.printing import pprint
from sympy import init_printing
from matplotlib import pyplot
init_printing(use_latex=True)

x, nu, t = sympy.symbols('x nu t')  # Setting symbols for x, nu, and t from symbol library.
# An example equation to show the look of output.
phi = (sympy.exp(-(x - 4 * t)**2 / (4 * nu * (t+ 1))) +
       sympy.exp(-(x - 4 * t - 2 * numpy.pi)**2 / (4 * nu * (t + 1))))
pprint("Phi")  # Labeling the following equation.
pprint(phi)  # Prints Phi using pretty print, outputs the result in equation form.

pprint("Phi prime")  # Labeling the following equation.
phiprime = phi.diff(x)  # Solves for the derivative of phi.
pprint(phiprime)  # Prints Phi' using pretty print, outputs the result in equation form.

from sympy.utilities.lambdify import lambdify
u = -2 * nu * (phiprime / phi) + 4
pprint(u)

ufunc = lambdify((t, x, nu), u)
pprint(ufunc(1, 4, 3))

# Burger's Equation
nx = 101  # Set number of grid points in x dir
nt = 100  # Set number of time steps
dx = 2 * numpy.pi / (nx - 1)
nu = 0.07  # Viscosity
dt = dx * nu  # Time step length is a function of grid spacing and viscosity

x = numpy.linspace(0, 2 * numpy.pi, nx)
un = numpy.empty(nx)
t = 0

u = numpy.asarray([ufunc(t, x0, nu) for x0 in x])
print(u)

pyplot.figure(figsize=(11, 7), dpi=100)
pyplot.plot(x, u, marker='o', lw=2)
pyplot.xlim([0, 2 * numpy.pi])
pyplot.ylim([0, 10])
pyplot.show()

for n in range(nt):
    un = u.copy()
    for i in range(1, nx-1):
        u[i] = un[i] - un[i] * dt / dx * (un[i] - un[i - 1]) + nu * dt / dx**2 *\
               (un[i+1] - 2 * un[i] + un[i - 1])
    u[0] = un[0] - un[0] * dt / dx * (un[0] - un[-2]) + nu * dt / dx**2 *\
               (un[1] - 2 * un[0] + un[-2])
    u[-1] = u[0]
u_analytical = numpy.asarray([ufunc(nt * dt, xi, nu) for xi in x])

pyplot.figure(figsize=(11, 7), dpi=100)
pyplot.plot(x,u, marker='o', lw=2, label='Computational')
pyplot.plot(x, u_analytical, label='Analytical')
pyplot.xlim([0, 2 * numpy.pi])
pyplot.ylim([0, 10])
pyplot.legend();
pyplot.show()
