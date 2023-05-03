import pandas as pd
from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
import numpy as np
from utils import save_but_not_show
from Models.src.join_model_results import ds

def plot_grid_wind(
        ax, dn, values, 
        lons, lats, ticks):
    
    vmin = ticks[0] 
    vmax = ticks[-1]
    
    levels = np.linspace(vmin, vmax, 50)
    
    img = ax.contourf(lons, lats, values, 
                      levels = levels,
                      cmap = "rainbow")
    
    s.colorbar_setting(
        img, ax, ticks, 
        label = 'Velocidade zonal (m/s)'
        )
    
    lat_lims = dict(min = -20, 
                    max = 14,
                    stp = 5)

    lon_lims = dict(min = -75, 
                    max = -35, 
                    stp = 10)    
    
    quick_map(ax, lon_lims, lat_lims)
    
    ax.set(title = dn)
    
    return ax, img


def plot_winds_over_map(ds, dn, coord = "zonal"):
    
    vmin = ds[coord].min().round()
    vmax = ds[coord].max().round()
    
    ticks = np.arange(vmin, vmax + 20, 20)
    
    fig, ax = plt.subplots( 
        figsize = (8, 8),
        dpi = 300,
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    t = ds.sel(time = dn)[coord]
    
    ax = plot_grid_wind(ax, dn, t.values, t.lon, t.lat, ticks)
    return fig


def save_plots(ds, coord = "meridional"):
    """
    Running lastly functions and save plots
    """
    for dn in pd.to_datetime(ds.time.values):
        
        fig = plot_winds_over_map(ds, dn, coord = coord)
        
        FigureName = dn.strftime("%Y%m%d%H%M") + ".png"
        save_in = f"D:\\plots\\HWM14\\2013\\{coord}\\{FigureName}"
        
        print("save...", dn)
        
        save_but_not_show(fig, save_in)

save_plots(ds, coord = "zonal")