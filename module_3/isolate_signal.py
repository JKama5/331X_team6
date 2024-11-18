import sys
import numpy as np

# ----------------------------------------------------------
# Isolating signal samples from continuous receiving. (ECE331X Module 3)
#
# 11-18-2024
# Octavio Bittar (orbittar@wpi.edu)
# Jack Kamataris (jakamataris@wpi.edu)
# ----------------------------------------------------------

## Returns only the range of sample containing a signal with magnitude over a third of the maximum.
def isolateSignal(samples, sampling_freq):

    ## Isolating signal in time domain:
    start_index, end_index = None, None

    ## Determine the threshold magnitude
    threshold_abs = max(abs(samples)) / 3

    #Move forward in the array until there is a signal.
    for i in range(len(samples) - 1):
        if abs(samples[i]) >= threshold_abs:
            start_index = i
            break

    #Move backwards in the array until there is a signal.
    for i in reversed(range(len(samples) - 1)):
        if abs(samples[i]) >= threshold_abs:
            end_index = i
            break

    if start_index == None or end_index == None:
        print("No signal found!")
        sys.exit(0)

    # Isolate the range between between when the signal started and ended.
    signal_samples = samples[start_index:end_index]
    print("Isolated signal from", start_index/sampling_freq, "s to", end_index/sampling_freq, "s.")
    return signal_samples