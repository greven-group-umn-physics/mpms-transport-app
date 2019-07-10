'''Measurement commands module for resistivity measurements'''


def measure_resistance(lockin, shunt_resistance):
    src = lockin.output_amplitude
    ch1r = lockin.mag1
    ch2r = lockin.mag1
    current = src / (shunt_resistance + 50 + 12)  # 50 ohm internal resistiance
    rho = ch1r / current
    return src, ch1r, ch2r, rho
