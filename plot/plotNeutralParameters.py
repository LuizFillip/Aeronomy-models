import pandas as pd
from common import runMSISE
from RTIparameters import neutrals
from datetime import datetime
import matplotlib.pyplot as plt
from plotConfig import *

date = datetime(2014, 1, 1, 21, 10)

dat = runMSISE(date)

neutral = neutrals(dat.Tn.values, 
                              dat.O.values, 
                              dat.O2.values, 
                              dat.N2.values)


fig, ax = plt.subplots(ncols = 3, 
                       sharey = True, 
                       figsize = (25, 20))

plt.subplots_adjust(wspace = 0.1)
nu = neutral.collision
r = neutral.recombination


args = dict(lw = 3)
ax[0].plot(dat.Tn, dat.index, **args, color = "k")

ax[0].set(xlabel = "Temperatura (K)", 
          ylabel = "Altitude (km)",
          xlim = [0, 1200])

ax[1].plot(dat[["O", "O2", "N2"]], 
           dat.index, **args)

ax[1].legend(["$O$", "$O_2$", "$N_2$"])
ax[1].set(xscale = "log",
          xlabel = "Concentração $(cm^{-3})$", 
          xlim = [10, 10e14])


ax[2].plot(nu, dat.index, **args, color = "k")
ax[2].set(xscale = "log",  
          xlim = [1e-3, 10e4],
          xlabel = ("Frequência de colisão \n íon-neutro," + 
     r" $\nu_{in}~(s^{-1})$"))



ax1 = ax[2].twiny()

p1, = ax1.plot(r, dat.index, **args, color = '#0C5DA5')

ax1.xaxis.label.set_color(p1.get_color())

ax1.tick_params(axis = 'x', colors = p1.get_color())

ax1.spines['top'].set_color(p1.get_color()) 

ax1.set(xscale = "log", 
        xlim = [1e-9, 10e2],
        xlabel = ("Taxa de recombinação,\n " + 
        r"$\nu_R~(s^{-1})$"))

text_painels(ax, x = 0.01, y = 0.95, 
                 fontsize = 35)


fig.savefig(path_tex("methods") + "\\neutral_parameters.png")