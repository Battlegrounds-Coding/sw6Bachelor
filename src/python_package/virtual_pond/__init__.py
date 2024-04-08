"""Virtual pond module"""

import math


class PondData:  # pylint: disable=R0903
    """Data from the virtual pond"""

    def __init__(self, height_over_min: float, height_overall: float, overflow: bool):
        self.height_over_min = height_over_min
        self.height_overall = height_overall
        self.overflow = overflow


class VirtualPond:
    """Virtual pond class"""

    def __init__(
        self,
        urban_catchment_area: float,
        surface_reaction_factor: float,
        discharge_coeficent: float,
        pond_area: float,
        water_level_min: float,
        water_level_max: float,
    ):  # pylint: disable=R0913
        self.urban_catchment_area = urban_catchment_area
        self.surface_reaction_factor = surface_reaction_factor
        self.discharge_coeficent = discharge_coeficent
        self.pond_area = pond_area
        self.water_level_min = water_level_min
        self.water_level_max = water_level_max

    def calculate_water_volume(self) -> float:
        """
        Calculate water volume in pond.
        Returns m^3.
        """

        # Get weather forcast from DMI API
        forcast = self.get_rain_data()

        # Get values from previous stradegy
        water_level = self.get_previous_water_level()
        orifice = self.get_previous_orifice()

        # Water volume in cm^3
        volume_in = self.water_in(self.surface_reaction_factor, forcast, self.urban_catchment_area)
        volume_out = self.water_out(self.discharge_coeficent, orifice, water_level)

        water_volume = volume_in - volume_out

        return water_volume

    def get_previous_water_level(self) -> float:
        """
        Get previous water level from stradegy.
        Returns cm.
        """

        # Placeholder
        water_level = 200

        return water_level

    def get_previous_orifice(self) -> float:
        """
        Get previous orifice value from stradegy.
        Returns cm.
        """

        # Placeholder
        orifice_max = 17.5
        # orifice_med = orifice_max * (4 / 7)
        # orifice_min = orifice_max * (1 / 7)

        orifice = orifice_max

        return orifice

    def get_rain_data(self) -> float:
        """
        Get weather forcast from DMI api.
        Returns mm.
        """

        # Peters code

        # placeholder
        rain_mm = 20

        return rain_mm

    def generate_virtual_sensor_reading(self, water_volume: float) -> PondData:
        """
        Genereate the virtual value of expected water level.
        Returns height_over_min, height_overall in cm and overflow bool.
        """

        height_cm = (water_volume / self.pond_area) * 100

        height_cm = max(height_cm, 0)

        height_over_min = height_cm
        height_overall = height_over_min + self.water_level_min

        overflow = False

        if height_overall > self.water_level_max:
            overflow = True

        pond_data = PondData(height_over_min, height_overall, overflow)

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
