import numpy as np
import adi
import time

def capture_pluto_samples(center_freq=915e6, sample_rate=0.521e6, num_seconds=30, gain=70.0):
    """
    Capture samples from PlutoSDR for specified duration.
    
    Args:
        center_freq (float): Center frequency in Hz (default: 915 MHz)
        sample_rate (float): Sample rate in Hz (default: 1 MHz)
        num_seconds (float): Duration of capture in seconds (default: 30)
        gain (float): RX gain in dB (default: 70.0)
    
    Returns:
        numpy.ndarray: Complex samples captured from SDR
    """
    # Initialize PlutoSDR
    sdr = adi.Pluto("ip:192.168.2.1")
    
    # Configure SDR parameters
    sdr.sample_rate = int(sample_rate)
    sdr.rx_rf_bandwidth = int(sample_rate/4)
    sdr.rx_lo = int(center_freq)
    sdr.gain_control_mode_chan0 = 'manual'
    sdr.rx_hardwaregain_chan0 = gain
    
    # Calculate number of samples needed
    num_samples = int(sample_rate * num_seconds)
    
    # Create buffer to store samples
    samples = np.zeros(num_samples, dtype=np.complex64)
    
    # Calculate buffer size for each read
    buffer_size = 2**15  # Adjust this based on your system's capabilities
    sdr.rx_buffer_size = buffer_size
    num_buffers = num_samples // buffer_size
    
    print(f"Starting capture for {num_seconds} seconds...")
    start_time = time.time()
    
    # Read samples in chunks
    for i in range(num_buffers):
        start_idx = i * buffer_size
        end_idx = start_idx + buffer_size
        samples[start_idx:end_idx] = sdr.rx()
        
        # Print progress
        if i % 10 == 0:
            progress = (i / num_buffers) * 100
            print(f"Progress: {progress:.1f}%")
    
    # Get remaining samples if any
    remaining_samples = num_samples % buffer_size
    if remaining_samples > 0:
        samples[-remaining_samples:] = sdr.rx()[:remaining_samples]
    
    end_time = time.time()
    print(f"Capture completed in {end_time - start_time:.2f} seconds")
    
    # Cleanup
    sdr.rx_destroy_buffer()
    
    return samples

if __name__ == "__main__":
    # Example usage
    samples = capture_pluto_samples()
    
    # Print basic statistics
    print(f"\nCapture Statistics:")
    print(f"Number of samples: {len(samples)}")
    print(f"Data type: {samples.dtype}")
    print(f"Mean amplitude: {np.mean(np.abs(samples)):.3f}")
    
    # Optionally save to file
    np.save('pluto_samples.npy', samples)
    print("\nSamples saved to 'pluto_samples.npy'")