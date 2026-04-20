import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose=True):
        self.bus = smbus.SMBus(1)

        self.address = address
        self.wm=0x00
        self.pds=0x00

        self.verbose = verbose
        self.dynamic_range =dynamic_range

    def deinit(self):
        self.bus.close()
        if self.verbose:
            print("I2C шина закрыта")
        
    def set_numbers(self, number):
        if not isinstance(number, int):
            print("Можно подавать только целые числа")
            return
        if not (0<=number<= 4095):
            print("Число выходит из допустимого диапазона")
            return
        first_byte=(self.wm<<4)|(self.pds<<2)|(number>>8)
        second_byte= number & 0xFF
        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")
        self.bus.write_byte_data(self.address, first_byte, second_byte)

    def set_voltage(self, voltage):
        if not (0.0<=voltage<=self.dynamic_range):
            if self.verbose:
                print("Устанавливаем 0В")
            number=0
        else:
            number=int(voltage/self.dynamic_range*4095)
            if self.verbose:
                print(f"Устанавливаем напряжение: {voltage:.2f} В")
        self.set_numbers(number)
if __name__=="__main__":
    try:
        dac = MCP4725(5.11, 0x61, True)

        while True:
            try:
                voltage = float(input("ВВедите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Выввели не число, Попрбуйте еще раз")
    finally:
        dac.deinit()