import numpy as np
from scipy.constants import constants as cs
import datetime as dt
from RayleighTaylor.src.common import load
import pandas as pd
from nrlmsise00 import msise_flat
from PlanetaryIndices.core import get_indices
from astropy import units as u


class electron_density:
    
    def __init__(
            self, 
            zl, 
            fo = 9.63, 
            hm = 390.0
            ):
        
        
        self.zl = zl * u.rad
        self.fo = fo * u.MHz
        self.hm = hm * u.km 
        
    @property   
    def hmF2(self):
        """
        HmF2 vs latitude       
        HMF2 = 297.96739 +(423.61233-287.96739)*
                (1. + EXP((ZLAMDA-0.122270)/0.08602))
        """
        return self.hm * np.cos(
            np.radians(self.zl.value))**2.0
    
    @property
    def foF2(self):
        """Frequency vs latitude"""
        return ((9.63903 *  + 
                 6.93680 * self.zl.value + 
                 107.61039 * pow(self.zl.value, 2) -
                 504.08374 * pow(self.zl.value, 3))
                * self.fo / 9.63903)
    @property
    def Nmax(self):
        """Density of peak vs latitude"""
        return 1.24e10 * pow(self.foF2, 2)
        
    def E_layer(self, z):
        """E-layer density Chapman"""
        ze = ((z - 100.0 * u.km) / 50.0)
        # return 1e10
        return self.chapman_layer(3.0e09, ze.value) 
    
    def F_layer(self, z):
        """F-layer density Model: Chapman or Epstein"""
        
        zf = (z - self.hmF2) / 60.
        return self.chapman_layer(self.Nmax.value, zf.value)  

    def ne(self, z):
        """Get total electron density profile"""
        return (self.E_layer(z) + self.F_layer(z)) #* u.m**(-3)
    
    @staticmethod
    def chapman_layer(Ne, z):
        """Chapman layer model"""
        return Ne * np.exp(1.0 - z - np.exp(-z)) * u.m**(-3)
    



def load_ne(dn):
    df = load().IRI(L = False)
    df = df.loc[df.index == dn]
    return df.set_index("alt")



dn  = dt.datetime(2002, 1, 1, 20)

def get_parameters(
        dn, 
        zeq, 
        den, 
        points = 301, 
        glat = -7.5, 
        glon = -54.8, 
        f107a = 162, 
        AP = 7):
    
    perd = np.zeros(points)
    hall = np.zeros(points)
    
    t = get_indices(dn.date())

    for i in range(points):
        
        res = msise_flat(
            dn, 
            zeq[i], 
            glat, 
            glon, 
            f107a, #t.get("F10.7a"), 
            t.get("F10.7obs"), 
            AP#t.get("Ap")
            )
        
        nu = collision_frequencies(res)
        nue = nu.electrons_neutrals
        nui = nu.ion_neutrals
        
        cond = conductivity(den[i], nue, nui)
        perd[i] = cond.pedersen
        hall[i] = cond.hall
    
    return perd, hall

