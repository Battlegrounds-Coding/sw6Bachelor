"THIS IS THE MAIN FILE"

from python_package.log import LogLevel, PrintLogger
from python_package.serial import SerialCom, serial_exceptions
from python_package.kalman_filter.kalman_bank import KalmanBank
from python_package.kalman_filter.kalman import MeasurementData
from python_package.serial.headless import Headless
from python_package.time import Time
from python_package.virtual_pond import VirtualPond
from python_package.rain.artificial_rain import ArtificialConstRain
from datetime import timedelta, datetime
import pause
from python_package.args import ARGS, Mode


LOGGER = PrintLogger()
FAULTS = [
    lambda x: x,
    lambda x: x + 10,
    lambda x: x - 10,
    lambda _: 10,
    lambda _: -10
]

# -- POND DATA
URBAN_CATCHMENT_AREA = 0.59
SURFACE_REACTION_FACTOR = 0.25
DISCHARGE_COEFICENT = 0.6
POND_AREA = 5572
WATER_LEVEL_MIN = 100
WATER_LEVEL_MAX = 300


def handle_controler_exeption(exception: serial_exceptions.exceptions):
    match exception:
        case serial_exceptions.exceptions.NO_RESPONSE:
            LOGGER.log(
                "No responce from device",
                level=LogLevel.ERROR)
        case serial_exceptions.exceptions.INCORRECT_INPUT:
            LOGGER.log(
                "Incorrect input to physical setup",
                level=LogLevel.ERROR)
        case serial_exceptions.exceptions.PUMP_VALUE_OUT_OF_BOUNDS:
            LOGGER.log(
                "Pump value was out of bounds",
                level=LogLevel.ERROR)
        case serial_exceptions.exceptions.NO_SENSOR_READINGS:
            LOGGER.log(
                "No readings from the sensor in the physical setup",
                level=LogLevel.ERROR)
        case serial_exceptions.exceptions.COMUNICATION_ERROR:
            LOGGER.log(
                "Failed to communicate with device",
                level=LogLevel.ERROR)
        case serial_exceptions.exceptions.CONVERSION_ERROR:
            LOGGER.log(
                "Could not parse the data form sensor",
                level=LogLevel.ERROR)


if __name__ == '__main__':
    try:
        # SETUP
        # -- TIME
        TIME = Time(
            current_time=timedelta(seconds=0),
            delta=timedelta(seconds=10))
        START = datetime.now()

        # -- ARGUMENTS
        args = ARGS(START)

        # -- CONTROLER
        match args.mode:
            case Mode.SERIEL:
                controler = SerialCom()
                controler.begin()
            case Mode.HEADLESS:
                controler = SerialCom()
                controler.arduino = Headless(args.data, TIME)

        # -- CASHE
        # TODO: INIT CASHE

        # -- KALMAN BANK
        kalman_bank = KalmanBank(
            faults=FAULTS,
            time=TIME,
            initial_variance=10,
            noice=0.1,
            virtual_pond=VirtualPond(
                urban_catchment_area_ha=URBAN_CATCHMENT_AREA,
                surface_reaction_factor=SURFACE_REACTION_FACTOR,
                discharge_coeficent=DISCHARGE_COEFICENT,
                pond_area_m2=POND_AREA,
                water_level_cm=100,
                water_level_min_cm=WATER_LEVEL_MIN,
                water_level_max_cm=WATER_LEVEL_MAX,
                rain_data_mm=ArtificialConstRain(20)))

        # LOOP
        while True:
            try:
                # READ SENSOR
                avg_dist, invariance = controler.read_sensor()

                # STEP FILTERS
                kalman_bank.step_filters(MeasurementData(avg_dist, invariance))

                # Analyze
                # TODO: analyze the filters
            except serial_exceptions.exceptions as e:
                handle_controler_exeption(e)

            # STEP TIME AND WAIT
            TIME.step()
            pause.until(START + TIME.get_current_time)
    except Exception as e:
        print(e)
        LOGGER.log(
            "Fatal error shutting down",
            level=LogLevel.CRITICAL_ERROR)
        raise e
