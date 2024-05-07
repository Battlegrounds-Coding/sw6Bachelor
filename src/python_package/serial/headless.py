"""THIS FILE CONTAINS THE INITIALIZATION OF A HEADLESS SETUP"""

from datetime import timedelta
import csv
from python_package.time import Time
from . import serial


class Headless(serial.Serial):
    def __init__(self, file: str, time: Time):
        self._time = time
        self._inv = False
        self._read_before = False
        self._before = b"Rvd:30"
        self._rtn_none = False
        with open(file) as f:
            reader = csv.reader(f)
            self._buffer = [
                (timedelta(seconds=int(sec)), bytes(f"Rvd:{int(float(reading))}", "utf-8")) for sec, reading in reader
            ]

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, setting: list[tuple[timedelta, bytes]]):
        self._buffer = setting

    def write(self, _, /) -> int | None:
        return 1

    @serial.Serial.in_waiting.getter
    def in_waiting(self) -> int:
        if self._inv:
            return 1
        if len(self._buffer) > 0:
            time, _ = self._buffer[0]
            if self._time.get_current_time <= time:
                return 2
        else:
            self._read_before = True

        if not self._rtn_none:
            self._rtn_none = True
            return 0
        else:
            self._rtn_none = False
            self._read_before = True
            return 1

    def read_until(self, expected: bytes = b"\n", size: int | None = None) -> bytes:
        self._inv = not self._inv
        if self._inv:
            reading = b"invariance:3"
        elif self._read_before:
            try:
                reading = self._before
                self._read_before = False
            except Exception as e:
                raise ValueError(f"IN HEADLESS: No reading read at time 0, {e}")
        else:
            _, reading = self.buffer.pop(0)
            self._before = reading
        return reading
