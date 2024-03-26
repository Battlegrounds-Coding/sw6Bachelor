"""Virtual pond module"""

import math


def placeholder():
    """Placeholde for test"""
    # Surface reaction factor
    surface_reaction_factor = 0.25

    # Urban catchmentare in Ha
    urban_catchment_area = 0.59

    # Discharge coeficent
    discharge_coeficent = 0.6

    # Pond area in m^2
    pond_area = 5572

    # Minimum and maximum water level in cm
    # max_water_level = 300
    # min_water_level = 100

    pond = VirtualPond()

    volume_in, volume_out = pond.calculate_water_volume(
        discharge_coeficent, surface_reaction_factor, urban_catchment_area
    )

    height_cm = pond.generate_virtual_sensor_reading(volume_in, volume_out, pond_area)

    print(f"Height: {height_cm} cm.")
    print(f"Volume in: {volume_in} m^3.")
    print(f"Volume out: {volume_out} m^3.")


class VirtualPond:
    """Virtual pond class"""

    def calculate_water_volume(
        self,
        discharge_coeficent,
        surface_reaction_factor,
        urban_catchment_area,
    ):
        """Calculate water volume in pond"""

        # Get weather forcast from DMI API
        forcast = self.get_weather_forecast()

        # Get values from previous stradegy
        water_level, orifice = self.get_previous_reading()

        # Water volume in cm^3
        volume_in = self.water_in(surface_reaction_factor, forcast, urban_catchment_area)
        volume_out = self.water_out(discharge_coeficent, orifice, water_level)

        return volume_in, volume_out

    def get_previous_reading(self):
        "Get the previous pond reading"

        # Palceholder
        water_level = 200  # unit: cm

        # Orifice diameter in cm
        orifice_max = 17.5
        # orifice_med = orifice_max * (4 / 7)
        # orifice_min = orifice_max * (1 / 7)

        orifice = orifice_max

        return water_level, orifice

    def get_weather_forecast(self):
        "Get weather forcast from DMI api"

        # Peters code

        # placeholder
        rain_mm = 20

        return rain_mm

    def generate_virtual_sensor_reading(
        self,
        volume_in,
        volume_out,
        pond_area,
    ):
        "Genereate the virtual value of expected water level"

        water_volume = volume_in - volume_out

        height_cm = (water_volume / pond_area) * 100

        return height_cm

    def water_in(self, k, s, a_uc):
        """Water going into the pond
        Q_in = kSA_(uc)
        k: Urban surface reaction factor, in paper 0.25 (offline example)
        S: Difference between the rain falling into the urban area and the storm water leaving it
        A_uc : Urban catchment surface area, in paper 0.59 ha (offline example)
        Returns m^3
        """

        # Convert mm to m
        s = s / 1000

        # Conver ha to m^2
        a_uc = a_uc * 10000

        q_in = k * s * a_uc

        return q_in

    def water_out(self, c, d, w):
        """Water going out of the pond
        Q_out = C(Pi/4)d^2 *sqrt(2gw)
        C: Discharge coefficient
        d: Chosen diameter of the orifice in cm
        w: Water level in cm
        g: gravitational acceleration (only valid if the orifice is fully submarged ie w >= d)
        Returns m^3
        """

        g = 9.81

        # Convert from cm to m
        w = w / 100
        d = d / 100

        q_out = c * (math.pi / 4) * (math.pow(d, 2)) * math.sqrt(2 * g * w)

        return q_out


if __name__ == "__placeholder__":
    placeholder()
