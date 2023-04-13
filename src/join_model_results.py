import os
import pandas as pd
import xarray as xr
import numpy as np
from Models.src.utils import (sel_columns,  
                              create_dict,  
                              convert_to_array)



def load(infile, coord = "zon"):

    df = pd.read_csv(infile, index_col = 0)
    return pd.pivot_table(
        df, 
        values = coord, 
        columns = "lon", 
        index = "lat"
        )


def parameters_into_dict(infile):
    
    files = os.listdir(infile)

    chunk = pd.read_csv(
        os.path.join(infile, files[0]), 
                     index_col = 0
                     )

    cols = sel_columns(chunk)
    
    data = create_dict(cols)
    
    for filename in files:

        for coord in cols:
            df = load(os.path.join(
                infile, filename), 
                coord = coord)
            data[coord].append(df.values)
            
    coords = {"lon": df.columns.values, 
              "lat": df.index.values}
            
    return convert_to_array(data), coords






def save_in_dataset(zon, mer):

    lats = np.arange(-20, 20, 1)
    lons = np.arange(-75, -25, 1)
    
    times = pd.date_range("2013-1-1 00:00", "2013-1-1 23:50", freq = "10min")
    
    ds = xr.Dataset(
        {
         "zonal": (["time", "lat", "lon"], zon), 
         "meridional":(["time", "lat", "lon"], mer),
             }, 
        coords = {
            "time": times,
            "lon": lons,
            "lat": lats
                        })
    
    return ds
infile = "D:\\iri2016\\" 
data, coords = parameters_into_dict(infile)

print(coords)

#ds = save_in_dataset(zon, mer)
