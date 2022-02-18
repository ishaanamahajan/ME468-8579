import numpy as np
import matplotlib.pyplot as plt
from math import e, sin, cos

m = 1000
k = 50000
c = 4000
l = 0.4
g = 10

x0 = l - m*g/(4*k)
xi = m*g/(4*k)

vi = 0
v0 = 0


def bEuler(h): 
 
 t = np.arange(0, 5 + h, h)
 position = np.zeros(t.size)
 x = np.zeros((2,t.size))

 x[0,0] = xi
 x[1,0] = vi

 for i in np.arange(1,t.size):
  
    x[0,i] = x[0, i-1] + h * x[1, i-1]
    x[1,i] = (x[1, i-1] - x[0, i-1] *4 *h * k/m ) / (1 + 4 * h * c/m+ 4 * k*h ** 2/m)

 position = np.zeros(t.size)    
 position = x[0,:] + x0

 velocity = x[1,:]
 plt.plot(t, position)
 plt.title("Position of Sprung Mass")
 plt.show()



 actual_pos = e**(-8 * t) * ((0.05 * np.cos(2* (34 ** 0.5)* t) + np.sin(2* (34 ** 0.5)* t))/ (5 ** (34 ** 0.5))) + 0.35
 actual_vel = -5 *(e** (-8 *t) * np.sin(2 * (34 ** 0.5) * t)) / (34 ** 0.5)


 error_pos = np.max(np.abs(position - actual_pos))
 error_vel = np.max(np.abs(velocity - actual_vel))

 

 print("Largest error in position: ", error_pos)
 print("Largest error in velocity: ", error_vel)
 
 

 return np.array(([error_pos, error_vel]))
 

bEuler(10**(-4))

h_vals = np.array([10** (-1),10** (-2),10** (-3), 10** (-4), 10** (-5)])
error_pos = np.zeros(5)
error_vel = np.zeros(5)
for i in np.arange(0,h_vals.size):
    error_pos[i] = bEuler(h_vals[i])[0]
    error_vel[i] = bEuler(h_vals[i])[1]

plt.plot(h_vals, error_pos, label = "Position error")
plt.plot(h_vals, error_vel, label = "velocity error")
plt.legend()
plt.xscale('log')
plt.yscale('log')
plt.show()
