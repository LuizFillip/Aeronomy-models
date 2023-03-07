import pandas as pd
from build import paths 
import matplotlib.pyplot as plt
import numpy as np
import setup as s

infile = paths().get_pathfile("IRI")



def plotElectronContourf(infile):
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df1 = pd.pivot_table(df, 
                         columns = df.index, 
                         index = "alt", 
                         values = "Ne")
    
    fig, ax = plt.subplots(figsize = (8, 5))
    
    s.config_labels()
    
    cs = plt.contourf(df1.columns , 
                     df1.index, 
                     df1.values, 50, 
                     cmap = "Blues")
    
    plt.colorbar(cs)
    
    ax.set(ylabel = "Altitude (km)", 
           xlabel = "Meses")
    
    s.format_axes_date(ax)
