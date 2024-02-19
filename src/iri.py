import iri2016 as iri
import numpy as np
import datetime as dt
from GEO import sites
import pandas as pd
import aeronomy as io
from tqdm import tqdm 
import GEO as gg

class ne_from_latitude:
    
    def __init__(
            self, 
            zl, 
            fo = 9.63, 
            hm = 390.0
            ):
        
        
        self.zl = zl 
        self.fo = fo 
        self.hm = hm 
        
    @property   
    def hmF2(self):
        """
        HmF2 vs latitude       
        HMF2 = 297.96739 +(423.61233-287.96739)*
                (1. + EXP((ZLAMDA-0.122270)/0.08602))
        """
        return self.hm * np.cos(np.radians(self.zl))**2.0
    
    @property
    def foF2(self):
        """Frequency vs latitude"""
        return ((9.63903 *  + 
                 6.93680 * self.zl + 
                 107.61039 * pow(self.zl, 2) -
                 504.08374 * pow(self.zl, 3))
                * self.fo / 9.63903)
    @property
    def Nmax(self):
        """Density of peak vs latitude"""
        return 1.24e10 * pow(self.foF2, 2)
        
    def E_layer(self, z):
        """E-layer density Chapman"""
        ze = ((z - 100.0) / 50.0)
        return self.chapman_layer(3.0e09, ze) 
    
    def F_layer(self, z):
        """F-layer density Model: Chapman or Epstein"""
        
        zf = (z - self.hmF2) / 60.
        return self.chapman_layer(self.Nmax, zf)  

    def ne(self, z):
        """Get total electron density profile"""
        return (self.E_layer(z) + self.F_layer(z)) 
    
    @staticmethod
    def chapman_layer(Ne, z):
        """Chapman layer model"""
        return Ne * np.exp(1.0 - z - np.exp(-z)) 
    

def point_iri(dn, glat, glon, alt):
    ds = iri.IRI(dn, [alt, alt, 1], glat, glon)
    
    ne = ds["ne"].values[0]
    Te = ds["Te"].values[0]
    return {"ne": ne, "te": Te}


def altrange_iri(
        dn: dt.datetime,
        glat: float, 
        glon: float,
        hmin: float = 200.0, 
        hmax: float = 500.0, 
        step: float = 1.0
        ):
    
    ds = iri.IRI(dn, [hmin, hmax, step], glat, glon)
    
    df = ds.where(ds.alt_km).to_dataframe()
    
    df.index = df.index.get_level_values(0)
    
    return df.drop(columns = "Tn")



def timeseries_iri(site = "saa"):
    
    glat, glon = sites[site]["coords"]
    
    times = pd.date_range(
            dt.datetime(2013, 3, 16), 
            dt.datetime(2013, 3, 20), 
            freq = "10min")
    
    
    out = []
    
    for dn in times:

        ds = altrange_iri(
                      dn, glat, glon,
                      hmin = 200, 
                      hmax = 500,
                      step = 10
                      )
        
        ds['L'] = io.scale_gradient(ds['ne'], ds.index)
        ds["alt"] = ds.index
        ds.index = [dn] * len(ds)
        
        out.append(ds)

    return pd.concat(out)



def build_IRI_dataset(dn, glat, glon):
    
    ds = iri.IRI(dn, [280, 320, 1], 
                 float(glat), 
                 float(glon))

    df = ds.where(ds.alt_km).to_dataframe()

    df.index = df.index.get_level_values(0)

    df['L'] = io.scale_gradient(df['ne'], df.index)

    cols = [
        'ne', 'Tn', 'Ti', 'Te', 'dn',
        'NmF2', 'hmF2', 'foF2', 'L']

    df['dn'] = dn
    
    return df.loc[df.index == 300, cols].set_index('dn')


    
   
def build_map():
    
    dn = dt.datetime(2013, 1, 24, 22,0)
    
    out = []
    for glon in tqdm(np.arange(-90, -29, 1)):
        for glat in np.arange(-30, 20, 1):
            ds = iri.IRI(dn, [300, 300, 1], int(glat), int(glon))
            
            out.append([glon, glat, ds['ne'].item()])
            
            
    df = pd.DataFrame(np.array(out))
    
    save = 'models/temp/map_iri.txt'
    
    df.to_csv(save)
    


def Equator_profiles(dn):

    glon, glat, x, y = gg.load_meridian(dn.year)
    
    
    ds = altrange_iri(
                   dn, glat, glon,
                   hmin = 100, 
                   hmax = 500,
                   step = 10
                   )
     
    ds['L'] = io.scale_gradient(ds['ne'], ds.index)
    ds["alt"] = ds.index
    
    return ds


# dn = dt.datetime(2013, 12, 24, 22)

