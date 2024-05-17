"THIS FILE CONTAINS A BANK OF KALMAN FILTERS"
from typing import List
from enum import Enum
from .kalman import Kalman, MeasurementData, PondState
from ..time import Time
from .fault import Fault, FaultType

DEBUG_MODE = False


class KalmanError(Exception, Enum):
    "Exception class for Kalman Filters"
    LOWER_THRESHOLD_EXCEEDED = 1
    HIGHER_THRESHOLD_EXCEEDED = 2


class KalmanBank:
    "A bank of Kalman filters with faults defined by the user. When initialized, all filters are identical."

    def __init__(
        self,
        faults: List[Fault],
        initial_state: float,
        initial_variance: float,
        time: Time,
        noice: float,
        out_file: str,
    ):
        self.faults: List[Fault] = []
        self.initial_state = initial_state
        self.kalman_bank: List[Kalman] = [Kalman(initial_state, initial_variance, time, noice)]
        self.initial_variance = initial_variance
        self.time = time
        self.noice = noice
        self.out_file = out_file

        with open(self.out_file, "w", encoding="utf-8"):
            pass

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

    def step_filters(
        self, pond_state: PondState, measured_data: MeasurementData, virtual_pond_water_level: float
    ) -> None:
        "Calls the step function for each filter with each fault"
        faulty_filters: List[Kalman] = []
        failed_faults: List[str] = []
        fault_detection = self.analyze_filters(measured_data, faulty_filters, failed_faults, virtual_pond_water_level)
        # save old predict data, feed to _write_to_csv
        predict_before_step = []

        for i, k in enumerate(self.kalman_bank):
            predict_before_step.append(k.get_predicted_state)
            if i == 0:
                k.step(pond_state, measured_data)
            else:
                k.step(pond_state, self.faults[i - 1].get_fault(measured_data))
        self._write_to_csv(measured_data, predict_before_step)
        # error reporting
        if not fault_detection and not len(self.out_file) == 1:
            if DEBUG_MODE:
                filter_report_string = "Waterlevel threshold exceeded in filters: \n"
                for i, f in enumerate(faulty_filters):
                    filter_report_string += (
                        f.print_kalman_filter() + " Expected filter to be: " + failed_faults[i] + "\n"
                    )
                filter_report_string += (
                    "Kalman filter without arbitrary measurement data faults: \n"
                    + self.kalman_bank[0].print_kalman_filter()
                )
                print(
                    "The measured water level exceeded the threshold in "
                    + str(len(faulty_filters))
                    + " kalman filters.\n"
                    + "Measured water level: "
                    + str(measured_data.height())
                    + "\n"
                    + filter_report_string
                )
            for i, f in enumerate(failed_faults):
                match f:
                    case "higher":
                        raise KalmanError.HIGHER_THRESHOLD_EXCEEDED
                    case "lower":
                        raise KalmanError.LOWER_THRESHOLD_EXCEEDED

    def analyze_filters(
        self,
        measured_data: MeasurementData,
        faulty_filters: List[Kalman],
        failed_faults: List[str],
        virtual_pond_water_level: float,
    ) -> bool:
        "Analyses filters in the KalmanBank. If measured_data goes past thresholds returns false, else return true"
        free_of_faults = True
        for i, k in enumerate(self.kalman_bank):
            if self.faults[i - 1].get_classification == "higher" and not i == 0:
                if k.get_predicted_state < measured_data.height():
                    faulty_filters.append(k)
                    free_of_faults = False
                    failed_faults.append(self.faults[i - 1].get_classification)
            if self.faults[i - 1].get_classification == "lower" and not i == 0:
                if k.get_predicted_state > measured_data.height():
                    faulty_filters.append(k)
                    free_of_faults = False
                    failed_faults.append(self.faults[i - 1].get_classification)
        for i, k in enumerate(self.kalman_bank):
            if (
                self.faults[i - 1].get_classification == "higher"
                and not i == 0
                and self.faults[i - 1].get_fault_type == FaultType.MULTIPLY
            ):
                if k.get_predicted_state < virtual_pond_water_level:
                    faulty_filters.append(k)
                    free_of_faults = False
                    failed_faults.append(self.faults[i - 1].get_classification)
            if (
                self.faults[i - 1].get_classification == "LOWER"
                and not i == 0
                and self.faults[i - 1].get_fault_type == FaultType.MULTIPLY
            ):
                if k.get_predicted_state > virtual_pond_water_level:
                    faulty_filters.append(k)
                    free_of_faults = False
                    failed_faults.append(self.faults[i - 1].get_classification)

        return free_of_faults

    def _write_to_csv(self, measured_data: MeasurementData, predicted_data: List[float]) -> None:
        """
        Writes kalman filter values to a csv file.
        """
        current_time = []
        noice = []
        current_state = []
        predicted_state = []
        variance = []
        predicted_variance = []
        delta_to_predicted_state = []

        for i, f in enumerate(self.kalman_bank):
            current_time.append(f.get_time.get_current_time.total_seconds())
            noice.append(f.get_noice)
            current_state.append(f.get_state)
            predicted_state.append(f.get_predicted_state)
            variance.append(f.get_variance)
            predicted_variance.append(f.get_predict_variance)
            delta_to_predicted_state.append(predicted_data[i] - measured_data.height())

        with open(self.out_file, "a", encoding="utf-8") as f:
            f.write(
                ",".join(
                    [
                        ",".join([str(x) for x in list(p)])
                        for p in zip(
                            current_time,
                            noice,
                            current_state,
                            predicted_state,
                            variance,
                            predicted_variance,
                            delta_to_predicted_state,
                        )
                    ]
                )
                + ","
                + str(measured_data.height())
                + "\n"
            )

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
