"THIS FILE CONTAINS A BANK OF KALMAN FILTERS"
from typing import List, Callable, Self
from .kalman import Kalman, MeasurementData, Data
from datetime import timedelta
import numpy as np


class KalmanBank:
    "A bank of Kalman filters with faults defined by the user. When initialized, all filters are identical."

    def __init__(
        self,
        faults: List[Callable[[MeasurementData], MeasurementData]],
        initial_state: np.float64,
        initial_variance: np.float64,
        delta: timedelta,
        noice: np.float64 = np.float64(0.0),
    ):
        self.faults = faults
        self.kalman_bank: List[Kalman] = []

        # create a kalman filter for each fault and append in kalman_bank
        for _ in faults:
            self.kalman_bank.append(Kalman(initial_state, initial_variance, delta, noice))

    def __eq__(self, other: Self) -> bool:
        return self.faults == other.get_faults and self.kalman_bank == other.get_kalman_bank

    @property
    def get_kalman_bank(self) -> List[Kalman]:
        "returns the List of Kalman filters"
        return self.kalman_bank

    @property
    def get_faults(self) -> List[Callable[[MeasurementData], MeasurementData]]:
        "returns the list of faults"
        return self.faults

    def print_bank(self):
        "Prints the field variables of each filter in the KalmanBank"
        for f in self.kalman_bank:
            f.print_kalman_filter()
            # print_bank is broken somewhere

    def add_faults(
        self,
        new_faults: List[Callable[[MeasurementData], MeasurementData]],
        initial_state: np.float64,
        initial_variance: np.float64,
        delta: timedelta,
        noice: np.float64 = np.float64(0.0),
    ):
        "Adds new faults and creates filters for them."
        for f in new_faults:
            if not f in self.faults:
                self.faults.append(f)
                # create kalman filter with f and append in kalman_bank
                self.kalman_bank.append(Kalman(initial_state, initial_variance, delta, noice))

    def step_filters(self, predicted_data: Data, measured_data: MeasurementData):
        "Calls the step function for each filter with each fault"
        i = 0
        for k in self.kalman_bank:
            k.step(predicted_data, self.faults[i](measured_data))
            i += 1
