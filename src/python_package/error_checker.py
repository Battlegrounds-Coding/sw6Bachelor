from abc import abstractmethod
from result import Result, Ok


class Data:
    pass


class ErrorCheker:
    @abstractmethod
    def check(self, pond: Data, virtual_pond: Data) -> Result[None]:
        """Checks the power  t"""
        ...


class SensorChecker(ErrorCheker):
    def check(self, pond: Data, virtual_pond: Data) -> Result[None]:
        return Ok()
