"THIS FILE CONTAINS THE IMPLEMENTATION OF THE KALMAN FILTER"

from abc import abstractmethod
from typing import Self
from ..time import Time
from ..virtual_pond import VirtualPond


class MeasurementData:
    "An abstract class for defining measurements, implements Data and adds a variance function"

    def __init__(self, height: float, variance: float):
        self._height = height
        self._variance = variance

    def __eq__(self, other) -> bool:
        "Equals function checks if the measured height is the same between two objects"
        if other is not Self:
            return False
        return self.variance_height() == other.variance_height() and self.height() == other.height()

    def height(self) -> float:
        "Returns the current height above min"
        return self._height

    def variance_height(self) -> float:
        "Returns the variance of the measurements"
        return self._variance

    def __add__(self, other: float | tuple[float, float]) -> "MeasurementData":
        if other is tuple[float, float]:
            return MeasurementData(self.height() + other[0], self.variance_height() + other[1])
        elif other is float:
            return MeasurementData(self.height() + other, self.variance_height())
        return self

    def __sub__(self, other: float | tuple[float, float]) -> "MeasurementData":
        if other is tuple[float, float]:
            return MeasurementData(self.height() - other[0], self.variance_height() - other[1])
        elif other is float:
            return MeasurementData(self.height() - other, self.variance_height())
        return self

    def __mul__(self, other: float | tuple[float, float]) -> "MeasurementData":
        if other is tuple[float, float]:
            return MeasurementData(self.height() - other[0], self.variance_height() - other[1])
        elif other is float:
            return MeasurementData(self.height() - other, self.variance_height())
        return self

    def __div__(self, other: float | tuple[float, float]) -> "MeasurementData":
        if other is tuple[float, float]:
            return MeasurementData(self.height() / other[0], self.variance_height() / other[1])
        elif other is float:
            return MeasurementData(self.height() / other, self.variance_height())
        return self


class Kalman:
    "Kalman filter class"

    def __init__(
        self,
        initial_variance: float,
        time: Time,
        virtual_pond: VirtualPond,
        noice: float = float(0.0),
    ):
        "Constructor for Kalman filter class"
        self.variance = initial_variance
        self.time = time
        self.noice = noice
        self.predict_state = virtual_pond.water_level
        self.predict_variance = self.variance
        self.virtual_pond = virtual_pond

    def __eq__(self, other) -> bool:
        "Equals function. Checks if all the data between two filters are the same"
        if other is not Self:
            return False
        return (
            self.variance == other.get_variance
            and self.get_time.get_current_time == other.get_time.get_current_time
            and self.get_time.get_delta == other.get_time.get_delta
            and self.noice == other.get_noice
            and self.get_state == other.get_state
            and self.predict_variance == other.get_predict_variance
            and self.virtual_pond == other.virtual_pond
        )

    def step(self, messured_data: MeasurementData):
        "Steps a kalman filter using pridicted data and measured data"
        # Update
        kalman_gain = self.predict_variance / (self.predict_variance + messured_data.variance_height())

        variance = (1 - kalman_gain) * self.variance

        s = self.virtual_pond.generate_virtual_sensor_reading(self.time.get_delta).height
        state = s + kalman_gain * (messured_data.height() - s)

        # Predict
        predict_variance = variance + self.noice
        self.virtual_pond.water_level = state
        self.variance = variance
        self.predict_variance = predict_variance

    def print_kalman_filter(self) -> None:
        "Prints all properties of a Kalman class"
        print(
            "State: "
            + str(self.get_state)
            + ", "
            + "Variance: "
            + str(self.variance)
            + ", "
            + "Delta: "
            + str(self.time.get_delta)
            + ", "
            + "Noice: "
            + str(self.noice)
            + ", "
            + "Predict_state: "
            + str(self.predict_state)
            + ", "
            + "Predict_variance: "
            + str(self.predict_variance)
        )

    @property
    def get_variance(self) -> float:
        "Getter method for variance"
        return self.variance

    @property
    def get_time(self) -> Time:
        "Getter method for delta"
        return self.time

    @property
    def get_noice(self) -> float:
        "Getter method for noice"
        return self.noice

    @property
    def get_state(self) -> float:
        "Getter method for the current state of the filter"
        return self.virtual_pond.water_level

    @property
    def get_predicted_state(self) -> float:
        return self.predict_state

    @property
    def get_predict_variance(self) -> float:
        "Getter method for predict_variance"
        return self.predict_variance
