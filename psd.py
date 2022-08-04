from data_processing import*
import nidaqmx
import matplotlib.pyplot as plt

with nidaqmx.Task() as task:
    sample_num = 420000
    task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
    task.timing.cfg_samp_clk_timing(2.8e5, samps_per_chan=sample_num)
    reader = AnalogSingleChannelReader(task.in_stream)
    read_array = np.zeros(sample_num)
    reader.read_many_sample(
        read_array, number_of_samples_per_channel=sample_num, timeout=10.0)

measurement = np.array(read_array, dtype=float)
sample_rate = 2.8e5
x = np.abs(measurement)
sampfft = 2 ** nextpow2(len(x) / 10)
ovl = sampfft // 2
f, pxx = signal.welch(x, sample_rate, window='hann', nperseg=sampfft, noverlap=ovl)
plt.semilogy(f, pxx)
plt.show()

