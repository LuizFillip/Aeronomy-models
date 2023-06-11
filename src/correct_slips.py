import matplotlib.pyplot as plt
import numpy as np
import FabryPerot as fp
import models as m
import pandas as pd
import datetime as dt
from common import load


def demonstrated():
    # Example phase measurements with cycle slips
    phases = np.array([1.0, 2.0, -3.0, -2.0, 4.0, 5.0, -6.0, -5.0])
    
    # Correct cycle slips
    corrected_phases = correct_cycle_slips(phases)
    
    plt.plot(phases)
    plt.plot(corrected_phases)
    

path = 'database/FabryPerot/2012/minime01_car_20130318.cedar.005.txt'
tp = fp.FPI(path).temp

def correct_cycle_slips(unwrapped_phases):
    # unwrapped_phases = np.unwrap(phases)
    diff_phases = np.diff(unwrapped_phases)
    cycle_slip_indices = np.where(np.abs(diff_phases) > np.pi)[0] + 1

    for index in cycle_slip_indices:
        diff = unwrapped_phases[index] + unwrapped_phases[index - 1]
        cycles = np.round(diff / (2 * np.pi))
        unwrapped_phases[index:] += cycles * 2 * np.pi

    return unwrapped_phases


# 

fig, ax = plt.subplots()


df = pd.read_csv('test_temp.txt', index_col=0)
df.index = pd.to_datetime(df.index)

# 



vls = df['Tn'].values

diff = np.diff(vls)

threshold = 10
for i, v in enumerate(diff):
    if diff[i] > threshold:
        cycle = (vls[i] - vls[i + 1])
        index = i
print
df['cTn'] = vls


ax.plot(df['cTn'])
ax.plot(df['Tn'])


len(vls), len(diff)