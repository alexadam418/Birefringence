from data_processing import *
import numpy as np
import matplotlib.pyplot as plt

freq = 50116
dc_offset = 0.18
with nidaqmx.Task() as task:
    sample_num = 1200000
    sample_rate = 8e5
    task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
    task.timing.cfg_samp_clk_timing(sample_rate, samps_per_chan=sample_num)
    reader = AnalogSingleChannelReader(task.in_stream)
    read_array = np.zeros(sample_num)
    reader.read_many_sample(
        read_array, number_of_samples_per_channel=sample_num, timeout=10.0)
data = read_array
time_data = np.linspace(0, 3, 2400000)
measurement = np.array(data, dtype=float)
x = np.abs(measurement)
sampfft = 2 ** nextpow2(len(x) / 10)
ovl = sampfft // 2
f, pxx = signal.welch(x, sample_rate, window='hann', nperseg=sampfft, noverlap=ovl, scaling='density')
bandwidth = f[2] - f[1]
fifty_range = pxx[round(49000 / bandwidth):round(51000 / bandwidth)]
one_f_peak = np.amax(fifty_range)
one_f_peak = one_f_peak * 1.5 * bandwidth
one_f_peak = np.sqrt(one_f_peak)
one_f_peak = one_f_peak * np.sqrt(2)
dc_value = np.mean(measurement) - 0.18
print("AC Value: {}, DC Value: {}".format(2*one_f_peak, dc_value))
plt.semilogy(f, pxx)
plt.show()
