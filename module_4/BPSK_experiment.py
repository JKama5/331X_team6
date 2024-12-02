import numpy as np
import matplotlib.pyplot as plt


signal = np.load("bpsk_signal.npy")
num_samples = len(signal)

# PLL Implementation
phase_estimate = 0
phase_error_arr = np.zeros(num_samples)
def simple_pll(signal, kp, ki):
    """
    A simple Phase-Locked Loop (PLL) for phase correction.
    
    Parameters:
    signal : numpy.ndarray
        The complex input signal.
    kp : float
        Proportional gain.
    ki : float
        Integral gain.
    
    Returns:
    corrected_signal : numpy.ndarray
        The phase-corrected output signal.
    phase_error : numpy.ndarray
        The phase error over time.
    """
    num_samples = len(signal)
    phase_estimate = 0
    frequency_estimate = 0
    loop_filter = 0
    phase_error = np.zeros(num_samples)
    corrected_signal = np.zeros(num_samples, dtype=complex)
    # Iterate over each sample
    for i, sample in enumerate(signal):
        # Generate reference signal
        ref_signal = np.exp(-1j * phase_estimate)

        # Mix the input signal down to baseband
        demodulated = sample * np.conj(ref_signal)

        # Calculate phase error
        error = np.angle(demodulated)
        phase_error[i] = error

        # Update loop filter (Integral part)
        loop_filter += ki * error

        # Update frequency and phase estimates
        frequency_estimate = kp * error + loop_filter
        phase_estimate += frequency_estimate
        phase_error_arr[i] = phase_estimate
        # Correct the signal
        corrected_signal[i] = demodulated

    return corrected_signal, phase_error, phase_error_arr

# Load the saved signal
# Replace 'bpsk_signal.npy' with the actual path to your saved data file
signal = np.load("bpsk_signal.npy")

# Normalize the signal and remove DC offset (optional)
signal = signal / np.abs(signal).max()
signal = signal - np.mean(signal)

# PLL Parameters
kp = 0.0001 # Proportional gain
ki = 0.00001000# Integral gain

# Apply PLL to the signal
corrected_signal, phase_error,phase_error_array = simple_pll(signal, kp, ki)

start_index = 4300  # Start searching after the 4000th sample

# Find the smallest absolute phase error after the 4000th sample
smallest_error_index = np.argmin(np.abs(phase_error[start_index:])) + start_index
smallest_phase_error = phase_error[smallest_error_index]  # Value of smallest phase error
corresponding_phase_difference = phase_error_array[smallest_error_index]  # Corresponding phase estimate
print(f"corresponding phase difference: {corresponding_phase_difference}")

corrected_signal = signal * np.exp(-1j * corresponding_phase_difference)

# Plot Results

# Plot Phase Error Over Time
plt.figure()
plt.plot(phase_error)
plt.title("Phase Error Over Time")
plt.xlabel("Sample Index")
plt.ylabel("Phase Error (radians)")
plt.grid()
plt.show()

# Plot Constellation Diagram Before Correction
plt.figure()
plt.scatter(np.imag(signal),np.real(signal),  alpha=0.5, label="Before Correction")
plt.title("Constellation Diagram (Before PLL)")
plt.xlabel("I (Imaginary)")
plt.ylabel("Q (Real)")
plt.legend()
plt.grid()
plt.axis("equal")
plt.show()

# Plot Constellation Diagram After Correction
plt.figure()
plt.scatter(np.imag(corrected_signal),np.real(corrected_signal),  alpha=0.5, label="After Correction")
plt.title("Constellation Diagram (After PLL)")
plt.xlabel("I (Imaginary)")
plt.ylabel("Q (Real)")
plt.legend()
plt.grid()
plt.axis("equal")
plt.show()


# Calculate magnitude of the signal
amplitude = np.abs(signal)

# Plot amplitude
plt.figure("Signal Amplitude Over Time")
plt.plot(amplitude)
plt.title("Signal Amplitude Over Time")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

normalized_signal = signal / np.abs(signal)
norm = normalized_signal * np.exp(-1j * corresponding_phase_difference)

# Plot amplitude
plt.figure("Signal Amplitude Over Time")
plt.plot(norm)
plt.title("Signal Amplitude Over Time")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

spectrum = np.fft.fftshift(np.fft.fft(signal))
freq_axis = np.fft.fftshift(np.fft.fftfreq(len(signal), 1 / 1e6))
plt.plot(freq_axis, 10 * np.log10(np.abs(spectrum)))
plt.title("Spectrum of Received Signal")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power (dB)")
plt.grid(True)
plt.show()

