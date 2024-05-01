import sys
import tempfile


DEFAULT_RAIN = 20
DEFAULT_FILTER_CACHE = f"{tempfile.gettempdir()}/filter.cache"
DEFAULT_CONTROLER_CACHE = f"{tempfile.gettempdir()}/controler.cache"

HELP = \
    f"""
    USAGE python <name_of_our_tool> ([ARGUMENT]=[VALUE])*
    [-r  | --rain]=/path/to/file             -- Location of the file that contains the raindata at a specific time
    [-cr | --constant-rain]=number           -- Specify a constant amount of rain in mm
                                                (default={DEFAULT_RAIN})

    [-s  | --strategy]=/path/to/file         -- Location of the file that contains the strategy used by the pond
    [-d  | --data]=/path/to/file             -- Location of the file that contains the moched data from the sensor

    [-fc | --filter-cache]=/path/to/file     -- Location of the file that the filter may chace to,
                                                (default={DEFAULT_FILTER_CACHE})
    [-cc | --controler-cache]=/path/to/file  -- Location of the file that the filter may chace to,
                                                (default={DEFAULT_CONTROLER_CACHE})
    """


class ARGS:
    def __init__(self):
        args = [x for x in sys.argv]
        args.pop(0)
        try:
            for arg in args:
                if arg == "-h" or arg == "--help":
                    print(HELP)
                    exit(0)


                cmd_argument, value = arg.split("=")
                match cmd_argument:
                    case "-r" | "--rain":
                        self._rain_file = value
                    case "-cr" | "--constant-rain":
                        self._constant_rain = int(value)
                    case "-s" | "--strategy":
                        self._strategy_file = value
                    case "-d" | "--data":
                        self._data = value
                    case "-fc" | "--file-cache":
                        self._file_cache = value
                    case "-cc" | "--controler-cache":
                        self._controler_cache = value
        except Exception as e:
            print(e)
            print(HELP)
            exit(1)

    @property
    def rain(self):
        return DEFAULT_RAIN

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






