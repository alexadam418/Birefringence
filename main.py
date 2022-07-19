from data_processing import *
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib import cm
import time

diameter = 100  # in mm
depth = 0.03  # in m
points = 1000
start_x = 115
start_z = 5
user_email = "alexadam418@gmail.com"

success = 0
box_start = [-60, -60]
gcode, x_loc, z_loc, width = create_gcode(points, diameter, start_x, start_z)  # creates gcode for scan
fan_threshold = fan_signal_check()  # specifies the threshold for when fans are on/off
npoints = width ** 2
r_1 = np.zeros(npoints)
r_2 = np.zeros(npoints)
send_command(gcode[0])  # sends commands to initalise 3D printer
send_command(gcode[1])
send_command(gcode[2])
send_command('M106 S0')
act1 = 2
act2 = 2
send_command("G1 X100 Z50 F300")  # Moves test mass so that alignment check can be done
begin = input("Please set polariser to 45 deg. If this is complete enter 'y': ")
if begin.lower() == "y":
    for i in range(3, npoints + 3):  # begins first set of measurements
        msg, act1 = send_commands(gcode[i])  # moves the test mass
        print(msg)
        time.sleep(1)
        while True:  # checks if test mass has arrived at next location
            wait = fan_signal()
            if wait >= fan_threshold:
                break
            else:
                time.sleep(1)
        # check if moved (needs to be written)
        r_1[i - 3] = take_measurement(1)  # takes data and calculates the "r" value
        send_command("M106 S0")  # re-initalises fan signal to off
        if act1 == 0:
            break
    send_command("G1 X100 Z50 F300")  # Moves test mass so alignment check can be conducted
    if act1 == 1:
        try:
            send_notif1(user_email)
        except:
            print("Error sending first email")
        check = input("Have you changed it to 0 degrees? (y/n): ")
        if check.lower() == "y":
            send_command("M106 S0")
            for i in range(3, npoints + 3):
                msg, act2 = send_commands(gcode[i])
                print(msg)
                time.sleep(1)
                while True:
                    wait = fan_signal()
                    if wait >= fan_threshold:
                        break
                    else:
                        time.sleep(1)
                r_2[i - 3] = take_measurement(2)
                send_command("M106 S0")
                if act2 == 0:
                    break
            if act2 == 1:  # completes final calculations and plots the data
                rho = 0.5*np.arctan(r_2/r_1)  # calculates phase shift in rad
                delta = np.sqrt(r_1 ** 2 + r_2 ** 2)
                delta_n = (delta * 1.995e-6) / (2 * np.pi * depth)  # calculates birefringence (unitless)
                measured_birefringence = np.reshape(delta_n, (width, width))
                measured_birefringence = np.rot90(measured_birefringence, 2, (0, 1))  # rotates scan correct way
                gcode, x_loc, z_loc, width = create_gcode(points, diameter, 0, -50)
                x_values = np.reshape(x_loc, npoints)
                z_values = np.reshape(z_loc, npoints)
                newpoints = np.floor(np.sqrt(12500000/points))  # ensures that there are not too many points for interp
                xq = np.linspace(box_start[0], box_start[0] + 20 + diameter, newpoints)
                zq = np.linspace(box_start[1], box_start[1] + 20 + diameter, newpoints)
                try:
                    interp_data = interpolate.interp2d(x_values, z_values, measured_birefringence, kind="linear")
                    plot_data = interp_data(xq, zq)
                    plt.figure(1)
                    plt.subplot()
                    plt.pcolormesh(xq, zq, plot_data, cmap=cm.jet)
                    plt.colorbar()
                    plt.clim(0, 5e-7)
                    plt.savefig("birefringence.png")  # saves interpolated figure
                except:
                    print("Error in interpolated plot")
                plt.figure(2)
                plt.scatter(x_loc, z_loc, c=np.flip(delta_n), cmap=cm.jet)
                plt.colorbar()
                plt.clim(0, 5e-7)
                plt.savefig("birefringence_scatter.png")  # saves scatter plot of data
                np.savetxt(fname="birefringence.txt", X=delta_n, newline="\n")  # saves data to txt file
                np.savetxt(fname="phase_shift.txt", X=rho, newline="\n")
                try:
                    send_notif2(user_email)
                except:
                    print("Error sending second email")
                success = 1

            else:
                print("Problem in Second Measurement")
        else:
            print("Scan Failed")
    else:
        print("Problem in First Measurement")
    if success == 0:
        send_notif3(user_email)
