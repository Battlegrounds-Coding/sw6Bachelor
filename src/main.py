"THIS IS THE MAIN FILE"

from python_package.virtual_pond_module import VirtualPond

URBAN_CATCHMENT_AREA = 0.59
SURFACE_REACTION_FACTOR = 0.25
DISCHARGE_COEFICENT = 0.6
POND_AREA = 5572
WATER_LEVEL_MIN = 100
WATER_LEVEL_MAX = 300


def main():
    """Main"""

    virtual_pond = VirtualPond(
        URBAN_CATCHMENT_AREA, SURFACE_REACTION_FACTOR, DISCHARGE_COEFICENT, POND_AREA, WATER_LEVEL_MIN, WATER_LEVEL_MAX
    )

    water_volume = virtual_pond.calculate_water_volume()

    pond_data = virtual_pond.generate_virtual_sensor_reading(water_volume)

    print(f"Height over min: {pond_data.height_over_min} cm.")
    print(f"Height overall: {pond_data.height_overall} cm.")
    print(f"Overflow: {pond_data.overflow}")


if __name__ == "__main__":
    main()
