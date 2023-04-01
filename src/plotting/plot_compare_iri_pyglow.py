import iri2016 as iri
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import settings as s
from GEO.src.core import coords


s.config_labels()

dn = dt.datetime(2013, 1, 1, 21, 0)

glat, glon = coords["saa"]

altitudes = np.arange(75, 705, 5)


ds = iri.IRI(dn, [75, 700, 5], glat, glon)


df = pd.read_csv("database/IRI/temp_ne_2013.txt", index_col = 0)

fig, ax = plt.subplots(dpi = 300)


#ax.plot(df["te"], df.index, label = "pyglow")
ax.plot(ds.Tn, df.index, label = "Neutra")
ax.plot(ds.Ti, df.index, label = "ionica")
ax.plot(ds.Te, ds.alt_km, label = "eletronica")

ax.legend()


plt.show()


#fig.savefig("test.png", dpi = 200)

