import smbus
import time
class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus=smbus.SMBus(1)
        self.dynamic_range=dynamic_range
        self.address=0x4D
        self.verbose=verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data= self.bus.read_word_data(self.address, 0)
        lower_data_byte=data>>8
        upper_data_byte=data & 0xFF
        number=(upper_data_byte<<6) | (lower_data_byte>>2)

        return number
    def get_voltage(self):
        digital_value=self.get_number()
        return (digital_value/1023.0)*self.dynamic_range
if __name__=="__main__":
    dynamic_range_volts=5.0
    adc=None
    try:
            adc=MCP3021(dynamic_range_volts, verbose=False)

            while True:
                voltage=adc.get_voltage()
                print(f"Напряжение:{voltage:.3f}В")
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nПрограмма остановленна пользователем")

    except Exception as e:
        print(f"Произошла ошибка{e}")
    finally:
        if adc:
            adc.deinit()
            