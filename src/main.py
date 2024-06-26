"THIS IS THE MAIN FILE"

import os
from datetime import timedelta, datetime
import pause
from python_package.plotter import plotting
from python_package.logger import LogLevel, PrintLogger
from python_package.serial import SerialCom, serial_exceptions
from python_package.serial.headless import Headless
from python_package.kalman_filter.kalman_bank import KalmanBank, Fault, KalmanError, FaultType
from python_package.kalman_filter.kalman import MeasurementData, PondState
from python_package.time import Time
from python_package.virtual_pond import VirtualPond
from python_package.args import ARGS, Mode
from python_package.out_mode import OutMode


LOGGER = PrintLogger()
FAULTS = [
    Fault(lambda x: x + 50.0, "higher", FaultType.ADD),
    Fault(lambda x: x - 50.0, "lower", FaultType.SUBTRACT),
    Fault(lambda x: x * 1.15, "higher", FaultType.MULTIPLY),
    Fault(lambda x: x * 0.85, "lower", FaultType.MULTIPLY),
]

# -- POND DATA
URBAN_CATCHMENT_AREA = 1.85
SURFACE_REACTION_FACTOR = 0.25
DISCHARGE_COEFICENT = 0.6
POND_AREA = 5572
WATER_LEVEL_MIN = 100
WATER_LEVEL_MAX = 850

# -- DELAY
KALMAN_DELAY = 50


def handle_controler_exception(exception: serial_exceptions.Exceptions):
    """Function for loggin serial module exceptions"""
    match exception:
        case serial_exceptions.Exceptions.NO_RESPONSE:
            LOGGER.log("No responce from device", level=LogLevel.ERROR)
        case serial_exceptions.Exceptions.INCORRECT_INPUT:
            LOGGER.log("Incorrect input to physical setup", level=LogLevel.ERROR)
        case serial_exceptions.Exceptions.PUMP_VALUE_OUT_OF_BOUNDS:
            LOGGER.log("Pump value was out of bounds", level=LogLevel.ERROR)
        case serial_exceptions.Exceptions.NO_SENSOR_READINGS:
            LOGGER.log("No readings from the sensor in the physical setup", level=LogLevel.ERROR)
        case serial_exceptions.Exceptions.COMUNICATION_ERROR:
            LOGGER.log("Data recieved from controller is outside specifications", level=LogLevel.ERROR)
        case serial_exceptions.Exceptions.CONVERSION_ERROR:
            LOGGER.log("Could not parse the data form sensor", level=LogLevel.ERROR)
        case serial_exceptions.Exceptions.SENSOR_READS_ZERO:
            LOGGER.log("Distance is reading zero", level=LogLevel.ERROR)


def handle_kalman_exception(exception: KalmanError):
    """Function for loggin kalman exceptions"""
    match exception:
        case KalmanError.LOWER_THRESHOLD_EXCEEDED:
            LOGGER.log("Lower threshhold exceeded in filter", level=LogLevel.WARNING)
        case KalmanError.HIGHER_THRESHOLD_EXCEEDED:
            LOGGER.log("Higher threshhold exceeded in filter", level=LogLevel.WARNING)


if __name__ == "__main__":
    try:
        LOGGER.log("SETUP")
        # SETUP
        CHANGE_MODE_TIME = 0
        change_array = []

        # -- TIME
        START = datetime.now()
        TIME = Time(start=START, current_time=timedelta(seconds=0), delta=timedelta(seconds=11))

        # -- ARGUMENTS
        args = ARGS(START)

        # -- TRUNCATE OUTPUT
        with open(args.out, "w", -1, "UTF-8") as f:
            f.truncate()

        # -- CONTROLER
        os.makedirs(args.controler_cache, exist_ok=True)
        controler = SerialCom(args.controler_cache)
        match args.mode:
            case Mode.SERIEL:
                controler.begin()
            case Mode.HEADLESS:
                controler.arduino = Headless(args.data, TIME)

        # -- RAIN
        rain = args.rain

        # -- VIRTUAL POND
        virtual_pond = VirtualPond(
            urban_catchment_area_ha=URBAN_CATCHMENT_AREA,
            surface_reaction_factor=SURFACE_REACTION_FACTOR,
            discharge_coeficent=DISCHARGE_COEFICENT,
            pond_area_m2=POND_AREA,
            water_level_cm=700,
            water_level_min_cm=WATER_LEVEL_MIN,
            water_level_max_cm=WATER_LEVEL_MAX,
            time=TIME,
            rain_data_mm=rain,
        )
        virtual_pond.set_orifice("med")

        # -- KALMAN BANK
        kalman_bank = KalmanBank(
            faults=FAULTS, time=TIME, initial_state=700, initial_variance=100, noice=0.1, out_file=args.kalman
        )

        AVG_DIST = 0
        OUT = 0

        out_mode = OutMode.SENSOR

        # LOOP
        while TIME.get_current_time.total_seconds() < args.time:
            # STEP VIRTUAL POND
            pond_data = virtual_pond.generate_virtual_sensor_reading()
            virtual_pond.water_level = pond_data.height
            if pond_data.overflow:
                LOGGER.log("Pond is overflowing", LogLevel.WARNING)

            if out_mode is not OutMode.SENSOR_ERROR:
                try:
                    # READ SENSOR
                    AVG_DIST, invariance = controler.read_sensor()
                    OUT = AVG_DIST

                    # STEP FILTERS
                    kalman_bank.step_filters(
                        PondState(q_in=pond_data.volume_in, q_out=pond_data.volume_out, ap=POND_AREA),
                        MeasurementData(AVG_DIST, invariance),
                        virtual_pond.water_level,
                    )

                except serial_exceptions.Exceptions as e:
                    if out_mode != OutMode.SENSOR_ERROR:
                        out_mode = OutMode.SENSOR_ERROR
                        CHANGE_MODE_TIME = TIME.get_current_time.total_seconds()
                        change_array.append([out_mode, CHANGE_MODE_TIME])
                    handle_controler_exception(e)
                except KalmanError as e:
                    if TIME.get_current_time.total_seconds() > KALMAN_DELAY:
                        handle_kalman_exception(e)
                        if out_mode != OutMode.VIRTUAL:
                            out_mode = OutMode.VIRTUAL
                            change_mode_time = TIME.get_current_time.total_seconds()
                            change_array.append([out_mode, change_mode_time])

            if out_mode is OutMode.VIRTUAL:
                OUT = virtual_pond.water_level
            elif out_mode is OutMode.SENSOR_ERROR:
                OUT = virtual_pond.water_level

            # OUTPUT
            with open(args.out, "a", -1, "UTF-8") as f:
                f.write(f"{TIME.get_current_time.total_seconds()},{OUT}\n")

            # STEP TIME AND WAIT
            TIME.step()
            if args.mode == Mode.SERIEL:
                pause.until(START + TIME.get_current_time)

        # END LOOP
        plotting(args, WATER_LEVEL_MIN, WATER_LEVEL_MAX, change_array)
    except Exception as e:
        print(e)
        LOGGER.log("Fatal error shutting down", level=LogLevel.CRITICAL_ERROR)
        raise e
