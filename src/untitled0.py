import matplotlib.pyplot as plt
import pandas as pd
import base as b 
import numpy as np
import datetime as dt 

b.config_labels(fontsize = 30)


def neutral_compostion():
    df = b.load('models/temp/msis_saa_300')
    
    df = df.loc[(df.index.time == dt.time(22, 0)) &
                (df.index.year  < 2023)]
    
    # df.index = df.index.to_series().apply(
    #     lambda n: n.replace(hour = 0))
    
    df['ON2'] = df['O'] / df['N2']
    
    df['month'] = df.index.year
    df['day'] = df.index.day_of_year
    
    return pd.pivot_table(
        df, values = 'ON2', columns = 'month', index = 'day')

def electron_density():

    df = b.load("ne_300")
    
    df['month'] = df.index.year
    df['day'] = df.index.day_of_year
    return pd.pivot_table(
       df, values = 'ne', columns = 'month', index = 'day')
    
ds = neutral_compostion()


fig, ax = plt.subplots(
    ncols = 2, 
    dpi = 300,
    figsize = (16, 8), 
    sharey = True
    )

plt.subplots_adjust(wspace= 0.05)


img = ax[0].contourf(ds.columns, ds.index, ds.values, 40)


label = '$[O]/[N_2]$'

ax[1].plot(ds.mean(axis = 1), ds.index)
ax[1].set(xlabel = label)
ax[0].set(yticks = np.arange(0, 366, 60), 
          xticks = np.arange(2013, 2022, 2), 
          ylabel = 'Day of year', 
          xlabel = 'Years')

ticks = np.linspace(4, 8, 5)
b.colorbar(
        img, 
        ax[0], 
        ticks, 
        label = label, #'$n_0$ ($m^{-3}$)', 
        height = '10%' , 
        width = "80%",
        orientation = "horizontal", 
        anchor = (-0.26, 0.4, 1.26, 0.9)
        )
