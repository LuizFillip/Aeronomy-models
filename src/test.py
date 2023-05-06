# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:45:00 2023

@author: Luiz
"""

def main():
    infile = "database/FluxTube/profiles/north_results_E2.txt"
    
        
    df = pd.read_csv(infile, index_col = 0)
    
    alts = df["apex"].unique()
    apex = 510
    base = 80
    rlat = Apex(apex).apex_lat_base(base = base)
    nx, ny, x, y = load_meridian()
    
    lon, lat = sep_meridian(
            rlat,
            hemisphere = "north"
            )
    
    mlat_range = np.linspace(rlat, 0, len(lon))
    for i, mlat in enumerate(mlat_range):
        print(lat[i], lon[i],  mlat, np.rad2deg(mlat))
    
