"""Testing of virtual pond module"""

from python_package.virtual_pond_module import VirtualPond


def test_water_in():
    """Test water going into the pond
    k: Urban surface reaction factor, in paper 0.25 (offline example)
    S: Difference between the rain falling into the urban area and the storm water leaving it
    A_uc : Urban catchment surface area, in paper 0.59 ha (offline example)
    waterIn returns m^3
    """

    virtual_pond = VirtualPond()

    k = 0.25
    s = 20
    a_uc = 0.5

    volumeIn = virtual_pond.water_in(k, s, a_uc)

    assert volumeIn == 25


def test_water_out():
    """Test water going out of the pond"""
