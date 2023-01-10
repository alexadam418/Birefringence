from polarisercontrol import *
from data_processing import *
import numpy as np

movepolariser(45)
r_1 = take_measurement(1)
movepolariser(0)
r_2 = take_measurement(2)

delta = np.sqrt(r_1 ** 2 + r_2 ** 2)
delta_n = (delta * 1.995e-6) / (2 * np.pi * 0.03)

print(delta_n)