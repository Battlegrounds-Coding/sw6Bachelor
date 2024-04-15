"""Custom exception class for the project"""

from enum import Enum


class exceptions(Exception, Enum):
    """Exeption class with enums for specifing error"""

    NO_RESPONSE = 1
    PUMP_VALUE_OUT_OF_BOUNDS = 2
