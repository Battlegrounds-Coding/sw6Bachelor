"""
WORK IN PROGRESS
Contains basic supertypes for an error checker
"""

from abc import abstractmethod
from result import Result, Ok


class Data:  # pylint: disable=R0903
    """Data that is comming from the system"""


class ErrorCheker:  # pylint: disable=R0903
    """Interface for an error checker"""

    @abstractmethod
    def check(self, pond: Data, virtual_pond: Data) -> Result[None]:
        """Checks if there is an error in the data"""


class SensorChecker(ErrorCheker):  # pylint: disable=R0903
    """Dummy implementation of interface ErrorChecker"""

    def check(self, pond: Data, virtual_pond: Data) -> Result[None]:
        return Ok()
