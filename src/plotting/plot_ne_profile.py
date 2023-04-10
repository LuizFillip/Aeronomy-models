import pandas as pd
import datetime as dt
import settings as s
from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(
    figsize = (8, 8), 
    dpi = 300, 
    subplot_kw = 
    {'projection': ccrs.PlateCarree()}
    )

s.config_labels(fontsize = 15)

lat_lims = dict(min = -20, max = 15, stp = 5)
lon_lims = dict(min = -75, max = -40, stp = 10)    

quick_map(ax, lon_lims, lat_lims)

s.config_labels()

dn = dt.datetime(2013, 1, 1, 21, 0)

infile = "WSL/ne.txt"

def pivot_table(infile):
    df = pd.read_csv(infile, index_col = 0)
    
    return pd.pivot(df, columns = "1", index = "0", values = "2")

def plot_contours(df):
    img = ax.contourf(
        df.columns, 
        df.index, 
        df.values, 50, cmap = "rainbow")
    
    vls = df.values.flatten()
    ticks = np.linspace(min(vls), max(vls), 10)
    
    s.colorbar_setting(img, ax, ticks, label = 'Ne ($cm^{-3}$)')