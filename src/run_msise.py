from GEO.src.core import sites
import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
from PlanetaryIndices.core import get_indices

site = "saa"
glat, glon = sites[site]["coords"]


def run_msise(
        dn,
        glat, 
        glon,
        hmin = 200, 
        hmax = 500, 
        step = 1, 
        ):
    
    
    """
    Running models MSISE00
    
    densities: list of floats
	
    	0. He number density [cm^-3]
		1. O number density [cm^-3]
		2. N2 number density [cm^-3]
		3. O2 number density [cm^-3]
		4. AR number density [cm^-3]
		5. total mass density [g cm^-3] (includes d[8] in gtd7d)
		6. H number density [cm^-3]
		7. N number density [cm^-3]
		8. Anomalous oxygen number density [cm^-3]
            peratures: list of floats
		0. Exospheric temperature [K]
		1. Temperature at `alt` [K]
    
    """
    
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
        
        ts = run_msise(
            dn, 
            hmin = fixed_alt, 
            hmax = fixed_alt)
        
        ts.index = [dn]
        out.append(ts)
    
    return pd.concat(out)