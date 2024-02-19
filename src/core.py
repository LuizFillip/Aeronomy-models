import models as m 
import pandas as pd
import GEO as gg
import pyIGRF 



def altrange_models(**kargs):
    
    iri = m.altrange_iri(**kargs)
    
    msi = m.altrange_msis(**kargs)
    
    df = pd.concat([msi, iri], axis = 1)
    
    d, i, _, _, _, _, f = pyIGRF.igrf_value(
        kargs['glat'], 
        kargs['glon'], 
        alt = 300, 
        year = gg.year_fraction(kargs['dn'])
        )
    
    df["d"] = d
    df["i"] = i
    df["Bf"] = f * 1e-9
    
    return df
        


def point_models(**kwargs):
    """Ne, Te, He, O, N2, O2, H, N, Tn"""

    return {**m.point_iri(**kwargs), 
            **m.point_msis(**kwargs), 
            **m.point_igrf(**kwargs)}



def kwargs(dn, hmin = 100, hmax = 500, step = 10):
  glon, glat, x, y = gg.load_meridian(dn.year)
  return dict(
      dn = dn, 
      glat = glat, 
      glon = glon, 
      hmin = hmin, 
      hmax = hmax, 
      step = step
      )
  
import datetime as dt


kwargs = dict(dn = dt.datetime(2013, 1, 1, 0, 0), 
              zeq = 300,
              glat = -11,
              glon = -80)

m.point_iri(**kwargs)