import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import os

#
# Plots a waterfall plot, Stokes I and time series plot for a voltage dump file from GReX using the default file structure
#

# Plot parameters
left, width = 0.15, 0.55
left2 = left + width + 0.05
bottom, height = 0.3, 0.55
width2, height2 = 0.2, 0.2
bottom2 = bottom - height2

rect_waterfall = [left, bottom, width, height]
rect_stokesi = [left, bottom2, width, height2]
rect_timeseries = [left + width, bottom, width2, height]

nullfmt = NullFormatter()

# Check all voltage dumps
voltage_files = [f[:20] for f in os.listdir("/hdd/data/voltages") if os.path.isfile(os.path.join("/hdd/data/voltages/", f)) and f[-3:] == ".nc"]

# Import data
volt = None

while volt == None:
    file = input("Name of a voltage dump file to process: ")

    if file[-3:] == ".nc":
        file = file[:-3]

    if file in voltage_files:
        volt = file
        break
    else:
        print("Please choose a voltage dump file in /hdd/data/voltages/")

ds = xr.open_dataset(f"/hdd/data/voltages/{volt}.nc")

log = None

while log == None:
    logged = input("Take log of the values? [Y/N]")

    if logged.upper()[0] == "Y":
        log = True
        break
    elif logged.upper()[0] == "N":
        log = False
        break

# Get complex voltages
voltages = ds["voltages"].sel(reim="real") + ds["voltages"].sel(reim="imaginary")*1j

# Get datasets to plot
waterfall = np.square(abs(voltages)).sum(dim='pol')
stokesi = waterfall.sum(dim='time')
timeseries = waterfall.sum(dim='freq')

if log == True:
    waterfall = np.log(waterfall)

print("Generating Stokes I plot")
axStokesI = plt.axes(rect_stokesi)
stokesi.plot()
plt.title('')
if log == True:
    plt.yscale('log')
plt.xlim([stokesi['freq'][0], stokesi['freq'][-1]])

print("Generating Waterfall plot")
axWaterfall = plt.axes(rect_waterfall,sharex=axStokesI)
waterfall.plot(add_colorbar=False)
plt.xlabel('')
plt.title(volt)
plt.setp(axWaterfall.get_xticklabels(), visible=False)

print("Generating Time series plot")
axTimeseries = plt.axes(rect_timeseries)
timeseries.plot(y="time")
axTimeseries.yaxis.set_major_formatter(nullfmt)
plt.ylabel('')
plt.ylim([timeseries['time'][-1], timeseries['time'][0]])

if log == True:
    plt.savefig(f"{volt}_log.png")
else:
    plt.savefig(f"{volt}.png")
