import pandas as pd
import os
import datetime as dt

from utils import split_time


infile = "database/MSIS/net/"
files = os.listdir(infile)

filename = files[0]
def first_process(infile):
    df = pd.read_csv(infile, header = 33, 
                     delim_whitespace=True)
    
    df.columns = ['Year', 'Month', 'Day', 'Hour',
                 'O', 'N2','O2','Tn','He',
                 'Ar', 'H',    'N']
    dn = []
    for i, tn in enumerate(df["Hour"]):
        year, month, day = tuple(df.iloc[i, slice(0, 3)].values)
        hour, minute = split_time(tn)
        if hour == 24: hour = 0
        dn.append(dt.datetime(int(year), int(month), int(day), 
                         int(hour), int(minute)))
        
        
    df.index = dn
    
    df = df.drop(columns = ['Year', 'Month','Day','Hour'])
    
    return df
out = []
for filename in files:
    out.append(first_process(infile + filename))
    
ds = pd.concat(out)

ds.to_csv("database/MSIS/cont_msis.txt")