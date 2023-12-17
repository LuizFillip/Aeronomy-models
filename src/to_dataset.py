import os
import pandas as pd
import xarray as xr
import datetime as dt
import numpy as np


def sel_columns(df):

    cols = list(df.columns)
        
    return [i for i in cols if i not in ["lat", "lon"]]



def create_dict(cols):
    out = {}
    
    for i in range(len(cols)):
        out[cols[i]] = []

    return out

def convert_to_array(out):
     for key in out.keys():
         out[key] =  np.array(out[key])
     return out





def datetime_from_str(filename):
    f = filename.replace(".txt", "")
    return dt.datetime.strptime(f, "%Y%m%d%H%M")


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
    times = []
    
    for filename in files:
        
        times.append(datetime_from_str(filename))

        for coord in cols:
            df = load(os.path.join(
                infile, filename), 
                coord = coord)
            data[coord].append(df.values)
            
    lon = df.columns.values
    lat = df.index.values
            
    coords = {
        "lon": lon,
        "lat": lat,
        "time": times
              }
            
    return convert_to_array(data), coords


def save_in_dataset(infile):

    data, coords = parameters_into_dict(infile)


    def update_data_vars(data):
        data_vars = {}
        
        for key in data.keys():
        
            data_vars[key] = (
                ["time", "lat", "lon"], data[key])
        
        return data_vars


    ds = xr.Dataset(update_data_vars(data))

    ds.coords["time"] = coords["time"]
    ds.coords["lon"] = coords["lon"]
    ds.coords["lat"] = coords["lat"]
    
    return ds


    


