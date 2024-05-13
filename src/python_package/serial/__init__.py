"""Contains class for serial communicating over ttf"""

# Importing Libraries
from datetime import datetime
import os
import re
import time
import serial
from python_package.serial.serial_exceptions import serial_exceptions
from python_package.cash.cash import FileCache, CacheData
from python_package.args import ARGS as args

BAUDRATE = 9600
COM = "COM3"  # <-----


class SerialCom:
    """Serial comunication class"""

    def __init__(self, log_folder: str = str(args.controler_cache), port=COM, debug=False) -> None:
        self.debug = debug
        self.port = port
        if log_folder == "def":
            os.path.join(os.getcwd(), "")
        self.arduino = serial.Serial()
        self.log_folder = log_folder

    def begin(self) -> None:
        """Starts serial connection"""
        self.arduino = serial.Serial(port=self.port, baudrate=BAUDRATE, timeout=10)

    def write(self, x: str) -> None:
        """Write a bytes package to the connected device, every command ends on a cardinal return"""
        self.arduino.write(bytes(x + "\r", "utf-8"))

    def read(self) -> str:
        """wait for up to 5 seconds on response from connected device,
        either raise an exception or return the first response"""
        timeout = time.time() + 5  # 5 seconds from now
        while self.arduino.in_waiting == 0:
            if time.time() > timeout:
                raise serial_exceptions.Exceptions.NO_RESPONSE
        string = self.arduino.read_until(b"\r").decode()
        string = string.removesuffix("\r")
        if string.find("Error") != -1:
            print("Controller error " + string)
            enum_val = serial_exceptions.ExceptionEnum(self.string_to_int(string)).name
            self.log_error(
                serial_exceptions.Exceptions[enum_val],
                f"Controller error raised: {serial_exceptions.Exceptions[enum_val]}",
            )

        if self.debug:
            print(string)

        return string

    def set_pump(self, value: int) -> None:
        """set pump value for connected device, by sending a value with a prefix 'P',
        raise an exeption if incorrect value is given"""
        r_val = -1
        rtn = self.read_all()

        if value < 0 or value > 100:
            self.log_error(
                serial_exceptions.Exceptions.INCORRECT_INPUT,
                f"Attempted to set pump with value out of bounds[0..100] with value:{value}",
            )
        self.write("P" + str(value))

        for i in rtn:
            if i.find("pump update:") != -1:
                r_val = self.string_to_int(i)
        if r_val != value:
            self.log_error(serial_exceptions.Exceptions.COMUNICATION_ERROR, "Pump update response not recieved")

    def read_sensor(self) -> tuple[int, int]:
        """Sends a msg with the string 'S' which tells the connected device to return sensor readings"""
        self.write("S")
        rtn = self.read_all()
        invariance = -1
        avg_distance = -1
        for string in rtn:
            if string.find("invariance:") != -1:
                invariance = self.string_to_int(string)
            elif string.find("Rvd:") != -1:
                avg_distance = self.string_to_int(string)

        if invariance == -1 or avg_distance == -1:
            self.log_error(
                serial_exceptions.Exceptions.NO_SENSOR_READINGS,
                f"Non-positive values in avg-dist:{avg_distance} and invariance:{invariance}",
            )
        if avg_distance == 0:
            self.log_error(serial_exceptions.Exceptions.SENSOR_READS_ZERO, "The distance sensor reads zero")
        if avg_distance < 30 or avg_distance > 9998:
            self.log_error(
                serial_exceptions.Exceptions.COMUNICATION_ERROR, f"Distance out of bounds for sensor: {avg_distance}"
            )

        return avg_distance, invariance

    def read_all(self) -> list[str]:
        """Wait for up to 5 seconds for response from connected device,
        either throw exception or read all responses into an array"""
        #string_array: list[str] = [self.read()]  # run initial read
        string_array = []
        while self.arduino.in_waiting > 0:  # Repeat read while buffer is not empty
            string_array.append(self.read())
        return string_array

    def string_to_int(self, input_str: str) -> int:
        """Search string for a int, will raise an exception if none is found"""
        res = re.search(r"\d+", input_str)
        if res is not None:
            return int(res.group())

        self.log_error(
            serial_exceptions.Exceptions.CONVERSION_ERROR, "Could not fint int in: " + input_str
        )  # will raise exception
        return -1

    def log_error(self, error: serial_exceptions.Exceptions, msg: str):
        """Write error and communication buffer to file, before throwing exception"""
        now = datetime.now()
        time_now = str(now).replace(":", "..")
        file = FileCache(f"{self.log_folder}/Error-log {error.name} {time_now}")

        data_arr = [msg]
        data = CacheData(0, now, data_arr)
        file.insert(data)
        while self.arduino.in_waiting:
            string = self.arduino.read_until(b"\r").decode().removesuffix("\r")
            data_arr.append(string)
            data = CacheData(0, now, data_arr)
            file.insert(data)
        raise error
