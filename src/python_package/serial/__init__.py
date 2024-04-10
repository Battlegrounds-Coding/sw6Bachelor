# Importing Libraries 
import serial 
import time 

BAUDRATE =  9600
COM = "COM3" #<-----

arduino = serial.Serial(port=COM, baudrate=BAUDRATE, timeout=10) 
def write_read(x): 
	arduino.write(bytes(x + '\r', 'utf-8'))
	arduino.write(bytes(" test 2" + '\r', 'utf-8'))

	# arduino.write(x)
	time.sleep(0.3)
	# data = arduino.readline() 
	while(arduino.in_waiting) :
		print(arduino.read_until(b'\r')) #read all lines
	return  
while True: 
	num = input("Enter a number: ") # Taking input from user a
	value = write_read(num) 
	# print(value) # printing the value 
