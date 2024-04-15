"""Testing of virtual pond module"""

from python_package.virtual_pond import VirtualPond
from python_package import rain

URBAN_CATCHMENT_AREA = 0.59
DISCHARGE_COEFICENT = 0.6
POND_AREA = 5572
SURFACE_REACTION_FACTOR = 0.25
WATER_LEVEL_MIN = 100
WATER_LEVEL_MAX = 300
rain_data = rain.Rain()


def test_water_in():
    """
    Test water going into the pond.
    k: Urban surface reaction factor.
    S: Difference between the rain falling into the urban area and the storm water leaving it.
    A_uc : Urban catchment surface area.
    water_in returns m^3.
    """

    water_level = 200

    virtual_pond = VirtualPond(
        URBAN_CATCHMENT_AREA,
        SURFACE_REACTION_FACTOR,
        DISCHARGE_COEFICENT,
        POND_AREA,
        water_level,
        WATER_LEVEL_MIN,
        WATER_LEVEL_MAX,
        rain_data,
    )

    k = 0.25
    s = 20
    a_uc = 0.5

    volume_in = virtual_pond.water_in(k, s, a_uc)

    assert volume_in == 25


def test_water_out():
    """
    Test water going out of the pond.
    c: Discharge coefficient.
    d: Chosen diameter of the orifice in cm.
    w: Water level in cm.
    water_out returns m^3.
    """

    water_level = 200

    virtual_pond = VirtualPond(
        URBAN_CATCHMENT_AREA,
        SURFACE_REACTION_FACTOR,
        DISCHARGE_COEFICENT,
        POND_AREA,
        water_level,
        WATER_LEVEL_MIN,
        WATER_LEVEL_MAX,
        rain_data,
    )

    c = 0.6
    d = 15
    w = water_level

    volume_out = virtual_pond.water_out(c, d, w)
    volume_out = round(volume_out, 4)

    assert volume_out == 0.0664


def test_tba():
    """TBA"""
