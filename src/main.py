"THIS IS THE MAIN FILE"

import os
from enum import Enum
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import pause
from python_package.logger import LogLevel, PrintLogger
from python_package.serial import SerialCom, serial_exceptions
from python_package.serial.headless import Headless
from python_package.kalman_filter.kalman_bank import KalmanBank, Fault, KalmanError
from python_package.kalman_filter.kalman import MeasurementData, PondState
from python_package.time import Time
from python_package.virtual_pond import VirtualPond
from python_package.plotter import plot, plot_kalman_filters_delta, plot_kalman_filters_state_measured
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import pause
import os
import sys
from pathlib import Path
from python_package.args import ARGS, Mode


class OutMode(Enum):
    """Enum for defining Sensor or virtual height value"""

    SENSOR = 0
    VIRTUAL = 1


def plotting(plot_args: ARGS):
    """Function for plotting data"""

    directory = "experiment_data_results"
    if not os.path.exists(directory):
        os.makedirs(directory)

    test_file = "bob"

    # test_file = "hej"
    axs = plt.subplots(4, 1, figsize=(10, 5), gridspec_kw={"height_ratios": [1, 1, 2, 2]})[1]

    plt.suptitle(f"File: {test_file}")

    plot(args.rain_file, "red", "Rain", 1, axs[0])
    axs[0].set_ylabel("Rain mm")

    plot(args.out, "blue", "Virtual pond", 1, axs[1])
    plot(args.data, "red", "Sensor", 1, axs[1])
    plot(args.data_control, "green", "Control, fixed orifice", 1, axs[1])
    axs[1].set_ylim(0, 900)
    axs[1].set_ylabel("Water level cm")
    axs[1].set_xlabel("Time sec")
    axs[0].legend()

    plot(plot_args.out, "blue", "Estimated height", 1, axs[1])
    plot(plot_args.data, "red", "Sensor height", 1, axs[1])
    plot(plot_args.data_control, "green", "Control, fixed orifice", 1, axs[1])
    axs[1].set_ylim(0, 900)
    axs[1].set_ylabel("Water level cm")
    axs[1].set_xlabel("Time sec")
    axs[1].legend()

    color_label_tuples = [
        ("blue", "Main filter"),
        ("red", "Constant offset 10"),
        ("yellow", "Constant offset -10"),
        ("green", "10 Percent over"),
        ("purple", "10 percent under"),
    ]
    plot_kalman_filters_delta(args.kalman, color_label_tuples, 1, axs[2])
    plot_kalman_filters_state_measured(args.kalman, color_label_tuples, 1, axs[3])
    axs[2].legend()

    plt.savefig(f"experiment_data_results/test_{test_file}.png", bbox_inches="tight")
    plt.show()


LOGGER = PrintLogger()
FAULTS = [
    Fault(lambda x: x + 300.0, "higher"),
    Fault(lambda x: x - 300.0, "lower"),
    Fault(lambda x: x * 1.2, "higher"),
    Fault(lambda x: x * 0.80, "lower"),
]

# -- POND DATA
URBAN_CATCHMENT_AREA = 1.85
SURFACE_REACTION_FACTOR = 0.25
DISCHARGE_COEFICENT = 0.6
POND_AREA = 5572
WATER_LEVEL_MIN = 100
WATER_LEVEL_MAX = 850


def handle_controler_exeption(exception: serial_exceptions.exceptions):
    """Function for itteration over serial module exceptions"""
    match exception:
        case serial_exceptions.exceptions.NO_RESPONSE:
            LOGGER.log("No responce from device", level=LogLevel.ERROR)
        case serial_exceptions.exceptions.INCORRECT_INPUT:
            LOGGER.log("Incorrect input to physical setup", level=LogLevel.ERROR)
        case serial_exceptions.exceptions.PUMP_VALUE_OUT_OF_BOUNDS:
            LOGGER.log("Pump value was out of bounds", level=LogLevel.ERROR)
        case serial_exceptions.exceptions.NO_SENSOR_READINGS:
            LOGGER.log("No readings from the sensor in the physical setup", level=LogLevel.ERROR)
        case serial_exceptions.exceptions.COMUNICATION_ERROR:
            LOGGER.log("Data recieved from controller is outside specifications", level=LogLevel.ERROR)
        case serial_exceptions.exceptions.CONVERSION_ERROR:
            LOGGER.log("Could not parse the data form sensor", level=LogLevel.ERROR)
        case serial_exceptions.exceptions.SENSOR_READS_ZERO:
            LOGGER.log("Distance is reading zero", level=LogLevel.ERROR)


if __name__ == "__main__":
    try:
        LOGGER.log("SETUP")
        # SETUP
        # -- TIME
        START = datetime.now()
        TIME = Time(start=START, current_time=timedelta(seconds=0), delta=timedelta(seconds=10))

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

        # -- CASHE
        # TODO: INIT CASHE

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
            faults=FAULTS, time=TIME, initial_state=700, initial_variance=10, noice=0.1, out_file=args.kalman
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

            if out_mode is OutMode.SENSOR:
                try:
                    # READ SENSOR
                    AVG_DIST, invariance = controler.read_sensor()
                    OUT = AVG_DIST

                    # STEP FILTERS
                    kalman_bank.step_filters(
                        PondState(q_in=pond_data.volume_in, q_out=pond_data.volume_out, ap=POND_AREA),
                        MeasurementData(AVG_DIST, invariance),
                    )
                except serial_exceptions.exceptions as e:
                    out_mode = OutMode.VIRTUAL
                    handle_controler_exeption(e)
                except KalmanError as e:
                    if TIME.get_current_time.seconds > 100:
                        out_mode = OutMode.VIRTUAL
                        print(e)

            if out_mode is OutMode.VIRTUAL:
                OUT = virtual_pond.water_level

            # OUTPUT
            with open(args.out, "a", -1, "UTF-8") as f:
                f.write(f"{TIME.get_current_time.total_seconds()},{OUT}\n")

            # STEP TIME AND WAIT
            TIME.step()
            if args.mode == Mode.SERIEL:
                pause.until(START + TIME.get_current_time)
    except Exception as e:
        print(e)
        LOGGER.log("Fatal error shutting down", level=LogLevel.CRITICAL_ERROR)
        LOGGER.log("Fatal error shutting down", level=LogLevel.CRITICAL_ERROR)
        raise e
    plotting(args)
