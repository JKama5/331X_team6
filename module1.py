import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy import signal
import adi  # Library for Pluto SDR
import time

# https://pysdr.org/content/pluto.html // cool link 

np.set_printoptions(threshold=sys.maxsize)
try:
    sdr = adi.Pluto("ip:192.168.2.1")
except:
    print("No Pluto Radio device found")
    sys.exit(0)


#Setting up SDR variables
carrier_freq = 433900000
sampling_freq = 100000
time_duration = 5

# Pluto SDR settings
sdr.rx_rf_bandwidth = 4000000
sdr.sample_rate = int(sampling_freq)  # Set sample rate to 1 MSPS (adjust as needed)
sdr.center_freq = int(carrier_freq)  # Set center frequency to 100 MHz (adjust as needed)
sdr.rx_lo = int(carrier_freq)       # Local oscillator frequency
sdr.rx_hardwaregain_chan0 = 50  # Adjust gain (dB)
sdr.rx_buffer_size = time_duration*sampling_freq


# do stuff


#Spectogram settings
Fs = int(sampling_freq)
N = 512  # Length of each segment
M = 64   # Overlap
#data = sdr.rx() #return 1024 samples

#Collecting data samples
thirty_sec_data = []

start_time = time.time()

data = sdr.rx()


end_time = time.time()
print('seconds elapsed:', end_time - start_time)
print(len(thirty_sec_data))
data = thirty_sec_data

#thirty_sec_data = thirty_sec_data[0:time_duration*int(sampling_freq)]


#duration of 1 slice = (N-M/2)/Fs
#number of slices = (len(data) - M/2) / (N-M/2)
#len(data) = 30 * Fs

#total duration = (30*Fs - M/2) / (N-M/2) * (N-M/2)/Fs = 30 s

#Recieving data
# plutoData = sdr.rx()
# data = []

# for x in range(30*sampling_freq):
#     data[x] = plutoData[x]

# Define the handmade spectrogram function
def myspectrogram(data, N, M, Fs):
    num_windows = int((len(data) - (M/2)) // (N - (M/2)))
    hamming_window = np.hamming(N)
    t_spectro = np.arange(0, (num_windows) * (N * (1 / Fs)), N * (1 / Fs))
    f_spectro = np.arange(0, 1, 1 / N)
    spectrogram_results = np.zeros((num_windows, N))
    for i in range(num_windows):
        start_ind = i * (int(N - (M/2)))
        seg = data[start_ind:(start_ind + N)]
        windowed_seg = seg * hamming_window
        abs_fft_result = np.abs(np.fft.fft(windowed_seg))
        spectrogram_results[i] = abs_fft_result
    return t_spectro, f_spectro, spectrogram_results


# Generate the handmade spectrogram of the received signal
t_spectro, f_spectro, specresults = myspectrogram(data, N, M, Fs)

# Plot the handmade spectrogram
plt.pcolormesh(t_spectro, f_spectro, np.log10(specresults.T), shading='auto')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [seconds]')
plt.show()

# Generate and plot the SciPy spectrogram for comparison
t_spectro1, f_spectro1, specresults1 = signal.spectrogram(data, Fs, 'hamming', N, M)
plt.pcolormesh(t_spectro1, f_spectro1, np.log10(specresults1.T), shading='auto')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [seconds]')
plt.show()