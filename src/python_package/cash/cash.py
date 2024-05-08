"""Create log files from cache data"""

from abc import abstractmethod
from datetime import datetime
from typing import Any, List, Self
import numpy as np
import io

DATE_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"


class CacheData:
    """CacheData instance"""

    def __init__(self, id: int, time: datetime, data_list: List[Any]):
        self.data_list = data_list
        self.time = time


class CacheIter:
    def __iter__(self) -> Self:
        return self

    @abstractmethod
    def __next__(self) -> CacheData: ...


class Cache:
    @abstractmethod
    def insert(self, data: CacheData): ...

    @abstractmethod
    def get(self, id: int) -> CacheData | None: ...

    @abstractmethod
    def get_nearest_before(self, time: datetime) -> CacheData | None: ...

    @abstractmethod
    def get_nearest_after(self, time: datetime) -> CacheData | None: ...

    def get_nearest(self, time: datetime) -> CacheData | None:
        before = self.get_nearest_before(time)
        after = self.get_nearest_after(time)

        if before and after:
            if abs((before.time - time).total_seconds()) < abs((after.time - time).total_seconds()):
                return before
            else:
                return after
        elif before:
            return before
        return after

    @abstractmethod
    def __iter__(self) -> CacheIter: ...


class FileCache(Cache):
    def __init__(self, file_name: str):
        self._file = open(file_name, "a+")
        self._index = self._get_index_at_end_of_file()

    def __del__(self):
        self._file.close()

    def __iter__(self) -> CacheIter:
        self._file.seek(0)
        return FileCacheIter(self._file.readlines())

    def _get_index_at_end_of_file(self):
        self._file.seek(0, io.SEEK_END)
        end = self._file.tell()
        if end <= 2:
            return 0

        self._file.seek(end - 2)

        while self._file.read(1) != "\n":
            new_pos = self._file.tell() - 2
            if new_pos < 0:
                return 1
            self._file.seek(new_pos)
        last = self._file.read()
        print(last.split("#")[0])
        return int(last.split("#")[0])

    def insert(self, data: CacheData):
        self._index += 1
        self._file.seek(0, io.SEEK_END)
        file_data = ";".join([str(x) for x in data.data_list])
        self._file.write(f"{self._index}#{data.time.strftime(DATE_STRING_FORMAT)}#{file_data}\n")

    def get(self, id: int) -> CacheData | None:
        self._file.seek(0)
        for line in self._file.readlines():
            s = line.split("#")
            if int(s[0]) == id:
                return CacheData(id, datetime.strptime(s[1], DATE_STRING_FORMAT), s[2].split(";"))

    def get_nearest_before(self, time: datetime) -> CacheData | None:
        self._file.seek(0)
        lines = self._file.readlines()
        before_line = None
        for line in lines:
            s = line.split("#")
            time_now = datetime.strptime(s[1], DATE_STRING_FORMAT)
            if time <= time_now:
                if before_line:
                    return CacheData(
                        int(before_line[0]),
                        datetime.strptime(before_line[1], DATE_STRING_FORMAT),
                        before_line[2].split(";"),
                    )
                else:
                    return None
            before_line = s

    def get_nearest_after(self, time: datetime) -> CacheData | None:
        self._file.seek(0)
        lines = self._file.readlines()
        for line in lines:
            s = line.split("#")
            time_now = datetime.strptime(s[1], DATE_STRING_FORMAT)
            if time <= time_now:
                return CacheData(int(s[0]), time_now, s[2].split(";"))

    def get_nearest(self, time: datetime) -> CacheData | None:
        self._file.seek(0)
        lines = self._file.readlines()
        lines = lines.__iter__()
        for line in lines:
            s = line.split("#")
            time_now = datetime.strptime(s[1], DATE_STRING_FORMAT)
            if time <= time_now:
                s_after = lines.__next__().split("#")
                time_after = datetime.strptime(s_after[1], DATE_STRING_FORMAT)

                if abs((time_after - time).total_seconds() > abs((time_now - time).total_seconds())):
                    return CacheData(int(s[0]), time_now, s[2].split(";"))
                else:
                    return CacheData(int(s_after[0]), time_after, s_after[2].split(";"))


class FileCacheIter(CacheIter):
    def __init__(self, lines: list[str]):
        self.lines = lines.__iter__()

    def __next__(self) -> CacheData:
        line = self.lines.__next__()
        s = line.split("#")
        return CacheData(int(s[0]), datetime.strptime(s[1], DATE_STRING_FORMAT), s[2].split(";"))
