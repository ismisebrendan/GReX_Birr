import blimpy as bl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import os

#
# Plots a waterfall plot, Stokes I and time series plot for a filterbank file from GReX using the default file structure
#


# Import data
grex_fil = None

filterbank_files = [f[:20] for f in os.listdir("/hdd/data/filterbanks") if os.path.isfile(os.path.join("/hdd/data/filterbanks/", f)) and f[-4:] == ".fil"]

while grex_fil == None:
    file = input("Name of a filterbank file to process: ")

    if file[-4:] == ".fil":
        file = file[:-4]

    if file in filterbank_files:
        grex_fil = file
        break
    else:
        print("Please choose a filterbank file in /hdd/data/filterbanks/")

obs = bl.Waterfall(f'/hdd/data/filterbanks/{grex_fil}.fil')

logged = None

while logged == None:
    log = input("Take log of the values? [Y/N]")

    if log.upper()[0] == "Y":
        logged = True
        break
    elif log.upper()[0] == "N":
        logged = False
        break

# Plot locations
left, width = 0.1, 0.7
left2 = left + width + 0.05
bottom, height = 0.3, 0.65
width2, height2 = 0.2, 0.2
bottom2 = bottom - height2

rect_waterfall = [left, bottom, width, height]
rect_spectrum = [left, bottom2, width, height2]
rect_timeseries = [left + width, bottom, width2, height]

nullfmt = NullFormatter()

# Plots
axSpectrum = plt.axes(rect_spectrum)
print('Plotting Spectrum')
obs.plot_spectrum(logged=logged)
plt.title('')
plt.legend(bbox_to_anchor=(1, 0.5))

axWaterfall = plt.axes(rect_waterfall,sharex=axSpectrum)
print('Plotting Waterfall')
obs.plot_waterfall(logged=logged, cb=False)
plt.xlabel('')
plt.title(grex_fil)
plt.setp(axWaterfall.get_xticklabels(), visible=False)

axTimeseries = plt.axes(rect_timeseries)
print('Plotting Timeseries')
obs.plot_time_series(orientation='v')
axTimeseries.yaxis.set_major_formatter(nullfmt)

if logged == False:
    plt.savefig(f'{grex_fil}.png')
else:
    plt.savefig(f'{grex_fil}_log.png')
