import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
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
    def successive_approximation_adc(self):
        result=0
        for bit in range(7, -1, -1):
            test_value = result | (1<<bit)
            self.number_to_dac(test_value)
            time.sleep(self.compare_time)

            if GPIO.input(self.comp_gpio)==0:
                result=test_value

        return result
    def get_sar_voltage(self):
        digital_value=self.successive_approximation_adc()
        return (digital_value/255.0)*self.dynamic_range

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage, '-b', linewidth=2)
    plt.title("Зависимость напряжения от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.ylim(0, max_voltage*1.1)
    plt.xlim(0, max(time) if time else 1)
    plt.grid(True)
    plt.show()

if __name__=="__main__":
    dynamic_range_volts=3.3

    voltage_values =[]
    time_values=[]
    duration=3.0

    adc=None

    try:
        adc = R2R_ADC(dynamic_range_volts, compare_time=0.0001, verbose=False)
        start_time=time.time()

        while time.time()-start_time<duration:
            voltage = adc.get_sc_voltage()
            current_time=time.time() - start_time
            voltage_values.append(voltage)
            time_values.append(current_time)
            print(f"t={current_time:.3f} с, U={voltage:.3f} В")
            time.sleep(0.01)
        plot_voltage_vs_time(time_values, voltage_values, dynamic_range_volts)
    except KeyboardInterrupt:
        pass
    finally:
        if adc:
            adc.__del__()