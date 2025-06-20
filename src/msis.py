from GEO import sites
import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
from indices import GFZ
import datetime as dt
import models as mm
from tqdm import tqdm 



def altrange_msis(
       dn: dt.datetime,
       glat: float, 
       glon: float,
       hmin: float = 200.0, 
       hmax: float = 500.0, 
       step: float = 1.0
       ):
    
    alts = np.arange(hmin, hmax + step, step)
     
    ind = GFZ(dn)
    
    f107a = ind.get('F10.7a')
    f107o = ind.get("F10.7obs")
    ap = ind.get("Ap")
    
    res = msise_flat(
        dn, 
        alts[None, :], 
        glat, glon, 
        f107a, 
        f107o, 
        ap
        )
    
    columns = ["He", "O", "N2", "O2", "Ar", 
              "mass", "H", "N", "AnO", "Tex", "Tn"]
    
    df = pd.DataFrame(
        res[0], 
        index = alts, 
        columns = columns
        )
        
    df.drop(["Ar", "mass", "N", "AnO", "Tex"], 
            axis = 1, 
            inplace = True)
    
    return df




def timerange_msis(
        times, 
        site = "car", 
        altitude = 300, 
        correct = True):
    
    glat, glon = sites[site]["coords"]
        
    out = []
   
    for dn in tqdm(times):
        
        ts = pd.DataFrame(
            mm.point_msis(dn, altitude, glat, glon),
            index = [dn]
            )
        
        out.append(ts)
  

    return  pd.concat(out)



def test_timerange_msis():
    
    times = pd.date_range(
        '2015-12-19', 
        '2015-12-23', 
        freq = '10min'
        )
    
    df = timerange_msis(times, site = "saa")
    
    df.to_csv('msis250')
    
    
    