import models as m 
import GEO as gg
import pandas as pd
import pyIGRF 


def kwargs_from_meridian(dn, hmin = 100, hmax = 500, step = 10):
  glon, glat, x, y = gg.load_meridian(dn.year)
  return dict(
      dn = dn, 
      glat = glat, 
      glon = glon, 
      hmin = hmin, 
      hmax = hmax, 
      step = step
      )

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
        