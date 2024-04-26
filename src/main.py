"THIS IS THE MAIN FILE"

from python_package.log import LogLevel, PrintLogger
from python_package.serial import SerialCom, serial_exceptions
from datetime import timedelta, datetime
import pause


DELTA = timedelta(seconds=10)
LOGGER = PrintLogger()


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

        # -- CONTROLER
        controler = SerialCom()
        controler.begin()

        # -- CASHE
        # TODO: INIT CASHE

        # -- KALMAN BANK
        # TODO: INIT KALMAN BANK

        # -- TIME
        now = datetime.now()
        START = now

        # LOOP
        while True:
            try:
                avg_dist, invariance = controler.read_sensor()
            except serial_exceptions.exceptions as e:
                handle_controler_exeption(e)
            # TODO: Step every instance with now - START

            now = max(datetime.now(), now + DELTA)
            pause.until(now)
    finally:
        LOGGER.log(
            "Fatal error shutting down",
            level=LogLevel.CRITICAL_ERROR)
        exit(1)

