"THIS IS THE MAIN FILE"

from python_package.log import LogLevel, PrintLogger
from python_package.serial import SerialCom, serial_exceptions
from python_package.serial.headless import Headless
from python_package.kalman_filter.kalman_bank import KalmanBank, Fault
from python_package.kalman_filter.kalman import MeasurementData, PondState
from python_package.time import Time
from python_package.virtual_pond import VirtualPond
from python_package.rain.artificial_rain import ArtificialConstRain
from python_package.plotter import plot
from datetime import timedelta, datetime
import csv
import numpy as np
import matplotlib.pyplot as plt
import pause
from python_package.args import ARGS, Mode

def plotting(rain_file:str, data:str, data_control:str):
    plt.figure()
    plt.subplot(211)
    p1 = plot(rain_file, "red", "Rain", 1)
    plt.ylabel("Rain mm")

    plt.subplot(212)
    p2 = plot(virtual_pond_file, "blue", "virtual pond test", 1)
    
    p3 = plot(data, "red", "Control fixed", 1)
    p4 = plot(data_control, "green", "Control optimal", 1)

    plt.ylabel("Water level cm")

    plt.xlabel("Time sec")

    plt.legend()
    plt.show()

LOGGER = PrintLogger()
FAULTS = [
    Fault(lambda x: x + 10, "lower"),
    Fault(lambda x: x - 10, "lower"),
    Fault(lambda _: MeasurementData(10, 0), "lower"),
    Fault(lambda _: MeasurementData(0, 0), "lower"),
]

# -- POND DATA
URBAN_CATCHMENT_AREA = 1.85
SURFACE_REACTION_FACTOR = 0.25
DISCHARGE_COEFICENT = 0.6
POND_AREA = 5572
WATER_LEVEL_MIN = 100
WATER_LEVEL_MAX = 850


def handle_controler_exeption(exception: serial_exceptions.exceptions):
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
            LOGGER.log("Failed to communicate with device", level=LogLevel.ERROR)
        case serial_exceptions.exceptions.CONVERSION_ERROR:
            LOGGER.log("Could not parse the data form sensor", level=LogLevel.ERROR)
    
if __name__ == "__main__":
    try:
        LOGGER.log("SETUP")
        # SETUP
        # -- TIME
        START = datetime.now()
        TIME = Time(
            start=START,
            current_time=timedelta(seconds=0), 
            delta=timedelta(seconds=10))

        virtual_pond_file = "data\\VirtualPondData.csv"
        vp_file = open(virtual_pond_file, "w")
        vp_file.truncate()
        vp_file.close()

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
            rain_data_mm=rain)
        virtual_pond.set_orifice("med")


        # -- KALMAN BANK
        kalman_bank = KalmanBank(
            faults=FAULTS,
            time=TIME,
            initial_state=100,
            initial_variance=10,
            noice=0.1)

        # LOOP
        while TIME.get_current_time.total_seconds() < 1000:
            try:
                # READ SENSOR
                avg_dist, invariance = controler.read_sensor()

                # STEP VIRTUAL POND
                pond_data = virtual_pond.generate_virtual_sensor_reading()
                virtual_pond.water_level = pond_data.height

                # STEP FILTERS
                kalman_bank.step_filters(
                    PondState(q_in=pond_data.volume_in, q_out=pond_data.volume_out, ap=POND_AREA),
                    MeasurementData(avg_dist, invariance))
                
                # Analyze
                # TODO: analyze the filters
            except serial_exceptions.exceptions as e:
                handle_controler_exeption(e)

            # STEP TIME AND WAIT
            TIME.step()
            if args.mode == Mode.SERIEL:
                pause.until(START + TIME.get_current_time)
    except Exception as e:
        print(e)
        LOGGER.log("Fatal error shutting down", level=LogLevel.CRITICAL_ERROR)
        raise e
    plotting(args.rain_file, args.data, args.data_control)


