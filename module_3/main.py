import isolate_signal
import find_offset
import numpy as np
import matplotlib.pyplot as plt


## Defining parameters
sampling_freq = 521000 
T = 1 / sampling_freq
carrier_freq = 433900000
threshhold_abs = 100

# Spectogram Variables
slice_size = 1024
overlap_size = 128

## Recieve samples
file = 'module_2/pluto_samples.npy' # make path to your saved 30 seconds of data 


## Isolate the blip from 30 seconds of samples:
signalSamples = isolate_signal.isolateSignal(file, sampling_freq, threshhold_abs) # See isolate_signal.py

## Find the frequency offset
freq_offset = find_offset.findOffset(signalSamples, sampling_freq, carrier_freq, 2, len(signalSamples), 0)
print(freq_offset)

t = np.arange(0, len(signalSamples)*T, T) # time vector

Real = np.real(signalSamples)
Imag = np.imag(signalSamples)
R = abs(signalSamples)
phase = np.atan2(Real,Imag)

## Drawing spectogram
plt.figure(0)
plt.specgram(signalSamples, Fs = sampling_freq, NFFT=slice_size, noverlap=overlap_size, Fc=carrier_freq)
plt.title('Spectrogram of RF on '+ str(carrier_freq/1000000.0) + "MHz band")
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

## Plot IQ data (Signal Constellation):
plt.figure(1)
plt.scatter(Real[0:50], Imag[0:50], linewidths=0.3)
plt.axvline(x=0,)
plt.axhline(y=0)
plt.title("Signal Constellation of the Signal")
plt.xlabel('I')
plt.ylabel('Q')
plt.show()