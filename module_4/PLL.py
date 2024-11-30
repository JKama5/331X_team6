import sys
import adi
import time
import math
import numpy as np
from  scipy import signal
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# 
# 
#
# 11-18-2024
# Octavio Bittar (orbittar@wpi.edu)
# Jack Kamataris (jakamataris@wpi.edu)
# -----------------------------------------------------------

def fineFrequencyCorrection(samples):
    num_samples = len(samples)
    R = abs(samples)
    theta = np.atan2(np.imag(samples), np.real(samples))

    theta_reference_quadrant = np.zeros(num_samples)

    for i in range(num_samples):
        if theta[i] < 0:
            theta_reference_quadrant[i] = theta[i] + np.pi

    theta_error = np.zeros(num_samples)
    theta_error[0] = 0
    theta_correction = np.zeros(num_samples)
    theta_correction[0] = 0

    moving_average_size = 50
    margin = 0.1

    for i in range(1, num_samples):
        delta_theta = theta_reference_quadrant[i] - theta_reference_quadrant[i-1]

        if delta_theta < 0:
            delta_theta += np.pi

        moving_range = theta_error[max(0, i-moving_average_size):i]
        new_moving_average = (sum(moving_range) + delta_theta) / (len(moving_range) + 1)
        
        theta_error[i] = new_moving_average
        theta_correction[i] = theta_correction[i-1] + new_moving_average

       
    corrected_samples = samples * np.exp(-1j*theta_correction)

    plt.plot(theta_error)
    plt.show()

    return corrected_samples

