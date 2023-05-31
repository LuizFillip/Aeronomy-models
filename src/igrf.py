# -*- coding: utf-8 -*-
"""
Created on Wed May 31 15:19:06 2023

@author: Luiz
"""

import pyIGRF
import pandas as pd
from GEO import sites


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