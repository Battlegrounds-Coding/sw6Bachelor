"THIS FILE CONTAINS THE IMPLEMENTATION OF THE KALMAN FILTER"

from abc import abstractmethod
from typing import Self
from ..time import Time
from ..virtual_pond import VirtualPond


class PondState:
    def __init__(self, q_in: float, q_out: float, ap: float):
        self.q_in = q_in
        self.q_out = q_out
        self.ap = ap


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
        initial_state: float,
        initial_variance: float,
        time: Time,
        noice: float = float(0.0),
    ):
        "Constructor for Kalman filter class"
        self.state = initial_state
        self.predict_state = initial_state
        self.variance = initial_variance
        self.predict_variance = self.variance
        self.time = time
        self.noice = noice

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
        )

    def step(self, pond_state: PondState, messured_data: MeasurementData):
        "Steps a kalman filter using pridicted data and measured data"
        # Update
        kalman_gain = self.predict_variance / (self.predict_variance + messured_data.variance_height())
        variance = (1 - kalman_gain) * self.variance
        state = self.predict_state + kalman_gain * (messured_data.height() - self.predict_state)

        # Predict
        t = self.time.get_delta.total_seconds()
        predict_state = t * (pond_state.q_in - pond_state.q_out) / pond_state.ap + state
        predict_variance = variance + self.noice

        # Set Values
        self.state = state
        self.predict_state = predict_state
        self.variance = variance
        self.predict_variance = predict_variance

    def print_kalman_filter(self) -> str:
        "Prints all properties of a Kalman class"
        print_string = (
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
        print(print_string)
        return print_string

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
        return self.state

    @property
    def get_predicted_state(self) -> float:
        "Getter method for the predicted state of the kalman filter"
        return self.predict_state

    @property
    def get_predict_variance(self) -> float:
        "Getter method for predict_variance"
        return self.predict_variance
