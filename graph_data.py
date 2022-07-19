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
delta_n = np.loadtxt('birefringence.txt')
measured_birefringence = np.reshape(delta_n, (width, width))
measured_birefringence = np.rot90(measured_birefringence, 2, (0, 1))  # rotates scan correct way
gcode, x_loc, z_loc, width = create_gcode(points, diameter, 0, -50)
x_values = np.reshape(x_loc, n_points)
z_values = np.reshape(z_loc, n_points)
newpoints = np.floor(np.sqrt(12500000/points))  # ensures that there are not too many points for interp
xq = np.linspace(box_start[0], box_start[0] + 20 + diameter, newpoints)
zq = np.linspace(box_start[1], box_start[1] + 20 + diameter, newpoints)
interp_data = interpolate.interp2d(x_values, z_values, measured_birefringence, kind="linear")
plot_data = interp_data(xq, zq)
plt.figure(1)
plt.subplot()
plt.pcolormesh(xq, zq, plot_data, cmap=cm.jet)
plt.colorbar()
plt.clim(0, 5e-7)
plt.savefig("birefringence.png")  # saves interpolated figure
plt.figure(2)
plt.scatter(x_loc, z_loc, c=np.flip(delta_n), cmap=cm.jet)
plt.colorbar()
plt.clim(0, 5e-7)
plt.savefig("birefringence_scatter.png")  # saves scatter plot of data