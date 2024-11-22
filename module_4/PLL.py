import sys
import adi
import time
import math
import numpy as np
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
    R = abs(samples)
    theta = np.arctan2(np.imag(samples), np.real(samples))

    theta_shifted_Q1 = theta % np.pi/2
    theta_shifted_0 = theta_shifted_Q1 - np.pi/4


    samples_shifted_0 = R * np.exp(1j*theta_shifted_0)

    return samples_shifted_0

