# Importing Libraries 
import serial 
import time 

BAUDRATE =  9600
COM = "COM4" #<-----

arduino = serial.Serial(port=COM, baudrate=BAUDRATE, timeout=10) 
def write_read(x): 
	arduino.write(bytes(x, 'utf-8'))
	time.sleep(0.05)
	data = arduino.readline() 
	return data 
while True: 
	num = input("Enter a number: ") # Taking input from user 
	value = write_read(num) 
	print(value) # printing the value 
