import pandas as pd
import GEO as gg 
import models as m 
from tqdm import tqdm 
import datetime as dt 

def test_datasets(site):
    
    glat, glon = gg.sites[site]['coords']
    dn = dt.datetime(2013, 1, 1, 0, 0)
    alt = 300 
    
    build_MSIS_dataset(dn, glat, glon, alt)

def build_MSIS_dataset(dn, glat, glon, alt = 300):
    
    kwargs = dict(
        dn = dn, 
        glat = glat,
        glon = glon,
        alt = alt
        )
    
    return pd.DataFrame(m.point_msis(**kwargs), index = [dn])


def concat_datasets(dn, glat, glon):
    df1 = build_MSIS_dataset(dn, glat, glon)
    df2 = m.build_IRI_dataset(dn, glat, glon)
    
    return pd.concat([df1, df2], axis = 1)


def running_datasets(site, times):
    
    glat, glon = gg.sites[site]['coords']
 
    out = []
        
    for dn in tqdm(times, desc = site):
        try:
            out.append(concat_datasets(dn, glat, glon))
        except:
            continue
            
    return pd.concat(out)




def build_times(year):
    start = dt.datetime(year, 1, 1, 23)
    end = dt.datetime(year, 12, 31, 23)
    
    times = pd.date_range(start, end, freq = "1D")
    
    def last_range(ss):
        
        dl = dt.timedelta(hours = 4)
        return [dn for dn in pd.date_range(
            ss, ss + dl, freq = '30min')]
    
    out = []
    for ss in times:
        out.extend(last_range(ss))
        
        
    return out


site = 'jic'
year = 2021

def save_data(year, site):
    times = build_times(year)
    df = running_datasets(site, times)
    
    save_in = f'models/temp/local_{year} '
    
    df.to_csv(save_in)