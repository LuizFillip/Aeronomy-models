import pandas as pd
import GEO as g
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
import numpy as np
import matplotlib as mpl
import datetime as dt


def plot_grid(
        ax, 
        ds, 
        time, 
        coord = "mer",
        cmap = "rainbow"):
    
    ds = ds.loc[ds["dn"] == time]
  
    df = pd.pivot_table(
        ds, 
        values = coord, 
        index = "lat", 
        columns = "lon"
        )
    
    vmin = round(ds[coord].min())
    vmax = round(ds[coord].max())
    
    levels = np.linspace(vmin, vmax, 30)
    
    ax.contourf(
        df.columns,
        df.index, 
        df.values, 
        levels = levels,
        cmap = cmap
        )
    
    
    ax.set(title = time.strftime("%d/%m %H:%M"))
    
    return ax
    
    
def plot_colorbar(
        fig,
        vmin, 
        vmax, 
        coord = "mer", 
        rainbow = "rainbow",
        fontsize = 40
        ):
    
    norm = mpl.colors.Normalize(
        vmin = vmin, vmax=vmax
        )
   
    cax = plt.axes([0.2, 1.001, 0.6, 0.02])
    
    if coord == "zon":
        label = "Velocidade zonal (m/s)"
    else:
        label = "Velocidade meridional (m/s)"
        
    cb = fig.colorbar(
        mpl.cm.ScalarMappable(
            norm = norm, 
            cmap = rainbow
            ),
        ticks = np.arange(vmin, vmax, 10),
        label = label, 
        cax = cax, 
        orientation = "horizontal", 
        )
    cb.set_label(label, fontsize = fontsize)



def plot_winds_geogrid(
        ds, 
        coord = "mer", 
        fontsize = 40
        ):
    
    fig, ax = plt.subplots( 
          figsize = (20, 15),
          dpi = 300, 
          ncols = 5, 
          nrows = 3,
          sharex= True, 
          sharey=True, 
          subplot_kw = {'projection': ccrs.PlateCarree()}
          )
    
    plt.subplots_adjust(hspace = 0.2, wspace = 0.001)
    
    vmin = round(ds[coord].min())
    vmax = round(ds[coord].max())
    
    vlats = dict(min = -30, max = 10, stp = 5)
    vlons = dict(min = -60, max = -30, stp = 5)   
    
    delta = dt.timedelta(hours = 4)
    
    for row, day in enumerate([16, 17, 18]):
        
        dn = dt.datetime(2013, 3, day, 22, 0)
        times = pd.date_range(dn, dn + delta, freq = "1H")
        
        for col, time in enumerate(times):
            
            plot_grid(
                ax[row, col], 
                ds, 
                time
                )
            g.mag_equator(ax[row, col])
            g.map_features(ax[row, col])
    
            
            ax[row, col].set(
                ylim = [vlats['min'], vlats['max']], 
                xlim = [vlons['min'], vlons['max']]
                )
            
        ax[row, 0].set(
            xticks = np.arange(
                vlons['min'], vlons['max'] + 10, 10
                ), 
            yticks = np.arange(
                vlats['min'], vlats['max'] + 10, 10
                )
            )
            
    s.config_labels(fontsize = 20)
    plot_colorbar(fig, vmin, vmax, coord = coord)
    
    
    fig.text(.07, 0.43, "Latitude (°)", 
             rotation = "vertical", fontsize = fontsize)
    fig.text(.43, 0.07, "Longitude (°)", 
             fontsize = fontsize)
    
    plt.show()
    
    return fig

infile = "database/HWM/grid_2013_03.txt"
ds = pd.read_csv(infile)

ds["dn"] = pd.to_datetime(ds["dn"])

f = plot_winds_geogrid(ds, coord = "mer", 
                       fontsize = 40)

f.savefig("models/figures/windsgrid.png", dpi = 300)
