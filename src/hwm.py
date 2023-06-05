
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

