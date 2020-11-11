class SerialMonitor(object)
	
	def __init__(self, myport = '/dev/ttyUSB1', baud = 38400):
		self.name = "Cori"
		try:
			self.serial = serial.Serial(
				port= myport,
				baudrate= baud,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				bytesize=serial.EIGHTBITS
				)
		except:
			print("Port not found")

	def Loopbacktest(self):
		self.serial.open()
		self.serial.isOpen()

		print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

		input=1
		while 1 :
			# get keyboard input
			input = raw_input(">> ")
        		# Python 3 users
        		# input = input(">> ")
			if input == 'exit':
				ser.close()
				exit()
			else:
				# send the character to the device
				# (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
				ser.write(input + '\r\n')
				out = ''
				# let's wait one second before reading output (let's give device time to answer)
				time.sleep(1)
				while ser.inWaiting() > 0:
					out += ser.read(1)
			
				if out != '':
					print ">>" + out