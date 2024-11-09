import isolate_signal
import numpy as np
import matplotlib.pyplot as plt


## Defining parameters
file = 'module_2/pluto_samples.npy'
sampling_freq = 521000
T = 1 / sampling_freq
carrier_freq = 433900000
threshhold_abs = 100

## Isolate the blip from 30 seconds of samples:
samples = isolate_signal.isolateSignal(file, sampling_freq, threshhold_abs)

t = np.arange(0, len(samples)*T, T) # time vector

# v = np.real(samples * np.exp(1j * 2*np.pi * carrier_freq * t)) # Bandpass waveform

## Plot amplitude over time:
R = abs(samples)

plt.figure(0)
plt.plot(t, R)
plt.title("Amplitude Plot of the Signal")
plt.xlabel('Time [sec]')
plt.ylabel('Amplitude')
plt.show()

## Plot phase over time:
Θ = np.angle(samples)

plt.figure(1)
plt.plot(t, Θ)
plt.title("Phase Plot of the Signal")
plt.xlabel('Time [sec]')
plt.ylabel('Phase [rad]')
plt.show()