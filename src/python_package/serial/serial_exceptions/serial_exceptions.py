"""Custom exception class for the project"""

from enum import Enum


class exceptions(Exception, Enum):
    """Exeption class with enums for specifing error"""

    #     return enu
    NO_RESPONSE = 0
    """Comunication timed oud"""
    INCORRECT_INPUT = 4
    """Input value out of bounds"""
    CONVERSION_ERROR = 5
    """Failed to find int"""
    COMUNICATION_ERROR = 6
    """Read values should not be possible"""

    # Controller errors:
    INCORECT_DISTANCE_READING = 1
    PUMP_VALUE_OUT_OF_BOUNDS = 2
    NO_SENSOR_READINGS = 3


class enum(Enum):
    NO_RESPONSE = 0
    """Comunication timed oud"""
    INCORRECT_INPUT = 4
    """Input value out of bounds"""
    CONVERSION_ERROR = 5  #
    """Failed to find int"""
    COMUNICATION_ERROR = 6
    """Read values should not be possible"""

    # Controller errors:
    INCORECT_DISTANCE_READING = 1
    PUMP_VALUE_OUT_OF_BOUNDS = 2
    NO_SENSOR_READINGS = 3
