"""Testing of virtual pond module"""

from python_package.virtual_pond_module import VirtualPond


def test_water_in():
    """
    Test water going into the pond.
    k: Urban surface reaction factor.
    S: Difference between the rain falling into the urban area and the storm water leaving it.
    A_uc : Urban catchment surface area.
    water_in returns m^3.
    """

    virtual_pond = VirtualPond()

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

    virtual_pond = VirtualPond()

    c = 0.6
    d = 15
    w = 200

    volume_out = virtual_pond.water_out(c, d, w)
    volume_out = round(volume_out, 4)

    assert volume_out == 0.0664


def test_generate_virtual_sensor_reading():
    """
    Test generating the water level in the pond.
    volume_in in m^3.
    volume_out in m^3.
    pond_area in m^2.
    generate_virtual_sensor_reading return height in cm.
    """

    virtual_pond = VirtualPond()

    min_water_level = 100
    max_water_level = 300

    volume_in = 45
    volume_out = 15
    pond_area = 400

    water_volume = volume_in - volume_out

    virtual_pond_data = virtual_pond.generate_virtual_sensor_reading(
        water_volume, pond_area, min_water_level, max_water_level
    )

    assert virtual_pond_data.height_over_min == 7.5
    assert virtual_pond_data.height_overall == 107.5
    assert virtual_pond_data.overflow == False


def test_tba():
    """TBA"""
