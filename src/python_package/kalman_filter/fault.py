"THIS FINE CONTAINS THE FAULT CLASS FOR THE KALMAN FILTERS"
from typing import Callable
from .kalman import MeasurementData


class Fault:
    """
    Fault class contains a fault function and a classification if the fault adds or subtracts to the sensor reading.
    """

    def __init__(self, fault: Callable[[MeasurementData], MeasurementData], classification: str) -> None:
        self._fault = fault
        match classification:
            case "higher":
                self._classification = "higher"
            case "lower":
                self._classification = "lower"
            case _:
                raise ValueError("Bad input exception. Classification must be set to 'higher' or 'lower'")

    def set_classification(self, assesment: str) -> None:
        "Sets the classification of the fault to either be strings 'higher' or 'lower'"
        match assesment:
            case "higher":
                self._classification = "higher"
            case "lower":
                self._classification = "lower"
            case _:
                raise ValueError("Bad input exception. Classification must be set to 'higher' or 'lower'")

    @property
    def get_classification(self) -> str:
        "Returns the classification of the fault"
        return self._classification

    @property
    def get_fault(self) -> Callable[[MeasurementData], MeasurementData]:
        "Returns the fault function"
        return self._fault
