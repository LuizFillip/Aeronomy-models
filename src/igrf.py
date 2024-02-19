import pyIGRF
import pandas as pd
from GEO import sites, year_fraction

def point_igrf(dn, glat, glon, alt):
    
    d, i, _, _, _, _, f = pyIGRF.igrf_value(
        glat, 
        glon, 
        alt = alt, 
        year = gg.year_fraction(dn)
        ) 
    return {'d': d, 'i': i, 'Bf': f * 1e-9}


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

# lat, lon = sites['saa']["coords"]

# D, I, H, X, Y, Z, F = pyIGRF.igrf_value(
#      lat, 
#      lon, 
#      alt = 0, 
#      year = 2013
#      )

# D