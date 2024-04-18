import serial
import pytest
import time
from python_package.serial import SerialCom
from python_package.serial.serial_exceptions import serial_exceptions

# ____________________________Setup_____________________________
test = SerialCom()


class ow_arduino(serial.Serial):
    def __init__(self) -> None:
        # self._timeout = 1
        self._buffer = []

    @property
    def buffer(self):  # custom str array for simulating controller response
        return self._buffer

    @buffer.setter
    def buffer(self, string_array: list[str]):
        self._buffer = string_array

    @serial.Serial.in_waiting.getter
    def in_waiting(self) -> int:
        """overwriten"""
        return len(self.buffer)

    def write(self, data) -> int | None:
        return 1

    def read_until(self, size=1) -> bytes:
        # if(self.in_waiting):
        #     self.in_waiting -= 1
        s: str = self.buffer.pop(0)
        output: bytes = bytes(s + "\r", "utf-8")
        return output


custom_serial = ow_arduino()
test.arduino = custom_serial

# __________________________TEST_______________________________


def test_read():
    custom_serial.buffer = ["test"]
    # test.arduino.buffer = ["test"]
    assert test.read() == "test"

    custom_serial.buffer = ["1", "2"]

    assert test.read() == "1"
    assert test.read() == "2"

    # empty buffer
    with pytest.raises(Exception) as excinfo:
        test.read()  # will timeout
    assert excinfo.value is serial_exceptions.exceptions.NO_RESPONSE


def test_controller_exception():
    custom_serial.buffer = [
        "Error:1 distance reading: -999",
        "Error:2 Pump value out of bounds [0..100]: 420",
        "Error:3 sensor did not read",
    ]
    with pytest.raises(Exception) as excinfo:
        test.read()
    assert excinfo.value is serial_exceptions.exceptions.INCORECT_DISTANCE_READING

    with pytest.raises(Exception) as excinfo:
        test.read()
    assert excinfo.value is serial_exceptions.exceptions.PUMP_VALUE_OUT_OF_BOUNDS

    with pytest.raises(Exception) as excinfo:
        test.read()
    assert excinfo.value is serial_exceptions.exceptions.NO_SENSOR_READINGS


def test_read_all():
    custom_serial.buffer = ["test"]
    test.read_all()
    assert len(custom_serial.buffer) == 0

    # empty buffer
    with pytest.raises(Exception) as excinfo:
        test.read_all()  # will timeout
    assert excinfo.value is serial_exceptions.exceptions.NO_RESPONSE

    custom_serial.buffer = [
        "1",
        "2",
        "3",
        "4",
        "5",
    ]
    temp = custom_serial.buffer.copy()
    res = test.read_all()
    assert res == temp
    assert len(custom_serial.buffer) == 0


# TODO: read_sensor should check bounds, though it should not be possible for the controller to send wrong values, there might be communication errors :)
def test_read_sensor():
    custom_serial.buffer = ["invariance: 5", "Rvd:111"]
    assert test.read_sensor() == (111, 5)

    custom_serial.buffer = ["Rvd:200", "invariance:5"]
    assert test.read_sensor() == (200, 5)

    custom_serial.buffer = ["Rvd:50"]
    with pytest.raises(Exception) as excinfo:
        test.read_sensor()
    assert excinfo.value is serial_exceptions.exceptions.NO_SENSOR_READINGS

    custom_serial.buffer = ["invariance:50"]
    with pytest.raises(serial_exceptions.exceptions) as excinfo:
        test.read_sensor()
    assert excinfo.value is serial_exceptions.exceptions.NO_SENSOR_READINGS

    custom_serial.buffer = ["Rvd:99999", "invariance:5"]
    with pytest.raises(Exception) as excinfo:
        test.read_sensor()
    assert excinfo.value is serial_exceptions.exceptions.COMUNICATION_ERROR

    custom_serial.buffer = ["Rvd: abc", "invariance:5"]
    with pytest.raises(Exception) as excinfo:
        test.read_sensor()
    assert excinfo.value is serial_exceptions.exceptions.CONVERSION_ERROR

    custom_serial.buffer = ["Rvd: 1", "invariance:d"]
    with pytest.raises(Exception) as excinfo:
        test.read_sensor()
    assert excinfo.value is serial_exceptions.exceptions.CONVERSION_ERROR


def test_set_pump():
    reset_buffer()
    with pytest.raises(Exception) as excinfo:
        test.set_pump(-5)
    assert excinfo.value is serial_exceptions.exceptions.INCORRECT_INPUT

    reset_buffer()
    with pytest.raises(Exception) as excinfo:
        test.set_pump(105)
    assert excinfo.value is serial_exceptions.exceptions.INCORRECT_INPUT

    custom_serial.buffer = ["pump update: 55"]
    assert test.set_pump(55) == None

    custom_serial.buffer = ["pump update: 0"]
    assert test.set_pump(0) == None

    custom_serial.buffer = ["pump update: 100"]
    assert test.set_pump(100) == None

    custom_serial.buffer = ["pump update: 10"]
    with pytest.raises(Exception) as excinfo:
        test.set_pump(100)
    assert excinfo.value is serial_exceptions.exceptions.COMUNICATION_ERROR

    custom_serial.buffer = ["pump update: 11"]
    with pytest.raises(Exception) as excinfo:
        test.set_pump(10)
    assert excinfo.value is serial_exceptions.exceptions.COMUNICATION_ERROR


def reset_buffer():
    custom_serial.buffer = ["test"]
