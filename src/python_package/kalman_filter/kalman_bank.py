"THIS FILE CONTAINS A BANK OF KALMAN FILTERS"
from typing import List, Callable, Self
from .kalman import Kalman, MeasurementData
from ..virtual_pond import VirtualPond
from ..time import Time
import copy


class KalmanBank:
    "A bank of Kalman filters with faults defined by the user. When initialized, all filters are identical."

    def __init__(
        self,
        faults: List[Callable[[MeasurementData], MeasurementData]],
        initial_variance: float,
        time: Time,
        virtual_pond: VirtualPond,
        noice: float,
    ):
        self.faults = []
        self.kalman_bank: List[Kalman] = []
        self.initial_variance = initial_variance
        self.time = time
        self.virtual_pond = virtual_pond
        self.noice = noice

        self.add_faults(faults)

    def __eq__(self, other: Self) -> bool:
        "Equals function. If all properties of two KalmanBanks are equals, they are considered equal banks"
        return (
            self.faults == other.get_faults
            and self.kalman_bank == other.get_kalman_bank
            and self.initial_variance == other.get_initial_variance
            and self.time.get_current_time == other.get_time.get_current_time
            and self.time.get_delta == other.get_time.get_delta
            and self.noice == other.get_noice
            and self.get_virtual_pond == other.get_virtual_pond
        )

    @property
    def get_kalman_bank(self) -> List[Kalman]:
        "returns the List of Kalman filters"
        return self.kalman_bank

    @property
    def get_faults(self) -> List[Callable[[MeasurementData], MeasurementData]]:
        "returns the list of faults"
        return self.faults

    @property
    def get_initial_variance(self) -> float:
        "returns the initial variance as a float"
        return self.initial_variance

    @property
    def get_time(self) -> Time:
        "Returns the time class"
        return self.time

    @property
    def get_virtual_pond(self) -> VirtualPond:
        "Returns the virtual pond used to create Kalman filters"
        return self.virtual_pond

    @property
    def get_noice(self) -> float:
        "Returns the noice as a float"
        return self.noice

    def print_bank(self):
        "Prints the field variables of each filter in the KalmanBank"
        for f in self.kalman_bank:
            f.print_kalman_filter()

    def add_faults(
        self,
        new_faults: List[Callable[[MeasurementData], MeasurementData]],
    ):
        "Adds new faults and creates filters for them."
        for f in new_faults:
            if f not in self.faults:
                self.faults.append(f)
                # create kalman filter with f and append in kalman_bank
                self.kalman_bank.append(
                    Kalman(self.initial_variance, self.time, copy.copy(self.virtual_pond), self.noice)
                )

    def step_filters(self, measured_data: MeasurementData):
        "Calls the step function for each filter with each fault"
        i = 0
        for k in self.kalman_bank:
            k.step(self.faults[i](measured_data))
            i += 1
