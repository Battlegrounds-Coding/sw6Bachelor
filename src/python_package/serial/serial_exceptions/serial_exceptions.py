"""Custom exception class for the project"""

from enum import Enum


class Exceptions(Exception, Enum):
    """Exeption class with enums for specifing error"""

    NO_RESPONSE = 0
    """Comunication timed oud"""
    INCORRECT_INPUT = 4
    """Input value out of bounds"""
    CONVERSION_ERROR = 5
    """Failed to find int"""
    COMUNICATION_ERROR = 6
    """Read values should not be possible"""
    SENSOR_READS_ZERO = 7
    """Distance sensor reads zero"""

    # Controller errors:
    INCORECT_DISTANCE_READING = 1
    PUMP_VALUE_OUT_OF_BOUNDS = 2
    NO_SENSOR_READINGS = 3


class ExceptionEnum(Enum):
    """Enum over serial communication errors"""

    NO_RESPONSE = 0
    """Comunication timed oud"""
    INCORRECT_INPUT = 4
    """Input value out of bounds"""
    CONVERSION_ERROR = 5  #
    """Failed to find int"""
    COMUNICATION_ERROR = 6
    """Read values should not be possible"""
    SENSOR_READS_ZERO = 7
    """Distance sensor reads zero"""

    # Controller errors:
    INCORECT_DISTANCE_READING = 1
    PUMP_VALUE_OUT_OF_BOUNDS = 2
    NO_SENSOR_READINGS = 3
