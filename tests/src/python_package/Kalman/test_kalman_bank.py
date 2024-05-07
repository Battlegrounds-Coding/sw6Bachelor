from datetime import timedelta
from typing import List, Callable
from .data import TestMeasurementData
from python_package import rain
from python_package.rain import artificial_rain
import python_package.kalman_filter.fault as fault
import python_package.kalman_filter.kalman_bank as b
import python_package.kalman_filter.kalman as filter
import python_package.time as time
import python_package.virtual_pond as virtual_pond
import copy


def fault_one() -> fault.Fault:
    return fault.Fault(
        fault=lambda data: TestMeasurementData(data.height() - 10, data.variance_height() - 10), classification="lower"
    )


def fault_two() -> fault.Fault:
    return fault.Fault(lambda data: TestMeasurementData(data.height() + 10, data.variance_height() + 10), "higher")


def fault_three() -> fault.Fault:
    return fault.Fault(lambda data: TestMeasurementData(data.height() * 1.2, data.variance_height() * 1.2), "higher")


def fault_four() -> fault.Fault:
    return fault.Fault(lambda data: TestMeasurementData(data.height() * 0.8, data.variance_height() * 0.8), "lower")


def test_kalman_bank_constructor_faults():
    faults: List[fault.Fault] = [fault_one(), fault_two()]

    pond = virtual_pond.VirtualPond(0.59, 0.25, 0.6, 5572, 200, 100, 300, rain.Rain())

    bank_one = b.KalmanBank(faults, 60, time.Time(timedelta(seconds=0), timedelta(seconds=5)), copy.copy(pond), 10)
    bank_two = b.KalmanBank(faults, 60, time.Time(timedelta(seconds=0), timedelta(seconds=5)), copy.copy(pond), 10)
    bank_three = b.KalmanBank(faults, 40, time.Time(timedelta(seconds=0), timedelta(seconds=5)), copy.copy(pond), 10)
    bank_four = b.KalmanBank(faults, 60, time.Time(timedelta(seconds=0), timedelta(seconds=4)), copy.copy(pond), 10)
    bank_five = b.KalmanBank(faults, 60, time.Time(timedelta(seconds=2), timedelta(seconds=5)), copy.copy(pond), 10)
    bank_six = b.KalmanBank(
        faults,
        60,
        time.Time(timedelta(seconds=0), timedelta(seconds=5)),
        virtual_pond.VirtualPond(0.69, 0.2, 0.2, 5571, 220, 103, 500, artificial_rain.ArtificialConstRain(20)),
        10,
    )
    bank_seven = b.KalmanBank(faults, 60, time.Time(timedelta(seconds=0), timedelta(seconds=5)), copy.copy(pond), 20)

    assert bank_one == bank_two
    assert not bank_one == bank_three
    assert not bank_one == bank_four
    assert not bank_one == bank_five
    assert not bank_one == bank_six
    assert not bank_one == bank_seven
    assert not bank_four == bank_five


def test_kalman_constructor_create_bank():
    faults: List[fault.Fault] = [fault_one(), fault_two()]

    bank_one = b.KalmanBank(
        faults,
        60,
        time.Time(timedelta(seconds=2), timedelta(seconds=5)),
        virtual_pond.VirtualPond(0.69, 0.2, 0.2, 5571, 220, 103, 500, artificial_rain.ArtificialConstRain(20)),
        10,
    )

    assert len(bank_one.get_kalman_bank) - len(faults) == 1

    new_faults: List[fault.Fault] = [fault_three(), fault_four()]

    bank_one.add_faults(new_faults)
    assert (len(bank_one.get_kalman_bank) - len(faults)) == 3 and len(bank_one.get_faults) == 4

    # Tests that the add_faults function does not create filters with existing faults
    bank_one.add_faults(new_faults)
    assert len(bank_one.get_kalman_bank) - len(faults) == 3 and not len(bank_one.get_faults) == 5


def test_step_filters():
    faults: List[fault.Fault] = [fault_one(), fault_two(), fault_three()]

    test_bank = b.KalmanBank(
        faults,
        60,
        time.Time(timedelta(seconds=2), timedelta(seconds=5)),
        virtual_pond.VirtualPond(0.69, 0.2, 0.2, 5571, 220, 103, 500, artificial_rain.ArtificialConstRain(20)),
        10,
    )

    assert test_bank.get_kalman_bank[0] == test_bank.get_kalman_bank[1]
    assert test_bank.get_kalman_bank[0] == test_bank.get_kalman_bank[2]
    assert test_bank.get_kalman_bank[1] == test_bank.get_kalman_bank[2]

    test_bank.step_filters(TestMeasurementData(float(2), float(4)))
    assert test_bank.get_kalman_bank[0] != test_bank.get_kalman_bank[1]
    assert test_bank.get_kalman_bank[0] != test_bank.get_kalman_bank[2]
    assert test_bank.get_kalman_bank[1] != test_bank.get_kalman_bank[2]
