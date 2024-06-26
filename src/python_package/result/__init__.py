"""
Contains a super class Result that can be used if a function might return an Error
Return Ok(value) or a class derived from it if function is a success
Return Error or a class derived from it if function is a failure
"""

from typing import Generic, TypeVar, Callable
from ..logger import Log, LogLevel, PrintLogger

T = TypeVar("T")
U = TypeVar("U")


class Result(Generic[T]):
    "Can either be an Ok or an Error"

    def unwrap(self) -> T | None:
        """Returns the value if Result is Ok else returns None"""
        if self is Ok[T]:
            return self.value()  # pylint: disable=E1101
        return None

    def map(self, fn: Callable[[T], U]) -> "Ok[U] | None":
        """If the result is Ok then maps the value of the result"""
        if self is Ok[T]:
            return self.map(fn)
        return None


class Ok(Generic[T], Result[T]):
    "A success result"

    def __init__(self, value: T = None) -> None:
        """Creates a new result of type Ok"""
        self._value = value

    def map(self, fn: Callable[[T], U]) -> "Ok[U]":
        """Maps the value to a different value using fn"""
        return Ok(fn(self._value))

    def value(self):
        """Returns the contained value"""
        return self._value


class Error(Result):
    "An Failed Result"

    msg = "Error Not Defined"

    def __init__(self, logger: Log = PrintLogger()) -> None:
        """Creates a new undefined Error"""
        self._logger = logger

    def message(self) -> str:
        """Returns the method"""
        return self.msg

    def log(self, level: LogLevel) -> None:
        """Logs the method using the provided logger"""
        self._logger.log(self.message(), level)


class ValveError(Error):
    "A Valve Error"

    def __init__(self, logger: Log = PrintLogger()) -> None:
        """Creates a new Valve Error"""
        super().__init__(logger)

    def break_down(self):
        """Sets message to "Valve has broken down" """
        self.msg = "Valve has broken down"
        return self

    def inccorect_valve_ajustment(self):
        """
        Sets message to "Inccorect valve adjustment,
        leading to unexpecded sensor error"
        """
        self.msg = "Incorrect valve adjustment leading to unexpected sensor reading"
        return self


class ControllerError(Error):
    "A Controller Error"

    def __init__(self, logger: Log = PrintLogger()) -> None:
        """Creates a new Controller Error"""
        super().__init__(logger)

    def lost_connection_to_sensor(self):
        """Sets message to "Lost connection to sensor" """
        self.msg = "Lost connection to sensor"
        return self

    def lost_connection_to_valve(self):
        """Sets message to "Lost connection to valve" """
        self.msg = "Lost connection to valve"
        return self

    def lost_connection_to_weather(self):
        """Sets message to "Lost connection to weather" """
        self.msg = "Lost connection to weather data"
        return self


class SensorError(Error):
    "A Sensor Error"

    def __init__(self, logger: Log = PrintLogger()) -> None:
        """Creates a new Sensor Error"""
        super().__init__(logger)

    def not_mounted(self):
        """
        Sets message to "Sensor is not mounted correctly,
        might have fallen off"
        """
        self.msg = "Sensor is not mounted correctly, might have fallen off"
        return self

    def no_power(self):
        """Sets message to "Sensor has no power" """
        self.msg = "Sensor has no power"
        return self

    def unstable_power(self):
        """Sets message to "The power provided to the sensor is unstable" """
        self.msg = "The power provided to the sensor is unstable"
        return self

    def sensor_blocked(self):
        """Sets message to "Sensor is blocked" """
        self.msg = "Sensor is blocked"
        return self
