import os
import pandas as pd
import xarray as xr
import datetime as dt
from FluxTube.src.core import get_conductivities
from Models.src.utils import (sel_columns,  
                              create_dict,  
                              convert_to_array)


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
        
            data_vars[key] = (["time", "lat", "lon"], data[key])
        
        return data_vars


    ds = xr.Dataset(update_data_vars(data))

    ds.coords["time"] = coords["time"]
    ds.coords["lon"] = coords["lon"]
    ds.coords["lat"] = coords["lat"]
    
    return ds



def join_models_results(
        path_iri, 
        path_msis,
        filename):
    
    """
    Get results grid from iri and msis and concate them
    
    """

    df1 = pd.read_csv("WSL/data/iri2016/201301010000.txt", index_col = 0)
    df1.columns = [c.lower() for c in df1.columns]
    
    df1 = df1.set_index(["lat", "lon"])
    
    
    df = pd.read_csv("201301010000.txt", index_col = 0)
    
    df.columns = [c.lower() for c in df.columns]
    
    df = df.set_index(["lat", "lon"])
    
    ds = pd.concat([df, df1], axis = 1)
    
    hall, perd = get_conductivities(ds)
    
    ds["perd"] =  perd
    ds["hall"] =  hall
    
    ds.to_csv("2013010100002.txt")
    
    
    
def main():
    infile = "D:\\iri2016\\" 
    
    ds = save_in_dataset(infile)
    
    print(ds)

