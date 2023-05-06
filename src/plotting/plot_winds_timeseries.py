import pandas as pd
import datetime as dt
import settings as s
from atmosphere import effective_wind
from models import altrange_iri
from GEO import sites 

dn = dt.datetime()
df = altrange_iri()



def plot_meridional(
        ax, 
        df, 
        **kargs
        ):
    
    U = effective_wind()
            
    d, i = -19.6, -6
    
    Ux = U.eff_meridional(df.zon, df.mer, d, i)
    
    d, i = round(d, 2), round(i, 2)
    
    eq = r"$U_x = (U_\theta \cos D + U_\phi \sin D)\cos I$"
    
    ax.plot(Ux, 
            label = f"{eq}\nD = {d}°, I = {i}°", 
            lw = 2, 
            color = "k"
            )
    ax.legend(loc = "upper right")
             
    ax.set(
        ylabel = "$U_y^{ef}$ (m/s)", 
        ylim = [-100, 100]
        )
    
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 1
        )
    return Ux 
