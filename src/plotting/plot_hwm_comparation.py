import datetime as dt
import matplotlib.pyplot as plt
from common import load
import settings as s

def plot_component(ax, df, name, color):
    
    ax.plot(df, label = name, color = color)
    ax.legend(loc = "lower left")
    ax.grid()
     
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 4)
    
def plot_hwm_comparation(
        date = dt.datetime(2002, 10, 11), 
        folder = "HWM14"
        ):
    
    fig, ax = plt.subplots(
        figsize = (12, 5), 
        ncols = 2, 
        sharex = True
        )    
    plt.subplots_adjust(wspace = 0.2)
    
    names = ["Boa Vista", "Cachimbo", "Campo Grande"]
    
    colors = ["red", "black", "blue"]
    
    
    for n, site in enumerate(["boa", "ccb", "cgg"]):
    
        df = load_HWM(
            infile = f"database/HWM/{folder}/{site}3502002.txt"
            )
        
        df.index = df.index - dt.timedelta(hours = 3)
        
        df = df.loc[df.index.date == date.date()]
        
        df["mer"] = df["mer"] * (-1)
        
        plot_component(
            ax[1], df["zon"], names[n], colors[n]
            )
        
        plot_component(
            ax[0], df["mer"], names[n], colors[n]
            )
     
    ax[1].set(
        ylim = [-300, 300], 
        ylabel = "Velocidade zonal (+L)", 
        xlabel = "Hora local"
        )  
    ax[0].set(
        ylim = [-100, 100], 
        ylabel = "Velocidade meridional (+S)", 
        xlabel = "Hora local"
        )
    
    dt_str = date.strftime("%d/%m/%Y - (%j)")
    
    fig.suptitle(f"{dt_str} - {folder}")
    
    return fig 

df = load().HWM()
dn = dt.date(2013, 1, 1)
print(df.loc[df.index.date == dn].plot())