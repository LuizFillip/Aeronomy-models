import pandas as pd
from common import getPyglow
from RTIparameters import scale_gradient
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


date = datetime(2014, 1, 1, 21, 10)

pyglow = getPyglow(date)


ne = pyglow.density()


fig, ax = plt.subplots(ncols = 2, 
                       sharey = True, 
                       figsize = (15, 15))


plt.subplots_adjust(wspace = 0.1)

alts = np.arange(100, 600 + 1, 1)


args = dict(lw = 4, color = "k")

ax[0].plot(ne, alts, **args)

ax[1].plot(scale_gradient(ne), alts, **args)

ax[0].set(ylabel = "Altitude (km)", 
          xscale = "log", 
          xlabel = ("Densidade eletrônica,\n"+ 
                              r" $n_0~(cm^{-3}$)"),)

ax[1].axvline(0, linestyle = "--", lw = 2, color = "k")
ax[1].set(xlim = [-6e-5, 6e-5], 
          xlabel = ("Gradiente de escala \n" + 
       r"$ L^{-1} = \frac{1}{n_0} \frac{\partial n_0}{\partial z} (10^{-3} m^{-1})$"))


ax[1].xaxis.set_major_formatter(
    ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/1e-3)))



