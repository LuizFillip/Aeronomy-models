from GEO.src.core import coords
import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
from PlanetaryIndices.core import get_indices

def run_msise(
        datetime, 
        hmin = 200, 
        hmax = 500, 
        step = 1, 
        site = "saa"
        ):
    
    glat, glon = coords[site]
    
    """Running models MSISE00"""
    
    alts = np.arange(hmin, hmax + step, step)
     
    t = get_indices(datetime.date())
    
    res = msise_flat(datetime, alts[None, :], 
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



def timerange_MSISE(
        dn, 
        fixed_alt = 300, 
        periods = 67):
        
    out = []
    for dn in pd.date_range(
            dn, 
            periods = periods, 
            freq = "10min"
            ):
        
        ts = run_msise(dn, hmin = fixed_alt, hmax = fixed_alt)
        
        ts.index = [dn]
        # ts["R"] = R(ts.O2,  ts.N2)
        # ts["nu"] = nui(ts.Tn, ts.O, ts.O2,  ts.N2)
        out.append(ts)
    
    return pd.concat(out)