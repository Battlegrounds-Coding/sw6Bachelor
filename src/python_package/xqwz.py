"THIS FILE CONTAINS THE IMPLEMENTATION OF THE CALMAN FILTER"

from abc import abstractmethod
import numpy as np
from datetime import timedelta


class Data:
    @abstractmethod
    def height(self) -> np.float32:
        "Returns the current height above min"


class MessurementData(Data):
    "An abstract class for defining messurements, implements Data and adds a variance function"

    @abstractmethod
    def variance_height(self) -> np.float32:
        "Returns the variance of the messurements"


class Xqwz:
    def __init__(self, initial_state: np.float32, initial_variance: np.float32, delta: timedelta, noice: np.float32 = np.float32(0.0)):
        self.state = initial_state
        self.variance = initial_variance
        self.delta = np.float32(delta.total_seconds())
        self.noice = noice

        self.predict_state = self.state
        self.predict_variance = self.variance

    def step(self, predict_data: Data, messured_data: MessurementData):
        # Update
        kalman_gain = self.predict_variance / (self.predict_variance + messured_data.variance_height())
        variance = (1 - kalman_gain) * self.variance
        state = self.predict_state + kalman_gain * (messured_data.height() - self.predict_state)

        # Predict
        predict_state = predict_data.height() + self.noice
        predict_variance = variance

        self.state = state
        self.variance = variance
        self.predict_state = predict_state
        self.predict_variance = predict_variance

    def current_state(self) -> np.float32:
        return self.state


