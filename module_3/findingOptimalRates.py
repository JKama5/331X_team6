import sys
import adi  
import time
import math
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


#-------------------------------------------------------------------------------------------------------------
# Methods
#-------------------------------------------------------------------------------------------------------------

## Returns a number of samples based on the parameter variables.
def recieveSamples(num_samples, buffer_size, sdr, sampling_freq):

    if num_samples % buffer_size != 0:
        print("num_samples is not divisible by buffer_size!")
        return 0

    # Create a local buffer array to store samples as we recieve them
    samples = np.zeros(num_samples, dtype=np.complex64) # replacing is faster than adding

    # Calculate the number of sdr.rx() calls needed.
    num_buffers = num_samples // buffer_size

    # Start timer
    start_time = time.time()

    # Recieve the samples by reading the buffer multiple times
    for i in range(num_buffers):
        # calculate the indexes for where we are in the local buffer
        start_idx = i * buffer_size
        end_idx = start_idx + buffer_size

        # add sdr.rx() data to the local buffer
        samples[start_idx:end_idx] = sdr.rx()

    # Stop timer
    end_time = time.time()
    print("Recorded ", num_samples, " in ", (end_time - start_time), " seconds.")
    observed_sampling_rate = num_samples/(end_time-start_time)
    print("sampling rate: ", observed_sampling_rate)
    print(observed_sampling_rate/sampling_freq*100, "% of data recieved.")
    
    # Clears the Pluto buffer
    sdr.rx_destroy_buffer()
    
    # Save samples to a file
    #np.save('pluto_samples.npy', samples)
    
    return samples

#-------------------------------------------------------------------------------------------------------------
# Program
#-------------------------------------------------------------------------------------------------------------

# ## Connect to Pluto SDR
# try:
#     sdr = adi.Pluto("ip:192.168.2.1")
# except:
#     print("No Pluto Radio device found!")
#     sys.exit(0)


# ## SDR variables (user defined)
# carrier_freq = 433900000 # Specific frequency of the AcuRite Wireless Digital Weather Thermometer located in Room AK320.
# target_time_duration = 30 # how long we want to collect data for (thermometer transmits every 15-30 seconds).

# # these impact the sampling rate (must be optimized)
# sampling_freq = 521000 # ADC samples per second, min 521 kHz.
# bandwidth = carrier_freq/4 # The bandwidth of the reciever.
# buffer_size = 2**15 # size of the sample buffer on the SDR (each sdr.rx() call returns this ammount of samples).

# ## Configuring Pluto SDR
# sdr.sample_rate = int(sampling_freq)
# sdr.center_freq = int(carrier_freq)
# sdr.rx_rf_bandwidth = int(bandwidth)
# sdr.rx_lo = int(carrier_freq) # Local oscillator frequency, just set it to the carrier frequency.
# sdr.rx_buffer_size = int(buffer_size)

# ## Collect samples from Pluto SDR
# num_samples = math.ceil(sampling_freq*target_time_duration/buffer_size) * buffer_size
# samples = recieveSamples(num_samples, buffer_size)

# ## Spectogram

# # Spectogram Variables
# slice_size = 256
# overlap_size = 64

# # Generate the Matplotlib spectrogram of the two sinusoidal signals
# t_spectro, f_spectro, specresults = signal.spectrogram(samples, sampling_freq,'hamming', int(slice_size), int(overlap_size))