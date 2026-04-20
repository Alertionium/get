import pwm_dac as pwm
import signal_generator as sg
import time
amplitude= 3.2
signal_frequency= 10
sampling_frequency=1000

try:
    dac=pwm.PWM_DAC(12, 1000, 3.3, False)

    start_time=time.time()

    while True:
        current_time=time.time()-start_time
        normalized_amp = sg.get_sin_wave_amplitude(signal_frequency, current_time)
        voltage=normalized_amp*amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()