import numpy as np
import time
def get_sin_wave_amplitude(freq, time):
    sin_value = np.sin(2 * np.pi *freq * time)
    shifted = sin_value +1
    normalized = shifted/2
    return normalized
def wait_for_sampling_period(sampling_frequency):
    sampling_period=1 /sampling_frequency
    time.sleep(sampling_period)
