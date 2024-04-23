from datetime import timedelta
from typing import List, Callable
import python_package.kalman_filter.kalman_bank as b
import python_package.kalman_filter.kalman as filter
import numpy as np
from data import TestData, TestMeasurementData


def fault_one(data: filter.MeasurementData) -> filter.MeasurementData:
    return data


def fault_two(data: filter.MeasurementData) -> filter.MeasurementData:
    return data


def fault_three(data: filter.MeasurementData) -> filter.MeasurementData:
    return data


def test_kalman_bank_constructor_faults():
    faults: List[Callable[[filter.MeasurementData], filter.MeasurementData]] = [
        lambda data: TestMeasurementData(data.height(), data.variance_height()),
        fault_one,
    ]
    bank_one = b.KalmanBank(faults, np.float64(60), np.float64(100**2), delta=timedelta(seconds=5))
    bank_two = b.KalmanBank(faults, np.float64(60), np.float64(100**2), delta=timedelta(seconds=5))
    bank_three = b.KalmanBank(faults, np.float64(40), np.float64(100**2), delta=timedelta(seconds=5))
    bank_four = b.KalmanBank(faults, np.float64(60), np.float64(20**2), delta=timedelta(seconds=5))
    bank_five = b.KalmanBank(faults, np.float64(60), np.float64(100**2), delta=timedelta(seconds=4))

    assert bank_one == bank_two
    assert not bank_one == bank_three
    assert not bank_one == bank_four
    assert not bank_one == bank_five


def test_kalman_constructor_create_bank():
    faults_one: List[Callable[[filter.MeasurementData], filter.MeasurementData]] = [
        lambda data: TestMeasurementData(data.height(), data.variance_height()),
        fault_one,
    ]

    bank_one = b.KalmanBank(faults_one, np.float64(60), np.float64(100**2), delta=timedelta(seconds=5))

    assert len(faults_one) == len(bank_one.get_kalman_bank())

    new_faults: List[Callable[[filter.MeasurementData], filter.MeasurementData]] = [
        lambda data: TestMeasurementData(data.height() + 10, data.variance_height()),
        fault_two,
    ]

    bank_one.add_faults(new_faults, np.float64(50), np.float64(200**2), delta=timedelta(seconds=6))
    assert len(faults_one) == len(bank_one.get_kalman_bank()) and len(bank_one.get_faults()) == 4

    # Tests that the add_faults function does not create filters with existing faults
    bank_one.add_faults(new_faults, np.float64(50), np.float64(200**2), delta=timedelta(seconds=6))
    assert len(faults_one) == len(bank_one.get_kalman_bank()) and not len(bank_one.get_faults()) == 5


def test_step_filters():
    faults: List[Callable[[filter.MeasurementData], filter.MeasurementData]] = [
        lambda data: TestMeasurementData(data.height(), data.variance_height()),
        lambda data_two: TestMeasurementData(data_two.height() + 10, data_two.variance_height() + 10),
        lambda data_three: TestMeasurementData(data_three.height() - 10, data_three.variance_height() - 10),
    ]

    test_bank = b.KalmanBank(faults, np.float64(60), np.float64(100**2), delta=timedelta(seconds=5))

    assert test_bank.get_kalman_bank()[0] == test_bank.get_kalman_bank()[1]
    assert test_bank.get_kalman_bank()[0] == test_bank.get_kalman_bank()[2]
    assert test_bank.get_kalman_bank()[1] == test_bank.get_kalman_bank()[2]

    test_bank.step_filters(TestData(np.float64(3)), TestMeasurementData(np.float64(2), np.float64(4)))
    assert test_bank.get_kalman_bank()[0] != test_bank.get_kalman_bank()[1]
    assert test_bank.get_kalman_bank()[0] != test_bank.get_kalman_bank()[2]
    assert test_bank.get_kalman_bank()[1] != test_bank.get_kalman_bank()[2]
