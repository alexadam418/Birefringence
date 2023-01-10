from data_processing import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from matplotlib import cm

n_points = 300
diameter = 100
width = round(np.sqrt(n_points))
points = width**2
box_start = [-60, -60]
delta_n = np.loadtxt("2023-Jan-09-1532hrs-289-pts-biref-data.txt")
phase = np.flip(np.loadtxt("2023-Jan-09-1532hrs-289-pts-phase_shift.txt"))
measured_birefringence = np.reshape(delta_n, (width, width))
meas_phase = np.reshape(phase, (width, width))
measured_birefringence = np.rot90(measured_birefringence, 2, (0, 1))  # rotates scan correct wa = np.rot90(measured_birefringence, 2, (0, 1))
gcode, x_loc, z_loc, width = create_gcode(points, diameter, 0, -15)
x_values = np.reshape(x_loc, points)
z_values = np.reshape(z_loc, points)
newpoints = 500  # ensures that there are not too many points for interp
u = np.cos(phase)
v = np.sin(phase)
xq = np.linspace(box_start[0], box_start[0] + 20 + diameter, newpoints)
zq = np.linspace(box_start[1], box_start[1] + 20 + diameter, newpoints)
plt.figure(1)
xq, zq = np.meshgrid(xq, zq)
combined = np.vstack((x_values, z_values)).T
flipped = np.flip(delta_n)
grid_1 = interpolate.griddata(combined, flipped, (xq, zq), method='linear')
plt.imshow(grid_1, origin='lower', cmap="jet", extent=[-60, 60, -60, 60])
plt.colorbar()
plt.clim(0, 1e-8)
plt.savefig("birefringence_interp.png")
plt.figure(2)
colourmap = cm.jet
plt.scatter(x_loc, z_loc, c=np.flip(delta_n), cmap=cm.jet)
#plt.quiver(x_loc, z_loc, u, v,)
plt.colorbar()
plt.xlabel("mm")
plt.ylabel("mm")
plt.clim(0, 1e-8)
plt.savefig("birefringence_scatterphase.png")  # saves scatter plot of data
plt.show()
print(np.min(delta_n))

