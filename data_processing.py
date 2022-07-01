import numpy as np
from scipy import signal
from scipy import special
import nidaqmx
from nidaqmx.stream_readers import AnalogSingleChannelReader
import time
import json
import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


def create_gcode(point, diameter, start_x, start_z):
    margin = 20
    gcode = ["G90", "M82", "G21"]
    act_width = diameter + margin
    box_start = [start_x - act_width * 0.5, start_z - 0.5 * margin]
    width = round(np.sqrt(point))
    line_size = np.array(range(1, width + 1))
    point_diff = act_width / width
    x_points = point_diff * (line_size - 0.5) + box_start[0]
    z_points = point_diff * (line_size - 0.5) + box_start[1]
    scan_rx, scan_rz = np.meshgrid(x_points, z_points)
    for i in range(0, width):
        for j in range(0, width):
            gcode_str = "G1 X{:.2f} Z{:.2f} F300"
            gcode.append(gcode_str.format(scan_rx[i, j], scan_rz[i, j]))
    return gcode, scan_rx, scan_rz, width


def nextpow2(number):
    return np.ceil(np.log2(number))


def find_r(data, sample_rate, channel):
    measurement = np.array(data, dtype=float)
    x = np.abs(measurement)
    sampfft = 2 ** nextpow2(len(x) / 10)
    ovl = sampfft // 2
    f, pxx = signal.welch(x, sample_rate, window='hann', nperseg=sampfft, noverlap=ovl)
    bandwidth = f[2] - f[1]
    fifty_range = pxx[round(49000 / bandwidth):round(51000 / bandwidth)]
    one_f_peak = np.max(fifty_range)
    one_f_peak = one_f_peak * 1.5 * bandwidth
    one_f_peak = np.sqrt(one_f_peak)
    one_f_peak = one_f_peak * 2 * np.sqrt(2)
    dc_value = np.mean(measurement)
    a = 1.2
    v_ratio = one_f_peak / dc_value
    r_val = 1
    if channel == 1:
        r_val = v_ratio * ((1 - special.jv(0, a)) / (2 * special.jv(1, a)))
    elif channel == 2:
        r_val = v_ratio * (1 / (2 * special.jv(1, a)))
    return r_val


def init_sd():
    api_key = "78BE310B9A1C4098815EEA0ECEED0B35"
    api_url = 'http://192.168.1.2/api/printer/sd'

    headers = {'Content-Type': 'application/json',
               'x-Api-Key': api_key
               }

    data = {
        'command': 'release'}
    response = requests.post(api_url, headers=headers, json=data)
    return


def set_sd():
    api_key = "78BE310B9A1C4098815EEA0ECEED0B35"
    api_url = 'http://192.168.1.2/api/printer/command'

    headers = {'Content-Type': 'application/json',
               'x-Api-Key': api_key
               }

    data = {
        'command': 'M21'}
    response = requests.post(api_url, headers=headers, json=data)
    return


def send_command(command):
    api_key = "78BE310B9A1C4098815EEA0ECEED0B35"
    api_url = 'http://192.168.1.2/api/printer/command'

    headers = {'Content-Type': 'application/json',
               'x-Api-Key': api_key
               }
    data = {
        'command': command}
    failures = 0
    while True:
        response = requests.post(api_url, headers=headers, json=data)  # either json=data or data=data
        response_code = int(response.status_code)
        if response_code < 300:
            message = 'Success: Command Sent'
            action = 1
            break
        else:
            time.sleep(2)
            failures += 1
        if failures > 10:
            message = 'Connection Error: Cannot Send Command to Octoprint'
            action = 0
            break
    return message, action


def is_moving():
    api_key = "78BE310B9A1C4098815EEA0ECEED0B35"
    api_url = 'http://192.168.1.2/api/printer?exclude=temperature,sd'
    headers = {'Content-Type': 'application/json',
               'x-Api-Key': api_key
               }
    failures = 0
    while True:
        response = requests.get(api_url, headers=headers)  # either json=data or data=data
        response_code = int(response.status_code)
        if response_code < 300:
            action = 1
            break
        else:
            time.sleep(2)
            failures += 1
        if failures > 10:
            action = 0
            break
    if action == 1:
        info = response.json()
        sd_status = info.get('state', {}).get('flags', {}).get('sdReady')
        return sd_status
    else:
        return "error"


def take_measurement(channel):
    with nidaqmx.Task() as task:
        sample_num = 300000
        task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
        task.timing.cfg_samp_clk_timing(2.1e5, samps_per_chan=sample_num)
        reader = AnalogSingleChannelReader(task.in_stream)
        read_array = np.zeros(sample_num)
        reader.read_many_sample(
            read_array, number_of_samples_per_channel=sample_num, timeout=10.0)
    r_value = find_r(read_array, 210000, channel)
    return r_value


def send_notif1(receivers_address):
    ctx = ssl.create_default_context()
    password = "qojxkexwarkaubtm"
    sender = "birefringenceprogram@gmail.com"
    receiver = receivers_address
    message = """\
    From: "Birefringence Program" <birefringenceprogram@gmail.com>
    Subject: Program 50% Complete

    Measurement step 1 complete: Awaiting User Input.
    """

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
    return


def send_notif2(receivers_address):
    ctx = ssl.create_default_context()
    password = "qojxkexwarkaubtm"
    sender = "birefringenceprogram@gmail.com"
    receiver = receivers_address
    message = MIMEMultipart("mixed")
    message["Subject"] = "Birefringence Scan Finished"
    message["From"] = sender
    message["To"] = receiver

    message.attach(MIMEText("Birefringence Scan Finished", "plain"))
    filename = r"C:\Users\jadam\PycharmProjects\pythonProject\testdata.png"
    with open(filename, "rb") as f:
        file = MIMEApplication(f.read())
    disposition = f"attachment; filename={filename}"
    file.add_header("Content-Disposition", disposition)
    message.attach(file)

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
    return


def send_commands(command):
    api_key = "78BE310B9A1C4098815EEA0ECEED0B35"
    api_url = 'http://192.168.1.2/api/printer/command'
    commands = [command, 'M106 S10']

    headers = {'Content-Type': 'application/json',
               'x-Api-Key': api_key
               }
    data = {
        'commands': commands}
    failures = 0
    while True:
        response = requests.post(api_url, headers=headers, json=data)  # either json=data or data=data
        response_code = int(response.status_code)
        if response_code < 300:
            message = 'Success: Command Sent'
            action = 1
            break
        else:
            time.sleep(2)
            failures += 1
        if failures > 10:
            message = 'Connection Error: Cannot Send Command to Octoprint'
            action = 0
            break
    return message, action


def fan_signal():
    with nidaqmx.Task() as task:
        sample_num = 1000
        task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
        task.timing.cfg_samp_clk_timing(1000, samps_per_chan=sample_num)
        reader = AnalogSingleChannelReader(task.in_stream)
        read_array = np.zeros(sample_num)
        reader.read_many_sample(
            read_array, number_of_samples_per_channel=sample_num, timeout=10.0)
    max_val = np.max(read_array)
    return max_val
