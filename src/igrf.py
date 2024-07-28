import pyIGRF
import pandas as pd
import GEO as gg



def load_igrf(df, site = "saa"):
   
    lat, lon = gg.sites[site]["coords"]
    
    out = {"D": [], "H": [], "Z": [], 
           "I": [], "F": [], "X": [], 
           "Y": []
           }
    for dn in df.index:
        D, I, H, X, Y, Z, F = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = 0, 
            year = gg.year_fraction(dn)
            )
        
        for key in out.keys():
            out[key].append(vars()[key])
  
    return pd.DataFrame(out, index = df.index)

