#Collaborated with Harry Zhang and referred to - http://csundergrad.science.uoit.ca/courses/csci3010u/code/rk4-help/rk4-help.html

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode

m = 1000
ks = 50000
cs = 4000
los = 0.4
g = 10

xi = m*g/(4*ks)
x0 = los - xi
vi = 0

def dop853(t, state):
   
    x, y = state
    val = [y,-4*cs / m*y - 4*ks/m * x]
    return val

solver = ode(dop853)
solver.set_integrator('dop853')

t0 = 0.0
z0 = [xi, vi]
solver.set_initial_value(z0, t0)

t1 = 5
N = 200
t = np.linspace(t0, t1, N)
sol = np.empty((N, 2))
sol[0] = z0

i = 1
while solver.successful() and solver.t < t1:
    solver.integrate(t[i])
    sol[i] = solver.y
    i += 1
sol[:,0]=sol[:,0]+ x0

plt.plot(t, sol[:,0])
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('DOP853-pos')
plt.show()

plt.plot(t, sol[:,1], label='v')
plt.xlabel('Time')
plt.ylabel('Velocity')
plt.title('DOP853-vel')
plt.show()