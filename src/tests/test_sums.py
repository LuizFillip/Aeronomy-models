import pandas as pd
from FluxTube.src.core import get_conductivities
from scipy.interpolate import CubicSpline
import numpy as np


def test_sum_perd():
    for col in ["south", "north", "both"]:
        
        infile = f"results_{col}.txt"
        
        df = pd.read_csv(infile, index_col = 0)
        
        hs = df.alt.unique()
        
        df1 = df.loc[df["alt"] == hs[0]]
            
        hall, perd = get_conductivities(df1)
        

    

def sep_altitudes(df, h):
    
    arr = df.loc[df.index == h]
     
    return arr.lon.values, arr.lat.values

def interpol_coords(df, h, points = 30):
    
    lons, lats = sep_altitudes(df, h)
    
    spl = CubicSpline(lons, lats)

    new_lon = np.linspace(lons[0], lons[-1], points)    
    new_lat = spl(new_lon)
    return np.round(new_lon, 3), np.round(new_lat, 3)

import iri2016 as iri


h = 500

# for col in ["south", "north", "both"]:
col = "both"
    
infile = f"ranges_{col}.txt"

df = pd.read_csv(infile, index_col = 0)

#df1 = df.loc[df.index == 300]
lon, lat = interpol_coords(df, h, points = 30)

print(lon, lat)