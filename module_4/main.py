import sys
import adi
import time
import math
import numpy as np
import receiver
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# Fine frequency correction (ECE331X Module 4). 
# 
# 11-18-2024
# Octavio Bittar (orbittar@wpi.edu)
# Jack Kamataris (jakamataris@wpi.edu)
# -----------------------------------------------------------

# Connect to Pluto SDR
try:
    sdr = adi.Pluto("ip:192.168.2.1")
except:
    print("No Pluto Radio device found!")
    # sys.exit(0)

#-------------------------------------------------------------------------------------------------------------
# Variables
#-------------------------------------------------------------------------------------------------------------
sampling_freq = 5e6 # ADC samples per second, min 521 kHz.
T = 1 / sampling_freq
carrier_freq = 2.426e9 # Specific frequency of the signal coming from in Room AK320.
target_num_samples = 2e6 # How many samples we want to collect.
bandwidth = 1e6 # The bandwidth of the receiver.
buffer_size = 2**21 # size of the sample buffer on the SDR (each sdr.rx() call returns this amount of samples).

# FFT Variables
slice_size = 1024
overlap_size = 128

#-------------------------------------------------------------------------------------------------------------
# Sampling/Receiving
#-------------------------------------------------------------------------------------------------------------

# Configuring Pluto SDR
sdr.sample_rate = int(sampling_freq)
sdr.center_freq = int(carrier_freq)
sdr.rx_rf_bandwidth = int(bandwidth)
sdr.rx_lo = int(carrier_freq) # Local oscillator frequency, initially set to carrier frequency.
sdr.rx_buffer_size = int(buffer_size)

# Adding gain
sdr.gain_control_mode_chan0 = "manual"
sdr.rx_hardwaregain_chan0 = 50  # Adjust gain (dB)

# Receiving samples
num_samples = math.ceil(target_num_samples/buffer_size) * buffer_size
# uncorrected_samples = receiver.receiveSamples(num_samples, buffer_size, sdr, sampling_freq) # See findingOptimalRates.py

# np.save('module_4_samples/uncorrected_samples.npy', uncorrected_samples)
uncorrected_samples = np.load("module_4_samples/uncorrected_samples.npy")


# Plotting original data
t = np.arange(0, T*len(uncorrected_samples), T) # create time vector

plt.figure(0)
plt.specgram(uncorrected_samples, Fs = sampling_freq, NFFT=slice_size, noverlap=overlap_size, Fc=carrier_freq)
plt.title('Spectrogram of RF on '+ str((carrier_freq)/1e9) + "GHz band")
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

Real = np.real(uncorrected_samples)
Imag = np.imag(uncorrected_samples)
R = abs(uncorrected_samples)
phase = np.atan2(Real,Imag)


# ## Plot amplitude over time:
# plt.figure(2)
# plt.plot(t, R)
# plt.title("Amplitude Plot of the Signal")
# plt.xlabel('Time [sec]')
# plt.ylabel('Amplitude')
# plt.show()

# ## Plot phase over time:
# plt.figure(3)
# plt.plot(t, phase)
# plt.title("Phase Plot of the Signal")
# plt.xlabel('Time [sec]')
# plt.ylabel('Phase [rad]')
# plt.show()

## Plot IQ data:
plt.figure(4)
plt.scatter(Real, Imag, linewidths=0.3)
plt.title("Signal Constellation of the Signal")
plt.xlabel('I')
plt.ylabel('Q')
plt.show()

#-------------------------------------------------------------------------------------------------------------
# Coarse Frequency Correction
#-------------------------------------------------------------------------------------------------------------

# Find the frequency offset
# freq_offset = find_offset.findOffset(isolated_raw_signal, sampling_freq, carrier_freq, 1, 1024, 128) # See find_offset.py

# Adjusting LO to compensate for offset
# sdr.rx_lo = int(carrier_freq + freq_offset)
