import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range,compare_time=0.01, verbose=False):
        self.dynamic_range=dynamic_range
        self.verbose=verbose
        self.compare_time=compare_time

        self.bits_gpio=[26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio=21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        for i, gpio_pin in enumerate(self.bits_gpio):
            bit_value = (number>>(7-i))&1
            GPIO.output(gpio_pin, bit_value)

    def sequential_counting_adc(self):
        for test_value in range(256):
            self.number_to_dac(test_value)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio)==1:
                return test_value
        return 255
    def get_sc_voltage(self):
        digital_value =self.sequential_counting_adc()
        return (digital_value/255.0)*self.dynamic_range
    
if __name__=="__main__":
    dynamic_range_volts=3.30

    adc=None

    try:
        adc = R2R_ADC(dynamic_range_volts, verbose=False)

        while True:
            voltage = adc.get_sc_voltage()
            print(f"{voltage:3f} В")
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        if adc:
            adc.__del__()