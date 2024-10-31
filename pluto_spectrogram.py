import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import adi  # Library for Pluto SDR

# Initialize Pluto SDR
sdr = adi.Pluto("ip:192.168.2.1")  # Ensure the IP matches your SDR's IP

# Pluto SDR settings
sdr.sample_rate = 1000000  # Set sample rate to 1 MSPS (adjust as needed)
sdr.center_freq = 100000000  # Set center frequency to 100 MHz (adjust as needed)
sdr.rx_lo = 100000000       # Local oscillator frequency
sdr.rx_hardwaregain_chan0 = 50  # Adjust gain (dB)

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

# Fetch data from the Pluto SDR
Fs = int(sdr.sample_rate)
N = 256  # Length of each segment
M = 64   # Overlap

# Collect a sample of data
data = sdr.rx()  # Fetch data from Pluto SDR

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
