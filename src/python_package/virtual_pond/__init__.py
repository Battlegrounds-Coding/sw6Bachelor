"""Virtual pond module"""

import math
import numpy as np
import csv
from typing import Self
from datetime import datetime, timedelta
from python_package.rain import Rain
from python_package.rain import area
from python_package.rain.artificial_rain import ArtificialConstRain
from python_package.time import Time


class PondData:
    """Data from the virtual pond"""

    def __init__(self, height: float, overflow: bool, volume_in: float, volume_out: float):
        self.height = height
        self.overflow = overflow
        self.volume_in = volume_in
        self.volume_out = volume_out


class VirtualPond:
    """Virtual pond class"""

    def __init__(
        self,
        urban_catchment_area_ha: float,
        surface_reaction_factor: float,
        discharge_coeficent: float,
        pond_area_m2: float,
        water_level_cm: float,
        water_level_min_cm: float,
        water_level_max_cm: float,
        time: Time,
        rain_data_mm: Rain,
    ):
        self.urban_catchment_area = urban_catchment_area_ha
        self.surface_reaction_factor = surface_reaction_factor
        self.discharge_coeficent = discharge_coeficent
        self.pond_area = pond_area_m2
        self.water_level = water_level_cm
        self.water_level_min = water_level_min_cm
        self.water_level_max = water_level_max_cm
        self.rain_data = rain_data_mm
        self.time = time
        self.orifice = 17.5

    def __eq__(self, other: Self):
        """
        Checks if all field variables have the same value.
        """
        return (
            self.urban_catchment_area == other.urban_catchment_area
            and self.surface_reaction_factor == other.surface_reaction_factor
            and self.discharge_coeficent == other.discharge_coeficent
            and self.pond_area == other.pond_area
            and self.water_level == other.water_level
            and self.water_level_min == other.water_level_min
            and self.water_level_max == other.water_level_max
            and self.rain_data == other.rain_data
        )

    def calculate_water_volume(self) -> tuple[float, float, float]:
        """
        Calculate water volume in pond.
        Returns m^3.
        """

        # Get weather forcast from DMI API
        forcast = self.get_rain_data()

        # Water volume change in cm^3
        volume_in = self.water_in(self.surface_reaction_factor, forcast, self.urban_catchment_area)
        volume_out = self.water_out(self.discharge_coeficent, self.orifice, self.water_level)

        # Find the change in volume in the pond
        water_volume_change = volume_in - volume_out

        # Find the current volume of the pond
        current_volume = self.pond_area * (self.water_level / 100)

        min_water_volume = self.pond_area * (self.water_level_min / 100)

        # Find the volume of the pond after taking change into account
        water_volume = current_volume + (water_volume_change)

        water_volume = max(water_volume, min_water_volume)

        return water_volume, volume_in, volume_out

    def generate_virtual_sensor_reading(self) -> PondData:
        """
        Genereate the virtual value of expected water level.
        Returns height in cm, overflow bool, volume_in avrage and volume_out avrage.
        """
        volume_in_avg = 0
        volume_out_avg = 0

        delta = int(self.time.get_delta.total_seconds())
        for x in range(delta):
            water_volume, volume_in, volume_out = self.calculate_water_volume()

            volume_in_avg = volume_in_avg + volume_in
            volume_out_avg = volume_out_avg + volume_out

            overflow = False

            height_cm = (water_volume / self.pond_area) * 100

            height_cm = max(height_cm, 0)

            if height_cm > self.water_level_max:
                # TODO: call alarm
                overflow = True
                height_cm = self.water_level_max
            elif height_cm <= self.water_level_min:
                height_cm = self.water_level_min

            self.water_level = height_cm

            x = x + 1

        volume_in_avg = volume_in_avg / delta
        volume_out_avg = volume_out_avg / delta

        pond_data = PondData(height_cm, overflow, volume_in_avg, volume_out_avg)

        return pond_data

    def water_in(self, k: float, s: float, a_uc: float) -> float:
        """
        Water going into the pond.
        Q_in = kSA_(uc)
        k: Urban surface reaction factor.
        S: Difference between the rain falling into the urban area and the storm water leaving it in mm.
        A_uc : Urban catchment surface area in ha.
        Returns m^3.
        """
        # Convert mm to m
        s = s / 1000

        # Conver ha to m^2
        a_uc = a_uc * 10000

        q_in = k * s * a_uc

        return q_in

    def water_out(self, c: float, d: float, w: float) -> float:
        """
        Water going out of the pond.
        Q_out = C(Pi/4)d^2 *sqrt(2gw)
        c: Discharge coefficient.
        d: Chosen diameter of the orifice in cm.
        w: Water level in cm.
        g: gravitational acceleration (only valid if the orifice is fully submarged ie w >= d), constant of 9.81.
        Returns m^3.
        """

        g = 9.81

        # Convert from cm to m
        w = w / 100
        d = d / 100

        q_out = c * (math.pi / 4) * (math.pow(d, 2)) * math.sqrt(2 * g * w)

        return q_out

    def set_orifice(self, orifice_state: str) -> float:
        """
        Choose orifice, set defualt to max
        Return orifice diameter in cm
        """

        # orifice_max = 17.5
        orifice_max = 75

        match orifice_state:
            case "max":
                self.orifice = orifice_max
            case "med":
                self.orifice = orifice_max * (4 / 7)
            case "min":
                self.orifice = orifice_max * (1 / 7)
            case _:
                self.orifice = orifice_max

        return self.orifice

    def get_rain_data(self) -> float:
        """
        Get weather forcast.
        Returns mm.
        """

        rain_mm = self.rain_data.get_rain_fall(
            area.EmptyArea(self.urban_catchment_area * 10000),
            start_time=self.time.get_current_datetime,
            end_time=self.time.get_current_datetime_delta,
        )

        return rain_mm
