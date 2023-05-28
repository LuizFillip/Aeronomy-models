import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import settings as s
from labels import Labels


def plot_iono_part(ax, ion):
    ax1 = ax.twinx()
    
    p, = ax.plot(ion["Ne"] * 1e-6, color = "b")
    ax.set(ylabel = "Ne ($10^{6}~cm^{-3}$)")
    s.change_axes_color(ax, p)
    ax.grid()
    ax1.plot(ion["L"] * 1e5, color = "k")
    ax1.set(ylabel = "$L^{-1}~(10^{-5}~m^{-1}$)")
    s.config_labels()
    s.format_axes_date(ax, time_scale = "hour", interval = 2)
    ax1.axhline(0, color = "r")


fig, ax = plt.subplots(
    dpi = 300, figsize = (8, 4)
    )


ne_file = "database/IRI/SAA/20130101.txt"
