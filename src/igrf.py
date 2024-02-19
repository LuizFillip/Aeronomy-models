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


def magnetic_parameters(df):
    
    try:
        dn = df['dn'].values[0]
    except:
        dn = df.index[0]
        
    dn = pd.to_datetime(dn)
    
    dec = []
    inc = []
    total = []
    for lat, lon, alt in zip(df.glat, df.glon, df.alt):
        d, i, _, _, _, _, f = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = alt, 
            year = gg.year_fraction(dn)
            )
        
        dec.append(d)
        inc.append(i)
        total.append(f)
        
        
    df["d"] = dec
    df["i"] = inc
    df["Bf"] = total 
    
    df['Bf'] = df['Bf'] * 1e-9
        
    return df
