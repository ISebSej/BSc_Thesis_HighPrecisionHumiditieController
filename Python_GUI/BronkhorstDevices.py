import serial
import pygame
import serial

class MainDeviceClass(object):

	All = []

	def __init__(self, init_x, init_y):
		"""Append object to self.All so all devices can be listed globally"""
		self.All.append(self)
		"""Set up UI variables"""
		self.name      = 'Device not found'
		self.loc_x     = init_x
		self.loc_y     = init_y
		self.line1     = ["Status", "Not Found"]
		self.line2     = ["Set massflow", "0"]
		self.line3     = ["Measured flow", "0"]
		self.line4     = ["Label", "0"]
		self.lenline   = 4
		self.spacing   = 100
		self.inittext()
		"""Set up variables for serial communication"""
		self.baud = 38400
		self.isconnect = False
		self.myport    = None
		self.isheater    = False
		
		
	def inittext(self):
		self.txtclr    = (  0,   0,   0)
		self.txtfontsm = pygame.font.SysFont("Ubuntu", 22)
		self.txtfontlr = pygame.font.SysFont("Ubuntu", 44)
		self.txtfontmi = pygame.font.SysFont("Ubuntu", 33)
		self.Line0     = self.txtfontsm.render(self.name, True, self.txtclr)
		self.Line1l    = self.txtfontsm.render(self.line1[0], True, self.txtclr)
		self.Line2l    = self.txtfontsm.render(self.line2[0], True, self.txtclr)
		self.Line3l    = self.txtfontsm.render(self.line3[0], True, self.txtclr)
		self.Line4l    = self.txtfontsm.render(self.line4[0], True, self.txtclr)

	def writetoscreen(self, screen):
		screen.blit(self.Line0, [self.loc_x, self.loc_y - 15])


		if self.lenline > 0:
			screen.blit(self.Line1l, [self.loc_x, self.loc_y + 22])
			self.Line1r = self.txtfontsm.render(self.line1[1], True, self.txtclr)
			screen.blit(self.Line1r, [self.loc_x + self.spacing, self.loc_y + 22])


		if self.lenline > 1:
			screen.blit(self.Line2l, [self.loc_x, self.loc_y + 44])
			self.Line2r = self.txtfontsm.render(self.line2[1], True, self.txtclr)
			screen.blit(self.Line2r, [self.loc_x + self.spacing, self.loc_y + 44])

		if self.lenline > 2:
			screen.blit(self.Line3l, [self.loc_x, self.loc_y + 66])
			self.Line3r = self.txtfontsm.render(self.line3[1], True, self.txtclr)
			screen.blit(self.Line3r, [self.loc_x + self.spacing, self.loc_y + 66])

		if self.lenline > 3:
			screen.blit(self.Line4l, [self.loc_x, self.loc_y + 88])
			self.Line3r = self.txtfontsm.render(self.line3[1], True, self.txtclr)
			screen.blit(self.Line3r, [self.loc_x + self.spacing, self.loc_y + 88])


	def connect(self, port):
		self.isconnect = True
		self.myport    = port
		self.line1[1]  = "Connected"

	def disconnect(self):
		self.isconnect = False
		self.myport    = None
		self.line1[1]  = "Not Connected"

	def getSetpoint(self):
		try:
			with serial.Serial(self.port, self.baud) as ser:
				#test connection, get name, set isconnect = True
				ser.write(':06800401210121\r\n')    #setpoint: read, Process: 1, Parameter: 1, Type: integer
				msg = msg = ser.read_until('\r\n')    #:0680020121 7D00 \r\n measure = hex 7D00 = 32000 = 100%
				"""String manipulation to isolate relevant hex and convert to setpoint"""
				msg = msg.replace(':0680020121', '')
				msg = msg.replace('\r\n', '')
				setp = int(msg, 16) / 32000 * self.maxsetpoint
				self.setpoint = setp
				return self.setpoint

		except serial.SerialTimeoutException:
			print("Port 1 is not connected, check if device is plugged in")
			self.deviceDisconnect(device)
			return self.setpoint

		except serial.SerialException:
			print("Could not find port 1, check if RS232 board is connected")
			self.deviceDisconnect(device)
			return self.setpoint
		pass

	def getMeasure(self):
		try:
			with serial.Serial(self.port, self.baud) as ser:
				#test connection, get name, set isconnect = True
				ser.write(':06800401210120\r\n')    #measure: read, Process: 1, Parameter: 0, Type: integer
				msg = ser.read_until('\r\n')    #::0680020121 7D00 \r\n measure = hex 7D00 = 32000 = 100%
				"""String manipulation to isolate relevant hex and convert to setpoint"""
				msg = msg.replace(':0680020121', '')
				msg = msg.replace('\r\n', '')
				meas = int(msg, 16) / 32000 * self.maxmeasure
				self.measure = meas

		except serial.SerialTimeoutException:
			print("Port 1 is not connected, check if device is plugged in")
			self.disconnect(device)
			pass
		except serial.SerialException:
			print("Could not find port 1, check if RS232 board is connected")
			self.disconnect(device)

	def setSetpoint(self, setpoint):
		try:
			with serial.Serial(self.port, self.baud) as ser:
				msg = str(hex(int(float(setpoint)/self.maxsetpoint*32000)))
				msg = msg.replace('0x', '')
				while not len(msg) == 4:
					msg = '0' + msg

				ser.write(':0680010121{}\r\n'.format(msg))    #read usertag: Process: 113, Parameter: 6, Type: string
				ans  = ser.read_until('\r\n')    #::0680020121 7D00 \r\n measure = hex 7D00 = 32000 = 100%

		except serial.SerialTimeoutException:
			print("Port 1 is not connected, check if device is plugged in")
			self.disconnect()
			pass
		except serial.SerialException:
			print("Could not find port 1, check if RS232 board is connected")
			self.disconnect()
			
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class CoriFlow(MainDeviceClass):
	def __init__(self, init_x, init_y):
		super(CoriFlow, self).__init__(init_x, init_y)
		self.maxsetpoint  = 5
		self.usertag      = ':0D80027166005553455254414700\r\n'
		
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class ElFlow(MainDeviceClass):
	def __init__(self, init_x, init_y):
		super(ElFlow, self).__init__(init_x, init_y)
		self.maxsetpoint  = 5
		self.usertag      = ':0D80027166005553455212314700\r\n'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
		
class Heater(MainDeviceClass):
	def __init__(self, init_x, init_y):
		super(ElFlow, self).__init__(init_x, init_y)
		self.isheater       = True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
	print("Started running in BronkhorstDevices.py")
	#execfile('Main.py')		


