import pandas as pd

import datetime as dt
from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
import numpy as np

def load_HWM(dn):

    infile = "database/HWM/grid_winds_20130101.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df["time"] = pd.to_datetime(df["time"])
    
    df = df.loc[df["time"] == dn, 
                ["lat", "lon", "zon"]]
    
    df = df.loc[(df["lat"] >= -9) &
                (df["lat"] <= -3) &
                (df["lon"] >= -40) &
                (df["lon"] <= -34)]
    
    return pd.pivot_table(
        df, 
        values = "zon", 
        columns = "lon", 
        index = "lat")

def plot_grid_wind(dn):
    
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    df = load_HWM(dn)
    
    img = ax.contourf(df.columns, 
                 df.index, 
                 df.values, 
                 20, 
                 cmap = "rainbow")
    
    vmin = round(np.min(df.values))
    vmax = round(np.max(df.values))
    
    ticks = np.arange(vmin, vmax + 4, 2)
    
    s.colorbar_setting(
        img, ax, ticks, 
        label = 'Velocidade zonal (m/s)')
    
    lat_lims = dict(min = -9, 
                    max = -3, 
                    stp = 1)

    lon_lims = dict(min = -40, 
                    max = -34, 
                    stp = 1)    
    
    quick_map(ax, lon_lims, lat_lims)
    
    ax.set(title = dn)
    
dn = dt.datetime(2013, 1, 2, 3, 0)
plot_grid_wind(dn)
