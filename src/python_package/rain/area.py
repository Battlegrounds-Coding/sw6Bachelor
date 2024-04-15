"THIS FILE CONTAINS AREAS FOR DEFINNIG RAINFALL"

from abc import abstractmethod


class Coordinate:
    "A coordinate used to specify an area on the earth"

    def __init__(self, lon: float, lat: float):
        self.lon = lon
        self.lat = lat


class Area:
    "An abstract class for workin with multiple areas"

    @abstractmethod
    def contains(self, coordinate: Coordinate) -> bool:
        "Is the point within the area"

    @abstractmethod
    def calc_area(self) -> float:
        "Calculates the area in m2"

    def calc_area_ha(self) -> float:
        "Calculates the area en hectar"
        return self.calc_area() / 10000


class NorthboundRectangle(Area):
    """
    A rectangle whits sides are north, east, south and west
    """

    def __init__(self, corner1: Coordinate, corner2: Coordinate):
        "Creates a new NorthboundRectangle"
        self._c1 = corner1
        self._c2 = corner2

    def contains(self, coordinate: Coordinate) -> bool:
        """
        Is the coordinate located within the Rectangle
        """
        return (
            coordinate.lat < max(self._c1.lat, self._c2.lat)
            and coordinate.lat > min(self._c1.lat, self._c2.lat)
            and coordinate.lon < max(self._c1.lon, self._c2.lon)
            and coordinate.lon > min(self._c1.lon, self._c2.lon)
        )

    def calc_area(self) -> float:
        "Calculates the area of the Reactangle in m³"
        distance_between_deg_in_m = 111_120
        lat_max = max(self._c1.lat, self._c2.lat)
        lat_min = min(self._c1.lat, self._c2.lat)
        d_lat = (lat_max - lat_min) * distance_between_deg_in_m

        lon_max = max(self._c1.lon, self._c2.lon)
        lon_min = min(self._c1.lon, self._c2.lon)
        d_lon = (lon_max - lon_min) * distance_between_deg_in_m

        return d_lat * d_lon


class EmptyArea(Area):
    """Empty rain arae"""

    def __init__(self, area: float) -> None:
        self.area = area

    def contains(self, coordinate: Coordinate) -> bool:
        "Is the point within the area"
        return False

    def calc_area(self) -> float:
        "Calculates the area in m2"
        return self.area

    def calc_area_ha(self) -> float:
        "Calculates the area en hectar"
        return self.calc_area() / 10000
