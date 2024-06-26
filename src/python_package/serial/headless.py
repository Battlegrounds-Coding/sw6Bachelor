"""THIS FILE CONTAINS THE INITIALIZATION OF A HEADLESS SETUP"""

from datetime import timedelta
import csv
import copy
from python_package.time import Time
from . import serial


class Headless(serial.Serial):  # pylint: disable=R0901
    """
    Headless comunication class for running without physical setup
    """

    def __init__(self, file: str, time: Time):
        super(serial.Serial, self).__init__()
        self._time = time
        self._inv = False
        self._read_before = False
        self._before = b"Rvd:30"
        self._rtn_none = False
        self._in_waiting = 0
        self._last_fill = timedelta(seconds=-1)
        with open(file, "r", -1, "UTF-8") as f:
            reader = csv.reader(f)
            self._buffer = [
                (timedelta(seconds=int(float(sec))), bytes(f"Rvd:{int(float(reading))}", "utf-8"))
                for sec, reading in reader
            ]

    @property
    def buffer(self):
        """Buffer for height readings"""
        return self._buffer

    @buffer.setter
    def buffer(self, setting: list[tuple[timedelta, bytes]]):
        self._buffer = setting

    def write(self, _) -> int | None:
        return 1

    # @serial.Serial.in_waiting.getter
    @property
    def in_waiting(self) -> int:
        if self._in_waiting == 0:
            for i, (time, _) in enumerate(self._buffer):
                if time <= self._time.get_current_time:
                    self._in_waiting = (i + 1) * 2
                    self._last_fill = copy.deepcopy(self._time.get_current_time)
                    break
            try:
                if self._in_waiting == 0 and self._time.get_current_time == self._last_fill:
                    if self._rtn_none:
                        self._rtn_none = False
                        return 0
                    self._rtn_none = True
                    self._read_before = True
                    self._in_waiting = 2
            except AttributeError:
                pass
        return self._in_waiting

    def read_until(self, expected: bytes = b"\n", size: int | None = None) -> bytes:
        self._inv = not self._inv
        self._in_waiting -= 1
        self._rtn_none = True
        if not self._inv:
            reading = b"invariance:3"
        elif self._read_before:
            try:
                reading = self._before
                self._read_before = False
            except Exception as e:
                raise ValueError(f"IN HEADLESS: No reading read at time 0, {e}") from e
        else:
            _, reading = self.buffer.pop(0)
            self._before = reading
        return reading
