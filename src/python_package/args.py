"""File for defining Executable file arguments"""

from typing import List
from datetime import datetime
from enum import Enum
import sys
import tempfile
import os

from .rain import artificial_rain as ar, rain_data as rd


class OutType(Enum):
    "An enum descriping the fileformat that the graphs should be saved to"
    PNG = 0
    PGF = 1


class OutGraph(Enum):
    "An enum descriping what graph should be created if the OutType is PGF"
    RAIN = 0
    CONTROL = 1
    KALMAN_DELTA = 2
    KALMAN = 3


def out_graph_to_string(graph: OutGraph) -> str:
    "Converts an OutGraph enum to its corresponging string"
    match graph:
        case OutGraph.RAIN:
            return "rain"
        case OutGraph.CONTROL:
            return "control"
        case OutGraph.KALMAN:
            return "kalman"
        case OutGraph.KALMAN_DELTA:
            return "kalman-delta"


DEFAULT_RAIN = 10
DEFAULT_TIME = 100
DEFAULT_CONTROLER_CACHE = os.path.join(tempfile.gettempdir(), "virtual-pond-controler-errors")
DEFAULT_OUT = os.path.join(tempfile.gettempdir(), "out.csv")
DEFAULT_KALMAN = os.path.join(tempfile.gettempdir(), "kalman.csv")
DEFAULT_NAME = "Unnamed experiment"
DEFAULT_OUT_SHOW = False
DEFAULT_OUT_TYPE = OutType.PNG
DEFAULT_OUT_GRAPH = OutGraph.RAIN
DEFAULT_OUT_SUFFIX = False

