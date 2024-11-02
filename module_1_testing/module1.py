import numpy as np
import adi
import matplotlib.pyplot as plt
import time

sample_rate = 10e6 # Hz
center_freq = 100e6 # Hz
buffer = 102400

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
# sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = int(buffer) # this is the buffer the Pluto uses to buffer samples

start_time = time.time()
samples = sdr.rx() # receive samples off Pluto
end_time = time.time()
print(len(samples))

time = end_time-start_time
print('seconds elapsed:', time)
print(sample_rate)
print(buffer/time)