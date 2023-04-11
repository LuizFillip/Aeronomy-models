import os
import pandas as pd
import xarray as xr
import numpy as np


infile = "D:\\venv\\venv\\WSL\\data\\hwm2014\\"


def load(infile, coord = "zon"):

    df = pd.read_csv(infile, index_col = 0)
    return pd.pivot_table(df, values = coord, columns = "lon", index = "lat")


def get_coords_grid(infile):
    files = os.listdir(infile)
    
    zon = []
    mer = []
    
    for filename in files:
        
        for coord in ["zon", "mer"]:
            vars()[coord].append(
                load(os.path.join(infile, filename),
                     coord = coord).values)
    
    return np.array(zon),  np.array(mer)

zon, mer = get_coords_grid(infile)


def save_in_dataset(zon, mer):

    lats = np.arange(-20, 20, 1)
    lons = np.arange(-75, -25, 1)
    
    times = pd.date_range("2013-1-1 00:00", "2013-1-1 23:50", freq = "10min")
    
    ds = xr.Dataset(
        {
         "zonal": (["time", "lat", "lon"], zon), 
         "meridional":(["time", "lat", "lon"], mer),
             }, 
        coords = {
            "time": times,
            "lon": lons,
            "lat": lats
                        })
    
    return ds

ds = save_in_dataset(zon, mer)
