import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
class R2R_DAC:
    
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    
    def set_number(self,number):
        binary_array = [int (element) for element in bin(number)[2:].zfill(8)]
        print(f"биты: {binary_array}")
        return binary_array
   
    def set_voltage(self,voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавлниваем 0.0 В")
            number = 0
        number = int(voltage / self.dynamic_range * 255)
        print(f"число на вход ЦАП: {number}")
        return self.set_number(number)


gpio_pins = [16, 20, 21, 25, 26, 17, 27, 22]

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
               
                binary_array = dac.set_voltage(voltage)
                GPIO.output(gpio_pins,binary_array)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()

