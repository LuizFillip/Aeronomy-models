import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Base.src.winds import effective_wind
from GEO.src.core import run_igrf
import settings as s
from utils import save_plot

    

def plot_winds_profiles(
        dn = dt.datetime(2013, 1, 1, 21, 0), 
        site = "São Luis"):
    
    d, i = run_igrf(date = dn.year, 
                    site = "saa", 
                    alt = 300)
    
    infile = "database/HWM/2013_profiles.txt"

    df = pd.read_csv(infile, index_col = 0)

    fig = plt.figure(figsize = (6, 4), dpi = 300)

    ax = fig.add_subplot()

    s.config_labels()

    ax.plot(df[["mer", "zon"]], 
            df.index, 
            label = 
            ["$U_\\theta$ (meridional)", 
             "$U_\phi$ (zonal)"]
            )

    U = effective_wind()

    ax.plot(U.eff_zonal(df.zon, df.mer, d), 
            df.index, 
            label = "$U_y^{Ef} = U_\phi \cos D + U_{\\theta} \sin D$")

    ax.plot(U.eff_meridional(df.zon, df.mer, d, i), 
            df.index, 
            label = "$U_x^{Ef} = (U_{\\theta} \cos D + U_\phi \sin D) \cos I$")

    ax.legend(loc = "upper left")


    ax.axvline(0, color = "k", lw = 0.5, linestyle = "--")

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

    plt.show()

    return fig

# fig = plot_winds_profiles(
#         dn = dt.datetime(2013, 1, 1, 21, 0), 
#         site = "São Luis")

save_plot(plot_winds_profiles)