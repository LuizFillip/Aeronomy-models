from GEO import sites
import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
from indices import get_indices
import datetime as dt
import models as mm


def point_msis(dn, zeq, glat, glon):
    
    """
    densities: list of floats
    		0. He number density [cm^-3]
    		1. O number density [cm^-3]
    		2. N2 number density [cm^-3]
    		3. O2 number density [cm^-3]
    		4. AR number density [cm^-3]
    		5. total mass density [g cm^-3] 
    		6. H number density [cm^-3]
    		7. N number density [cm^-3]
    		8. Anomalous oxygen number density [cm^-3]
        peratures: list of floats
    		0. Exospheric temperature [K]
    		1. Temperature at `alt` [K]

    """
    
    t = get_indices(dn.date())
    
    res = msise_flat(
       dn, zeq, glat, glon, 
       t.get("F10.7a"), t.get("F10.7obs"), t.get("Ap")
       )

    names = ["He", "O", "N2", "O2", "Ar", "mass", 
            "H", "N", "AnO", "Tex", "Tn"]

    return {key: value for key, value in zip(names, res)}


def altrange_msis(
       dn: dt.datetime,
       glat: float, 
       glon: float,
       hmin: float = 200.0, 
       hmax: float = 500.0, 
       step: float = 1.0
       ):
    
    alts = np.arange(hmin, hmax + step, step)
     
    t = get_indices(dn.date())
    
    res = msise_flat(dn, alts[None, :], 
                     glat, glon, 
                     t.get("F10.7a"), 
                     t.get("F10.7obs"), 
                     t.get("Ap"))
    
    columns = ["He", "O", "N2", "O2", "Ar", 
              "mass", "H", "N", "AnO", "Tex", "Tn"]
    
    df = pd.DataFrame(res[0], index = alts, 
                      columns = columns)
        
    df.drop(["Ar", "mass", "N", "AnO", "Tex"], 
            axis = 1, 
            inplace = True)
    
    return df




def timerange_msis(
        dn, 
        site = "car", 
        altitude = 300, 
        periods = 67, 
        parameter = "Tn", 
        correct = True):
    
    glat, glon = sites[site]["coords"]
        
    out = {'Tn' : [], 
           'O': [], 
           'O2': [], 
           'N2': [], 
           }
    times =  pd.date_range(
            dn, 
            periods = periods, 
            freq = "10min"
            )
    for dn in times:
        
        ts = point_msis(dn, altitude, glat, glon)
        for key in out.keys():
            out[key].append(ts[key])
            
    df = pd.DataFrame(out, index = times)
    
    if correct:
        for col in df.columns:
            df[col] = mm.correct_and_smooth(df[col])
    
    return df
