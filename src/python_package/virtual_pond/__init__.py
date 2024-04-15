"""Virtual pond module"""

import math


class PondData:  # pylint: disable=R0903
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
        urban_catchment_area: float,
        surface_reaction_factor: float,
        discharge_coeficent: float,
        pond_area: float,
        water_level: float,
        water_level_min: float,
        water_level_max: float,
    ):  # pylint: disable=R0913
        self.urban_catchment_area = urban_catchment_area
        self.surface_reaction_factor = surface_reaction_factor
        self.discharge_coeficent = discharge_coeficent
        self.pond_area = pond_area
        self.water_level = water_level
        self.water_level_min = water_level_min
        self.water_level_max = water_level_max

    def calculate_water_volume(self) -> tuple[float, float, float]:
        """
        Calculate water volume in pond.
        Returns m^3.
        """

        # Get weather forcast from DMI API
        forcast = self.get_rain_data()

        # Get values from previous stradegy
        orifice = self.get_previous_orifice()

        # Water volume change in cm^3
        volume_in = self.water_in(self.surface_reaction_factor, forcast, self.urban_catchment_area)
        volume_out = self.water_out(self.discharge_coeficent, orifice, self.water_level)

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
        Returns height_over_min, height in cm and overflow bool.
        """

        water_volume, volume_in, volume_out = self.calculate_water_volume()

        overflow = False

        height_cm = (water_volume / self.pond_area) * 100

        height_cm = max(height_cm, 0)

        if height_cm > self.water_level_max:
            overflow = True
            height_cm = self.water_level_max
        elif height_cm <= self.water_level_min:
            height_cm = self.water_level_min

        pond_data = PondData(height_cm, overflow, volume_in, volume_out)

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


    #TODO: get orifice data
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

    #TODO: get rain data from peter
    def get_rain_data(self) -> float:
        """
        Get weather forcast from DMI api.
        Returns mm.
        """

        # Peters code

        # placeholder
        rain_mm = 20

        return rain_mm
