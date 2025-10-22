import RPi.GPIO as GPIO
import time as t

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    
    def set_number(self, number):
        binary_array = [int(element) for element in bin(number)[2:].zfill(8)]
        print(f"биты: {binary_array}")
        return binary_array

    def number_to_dac(self, number):
       

        binary_str = bin(number)[2:].zfill(8)
        
       
        for i, pin in enumerate(self.bits_gpio):
            bit_value = int(binary_str[i])
            GPIO.output(pin, bit_value)
        
        if self.verbose:
            print(f"Подано число {number} ({binary_str}) на ЦАП")

    def sequential_counting_adc(self):
       
        for number in range(256):
            
            self.number_to_dac(number)
            
           
            t.sleep(self.compare_time)
            
        
            comparator_state = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Шаг {number}: ЦАП = {number}, Компаратор = {comparator_state}")
            
            
            if comparator_state == 0:
                
                result = max(0, number - 1)
                if self.verbose:
                    print(f"Напряжение превышено! Возвращаем {result}")
                return result
        
   
        if self.verbose:
            print("Достигнут максимум диапазона (255)")
        return 255

    def get_sc_voltage(self):
        
        
        digital_value = self.sequential_counting_adc()
        
        
        voltage = (digital_value / 255.0) * self.dynamic_range
        
        if self.verbose:
            print(f"Цифровое значение: {digital_value}, Напряжение: {voltage:.3f} В")
        
        return voltage


if __name__ == "__main__":
    adc = None
    try:
        
        adc = R2R_ADC(dynamic_range=3.28, compare_time=0.01, verbose=False)
        
        print("АЦП последовательного счёта запущен. Ctrl+C для остановки.")
        
       
        while True:
            
            voltage = adc.get_sc_voltage()
            
            
            print(f"Измеренное напряжение: {voltage:.3f} В")
            
            
            t.sleep(1)
    
    finally:
        dac.deinit()