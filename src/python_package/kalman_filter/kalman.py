"THIS FILE CONTAINS THE IMPLEMENTATION OF THE KALMAN FILTER"

from abc import abstractmethod
from typing import Self
from datetime import timedelta
import numpy as np


class Data:
    "An abstract class that contains data from Kalman filters"
    def __eq__(self, other: Self) -> bool:
        return self.height() == other.height()

    @abstractmethod
    def height(self) -> np.float64:
        "Returns the current height above min"


class MeasurementData(Data):
    "An abstract class for defining measurements, implements Data and adds a variance function"

    def __eq__(self, other: Self) -> bool:
        return super().__eq__(other) and self.variance_height() == other.variance_height()

    @abstractmethod
    def variance_height(self) -> np.float64:
        "Returns the variance of the measurements"


class Kalman:
    "Kalman filter class"
    def __init__(
        self,
        initial_state: np.float64,
        initial_variance: np.float64,
        delta: timedelta,
        noice: np.float64 = np.float64(0.0),
    ):
        self.state = initial_state
        self.variance = initial_variance
        self.delta = np.float64(delta.total_seconds())
        self.noice = noice
        self.predict_state = self.state
        self.predict_variance = self.variance

    def __eq__(self, other: Self) -> bool:
        "Equals function. Checks if all the data between two filters are the same"
        return (
            self.state == other.get_state
            and self.variance == other.get_variance
            and self.delta == other.get_delta
            and self.noice == other.get_noice
            and self.predict_state == other.get_predict_state
            and self.predict_variance == other.get_predict_variance
        )

    def step(self, predict_data: Data, messured_data: MeasurementData):
        "Steps a kalman filter using pridicted data and measured data"
        # Update
        kalman_gain = self.predict_variance / (self.predict_variance + messured_data.variance_height())

        variance = (1 - kalman_gain) * self.variance

        state = self.predict_state + kalman_gain * (messured_data.height() - self.predict_state)

        # Predict
        predict_state = state
        predict_variance = variance + self.noice

        self.state = state
        self.variance = variance
        self.predict_state = predict_state
        self.predict_variance = predict_variance

    def print_kalman_filter(self) -> None:
        "Prints all properties of a Kalman class"
        print(
            "State: "
            + str(self.state)
            + ", "
            + "Variance: "
            + str(self.variance)
            + ", "
            + "Delta: "
            + str(self.delta)
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
    def current_state(self) -> np.float64:
        return self.state

    @property
    def get_state(self) -> np.float64:
        return self.state

    @property
    def get_variance(self) -> np.float64:
        return self.variance

    @property
    def get_delta(self) -> np.float64:
        return self.delta

    @property
    def get_noice(self) -> np.float64:
        return self.noice

    @property
    def get_predict_state(self) -> np.float64:
        return self.predict_state

    @property
    def get_predict_variance(self) -> np.float64:
        return self.predict_variance
    