from GEO import sites
import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
from PlanetaryIndices import get_indices
import datetime as dt

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
    
    He, O, N2, O2, Ar, mass, H, N, AnO, Tex, Tn = tuple(res)
    
    return He, O, N2, O2, H, N, Tn


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
        glat, glon, 
        altitude = 300, 
        periods = 67):
        
    out = []
    for dn in pd.date_range(
            dn, 
            glat, glon,
            periods = periods, 
            freq = "10min"
            ):
        
        ts = point_msis(dn, altitude, glat, glon)
        
        ts.index = [dn]
        out.append(ts)
    
    return pd.concat(out)

def main():
    site = "saa"
    glat, glon = sites[site]["coords"]
    dn = dt.datetime(2013, 1, 1)
    
    df =  altrange_msis(
            dn,
            glat, 
            glon,
            hmin = 200, 
            hmax = 500, 
            step = 1, 
            )
    
    df
    
    
def con_from_point(
        tn, 
        o_point, 
        o2_point, 
        n2_point, 
        step,  
        base_height = 200.0 
        ):
    
    """
    Get concetrantions profiles from neutral constituints 
    from point
    """

    CO = np.zeros(len(tn))
    CO2 = np.zeros(len(tn))                
    CN2 = np.zeros(len(tn))                

    
    for i in range(0, len(tn)):
        
        Z1 = base_height + step * i
        
        GR = 1.0 / pow(1.0 + Z1 / 6370.0, 2)
        
        HO = 0.0528 * tn[i] / GR                               # scale height of O [km]
        HO2 = 0.0264 * tn[i] / GR                              # scale height of O2 [km]
        HN2 = 0.0302 * tn[i] / GR                              # scale height of N2 [km]

        p_co = o_point / 5.33 * 8.55
        p_co2 = o2_point / 1.67 * 4.44
        p_cn2 = n2_point / 9.67 * 2.26

        CO[i] = p_co * np.exp(-(Z1 - 335.0) / HO)           # atomic oxygen [cm-3]
        CO2[i] = p_co2 * np.exp(-(Z1 - 335.0) / HO2)        # molecular oxygen [cm-3]
        CN2[i] = p_cn2 * np.exp(-(Z1 - 335.0) / HN2) 
    
    return CO, CO2, CN2