import RPi.GPIO as GPIO
import time
class PWM_DAC:
    def __init__(self, gpio_bits, pwm_frequency, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.pwm_frequency= pwm_frequency

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)
        self.pwm= GPIO.PWM(self.gpio_bits, self.pwm_frequency)
        self.pwm.start(0)

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()
    
   
    def set_voltage(self, voltage):
        if not(0.0 <=voltage <=self.dynamic_range):
            if self.verbose:
                print(f"Напряжение {voltage:.2f} В выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В")
                print("Устанавливаем 0.0")
            number=0
        else:
            number= (voltage/self.dynamic_range)*100
            if self.verbose:
                print(f"Кэффицент заполнения: {number:.1f}%")
        self.pwm.ChangeDutyCycle(number)
if __name__=="__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                voltage=float(input("Введите напряжение в Вольтах:"))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()