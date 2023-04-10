import pandas as pd
import datetime as dt
from GEO.src.mapping import quick_map, limits
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

def plot_grid_wind(ax, df):
    
    
    
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
        label = 'Velocidade zonal (m/s)'
        )
    
    lat_lims = dict(min = -9, 
                    max = -3, 
                    stp = 1)

    lon_lims = dict(min = -40, 
                    max = -34, 
                    stp = 1)    
    
    quick_map(ax, lon_lims, lat_lims)
    
    ax.set(title = dn)
    
    return ax, img
    



out = []
times = [dt.datetime(2013, 1, 1, 21, 0),
           dt.datetime(2013, 1, 2, 0, 0),
           dt.datetime(2013, 1, 2, 3, 0)]
for dn in times:
    df = load_HWM(dn)
    out.append(df.values)
import xarray as xr

lat_lims = dict(min = -9, 
                max = -3, 
                stp = 1)

lon_lims = dict(min = -40, 
                max = -34, 
                stp = 1)   

def create_arange(kargs):           
    l = limits(**kargs)
    return np.arange(l.min, l.max + l.stp, l.stp)

lon = df.columns
lat = df.index



ds = xr.Dataset({"zonal": (["time", "lon", "lat"], out)}, 
                coords = {
                "time": times, 
                "lon": lon, 
                "lat": lat})

g = ds.isel(time = slice(0, 3)).copy()

ax = plt.subplot(projection=ccrs.PlateCarree())


g.plot.pcolormesh(x="lon", y="lat", ax = ax)          
print()

#%%

fig, ax = plt.subplots( 
    ncols = 3, 
    sharex = True, 
    sharey = True, 
    figsize = (12, 10),
    dpi = 300,
    subplot_kw = {'projection': ccrs.PlateCarree()}
    )

plt.subplots_adjust(wspace = 0.5)


for i, ax in enumerate(ax.flat):
    im = ax.imshow(out[i], cmap = "rainbow")
    lat_lims = dict(min = -9, 
                    max = -3, 
                    stp = 1)

    lon_lims = dict(min = -40, 
                    max = -34, 
                    stp = 1)    
    
    quick_map(ax, lon_lims, lat_lims)
    
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(im, cax=cbar_ax)

