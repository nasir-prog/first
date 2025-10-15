import numpy
import time as t
from math import sin,pi

def get_triangle_wave_amplitude(freq, time):
    period = 1.0 / freq  # Период в секундах
    position_in_period = time % period  # Позиция в текущем периоде
    phase = position_in_period/period
    if phase < 0.5:
        return phase
    else:
        return -1*phase