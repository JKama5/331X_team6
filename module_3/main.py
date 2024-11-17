import sys
import os
import isolate_signal
import find_offset
import numpy as np
import matplotlib.pyplot as plt
import adi
import math
import findingOptimalRates
import time
import matplotlib.animation as animation

## Defining parameters
sampling_freq = 521000 
T = 1 / sampling_freq
carrier_freq = 433900000
threshhold_abs = 100

# Spectogram Variables
slice_size = 1024
overlap_size = 128

## Recieve samples
file = 'pluto_samples.npy' # make path to your saved 30 seconds of data 


## Isolate the blip from 30 seconds of samples:
signalSamples = isolate_signal.isolateSignal(file, sampling_freq, threshhold_abs) # See isolate_signal.py

## Find the frequency offset
freq_offset = find_offset.findOffset(signalSamples, sampling_freq, carrier_freq, 2, len(signalSamples), 0)

t = np.arange(0, T*len(signalSamples), T) # create time vector
# samples = signalSamples * np.exp(-1j*2*np.pi*freq_offset*t)




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
sdr.rx_lo = int(carrier_freq + freq_offset) # Local oscillator frequency, just set it to the carrier frequency.
sdr.rx_buffer_size = int(buffer_size)

# Adding gain
sdr.gain_control_mode_chan0 = "manual"
sdr.rx_hardwaregain_chan0 = 50  # Adjust gain (dB)

## Spectogram Variables
slice_size = 1024
overlap_size = 128

#-------------------------------------------------------------------------------------------------------------
# Creating the spectogram
#-------------------------------------------------------------------------------------------------------------

## Collecting samples
num_samples = math.ceil(sampling_freq*target_time_duration/buffer_size) * buffer_size
data = findingOptimalRates.recieveSamples(num_samples, buffer_size, sdr, sampling_freq)

# Save samples to a file
np.save('pluto_samples_corrected.npy', data)

time.sleep(2)


# plt.specgram(data, Fs = sampling_freq, NFFT=slice_size, noverlap=overlap_size, Fc=carrier_freq+int(freq_offset))
# plt.title('Spectrogram of RF on '+ str((carrier_freq+int(freq_offset))/1000000.0) + "MHz band")
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()

samples = isolate_signal.isolateSignal("pluto_samples_corrected.npy", sampling_freq, 40)
t = np.arange(0, len(samples)*T, T) # time vector

Real = np.real(samples)
Imag = np.imag(samples)
R = abs(samples)
phase = np.atan2(Real,Imag)


## Plot amplitude over time:
plt.figure(0)
plt.plot(t, R)
plt.title("Amplitude Plot of the Signal")
plt.xlabel('Time [sec]')
plt.ylabel('Amplitude')
plt.show()

## Plot phase over time:
plt.figure(1)
plt.plot(t, phase)
plt.title("Phase Plot of the Signal")
plt.xlabel('Time [sec]')
plt.ylabel('Phase [rad]')
plt.show()

## Plot IQ data:
plt.figure(2)
plt.scatter(Real, Imag, linewidths=0.3)
plt.title("Signal Constellation of the Signal")
plt.xlabel('I')
plt.ylabel('Q')
plt.show()