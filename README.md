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
5. When you want to stop, press `Ctrl + C` in the python script window.

## Development notes
This is setup in a (Windows? Python?) `virtualenv`. To enter the `virtualenv` in a shell (on the MPMS control computer), open a Command Prompt and type `workon QdPyInterface`. Note that `workon` is a `cmd` batch file. To use it in PowerShell, try some of the work-arounds [here](https://stackoverflow.com/questions/38944525/workon-command-doesnt-work-in-windows-powershell-to-activate-virtualenv).
