from polarisercontrol import *
from data_processing import *
import numpy as np
import matplotlib.pyplot as plt

npoints = 500
r_1 = np.zeros(npoints)
r_2 = np.zeros(npoints)
delta = np.zeros(npoints)
delta_n = np.zeros(npoints)

movepolariser(45)
for i in range(npoints):
    r_1[i] = take_measurement(1)
movepolariser(0)
for i in range(npoints):
    r_2 = take_measurement(2)

delta = np.sqrt(r_1 ** 2 + r_2 ** 2)
delta_n = (delta * 1.995e-6) / (2 * np.pi * 0.03)
np.savetxt(fname="repeatmeasdata.txt", X=delta_n, newline="\n")
print(np.mean(delta_n), np.std(delta_n))
plt.plot(delta_n)
plt.show()