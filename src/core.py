from GEO.src.core import sites
import iri2016 as iri
import datetime as dt 
from Models.src.run_msise import run_msise
from Base.src.iono import collision_frequencies, conductivity, conductivity2
import pandas as pd

def neutral_iono_parameters(
        dn = dt.datetime(2013, 1, 1, 21, 0), 
        hmin = 100, 
        hmax = 500, 
        step = 1, 
        site = "saa"
        ):
    
    glat, glon = sites[site]["coords"]

    
    ds = iri.IRI(dn, [hmin, hmax, step], glat, glon)
    
    ne = ds["ne"].values
    Te = ds["Te"].values
    
    msis = run_msise(
        dn,
        hmin = hmin, 
        hmax = hmax, 
        step = step)
    
        
    nu = collision_frequencies()
        
    nue = nu.electrons_neutrals(
        msis.O, msis.O2, msis.N2,
        msis.He, msis.H, Te
        )
    
    nui = nu.ion_neutrals(
        msis.O, msis.O2, 
        msis.N2, msis.Tn
        )
    
    cond = conductivity2(ne, nue, nui)
    
    data = {
        "nue": nue, 
        "nui": nui, 
        "perd": cond.pedersen, 
        "hall": cond.hall, 
        "par": cond.parallel
        }
    
    return pd.DataFrame(data, index = msis.index)



