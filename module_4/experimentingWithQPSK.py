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

def fineFrequencyCorrection(samples, Fs):
    num_samples = len(samples)
    R = abs(samples)
    theta = np.atan2(np.imag(samples), np.real(samples))

    theta_reference_quadrant = np.zeros(num_samples)

    #Moving everything to the first signal region so we can find the angle error
    for i in range(num_samples):
        if theta[i] >= 3*np.pi/2:
            theta_reference_quadrant[i] = theta[i] - 3*np.pi/2
        elif theta[i] >= np.pi:
            theta_reference_quadrant[i] = theta[i] - np.pi
        elif theta[i] >= np.pi/2:
            theta_reference_quadrant[i] = theta[i] - np.pi/2
        elif theta[i] >= 0:
            theta_reference_quadrant[i] = theta[i]
        elif theta[i] >= -np.pi/2:
            theta_reference_quadrant[i] = theta[i] + np.pi/2
        elif theta[i] >= -np.pi:
            theta_reference_quadrant[i] = theta[i] + np.pi
        elif theta[i] >= -3*np.pi/2:
            theta_reference_quadrant[i] = theta[i] + 3*np.pi/2
        else:
            theta_reference_quadrant[i] = theta[i]

    theta_reference_quadrant = theta_reference_quadrant #- np.pi/4
    
    # T = 1/Fs
    # t = np.arange(0, T*num_samples, T) # create time vector

    theta_error = np.zeros(num_samples)
    theta_error[0] = 0
    theta_correction = np.zeros(num_samples)
    theta_correction[0] = 0

    moving_average_size = 50
    margin = 0.1

    s = R * np.exp(1j*theta_reference_quadrant)

    for i in range(1, num_samples):
        #We take how much the point has moved as the error
        delta_theta = theta_reference_quadrant[i] - theta_reference_quadrant[i-1]

        if delta_theta <= -np.pi/2+margin:
            delta_theta += np.pi/2
        elif delta_theta >= np.pi/2-margin:
            delta_theta -= np.pi/2

        moving_range = theta_error[max(0, i-moving_average_size):i]
        new_moving_average = (sum(moving_range) + delta_theta) / (len(moving_range) + 1)
        
        theta_error[i] = new_moving_average
        theta_correction[i] = theta_correction[i-1] + new_moving_average #summing the current error with the errors that came before it, so rotate the sample all the way back to the correct position

       
    corrected_samples = samples * np.exp(-1j*theta_correction)

    plt.plot(theta_error)
    plt.show()

    return corrected_samples[20000: num_samples]

# ----------------------------------------------------------
# Example code illustrating the impact of frequency offsets
# in modulation and demodulation
#
# Alexander Wyglinski (alexw@wpi.edu)
# 11-12-2024
# ----------------------------------------------------------

# ----------------------------------------------------------
# Define simulation parameters
Fss = 1000 # Sampling frequency
Ts = 1/Fss # Sampling period
Fcc = 100 # Carrier frequency
T_tot = 100 # Total time duration
N_symb = T_tot # Number of QPSK symbols
sigma = 0.05 # Standard deviation of AWGN channel
Foffset = 2 # Frequency offset at receiver
numtaps = 101 # Number of taps for lowpass filter
Fnyquist = Fss/2 # Nyquist frequency
Fcutoff = Fcc # Lowpass filter cutoff frequency (should match carrier frequency)


# ----------------------------------------------------------
# Generate transmitter cosine and sine carrier signals
t = np.arange(0, T_tot, Ts) # Generate time signal at uniform discrete intervals
carrier_I_tx = np.cos(2*np.pi*Fcc*t) # Generate transmitter cosine carrier signal
carrier_Q_tx = np.sin(2*np.pi*Fcc*t) # Generate transmitter sine carrier signal

# ----------------------------------------------------------
# Generate random QPSK symbols
length = t.size
x_value = np.random.choice([-(1/math.sqrt(2)),(1/math.sqrt(2))],size=N_symb)
y_value = np.random.choice([-(1/math.sqrt(2)),(1/math.sqrt(2))],size=N_symb)
x_array = np.ones(length)
y_array = np.ones(length)
for ind in range(N_symb):
   start = ind*Fss
   end = (ind+1)*Fss
   x_array[start:end] *= x_value[ind]
   y_array[start:end] *= y_value[ind]


# ----------------------------------------------------------
# Generate Transmit (Ideal) Passband Signal
s_passband = x_array * carrier_I_tx - y_array * carrier_Q_tx

# ----------------------------------------------------------
# Add Zero-Mean Uncorrelated Gaussian Noise to Passband Signal (Non-Ideal Channel)
noise = np.random.normal(loc=0,scale=sigma,size=length)
r_passband = s_passband #+ noise

# ----------------------------------------------------------
# Generate receiver cosine and sine carrier signals (w/ and w/o frequency offset)
carrier_I_rx_no_offset = np.cos(2*np.pi*(Fcc)*t) # Generate receiver cosine carrier signal no offset
carrier_Q_rx_no_offset = np.sin(2*np.pi*(Fcc)*t) # Generate receiver sine carrier signal no offset
carrier_I_rx_yes_offset = np.cos(2*np.pi*(Fcc+Foffset)*t) # Generate receiver cosine carrier signal with offset
carrier_Q_rx_yes_offset = np.sin(2*np.pi*(Fcc+Foffset)*t) # Generate receiver sine carrier signal with offset

# ----------------------------------------------------------
# Mix intercepted passband signal with receiver cosine and sine signals
mixed_I_rx_no_offset = r_passband * carrier_I_rx_no_offset
mixed_Q_rx_no_offset = r_passband * carrier_Q_rx_no_offset
mixed_I_rx_yes_offset = r_passband * carrier_I_rx_yes_offset
mixed_Q_rx_yes_offset = r_passband * carrier_Q_rx_yes_offset

# ----------------------------------------------------------
# Design the lowpass filter for removing double frequency terms
coeffs = signal.firwin(numtaps,Fcutoff/Fnyquist)

# ----------------------------------------------------------
# Lowpass filter the In-Phase and Quadrature components to get reconstructed x(t) and y(t)
x_array_reconstruct_no_offset = signal.lfilter(coeffs,1.0,mixed_I_rx_no_offset)
y_array_reconstruct_no_offset = signal.lfilter(coeffs,1.0,mixed_Q_rx_no_offset)
x_array_reconstruct_yes_offset = signal.lfilter(coeffs,1.0,mixed_I_rx_yes_offset)
y_array_reconstruct_yes_offset = signal.lfilter(coeffs,1.0,mixed_Q_rx_yes_offset)



samples = x_array_reconstruct_yes_offset + 1j*y_array_reconstruct_yes_offset

samples = fineFrequencyCorrection(samples, Fss)

plt.scatter(np.real(samples), np.imag(samples), linewidths=0.2)
# plt.plot(np.angle(samples))
plt.show()