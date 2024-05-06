"THIS FILE CONTAINS A BANK OF KALMAN FILTERS"
import copy
import numpy as np
import csv
from typing import List, Self
from .fault import Fault
from .kalman import Kalman, MeasurementData, PondState
from ..virtual_pond import VirtualPond
from ..time import Time


class KalmanBank:
    "A bank of Kalman filters with faults defined by the user. When initialized, all filters are identical."

    def __init__(
        self,
        faults: List[Fault],
        initial_state: float,
        initial_variance: float,
        time: Time,
        noice: float,
    ):
        self.faults = []
        self.initial_state = initial_state
        self.kalman_bank: List[Kalman] = [Kalman(initial_state, initial_variance, time, noice)]
        self.initial_variance = initial_variance
        self.time = time
        self.noice = noice

        self.add_faults(faults)

    def __eq__(self, other) -> bool:
        "Equals function. If all properties of two KalmanBanks are equals, they are considered equal banks"
        if other is KalmanBank:
            return (
                self.faults == other.get_faults
                and self.kalman_bank == other.get_kalman_bank
                and self.initial_variance == other.get_initial_variance
                and self.time.get_current_time == other.get_time.get_current_time
                and self.time.get_delta == other.get_time.get_delta
                and self.noice == other.get_noice
            )

        return False

    def print_bank(self):
        "Prints the field variables of each filter in the KalmanBank"
        for f in self.kalman_bank:
            f.print_kalman_filter()

    def add_faults(
        self,
        new_faults: List[Fault],
    ):
        "Adds new faults and creates filters for them."
        for f in new_faults:
            if f not in self.faults:
                self.faults.append(f)
                # create kalman filter with f and append in kalman_bank
                self.kalman_bank.append(Kalman(self.initial_state, self.initial_variance, self.time, self.noice))

    def step_filters(self, pond_state: PondState, measured_data: MeasurementData):
        "Calls the step function for each filter with each fault"
        faulty_filters: List[Kalman] = []
        fault_detection = self.analyze_filters(measured_data, faulty_filters)

        for i, k in enumerate(self.kalman_bank):
            if k == self.kalman_bank[0]:
                k.step(pond_state, measured_data)
            else:
                k.step(pond_state, self.faults[i - 1].get_fault(measured_data))
        self._write_to_csv(measured_data)

        if not fault_detection and not self.kalman_bank[0] == self.kalman_bank[1]:
            filter_report_string = "Waterlevel threshold exceeded in filters: \n"
            for f in faulty_filters:
                filter_report_string += f.print_kalman_filter() + "\n"
            filter_report_string += (
                "Kalman filter without arbitrary measurement data faults: \n"
                + self.kalman_bank[0].print_kalman_filter()
            )
            raise ValueError(
                "The measured water level exceeded the threshold in"
                + str(len(faulty_filters))
                + " kalman filters.\n"
                + "Measured water level: "
                + str(measured_data.height())
                + "\n"
                + filter_report_string
            )

    def analyze_filters(self, measured_data: MeasurementData, faulty_filters: List[Kalman]) -> bool:
        "Analyses filters in the KalmanBank. If measured_data goes past thresholds returns false, else return true"
        return self._analyze_higher_filters(measured_data, faulty_filters) and self._analyze_lower_filters(
            measured_data, faulty_filters
        )

    def _analyze_higher_filters(self, measured_data: MeasurementData, faulty_filters: List[Kalman]) -> bool:
        """
        Analyses the filters that are supposed to have a higher water height than the measured data.
        If measured data height is higher than the predicted data from the filters, return False. Else return True
        """
        higher_filters: List[Kalman] = []
        free_of_faults = True
        for i, k in enumerate(self.kalman_bank):
            if k == self.kalman_bank[0]:
                break
            if self.faults[i - 1].get_classification == "higher":
                higher_filters.append(self.kalman_bank[i])
        for f in higher_filters:
            if f.get_predicted_state < measured_data.height():
                faulty_filters.append(f)
                free_of_faults = False
        return free_of_faults

    def _analyze_lower_filters(self, measured_data: MeasurementData, faulty_filters: List[Kalman]) -> bool:
        """
        Analyses the filters that are supposed to have a lower water height than the measured data.
        If measured data height is lower than the predicted hight from any filter, return False, else return True
        """
        lower_filters: List[Kalman] = []
        free_of_faults = True
        for i, k in enumerate(self.kalman_bank):
            if self.faults[i - 1].get_classification == "lower" and not k == self.kalman_bank[0]:
                lower_filters.append(self.kalman_bank[i])
        for f in lower_filters:
            if f.get_predicted_state > measured_data.height():
                faulty_filters.append(f)
                free_of_faults = False
        return free_of_faults
    
    def _write_to_csv(self, measured_data: MeasurementData) -> None:
        """
        Writes kalman filter values to a csv file.
        """
        kalman_bank_csv = "data\\KalmanBankData.csv"

        with open(kalman_bank_csv, "r", encoding="utf-8") as csvfile:
            if len(csvfile.readlines()) <= 0:
                current_time = []
                noice = []
                current_state = []
                predicted_state = []
                variance = []
                predicted_variance = []
                delta_to_predicted_state = []
                for f in self.kalman_bank:
                    current_time.append(f.get_time.get_current_time.seconds)
                    noice.append(f.get_noice)
                    current_state.append(f.get_state)
                    predicted_state.append(f.get_predicted_state)
                    variance.append(f.get_variance)
                    predicted_variance.append(f.get_predict_variance)
                    delta_to_predicted_state.append(f.get_predicted_state - measured_data.height())

                np.savetxt(kalman_bank_csv, \
                           [p for p in zip(current_time, noice, current_state, predicted_state, variance, predicted_variance, delta_to_predicted_state)], \
                           delimiter=",", fmt="%s")
            else:
                current_time = []
                noice = []
                current_state = []
                predicted_state = []
                variance = []
                predicted_variance = []
                delta_to_predicted_state = []
                with open(kalman_bank_csv, "r", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile, delimiter="\t")
                    for _, line in enumerate(reader): 
                        line = str(line[0]).split(",")
                        current_time.append(float(line[0]))
                        noice.append(float(line[1]))
                        current_state.append(float(line[2]))
                        predicted_variance.append(float(line[3]))
                        variance.append(float(line[4]))
                        predicted_variance.append(float(line[5]))
                        delta_to_predicted_state.append(float(line[6]))
                for f in self.kalman_bank:
                    current_time.append(f.get_time.get_current_time)
                    noice.append(f.get_noice)
                    current_state.append(f.get_state)
                    predicted_state.append(f.get_predicted_state)
                    variance.append(f.get_variance)
                    predicted_variance.append(f.get_predict_variance)
                    delta_to_predicted_state.append(f.get_predicted_state - measured_data.height())
                np.savetxt(kalman_bank_csv, \
                           [p for p in zip(current_time, noice, current_state, predicted_state, variance, predicted_variance, delta_to_predicted_state)], \
                           delimiter=",", fmt="%s")




    @property
    def get_kalman_bank(self) -> List[Kalman]:
        "returns the List of Kalman filters"
        return self.kalman_bank

    @property
    def get_faults(self) -> List[Fault]:
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
    def get_noice(self) -> float:
        "Returns the noice as a float"
        return self.noice
