import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import smooth
import settings as s




def find_slip(vls, threshold = 8):
    diff = np.diff(vls)
    index = [i for i, v in enumerate(diff) 
             if diff[i] > threshold][0]
    cycle = vls[index] - vls[index + 1]
    vls[index + 1:]  += cycle
    return vls


def correct_and_smooth(
        vls, 
        threshold = 8, 
        pts = 10, 
        window = 2
        ):
    vls = find_slip(vls, threshold = threshold)
    return smooth(vls, pts = pts, window = 2)

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
    
# plot_result()