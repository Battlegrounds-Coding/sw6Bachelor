"THIS FILE CONTAINS THE RADAR CLASS"

from datetime import datetime
from typing import Self
import h5py as h5
from .. import Rain 
from ..area import Area 


class Radar(Rain):
    "Defindes a radarinput"

    def __init__(self, area: Area) -> None:
        "Creates a new radar object"
        self._area = area

    def set_area(self, area: Area) -> Self:
        "Sets the area of the radar"
        self._area = area
        return self

    def get_rain_fall(self, area: Area, start_time: datetime, end_time: datetime) -> float:
        "TODO"
        return 0.0


class RadarData:
    def __init__(self):
        "Creats new radardata"
        self._f = h5.File("/home/kamya/AAU/Projekt/P6/DMI/dk.com.202311231405.500_max.h5")

    def __del__(self) -> None:
        "Destryies the radar object"
        self._f.close()

    def test(self) -> None:
        "Tests the system"
        a = self._f["where"].attrs["LL_lat"]
        print(a)







