import matplotlib.pyplot as plt
from models import altrange_iri
import ionosphere as io
import datetime as dt
from GEO import sites
from labels import Labels


def plot_scale_gradient(
        ax, ds
        ):

    lbs = Labels().infos["L"]
    
    ax.plot(ds["L"], ds.index, color = "k", lw = 1)
    ax.axvline(0, linestyle = "--")
    ax.axhline(300, linestyle = "--")
    
    ax.set(
        title = lbs["name"],
        xlabel = (f"{lbs['symbol']} ({lbs['units']})")
        )

def plot_electron_density(ax, df):
       
    ax.plot(df["ne"], df.index, color = "k", lw = 1)
    lbs = Labels().infos["ne"]
    ax.set(
       title = lbs["name"],
       xlabel = (f"{lbs['symbol']} ({lbs['units']})")
       )
    
    ax.axhline(300, linestyle = "--")


def plot_ne_grad_profiles():
    
    dn = dt.datetime(2013, 1, 1, 21, 0)
    lat, lon = sites["saa"]["coords"]
    
    ds = altrange_iri(
        dn, 
        hmin = 150, 
        glat = lat, 
        glon = lon
        )
    
    ds["L"] = io.scale_gradient(ds["ne"])
    
    fig, ax = plt.subplots(
        figsize = (8, 6), 
        ncols = 2,
        dpi = 300, 
        sharey = True
        )
    
    plt.subplots_adjust(wspace = 0.05)
    plot_electron_density(ax[0], ds)
    plot_scale_gradient(ax[1], ds)
    
    return fig
    
fig = plot_ne_grad_profiles()