"""Virtual pond module"""

import math


def main():
    """Placeholde for test"""
    # Surface reaction factor
    surface_reaction_factor = 0.25

    # Discharge coeficent
    discharge_coeficent = 0.6

    # Pond area in m^2
    pond_area = 5572

    # Minimum and maximum water level in cm
    max_water_level = 300
    min_water_level = 100

    pond = VirtualPond()

    water_volume = pond.calculate_water_volume(discharge_coeficent, surface_reaction_factor)

    height_over_min, height_overall = pond.generate_virtual_sensor_reading(
        water_volume, pond_area, min_water_level, max_water_level
    )

    print(f"Height over min: {height_over_min} cm.")
    print(f"Height overall: {height_overall} cm.")


class VirtualPond:
    """Virtual pond class"""

    def calculate_water_volume(self, discharge_coeficent, surface_reaction_factor) -> float:
        """Calculate water volume in pond"""

        # Get weather forcast from DMI API
        forcast = self.get_rain_data()
        urban_catchment_area = self.get_rain_area()

        # Get values from previous stradegy
        water_level = self.get_previous_water_level()
        orifice = self.get_previous_orifice()

        # Water volume in cm^3
        volume_in = self.water_in(surface_reaction_factor, forcast, urban_catchment_area)
        volume_out = self.water_out(discharge_coeficent, orifice, water_level)

        water_volume = volume_in - volume_out

        return water_volume

    def get_previous_water_level(self) -> float:
        """Get previous water level from stradegy
        water_level in cm"""

        # Placeholder
        water_level = 200

        return water_level

    def get_previous_orifice(self) -> float:
        """Get previous orifice value from stradegy
        orifice oppening in cm diameter"""

        # Placeholder
        orifice_max = 17.5
        # orifice_med = orifice_max * (4 / 7)
        # orifice_min = orifice_max * (1 / 7)

        orifice = orifice_max

        return orifice

    def get_rain_data(self) -> float:
        "Get weather forcast from DMI api"

        # Peters code

        # placeholder
        rain_mm = 20

        return rain_mm

    def get_rain_area(self) -> float:
        """Get rain catchment area in Ha"""
        # Peter code

        # placeholder
        area = 0.59

        return area

    def generate_virtual_sensor_reading(
        self, water_volume, pond_area, min_water_level, max_water_level
    ) -> tuple[float, float]:
        "Genereate the virtual value of expected water level"

        height_cm = (water_volume / pond_area) * 100

        if height_cm < 0:
            height_cm = 0

        height_over_min = height_cm
        height_overall = height_over_min + min_water_level

        if height_overall >= max_water_level:
            height_overall = max_water_level

        return height_over_min, height_overall

    def water_in(self, k, s, a_uc) -> float:
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

    def water_out(self, c, d, w) -> float:
        """Water going out of the pond
        Q_out = C(Pi/4)d^2 *sqrt(2gw)
        c: Discharge coefficient
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


if __name__ == "__main__":
    main()
