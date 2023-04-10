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


ds = iri.geoprofile(dn, [75, 700, 5], glat, glon)


df = pd.read_csv("database/IRI/temp_ne_2013.txt", index_col = 0)

fig, ax = plt.subplots(dpi = 300)

ax.plot(ds.ne, ds.alt_km, label = "IRI2016")
ax.plot(df["ne"] * 1e6, df.index, label = "Pyglow")

ax.legend()


plt.show()



