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
    
    def __del__(self):
        """Деструктор - очистка GPIO при удалении объекта"""
        self.deinit()
    
    def deinit(self):
        """Очистка GPIO и установка 0 на выходах"""
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
        if self.verbose:
            print("GPIO очищен")
    
    def set_number(self, number):
        """Преобразует число в двоичный массив (для отладки)"""
        binary_array = [int(element) for element in bin(number)[2:].zfill(8)]
        print(f"биты: {binary_array}")
        return binary_array

    def number_to_dac(self, number):
        """
        Подаёт число на вход ЦАП
        
        Args:
            number (int): Число от 0 до 255 для подачи на ЦАП
        """
        # Преобразуем число в двоичное представление
        binary_str = bin(number)[2:].zfill(8)
        
        # Устанавливаем каждый бит на соответствующий GPIO пин
        for i, pin in enumerate(self.bits_gpio):
            bit_value = int(binary_str[i])
            GPIO.output(pin, bit_value)
        
        if self.verbose:
            print(f"Подано число {number} ({binary_str}) на ЦАП")

    def sequential_counting_adc(self):
        """
        Реализация АЦП последовательного счёта
        
        Returns:
            int: Цифровое значение от 0 до 255
        """
        # Последовательно увеличиваем число на ЦАП от 0 до 255
        for number in range(256):
            # Подаём текущее число на ЦАП
            self.number_to_dac(number)
            
            # Ждём стабилизации компаратора
            t.sleep(self.compare_time)
            
            # Читаем состояние компаратора
            # Если компаратор возвращает 0 - значит напряжение ЦАП превысило входное
            comparator_state = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"Шаг {number}: ЦАП = {number}, Компаратор = {comparator_state}")
            
            # Если компаратор показывает 0, возвращаем предыдущее значение
            if comparator_state == 0:
                # Возвращаем предыдущее число (текущее уже превысило)
                result = max(0, number - 1)
                if self.verbose:
                    print(f"Напряжение превышено! Возвращаем {result}")
                return result
        
        # Если не превысили за весь диапазон, возвращаем максимальное значение
        if self.verbose:
            print("Достигнут максимум диапазона (255)")
        return 255

    def get_sc_voltage(self):
        """
        Измеряет напряжение и возвращает его в Вольтах
        
        Returns:
            float: Напряжение в Вольтах
        """
        # Получаем цифровое значение
        digital_value = self.sequential_counting_adc()
        
        # Преобразуем в напряжение: (цифровое значение / 255) * динамический диапазон
        voltage = (digital_value / 255.0) * self.dynamic_range
        
        if self.verbose:
            print(f"Цифровое значение: {digital_value}, Напряжение: {voltage:.3f} В")
        
        return voltage


# Основной охранник
if __name__ == "__main__":
    adc = None
    try:
        # Создаём объект АЦП
        # dynamic_range нужно измерить мультиметром для вашего ЦАП (обычно 3.3V или 5V)
        adc = R2R_ADC(dynamic_range=3.3, compare_time=0.01, verbose=False)
        
        print("АЦП последовательного счёта запущен. Ctrl+C для остановки.")
        
        # Бесконечный цикл измерений
        while True:
            # Измеряем напряжение
            voltage = adc.get_sc_voltage()
            
            # Выводим результат
            print(f"Измеренное напряжение: {voltage:.3f} В")
            
            # Пауза между измерениями
            t.sleep(1)
            
    except KeyboardInterrupt:
        print("\nИзмерение прервано пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Гарантированно очищаем ресурсы
        if adc:
            adc.deinit()
