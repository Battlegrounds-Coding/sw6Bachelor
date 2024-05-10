"""File for defining Executable file arguments"""

from datetime import datetime
from enum import Enum
import sys
import tempfile
import os

from .rain import artificial_rain as ar, rain_data as rd


DEFAULT_RAIN = 10
DEFAULT_TIME = 100
DEFAULT_FILTER_CACHE = os.path.join(tempfile.gettempdir(), "filter.cache")
DEFAULT_CONTROLER_CACHE = os.path.join(tempfile.gettempdir(), "virtual-pond-controler-errors")
DEFAULT_OUT = os.path.join(tempfile.gettempdir(), "out.csv")
DEFAULT_KALMAN = os.path.join(tempfile.gettempdir(), "kalman.csv")
DEFAULT_NAME = "Unnamed experiment"

HELP = f"""USAGE python <name_of_our_tool> ([ARGUMENT]=[VALUE])*
    [-r  | --rain]=/path/to/file             -- Location of the file that contains the raindata at a specific time
    [-cr | --constant-rain]=number           -- Specify a constant amount of rain in mm
                                                (default={DEFAULT_RAIN})

    [-s  | --strategy]=/path/to/file         -- Location of the file that contains the strategy used by the pond

    [-fc | --filter-cache]=/path/to/file     -- Location of the file that the filter may chace to,
                                                (default={DEFAULT_FILTER_CACHE})
    [-cc | --controler-cache]=/path/to/file  -- Location of the file that the filter may chace to,
                                                (default={DEFAULT_CONTROLER_CACHE})

    [-m  | --mode]=[headless | seriel]       -- What mode is the setup working in, headless there is no real world
                                                connection to a setup. Seriel there is a connection to a real world
                                                setup.
                                                (default=seriel)
    [-d  | --data]=/path/to/file             -- Location of the file that contains the moched data from the sensor,
                                                If mode is headless, otherwise this is ignored
    [-dc | --data-control]=/path/to/file     -- Location of the file that contains the control data from a project.
    [-t  | --time]=time                      -- For how long should the simmulation run in seconds.
                                                (default={DEFAULT_TIME})
    [-o  | --output]=/path/to/file           -- Specifies the output file of the system
                                                (default={DEFAULT_OUT})
    [-oi | --output-image]=/path/to/file     -- Path to the saved plotting image
    [-k  | --kalman-bank]=/path/to/file      -- Specifies the output file for the kalman banks
                                                (default={DEFAULT_KALMAN})
    [-n  | --name]=string                    -- The name of the experiment
                                                (default={DEFAULT_NAME})
    """


class ARGS:
    """Class for defining executable arguments"""

    def __init__(self, start: datetime):
        args = list(sys.argv)  # [x for x in sys.argv]
        args.pop(0)
        try:
            for arg in args:
                if arg in ("-h", "--help"):
                    print(HELP)
                    sys.exit(0)

                cmd_argument, value = arg.split("=")
                match cmd_argument:
                    case "-r" | "--rain":
                        rain_data = rd.save_rain_data(value)
                        self._rain = ar.ArtificialVariableRain(start, rain_data)
                        self._rain_file = value
                    case "-cr" | "--constant-rain":
                        self._rain = ar.ArtificialConstRain(int(value))
                    case "-s" | "--strategy":
                        self._strategy_file = value
                    case "-d" | "--data":
                        self._data = value
                    case "-fc" | "--file-cache":
                        self._file_cache = value
                    case "-cc" | "--controler-cache":
                        self._controler_cache = value
                    case "-m" | "--mode":
                        self._mode = value
                    case "-dc" | "--data-control":
                        self._data_control = value
                    case "-t" | "--time":
                        self._time = int(value)
                    case "-o" | "--output":
                        self._out = value
                    case "-oi" | "--output-image":
                        self._out_image = value
                    case "-k" | "--kalman-bank":
                        self._kalman = value
                    case "-n" | "--name":
                        self._name = value
        except ValueError as e:
            print(e)
            print("\n" + HELP)
            sys.exit(1)

    @property
    def rain(self):
        """Getter for rain
        if not defined, returns 'ar.ArtificialConstRain(DEFAULT_RAIN)'"""
        if not self._rain:
            return ar.ArtificialConstRain(DEFAULT_RAIN)
        return self._rain

    @property
    def rain_file(self):
        """getter for rain file"""
        return self._rain_file

    @property
    def strategy(self):
        """Getter for strategy
        if not defined, raises exceotion"""
        if self._strategy_file:
            return self._strategy_file

        raise AttributeError("No strategy file given")

    @property
    def data(self):
        """Getter for data
        if not defined, raises exception"""
        if self._data:
            return self._data

        raise AttributeError("No datafile given")

    @property
    def filter_cache(self):
        """Getter for filter_cache
        if not defined, returns 'DEFAULT_FILTER_CACHE'"""
        if self._file_cache:
            return self._file_cache

        return DEFAULT_FILTER_CACHE

    @property
    def controler_cache(self):
        """Getter for controler cache
        if not defined, returns 'DEFAULT_CONTROLER_CACHE'"""
        try:
            return self._controler_cache
        except AttributeError:
            return DEFAULT_CONTROLER_CACHE

    @property
    def time(self):
        """getter for time
        if not defined, returns 'DEFAULT_TIME'"""
        if self._time:
            return self._time

        return DEFAULT_TIME

    @property
    def mode(self):
        """getter for mode
        returns 'Mode' enum"""
        if self._mode != "headless":
            return Mode.SERIEL
        return Mode.HEADLESS

    @property
    def data_control(self):
        """getter for data control"""
        return self._data_control

    @property
    def out(self):
        """Getter for out"""
        try:
            return self._out
        except AttributeError:
            return DEFAULT_OUT

    @property
    def out_image(self) -> str | None:
        """Output path for plot png"""
        print(self._out_image)
        try:
            return self._out_image
        except AttributeError:
            return None

    @property
    def kalman(self):
        """Getter for kalmantfilter"""
        try:
            return self._kalman
        except AttributeError:
            return DEFAULT_KALMAN

    @property
    def name(self):
        """Getter for kalmantfilter"""
        try:
            return self._name
        except AttributeError:
            return DEFAULT_NAME


class Mode(Enum):
    """Enum for defining rather to get data from virtual pond or the physical pond"""
    SERIEL = 0
    HEADLESS = 1
