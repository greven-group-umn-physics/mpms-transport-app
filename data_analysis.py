import pandas as pd
import matplotlib.pyplot as plt


def geomfactor(cs1, cs2, length):
    '''convert units (including sample geometries) so that [Ohm] becomes [Ohm m]

    cs1 and cs2 are the sides making up the cross-section:
        Area of cross section: A = cs1 * cs2

    length is the length of the path the current takes, as in:

    R = \rho * Length / A
    \rho = R * A / Length

    all units to be given in [mm]

    for other units ([Ohm cm]), the unit conversion
        needs to be applied 'inversly'
        [Ohm m] to [Ohm cm] has a factor of 1e2

    returns: factor to be applied to the resistance
    '''
    # area in mm^2
    Amm2 = cs1 * cs2
    # area in m^2
    Am2 = Amm2 * 1e-6
    # length in m
    le = length * 1e-3
    fac = Am2 / le
    return fac


data = pd.read_csv('cu-RvsT-3.csv')


plt.plot(data['temp'], data['rho'] * geomfactor(1.15, 1.28. 3.1))
plt.show()
