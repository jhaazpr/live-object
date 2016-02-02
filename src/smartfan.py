from time import sleep
import serial
ser = serial.Serial('/dev/tty.usbmodem1411', 9600) # Establish the connection on a specific port



def off():
	print "sent off"!
	ser.write(str(chr(0))) 
def low():
	print "sent low"!
	ser.write(str(chr(1))) 
def med():
	print "sent med"!
	ser.write(str(chr(2))) 
def high():
	print "sent high!"
	ser.write(str(chr(3))) 
