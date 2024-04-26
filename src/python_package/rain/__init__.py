"THIS FILE CONTAINS THE SimulatedRain ABSTRACT CLASS"


from abc import abstractmethod
from datetime import datetime
from .area import Area


class Rain:
    "An abstract class for combining rain prediction methods"

    @abstractmethod
    def get_rain_fall(self, area: Area, start_time: datetime, end_time: datetime) -> float:
        """
        This method takes a start_time, end_time and area and
        returns the rainfall in mm
        """
