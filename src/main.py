"THIS IS THE MAIN FILE"

from python_package.virtual_pond import VirtualPond

URBAN_CATCHMENT_AREA = 0.59
SURFACE_REACTION_FACTOR = 0.25
DISCHARGE_COEFICENT = 0.6
POND_AREA = 5572
WATER_LEVEL_MIN = 100
WATER_LEVEL_MAX = 300



def main():
    """Main"""
    water_level = 100
    x = 0

    while x < 20:

        virtual_pond = VirtualPond(
            URBAN_CATCHMENT_AREA, SURFACE_REACTION_FACTOR, DISCHARGE_COEFICENT, POND_AREA, water_level, WATER_LEVEL_MIN, WATER_LEVEL_MAX
        )

        pond_data = virtual_pond.generate_virtual_sensor_reading()

        water_level = pond_data.height
        #print(f"Volume in: {pond_data.volume_in} m^3/s")
        #print(f"Volume out: {pond_data.volume_out} m^3/s")
        print(f"Height: {pond_data.height} cm.")
        #print(f"Overflow: {pond_data.overflow}")

        x += 1


if __name__ == "__main__":
    main()
