import pandas as pd
import numpy as np
import iri2016 as iri
from Base.src.iono import collision_frequencies, conductivity
from nrlmsise00 import msise_flat
from PlanetaryIndices.core import get_indices
from FluxTube.src.mag import Apex
import datetime as dt
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def get_ne_te(dn, zeq, glat, glon):
    ds = iri.IRI(dn, [zeq, zeq, 1], glat, glon)
    
    ne = ds["ne"].values[0]
    Te = ds["Te"].values[0]
    return ne, Te

def run_models(dn, zeq, glat, glon):
    
    t = get_indices(dn.date())
    
    
    ds = iri.IRI(dn, [zeq, zeq, 1], glat, glon)
    
    ne = ds["ne"].values[0]
    Te = ds["Te"].values[0]
    
    res = msise_flat(
        dn, zeq, glat, glon, 
        t.get("F10.7a"), t.get("F10.7obs"), t.get("Ap")
        )
    

    nu = collision_frequencies()
    nue = nu.electrons_neutrals(
            res[1], res[3], res[2], 
            res[0], res[6], Te
            )
    nui = nu.ion_neutrals(
        res[1], res[3], 
        res[2], res[-1]
        )
         
    cond = conductivity(ne, nue, nui)
    


def get_and_interpol(df, h, points = 50):
    
    arr = df.loc[df.index == h]
    
    lons = arr.lon.values
    lats = arr.lat.values
    
    spl = CubicSpline(lons, lats)

    range_lon = np.linspace(lons[0], lons[-1], points)    
    return range_lon, spl(range_lon)




df = pd.read_csv("test2.txt", index_col = 0)

apex_heights = df.index.unique()


base = 150
dn = dt.datetime(2013, 1, 1, 21, 0)

out = {
    "ne": [], 
    "Te": [], #  "hall" : [],     "mlat": []
    "alts": [], 
    "lats": [], 
    "lons": [],
       }

points = 50

for h in apex_heights:
    
    glon, glat = get_and_interpol(df, h, points = points)
    
    mlat = Apex(h).apex_lat_base(base = base)
    
    for i in range(points):
        
        zeq = Apex(h).apex_height(mlat)
        
        ne, te = get_ne_te(dn, zeq, glat[i], glon[i])
        
    

    
