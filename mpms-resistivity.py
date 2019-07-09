"""Hacked-together script for 4-point resistance measurements.

WARNING: This is a first test, it's not correct (but it's close). In particular,
a voltage source (lock-in internal oscillator) and series resistor are used
instead of a current source.

This is designed to be used for 4-point resistance measurements in the MPMS,
using the following protocol:
    1. Hook up your sample to the lock-in as you would expect.
        - Use Ch1 for Vxx and Ch2 for Vxy.
        - Use the lock-in Osc Out for the "current" source with a resistor in 
          series with the sample.
    2. Run this script.
    3. Start whatever temperature or field sweeps you want using MultiVu.
    4. Stop the script using TODO:[some key or command] to save the data.

Script usage:
    python script-name.py [args]
        [args] can be:
            -f=filename
"""

import time as t
import msvcrt as ms
import numpy as np
import pandas as pd
import visa as v
from visa import VisaIOError
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import os as os
import os.path as op
import datetime

# Config variables
# delay = 1.0
# NOTE: Instrument setup is not (yet) implemented. Use the front panel.
lockin_tc = 1 # see manual, page 6-14
lockin_sens = 19 # see manual, page 6-11
lockin_freq = 1234.567
lockin_amp  = 1 # amplitude in μV


# Set up instruments
# tmpctl = v.ResourceManager().open_resource('GPIB0::8::INSTR')
lockin = v.ResourceManager().open_resource('GPIB0::12::INSTR')
# TODO: lockin.write('') # set up config variables ...

# src  = []
# ch1r = []
# ch2r = []
# temp = []
# rho = []
# times = []
# field = []

df = pd.DataFrame(dict(time = [], src=[], ch1r = [], ch2r = [], temp = [], rho = [], field = [],)) 

datafile_write = 'cu-RvsT-2.csv'
datafile_MPMS = 'data.dc.dat'

if op.exists(datafile_MPMS):
    if input("MPMS data file already exists. Delete? [y/N]: ") == 'y':
        os.remove(datafile_MPMS)

class Dontmeasure(Exception):
    pass

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

def measure_resistivity(lockin, shunt_resistance):
    src = float(lockin.query('OA.').split()[0])
    ch1r = float(lockin.query('MAG1.').split()[0])
    ch2r = float(lockin.query('MAG2.').split()[0])
    current = src / (shunt_resistance + 50 + 12) # 50 ohm internal resistiance
    rho = ch1r / current
    return src, ch1r, ch2r, rho

# TODO: field = []

fig = plt.figure()
grid = gs.GridSpec(3, 2, figure=fig)
ax1 = fig.add_subplot(grid[0,:])
ax1.set_xlabel("T (K)")
ax1.set_ylabel("R (ohm)")
line0, = ax1.plot(df['rho'], df['temp'], 'k.-')
ax2 = fig.add_subplot(grid[1,:])
ax2.set_xlabel("T (K)")
ax2.set_ylabel("V (V)")
line1, = ax2.plot(df['ch1r'], df['temp'], 'r.-', label='Ch. 1')
line2, = ax2.plot(df['ch2r'], df['temp'], 'b.-', label='Ch. 2')
ax2.legend()
ax3 = fig.add_subplot(grid[2,0])
ax3.set_xlabel("time")
ax3.set_ylabel("T (K)")
line3, = ax3.plot_date(df['temp'], df['time'], 'k.-')
ax4 = fig.add_subplot(grid[2,1])
ax4.set_xlabel("time")
ax4.set_ylabel("H (Oe)")
line4, = ax4.plot_date(df['field'], df['time'], 'k.-')

print("Start of loop message. Press 'CTRL + C' to stop measuring") # and save the data.")
n_lines = 0
while True:
    try:
        try:
            tem, H, n_lines = getMPMS_data(datafile_MPMS, n_lines)

            src_now, ch1r_now, ch2r_now, rho_now = measure_resistivity(lockin, shunt_resistance=1e4)

            df = df.append(dict(src=src_now, ch1r = ch1r_now, ch2r = ch2r_now, temp = tem, rho = rho_now, time = datetime.datetime.now(), field = H,), ignore_index=True)
            with open(datafile_write, 'a') as f:
                df.tail(1).to_csv(f, header=f.tell()==0)

            # src.append(src_now)
            # ch1r.append(ch1r_now)
            # ch2r.append(ch2r_now)
            # rho.append(rho_now)
            # temp.append(tem)
            # field.append(H)
            # times.append(datetime.datetime.now())
            print(df.tail(1))
        except Dontmeasure:
            continue
        except VisaIOError:
            pass
        except ValueError:
            pass
        # TODO: field.append(TODO.query(TODO))
    
        # update plot
        line1.set_ydata(df['ch1r'])
        line1.set_xdata(df['temp'])
        line2.set_ydata(df['ch2r'])
        line2.set_xdata(df['temp'])
        line0.set_ydata(df['rho'])
        line0.set_xdata(df['temp'])
        line3.set_ydata(df['temp'])
        line3.set_xdata(df['time'])
        line4.set_ydata(df['field'])
        line4.set_xdata(df['time'])
        for a in [ax1, ax2, ax3, ax4]:
            a.relim()
            a.autoscale_view()

        #fig.canvas.draw()
        #fig.canvas.flush_events()
        plt.draw()
        plt.pause(1)
        # t.sleep(delay)
    except KeyboardInterrupt:
        break



# save the data
# fname = input("Enter a file name to save the data.      ")
# if fname.endswith('.npz'):
#     np.savez(fname, source=src, ch1R=ch1r, ch2R=ch2r, temperature=temp, resistivity=rho, time=time)
# else:
#     np.savetxt(fname, (temp, src, ch1r, ch2r, rho))

# plt.close(fig=fig)