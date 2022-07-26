from data_processing import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from matplotlib import cm

n_points = 2000
diameter = 100
width = round(np.sqrt(n_points))
points = width**2
box_start = [-60, -60]
delta_n = np.loadtxt('scan data/B 2000pts 20 Jul second.txt')
measured_birefringence = np.reshape(delta_n, (width, width))
measured_birefringence = np.rot90(measured_birefringence, 2, (0, 1))  # rotates scan correct way
gcode, x_loc, z_loc, width = create_gcode(points, diameter, 0, -50)
x_values = np.reshape(x_loc, points)
z_values = np.reshape(z_loc, points)
newpoints = 500  # ensures that there are not too many points for interp

xq = np.linspace(box_start[0], box_start[0] + 20 + diameter, newpoints)
zq = np.linspace(box_start[1], box_start[1] + 20 + diameter, newpoints)
plt.figure(1)
xq, zq = np.meshgrid(xq, zq)
combined = np.vstack((x_values, z_values)).T
flipped = np.flip(delta_n)
grid_1 = interpolate.griddata(combined, flipped, (xq, zq), method='linear')
plt.imshow(grid_1, origin='lower', cmap="jet", extent=[-60, 60, -60, 60])
plt.colorbar()
plt.clim(0, 5e-7)
plt.savefig("birefringence_interp.png")
plt.figure(2)
plt.scatter(x_loc, z_loc, c=np.flip(delta_n), cmap=cm.jet)
plt.colorbar()
plt.clim(0, 5e-7)
plt.savefig("birefringence_scatter.png")  # saves scatter plot of data
