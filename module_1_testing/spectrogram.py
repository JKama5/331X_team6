import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
# ----------------------------------------------------------
# Example code to implement a handmade spectrogram
#
# Alexander Wyglinski (alexw@wpi.edu)
# 10-28-2024
# ----------------------------------------------------------
# ----------------------------------------------------------
# Define the handmade spectrogram function
def myspectrogram(data,N,M,Fs):
# Calculate number of windows to be processed
num_windows = int((len(data) - (M/2)) // (N - (M/2)))
# Generate Hamming window
hamming_window = np.hamming(N)
# Define time instances for FFT slices
t_spectro = np.arange(0, (num_windows)*(N*(1/Fs)), N*(1/Fs))
# Define FFT bin frequencies (normalized by 2\pi)
f_spectro = np.arange(0, 1, 1/N)
# Divide up data into blocks of size N, with M/2 overlap with previous
# block and M/2 overlap with next block, and multiple with hamming window
spectrogram_results = np.zeros((num_windows,N))
for i in range(num_windows):
start_ind = i*(int(N - (M/2)))
seg = data[start_ind:(start_ind + N)]
windowed_seg = seg*hamming_window
abs_fft_result = np.abs(np.fft.fft(windowed_seg))
spectrogram_results[i] = abs_fft_result
return t_spectro, f_spectro, spectrogram_results
# ----------------------------------------------------------
# Generate example sinusoid signals summed together for testing
Fs = 1000 # Sampling frequency
Ts = 1/Fs # Sampling period
Fc1 = 100 # Carrier frequency 1
Fc2 = 150 # Carrier frequency 2
t = np.arange(0, 100, Ts) # Generate time signal at uniform discrete intervals
x = np.sin(2*np.pi*Fc1*t) + np.sin(2*np.pi*Fc2*t) # Generate two sinusoidal signals
with different frequencies
# ----------------------------------------------------------
# Generate the handmade spectrogram of the two sinusoidal signals
t_spectro, f_spectro, specresults = myspectrogram(x,256,64,Fs)
# print(len(t_spectro))
# print(len(f_spectro))
# print(specresults.shape)
# ----------------------------------------------------------
# Generate the Matplotlib spectrogram of the two sinusoidal signals
t_spectro1, f_spectro1, specresults1 = signal.spectrogram(x,Fs,'hamming',256,64)
# ----------------------------------------------------------
# Plot handmade version of spectrogram using color mesh plotting routine
plt.pcolormesh(t_spectro,f_spectro,np.log10(specresults.T),shading='auto')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [seconds]')
plt.show()
# ----------------------------------------------------------
# Plot "SciPy" version of spectrogram using color mesh plotting routine
plt.pcolormesh(t_spectro1,f_spectro1,np.log10(specresults1.T),shading='auto')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [seconds]')
plt.show()
