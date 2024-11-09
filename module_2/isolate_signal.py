import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

## Returns only the range of sample containing a signal with magnitude over threshhold_abs.
def isolateSignal(file = 'module_2/pluto_samples.npy', sampling_freq = 521000, threshhold_abs = 100):

    ## Retreave samples from file:
    samples = np.load(file)

    ## Isolating signal in time domain:
    start_index, end_index = None, None

    for i in range(len(samples) - 1):
        if abs(samples[i]) >= threshhold_abs:
            start_index = i
            break

    for i in reversed(range(len(samples) - 1)):
        if abs(samples[i]) >= threshhold_abs:
            end_index = i
            break

    if start_index == None or end_index == None:
        print("No signal found!")
        sys.exit(0)

    signal_samples = samples[start_index:end_index]
    print("Isolated signal from", start_index/sampling_freq, "s to", end_index/sampling_freq, "s.")
    return signal_samples