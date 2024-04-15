"""Custom exception class for the project"""

from enum import Enum


class Error(Exception, Enum):
    """Exeption class with enums for specifing error"""

    no_response = 1
