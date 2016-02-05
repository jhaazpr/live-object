from time import sleep
import serial

class SmartFan:

	def __init__(self, name='fan', port='/dev/tty.usbmodem1411'):
		# Establish the connection on a specific port
		self.name = name
		self.baudrate = 9600
		# self.ser = serial.Serial(port, self.baudrate)

	def off(self):
		print "sent off to {}".format(self.name)
		# self.ser.write(str(chr(0)))

	def low(self):
		print "sent low to {}".format(self.name)
		# self.ser.write(str(chr(1)))

	def med(self):
		print "sent med to {}".format(self.name)
		# self.ser.write(str(chr(2)))

	def high(self):
		print "sent high to {}".format(self.name)
		# self.ser.write(str(chr(3)))
