import numpy as np
import datetime as dt
from common import load


class Ne:
    
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
    



def load_ne(dn):
    df = load().IRI(L = False)
    df = df.loc[df.index == dn]
    return df.set_index("alt")



dn  = dt.datetime(2002, 1, 1, 20)

