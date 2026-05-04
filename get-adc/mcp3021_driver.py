import smbus
import time
import matplotlib.pyplot as plt

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
def plot_sampling_period_hist(time):
    sampling_periods=[]
    for i in range(1, len(time)):
        period=time[i]-time[i-1]
        sampling_periods.append(period)
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=20, edgecolor='black')
    plt.title("Распределение периодов измерений")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")
    plt.xlim(0, 0.6)
    plt.grid(True)
    plt.show()

if __name__=="__main__":
    dynamic_range_volts=5.0
    voltage_values=[]
    time_values=[]
    duration=3.0
    adc=None
    try:
        adc=MCP3021(dynamic_range_volts, verbose=False)

        start_time=time.time()
        while time.time()-start_time<duration:
                voltage=adc.get_voltage()
                current_time=time.time()-start_time

                voltage_values.append(voltage)
                time_values.append(current_time)
                print(f"t={current_time:.3f}с, U={voltage:.3f}В")
                time.sleep(0.1)
        plot_voltage_vs_time(time_values, voltage_values, dynamic_range_volts)
        plot_sampling_period_hist(time_values)
    except KeyboardInterrupt:
        print("\nПрограмма остановленна пользователем")

    except Exception as e:
        print(f"Произошла ошибка{e}")
    finally:
        if adc:
            adc.deinit()
            