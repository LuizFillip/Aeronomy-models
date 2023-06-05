import matplotlib.pyplot as plt
import numpy as np
import FabryPerot as fp
import models as m
import pandas as pd
import datetime as dt


def demonstrated():
    # Example phase measurements with cycle slips
    phases = np.array([1.0, 2.0, -3.0, -2.0, 4.0, 5.0, -6.0, -5.0])
    
    # Correct cycle slips
    corrected_phases = correct_cycle_slips(phases)
    
    plt.plot(phases)
    plt.plot(corrected_phases)
    

path = 'database/FabryPerot/2012/minime01_car_20130318.cedar.005.txt'
tp = fp.FPI(path).temp
# ds = m.load_hwm(wd, alt = 250, site = "caj")
dn = dt.datetime(2013, 3, 16, 20)
df = m.timerange_msis(dn, site = "car")


def correct_cycle_slips(phases):
    unwrapped_phases = np.unwrap(phases)
    diff_phases = np.diff(unwrapped_phases)
    cycle_slip_indices = np.where(np.abs(diff_phases) > np.pi)[0] + 1

    for index in cycle_slip_indices:
        diff = unwrapped_phases[index] + unwrapped_phases[index - 1]
        cycles = np.round(diff / (2 * np.pi))
        unwrapped_phases[index:] += cycles * 2 * np.pi

    return unwrapped_phases

#%%
correct =correct_cycle_slips(df["Tn"])

fig, ax = plt.subplots()

ax.plot(df["Tn"])

from common import load
infile = "database/MSIS/cont_msis.txt"

ds = load(
        infile, 
        start = dt.datetime(2013, 3, 16, 20), 
        end = dt.datetime(2013, 3, 17, 7)
        )

ax.plot(ds["Tn"])