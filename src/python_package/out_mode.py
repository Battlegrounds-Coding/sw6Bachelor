"THIS FILE CONTAINS THE OutMode ENUM"
from enum import Enum


class OutMode(Enum):
    """Descriptor for what the output error should output.
    SENSOR: Trust the sensor
    VIRTUAL: Don't trust the sensor, output the virtual pond
    SENSOR_ERROR: The sensor has encountered an error output the virtual pond
                  Don't continue reading
    """

    SENSOR = 0
    VIRTUAL = 1
    SENSOR_ERROR = 2
