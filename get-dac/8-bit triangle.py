
import supporter_for_triangle as sup
import r2r_dac as r2r
import signal_generator as sg
import time
import RPi.GPIO as GPIO
from math import  sin,pi

print('введите значение амлитуды:')
amplitude = float(input())
print('введите значение частоты:')
signal_frequency =float(input())
print('введите значение частоты дискретизации:')
sampling_frequency =float(int(input()))

start_time = time.time()

if __name__ == "__main__":
    try:
        dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
        gpio_pins=[16, 20, 21, 25, 26, 17, 27, 22]
        while True:
            try:
                start_time = time.time()
                current_time = time.time()-start_time
                sg.wait_for_sampling_period(sampling_frequency)
                voltage  = sup.get_square_wave_amplitude(signal_frequency,current_time)

                binary_array = dac.set_voltage(voltage)
                GPIO.output(gpio_pins,binary_array)
                current_time = time.time()-start_time
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    
    finally:
        dac.deinit()                
