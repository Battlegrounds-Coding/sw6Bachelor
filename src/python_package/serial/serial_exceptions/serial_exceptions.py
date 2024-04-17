"""Custom exception class for the project"""

from enum import Enum


class exceptions(Exception, Enum):
    """Exeption class with enums for specifing error"""

    NO_RESPONSE = 0
    INCORRECT_INPUT = 4
    CONVERSION_ERROR = 5

    # Controller errors:
    INCORECT_DISTANCE_READING = 1
    PUMP_VALUE_OUT_OF_BOUNDS = 2
    NO_SENSOR_READINGS = 3
