from time import sleep
import serial

class SmartFan:

	def __init__(self, name='fan', port='/dev/tty.usbmodem1411'):
		# Establish the connection on a specific port
		self.name = name
		self.baudrate = 9600
		if not port: # no port, no physical fan
			self.ser = None
		else:
			self.ser = serial.Serial(port, self.baudrate)

	def off(self):
		if self.ser:
			print "sent off to {}".format(self.name)
			self.ser.write(str(chr(0)))
		else:
			print "would have sent off to {}".format(self.name)

	def low(self):
		if self.ser:
			print "sent low to {}".format(self.name)
			self.ser.write(str(chr(1)))
		else:
			print "would have sent low to {}".format(self.name)

	def med(self):
		if self.ser:
			print "sent med to {}".format(self.name)
			self.ser.write(str(chr(2)))
		else:
			print "would have sent med to {}".format(self.name)

	def high(self):
		if self.ser:
			print "sent high to {}".format(self.name)
			self.ser.write(str(chr(3)))
		else:
			print "would have sent high to {}".format(self.name)
