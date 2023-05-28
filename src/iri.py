import iri2016 as iri
import numpy as np
import datetime as dt
from GEO import sites


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
    

def point_iri(dn, zeq, glat, glon):
    ds = iri.IRI(dn, [zeq, zeq, 1], glat, glon)
    
    ne = ds["ne"].values[0]
    Te = ds["Te"].values[0]
    return ne, Te


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


import pandas as pd

def timeseries_iri():
    glat, glon = sites["saa"]["coords"]
    out = []
    
    for dn in pd.date_range(
            dt.datetime(2013, 3, 16), 
            dt.datetime(2013, 3, 20), 
            freq = "20min"):
        
        df = altrange_iri(
              dn, glat, glon,
              hmin = 250, hmax = 350,
              step = 10)
    
        df["dn"] = dn
        df["alt"] = df.index
        df = df.set_index(df["dn"])
        out.append(df)
        
    
    ds = pd.concat(out)

    ds.to_csv("database/IRI/march_2013.txt") 

timeseries_iri()
