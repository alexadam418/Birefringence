from data_processing import*
import time
send_command('M106 S0')
standard = fan_signal()
print(standard)
send_command('M106 S10')
measurement = fan_signal()
print(measurement)
