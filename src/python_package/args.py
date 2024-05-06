from datetime import datetime
from enum import Enum
import sys
import tempfile

from .rain import artificial_rain as ar, rain_data as rd


DEFAULT_RAIN = 10
DEFAULT_TIME = 100
DEFAULT_FILTER_CACHE = f"{tempfile.gettempdir()}/filter.cache"
DEFAULT_CONTROLER_CACHE = f"{tempfile.gettempdir()}/controler.cache"

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
    """


class ARGS:
    def __init__(self, start: datetime):
        args = [x for x in sys.argv]
        args.pop(0)
        try:
            for arg in args:
                if arg == "-h" or arg == "--help":
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
        except Exception as e:
            print(e)
            print("\n" + HELP)
            sys.exit(1)

    @property
    def rain(self):
        if not self._rain:
            return ar.ArtificialConstRain(DEFAULT_RAIN)
        return self._rain

    @property
    def rain_file(self):
        return self._rain_file

    @property
    def strategy(self):
        if self._strategy_file:
            return self._strategy_file
        else:
            raise Exception("No strategy file given")

    @property
    def data(self):
        if self._data:
            return self._data
        else:
            raise Exception("No datafile given")

    @property
    def filter_cache(self):
        if self._file_cache:
            return self._file_cache
        else:
            return DEFAULT_FILTER_CACHE

    @property
    def controler_cache(self):
        if self._controler_cache:
            return self._controler_cache
        else:
            return DEFAULT_CONTROLER_CACHE

    @property
    def time(self):
        if self._time:
            return self._time
        else:
            return DEFAULT_TIME

    @property
    def mode(self):
        if self._mode != "headless":
            return Mode.SERIEL
        return Mode.HEADLESS

    @property
    def data_control(self):
        return self._data_control


class Mode(Enum):
    SERIEL = 0
    HEADLESS = 1
