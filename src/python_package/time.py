"THIS FILE CONTAINS A CLASS THAT KEEPS TRACK OF TIME IN THE SYSTEM"
from datetime import timedelta, datetime


class Time:
    "This class contains the time delta between readings and the current time of the system."

    def __init__(self, start: datetime, current_time: timedelta, delta: timedelta):
        "Constructor for the time class."
        self._current_time = current_time
        self._delta = delta
        self._start = start

    def step(self):
        self._current_time += self._delta

    @property
    def get_current_time(self) -> timedelta:
        "Getter method for current_time variable."
        return self._current_time

    @property
    def get_delta(self) -> timedelta:
        "Getter method for the change in time."
        return self._delta
    
    @property
    def get_current_datetime(self) -> datetime:
        return self._start + self._current_time
    
    @property
    def get_current_datetime_delta(self) -> datetime:
        return self._start + self._current_time + self._delta
