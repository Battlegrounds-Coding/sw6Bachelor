"""
Contains an artificial rain implementation
"""

from datetime import datetime, timedelta
from typing import List, Self, Tuple
import bisect
from . import Rain
from .area import Area


class ArtificialVariableRainPrediction:
    "Used as input to the ArtificialVariable Rain to create simulated rainfall"

    def __init__(self):
        "Creates a new ArtificialVariableRainPrediction"
        self._prediction: List[Tuple[timedelta, float]] = []

    def add_point(self, time: timedelta, rain: float) -> Self:
        "Adds a point into the rain prediction"
        bisect.insort(self._prediction, (time, rain), key=lambda x: x[0])
        return self

    def get_closest_index(self, time: timedelta) -> int:
        "Gets the closes lower bounded time to the timedelta"
        index = bisect.bisect_left(self._prediction, time, key=lambda x: x[0])
        return index

    def get_prediction(self, index: int) -> None | Tuple[timedelta, float]:
        "Gets the prediction at index, returns none if it doesn't exist"
        if len(self._prediction) <= index:
            return None
        return self._prediction[index]


class ArtificialVariableRain(Rain):
    "This is an artificial created rain simulation"

    def __init__(self, begining_of_time: datetime, simulation: ArtificialVariableRainPrediction):
        """
        Creates a new ArtificialVariableRain,
        requires a begining_of_time from where the timedeltas in the ArtificialVariableRainPrediction are calculated
        """
        self.begining = begining_of_time
        self.simulation = simulation

    def get_rain_fall(self, area: Area, start_time: datetime, end_time: datetime) -> float:
        """
        Gets the averge rainfall within the given start_time and end_time
        """
        rain_time: List[Tuple[timedelta, float]] = []
        start_stamp = start_time - self.begining
        end_stamp = end_time - self.begining
        index = self.simulation.get_closest_index(start_stamp)

        while True:
            now = self.simulation.get_prediction(index)
            index += 1
            after = self.simulation.get_prediction(index)
            if after:
                after_time, _ = after
            else:
                after_time = end_stamp

            if now:
                now_time, now_rain = now
                now_time = max(now_time, start_stamp)
            else:
                return 0

            rain_time.append((after_time - now_time, now_rain))

            if after_time >= end_stamp:
                break

        total_rain = 0.0
        total_time = timedelta()
        for time, rain in rain_time:
            total_rain += rain * time.total_seconds()
            total_time += time

        if total_time.total_seconds() == 0:
            return 0.0
        return total_rain / total_time.total_seconds()


class ArtificialConstRain(Rain):
    "An rainpredicter that predicts constant rain"

    def __init__(self, rain: float):
        "Creates a new ArtificialConstRain"
        self._rain = rain

    def get_rain_fall(self, area: Area, start_time: datetime, end_time: datetime) -> float:
        "Returns the constant rainfall"
        return self._rain
