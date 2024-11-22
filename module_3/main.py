import sys
import adi
import time
import math
import numpy as np
import find_offset
import isolate_signal
import findingOptimalRates
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# Coarse frequency correction (ECE331X Module 3). 
# Finds the offset, then adjusts LO and collects new samples.
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
sampling_freq = 521000 # ADC samples per second, min 521 kHz.
T = 1 / sampling_freq
carrier_freq = 433900000 # Specific frequency of the AcuRite Wireless Digital Weather Thermometer located in Room AK320.
target_time_duration = 30 # how long we want to collect data for (thermometer transmits every 15-30 seconds).
bandwidth = carrier_freq/4 # The bandwidth of the receiver.
buffer_size = 2**15 # size of the sample buffer on the SDR (each sdr.rx() call returns this amount of samples).

# FFT Variables
slice_size = 1024
overlap_size = 128

#-------------------------------------------------------------------------------------------------------------
# Calibration sample collection (no frequency compensation)
#-------------------------------------------------------------------------------------------------------------

# Configuring Pluto SDR
# sdr.sample_rate = int(sampling_freq)
# sdr.center_freq = int(carrier_freq)
# sdr.rx_rf_bandwidth = int(bandwidth)
# sdr.rx_lo = int(carrier_freq) # Local oscillator frequency, initially set to carrier frequency.
# sdr.rx_buffer_size = int(buffer_size)

# Adding gain
# sdr.gain_control_mode_chan0 = "manual"
# sdr.rx_hardwaregain_chan0 = 50  # Adjust gain (dB)

# Receiving samples
# num_samples = math.ceil(sampling_freq*target_time_duration/buffer_size) * buffer_size
# raw_samples = findingOptimalRates.receiveSamples(num_samples, buffer_size, sdr, sampling_freq) # See findingOptimalRates.py
# np.save('module_3_samples/uncorrected_samples.npy', raw_samples)
raw_samples = np.load("module_3_samples/uncorrected_samples.npy")

# Isolate the blip from 30 seconds of samples:
isolated_raw_signal = isolate_signal.isolateSignal(raw_samples, sampling_freq) # See isolate_signal.py

t = np.arange(0, T*len(isolated_raw_signal), T) # create time vector

plt.figure(0)
plt.specgram(raw_samples, Fs = sampling_freq, NFFT=slice_size, noverlap=overlap_size, Fc=carrier_freq)
plt.title('Spectrogram of RF on '+ str((carrier_freq)/1000000.0) + "MHz band")
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

Real = np.real(isolated_raw_signal)
Imag = np.imag(isolated_raw_signal)
R = abs(isolated_raw_signal)
phase = np.atan2(Real,Imag)


## Plot amplitude over time:
plt.figure(2)
plt.plot(t, R)
plt.title("Amplitude Plot of the Signal")
plt.xlabel('Time [sec]')
plt.ylabel('Amplitude')
plt.show()

## Plot phase over time:
plt.figure(3)
plt.plot(t, phase)
plt.title("Phase Plot of the Signal")
plt.xlabel('Time [sec]')
plt.ylabel('Phase [rad]')
plt.show()

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
freq_offset = find_offset.findOffset(isolated_raw_signal, sampling_freq, carrier_freq, 1, 1024, 128) # See find_offset.py

# Adjusting LO to compensate for offset
# sdr.rx_lo = int(carrier_freq + freq_offset)

#-------------------------------------------------------------------------------------------------------------
# Sample collection (with frequency compensation)
#-------------------------------------------------------------------------------------------------------------
# corrected_samples = findingOptimalRates.receiveSamples(num_samples, buffer_size, sdr, sampling_freq) # See findingOptimalRates.py
# np.save('module_3_samples/corrected_samples.npy', corrected_samples)
corrected_samples = np.load("module_3_samples/corrected_samples.npy")

# Isolate the blip from 30 seconds of samples:
isolated_corrected_signal = isolate_signal.isolateSignal(corrected_samples, sampling_freq) # See isolate_signal.py

plt.figure(1)
plt.specgram(corrected_samples, Fs = sampling_freq, NFFT=slice_size, noverlap=overlap_size, Fc=carrier_freq+freq_offset)
plt.title('Spectrogram of RF on '+ str((carrier_freq+freq_offset)/1000000.0) + "MHz band")
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

#-------------------------------------------------------------------------------------------------------------
# Corrected data visualization
#-------------------------------------------------------------------------------------------------------------
t = np.arange(0, T*len(isolated_corrected_signal), T) # create time vector

Real = np.real(isolated_corrected_signal)
Imag = np.imag(isolated_corrected_signal)
R = abs(isolated_corrected_signal)
phase = np.atan2(Real,Imag)


## Plot amplitude over time:
plt.figure(2)
plt.plot(t, R)
plt.title("Amplitude Plot of the Signal")
plt.xlabel('Time [sec]')
plt.ylabel('Amplitude')
plt.show()

## Plot phase over time:
plt.figure(3)
plt.plot(t, phase)
plt.title("Phase Plot of the Signal")
plt.xlabel('Time [sec]')
plt.ylabel('Phase [rad]')
plt.show()

## Plot IQ data:
plt.figure(4)
plt.scatter(Real, Imag, linewidths=0.3)
plt.title("Signal Constellation of the Signal")
plt.xlabel('I')
plt.ylabel('Q')
plt.show()