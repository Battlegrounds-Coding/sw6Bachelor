"Contains definitions of logging interface and levels"

from abc import abstractmethod
import enum


class LogLevel(enum.Enum):
    """Sets the log level"""

    NOT_CIRITCAL = 0
    WARNING = 1
    ERROR = 2
    CRITICAL_ERROR = 3


class Log:  # pylint: disable=R0903
    """A superclass for a Logger"""

    @abstractmethod
    def _err(self, msg):
        ...

    @abstractmethod
    def _warn(self, msg):
        ...

    @abstractmethod
    def _not_critical(self, msg):
        ...

    @abstractmethod
    def _critical_error(self, msg):
        ...

    level = LogLevel.NOT_CIRITCAL

    def log(self, msg):
        """ "Logs the method"""
        match self.level:
            case LogLevel.CRITICAL_ERROR:
                self._critical_error(msg)
            case LogLevel.ERROR:
                self._err(msg)
            case LogLevel.WARNING:
                self._warn(msg)
            case _:
                self._not_critical(msg)


class PrintLogger(Log):  # pylint: disable=R0903
    "Logs to stdout"

    def _critical_error(self, msg):
        print(f"[CRITICAL ERROR]: {msg}")

    def _err(self, msg):
        print(f"[ERROR]: {msg}")

    def _warn(self, msg):
        print(f"[WARNING]: {msg}")

    def _not_critical(self, msg):
        print(f"{msg}")


DEFAULT_LOG = PrintLogger()
