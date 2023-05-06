from FluxTube.src.iono import electron_density
from astropy import units as u

class TestIono:
    
    def __init__(self):
        z30 = 0.30 * u.rad
        
        self.n = electron_density(z30)
    
    def test_default(self):
        assert self.n.fo == 9.63 * u.Hz
        assert self.n.hm == 390.0 * u.km 
        
    def test_hmF2(self):
        assert u.isclose(self.n.hmf2, 389.989 * u.km)
        
    def test_foF2(self):
        assert u.isclose(self.n.foF2, 16.1187 * u.MHz)
        
    def test_Elayer(self):
        h300 = 300 * u.km 
        assert u.isclose(self.n.E_layer(h300),
                         146650459.504 * u.m**(-3))
        
    def test_Flayer(self):
        h300 = 300 * u.km 
        assert u.isclose(self.n.F_layer(h300),
                         444342744276.69 * u.m**(-3))




