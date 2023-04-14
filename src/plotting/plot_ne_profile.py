import pandas as pd
import datetime as dt
import settings as s
from GEO.src.mapping import quick_map
from GEO.src.plotting.plot_apex_range_over_meridian import plot_site_and_closest_meridian
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from Models.src.load_results import load
from Models.src.core import sites

import os
from GEO.src.terminator import terminator

p_labels = {"o": "$O$ ($cm^{-3}$)", 
            "ne": "$Ne$ ($m^{-3}$)", 
            "te": "Temperatura eletrônica ($K$)", 
            "tn": "Temperatura ($K$)", 
            "perd": "$\sigma_P$ (ohms)", 
            "hall": "$\sigma_H$ (ohms)"}
  

def datetime_from_fn(infile):
    fname = os.path.split(infile)[-1]
    
    dn = fname.replace(".txt", "")
    try:
        dn = fname.replace(".txt", "")
        return  dt.datetime.strptime(dn, "%Y%m%d%H%M")
    except:
        dn = fname.replace(".txt", "")[:-1]
        return dt.datetime.strptime(dn, "%Y%m%d%H%M")
   

def plot_terminator(ax, dn):
    tlon, tlat = terminator(dn, 18)
    
    ax.plot(tlon, tlat, lw = 2, 
            linestyle = "--", color = "white")

def plot_contours(ax, df, parameter):
    img = ax.contourf(df.columns, df.index, 
        df.values, 50, cmap = "rainbow")
    
    vls = df.values.flatten()
    
    ticks = np.linspace(min(vls), max(vls), 10)
    
    p  = parameter.lower()
    s.colorbar_setting(img, ax, ticks, 
                       label = p_labels[p])
    
def plot_ne_geogrid(infile, parameter = "Tn"):
    
    dn = datetime_from_fn(infile)
    
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        dpi = 300, 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    s.config_labels(fontsize = 15)
    
    lat_lims = dict(min = -20, max = 15, stp = 5)
    lon_lims = dict(min = -75, max = -30, stp = 5)    
    
    quick_map(ax, lon_lims, lat_lims)
    
    s.config_labels()
    
    
    df = load(infile, coord = parameter)
    
    plot_contours(ax, df, parameter = parameter)
    
    plot_terminator(ax, dn)
    
    plot_site_and_closest_meridian(
            ax, 
            site = "saa")
    
    ax.set(title = f"{dn} - 300 km")
    
    ax.legend()
    return fig


#infile = "WSL/data/iri2016/201301010000.txt"
infile = "2013010100002.txt"
parameter = "hall"
plot_ne_geogrid(infile, parameter = parameter)

# df = load(infile, coord = parameter)
# vls = df.values.flatten()
# ticks = np.linspace(round(min(vls)), round(max(vls)), 10)

# ticks

