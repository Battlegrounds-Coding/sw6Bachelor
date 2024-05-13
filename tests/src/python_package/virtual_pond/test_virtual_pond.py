"""Testing of virtual pond module"""

from datetime import timedelta, datetime

from python_package.virtual_pond import VirtualPond
from python_package import rain
from python_package.rain import artificial_rain
from python_package.time import Time


URBAN_CATCHMENT_AREA = 0.59
DISCHARGE_COEFICENT = 0.6
POND_AREA = 5572
SURFACE_REACTION_FACTOR = 0.25
WATER_LEVEL_MIN = 100
WATER_LEVEL_MAX = 300


def test_water_in():
    """
    Test water going into the pond.
    k: Urban surface reaction factor.
    S: Difference between the rain falling into the urban area and the storm water leaving it.
    A_uc : Urban catchment surface area.
    water_in returns m^3.
    """

    water_level = 200
    rain_data = rain.Rain()

    START = datetime.now()
    TIME = Time(start=START, current_time=timedelta(seconds=0), delta=timedelta(seconds=10))

    virtual_pond = VirtualPond(
        URBAN_CATCHMENT_AREA,
        SURFACE_REACTION_FACTOR,
        DISCHARGE_COEFICENT,
        POND_AREA,
        water_level,
        WATER_LEVEL_MIN,
        WATER_LEVEL_MAX,
        time=TIME,
        rain_data_mm=rain_data,
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
    rain_data = rain.Rain()

    START = datetime.now()
    TIME = Time(start=START, current_time=timedelta(seconds=0), delta=timedelta(seconds=10))

    virtual_pond = VirtualPond(
        URBAN_CATCHMENT_AREA,
        SURFACE_REACTION_FACTOR,
        DISCHARGE_COEFICENT,
        POND_AREA,
        water_level,
        WATER_LEVEL_MIN,
        WATER_LEVEL_MAX,
        time=TIME,
        rain_data_mm=rain_data,
    )
    # Set orifice oppening to max
    virtual_pond.set_orifice("max")

    c = 0.6
    d = 15
    w = water_level

    volume_out = virtual_pond.water_out(c, d, w)
    volume_out = round(volume_out, 4)

    assert volume_out == 0.0664


def test_generate_virtual_sensor_reading():
    """Test generate_virtual_sensor_reading"""
    water_level = 200

    rain_data = artificial_rain.ArtificialConstRain(20)

    START = datetime.now()
    TIME = Time(start=START, current_time=timedelta(seconds=0), delta=timedelta(seconds=10))

    virtual_pond = VirtualPond(
        URBAN_CATCHMENT_AREA,
        SURFACE_REACTION_FACTOR,
        DISCHARGE_COEFICENT,
        POND_AREA,
        water_level,
        WATER_LEVEL_MIN,
        WATER_LEVEL_MAX,
        time=TIME,
        rain_data_mm=rain_data,
    )

    # Set orifice oppening to max
    virtual_pond.set_orifice("max")

    pond_data = virtual_pond.generate_virtual_sensor_reading()
    height = round(pond_data.height, 4)

    assert height == 204.9947


def test_calculate_water_volume():
    """Test calculate_water_volume"""

    water_level = 100

    rain_data = artificial_rain.ArtificialConstRain(20)

    START = datetime.now()
    TIME = Time(start=START, current_time=timedelta(seconds=0), delta=timedelta(seconds=10))

    virtual_pond = VirtualPond(
        URBAN_CATCHMENT_AREA,
        SURFACE_REACTION_FACTOR,
        DISCHARGE_COEFICENT,
        POND_AREA,
        water_level,
        WATER_LEVEL_MIN,
        WATER_LEVEL_MAX,
        time=TIME,
        rain_data_mm=rain_data,
    )

    # Set orifice oppening to max
    virtual_pond.set_orifice("max")

    volume = virtual_pond.calculate_water_volume()

    volume = round(volume[0], 4)

    assert volume == 5600.3259
