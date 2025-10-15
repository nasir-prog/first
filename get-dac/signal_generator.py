import numpy
import time as t
from math import sin,pi

def get_sin_wave_amplitude(freq,time):
    return((sin(2*pi*freq*time)+1)/2)

def wait_for_sampling_period(sampling_frequency):
    period = 1.0/sampling_frequency
    t.sleep(period)

