from data_processing import *
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib import cm
import time

diameter = 100  # in mm
depth = 0.03  # in m
points = 50
start_x = 90
start_z = 5
user_email = "alexadam418@gmail.com"

box_start = [-60, -60]
gcode, x_loc, z_loc, width = create_gcode(points, diameter, start_x, start_z)

npoints = width ** 2
r_1 = np.zeros(npoints)
r_2 = np.zeros(npoints)
# some stuff happens
send_command(gcode[0])
send_command(gcode[1])
send_command(gcode[2])
send_command('M106 S0')
for i in range(3, npoints + 3):
    msg, act1 = send_commands(gcode[i])
    print(msg)
    time.sleep(1)
    while True:
        wait = fan_signal()
        if wait > 4:
            break
        else:
            time.sleep(1)
    # check if moved (needs to be written)
    r_2[i - 3] = take_measurement(2)
    send_command("M106 S0")
    if act1 == 0:
        break
if act1 == 1:
    send_notif1(user_email)
    check = input("Have you changed it to 45 degrees? (y/n): ")
    if check.lower() == "y":
        send_command("M106 S0")
        for i in range(3, npoints + 3):
            msg, act2 = send_commands(gcode[i])
            print(msg)
            time.sleep(1)
            while True:
                wait = fan_signal()
                if wait >= 4:
                    break
                else:
                    time.sleep(1)
            r_1[i - 3] = take_measurement(1)
            send_command("M106 S0")
            if act2 == 0:
                break
        if act2 == 1:
            rho = 0.5*np.arctan(r_2/r_1)
            delta = np.sqrt(r_1 ** 2 + r_2 ** 2)
            delta_n = (delta * 1.995e-6) / (2 * np.pi * depth)
            measured_birefringence = np.reshape(delta_n, (width, width))
            measured_birefringence = np.rot90(measured_birefringence, 2, (0, 1))
            gcode, x_loc, z_loc, width = create_gcode(points, diameter, 0, -50)
            x_values = np.reshape(x_loc, npoints)
            z_values = np.reshape(z_loc, npoints)
            newpoints = 500
            xq = np.linspace(box_start[0], box_start[0] + 20 + diameter, newpoints)
            zq = np.linspace(box_start[1], box_start[1] + 20 + diameter, newpoints)
            interp_data = interpolate.interp2d(x_values, z_values, measured_birefringence, kind="linear")
            plot_data = interp_data(xq, zq)
            plt.figure(1)
            plt.subplot()
            plt.pcolormesh(xq, zq, plot_data, cmap=cm.jet)
            plt.colorbar()
            plt.clim(0, 1e-7)
            plt.savefig("birefringence.png")
            send_notif2(user_email)
            plt.figure(2)
            plt.scatter(x_loc, z_loc, c=np.flip(delta_n), cmap=cm.jet)
            plt.colorbar()
            plt.clim(0, 1e-7)
            plt.savefig("birefringence_scatter.png")
            print("birefringence: {}").format(delta_n)
            print("phase shift: {}").format(rho)
        else:
            print("Problem in Second Measurement")
    else:
        print("Scan Failed")
else:
    print("Problem in First Measurement")
