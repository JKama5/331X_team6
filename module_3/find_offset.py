import sys
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt



def findOffset(samples, Fs, Fc, modulation_order, NFFT, Noverlap):

    # Raise signal to modulation order.
    samples = samples**modulation_order
    
    # Calculate number of windows to be processed
    num_slices = int((len(samples) - (Noverlap/2)) // (NFFT - (Noverlap/2)))
    
    #Iterate through all the FFT windows
    freq_offset_per_slice = []

    for i in range(num_slices):
        start_index = i*(int(NFFT - (Noverlap/2)))
        seg = samples[start_index:(start_index + NFFT)]
        
        FFT = None
        freq = None
        bin_to_freq_offset = 0

        # Handling conversion from bin to frequnecy when the carrier frequency is larger than the sampling rate.
        if Fc >= Fs/2/modulation_order:
            bin_to_freq_offset = Fc

        # FFT
        FFT = np.fft.fftshift(np.abs(np.fft.fft(seg)))
        freq = np.fft.fftshift(np.fft.fftfreq(len(seg), 1/Fs)) / modulation_order + bin_to_freq_offset
        
        # plt.plot(freq, FFT)
        # plt.show()
        
        # Finding the total area
        total_area = sum(FFT)
        
        # Finding the bin with the average area
        area = 0
        center_bin = -1
        for j in range(NFFT):
            area += FFT[j]
            if area >= total_area/2.0:
                if(abs(total_area/2 - (area - FFT[j])) < abs(total_area/2 - area) ):
                    center_bin = j-1
                else:
                    center_bin = j
                break
        
        if center_bin == -1:
            print("ERROR: center frequency not found.")
            sys.exit(0)

           
        actual_center_freq = freq[center_bin]
        freq_offset = actual_center_freq - bin_to_freq_offset
        freq_offset_per_slice.append(freq_offset)
    
    average_freq_offset = sum(freq_offset_per_slice)/len(freq_offset_per_slice)
    print("Frequency offset:", average_freq_offset)

    return int(average_freq_offset)
            
           
    
    
# sampling_freq = 521000 
# carrier_freq = 433900000
# slice_size = 1024
# overlap_size = 128
# import isolate_signal
# file = 'pluto_samples.npy' 
# samples = np.load(file)
# signalSamples = isolate_signal.isolateSignal(file, sampling_freq, 100)

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import signal
# import math

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import signal
# import math

# # ----------------------------------------------------------
# # Example code illustrating the impact of frequency offsets
# # in modulation and demodulation
# #
# # Alexander Wyglinski (alexw@wpi.edu)
# # 11-12-2024
# # ----------------------------------------------------------

# # ----------------------------------------------------------
# # Define simulation parameters
# Fss = 1000 # Sampling frequency
# Ts = 1/Fss # Sampling period
# Fcc = 100 # Carrier frequency
# T_tot = 100 # Total time duration
# N_symb = T_tot # Number of QPSK symbols
# sigma = 0.05 # Standard deviation of AWGN channel
# Foffset = 2 # Frequency offset at receiver
# numtaps = 101 # Number of taps for lowpass filter
# Fnyquist = Fss/2 # Nyquist frequency
# Fcutoff = Fcc # Lowpass filter cutoff frequency (should match carrier frequency)


# # ----------------------------------------------------------
# # Generate transmitter cosine and sine carrier signals
# t = np.arange(0, T_tot, Ts) # Generate time signal at uniform discrete intervals
# carrier_I_tx = np.cos(2*np.pi*Fcc*t) # Generate transmitter cosine carrier signal
# carrier_Q_tx = np.sin(2*np.pi*Fcc*t) # Generate transmitter sine carrier signal

# # ----------------------------------------------------------
# # Generate random QPSK symbols
# length = t.size
# x_value = np.random.choice([-(1/math.sqrt(2)),(1/math.sqrt(2))],size=N_symb)
# y_value = np.random.choice([-(1/math.sqrt(2)),(1/math.sqrt(2))],size=N_symb)
# x_array = np.ones(length)
# y_array = np.ones(length)
# for ind in range(N_symb):
#    start = ind*Fss
#    end = (ind+1)*Fss
#    x_array[start:end] *= x_value[ind]
#    y_array[start:end] *= y_value[ind]


# # ----------------------------------------------------------
# # Generate Transmit (Ideal) Passband Signal
# s_passband = x_array * carrier_I_tx - y_array * carrier_Q_tx

# # ----------------------------------------------------------
# # Add Zero-Mean Uncorrelated Gaussian Noise to Passband Signal (Non-Ideal Channel)
# noise = np.random.normal(loc=0,scale=sigma,size=length)
# r_passband = s_passband + noise

# # ----------------------------------------------------------
# # Generate receiver cosine and sine carrier signals (w/ and w/o frequency offset)
# carrier_I_rx_no_offset = np.cos(2*np.pi*(Fcc)*t) # Generate receiver cosine carrier signal no offset
# carrier_Q_rx_no_offset = np.sin(2*np.pi*(Fcc)*t) # Generate receiver sine carrier signal no offset
# carrier_I_rx_yes_offset = np.cos(2*np.pi*(Fcc+Foffset)*t) # Generate receiver cosine carrier signal with offset
# carrier_Q_rx_yes_offset = np.sin(2*np.pi*(Fcc+Foffset)*t) # Generate receiver sine carrier signal with offset

# # ----------------------------------------------------------
# # Mix intercepted passband signal with receiver cosine and sine signals
# mixed_I_rx_no_offset = r_passband * carrier_I_rx_no_offset
# mixed_Q_rx_no_offset = r_passband * carrier_Q_rx_no_offset
# mixed_I_rx_yes_offset = r_passband * carrier_I_rx_yes_offset
# mixed_Q_rx_yes_offset = r_passband * carrier_Q_rx_yes_offset

# # ----------------------------------------------------------
# # Design the lowpass filter for removing double frequency terms
# coeffs = signal.firwin(numtaps,Fcutoff/Fnyquist)

# # ----------------------------------------------------------
# # Lowpass filter the In-Phase and Quadrature components to get reconstructed x(t) and y(t)
# x_array_reconstruct_no_offset = signal.lfilter(coeffs,1.0,mixed_I_rx_no_offset)
# y_array_reconstruct_no_offset = signal.lfilter(coeffs,1.0,mixed_Q_rx_no_offset)
# x_array_reconstruct_yes_offset = signal.lfilter(coeffs,1.0,mixed_I_rx_yes_offset)
# y_array_reconstruct_yes_offset = signal.lfilter(coeffs,1.0,mixed_Q_rx_yes_offset)


# test_samples_with_offset = x_array_reconstruct_yes_offset + 1j*y_array_reconstruct_yes_offset
# test_samples = x_array_reconstruct_no_offset + 1j*y_array_reconstruct_no_offset

# findOffset(signalSamples, sampling_freq, carrier_freq, 1, len(signalSamples), 0)