import pandas as pd
import GEO as gg 
import models as m 
from tqdm import tqdm 
import datetime as dt 




def running_iri(site, start, end):
    
    glat, glon = gg.sites[site]['coords']
    
    times = pd.date_range(start, end, freq = "1D")
    
    out = []
    
    desc = start.strftime('%Y' + site)
    
    for dn in tqdm(times, desc = desc):
        
        out.append(m.build_IRI_dataset(dn, glat, glon))
            
    return pd.concat(out)

start = dt.datetime(2013, 1, 1, 0)
end = dt.datetime(2013, 12, 31, 0)
site = 'jic'

df = running_iri(site, start, end)

save_in = 'models/temp/2013_iri.txt'

df.to_csv(save_in)
