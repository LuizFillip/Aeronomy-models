# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 18:39:12 2023

@author: Luiz
"""

import matplotlib.pyplot as plt
import pandas as pd
import settings as s


def plot_result():
    df = pd.read_csv('test_temp.txt', index_col=0)
    df.index = pd.to_datetime(df.index)
    
    
    vls = df['Tn'].values
    
    fig, ax = plt.subplots(dpi = 300)
    
    
    ax.plot(df.index, vls, label = 'original')
    vls = find_slip(vls, threshold = 8)
    
    ax.plot(df.index, vls, label = 'corrigido')
    ax.plot(df.index, smooth(vls, pts = 10, window = 2), 
            label = 'corrigido e suavizado')
    
    ax.legend()
    
    ax.set(ylabel = 'Temperatura (K)', 
           xlabel = 'Hora universal')
    
    s.format_time_axes(ax, hour_locator = 1)