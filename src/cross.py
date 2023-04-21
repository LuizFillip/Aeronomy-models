import pandas as pd
import numpy as np
from models import point_iri, point_msis
from FluxTube import Apex
import datetime as dt
from GEO import limit_hemisphere
from tqdm import tqdm
import json 
from scipy.interpolate import CubicSpline


dn = dt.datetime(2013, 1, 1, 23, 50)
base = 80
step = 1
amin = 90
amax = 500
heights = np.arange(amin, amax + step, step)

out = []


col = "south"

infile = "GEO/src/meridian.json"

dat = json.load(open(infile))

x = np.array(dat["mx"])
y = np.array(dat["my"])

nx = dat["nx"]
ny = dat["ny"]

def interpolate(x, y, points = 30):
         
    spl = CubicSpline(x, y)
    
    new_lon = np.linspace(x[0], x[-1], points)    
    new_lat = spl(new_lon)
    
    return np.round(new_lon, 3), np.round(new_lat, 3)

for h in tqdm(heights, desc = col):

    rlat = Apex(h).apex_lat_base(base = base)
    
    
    glon, glat = limit_hemisphere(
            x, y, nx, ny, 
            np.degrees(rlat), 
            hemisphere = col
            )
    
    lon, lat = interpolate(glon, glat, points = 30)
             
    mlat_range = np.linspace(0, rlat, len(lon))
    
    print(len(lon))     
    for i, mlat in enumerate(mlat_range):
        
        zeq = Apex(h).apex_height(mlat)
        
        #ne, te = get_iri(dn, zeq, glat[i], glon[i])
        # He, O, N2, O2, H, N, Tn = get_msis(
        #     dn, zeq, glat[i], glon[i])
        
        # out.append(
        #     [zeq, h, glat[i], glon[i], 
        #       mlat, He, O, N2, O2, H, N, Tn]
        #     )
        
        





def save_results(col):
        
    cols = ["zeq", "apex", "lat",
            "lon", "mlat", "He", "O", "N2", 
            "O2", "H", "N", "Tn"]

    df = pd.DataFrame(out, columns = cols)

    fname = "msis.txt"
    path_to_save = f"database/FluxTube/profiles/{fname}"
    df.to_csv(path_to_save, index = True)
        
    return df
        
    
