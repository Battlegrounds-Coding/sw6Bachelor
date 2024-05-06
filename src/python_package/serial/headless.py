"""THIS FILE CONTAINS THE INITIALIZATION OF A HEADLESS SETUP"""

from datetime import timedelta
import csv
from python_package.time import Time
from . import serial


class Headless(serial.Serial):
    def __init__(self, file: str, time: Time):
        self._time = time
        self._inv = False
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
        i = 0
        for time, _ in self.buffer:
            if self._time.get_current_time < time:
                break
            i += 2
        return i + (-1 if self._inv else 0)

    def read_until(self, expected: bytes = b"\n", size: int | None = None) -> bytes:
        self._inv = not self._inv
        if not self._inv:
            _, reading = self.buffer.pop(0)
            return reading
        return b"invariance:3"
