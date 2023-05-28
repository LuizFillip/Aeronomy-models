# -*- coding: utf-8 -*-
"""
Created on Sun May 28 19:24:04 2023

@author: Luiz
"""

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


def correct_slips():
    path = 'database/FabryPerot/2012/minime01_car_20130316.cedar.005.txt'
    # main()
    ds = fp.FPI(path).wind

    shift = df["zon"].diff()