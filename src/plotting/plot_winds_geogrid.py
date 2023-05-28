import pandas as pd
from GEO import map_attrs
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
import numpy as np
from utils import save_but_not_show
import matplotlib as mpl







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

# save_plots(ds, coord = "zonal")




def plot_grid_wind(
        ax, dn, values, 
        lons, lats, vmin, vmax):
    

    levels = np.linspace(vmin, vmax, 30)
    
    img = ax.contourf(lons, lats, values, 
                      levels = levels,
                      cmap = "jet")
    
    lat_lims = dict(min = -10, 
                    max = -2,
                    stp = 1)

    lon_lims = dict(min = -45, 
                    max = -35, 
                    stp = 1)    
    
    map_attrs(ax, lon_lims, lat_lims)
    
    ax.set(title = dn)
    
    return ax, img


infile = "database/HWM/grid_winds_20130101.txt"

def set_data(infile, coord = "mer"):
    
    ds = pd.read_csv(infile, index_col = 0)
    
    
    ds = ds.loc[(ds["lat"] <= -2) &
                (ds["lat"] >= -10) &
                (ds["lon"] >= -45) & 
                (ds["lon"] <= -35)]

    vmin = round(ds[coord].min())
    vmax = round(ds[coord].max())
    return ds, vmin, vmax

def plot_winds_over_map(infile, coord = "zon"):

    fig, ax = plt.subplots( 
        figsize = (12, 12),
        dpi = 300, 
        ncols = 2,
        nrows = 2,
        sharex= True, sharey=True, 
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    plt.subplots_adjust(hspace = 0., wspace = 0.2)
    
    
    
    ds, vmin, vmax =  set_data(infile, coord = coord)
    
    times = ds["time"].unique()
    
    for num, ax in enumerate(ax.flat):
                
        ds1 = ds.loc[(ds["time"] == times[num])]
        
        df = pd.pivot_table(
            ds1, 
            values = coord, 
            index = "lat", 
            columns = "lon"
            )
        
        plot_grid_wind(
                ax, times[num], df.values, 
                df.columns, df.index, 
                vmin, vmax
                )
        
        
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cax = plt.axes([0.95, 0.15, 0.03, 0.68])
    
    if coord == "zon":
        label = "Velocidade zonal (m/s)"
    else:
        label = "Velocidade meridional (m/s)"
    fig.colorbar(
        mpl.cm.ScalarMappable(norm = norm, cmap = "rainbow"),
             label = label, cax = cax)
    
    return fig

fig = plot_winds_over_map(infile, coord = "zon")