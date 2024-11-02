import sys
import adi  
import time
import math
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import findingOptimalRates

## Connect to Pluto SDR
try:
    sdr = adi.Pluto("ip:192.168.2.1")
except:
    print("No Pluto Radio device found!")
    sys.exit(0)

#-------------------------------------------------------------------------------------------------------------
# Variables
#-------------------------------------------------------------------------------------------------------------

## SDR variables (user defined)
carrier_freq = 433900000 # Specific frequency of the AcuRite Wireless Digital Weather Thermometer located in Room AK320.
target_time_duration = 30 # how long we want to collect data for (thermometer transmits every 15-30 seconds).
sampling_freq = 521000 # ADC samples per second, min 521 kHz.
bandwidth = carrier_freq/4 # The bandwidth of the reciever.
buffer_size = 2**15 # size of the sample buffer on the SDR (each sdr.rx() call returns this ammount of samples).

## Configuring Pluto SDR
sdr.sample_rate = int(sampling_freq)
sdr.center_freq = int(carrier_freq)
sdr.rx_rf_bandwidth = int(bandwidth)
sdr.rx_lo = int(carrier_freq) # Local oscillator frequency, just set it to the carrier frequency.
sdr.rx_buffer_size = int(buffer_size)

# Adding gain
sdr.rx_hardwaregain_chan0 = 50  # Adjust gain (dB)

## Spectogram Variables
slice_size = 256
overlap_size = 64

#-------------------------------------------------------------------------------------------------------------
# Creating the spectogram
#-------------------------------------------------------------------------------------------------------------

## Collecting samples
num_samples = math.ceil(sampling_freq*target_time_duration/buffer_size) * buffer_size
data = findingOptimalRates.recieveSamples(num_samples, buffer_size, sdr, sampling_freq)

## Drawing spectogram
plt.specgram(data, Fs = sampling_freq, NFFT=slice_size, noverlap=overlap_size, Fc=carrier_freq)
plt.show()