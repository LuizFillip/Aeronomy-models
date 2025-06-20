import GEO as gg
import pyIGRF 
import iri2016 as iri
from indices import GFZ
from nrlmsise00 import msise_flat


def point_msis(dn, glat, glon, alt):
    
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
    
    ind = GFZ(dn)
    
    f107a = ind.get('F10.7a')
    f107o = ind.get("F10.7obs")
    ap = ind.get("Ap")
    
    res = msise_flat(
        dn, 
        alt, 
        glat, glon, 
        f107a, 
        f107o, 
        ap
        )

    names = ["He", "O", "N2", "O2", "Ar", "mass", 
            "H", "N", "AnO", "Tex", "Tn"]

    dic = {key: value for key, value in zip(names, res)}
        
    for chave in ['Tex', 'AnO', 'mass', 'Ar']:
        if chave in dic:
            del dic[chave]
        
    return dic


def point_iri(dn, glat, glon, alt):
    ds = iri.IRI(dn, [alt, alt, 1], glat, glon)
    
    ne = ds["ne"].values[0]
    Te = ds["Te"].values[0]
    return {"ne": ne, "te": Te}


def point_igrf(dn, glat, glon, alt):
    
    d, i, _, _, _, _, f = pyIGRF.igrf_value(
        glat, 
        glon, 
        alt = alt, 
        year = gg.year_fraction(dn)
        ) 
    return {'d': d, 'i': i, 'Bf': f * 1e-9}

def point_models(**kwargs):
    """Ne, Te, He, O, N2, O2, H, N, Tn"""

    return {**point_iri(**kwargs), 
            **point_msis(**kwargs), 
            **point_igrf(**kwargs)}



def main():
    import datetime as dt 
    dn = dt.datetime(2024, 10, 12)
    
    glon, glat = -40, -7
    alt = 300
    
    kwargs   = dict(
        dn   = dn, 
        glat = glat,
        glon = glon, 
        alt  = alt, 
        )
    
    res = point_models(**kwargs)
    
    print(res)
    
# main()