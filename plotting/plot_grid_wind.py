import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from GEO.mapping import quick_map
import cartopy.crs as ccrs
import setup as s
import numpy as np

def load_HWM():

    infile = "database/HWM/grid_winds_20130101.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df["time"] = pd.to_datetime(df["time"])
    
    dn = dt.datetime(2013, 1, 1, 21, 0)
    
    df = df.loc[df["time"] == dn, 
                ["lat", "lon", "zon"]]
    
    df = df.loc[(df["lat"] >= -10) &
                (df["lat"] <= -3) &
                (df["lon"] >= -40) &
                (df["lon"] <= -32)]
    
    return pd.pivot_table(
        df, 
        values = "zon", 
        columns = "lon", 
        index = "lat")

def plot_grid_wind():
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    df = load_HWM()
    
    img = ax.contourf(df.columns, 
                 df.index, 
                 df.values, 
                 20, 
                 cmap = "rainbow")
    
    vmin = round(np.min(df.values))
    vmax = round(np.max(df.values))
    
    ticks = np.arange(vmin, vmax, 5)
    
    s.colorbar_setting(
        img, ax, ticks, 
        label = 'Velocidade zonal (m/s)')
    
    quick_map(ax)
    
plot_grid_wind()
