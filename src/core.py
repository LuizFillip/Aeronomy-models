import models as m 
import pandas as pd
import GEO as gg
import datetime as dt


def altrange_models(**kargs):
    
    iri = m.altrange_iri(**kargs)
    
    msi = m.altrange_msis(**kargs)
    
    return pd.concat([msi, iri], axis = 1)

def point_models(**kwargs):
    """Ne, Te, He, O, N2, O2, H, N, Tn"""

    return {**m.point_iri(**kwargs), **m.point_msis(**kwargs)}



def kargs(dn, hmin = 100, hmax = 500, step = 10):
  glon, glat, x, y = gg.load_meridian(dn.year)
  return dict(
      dn = dn, 
      glat = glat, 
      glon = glon, 
      hmin = hmin, 
      hmax = hmax, 
      step = step
      )
  


