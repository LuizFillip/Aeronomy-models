import pyIGRF
import pandas as pd
from GEO import sites, year_fraction


def load_igrf(df, site = "saa"):
   
    lat, lon = sites[site]["coords"]
    
    out = {"D": [], "H": [], "Z": [], 
           "I": [], "F": [], "X": [], 
           "Y": []
           }
    for dn in df.index:
        D, I, H, X, Y, Z, F = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = 0, 
            year = year_fraction(dn)
            )
        
        for key in out.keys():
            out[key].append(vars()[key])
  
    return pd.DataFrame(out, index = df.index)


def run_igrf(df):
    
    dn = pd.to_datetime(df['dn'].values[0])
    
    dec = []
    inc = []
    total = []
    for lat, lon, alt in zip(df.glat, df.glon, df.alt):
        d, i, _, _, _, _, f = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = alt, 
            year = year_fraction(dn)
            )
        
        dec.append(d)
        inc.append(i)
        total.append(f)
        
        
    df["d"] = dec
    df["i"] = inc
    df["Bf"] = total 
    
    df['Bf'] = df['Bf'] * 1e-9
        
    return df