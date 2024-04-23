"THIS FILE CONTAINS MOCKCLASSES USED TO SAVE MOCKDATA FOR UNIT TESTS"
import numpy as np
import python_package.kalman_filter.kalman as f


class TestData(f.Data):
    "Mockdata for unit tests"

    def __init__(self, data: np.float64) -> None:
        self.data = data

    def height(self) -> np.float64:
        return self.data

    __test__ = False

    # pylint: disable=locally-disabled, multiple-statements, fixme, too-few-public-methods


class TestMeasurementData(f.MeasurementData):
    "Mock measurement data for unit tests"

    def __init__(self, data: np.float64, variance: np.float64) -> None:
        self.data = data
        self.variance = variance

    def height(self) -> np.float64:
        return self.data

    def variance_height(self) -> np.float64:
        return self.variance

    __test__ = False
