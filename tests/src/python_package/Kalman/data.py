"THIS FILE CONTAINS MOCKCLASSES USED TO SAVE MOCKDATA FOR UNIT TESTS"
import python_package.kalman_filter.kalman as f


class TestMeasurementData(f.MeasurementData):
    "Mock measurement data for unit tests"

    def __init__(self, data: float, variance: float) -> None:
        self.data = data
        self.variance = variance

    def height(self) -> float:
        return self.data

    def variance_height(self) -> float:
        return self.variance

    __test__ = False
