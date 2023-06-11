import pandas as pd
import models as mm
import datetime as dt



def load_hwm(ds, alt = 250, site = "car"):
    
    infile = "database/HWM/winds_all_sites.txt"
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    if isinstance(ds, pd.DataFrame):
        idx_cond = ((df.index >= ds.index[0]) & 
                    (df.index <= ds.index[-1]))
    elif isinstance(ds, tuple):
        
        idx_cond = ((df.index >= ds[0]) & 
                    (df.index <= ds[-1]))
    
    sit_cond = (df["site"] == site)
    
    alt_cond = (df["alt"] == alt)
    
    df = df.loc[sit_cond & alt_cond & idx_cond]
    
    for col in df.columns:
        df[col] = mm.correct_and_smooth(df[col])

    return df




