"""Create log files from cache data"""

from abc import abstractmethod
from datetime import datetime
from typing import Any, List, Self
import io

DATE_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"


class CacheData:
    """CacheData instance"""

    def __init__(self, data_id: int, time: datetime, data_list: List[Any]):
        self.data_list = data_list
        self.time = time
        self.data_id = data_id


class CacheIter:
    """Iterator over cache"""

    def __iter__(self) -> Self:
        return self

    @abstractmethod
    def __next__(self) -> CacheData: ...


class Cache:
    """Creates a header for a file that can be written and read from"""

    @abstractmethod
    def insert(self, data: CacheData):
        """Insert 'data' into the file"""

    @abstractmethod
    def get(self, data_id: int) -> CacheData | None:
        """Get data from cache with the id 'id'"""

    @abstractmethod
    def get_nearest_before(self, time: datetime) -> CacheData | None:
        """Get nearest dataset with timestamp before 'time'"""

    @abstractmethod
    def get_nearest_after(self, time: datetime) -> CacheData | None:
        """Get nearest dataset with timestamp after 'time'"""

    def get_nearest(self, time: datetime) -> CacheData | None:
        """Get data with  nearest timestamp to 'time'"""
        before = self.get_nearest_before(time)
        after = self.get_nearest_after(time)

        if before and after:
            if abs((before.time - time).total_seconds()) < abs((after.time - time).total_seconds()):
                return before
            return after
        if before:
            return before
        return after

    @abstractmethod
    def __iter__(self) -> CacheIter: ...


class FileCache(Cache):
    """Class for defineing a file for writing and reading data"""

    def __init__(self, file_name: str):
        self.file_name = file_name  # open(file_name, "a+", -1, "UTF-8")
        self._index = self._get_index_at_end_of_file()

    def __iter__(self) -> CacheIter:
        with open(self.file_name, "a+", -1, "UTF-8") as file:
            file.seek(0)
            return FileCacheIter(file.readlines())

    def _get_index_at_end_of_file(self):
        with open(self.file_name, "a+", -1, "UTF-8") as file:
            file.seek(0, io.SEEK_END)
            end = file.tell()
            if end <= 2:
                return 0

            file.seek(end - 2)

            while file.read(1) != "\n":
                new_pos = file.tell() - 2
                if new_pos < 0:
                    return 1
                file.seek(new_pos)
            last = file.read()
            print(last.split("#")[0])
            return int(last.split("#")[0])

    def insert(self, data: CacheData):
        with open(self.file_name, "a+", -1, "UTF-8") as file:
            self._index += 1
            file.seek(0, io.SEEK_END)
            file_data = ";".join([str(x) for x in data.data_list])
            file.write(f"{self._index}#{data.time.strftime(DATE_STRING_FORMAT)}#{file_data}\n")

    def get(self, data_id: int) -> CacheData | None:
        with open(self.file_name, "a+", -1, "UTF-8") as file:
            file.seek(0)
            for line in file.readlines():
                s = line.split("#")
                if int(s[0]) == data_id:
                    return CacheData(data_id, datetime.strptime(s[1], DATE_STRING_FORMAT), s[2].split(";"))
            return None

    def get_nearest_before(self, time: datetime) -> CacheData | None:
        with open(self.file_name, "a+", -1, "UTF-8") as file:
            file.seek(0)
            lines = file.readlines()
            before_line = None
            for line in lines:
                s = line.split("#")
                time_now = datetime.strptime(s[1], DATE_STRING_FORMAT)
                if time <= time_now:
                    if before_line is not None:
                        return CacheData(
                            int(before_line[0]),
                            datetime.strptime(before_line[1], DATE_STRING_FORMAT),
                            before_line[2].split(";"),
                        )

                    return None
            before_line = s
        return None

    def get_nearest_after(self, time: datetime) -> CacheData | None:
        with open(self.file_name, "a+", -1, "UTF-8") as file:
            file.seek(0)
            lines = file.readlines()
            for line in lines:
                s = line.split("#")
                time_now = datetime.strptime(s[1], DATE_STRING_FORMAT)
                if time <= time_now:
                    return CacheData(int(s[0]), time_now, s[2].split(";"))
            return None

    def get_nearest(self, time: datetime) -> CacheData | None:
        with open(self.file_name, "a+", -1, "UTF-8") as file:
            file.seek(0)
            lines = file.readlines()
            lines = iter(lines)
            # lines = lines.__iter__()
            for line in lines:
                s = line.split("#")
                time_now = datetime.strptime(s[1], DATE_STRING_FORMAT)
                if time <= time_now:
                    s_after = next(lines).split("#")
                    # s_after = lines.__next__().split("#")
                    time_after = datetime.strptime(s_after[1], DATE_STRING_FORMAT)

                    if abs((time_after - time).total_seconds() > abs((time_now - time).total_seconds())):
                        return CacheData(int(s[0]), time_now, s[2].split(";"))

                    return CacheData(int(s_after[0]), time_after, s_after[2].split(";"))
            return None


class FileCacheIter(CacheIter):
    """Iterater for cache files"""

    def __init__(self, lines: list[str]):
        self.lines = lines.__iter__()

    def __next__(self) -> CacheData:
        line = self.lines.__next__()
        s = line.split("#")
        return CacheData(int(s[0]), datetime.strptime(s[1], DATE_STRING_FORMAT), s[2].split(";"))
