import pandas as pd
import numpy as np
import iri2016 as iri
from nrlmsise00 import msise_flat
from PlanetaryIndices.core import get_indices
from FluxTube.src.mag import Apex
import datetime as dt
from scipy.interpolate import CubicSpline

def get_ionos(dn, zeq, glat, glon):
    ds = iri.IRI(dn, [zeq, zeq, 1], glat, glon)
    
    ne = ds["ne"].values[0]
    Te = ds["Te"].values[0]
    return ne, Te

def get_neutrals(dn, zeq, glat, glon):
    
    t = get_indices(dn.date())
     
    res = msise_flat(
        dn, zeq, glat, glon, 
        t.get("F10.7a"), t.get("F10.7obs"), t.get("Ap")
        )
    
    He, O, N2, O2, Ar, mass, H, N, AnO, Tex, Tn = tuple(res)
    
    return He, O, N2, O2, H, N, Tn


def sep_altitudes(df, h):
    
    arr = df.loc[df.index == h]
     
    return arr.lon.values, arr.lat.values

def interpol_coords(df, h, points = 30):
    
    lons, lats = sep_altitudes(df, h)
    
    spl = CubicSpline(lons, lats)

    new_lon = np.linspace(lons[0], lons[-1], points)    
    new_lat = spl(new_lon)
    
    return np.round(new_lon, 3), np.round(new_lat, 3)


def run_models(dn, h, glon, glat, mlat_range):
    
    out = []    
   
         
    return out
     
def save_results(out, name):
    cols = ["zeq", "alt", "lat", "lon", "mlat",
            "ne", "te", "he", "o", "n2", 
            "o2", "h", "n", "tn"]
    
    df = pd.DataFrame(out, columns = cols)
    
    df.to_csv(f"{name}", index = True)
    
    return df
    
dn = dt.datetime(2013, 1, 1, 21, 0)
base = 150

for col in ["south", "north", "both"]:
    
    infile = f"ranges_{col}.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    heights = df.index.unique()
    
    south = []
    north = []
    both = []
    
    for h in heights:
        
        rlat = np.radians(df.loc[df.index == h, "rlat"].unique()[0])
        
        
        if col == "south":
            s, e = 0, -rlat
        elif col == "north":
            s, e = rlat, 0
        else:
            s, e = -rlat, rlat
           
        
        glon, glat = sep_altitudes(df, h)
        mlat_range = np.linspace(s, e, len(glon))
            
        for i, mlat in enumerate(mlat_range):
            
            zeq = Apex(h).apex_height(mlat)
            
            ne, te = get_ionos(dn, zeq, glat[i], glon[i])
            
            He, O, N2, O2, H, N, Tn = get_neutrals(
                dn, zeq, glat[i], glon[i])
            
            vars()[col].append(
                [zeq, h, glat[i], glon[i], 
                 mlat, ne, te, He, O, 
                 N2, O2, H, N, Tn]
                )
    name = infile.replace("ranges", "results")
     
    cols = ["zeq", "alt", "lat", "lon", "mlat",
             "ne", "te", "he", "o", "n2", 
             "o2", "h", "n", "tn"]
     
    df = pd.DataFrame(vars()[col], columns = cols)
     
    df.to_csv(f"{name}", index = True)
     
                
           