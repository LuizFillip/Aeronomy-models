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

def interpol_coords(df, h, points = 50):
    
    lons, lats = sep_altitudes(df, h)
    
    spl = CubicSpline(lons, lats)

    range_lon = np.linspace(lons[0], lons[-1], points)    
    return range_lon, spl(range_lon)

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
    



def run_in_apex(
        infile, 
        dn = dt.datetime(2013, 1, 1, 21, 0), 
        base = 150, 
        points = 50
        ):
    
    df = pd.read_csv(infile, index_col = 0)

    heights = df.index.unique()

    out = []
    
    for h in heights:
        
        glon, glat = interpol_coords(df, h, points = points)
        
        max_lat = Apex(h).apex_lat_base(base = base)
                
        mlat_range = np.linspace(0, max_lat, points)
    
        print("process...", h) 
        for i, mlat in enumerate(mlat_range):
             
             zeq = Apex(h).apex_height(mlat)
     
             ne, te = get_ionos(dn, zeq, glat[i], glon[i])
             
             He, O, N2, O2, H, N, Tn = get_neutrals(
                 dn, zeq, glat[i], glon[i])
             
             out.append([zeq, h, glat[i], glon[i], 
                         mlat, ne, te, He, O, 
                         N2, O2, H, N, Tn])
         
        
    name = infile.replace("ranges", "results")
    
    cols = ["zeq", "alt", "lat", "lon", "mlat",
            "ne", "te", "he", "o", "n2", 
            "o2", "h", "n", "tn"]
    
    df = pd.DataFrame(out, columns = cols)
    
    df.to_csv(f"{name}", index = True)
    
    return df



infile = "ranges_north.txt"

run_in_apex(
        infile, 
        dn = dt.datetime(2013, 1, 1, 21, 0), 
        base = 150, 
        points = 50
        )