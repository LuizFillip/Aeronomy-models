import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import settings as s
from GEO.src.core import coords
import iri2016 as iri




altitudes = np.arange(75, 705, 5)
dates =  pd.date_range("2013-1-1", "2013-12-31", freq = "2D")

def get_ne_profiles(alts, dates):
    out = []
    
    step = alts[1] - alts[0]

    for dn in dates:
    
        glat, glon = coords["saa"]
        
        ds = iri.IRI(
            dn, [min(alts), max(alts), step], 
            glat, glon)
        
        out.append(ds.ne.values)
        
        
    ne = np.array(out)
    
    return ne 



def plot_ne_climatology(ne, dates, altitudes):
    
    fig, ax = plt.subplots(figsize = (8, 5), dpi = 300)

    s.config_labels()

    plt.contourf(
        dates, 
        altitudes, 
        ne.T, 
        40, 
        cmap = "Blues"
        )

    ax.set(ylabel = "Altitude (km)", 
           xlabel = "Meses")

    s.format_axes_date(ax)



