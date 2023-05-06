from .msis import point_msis, altrange_msis
from .iri import  point_iri, altrange_iri
import pandas as pd

def altrange_models(**kargs):
    
    iri = altrange_iri(**kargs)
    
    msi = altrange_msis(**kargs)
    
    return pd.concat([msi, iri], axis = 1)

def point_models(**kwargs):
    """Ne, Te, He, O, N2, O2, H, N, Tn"""
    return point_iri(**kwargs) + point_msis(**kwargs)


