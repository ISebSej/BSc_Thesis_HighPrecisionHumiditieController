import pygame
import pygame.locals as pg
import serial
import time
import button as bt 
import threading
import BronkhorstDevices as bronk
import Queue
import Display_Info as disin
import sys
import glob

"""
Written in Python 2.7.15rc1
		   pygame 1.9.4

"""

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Main(threading.Thread):
	"""The Main thread containing the user interface"""
	bgclr   = 	(176,196,222)

	def __init__(self, name='MainThread'):
		"""Enable to turn off the thread"""
		self._stopevent = threading.Event()

		"""Initialize Game variables"""
		self.screen  = pygame.display.get_surface()
		self.running = True
		self.width   = 800
		self.height  = 600
		self.fps     = 30

		"""Initialize pygame display"""
		pygame.init()
		self.surface = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Humidity Controller')
		self.surface.fill(self.bgclr)

		"""Create temperature and humidity objects"""
		self.Temp  = disin.Display_Info(50, 50, "Temperature", 21, "C")
		self.Humi  = disin.Display_Info(325, 50, "Humidity", 0 , "%")
		self.Mass  = disin.Display_Info(600, 50, "Massflow", 0 , "g/h")

		self.Cori = bronk.CoriFlow(50, 300)
		self.Heat = bronk.ElFlow(325, 300)
		self.Elfl = bronk.MainDeviceClass(600, 300)
		threading.Thread.__init__(self, name=name)


		"""Main content of thread is described here, This function is called by threading.Thread.__init__()"""
	def run(self):
		"""Main loop"""
		while self.running:
			"""Setup for main loop"""
			start = time.time()
			self.surface.fill(self.bgclr)
			"""Draw all Display info objects"""
			for textobject in disin.Display_Info.All:
				textobject.writetoscreen(self.surface)
				textobject.checkIncrement()

			"""Draw all buttons to screen"""
			for button in bt.Button.All:
				button.draw(self.surface)

			"""Draw Device information and status to screen"""
			for device in bronk.MainDeviceClass.All:
				device.writetoscreen(self.surface)

			"""Finalize main loop, makes sure to keep constant framerate self.fps"""
			time.sleep(max(1./self.fps - (time.time() - start), 0))
			pygame.display.update() 

			"""Handles pygame event BUTTONDOWN and QUIT, de/incement is in order to provide smooth scrolling of values"""
			for event in pygame.event.get():
				self.handleQuitEvent(event)
				self.handleButtonEvent(event)
				"""Handle clicking on the screen and check if button is pressed"""

		"""Shutdown, close all threads here"""
		Serialthread.join()
		pygame.quit()

	def join(self, timeout=None):
		""" Stop this thread. """
		self._stopevent.set(  )
		threading.Thread.join(self, timeout)

	def handleButtonEvent(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			for button in bt.Button.All:
				if button.isOver(event.pos) and button.text == 'up':
					button.parent.increment = True
				if button.isOver(event.pos) and button.text == 'down':
					button.parent.decrement = True
		if event.type == pg.MOUSEBUTTONUP:
			for button in bt.Button.All:
				button.parent.increment = False
				button.parent.decrement = False

	def handleQuitEvent(self, event):
		if event.type == pg.QUIT:
			self.running = False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SerialThread(threading.Thread):
	def __init__(self, name='SerialThread'):
		""" constructor, setting initial variables """
		self._stopevent = threading.Event()
		self._sleepperiod = 0.5
		self.findSerialPorts()
		self.ports = ['/dev/ttyUSB1', '/dev/ttyUSB2'] #only for testing, remove later
		threading.Thread.__init__(self, name=name)

	def run(self):
		""" main control loop """
		print "%s starts" % (self.getName(),)

		"""Start serial loop"""
		while not self._stopevent.isSet():
			"""Test connection to instrument"""
			for device in bronk.MainDeviceClass.All:
				if device.isconnect and not device.isheater:
					device.getSetpoint()
					device.getMeasure()
				else:
					"""Runs when devices has not been found, loops through ports to find suitable device"""
					for port in self.ports:
						self.testPort(port, device)

			MainThread.Temp.measure += 1  #for testing, remove later
			time.sleep(1)

		"""Closing Serial thread"""
		print "%s ends" % (self.getName(),)

	def findSerialPorts(self):
		""" Lists serial port names	"""
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		self.ports = result

	def testPort(self, port, device):
		try:
			with serial.Serial(port, device.baud) as ser:
				#test connection, get name, set isconnect = True
				ser.write(':0703047166716600\r\n') #read usertag: Process: 113, Parameter: 6, Type: string
				msg = ser.read_until('\r\n')
				#print(data)
				"""Checks if returned usertag matches devices objects usertag, then sets appropriate variables"""
				if msg == device.usertag: 
					device.connect(port)
				else:
					print("usertag seems to be wrong, please check")

		except serial.SerialTimeoutException:
			print("Port {} is not connected, check if device is plugged in".format(port))
			device.disconnect()
		except serial.SerialException:
			print("Could not find port {}, check if RS232 board is connected".format(port))
			device.disconnect()

	def join(self, timeout=None):
		""" Stop the thread. """
		self._stopevent.set()
		threading.Thread.join(self, timeout)

	# def getSetpoint(self, device):
	# 	try:
	# 		with serial.Serial(device.port, device.baud) as ser:
	# 			#test connection, get name, set isconnect = True
	# 			ser.write(':06800401210121\r\n')    #read usertag: Process: 113, Parameter: 6, Type: string
	# 			data = ser.read_until('\r\n')    #:0680020121 7D00 \r\n measure = hex 7D00 = 32000 = 100%
	# 			"""String manipulation to isolate relevant hex and convert to setpoint"""
	# 			data.replace(':0680020121', '')
	# 			data.replace('\r\n', '')
	# 			setp = int(data, 16) / 32000 * device.maxsetpoint
	# 			device.setpoint = setp
	# 			return setp
	# 	except serial.SerialTimeoutException:
	# 		print("Port 1 is not connected, check if device is plugged in")
	# 		self.deviceDisconnect(device)
	# 		pass
	# 	except serial.SerialException:
	# 		print("Could not find port 1, check if RS232 board is connected")
	# 		self.deviceDisconnect(device)
	# 	pass

	# def getMeasure(self, device):
	# 	try:
	# 		with serial.Serial(device.port, device.baud) as ser:
	# 			#test connection, get name, set isconnect = True
	# 			ser.write(':06800401210120\r\n')    #read usertag: Process: 113, Parameter: 6, Type: string
	# 			data = ser.read_until('\r\n')    #::0680020121 7D00 \r\n measure = hex 7D00 = 32000 = 100%
	# 			"""String manipulation to isolate relevant hex and convert to setpoint"""
	# 			data.replace(':0680020121', '')
	# 			data.replace('\r\n', '')
	# 			setp = int(data, 16) / 32000 * device.maxmeasure
	# 			device.setpoint = setp
	# 			return setp
	# 	except serial.SerialTimeoutException:
	# 		print("Port 1 is not connected, check if device is plugged in")
	# 		self.deviceDisconnect(device)
	# 		pass
	# 	except serial.SerialException:
	# 		print("Could not find port 1, check if RS232 board is connected")
	# 		self.deviceDisconnect(device)


	# def setSetpoint(self, device, setpoint):
	# 	try:
	# 		with serial.Serial(device.port, device.baud) as ser:
	# 			#test connection, get name, set isconnect = True
	# 			ser.write(':06800401210120\r\n')    #read usertag: Process: 113, Parameter: 6, Type: string
	# 			data = ser.read_until('\r\n')    #::0680020121 7D00 \r\n measure = hex 7D00 = 32000 = 100%
	# 			"""String manipulation to isolate relevant hex and convert to setpoint"""
	# 			data.replace(':0680020121', '')
	# 			data.replace('\r\n', '')
	# 			setp = int(data, 16) / 32000 * device.maxmeasure
	# 			device.setpoint = setp
	# 			return setp
	# 	except serial.SerialTimeoutException:
	# 		print("Port 1 is not connected, check if device is plugged in")
	# 		self.deviceDisconnect(device)
	# 		pass
	# 	except serial.SerialException:
	# 		print("Could not find port 1, check if RS232 board is connected")
	# 		self.deviceDisconnect(device)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
	print("Started running program")
	print("Initialize serial queue")

	serialq = Queue.Queue()
	lock = threading.Lock()
	count = 0

	print("Create Mainthread")
	MainThread = Main()
	print("Create SerialThread")
	Serialthread = SerialThread()

	MainThread.daemon = False
	Serialthread.deamon = False
	print("starting Application")
	MainThread.start()
	Serialthread.start()

	for item in range(1,30):
		serialq.put(item)