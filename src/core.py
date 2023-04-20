from GEO import sites
import iri2016 as iri
import datetime as dt 
from Models import run_msise
from Base import conductivity, conductivity2, collision_frequencies
import pandas as pd
from nrlmsise00 import msise_flat
from PlanetaryIndices import get_indices

def neutral_iono_parameters(
        dn = dt.datetime(2013, 1, 1, 21, 0), 
        hmin = 100, 
        hmax = 500, 
        step = 1, 
        site = "saa",
        B = 0.25e-04,
        mass = "effective"):
    
    glat, glon = sites[site]["coords"]
    
    ds = iri.IRI(dn, [hmin, hmax, step], glat, glon)
    
    ne = ds["ne"].values
    Te = ds["Te"].values
    
    msis = run_msise(
        dn,
        glat, glon,
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
    
    cond = conductivity2(ne, 
                         nue, 
                         nui, B = B, 
                         mass = mass)
    
    data = {
        "nue": nue, 
        "nui": nui, 
        "perd": cond.pedersen, 
        "hall": cond.hall, 
        "par": cond.parallel,
        "bi": cond.ion_mobility,
        "be": cond.electron_mobility, 
        "ke": cond.electron_ratio, 
        "ki": cond.ion_ratio
        }
    
    return pd.DataFrame(data, index = msis.index)


def get_iri(dn, zeq, glat, glon):
    ds = iri.IRI(dn, [zeq, zeq, 1], glat, glon)
    
    ne = ds["ne"].values[0]
    Te = ds["Te"].values[0]
    return ne, Te

def get_msis(dn, zeq, glat, glon):
    
    """
    densities: list of floats
    		0. He number density [cm^-3]
    		1. O number density [cm^-3]
    		2. N2 number density [cm^-3]
    		3. O2 number density [cm^-3]
    		4. AR number density [cm^-3]
    		5. total mass density [g cm^-3] 
    		6. H number density [cm^-3]
    		7. N number density [cm^-3]
    		8. Anomalous oxygen number density [cm^-3]
        peratures: list of floats
    		0. Exospheric temperature [K]
    		1. Temperature at `alt` [K]

    """
    
    t = get_indices(dn.date())
     
    res = msise_flat(
        dn, zeq, glat, glon, 
        t.get("F10.7a"), t.get("F10.7obs"), t.get("Ap")
        )
    
    He, O, N2, O2, Ar, mass, H, N, AnO, Tex, Tn = tuple(res)
    
    return He, O, N2, O2, H, N, Tn

