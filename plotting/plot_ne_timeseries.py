import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import setup as s
from RayleighTaylor.src.common import load


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


fig, ax = plt.subplots(figsize = (8, 4))

ts = load()

ne_file = "database/IRI/SAA/20130101.txt"

df = ts.ne(ne_file, alt = 300)

plot_iono_part(ax, df)