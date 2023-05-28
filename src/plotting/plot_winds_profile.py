import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from atmosphere import effective_wind
import settings as s
# from utils import save_plot
from labels import Labels
import pyIGRF
from GEO import sites, year_fraction

def plot_winds_profiles(
        dn = dt.datetime(2013, 1, 1, 21, 0), 
        site = "São Luis"):
    alt = 300
    lat, lon = sites["saa"]["coords"]
    
    d, i, _, _, _, _, f = pyIGRF.igrf_value(
        lat, 
        lon, 
        alt = alt, 
        year = year_fraction(dn)
        )
    
    infile = "database/HWM/2013_profiles.txt"

    df = pd.read_csv(infile, index_col = 0)

    fig = plt.figure(figsize = (8, 6), dpi = 300)

    ax = fig.add_subplot()

    s.config_labels()

    ax.plot(df[["mer", "zon"]], 
            df.index, 
            label = ["$U_\\theta$ (meridional)", "$U_\phi$ (zonal)"]
            )

    U = effective_wind()
    lbs = Labels().infos
    
    ax.plot(U.zonal(df.zon, df.mer, d), 
            df.index, 
            label = lbs["zon_ef"]["eq"]
            )

    ax.plot(U.meridional(df.zon, df.mer, d, i), 
            df.index, 
            label =  lbs["mer_ef"]["eq"])

    ax.legend(loc = "upper left")


    ax.axvline(0, color = "k", lw = 0.5, linestyle = "--")
    ax.axhline(300)
    dt_str = dn.strftime("%d/%m/%Y")
    
    
    d = round(d, 3)
    i = round(i, 3)
    
    ax.text(-130, 200, f"D = {d}°\nI = {i}°", transform = ax.transData)
    ax.set(
        xlim = [-140, 140], 
        ylim = [100, 500],
        xticks = np.arange(-150, 160, 30),
        title = f"{site} - {dt_str}", 
        ylabel = "Altitude (km)", 
        xlabel = "Velocidade (m/s)"
        )


    return fig

fig = plot_winds_profiles(
        dn = dt.datetime(2013, 1, 1, 21, 0), 
        site = "São Luis"
        )

# save_plot(plot_winds_profiles)