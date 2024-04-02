import h5py as h5


class Radar:
    "Defindes a radarinput"

    def __init__(self) -> None:
        "Creates a new radar object"
        self._f = h5.File("/home/kamya/AAU/Projekt/P6/DMI/dk.com.202311231405.500_max.h5")

    def test(self) -> None:
        "Tests the system"
        a = self._f["where"].attrs["LL_lat"]
        print(a)

    def __del__(self) -> None:
        "Destryies the radar object"
        self._f.close()
