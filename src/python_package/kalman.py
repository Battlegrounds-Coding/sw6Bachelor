"THIS FILE CONTAINS THE IMPLEMENTATION OF THE CALMAN FILTER"

from abc import abstractmethod
import numpy as np
from datetime import timedelta


class Data:
    @abstractmethod
    def height(self) -> np.float64:
        "Returns the current height above min"


class MessurementData(Data):
    "An abstract class for defining messurements, implements Data and adds a variance function"

    @abstractmethod
    def variance_height(self) -> np.float64:
        "Returns the variance of the messurements"


class Kalman:
    def __init__(self, initial_state: np.float64, initial_variance: np.float64, delta: timedelta, noice: np.float64 = np.float64(0.0)):
        self.state = initial_state
        self.variance = initial_variance
        self.delta = np.float64(delta.total_seconds())
        self.noice = noice

        self.predict_state = self.state
        self.predict_variance = self.variance

    def step(self, predict_data: Data, messured_data: MessurementData):
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

    def current_state(self) -> np.float64:
        return self.state


