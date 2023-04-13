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



