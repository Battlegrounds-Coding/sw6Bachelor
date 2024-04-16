from datetime import timedelta
import python_package.kalman as f
import numpy as np


class TestData(f.Data):
    def __init__(self, data: np.float32) -> None:
        self.data = data

    def height(self) -> np.float32:
        return self.data


class TestMessurementData(f.MessurementData):
    def __init__(self, data: np.float32, variance: np.float32) -> None:
        self.data = data
        self.variance = variance

    def height(self) -> np.float32:
        return self.data

    def variance_height(self) -> np.float32:
        return self.variance


def test_filter_case_temperature():
    filter = f.Kalman (np.float32(60), np.float32(100**2), delta=timedelta(seconds=5))
    data = np.array(
        [
            [49.986, 49.986],
            [49.963, 49.974],
            [50.090, 50.016],
            [50.001, 50.012],
            [50.018, 50.013],
            [50.050, 50.020],
            [49.938, 49.978],
            [49.858, 49.985],
            [49.965, 49.982],
            [50.114, 49.999]
        ],
        dtype=np.float32
    )
    variance = np.float32(0.01)

    for messurement, estimate in data:
        filter.step(TestData(filter.state), TestMessurementData(messurement, variance))
        a = np.abs(filter.state - estimate, dtype=np.float32)
        print("abs: " + str(a))
        assert a < np.float32(1e-5)




