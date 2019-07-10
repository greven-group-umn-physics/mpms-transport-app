'''Utility module for resistivity measurements

'''

import matplotlib.pyplot as plt


class Dontmeasure(Exception):
    pass


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


def getMPMS_data(datafile, n_lines):
    try:
        with open(datafile) as f:
            file = f.readlines()
            n = len(file)
            if n <= n_lines:
                plt.pause(0.2)
                raise Dontmeasure
            else:
                n_lines = n
        line = file[-1].split(',')
        tem = float(line[3])
        H = float(line[2])
        return tem, H, n_lines
    except OSError:
        plt.pause(0.2)
        raise Dontmeasure
