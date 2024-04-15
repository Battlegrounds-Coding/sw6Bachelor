"""Custom exception class for the project"""

from enum import Enum


class Error(Exception, Enum):
    """Exeption class with enums for specifing error"""

    NO_RESPONSE = 1