HELP = f"""USAGE python <name_of_our_tool> ([ARGUMENT]=[VALUE])*
    [-n  | --name]=string                    -- The name of the experiment
                                                (default={DEFAULT_NAME})
    [-r  | --rain]=/path/to/file             -- Location of the file that contains the raindata at a specific time
    [-cr | --constant-rain]=number           -- Specify a constant amount of rain in mm
                                                (default={DEFAULT_RAIN})
    [-s  | --strategy]=/path/to/file         -- Location of the file that contains the strategy used by the pond
    [-cc | --controler-cache]=/path/to/file  -- Location of the file that the filter may chace to,
                                                (default={DEFAULT_CONTROLER_CACHE})
    [-m  | --mode]=mode                      -- What mode is the setup working in, headless there is no real world
                                                connection to a setup. Seriel there is a connection to a real world
                                                setup.
                                                (supporteed mode=[headless | seriel])
                                                (default=seriel)
    [-d  | --data]=/path/to/file             -- Location of the file that contains the moched data from the sensor,
                                                If mode is headless, otherwise this is ignored
    [-dc | --data-control]=/path/to/file     -- Location of the file that contains the control data from a project.
    [-t  | --time]=time                      -- For how long should the simmulation run in seconds.
                                                (default={DEFAULT_TIME})
    [-o  | --output]=/path/to/file           -- Specifies the output csv file of the system
                                                (default={DEFAULT_OUT})
    [-oi | --output-image]=/path/to/file     -- Path to the saved plotting image (supported file types: [pgf | png])
                                                !NOTE if image type is pgf then --show is not supported
    [-og | --output-graph]=name,name,...     -- If --output-image type is pgf then what graph should be created
                                                (supported names: [rain | control | kalman | kalman-delta])
                                                (default={out_graph_to_string(DEFAULT_OUT_GRAPH)})
    [-os | --output-suffix]=boolean          -- If --output-image type is pgf the should the name be suffixed with
                                                the output graph, this is automatically enabeled if there are more
                                                output graphs.
                                                (default={DEFAULT_OUT_SUFFIX})
    [-s  | --show]=boolean                   -- Should the output be shown in the end
                                                !NOTE if the --output-image is of type pgf then --show is not supported
                                                (default={DEFAULT_OUT_SHOW})
    [-k  | --kalman-bank]=/path/to/file      -- Specifies the output file for the kalman banks
                                                (default={DEFAULT_KALMAN})
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
                    case "-og" | "--output-graph":
                        self._out_graph = []
                        for graph in value.split(","):
                            match graph:
                                case "rain":
                                    self._out_graph.append(OutGraph.RAIN)
                                case "control":
                                    self._out_graph.append(OutGraph.CONTROL)
                                case "kalman-delta":
                                    self._out_graph.append(OutGraph.KALMAN_DELTA)
                                case "kalman":
                                    self._out_graph.append(OutGraph.KALMAN)
                                case _:
                                    raise ValueError(f"{graph} is not a valid --output-graph")
                    case "-os" | "--out-suffix":
                        self._out_suffix =value.lower() == "true"
                    case "-s" | "--show":
                        self._show = value.lower() == "true"
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
        """Gets the rain object for the experiemt"""
        try:
            return self._rain
        except AttributeError:
            return ar.ArtificialConstRain(DEFAULT_RAIN)

    @property
    def rain_file(self):
        """Path to the file containing rain data"""
        return self._rain_file

    @property
    def strategy(self):
        """NOT IMPLEMENTED: Path to the file containing the stategy that the experiement should run"""
        if self._strategy_file:
            return self._strategy_file
        raise AttributeError("No strategy file given")

    @property
    def data(self):
        """Path to csv file containing fake readings for the sensor"""
        if self._data:
            return self._data
        raise AttributeError("No datafile given")

    @property
    def controler_cache(self):
        """Path to the folder where the controler dumps its errors"""
        try:
            return self._controler_cache
        except AttributeError:
            return DEFAULT_CONTROLER_CACHE

    @property
    def time(self):
        """The allotet time the experiment should run"""
        if self._time:
            return self._time
        return DEFAULT_TIME

    @property
    def mode(self):
        """Should the mode be headless or serial"""
        try:
            if self._mode != "headless":
                return Mode.SERIEL
        except AttributeError:
            pass
        return Mode.HEADLESS

    @property
    def data_control(self):
        """Path to the control data"""
        return self._data_control

    @property
    def out(self):
        """Path to where out should be saved"""
        try:
            return self._out
        except AttributeError:
            return DEFAULT_OUT

    @property
    def out_image(self) -> str | None:
        """The filepath that the polts are saved to."""
        try:
            return self._out_image
        except AttributeError:
            return None

    @property
    def out_type(self) -> OutType:
        """In which fileformat should the graphs be saved"""
        try:
            match self._out_image.split(".").pop():
                case "pgf":
                    return OutType.PGF
                case "png":
                    return OutType.PNG
                case _:
                    return DEFAULT_OUT_TYPE
        except AttributeError:
            return DEFAULT_OUT_TYPE

    @property
    def out_graph(self) -> List[OutGraph]:
        """What graphs should be created if the mode is pgf"""
        try:
            return self._out_graph
        except AttributeError:
            return [DEFAULT_OUT_GRAPH]

    @property
    def kalman(self):
        """The output file where the kalman bank should output its data"""
        try:
            return self._kalman
        except AttributeError:
            return DEFAULT_KALMAN

    @property
    def name(self):
        """Indicates the name of the experiment"""
        try:
            return self._name
        except AttributeError:
            return DEFAULT_NAME

    @property
    def show(self):
        """Should mathplotlib show that graph once done"""
        try:
            rtn = self._show
        except AttributeError:
            rtn = DEFAULT_OUT_SHOW
        return rtn and self.out_type is not OutType.PGF

    @property
    def out_suffix(self) -> bool:
        """Getter Should the outputted pgf file be suffixed wuth the corresponding --out-graph"""
        try:
            return len(self._out_graph) > 1
        except AttributeError:
            pass

        try:
            return self._out_suffix
        except AttributeError:
            return DEFAULT_OUT_SUFFIX


class Mode(Enum):
    """Enum for defining rather to get data from a data file rather than the physical setup"""

    SERIEL = 0
    HEADLESS = 1
