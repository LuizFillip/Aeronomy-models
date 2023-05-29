
import matplotlib.pyplot as plt
import FabryPerot as fp
import os
import settings as s
import pandas as pd




def load_hwm(ds, alt = 250, site = "car"):
    infile = "database/HWM/winds_all_sites.txt"
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    idx_cond = ((df.index > ds.index[0]) & 
                (df.index < ds.index[-1]))
    
    sit_cond = (df["site"] == site)
    
    alt_cond = (df["alt"] == alt)

    return df.loc[sit_cond & alt_cond & idx_cond]

import numpy as np

def correct_cycle_slips(phases):
    unwrapped_phases = np.unwrap(phases)
    diff_phases = np.diff(unwrapped_phases)
    cycle_slip_indices = np.where(np.abs(diff_phases) > np.pi)[0] + 1

    for index in cycle_slip_indices:
        diff = unwrapped_phases[index] - unwrapped_phases[index - 1]
        cycles = np.round(diff / (2 * np.pi))
        unwrapped_phases[index:] -= cycles * 2 * np.pi

    return unwrapped_phases


def main():
    # Example phase measurements with cycle slips
    phases = np.array([1.0, 2.0, -3.0, -2.0, 4.0, 5.0, -6.0, -5.0])
    
    # Correct cycle slips
    corrected_phases = correct_cycle_slips(phases)
    
    print("Original Phases:", phases)
    print("Corrected Phases:", corrected_phases)
    def correct_slips():
        path = 'database/FabryPerot/2012/minime01_car_20130316.cedar.005.txt'
        # main()
        ds = fp.FPI(path).wind
    
        shift = df["zon"].diff()