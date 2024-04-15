"""Contains class for serial communicating over ttf"""

# Importing Libraries
import time
import serial
from python_package.serial.serial_exceptions import serial_exceptions

BAUDRATE = 9600
COM = "COM3"  # <-----


class SerialCom:
    """Serial comunication class"""

    arduino = serial.Serial(port=COM, baudrate=BAUDRATE, timeout=10)

    def __init__(self, debug=True) -> None:
        self.debug = debug

    def write(self, x: str) -> None:
        """Write a bytes package to the connected device, every command ends on a cardinal return"""
        self.arduino.write(bytes(x + "\r", "utf-8"))

    def read(self) -> str:
        """wait for up to 5 seconds on response from connected device,
        either raise an exception or return the first response"""
        timeout = time.time() + 5  # 5 seconds from now
        while not self.arduino.in_waiting:
            if time.time() > timeout:
                raise serial_exceptions.exceptions.NO_RESPONSE
        string = self.arduino.read_until(b"\r").decode()
        if self.debug:
            print(string)

        return string

    def set_pump(self, value: int) -> None:
        """set pump value for connected device, by sending a value with a prefix 'P',
        raise an exeption if incorrect value is given"""

        self.write("P" + str(value))
        rtn = self.read_all()
        if rtn.pop(-1) == "Please apply a new value:":
            print("Invalid value, Out of bounds [0..255]")
            raise serial_exceptions.exceptions.PUMP_VALUE_OUT_OF_BOUNDS

    def read_sensor(self) -> int:
        """Sends a msg with the string 'S' which tells the connected device to return sensor readings"""
        self.write("S")
        return int(self.read_all().pop(-1))

    def read_all(self) -> list[str]:
        """Wait for up to 5 seconds for response from connected device,
        either trhow exception or read all responses into an array"""
        string_array: list[str] = []
        timeout = time.time() + 5  # 5 seconds from now
        while not self.arduino.in_waiting:
            if time.time() > timeout:
                raise serial_exceptions.exceptions.NO_RESPONSE

        while self.arduino.in_waiting:
            string = self.arduino.read_until(b"\r").decode()
            if self.debug:
                print(string)  # print all lines
            string_array.append(string)
        return string_array

    # def write_read(self, x):
    #     self.write(x)
    #     self.write(" test 2")

    #     # arduino.write(x)
    #     time.sleep(0.3)
    #     # data = arduino.readline()
    #     while self.arduino.in_waiting:
    #         print(self.arduino.read_until(b"\r"))  # read all lines
    #     return

    # while True:
    # 	num = input("Enter a number: ") # Taking input from user a
    # 	value = write_read(num)
    # 	# print(value) # printing the value
