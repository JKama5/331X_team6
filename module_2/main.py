import isolate_signal
import numpy as np
import matplotlib.pyplot as plt


## Defining parameters
file = 'module_2/pluto_samples.npy' # make path to your saved 30 seconds of data 
sampling_freq = 521000 # match this frequency to what you sampled your data in 
T = 1 / sampling_freq
carrier_freq = 433900000
threshhold_abs = 100

## Isolate the blip from 30 seconds of samples:
samples = isolate_signal.isolateSignal(file, sampling_freq, threshhold_abs) # See isolate_signal.py for brief

t = np.arange(0, len(samples)*T, T) # time vector

Real = np.real(samples)
Imag = np.imag(samples)
sR = abs(samples)
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