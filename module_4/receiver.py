import sys
import adi  
import time
import math
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# Receiving continuous samples data from Pluto SDR
#
# 11-18-2024
# Octavio Bittar (orbittar@wpi.edu)
# Jack Kamataris (jakamataris@wpi.edu)
# ----------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------
# Methods
#-------------------------------------------------------------------------------------------------------------

## Returns a number of samples based on the parameter variables.
def receiveSamples(num_samples, buffer_size, sdr, sampling_freq):

    if num_samples % buffer_size != 0:
        print("num_samples is not divisible by buffer_size!")
        return 0

    # Create a local buffer array to store samples as we receive them
    samples = np.zeros(num_samples, dtype=np.complex64) # replacing is faster than adding

    # Calculate the number of sdr.rx() calls needed.
    num_buffers = num_samples // buffer_size

    if num_buffers == 1:
        samples = sdr.rx()
        print("Recorded", buffer_size, "samples in a burst.")
    else:
        # Start timer
        start_time = time.time()

        # Receive the samples by reading the buffer multiple times
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
        print(observed_sampling_rate/sampling_freq*100, "% of data received.")
    
    # Clears the Pluto buffer
    sdr.rx_destroy_buffer()
    
    # Save samples to a file
    #np.save('pluto_samples.npy', samples)
    
    return samples