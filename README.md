# MPMS Transport Code
For doing transport measurements in a Quantum Design MPMS.

This is a work in progress; it may require you to know what you're doing.

More documentation is (hopefully) incoming.

## Usage notes
To do a measurement:
1. Edit the relevant script file (e.g. `mpms-resistivity.py`).
    1. Change the output data file (`datafile_write`).
    2. Change `shunt_resistance` if necessary to match the actual value.
2. Run the script (`python mpms-resistivity.py`).
3. If the MPMS data file (`datafile_MPMS`) still exists from the previous measurement, allow it to be deleted by the script.
4. Run the MPMS sequence to control temperature/field. This sequence should have several properties:
    - Any time you want a data point recorded the MPMS should do something that puts a new line in `datafile_MPMS`. The current convention is to do a `Measure DC` with 0 scan length and 8 data points (the minimum value).
    - Since the script (probably) needs the `datafile_MPMS` to exist during every pass through the measurement loop, it's a good idea for the script to start with a `Measure DC` in order to create the file that you (probably) just deleted.
5. Once the `datafile_MPMS` has been created (e.g. after the first `Measure DC`), press Enter to begin the measurement loop.
6. When you want to stop, press `Ctrl + C` in the python script window.

## Development notes
This is setup in a (Windows? Python?) `virtualenv`. To enter the `virtualenv` in a shell (on the MPMS control computer), open a Command Prompt and type `workon QdPyInterface`. Note that `workon` is a `cmd` batch file. To use it in PowerShell, try some of the work-arounds [here](https://stackoverflow.com/questions/38944525/workon-command-doesnt-work-in-windows-powershell-to-activate-virtualenv).
